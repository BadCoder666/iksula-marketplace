# -*- coding: utf-8 -*-
"""sheet_to_ready — turn a raw recipient sheet + email copy into a cleaned,
de-duplicated, suppression-scrubbed, merge-VALIDATED package a human can import into
Woodpecker and send.

This is the "AI preps, a human presses send" path (Option A). It deliberately does
NOT send and does NOT enrol prospects via the agent — so it is safe by construction
and needs none of the live-send prerequisites (warmed mailbox / recorded lawful
basis). The human who imports the list and clicks send owns that decision and the
compliance hygiene (unsubscribe, basis) — exactly like the manual process today, but
with the agent doing the tedious, error-prone prep:

  * normalise + validate emails, drop bad rows
  * de-duplicate by email
  * scrub against a suppression list (existing clients / opt-outs you provide)
  * run the merge-preview so a broken {{field}} never reaches anyone
  * write a clean `recipients_ready.csv` + the copy + a READY_SUMMARY.md

Optionally (--build-draft) it can also create the Woodpecker DRAFT campaign shell via
the create-only client (never auto-sends; dry-run unless you explicitly commit).
"""
import os, csv, io, json, re
from . import merge_preview

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_EMAIL_KEYS = ("email", "email address", "e-mail", "email_address", "emailaddress")


def _norm(e):
    return (e or "").strip().lower()


def _read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _email_key(fieldnames):
    for k in (fieldnames or []):
        if k and k.strip().lower() in _EMAIL_KEYS:
            return k
    return None


def clean(rows, suppress_set):
    """Return (kept_rows, email_key, stats). Drops bad/duplicate/suppressed emails."""
    if not rows:
        raise ValueError("the recipient sheet is empty")
    ekey = _email_key(rows[0].keys())
    if not ekey:
        raise ValueError("no email column found — add a column named 'email'")
    seen, kept = set(), []
    bad = dupe = suppressed = 0
    for r in rows:
        e = _norm(r.get(ekey))
        if not e or not _EMAIL_RE.match(e):
            bad += 1; continue
        if e in suppress_set:
            suppressed += 1; continue
        if e in seen:
            dupe += 1; continue
        seen.add(e)
        r = dict(r); r[ekey] = e
        kept.append(r)
    stats = {"total": len(rows), "kept": len(kept),
             "dropped_bad_email": bad, "dropped_duplicate": dupe, "dropped_suppressed": suppressed}
    return kept, ekey, stats


def build_package(recipients_csv, subject, body, suppress_csv=None, out_dir="ready_package"):
    """Build the ready-to-send package. Returns a summary dict; writes files to out_dir."""
    rows = _read_csv(recipients_csv)
    suppress_set = set()
    if suppress_csv:
        srows = _read_csv(suppress_csv)
        sk = _email_key(srows[0].keys()) if srows else None
        if sk:
            suppress_set = {_norm(x.get(sk)) for x in srows}
    kept, ekey, stats = clean(rows, suppress_set)
    mp = merge_preview.validate(body, kept, subject=subject)

    if stats["kept"] == 0:
        verdict = "NOT READY — no valid recipients left after cleaning"
    elif not mp["clean"]:
        verdict = "NOT READY — fix the merge fields (a {{field}} would render literally)"
    else:
        verdict = "READY — a human can import recipients_ready.csv into Woodpecker and send"

    os.makedirs(out_dir, exist_ok=True)
    rec_path = os.path.join(out_dir, "recipients_ready.csv")
    if kept:
        with io.open(rec_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(kept[0].keys()))
            w.writeheader(); w.writerows(kept)
    copy_path = os.path.join(out_dir, "email_copy.txt")
    io.open(copy_path, "w", encoding="utf-8").write("SUBJECT: %s\n\n%s\n" % (subject.strip(), body.strip()))

    summary = {
        "verdict": verdict,
        "ready": verdict.startswith("READY"),
        "recipients": stats,
        "merge_preview": {"clean": mp["clean"], "fields": mp["fields"],
                          "leaking_count": mp["leaking_count"], "leaking_rows": mp["leaking_rows"][:10]},
        "outputs": {"recipients_ready_csv": rec_path if kept else None, "email_copy": copy_path},
    }
    io.open(os.path.join(out_dir, "READY_SUMMARY.md"), "w", encoding="utf-8").write(_render(summary))
    return summary


def _render(s):
    st = s["recipients"]; mp = s["merge_preview"]
    out = []
    out.append("# Ready-to-send summary\n")
    out.append("**Verdict: %s**\n" % s["verdict"])
    out.append("## Recipients")
    out.append("| | count |")
    out.append("|---|---|")
    out.append("| In the sheet | %d |" % st["total"])
    out.append("| **Ready to send** | **%d** |" % st["kept"])
    out.append("| Dropped — bad/blank email | %d |" % st["dropped_bad_email"])
    out.append("| Dropped — duplicate | %d |" % st["dropped_duplicate"])
    out.append("| Dropped — on suppression list (existing clients / opt-outs) | %d |" % st["dropped_suppressed"])
    out.append("\n## Merge-field check")
    if mp["clean"]:
        out.append("Clean — every personalization field (%s) resolves for every recipient." %
                   (", ".join("{{%s}}" % f for f in mp["fields"]) or "none"))
    else:
        out.append("**%d row(s) would leak a literal {{field}}** — fix before sending:" % mp["leaking_count"])
        for r in mp["leaking_rows"]:
            out.append("- row %s (%s): %s" % (r["row_index"], r.get("email", "?"), ", ".join(r["leaked_fields"])))
    out.append("\n## Next steps (human)")
    out.append("1. Open Woodpecker, create the campaign with the copy in `email_copy.txt` (or use `--build-draft`).")
    out.append("2. Import `recipients_ready.csv` as the prospect list (or use `--enroll`).")
    out.append("3. Review, then press send.")
    out.append("\n> **You (the sender) own compliance for this send.** This tool checked **data hygiene** "
               "(valid emails, no duplicates, your suppression list, merge fields) — it did **NOT** check "
               "**lawful basis**. Before you send, make sure you have permission / legitimate interest to "
               "email these people, a working **unsubscribe** is included, and you're sending from a mailbox "
               "you're happy to send this volume from.")
    out.append("\n*Prepared by the Lead Gen agent — it cleaned, de-duplicated and validated the list; it did not send anything. The send is a human decision.*")
    return "\n".join(out) + "\n"


# ---- optional: also create the Woodpecker DRAFT shell (create-only, never sends) ----
def build_draft(name, mailbox_id, subject, message_html, run_id=None, created_at_utc=None,
                dry_run=True, timezone="Asia/Kolkata", daily_enroll=50):
    """Create the Woodpecker DRAFT campaign shell via the create-only client (NEVER sends).
    `message_html` is the email body (HTML); `mailbox_id` must be an allow-listed, warmed,
    secondary-domain mailbox (never primary/live). Recipients are NOT enrolled here — a human
    imports them into the draft and presses send. Verified against the v2 schema 2026-06-23."""
    import uuid
    from .wp_client import WoodpeckerClient
    settings = {
        "timezone": timezone, "prospect_timezone": False, "daily_enroll": daily_enroll,
        "gdpr_unsubscribe": False, "list_unsubscribe": False,
        "open_disabled_list": [], "auto_pause_prospect_from_domain_statuses": [],
        "catch_all_verification_mode": "BALANCED",
    }
    steps = {  # NOTE: v2 'steps' is a single nested object, not an array
        "id": str(uuid.uuid4()), "type": "START",
        "followup": {
            "id": str(uuid.uuid4()), "type": "EMAIL",
            "delivery_time": {d: [{"from": "09:00", "to": "18:00"}] for d in
                              ("MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY")},
            "body": {"versions": [{"version": "A", "subject": subject, "message": message_html,
                                   "signature": "SENDER", "track_opens": True}]},
            "followup": None,
        },
    }
    c = WoodpeckerClient(dry_run=dry_run)
    return c.create_campaign(name, mailbox_id, settings, steps, run_id=run_id, created_at_utc=created_at_utc)


def build_sequence_draft(name, mailbox_id, steps_spec, run_id=None, created_at_utc=None,
                         dry_run=True, timezone="US/Eastern", daily_enroll=50):
    """Create a MULTI-STEP Woodpecker DRAFT (a follow-up sequence) via the create-only client.

    `steps_spec` is a list of dicts, one per EMAIL touch, in order:
        {"subject": str, "message": html, "days_to_next": int}
    `days_to_next` is the gap (in days) until the NEXT touch (ignored on the last step).
    The bodies typically reference per-prospect snippets ({{SNIPPET1}}..) so each prospect
    carries their own copy. Schema mirrors a live v2 campaign (verified 2026-06-24):
    steps = START -> EMAIL(followup_after) -> EMAIL ... ; never sends (DRAFT)."""
    import uuid
    from .wp_client import WoodpeckerClient
    WEEKDAYS = ("MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY")
    settings = {
        "timezone": timezone, "prospect_timezone": False, "daily_enroll": daily_enroll,
        "gdpr_unsubscribe": True, "list_unsubscribe": True,   # Woodpecker auto-appends a compliant unsubscribe link
        "open_disabled_list": [], "auto_pause_prospect_from_domain_statuses": [],
        "auto_pause_prospect_from_domain": None, "catch_all_verification_mode": "BALANCED",
        "count_followup_delay_in_working_days": True,
    }

    def email_step(spec, followup):
        return {
            "id": str(uuid.uuid4()), "type": "EMAIL",
            "followup_after": {"range": "DAY", "value": int(spec.get("days_to_next", 1))},
            "delivery_time": {d: [{"from": "09:00", "to": "18:00"}] for d in WEEKDAYS},
            "body": {"versions": [{"id": str(uuid.uuid4()), "version": "A",
                                   "subject": spec["subject"], "message": spec["message"],
                                   "signature": "SENDER", "track_opens": True}]},
            "followup": followup,
        }

    followup = None
    for spec in reversed(steps_spec):              # chain last -> first
        followup = email_step(spec, followup)
    steps = {"id": str(uuid.uuid4()), "type": "START", "followup": followup}

    c = WoodpeckerClient(dry_run=dry_run)
    return c.create_campaign(name, mailbox_id, settings, steps, run_id=run_id, created_at_utc=created_at_utc)


def main(argv=None):
    import argparse, sys, uuid, csv as _csv
    from datetime import datetime, timezone
    ap = argparse.ArgumentParser(description="Sheet -> ready-to-send package; optionally build + load the Woodpecker DRAFT (never sends).")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--recipients", help="CSV of recipients (must have an 'email' column)")
    src.add_argument("--sheet-url", dest="sheet_url",
                     help="Google Sheets link or id — fetched as CSV (the sheet must be shared 'Anyone with the link can view')")
    ap.add_argument("--subject", required=True, help="subject template file")
    ap.add_argument("--body", required=True, help="email body template file (Woodpecker {{FIELD}} tokens; case-insensitive)")
    ap.add_argument("--suppress", help="optional CSV of emails to exclude (existing clients / opt-outs)")
    ap.add_argument("--out", default="ready_package", help="output folder for the package")
    ap.add_argument("--build-draft", dest="build_draft", action="store_true",
                    help="also create the Woodpecker DRAFT campaign (create-only; needs WOODPECKER_AGENT_BUILD=on + --mailbox)")
    ap.add_argument("--enroll", action="store_true",
                    help="also load the cleaned recipients INTO the draft (DRAFT only; never sends). Implies --build-draft")
    ap.add_argument("--mailbox", help="warmed secondary-domain mailbox id for the draft sender (must be allow-listed)")
    ap.add_argument("--name", help="campaign name (default '[LG-AGENT] sheet <id>')")
    ap.add_argument("--commit", action="store_true",
                    help="actually write to the LIVE Woodpecker account; without it, --build-draft/--enroll run DRY (simulated)")
    args = ap.parse_args(argv)
    if args.enroll:
        args.build_draft = True
    if args.build_draft and not args.mailbox:
        ap.error("--build-draft needs --mailbox <warmed secondary-domain mailbox id>")

    os.makedirs(args.out, exist_ok=True)
    if args.sheet_url:
        from . import gsheet
        try:
            recipients_path = gsheet.fetch_csv(args.sheet_url, os.path.join(args.out, "source_sheet.csv"))
            print("Fetched the Google Sheet -> %s" % recipients_path)
        except ValueError as e:
            print("Could not fetch the sheet: %s" % e); return 2
    else:
        recipients_path = args.recipients

    subject = io.open(args.subject, encoding="utf-8-sig").read().strip()
    body = io.open(args.body, encoding="utf-8-sig").read()
    s = build_package(recipients_path, subject, body, suppress_csv=args.suppress, out_dir=args.out)
    print(json.dumps(s, indent=2, ensure_ascii=False))
    print("\n=== %s ===" % s["verdict"])
    print("Package written to: %s/  (recipients_ready.csv, email_copy.txt, READY_SUMMARY.md)" % args.out)

    if args.build_draft:
        if not s["ready"]:
            print("\nNot building the draft: the package is NOT READY (fix the above first).")
            return 2
        from .wp_client import WoodpeckerClient, ForbiddenAction, WoodpeckerError
        dry = not args.commit
        run_id = uuid.uuid4().hex[:8]
        name = args.name or ("[LG-AGENT] sheet " + run_id)
        created = datetime.now(timezone.utc).isoformat()
        print("\n%s Woodpecker DRAFT '%s' (sender mailbox %s)…" % ("Simulating" if dry else "Creating", name, args.mailbox))
        try:
            draft = build_draft(name, str(args.mailbox), subject, body, run_id=run_id, created_at_utc=created, dry_run=dry)
        except (ForbiddenAction, WoodpeckerError) as e:
            print("Draft refused/failed: %s" % e); return 2
        cid = draft["campaign_id"]
        print("  draft id=%s · status=%s · dry_run=%s" % (cid, draft["status"], draft["dry_run"]))
        if args.enroll:
            with open(os.path.join(args.out, "recipients_ready.csv"), encoding="utf-8-sig", newline="") as f:
                rows = list(_csv.DictReader(f))
            try:
                en = WoodpeckerClient(dry_run=dry).enroll_to_draft(cid, rows)
            except (ForbiddenAction, WoodpeckerError) as e:
                print("Enroll refused/failed: %s" % e); return 2
            print("  enrolled %s recipient(s) into the draft · dry_run=%s" % (en["enrolled"], en.get("dry_run", False)))
        print("\nNEXT (human): open the draft in Woodpecker, review, and press Run/Send. The agent does NOT send.")
        print("NOTE: this path checks data hygiene only — NOT lawful basis. You (the sender) are responsible")
        print("      for permission/legitimate interest to email these recipients, plus a live unsubscribe.")
    return 0 if s["ready"] else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())
