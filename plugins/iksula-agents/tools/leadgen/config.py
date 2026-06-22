# -*- coding: utf-8 -*-
"""Lead Gen execution toolkit — configuration & hard constants.

Single source of truth for the safety rails in `skills/lead-gen/references/sending-stack.md`
and `seam-and-compliance.md`. Nothing here sends email. Secrets come from the environment
only (never hardcoded/committed).
"""
import os

# ---- Secrets (env only) -------------------------------------------------------
# Woodpecker key lives in env WOODPECKER_API_KEY (or sourced from gitignored
# _woodpecker.local). We NEVER read it from a committed file or print it.
def get_woodpecker_key():
    return os.environ.get("WOODPECKER_API_KEY")

# ---- Kill switch --------------------------------------------------------------
# The agent makes ZERO write calls unless this is explicitly "on".
def build_enabled():
    return os.environ.get("WOODPECKER_AGENT_BUILD", "off").strip().lower() == "on"

# ---- Woodpecker connector facts (verified 2026-06-19) -------------------------
WP_BASE = "https://api.woodpecker.co"
WP_LIST_PATH = "/rest/v1/campaign_list"      # READ (metadata only, no PII)
WP_CREATE_PATH = "/rest/v2/campaigns"        # CREATE-ONLY (HTTP 201 -> DRAFT)

# State-changing verbs the agent must NEVER call, on ANY campaign incl. its own.
# Stored lowercase; the guard compares item.lower() so casing can't slip past.
FORBIDDEN_VERBS = frozenset(v.lower() for v in {
    "run", "start", "resume", "pause", "stop", "delete",
    "runCampaign", "pauseCampaign", "resumeCampaign", "stopCampaign", "deleteCampaign",
})

# The ONLY (method, path) pairs the HTTP layer may ever issue. Any other request
# — including a hand-built status=RUNNING PUT or a /run POST — is refused. This
# makes "the agent cannot send" an enforced invariant, not a naming convention.
ALLOWED_HTTP = frozenset({("GET", WP_LIST_PATH), ("POST", WP_CREATE_PATH)})

# Non-sending statuses a campaign may be left in / enrolled into.
NON_SENDING_STATUSES = frozenset({"DRAFT", "PAUSED"})

# ---- Lawful basis (Zoho field Data_Processing_Basis) --------------------------
# Acceptable *stored* values. NOTE: Zoho stores actual!=display for some picklist
# items (display 'Consent - Obtained' -> actual 'Obtained'); accept both forms.
VALID_LAWFUL_BASIS = frozenset({
    "Legitimate Interests", "Contract", "Consent - Obtained", "Obtained",
})

# Jurisdictions we are permitted to cold-email (Europe is never cold-emailed).
ALLOWED_COLD_REGIONS = frozenset({"US", "USA", "United States", "IN", "India"})
# ccTLDs / signals that must fail closed (foreign data subjects hide in 'USA').
BLOCKED_CCTLDS = frozenset({
    ".uk", ".co.uk", ".de", ".eu", ".ca", ".gc.ca", ".se", ".fr", ".nl", ".au", ".in",
})
FREE_WEBMAIL = frozenset({
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
    "icloud.com", "proton.me", "gmx.com", "live.com", "msn.com",
})

# ---- Mailbox isolation --------------------------------------------------------
PRIMARY_DOMAIN = "iksula.com"   # NEVER send cold from the primary domain.
# Real human mailboxes on the live account — never borrow these.
FORBIDDEN_MAILBOXES = frozenset({
    "sam@iksula.com", "vishal.s@iksula.com", "vishal.sobti@iksula.com",
    "pavan.k@iksula.com", "subhasan.d@iksula.com",
})
# Out-of-band allow-list of warmed, isolated secondary-domain mailbox IDs the
# agent MAY use. EMPTY by default => the agent cannot build at all (correct:
# no dedicated warmed cold-send mailbox has been provisioned yet, 260619).
def allowed_mailbox_ids():
    raw = os.environ.get("WOODPECKER_ALLOWED_MAILBOX_IDS", "").strip()
    return [x.strip() for x in raw.split(",") if x.strip()]

# ---- Caps ---------------------------------------------------------------------
MAX_CAMPAIGNS_PER_RUN = 5
NAME_PREFIX = "[LG-AGENT]"

# ---- Paths (local, non-PII artifacts only) ------------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
LEDGER_PATH = os.path.join(ROOT, "_state", "creation_ledger.jsonl")
AUDIT_PATH = os.path.join(ROOT, "_state", "audit_log.jsonl")
