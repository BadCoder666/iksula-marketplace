# -*- coding: utf-8 -*-
"""Growth Hacker execution toolkit.

Makes the `skills/growth-hacker/SKILL.md` + `seam-contract.md` rails structural:
a publish gate (paid/voice/broadcast gated), an idempotent seam emitter (no score/
ack, lawful-basis stamped, no PII to Brain), and a schema-locked aggregate-only
Brain writer. Nothing here posts publicly or sends email.
"""
from . import config, ulid, publish_gate, seam_emitter, brain_metrics, audit  # noqa: F401

__all__ = ["config", "ulid", "publish_gate", "seam_emitter", "brain_metrics", "audit"]
