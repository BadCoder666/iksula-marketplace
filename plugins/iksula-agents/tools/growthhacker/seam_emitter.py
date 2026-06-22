# -*- coding: utf-8 -*-
"""The GH -> Lead Gen seam — emit `content-sourced-lead` records to the Spine queue.

Enforces the seam contract structurally:
  * one record per interest event, keyed on a ULID `correlation_id`; re-emit of the
    same id is an idempotent no-op (at-least-once delivery, idempotent consume).
  * GH stamps `region` -> `lawful_basis_tag` (fail-safe to company-level for non-US).
  * GH NEVER qualifies/enriches/acks: any score/grade/MQL/ack_status/account field
    is rejected. `ack_status` is left null (Lead Gen writes it on consume).
  * writes ONLY to the Spine queue — never to the Brain (no PII in the Brain).
"""
import os, json
from . import config, ulid


def _seen_ids(path):
    ids = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except ValueError:
                    continue                         # skip a corrupt line, never crash future emits
                if isinstance(obj, dict):
                    ids.add(obj.get("correlation_id"))
    return ids


def emit(event, queue_path=None):
    """Emit one content-sourced-lead. `event` carries what GH actually observed.
    Required: source_asset_ref, source_channel, intent_signal{signal_type,...}, captured_at.
    Optional: contact_identity (verbatim/unenriched), region, consent_context, correlation_id.
    """
    queue_path = queue_path or config.SPINE_QUEUE

    # GH must not carry qualification / ack / enrichment across the seam — scan
    # RECURSIVELY (a score hidden inside intent_signal / contact_identity counts).
    bad = sorted(set(config.forbidden_keys_deep(event)))
    if bad:
        raise ValueError("seam record must not carry %s (GH never qualifies/acks/enriches)" % bad)

    sig = event.get("intent_signal") or {}
    if sig.get("signal_type") not in config.VALID_SIGNAL_TYPES:
        raise ValueError("invalid/absent signal_type: %r" % sig.get("signal_type"))
    if not event.get("source_asset_ref"):
        raise ValueError("source_asset_ref is required (ties back to the content package)")
    if event.get("source_channel") not in config.ALLOWED_CHANNELS:
        raise ValueError("source_channel %r not an allowed GH surface" % event.get("source_channel"))
    if not event.get("captured_at"):
        raise ValueError("captured_at (ISO-8601 UTC) is required")

    cid = event.get("correlation_id") or ulid.new_ulid()
    if not ulid.is_ulid(cid):
        raise ValueError("correlation_id must be a ULID")

    os.makedirs(os.path.dirname(queue_path), exist_ok=True)
    if cid in _seen_ids(queue_path):
        return {"status": "duplicate", "correlation_id": cid}   # idempotent no-op

    record = {
        "correlation_id": cid,
        "contact_identity": event.get("contact_identity"),     # verbatim, unenriched
        "source_asset_ref": event.get("source_asset_ref"),
        "source_channel": event.get("source_channel"),
        "intent_signal": sig,                                   # verbatim, NO score
        "region": event.get("region"),
        "lawful_basis_tag": config.lawful_basis_tag(event.get("region")),
        "captured_at": event.get("captured_at"),
        "consent_context": event.get("consent_context"),
        "emitted_by": config.EMITTED_BY,
        "ack_status": None,                                     # Lead Gen sets this, not GH
    }
    with open(queue_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return {"status": "emitted", "correlation_id": cid, "lawful_basis_tag": record["lawful_basis_tag"]}
