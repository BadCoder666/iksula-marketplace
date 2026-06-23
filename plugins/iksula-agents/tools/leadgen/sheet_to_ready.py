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
    out.append("1. Open Woodpecker, create the campaign with the copy in `email_copy.txt`.")
    out.append("2. Import `recipients_ready.csv` as the prospect list.")
    out.append("3. Review, then press send. (Make sure an unsubscribe is included and you're sending from a mailbox you're happy to send this volume from.)")
    out.append("\n*Prepared by the Lead Gen agent — it cleaned, de-duplicated and validated the list; it did not send anything. The send is a human decision.*")
    return "\n".join(out) + "\n"


# ---- optional: also create the Woodpecker DRAFT shell (create-only, never sends) ----
def build_draft(name, mailbox_id, subject, body, run_id=None, created_at_utc=None, dry_run=True):
    from .wp_client import WoodpeckerClient
    steps = [
        {"type": "START"},
        {"type": "EMAIL", "followup": False, "subject": subject,
         "body": {"versions": [{"body": body}]}},
    ]
    c = WoodpeckerClient(dry_run=dry_run)
    return c.create_campaign(name, mailbox_id, {"timezone": "Asia/Kolkata", "daily_enroll": 50},
                             steps, run_id=run_id, created_at_utc=created_at_utc)


def main(argv=None):
    import argparse, sys
    ap = argparse.ArgumentParser(description="Turn a recipient sheet + email copy into a ready-to-send package (no sending).")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--recipients", help="CSV of recipients (must have an 'email' column)")
    src.add_argument("--sheet-url", dest="sheet_url",
                     help="Google Sheets link or id — fetched as CSV (the sheet must be shared 'Anyone with the link can view')")
    ap.add_argument("--subject", required=True, help="subject template file ({{field}} tokens allowed)")
    ap.add_argument("--body", required=True, help="email body template file ({{field}} tokens allowed)")
    ap.add_argument("--suppress", help="optional CSV of emails to exclude (existing clients / opt-outs)")
    ap.add_argument("--out", default="ready_package", help="output folder for the package")
    args = ap.parse_args(argv)

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
    return 0 if s["ready"] else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())
