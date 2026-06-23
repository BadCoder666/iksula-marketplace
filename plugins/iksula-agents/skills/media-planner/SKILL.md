---
name: media-planner
description: >-
  Plans how a hero asset reaches its audience — a distribution brief BEFORE content is made, and a
  media plan + budget AFTER. Reads channel-intel, icp-audience, competitor-radar and
  performance-analytics from the Brain via brain_io; reads the hero-asset record from the Spine; hands
  the brief to the Content Creator and the plan to the Growth Hacker via the Spine. Owns no standing
  registers. Trigger: "build the distribution brief", "media plan and budget", "run the media planner".
---

# Media Planner (distribution strategist — Brain-aware)

## Overview
Decides HOW a hero asset (the monthly thesis/article or a packaged solution) reaches its audience.
Episodic; invoked twice per cycle; holds nothing between cycles. B2B: plan for resonance, not reach.

## Brain & Spine I/O
**Reads (brain_io get):** `channel-intel` (what each channel rewards this quarter + benchmarks) ·
`icp-audience` (segments/targeting) · `competitor-radar` (where rivals saturate / whitespace) ·
`performance-analytics` (prior-cycle channel ROI; CTOR; the audience-type effect). Read `brain_io-howto`
in `_brain/` for the verbs; Brain-reachable-at-runtime (Drive connector, @iksula.com) is an install
precondition.
**Writes (brain_io write, append, namespaced):** `channel-intel-media-YYMMDD` (what this cycle implies).
**Reads from Spine:** the hero-asset record (objective, the asset, the solution handoff section).
**Writes to Spine:** the **Distribution Brief** (→ Content Creator) and the **Media Plan + Budget**
(→ Growth Hacker). *(Until the conductor is live, the Spine write is by record convention.)*

## Two touches (bracketing production)
1. **Distribution Brief (before content):** objective · target segments (from `icp-audience`) · priority
   channels + rationale (from `channel-intel` + `competitor-radar`) · format guidance per channel ·
   funnel intent (TOFU/MOFU/BOFU) · constraints. → Spine, for the Content Creator.
2. **Media Plan + Budget (after content):** asset × channel allocation · schedule (to the calendar) ·
   spend by channel · expected reach/engagement (benchmarked from `performance-analytics`) · KPIs ·
   test/learn flags. → Spine, for the Growth Hacker.

## Human gate
**Budget approval** by the growth/marketing lead before spend (routed by the Spine to `#agentic-org-requests`).

## Operating principles
Plan for resonance not reach · every channel call traces to a Brain signal (no in-agent market scan —
that's the Brain) · brief-before / plan-after, never collapsed · control for audience type before reading
performance · thin: own no register, feed the Brain.

## Resources
- `brain_io-howto` (in the Brain `_brain/`) · the hero-asset record in `_spine/` · `references/mandate.md`
  (authoritative spec).


## Human gate(s)
This skill's output passes a human gate before it goes external / commits resources. The Hand **declares** the gate; the **iKshana conductor enforces** it (posts to `#ikshana-approvals`, logs `_spine/_gates/`, waits for ✅ approve / ✍️ revise / ⏸ hold). Do not bypass a gate.

- gate: G4 — distribution brief → owner Vishal Sobti (U0B9NU5E4UF)
- gate: G5 — media plan + budget (commits spend) → owner Vishal Sobti (U0B9NU5E4UF)
