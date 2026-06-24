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
import os, csv, io, json, uuid

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
FOOTER = ('<p>--<br>[Sender Name], [Title]<br>Iksula | <a href="https://www.iksula.com">iksula.com</a></p>'
          '<p style="font-size:11px;color:#888888">Iksula &mdash; [REGISTERED POSTAL ADDRESS REQUIRED '
          'BEFORE SEND]</p>')


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
            if "{{" in v or "}}" in v or "|" in v or '"' in v:
                bad = "%s has a template-breaking char ({{ }} | or \")" % k; break
        if bad:
            problems.append((i, e, bad)); continue
        ok.append(r)
    return ok, problems


def _steps_spec(subjects, delays):
    def body(n):
        return '<div><p>{{SNIPPET_%d | "%s"}}</p>%s</div>' % (n, FALLBACKS[n - 1], FOOTER)
    return [{"subject": subjects[i], "message": body(i + 1), "days_to_next": delays[i]} for i in range(3)]


def stage(recipients_csv, mailbox, name=None, commit=False, timezone="US/Eastern",
          daily_enroll=50, subjects=DEFAULT_SUBJECTS, delays=DEFAULT_DELAYS, batch=100):
    """Build the 3-step DRAFT and enroll. Returns a summary dict. Never sends."""
    from . import sheet_to_ready as s2r
    from .wp_client import WoodpeckerClient
    import datetime
    rows = _read_recipients(recipients_csv)
    ok, problems = validate(rows)
    if not ok:
        return {"ok": False, "reason": "no valid recipients", "problems": problems}

    dry = not commit
    run_id = uuid.uuid4().hex[:8]
    name = name or ("[LG-AGENT] CFO 3-step " + run_id)
    created = datetime.datetime.now(datetime.timezone.utc).isoformat()
    draft = s2r.build_sequence_draft(name, str(mailbox), _steps_spec(subjects, delays),
                                     run_id=run_id, created_at_utc=created, dry_run=dry,
                                     timezone=timezone, daily_enroll=daily_enroll)
    cid = draft["campaign_id"]
    client = WoodpeckerClient(dry_run=dry)
    enrolled = 0
    for i in range(0, len(ok), batch):
        en = client.enroll_to_draft(cid, ok[i:i + batch])
        enrolled += en["enrolled"]
    return {"ok": True, "campaign_id": cid, "status": draft["status"], "dry_run": dry,
            "enrolled": enrolled, "dropped": len(problems), "problems": problems[:10], "name": name}


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
    args = ap.parse_args(argv)
    try:
        s = stage(args.recipients, args.mailbox, name=args.name, commit=args.commit,
                  timezone=args.timezone, daily_enroll=args.daily_enroll)
    except (ForbiddenAction, WoodpeckerError, ValueError) as e:
        print("REFUSED/FAILED: %s" % e); return 2
    if not s["ok"]:
        print("Not staged: %s" % s["reason"])
        for i, e, why in s.get("problems", [])[:10]:
            print("  row %d (%s): %s" % (i, e, why))
        return 2
    print(json.dumps({k: s[k] for k in ("campaign_id", "status", "dry_run", "enrolled", "dropped", "name")}, indent=2))
    if s["dropped"]:
        print("dropped %d row(s) for empty/unsafe copy (first few):" % s["dropped"])
        for i, e, why in s["problems"]:
            print("  row %d (%s): %s" % (i, e, why))
    print("\nNEXT (human): open the draft in Woodpecker, add the real postal address to the footer, send a")
    print("test to yourself, confirm the unsubscribe link, then press Run on a warmed mailbox in a ramp.")
    print("The agent does NOT send. This path checks data hygiene only — you own lawful basis + unsubscribe.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
