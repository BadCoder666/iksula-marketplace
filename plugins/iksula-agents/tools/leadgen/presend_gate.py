# -*- coding: utf-8 -*-
"""The pre-send / pre-enroll guardrail gate — the WALL.

Implements the governance decision tree (flowchart segment 6) and the compliance
playbook pre-send order. Enrolling a prospect into Woodpecker IS a PII write, so
these checks run at ENROLL time, per record, against live data (the caller passes
freshly-read records; this module never caches).

Returns a structured verdict. With 100% of Zoho leads at null Data_Processing_Basis
today, the correct number of eligible records is ZERO and the cohort verdict is HALT.
Nothing here sends or enrolls; it only decides ALLOW / HALT and explains why.
"""
from . import config


# ---- per-record checks (the suppression + basis + geo gate) -------------------
def _domain(email):
    return (email or "").strip().lower().rsplit("@", 1)[-1] if "@" in (email or "") else ""


_FALSY = frozenset({"", "false", "0", "no", "n", "f", "none", "null", "na"})


def _flag(v):
    """Suppression-flag coercion with a FAIL-SAFE default: anything that isn't an
    explicit falsy token counts as SET (suppressed). So a garbled/unknown value
    ('X', 'opt-out', 'suppressed') suppresses rather than slipping through; only
    bool/None and the explicit falsy tokens are treated as not-suppressed."""
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    return str(v).strip().lower() not in _FALSY


def check_record(rec):
    """Return (eligible: bool, reasons: [str]) for one prospect record.

    rec keys (all caller-supplied, read live from the clean Sheet / Zoho):
      email, region/Country, data_processing_basis, email_opt_out,
      is_existing_client, is_competitor, is_internal, already_contacted, converted
    """
    reasons = []
    email = (rec.get("email") or rec.get("Email") or "").strip()
    dom = _domain(email)

    # 1. lawful basis present (re-read live, never cached)
    basis = (rec.get("data_processing_basis") or rec.get("Data_Processing_Basis") or "").strip()
    if basis not in config.VALID_LAWFUL_BASIS:
        reasons.append("no_lawful_basis")

    # 2. synchronous suppression scrub (fail-safe coercion)
    if _flag(rec.get("email_opt_out")) or _flag(rec.get("Email_Opt_Out")):
        reasons.append("opted_out")
    if _flag(rec.get("is_existing_client")) or _flag(rec.get("converted")) or _flag(rec.get("Converted__s")):
        reasons.append("existing_client")
    if _flag(rec.get("is_competitor")):
        reasons.append("competitor")
    if _flag(rec.get("is_internal")):
        reasons.append("internal_or_test")
    if _flag(rec.get("already_contacted")):
        reasons.append("already_contacted_suppress")

    # 3. email present + B2B domain (no free webmail, no foreign ccTLD)
    if not email or "@" not in email:
        reasons.append("missing_email")
    elif dom in config.FREE_WEBMAIL:
        reasons.append("free_webmail")
    elif any(dom.endswith(cc) for cc in config.BLOCKED_CCTLDS):
        reasons.append("foreign_cctld")

    # 4. geo-gate — FAIL CLOSED: a record must carry an explicitly permitted region.
    # An empty/unknown region is NOT permitted (we can't confirm jurisdiction).
    region = (rec.get("region") or rec.get("Country") or "").strip()
    if region not in config.ALLOWED_COLD_REGIONS:
        reasons.append("region_unknown_or_not_permitted")

    return (len(reasons) == 0, reasons)


# ---- cohort-level checks (the gates that must hold for the whole send) ---------
def evaluate(prospects, ctx):
    """Run the full gate over a cohort.

    ctx keys:
      source_type        : 'clean_sheet' | 'raw_zoho' | str   (must be clean_sheet)
      mailbox_id         : the sending mailbox id (must be in the allow-list)
      merge_preview_clean: bool   (from merge_preview.validate)
      approval_token     : str | None   (human approval; None => not approved)

    Returns a verdict dict. verdict == 'ALLOW' requires: build switch on, source is
    a clean Sheet, mailbox isolated+allow-listed, merge preview clean, human approval
    present, AND at least one record passes every per-record check.
    """
    halts = []

    # A. kill switch
    if not config.build_enabled():
        halts.append("build_switch_off (set WOODPECKER_AGENT_BUILD=on)")

    # B. source must be a clean Sheet, never raw Zoho (the 40k-blast trap)
    if ctx.get("source_type") != "clean_sheet":
        halts.append("source_not_clean_sheet (raw Zoho is never a send source)")

    # C. mailbox isolation
    mbox = (ctx.get("mailbox_id") or "").strip()
    allow = config.allowed_mailbox_ids()
    if not mbox:
        halts.append("no_mailbox (v2 create requires >=1 isolated warmed mailbox)")
    elif not allow:
        halts.append("no_allowlisted_mailbox (none provisioned — infra gap)")
    elif mbox not in allow:
        halts.append("mailbox_not_allowlisted")
    if mbox in config.FORBIDDEN_MAILBOXES or mbox.endswith("@" + config.PRIMARY_DOMAIN):
        halts.append("mailbox_is_live_or_primary (never borrow a live mailbox)")

    # D. merge-preview must be clean
    if ctx.get("merge_preview_clean") is not True:
        halts.append("merge_preview_not_clean (token leak risk)")

    # E. human approval
    if not ctx.get("approval_token"):
        halts.append("no_human_approval")

    # per-record eligibility — the verdict carries NO email/PII (row index + reasons
    # only), so it is safe to persist to the audit log / pass around.
    eligible_count = 0
    rejected = []
    histogram = {}
    for i, rec in enumerate(prospects):
        ok, reasons = check_record(rec)
        if ok:
            eligible_count += 1
        else:
            rejected.append({"row_index": i, "reasons": reasons})
            for r in reasons:
                histogram[r] = histogram.get(r, 0) + 1
    if eligible_count == 0:
        halts.append("zero_eligible_records (no record cleared lawful basis + suppression)")

    verdict = "ALLOW" if not halts else "HALT"
    return {
        "verdict": verdict,
        "halts": halts,
        "eligible_count": eligible_count,
        "rejected_count": len(rejected),
        "reason_histogram": histogram,
        "rejected_sample": rejected[:10],   # row indices + reasons only — no PII
    }
