# -*- coding: utf-8 -*-
"""stage_campaign — turn a cleaned recipients-with-copy CSV into a 3-step,
per-prospect Woodpecker DRAFT and load everyone in. NEVER sends.

This packages the proven, verified path so the agent does NOT have to re-derive
the Woodpecker schema each time (it took several HTTP 400s to learn the exact
snippet-token syntax). Use it after you have a CSV with, per row:
    email, snippet1, snippet2, snippet3   (+ optional first_name/last_name/company/title)
where snippet1/2/3 are this prospect's Warm InMail 1, Warm InMail 2 and Direct InMail.

It builds a START -> EMAIL -> EMAIL -> EMAIL sequence whose three step bodies render
{{SNIPPET_1|2|3}} (each prospect's own copy), with Woodpecker's auto-unsubscribe on,
from an allow-listed warmed SECONDARY mailbox only. Dry-run unless --commit. There is
STILL no send verb anywhere — a human opens the draft and presses Run.

Run from tools/ :  python -m leadgen.stage_campaign --recipients r.csv --mailbox 779855 [--commit]
"""
import os, csv, io, json, uuid, re

# Woodpecker snippet token syntax is exact (verified live): {{SNIPPET_n | "fallback"}}
#  - underscore in the name, spaces around the pipe, fallback in DOUBLE quotes.
# The prospect FIELD stays snippet1/2/3 (no underscore). Mismatched syntax -> HTTP 400
# "incorrect snippet, snippet fallback or spintax elements".
FALLBACKS = (
    "Hi, I'm reaching out from Iksula. We help finance leaders at mid-market companies get cleaner "
    "commerce and financial visibility without adding headcount. Worth a 20-minute call?",
    "Following up from Iksula - happy to share a relevant example if a short conversation makes sense.",
    "Hi, I'm from Iksula. We help finance teams consolidate and report across their business. "
    "Could we find 20 minutes?",
)
DEFAULT_SUBJECTS = (
    "A finance and commerce idea for {{COMPANY}}",
    "Re: a finance and commerce idea for {{COMPANY}}",
    "{{FIRST_NAME}}, worth 20 minutes?",
)
DEFAULT_DELAYS = (3, 4, 1)   # days to the next step (last is ignored)


def _footer(sender_name="[Sender Name]", sender_title="[Title]", postal_address=None):
    """The uniform signature appended after each personalized body. The copy itself is stripped of
    its own sign-off (see strip_signoff) so this is the ONE signature. Woodpecker auto-appends the
    unsubscribe link (gdpr_unsubscribe).

    postal_address: a valid physical postal address is a CAN-SPAM REQUIREMENT for US commercial
    email. If given, it renders as the address line; if None, the line is omitted — which is NOT
    CAN-SPAM compliant, so `stage`/`main` warn when it's absent."""
    sig = sender_name + ((", " + sender_title) if sender_title else "")
    footer = ('<p style="margin:18px 0 0 0">--<br>%s<br>'
              'Iksula | <a href="https://www.iksula.com">iksula.com</a></p>') % sig
    if postal_address:
        footer += ('<p style="font-size:11px;color:#888888;margin:10px 0 0 0">Iksula &mdash; %s</p>'
                   % postal_address)
    return footer


FOOTER = _footer()   # default (placeholder sender); kept as the module-level default

# Valedictions that mark the start of a hand-written sign-off in outreach copy. Because the
# template appends its own signature, we strip the copy's sign-off to avoid a DOUBLE signature
# (and a name clash with the sending mailbox).
_VALEDICTIONS = frozenset((
    "best", "best regards", "regards", "kind regards", "warm regards", "warmest regards",
    "best wishes", "thanks", "thank you", "many thanks", "cheers", "sincerely", "yours",
    "yours sincerely", "all the best", "warmly", "talk soon", "speak soon",
))


def strip_signoff(text):
    """Remove a trailing hand-written sign-off ('Best,\\nRohit - Iksula', 'Regards,\\n...') from
    outreach copy so it doesn't collide with the template's signature. Conservative: only cuts
    when a valediction appears on its OWN line within the last few lines (won't touch a 'Thanks'
    that's mid-sentence, and leaves sign-off-less copy untouched). Copy already rendered with
    <br> tags is left to the author (respected as-is)."""
    raw = str(text or "")
    if "<br" in raw.lower() or not raw.strip():
        return raw
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").rstrip().split("\n")
    cut = None
    for i in range(len(lines) - 1, max(-1, len(lines) - 7), -1):  # scan only the tail
        w = lines[i].strip().rstrip(",.!").lower()
        if w in _VALEDICTIONS:
            cut = i
            break
    if cut is not None:
        lines = lines[:cut]
    return "\n".join(lines).rstrip()


def strip_subject_line(text):
    """Remove a leading 'Subject: ...' line that some copy authors embed at the top of the message
    body. The subject is a SEPARATE field — left in the body it renders as literal text. Copy already
    rendered with <br> tags is respected as-is."""
    raw = str(text or "")
    if "<br" in raw.lower() or not raw.strip():
        return raw
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").lstrip("\n ").split("\n")
    if lines and re.match(r'(?i)^\s*subject\s*(line)?\s*:', lines[0]):
        lines = lines[1:]
        while lines and not lines[0].strip():   # drop the blank line under it
            lines = lines[1:]
    return "\n".join(lines)


def _split_sentences(t):
    """Conservative sentence split: break on . ? ! followed by whitespace + a capital or an
    opening quote. Won't split '15-25%', mid-sentence en-dashes, or decimals."""
    parts = re.split(r'(?<=[.?!])\s+(?=[A-Z"“‘])', t)
    return [p.strip() for p in parts if p.strip()]


def paragraphize(text):
    """Make outreach copy render as readable paragraphs in an HTML email instead of a wall of
    text. The key fact (verified live): Woodpecker COLLAPSES raw newlines when it renders a
    snippet into an HTML body, so an author's `\\n\\n` paragraph breaks disappear in the inbox.
    So:
      * copy that already has explicit <br> tags -> returned unchanged (idempotent);
      * copy with newline structure -> the author's breaks are preserved by converting blank
        lines to <br><br> (paragraph gap) and single newlines to <br> (line break, e.g. a
        two-line sign-off);
      * a single unbroken blob (no newlines) -> segmented by sentence into greeting/hook, body,
        and a trailing CTA question, joined with <br><br>.
    Introduces no template-breaking chars ({{ }} |)."""
    raw = str(text or "")
    if not raw.strip():
        return ""
    if "<br" in raw.lower():                     # author already formatted it — don't second-guess
        return raw.strip()
    t = raw.replace("\r\n", "\n").replace("\r", "\n")
    if "\n" in t:                                # preserve the author's own line/paragraph breaks
        paras = re.split(r'\n[ \t]*\n', t)
        out = ["<br>".join(seg.strip() for seg in p.split("\n") if seg.strip())
               for p in paras if p.strip()]
        return "<br><br>".join(out)
    sents = _split_sentences(t)                  # single blob: derive paragraphs by sentence
    if len(sents) <= 1:                          # nothing to break
        return t
    head, rest = sents[0], sents[1:]
    cta = None
    if rest and rest[-1].endswith("?"):
        cta, rest = rest[-1], rest[:-1]
    paras = [head]
    if rest:
        paras.append(" ".join(rest))
    if cta:
        paras.append(cta)
    return "<br><br>".join(paras)


def _lower_map(row):
    return {str(k).strip().lower(): (v if v is not None else "") for k, v in row.items()}


def _read_recipients(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = [_lower_map(r) for r in csv.DictReader(f)]
    if not rows:
        raise ValueError("recipients CSV is empty")
    need = ("email", "snippet1", "snippet2", "snippet3")
    missing = [c for c in need if c not in rows[0]]
    if missing:
        raise ValueError("recipients CSV missing column(s): %s (need email + snippet1/2/3)" % ", ".join(missing))
    return rows


def validate(rows):
    """Return (ok_rows, problems). Drops rows with an empty/unsafe snippet."""
    ok, problems = [], []
    for i, r in enumerate(rows):
        e = (r.get("email") or "").strip().lower()
        if not e:
            problems.append((i, "<no-email>", "no email")); continue
        bad = None
        for k in ("snippet1", "snippet2", "snippet3"):
            v = (r.get(k) or "").strip()
            if not v:
                bad = "%s empty" % k; break
            if "{{" in v or "}}" in v or "|" in v:
                bad = "%s has a template-breaking char ({{ }} or |)" % k; break
        if bad:
            problems.append((i, e, bad)); continue
        ok.append(r)
    return ok, problems


def _steps_spec(subjects, delays, footer=None):
    footer = footer or FOOTER
    def body(n):
        # The snippet carries its own <br><br> paragraph breaks (see paragraphize); wrapping it
        # in a <div> with a set line-height renders those as readable paragraphs rather than a wall.
        return ('<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;'
                'line-height:1.6;color:#222222">'
                '<div>{{SNIPPET_%d | "%s"}}</div>%s</div>') % (n, FALLBACKS[n - 1], footer)
    return [{"subject": subjects[i], "message": body(i + 1), "days_to_next": delays[i]} for i in range(3)]


def _split_body(text):
    """Clean copy (drop an embedded 'Subject:' line + the trailing sign-off) and split it into
    single-line paragraphs — one per <p> in the template. CRITICAL (verified live 1 Jul 2026):
    Woodpecker FLATTENS any HTML inside a snippet VALUE to plain text and then collapses newlines
    on render, so paragraph structure CANNOT live inside a single snippet — it must live in the
    message template as real <p> tags, with one snippet per paragraph."""
    clean = strip_signoff(strip_subject_line(text)).replace("\r\n", "\n").replace("\r", "\n")
    return [re.sub(r'\s*\n\s*', ' ', p).strip()
            for p in re.split(r'\n[ \t]*\n', clean) if p.strip()]


def _allocate_slots(counts, budget=15):
    """counts = the max paragraph count seen per step. Return per-step snippet slots summing to
    <= budget (Woodpecker allows snippet1..15), trimming the largest step first — its overflow
    paragraphs get merged into its last slot."""
    slots = [max(1, int(c)) for c in counts]
    while sum(slots) > budget:
        slots[slots.index(max(slots))] -= 1
    return slots


def _prospect_snippets(messages, slots):
    """Global snippet1..N dict for one prospect: each step's body is split into its slot count
    (overflow paragraphs merged into the last slot; shorter bodies padded with '')."""
    snips = {}; idx = 1
    for msg, k in zip(messages, slots):
        paras = _split_body(msg)
        if len(paras) > k:                       # merge overflow into the last slot
            paras = paras[:k - 1] + [" ".join(paras[k - 1:])]
        for j in range(k):
            snips["snippet%d" % idx] = paras[j] if j < len(paras) else ""
            idx += 1
    return snips


def _steps_spec_paragraphed(subjects, delays, slots, footer):
    """3-step spec that renders each step's paragraph-snippets as SEPARATE <p> blocks in the
    MESSAGE (message HTML renders faithfully; snippet HTML does not). One <p> per paragraph."""
    specs = []; start = 1
    for i in range(3):
        blocks = "".join('<p>{{SNIPPET_%d | " "}}</p>' % (start + j) for j in range(slots[i]))
        msg = ('<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;'
               'line-height:1.6;color:#222222">%s%s</div>') % (blocks, footer)
        specs.append({"subject": subjects[i], "message": msg, "days_to_next": delays[i]})
        start += slots[i]
    return specs


def stage(recipients_csv, mailbox, name=None, commit=False, timezone="US/Eastern",
          daily_enroll=50, subjects=DEFAULT_SUBJECTS, delays=DEFAULT_DELAYS, batch=100,
          sender_name=None, sender_title=None, postal_address=None):
    """Build the 3-step DRAFT and enroll. Returns a summary dict. Never sends.

    Each prospect's three messages are split into paragraphs; the template renders one <p> per
    paragraph (personalized by one plain-text snippet each) so the email reads as paragraphs, not
    a wall — the ONLY approach that survives Woodpecker flattening snippet-internal HTML."""
    from . import sheet_to_ready as s2r
    from .wp_client import WoodpeckerClient
    import datetime
    rows = _read_recipients(recipients_csv)
    msgs = [[(r.get("snippet%d" % i) or "") for i in (1, 2, 3)] for r in rows]
    max_counts = [max((len(_split_body(m[i])) for m in msgs), default=1) or 1 for i in range(3)]
    slots = _allocate_slots(max_counts)

    ready, problems = [], []
    for idx, r in enumerate(rows):
        e = (r.get("email") or "").strip().lower()
        if not e:
            problems.append((idx, "<no-email>", "no email")); continue
        body = [(r.get("snippet%d" % i) or "") for i in (1, 2, 3)]
        if not all(b.strip() for b in body):
            problems.append((idx, e, "missing one of the 3 messages")); continue
        snips = _prospect_snippets(body, slots)
        bad = next((k for k, v in snips.items() if "{{" in v or "}}" in v or "|" in v), None)
        if bad:
            problems.append((idx, e, "%s has a template-breaking char ({{ }} or |)" % bad)); continue
        row = {"email": e, "first_name": r.get("first_name", ""), "last_name": r.get("last_name", ""),
               "company": r.get("company", ""), "title": r.get("title", "")}
        row.update(snips)
        ready.append(row)
    if not ready:
        return {"ok": False, "reason": "no valid recipients", "problems": problems}

    dry = not commit
    run_id = uuid.uuid4().hex[:8]
    name = name or ("[LG-AGENT] CFO 3-step " + run_id)
    created = datetime.datetime.now(datetime.timezone.utc).isoformat()
    footer = _footer(sender_name or "[Sender Name]", sender_title or "[Title]", postal_address)
    draft = s2r.build_sequence_draft(name, str(mailbox),
                                     _steps_spec_paragraphed(subjects, delays, slots, footer),
                                     run_id=run_id, created_at_utc=created, dry_run=dry,
                                     timezone=timezone, daily_enroll=daily_enroll)
    cid = draft["campaign_id"]
    client = WoodpeckerClient(dry_run=dry)
    enrolled = 0
    for i in range(0, len(ready), batch):
        en = client.enroll_to_draft(cid, ready[i:i + batch])
        enrolled += en["enrolled"]
    return {"ok": True, "campaign_id": cid, "status": draft["status"], "dry_run": dry,
            "enrolled": enrolled, "dropped": len(problems), "problems": problems[:10], "name": name,
            "slots": slots, "has_postal_address": bool(postal_address)}


def main(argv=None):
    import argparse, sys
    from .wp_client import ForbiddenAction, WoodpeckerError
    ap = argparse.ArgumentParser(description="Stage a 3-step per-prospect Woodpecker DRAFT (never sends).")
    ap.add_argument("--recipients", required=True, help="CSV with email + snippet1/2/3 (per-prospect copy)")
    ap.add_argument("--mailbox", required=True, help="warmed, allow-listed SECONDARY-domain mailbox id (e.g. 779855)")
    ap.add_argument("--name", help="campaign name (default '[LG-AGENT] CFO 3-step <id>')")
    ap.add_argument("--commit", action="store_true", help="write to the LIVE account; without it, runs DRY")
    ap.add_argument("--timezone", default="US/Eastern")
    ap.add_argument("--daily-enroll", type=int, default=50)
    ap.add_argument("--sender-name", help="fills the signature (else '[Sender Name]'); should match the mailbox owner")
    ap.add_argument("--sender-title", help="fills the signature title (else '[Title]')")
    ap.add_argument("--postal-address", help="physical postal address for the footer (CAN-SPAM requirement for "
                                             "US commercial email); omitted if not given")
    args = ap.parse_args(argv)
    try:
        s = stage(args.recipients, args.mailbox, name=args.name, commit=args.commit,
                  timezone=args.timezone, daily_enroll=args.daily_enroll,
                  sender_name=args.sender_name, sender_title=args.sender_title,
                  postal_address=args.postal_address)
    except (ForbiddenAction, WoodpeckerError, ValueError) as e:
        print("REFUSED/FAILED: %s" % e); return 2
    if not s["ok"]:
        print("Not staged: %s" % s["reason"])
        for i, e, why in s.get("problems", [])[:10]:
            print("  row %d (%s): %s" % (i, e, why))
        return 2
    print(json.dumps({k: s[k] for k in ("campaign_id", "status", "dry_run", "enrolled", "dropped", "name", "slots")}, indent=2))
    if s["dropped"]:
        print("dropped %d row(s) for empty/unsafe copy (first few):" % s["dropped"])
        for i, e, why in s["problems"]:
            print("  row %d (%s): %s" % (i, e, why))
    if not s.get("has_postal_address"):
        print("\nWARNING: no --postal-address set, so the footer has NO physical postal address. A valid postal")
        print("address is a CAN-SPAM requirement for US commercial email; sending without one is non-compliant.")
    print("\nNEXT (human): open the draft in Woodpecker, send a test to yourself, confirm the unsubscribe link,")
    print("then press Run on a warmed mailbox in a ramp. The agent does NOT send. This path checks data hygiene")
    print("only — you own lawful basis, the postal address, and unsubscribe.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
