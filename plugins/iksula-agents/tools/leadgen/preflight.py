# -*- coding: utf-8 -*-
"""preflight — dry-run the pre-send gate over a cohort and print a PASS/HALT report.

This NEVER creates or sends anything. It is the operator's "would this be allowed?"
check: it loads a prospect CSV + an email template, runs merge-preview and the
pre-send gate, and prints exactly why a send would be held. Use it to prove the
wall is closed (today: HALT — zero lawful basis).

Usage:
  python -m leadgen.preflight --prospects leads.csv --template body.txt \
      --subject subj.txt --source clean_sheet --mailbox <warmed_id> [--approved TOKEN]
"""
import argparse, csv, json, sys
from . import merge_preview, presend_gate, config


def _read(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Dry-run the Lead Gen pre-send gate (no send, no create).")
    ap.add_argument("--prospects", required=True, help="CSV of prospect rows")
    ap.add_argument("--template", required=True, help="email body template file ({{field}} tokens)")
    ap.add_argument("--subject", help="optional subject template file")
    ap.add_argument("--source", default="raw_zoho", help="source_type: clean_sheet | raw_zoho")
    ap.add_argument("--mailbox", default="", help="sending mailbox id (must be allow-listed + warmed)")
    ap.add_argument("--approved", default="", help="human approval token (omit = not approved)")
    args = ap.parse_args(argv)

    rows = load_csv(args.prospects)
    body = _read(args.template)
    subject = _read(args.subject) if args.subject else None

    mp = merge_preview.validate(body, rows, subject=subject)
    ctx = {
        "source_type": args.source,
        "mailbox_id": args.mailbox,
        "merge_preview_clean": mp["clean"],
        "approval_token": args.approved or None,
    }
    gate = presend_gate.evaluate(rows, ctx)

    report = {
        "build_switch": "on" if config.build_enabled() else "off",
        "rows": len(rows),
        "merge_preview": {"clean": mp["clean"], "leaking_count": mp["leaking_count"],
                          "fields": mp["fields"], "leaking_rows": mp["leaking_rows"][:10]},
        "gate": gate,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print("\n=== VERDICT: %s ===" % gate["verdict"])
    if gate["verdict"] != "ALLOW":
        print("Held for: " + "; ".join(gate["halts"]))
    # non-zero exit on HALT so a wrapper/script can gate on it
    return 0 if gate["verdict"] == "ALLOW" else 2


if __name__ == "__main__":
    sys.exit(main())
