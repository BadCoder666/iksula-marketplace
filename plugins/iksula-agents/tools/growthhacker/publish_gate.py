# -*- coding: utf-8 -*-
"""The publish gate — nothing goes public unless its gate holds.

GH executes an APPROVED plan; the dangerous surfaces are: paid spend (needs the
Media Planner's budget approval), a reply as a named byline leader (needs a human
to own the voice), and a GH-owned broadcast email (human first-send gate). Organic
posts have no separate human gate (the calendar+plan were already approved) but
still must be instrumented and executing a Scheduled row. This module DECIDES
ALLOW/HOLD; it never actually posts.
"""
from . import config


def evaluate(action):
    """action keys:
      type            : one of config.VALID_ACTIONS
      channel         : an allowed online surface
      asset_ref       : must resolve to a real asset
      calendar_status : the plan row status (organic/paid must be 'Scheduled')
      utm, tracked_cta: instrumentation (required to publish organic/paid)
      is_named_byline : bool — reply posts as a named leader?
      approval_token  : human approval (voice gate / broadcast first-send)
      budget_approved : bool — Media Planner approved the spend (paid only)
    Returns {verdict: ALLOW|HOLD, holds: [...]}.
    """
    holds = []
    at = action.get("type")

    if not config.publish_enabled():
        holds.append("publish_switch_off (set GROWTH_PUBLISH=on)")
    if at not in config.VALID_ACTIONS:
        holds.append("unknown_action_type")
    if action.get("channel") not in config.ALLOWED_CHANNELS:
        holds.append("channel_not_allowed (GH is online/1-to-many only)")
    if not action.get("asset_ref"):
        holds.append("no_asset_ref (must resolve to a real asset, never improvise)")

    # anything that ships content must be instrumented (UTM + tracked CTA)
    if at in (config.ACTION_ORGANIC, config.ACTION_PAID, config.ACTION_BROADCAST_EMAIL):
        if not action.get("utm") or not action.get("tracked_cta"):
            holds.append("not_instrumented (UTM + tracked CTA required before publish)")

    # organic + paid execute an approved Scheduled calendar row
    if at in (config.ACTION_ORGANIC, config.ACTION_PAID):
        if action.get("calendar_status") not in config.PUBLISHABLE_STATUSES:
            holds.append("calendar_row_not_scheduled (execute the approved plan only)")

    # paid: inherits the Media Planner budget approval
    if at == config.ACTION_PAID and not action.get("budget_approved"):
        holds.append("paid_without_budget_approval (Media Planner gate)")

    # named-byline community reply: ALWAYS human-gated for this action type — a human
    # owns the voice. The gate is never opt-in via a caller-supplied flag.
    if at == config.ACTION_BYLINE_REPLY and not action.get("approval_token"):
        holds.append("byline_voice_not_approved (a human owns the voice - draft, never post unapproved)")

    # GH-owned broadcast/BOFU email: first-send is human-gated, never autonomous at scale
    if at == config.ACTION_BROADCAST_EMAIL and not action.get("approval_token"):
        holds.append("broadcast_first_send_not_human_approved")

    return {"verdict": "ALLOW" if not holds else "HOLD", "holds": holds}
