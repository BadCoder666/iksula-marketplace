# -*- coding: utf-8 -*-
"""Creation ledger — the source of truth for campaign OWNERSHIP.

A campaign is 'the agent's own' IFF its id is in this ledger — never inferred
from the [LG-AGENT] name prefix. Append-only JSONL. Records metadata only
(no prospect PII). In production this should be a Zoho custom record (system of
record); this local JSONL mirror keeps the toolkit runnable/testable offline.
"""
import os, json
from . import config


def _ensure_dir(path):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)


# Only these keys are ever persisted — keeps prospect PII out of the ledger.
_ALLOWED_KEYS = ("run_id", "campaign_id", "exact_name", "sender_mailbox",
                 "segment", "created_at_utc", "dry_run")


def append(entry, path=None):
    """Append one creation record (metadata only). created_at_utc is supplied by the
    caller (no clock here). Unknown keys are dropped so PII can't leak into the ledger."""
    path = path or config.LEDGER_PATH
    _ensure_dir(path)
    required = ("run_id", "campaign_id", "exact_name", "sender_mailbox", "created_at_utc")
    missing = [k for k in required if k not in entry]
    if missing:
        raise ValueError("ledger entry missing fields: %s" % ", ".join(missing))
    clean = {k: entry[k] for k in _ALLOWED_KEYS if k in entry}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(clean, ensure_ascii=False) + "\n")
    return clean


def load(path=None):
    path = path or config.LEDGER_PATH
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def owned_ids(path=None):
    """Set of campaign_ids the agent created (the ONLY ids it may write to)."""
    return {str(e["campaign_id"]) for e in load(path) if e.get("campaign_id") is not None}


def owns(campaign_id, path=None):
    return str(campaign_id) in owned_ids(path)
