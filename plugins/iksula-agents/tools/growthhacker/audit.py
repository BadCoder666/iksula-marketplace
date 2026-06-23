# -*- coding: utf-8 -*-
"""Append-only audit log — who published/emitted what, and every gate decision.
Metadata only; secret/PII-looking fields are scrubbed before write."""
import os, re, json
from . import config

_DENY = ("email", "headers", "authorization", "api_key", "apikey", "token",
         "password", "secret", "contact_identity", "first_name", "last_name",
         "phone", "profile_url", "handle")
_EMAIL_RE = re.compile(r"[^\s@]+@[^\s@]+\.[^\s@]+")
_HANDLE_RE = re.compile(r"@[A-Za-z][A-Za-z0-9_]{1,}")


def _redact_str(s):
    s = _EMAIL_RE.sub("<redacted-email>", s)
    s = _HANDLE_RE.sub("<redacted-handle>", s)
    return s


def _scrub(obj):
    """Recursively redact secret/PII keys and email/@handle values at ANY depth."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if any(b in str(k).lower() for b in _DENY):
                out[k] = "<redacted>"
            else:
                out[k] = _scrub(v)
        return out
    if isinstance(obj, (list, tuple)):
        return [_scrub(v) for v in obj]
    if isinstance(obj, str):
        return _redact_str(obj)
    return obj


def record(event, actor="growth-hacker-agent", run_id=None, ts=None, **fields):
    path = config.AUDIT_PATH
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    entry = {"ts": ts, "actor": actor, "run_id": run_id, "event": event}
    entry.update(_scrub(fields))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry
