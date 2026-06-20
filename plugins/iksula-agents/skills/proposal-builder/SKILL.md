---
name: proposal-builder
description: >-
  Iksula's proposal-building Hand — turns a qualified opportunity into a CEO-ready client proposal by
  COPYING the latest approved reference file and editing only the client-specific sections IN PLACE.
  It does NOT rebuild sections or reinvent the format: it outlines and fills the existing structure.
  Keeps the locked chrome (cover, live Table of Contents, header/footer, border) and the kept-as-is
  sections (About Iksula, Commercials, Payment Terms, Support & AMS, Delivery Assumptions), and marks
  every human-swap point — logo, proposal name, header client-logo, support hours/timezone/SLA/scope —
  with a visible highlight for the user to change. Reads proof-catalogue, solutions-catalogue,
  icp-audience and method-vocab from the Brain via brain_io; reads the client dossier, the solution
  asset record and the effort/scope workbook from the Spine; writes the finished proposal + record back
  to the Spine. Owns no standing register. Trigger: "build the proposal", "build a client proposal",
  "draft the proposal for <client>", "run the proposal builder", "make the CEO proposal".
---

# Proposal Builder (CEO-focused client proposals — Brain-aware)

## Overview

The Hand that converts a qualified, scoped opportunity into a proposal a CEO will read and say yes to. It **outlines the structure and fills it — it does not rebuild sections**. It starts from the latest approved reference `.docx`, keeps the locked format and chrome, edits only the client-specific narrative in place, and **highlights** every spot a human must swap rather than silently guessing. It does **not** invent scope, pricing or case studies — those arrive from the Spine. Episodic; owns no standing register; the approved reference `.docx` is its locked template.

## Brain & Spine I/O

**Reads (brain_io get):** `proof-catalogue` (case studies — ≥3, reframed as our work only, Appendix B) · `solutions-catalogue` (the packaged solution; scope + approach) · `icp-audience` (the buyer/CEO lens) · `method-vocab` (controlled delivery vocabulary so phases/AI-leverage language stays consistent). Read `brain_io-howto` in `_brain/` for the verbs; Brain-reachable-at-runtime (Drive connector, @iksula.com) is an install precondition. **Writes (brain_io write, append — RAW FIRST per `raw-capture-howto`):** every input gathered (client situation, effort numbers, chosen case studies + sources) to `_brain/_raw/` **before** any number reaches the proposal. Owns no register — never the writer of `proof-catalogue`/`solutions-catalogue`; if new reusable proof surfaces, hand it to that register's writer-of-record. **Reads from Spine:** the **client dossier** (client-research) · the **solution asset record** (solutions-architect) · the **effort/scope workbook** (authoritative effort, timeline, commercials). **Writes to Spine:** the finished **proposal `.docx`** + a **proposal record** (client, version, differentiator, the seven CEO answers, source links) into `_spine/assets/`. *(Until the conductor is live, the Spine write is by record convention.)*

## Proposal structure & edit map

Copy the reference; act on each element per the **Action** column. **Never rebuild a KEEP element from scratch; never silently fill a HIGHLIGHT element.** Section numbers follow the latest reference instance.

| # | Element | Action | Notes |
|---|---------|--------|-------|
| Cover | Cover page (content control [0]) | **KEEP layout + HIGHLIGHT swaps** | Keep design exactly. Highlight the **logo** (user replaces with client/Iksula logo) and the **proposal name/title** (user edits). Cover text is edited manually in Word. |
| TOC | Table of Contents (content control [1]) | **KEEP — must render** | Live TOC field stays. User refreshes with **F9** in Word after edits so all sections appear. Never delete or retype it. |
| Header | Page header | **KEEP + HIGHLIGHT** | Highlight a note that the **client logo in the header is to be changed** by the user. |
| Footer | Page number | **KEEP** | Untouched. |
| Exec Summary | Executive Summary | **REWRITE (Claude/user)** | Lead with the differentiator; the client situation, why-us, what-we-deliver + headline timeline. The one section guaranteed to be read. |
| 1 | About Iksula | **KEEP** (boilerplate) | Do not change the capability statement. Only **1.1 Relevant Experience** is reshaped to the client's problem type + case-study selection. |
| 2 | Our Understanding | **REWRITE per client** | Current state, the job, constraints (live/shared/partner/benchmarks). |
| 3 | Detailed Solution / Approach specifics | **REWRITE per client** | Channels/modules, shared-core reuse, what the client gets. Module detail → Appendix A. |
| 4 | Design Approach | **REWRITE per client** | Principles, journeys, deliverables for this client. |
| 5 | Our Approach for Delivery (+ AI) | **REWRITE per client** | Phases + headline timeline; honest activity-level AI leverage (no hype). Detail → Appendices C/D. |
| 6 | Architecture / Scale | **REWRITE per client** | Stack rationale, scale, integration. Data-flow detail → Appendix F. |
| 7 | Scope of Work | **REWRITE summary, point to A** | One-paragraph summary + pointer to Appendix A (the authoritative scope). |
| 8 | Commercials | **KEEP structure; update deal figures only** | Wording/table/terms locked; only the numbers change. Support-allocation figure here must match Appendix A3. |
| 9 | Payment Terms | **KEEP T&C verbatim; only the milestone split is project-specific** | All terms/rates/clauses locked (see library §9). The **milestone % split is the ONLY edit and MUST match the project plan**, total 100%. Do not rewrite the section. |
| 11 | Assumptions | **LINE-LEVEL (standard frame, project-specific slots)** | Per library §11: 11.1 categories + 11.2 principles KEEP; fill only `⟪…⟫` slots. **11.3 Delivery Assumptions = KEPT-AS-IS** (only timeline-weeks / parity slot). Edit lines, not the section. |
| 12 | Exclusions | **LINE-LEVEL** | Per library §12: standard exclusions stay verbatim; swap only the project-specific carve-outs. Delete the prior client's specific lines. |
| 13 | Change Control | **KEEP** | Locked process; links to ownership of fixes. |
| App A1/A2 | Scope of Work (detailed) | **REWRITE per client** | The authoritative functional scope, module by module, per channel. |
| App A3 | **Support and AMS** | **KEEP body (incl. A3.2 Engagement Structure) + HIGHLIGHT 4 swaps** | A3.1 BAU + **A3.2 Engagement Structure kept entirely as-is**. Highlight only: (1) support hours/month, (2) timezone, (3) SLA, (4) level/scope. |
| App B | Case Studies (≥3) | **SELECT per client** | From `proof-catalogue`; reframed as our work only — no vendor commentary. |
| App C–G | Delivery / AI-by-activity / Tech / Architecture / Risk | **REWRITE per client** | All depth lives here; the body only points to it. |

## Standard vs project-specific (edit lines, not sections)

**The #1 rule for the "standard" sections — Payment Terms, Support & AMS, Assumptions, Exclusions.** Claude's failure mode is rewriting a whole section when only a few lines are project-specific, which destroys firm-standard wording and legal boilerplate. Prevent it:
- Treat every line as either 🔒 **STANDARD** (firm-wide, copied **verbatim** — never edited/deleted/reworded) or ✏️ **PROJECT-SPECIFIC** (a `⟪…⟫` slot — the only thing that changes). The split for each section is defined in **`references/boilerplate-library.md`** — read it before touching these sections.
- **Edit by matching, not rewriting:** pass STANDARD lines through untouched; fill only the `⟪…⟫` slots from the dossier / solution record / **project plan** / effort workbook; leave unsourced slots **highlighted** for the user.
- **Delete the prior proposal's sample project-specific lines** (they belong to *that* client) and replace with this project's — never carry another client's specifics forward.
- **Reconcile cross-references:** payment milestones ↔ project plan (total 100%); §8 support hours ↔ Appendix A3; all numbers consistent.
- A line that fits neither bucket → **stop and ask**, don't assume.

## Highlight convention (do not silently fill)

Anything a human must change is **marked, not guessed**. Wrap each swap point in a visible **yellow text-highlight** with a bracketed instruction, e.g. `⟪REPLACE — client logo⟫`, `⟪EDIT — proposal title⟫`, `⟪SET — support hours / timezone / SLA / scope⟫`. Claude fills only what it has sourced evidence for; logos, brand marks, and any value not in the dossier/workbook stay highlighted for the user. The user resolves all highlights and refreshes the TOC (F9) before sending.

## Workflow

1. **Intake & scope.** brain_io get the four modules; read the dossier, solution record and effort workbook from the Spine. Fill the Playbook **Placeholders** (§9). Any missing placeholder → **stop and ask**; never invent scope, a number or a constraint.
2. **Raw-first capture.** Dump every input (situation, effort/timeline/commercials, chosen case studies + sources) to `_brain/_raw/`. Nothing enters the proposal that isn't traceable to raw + source; numbers must agree across the whole document.
3. **Copy, don't recreate.** Start from the latest approved reference file and copy it. Do not touch the locked chrome (format, cover, live TOC, header/footer, border) or the KEEP sections — per the edit map.
4. **Fill the structure in place.** Walk the edit map: REWRITE the client sections to one storyline, KEEP the locked ones (deal figures only), and HIGHLIGHT every human-swap point. Keep the body lean — each point = a short outcome + a pointer; push all depth to Appendices A–G.
5. **Verify.** Run the CEO Decision Checklist (Playbook §7 — seven questions answered in the right place) and the Pre-Flight Checklist (§8). Confirm TOC renders, effort/timeline/commercial numbers are consistent, Appendix A is the authoritative scope, and **all highlights are present where a human must act**.
6. **Gate, then hand off.** Route to the deal owner for sign-off (Human gate) before the client sees it. On ✅, write the `.docx` + record to `_spine/assets/`.

## Hard language rules (Playbook §2 - every line)

Plain, positive, professional · no buzzwords/filler · **no negatives, no commentary on any other vendor anywhere** (reframe past work as our work only) · bullets + short paragraphs with bold lead-ins · each point = outcome + pointer, not the detail · numbers credible and consistent · **never use an em-dash (—) or en-dash (–) - use a plain hyphen ( - ) everywhere, including in any text Claude writes or edits**.

## Human gate

**Proposal sign-off by the deal owner / sales lead** before it is sent to the client — routed by the Spine to Slack `#agentic-org-requests` (✅ approve / ✍️ revise / ⏸ hold). A client-CEO proposal never leaves on the agent's authority. The user manually edits cover text, resolves all highlights, and refreshes the TOC (F9) in Word as the final step.

## Operating principles

Outline and fill — never rebuild sections · **edit lines, not sections — keep STANDARD boilerplate verbatim, change only `⟪…⟫` project-specific slots, drop the prior client's sample lines** · copy the format, never reinvent it · keep the chrome and the KEEP sections intact · highlight every human-swap point, never silently guess · reconcile payment milestones to the project plan · one storyline, not sections · lean body / deep appendix · reach commercials fast · lead with the differentiator · honest over impressive · raw-first, every number traceable to raw + source · own no register · stop-and-ask on any missing placeholder · gate before the client ever sees it.

## Conventions (do not remove)

- **Two brands, deliberately separate.** The **client proposal** uses the **locked reference identity — Poppins, warm blue `#4A66AC`, navy `#243255`, light fill `#D9DFEF`, US-Letter** — and must NOT be reskinned to the iKshana internal brand. The iKshana house brand (**Carlito, primary red `#9A0D15`, light cards**) applies only to *internal* artifacts (the Spine record, internal summaries), never the client-facing `.docx`.
- **File naming:** `Iksula_<Client>_<Solution>_Proposal_v<N>_DDMonYYYY.docx` (match the reference); internal records `Name - YYMMDD` (v1/v2 same-day). Ask the user which folder to save to.
- **Verbs, not paths:** reach the Brain only via `brain_io`; append-only, raw-first; one writer per module — this skill writes to no register.
- **Punctuation:** plain hyphen ( - ) only - never an em-dash (—) or en-dash (–), anywhere in the document.
- Use the plugin root for intra-plugin paths; never hardcode absolute paths.

## Resources

- **Authoritative format + build spec:** `references/proposal-playbook.md`.
- **Standard vs project-specific line classification (READ before editing Payment / Support / Assumptions / Exclusions):** `references/boilerplate-library.md`.
- **Reference file to copy:** start from the latest **approved proposal instance in `_spine/`** when one exists (it carries the live cover [0] + TOC [1] and Support & AMS in Appendix A3). If there is no recent approved instance, copy the bundled clean template `assets/Iksula_Proposal_TEMPLATE_v1_19Jun2026.docx`. Always copy the newest approved file, never rebuild from scratch.
- `brain_io-howto` + `raw-capture-howto` (in the Brain `_brain/`) · the client dossier, solution asset record and effort workbook in `_spine/`.
