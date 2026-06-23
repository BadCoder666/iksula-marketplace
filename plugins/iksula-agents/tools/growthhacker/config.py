# -*- coding: utf-8 -*-
"""Growth Hacker execution toolkit — configuration & hard constants.

Encodes the rails in `skills/growth-hacker/SKILL.md` + `references/seam-contract.md`:
publish only the approved plan (paid inherits the Media Planner's budget gate;
named-byline community replies are human voice-gated; broadcast email is human
first-send-gated), emit the GH->Lead Gen seam idempotently with NO score/ack and a
stamped lawful-basis tag, and write ONLY aggregates (never PII) to the Brain.

Nothing here posts publicly or sends email. Secrets/switches come from env only.
"""
import os, re

# ---- Kill switch --------------------------------------------------------------
def publish_enabled():
    """Zero publish/post calls unless explicitly on."""
    return os.environ.get("GROWTH_PUBLISH", "off").strip().lower() == "on"

# ---- Publish action types -----------------------------------------------------
ACTION_ORGANIC = "organic_post"               # 1-to-many organic post (no separate human gate, but instrumented + scheduled)
ACTION_PAID = "paid_post"                      # paid distribution — inherits Media Planner budget approval
ACTION_BYLINE_REPLY = "community_reply_as_byline"  # reply as a named leader — VOICE GATE (human owns the voice)
ACTION_BROADCAST_EMAIL = "broadcast_email"     # GH-owned broadcast/BOFU email — first-send human gate
VALID_ACTIONS = frozenset({ACTION_ORGANIC, ACTION_PAID, ACTION_BYLINE_REPLY, ACTION_BROADCAST_EMAIL})

# Allowed online / 1-to-many surfaces. GH does NOT do 1-to-1 outreach (that's Lead Gen).
ALLOWED_CHANNELS = frozenset({
    "LinkedIn-post", "LinkedIn-page", "X-post", "X-thread", "YouTube-video",
    "YouTube-comment", "Blog-post", "Blog-form", "Telegram", "tracked-CTA-click",
})
# Calendar statuses an organic/paid publish may execute (must be an approved plan row).
PUBLISHABLE_STATUSES = frozenset({"Scheduled"})

# ---- The seam (content-sourced-lead) ------------------------------------------
VALID_SIGNAL_TYPES = frozenset({
    "comment", "reply", "dm", "form_fill", "content_download",
    "cta_click", "connection_accept", "mention",
})
# GH MUST NOT put any of these on the seam — qualification/ack/enrichment are Lead Gen's.
# Matched by NORMALIZED substring (so 'lead_grade', 'Tier', 'MQL ' etc. are all caught),
# and scanned RECURSIVELY through nested dicts/lists (a score hidden in intent_signal
# or contact_identity must not slip across the seam).
FORBIDDEN_SEAM_FRAGMENTS = frozenset({
    "score", "grade", "mql", "sql", "qualif", "ackstatus", "accountstatus",
    "isecs", "enrich", "disposition", "propensity", "tier", "rating", "ranking",
    "leadstage", "routeto",
})
EMITTED_BY = "growth-hacker"


def _norm_key(k):
    return re.sub(r"[^a-z0-9]", "", str(k).lower())


def is_forbidden_seam_key(key):
    nk = _norm_key(key)
    return any(frag in nk for frag in FORBIDDEN_SEAM_FRAGMENTS)


def forbidden_keys_deep(obj):
    """Recursively collect every dict key (at any nesting depth) that is forbidden."""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if is_forbidden_seam_key(k):
                found.append(k)
            found.extend(forbidden_keys_deep(v))
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            found.extend(forbidden_keys_deep(v))
    return found


def lawful_basis_tag(region):
    """Stamp region -> lawful-basis tag. FAIL-SAFE: anything not clearly US is
    company-level only (EU/India/other/unknown), the more restrictive setting."""
    r = (region or "").strip().upper()
    if r in ("US", "USA", "UNITED STATES", "U.S.", "U.S.A."):
        return "US: person-level de-anon permitted"
    return "non-US: company-level ONLY (GDPR/DPDP)"

# ---- Brain feeds (aggregate-only, no PII, schema-locked) ----------------------
BRAIN_METRIC_SCHEMA = ("period", "source", "asset_or_campaign", "channel",
                       "metric", "value", "audience_type", "notes")
# Key fragments that mark a row as per-prospect PII (forbidden in the Brain).
PII_LIKE_KEYS = ("email", "name", "handle", "profile_url", "contact", "phone",
                 "first_name", "last_name", "display_name", "ip", "click_id")

# ---- Paths (local mirrors of Spine/Brain; prod resolves Drive via brain_io) ----
ROOT = os.path.dirname(os.path.abspath(__file__))
SPINE_QUEUE = os.path.join(ROOT, "_state", "content_sourced_lead_queue.jsonl")
BRAIN_RAW_DIR = os.path.join(ROOT, "_state", "_brain_raw")
BRAIN_FEED_DIR = os.path.join(ROOT, "_state", "_brain_feeds")
AUDIT_PATH = os.path.join(ROOT, "_state", "audit_log.jsonl")
