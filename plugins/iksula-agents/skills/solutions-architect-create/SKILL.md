---
name: solutions-architect-create
description: >-
  Productizes a diagnosed opportunity into a named, sellable Iksula solution (internal intro deck +
  client pitch deck). Reads competitor-radar, icp-audience, proof-catalogue and method-vocab from the
  Brain via brain_io; writes the solution source-of-truth + handoff section as a Spine asset record;
  appends new sourced competitive intel and new proof back to the Brain. Owns no private research.
  Trigger: "package this solution", "build the solution intro/pitch deck", "productize a named
  opportunity", "how do we differentiate this solution".
---

# Solutions Architect - Create (productize an opportunity — Brain-aware)

# Overview
The role Accenture/McKinsey/Deloitte play between raw opportunity and packaged offering — for Iksula.
Takes ONE shortlisted opportunity, decides where Iksula can win, and produces the packaged solution
definition. Does not invent opportunities or capabilities, and does not deliver. Thin: standing intel
from the Brain, the solution record on the Spine.

## Brain & Spine I/O
**Reads (brain_io get):** `competitor-radar` (the standing landscape — start here, don't rebuild) ·
`proof-catalogue` (real Iksula capabilities/IP + named case studies + brand — **never invent a
capability**) · `icp-audience` (buyer) · `method-vocab` (archetype / value-lever vocabulary). Read
`brain_io-howto` in `_brain/` for the verbs; Brain-reachable-at-runtime (Drive connector, @iksula.com)
is an install precondition.
**Writes (brain_io write, append — raw first per `raw-capture-howto`):** `competitor-radar` for any
solution-specific findings (namespaced `competitor-radar-sa-YYMMDD`; `research-solutions` is the writer
of record for the standing radar) · `proof-catalogue` for any new win/proof surfaced.
**Reads from Spine:** the vertical-mapping **shortlist** + the opportunity record.
**Writes to Spine:** the **solution source-of-truth** (grounding + chosen edge) and the **handoff
section** (scope in/out, value metrics, segments, key messages, open questions) — the input contract to
Content / Delivery. *(Until the conductor is live, the Spine write is by record convention.)*

## Workflow (6 phases, 4 human gates)
0. **Intake & grounding** *(gate 1)* — read the shortlist + opportunity from the Spine; `brain_io get`
   `proof-catalogue` to identify the existing Iksula solution this builds on — **if unknown, ASK; never
   invent**. Restate opportunity, buyer, economic need. Sign-off.
1. **Solution outline** *(gate 2)* — name, buyer (from `icp-audience`), JTBD, concept, scope in/out.
2. **Competitive research** — start from `competitor-radar`; fill solution-specific gaps with live web
   research; **append sourced findings back (raw → `_raw/`, namespaced)**. Capture table-stakes.
3. **Differentiation** *(gate 3 — human-led)* — synthesise candidate wedges (Iksula assets × landscape
   gaps × economic lens) → user picks the edge (AskUserQuestion). Don't lock positioning alone.
4. **Build outputs** — Internal Solution Intro Deck + Client Pitch Deck (corporate intro, services,
   clients, **case studies from `proof-catalogue`**) using the `pptx` skill; on-brand per the brand spec
   in `proof-catalogue`/Brand Template.
5. **Verify & save** *(gate 4)* — every competitor claim sourced; no invented capabilities; buyer/need/
   edge consistent across outputs; the Internal deck is a clean input contract. Write the source-of-truth
   + handoff to the **Spine**; save decks in the solution folder.

## Outputs
A — **Internal Solution Introduction Deck** (primary + handoff contract): at-a-glance, buyer, need,
competitive landscape, differentiation, edge-in-practice, + the structured handoff section.
B — **Client Pitch Deck**: corporate intro (About/Services/Clients from `proof-catalogue`) → their world
& cost → future state → the solution → why Iksula/why now → case studies (real, from `proof-catalogue`) →
pilot CTA. C — **Source-of-truth note** (grounding + edge + sources) → the Spine asset record.
Default `.pptx`; one folder per solution under `Iksula_Strategy/Solutions/`.

## Operating principles
Productize don't consult · build on real assets (from `proof-catalogue`; if unknown, ask; never fabricate) ·
economic lens matches archetype · table-stakes ≠ differentiation · evidence sourced + current · human owns
the wedge · one source of truth (the Spine record) · standing intel lives in the Brain.

## Resources
- `brain_io-howto` + `raw-capture-howto` (in `_brain/`) · `references/deck-build-spec.md` *(unchanged)*.
- ~~`references/competitive-research-playbook.md`~~ → competitive research now reads/writes `competitor-radar`
  (standing radar owned by `research-solutions`).
