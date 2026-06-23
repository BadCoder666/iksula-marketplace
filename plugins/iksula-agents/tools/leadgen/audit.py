# -*- coding: utf-8 -*-
"""Append-only audit log — closes the 'who ran it' accountability gap.

Vishal's concern: "if the AI sends wrong at scale, who do you catch?" Every
consequential action (gate decision, create, enroll-attempt, abort) is logged
here with actor + run_id + outcome. Metadata only — never prospect PII bodies.
"""
import os, json
from . import config

# Field names that must NEVER be persisted (secrets / PII). Matched as substrings.
_DENY = ("email", "headers", "authorization", "api_key", "apikey", "x-api-key",
         "token", "password", "secret", "prospects", "rejected_sample",
         "first_name", "last_name", "phone")


def _scrub(fields):
    """Drop/redact anything that looks like a secret or prospect PII, so a careless
    caller can't write it to the local log. Audit is metadata-only by design."""
    out = {}
    for k, v in fields.items():
        kl = str(k).lower()
        if any(b in kl for b in _DENY):
            out[k] = "<redacted>"
            continue
        if isinstance(v, str) and "@" in v and "." in v.rsplit("@", 1)[-1]:
            out[k] = "<redacted-email>"      # value looks like an email address
            continue
        out[k] = v
    return out


def record(event, actor="lead-gen-agent", run_id=None, ts=None, **fields):
    """Append one audit entry. `ts` (ISO-8601 UTC) is supplied by the caller.
    Extra fields are scrubbed of secrets/PII before being written."""
    path = config.AUDIT_PATH
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    entry = {"ts": ts, "actor": actor, "run_id": run_id, "event": event}
    entry.update(_scrub(fields))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry
