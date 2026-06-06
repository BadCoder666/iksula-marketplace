---
name: vertical-process-mapping
description: >-
  Maps an industry vertical's functions at L1/L2/L3 to surface post-LLM automation opportunities,
  scored into a 6-tab workbook + an Iksula solution shortlist. Reads the scoring rubric + controlled
  vocabularies from the Brain (method-vocab) so every vertical stays comparable; reads competitor-radar
  for market context; writes the shortlist to the Spine and appends reusable-capability signals to the
  Brain. Trigger: "run the vertical mapping for a named industry", "process mapping", "map this vertical".
---

# Vertical Process Mapping (post-LLM automation opportunities — Brain-aware)

## Overview
Consultant-grade mapping that produces an Iksula solution pipeline — not an academic audit. Every
vertical is mapped identically so files stay comparable and reusable capabilities surface across
verticals. Thin: the scoring standard and market context come from the Brain; the shortlist hands off
via the Spine.

## Brain & Spine I/O
**Reads (brain_io get):** `method-vocab` (THE scoring rubric + controlled vocabularies — the single
shared source, also used by the Solution Architect; do NOT redefine locally) · `competitor-radar`
(market/incumbent context). Read `brain_io-howto` in `_brain/` for the get/list/write verbs;
Brain-reachable-at-runtime (Drive connector, @iksula.com) is an install precondition.
**Writes (brain_io write, append):** `method-vocab` ONLY when a standard genuinely changes (writer of
record) · `proof-catalogue`/capability — the cross-vertical reusable-capability signals.
**Writes to Spine:** the **Iksula Solution Shortlist** (the handoff contract to the Solution Architect)
+ the workbook reference. *(Until the conductor is live, the Spine write is by record convention.)*

## Workflow (method unchanged; Brain-wired ends)
1. **Scope** — organisation archetype · in/out functions · engagement mode (AskUserQuestion).
2. **Map every function** (taxonomy in `references/function-taxonomy.md`) — L1→L2→L3 with manual
   hotspots, tools, obvious vs non-obvious opportunities (most effort on the non-obvious).
3. **Economic lens** — match value to the archetype; never default to headcount.
4. **Build the 6-tab workbook** per `references/excel-build-spec.md`, scoring with the rubric **from
   `method-vocab`** and the controlled vocabularies **from `method-vocab`**.
5. **Synthesise & sequence** — cross-cutting horizontals + the shortlist (ROI-to-effort phases).
6. **Self-audit, recalc, save** — Coverage-Map audit; `python scripts/recalc.py <file>` → zero formula
   errors; verify tiers discriminate. **Write the shortlist to the Spine**; append the reusable-capability
   view to the Brain.

## Scoring & vocabularies
Read from `method-vocab` (Brain) — do not redefine here. (Impact / Data-Readiness / Integration-Ease /
Accuracy-Tolerance → Feasibility → Composite → Tier P1/P2/P3 / Quick-Win; Solution Archetype · Value
Lever · Reusability · Productizable.)

## Operating principles
Completeness is non-negotiable (Coverage-Map self-audit) · rubric + vocab come from `method-vocab`
(keeps verticals comparable — the whole point of centralising them) · economic lens matches archetype ·
reusability is the most commercially important attribute (feeds `proof-catalogue`/capability) · dense +
concrete, never generic · the shortlist is a **Spine handoff**, not a dead tab.

## Save
Default workbook location `/Users/dj/Iksula FY27/Iksula_Strategy/Services/Vertical - process mapping/`;
file name = vertical name only (no date suffix). Confirm the folder before saving. Present with present_files.

## Resources
- `brain_io-howto` (in the Brain `_brain/`) — the get/list/write procedures.
- `references/function-taxonomy.md` · `references/excel-build-spec.md` · `assets/B2B Distribution.xlsx` ·
  `scripts/build_template.py` · `scripts/recalc.py` *(all unchanged)*.
- ~~rubric + controlled vocabularies inline~~ → now read from `method-vocab` in the Brain.
