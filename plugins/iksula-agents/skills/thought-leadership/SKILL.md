---
name: thought-leadership
description: >-
  Produces Iksula's monthly opinion-led byline article that builds authority with senior buyers
  in the space where a solution lives. Reads voices, competitor-radar, icp-audience and
  proof-catalogue from the Brain via brain_io; reads/writes the editorial log + annual thesis as a
  Spine asset record. Owns no private registers. Trigger: "write the thought leadership article",
  "this month's article", "POV / byline piece".
---

# Thought Leadership (byline article that earns buyer trust — Brain-aware)

## Overview
A respected practitioner-thinker writing peer-to-peer to an expert reader. Advances how the buyer
thinks about a problem; demand follows trust. PACKAGES no product; invents no evidence. Thin: all
standing inputs from the Brain, continuity from the Spine.

## Brain & Spine I/O
**Reads (brain_io get):** `voices` (the roster + the byline personas to write AS) · `competitor-radar`
(what NOT to echo) · `icp-audience` (who the article is for) · `proof-catalogue` (proprietary
observations / anonymized proof — the differentiated evidence; never fabricate).
**Reads from Spine:** the solution source-of-truth (where Iksula earned the opinion) + the
**editorial log** (annual thesis, prior articles' claims, idea backlog, resonance).
**Writes to Spine:** the article + an **editorial-log update** (this thesis, claims made,
backlog changes, resonance to watch). *(Resonance is later enriched by Brain `performance-analytics`.)*

## Workflow (6 phases, 3 human gates)
0. **Intake & grounding** *(gate 1)* — read the editorial log + solution record from the Spine;
   `brain_io get` voices/competitor-radar/icp/proof. Restate space, byline, audience, annual-thesis fit. Sign-off.
1. **Discourse scan** — from `voices` (don't re-scan from scratch); map the roster's consensus +
   the unquestioned assumption; read `competitor-radar` for what to avoid.
2. **Topic & thesis** *(gate 2 — human-led)* — find the white space; one arguable thesis connecting
   two domains; present + get approval (AskUserQuestion).
3. **Draft** — in the byline's first-person voice (persona from `voices`); rigor + guardrails per
   `references/article-build-spec.md`.
4. **Self-critique** — deletion / platitude / steelman / "would a senior person already know this" tests.
5. **Verify & save** *(gate 3)* — update the **editorial log in the Spine**; save the article.

## Operating principles
Authority first; the deletion test; one arguable thesis; white space at the seams; evidence from
`proof-catalogue` only (never fabricate); steelman not strawman; no platitudes; human owns the thesis;
**the Brain is the roster/evidence and the Spine is the memory — keep nothing private**; stop-and-ask.

## Resources
- `brain_io-howto` (in `_brain/`) · `references/article-build-spec.md` *(unchanged)*
- ~~`references/roster-and-monitoring-playbook.md`~~ → **moved to the Brain** (`voices` + brain_io).
