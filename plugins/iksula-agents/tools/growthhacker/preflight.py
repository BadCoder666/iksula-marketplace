# -*- coding: utf-8 -*-
"""preflight — dry-run a publish action and a seam emit; print ALLOW/HOLD. No posting.

Usage:
  python -m growthhacker.preflight --action action.json [--event event.json]
`action.json` is a publish action (see publish_gate.evaluate). `event.json` is a
content-sourced-lead event (see seam_emitter.emit); it is written to a TEMP queue so
nothing touches the real Spine.
"""
import argparse, json, sys, tempfile, os
from . import publish_gate, seam_emitter, config


def main(argv=None):
    ap = argparse.ArgumentParser(description="Dry-run the Growth Hacker publish gate + seam emit.")
    ap.add_argument("--action", help="JSON file with a publish action")
    ap.add_argument("--event", help="JSON file with a content-sourced-lead event (written to a temp queue)")
    args = ap.parse_args(argv)

    out = {"publish_switch": "on" if config.publish_enabled() else "off"}

    if args.action:
        with open(args.action, encoding="utf-8") as f:
            action = json.load(f)
        out["publish_gate"] = publish_gate.evaluate(action)

    if args.event:
        with open(args.event, encoding="utf-8") as f:
            event = json.load(f)
        tmp = os.path.join(tempfile.gettempdir(), "gh_preflight_queue.jsonl")
        try:
            out["seam_emit"] = seam_emitter.emit(event, queue_path=tmp)
        except ValueError as e:
            out["seam_emit"] = {"status": "rejected", "reason": str(e)}
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

    print(json.dumps(out, indent=2, ensure_ascii=False))
    pg = out.get("publish_gate", {})
    if pg:
        print("\n=== PUBLISH: %s ===" % pg.get("verdict"))
        if pg.get("verdict") != "ALLOW":
            print("Held for: " + "; ".join(pg.get("holds", [])))
    return 0 if pg.get("verdict", "ALLOW") == "ALLOW" else 2


if __name__ == "__main__":
    sys.exit(main())
