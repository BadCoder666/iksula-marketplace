# -*- coding: utf-8 -*-
"""Lead Gen execution toolkit.

Makes the `skills/lead-gen/references/sending-stack.md` contract structural:
create-only Woodpecker access, a pre-send guardrail gate, merge-preview leak
detection, an ownership ledger, and an audit log. Nothing here starts a send.
"""
from . import config, merge_preview, presend_gate, ledger, audit  # noqa: F401

__all__ = ["config", "merge_preview", "presend_gate", "ledger", "audit", "wp_client"]
