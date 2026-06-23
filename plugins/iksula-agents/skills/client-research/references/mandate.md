# Client Research — Mandate (authoritative spec)

The single source of truth for what this Hand does and does not do. The SKILL.md is the operating
summary; this file is the contract. If the two ever disagree, fix the SKILL.md to match this.

## 1. Purpose
Turn public signal + the Iksula Brain into a **sourced, decision-grade view of ONE named account**, for
a specific account moment, and leave the firm's account memory richer than it found it. The output is
materials a seller or delivery lead actually uses to make a decision and take a next step — not a
research essay.

## 2. The account lifecycle this Hand serves (modes)
One skill, four modes. The mode is chosen at intake and decides emphasis, dossier shape and next action.
A/B/C are **company-level**; D is **person-level** and usually layers onto one of them.

- **A — Prospect Dossier.** The account is a target we have not yet engaged (or are about to first
  pitch). Centre of gravity: *who they are, what's changing (the timely hook), the Iksula-fit angle, the
  buying signals, and the way in.* Output buyer: Sales / Lead Gen / Solutions Architect.
- **B — Pre-Engagement Diligence.** Work is won or about to start; the team must walk in informed.
  Centre of gravity: *org & stakeholders, the tech/system landscape, incumbents and competitors already
  in the account, delivery risks, and the context the team needs on day one.* Output buyer: the delivery
  / engagement lead.
- **C — Account Expansion / Renewal.** An existing client we want to grow and retain. Centre of gravity:
  *whitespace and expansion plays, what's changed since we started, renewal risk signals, and the
  relationship map.* Output buyer: the account manager / Solutions Architect. **Compliance:** an existing
  client is on the suppression list for cold outreach — expansion goes through the relationship, never a
  cold sequence.
- **D — Buyer Profile.** We are about to pitch/meet a **specific named person** and want the pitch tuned
  to *them*, not just the company. Centre of gravity: *the individual — background, tenure, prior roles,
  mandate, what they measure, public views/posts, believer-vs-skeptic, and how to pitch to them.* Runs
  **layered onto A/B/C** (research the company AND the person) or **standalone** ("profile this person
  before my call"). The account research answers *what to pitch*; the buyer profile answers *how to pitch
  it to this person*. Output buyer: the seller / whoever is in the room, and the Solutions Architect who
  builds the person-tailored pitch. **Boundary:** professional, role-based, public information only — the
  goal is selling well to a person, never surveillance of one. The **pitch itself is the Architect's**;
  this Hand supplies the profile + the "how to pitch" read, not the pitch.

### Note on the tech stack → recommendation seam
Mode B (and A) infer the client's **tech & system landscape**. This Hand must make that landscape
*recommendation-ready*: each inferred system is mapped to the **named `solutions-catalogue` offer + the
integration hook** it implies, so the Solutions Architect writes a *specific* recommendation rather than
re-deriving it. The mapping is research's job; the recommendation/pitch built from it is the Architect's.

## 3. Scope
**In:** company snapshot; financial & strategic read; trigger events / what's changing; tech & system
landscape (inferred, labelled) **mapped to named offers + integration hooks**; competitor & incumbent
presence in the account; stakeholder / buyer map; **buyer profile of named individuals (Mode D) + the
"how to pitch to them" read**; Iksula-fit angle mapped to named solutions + proof; fit/priority scoring;
recommended next action.

**Out (downstream or sibling-owned):**
- the pitch / proposal / pricing → `solutions-architect-create`
- the outreach sequence / funnel work / de-anonymization → `lead-gen`
- running the engagement / workshops / roadmap → `ai-transformation-consultant`
- market sizing / vertical teardown / the standing competitor radar → `research-solutions`
- the buyer-truth register → `icp-audience` (shared; read-only here)

## 4. Lane vs. siblings (do not blur)
- **vs. `research-solutions`:** that Hand researches a **market / vertical / opportunity** and owns the
  standing `competitor-radar`. This Hand researches **one named company** and owns no register.
- **vs. `ai-transformation-consultant` → `client-research.md`:** that internal reference researches a
  client **specifically to prep an AI-transformation workshop program**. This skill is **engagement-
  agnostic** account intelligence for the whole GTM motion; when the downstream engagement *is* an AI
  transformation, this dossier is the richer upstream input that consultant consumes.
- **vs. `icp-audience`:** that register is the *generic* buyer truth across accounts. This Hand produces
  the *specific* stakeholder map for one company, grounded in that generic truth — and never rewrites it.

## 5. Ownership
- **Standing registers owned:** none. Writer-of-record for nothing.
- **Single source of truth produced:** the **Spine account record** for the company (one per account,
  versioned append-only).
- **Contributes (append-only, namespaced):** new sourced competitive intel → `competitor-radar-clientresearch-YYMMDD`;
  new sourced proof (with consent) → `proof-catalogue`.

## 6. I/O contract (summary — full verbs in `brain_io-howto`)
**Reads (brain_io get):** `icp-audience`, `competitor-radar`, `proof-catalogue`, `solutions-catalogue`,
`method-vocab`, and any prior Spine account record for the company.
**Writes (brain_io write, append-only, raw-first):** raw → `_brain/_raw/client-research-raw-<company>-YYMMDD.md`;
namespaced competitive append → `competitor-radar-clientresearch-YYMMDD`; proof append → `proof-catalogue`.
**Spine:** the account record + source-of-truth note + handoff section.

## 7. Human gates
- **Gate 1 — scope confirmation** (after intake, before research): company, mode, trigger, audience,
  deliverables wanted.
- **Gate 2 — accuracy sign-off** (after distil, before the Brain/Spine write is finalised): headline
  findings + sources shown to the user.
Inside the conductor, gates post to Slack `#agentic-org-requests` (✅ / ✍️ / ⏸). Standalone, confirm
in-session.

## 8. The four non-negotiables (inherited from the Brain contract)
1. **Append-only / versioned** writes — never overwrite a Brain or Spine file.
2. **One writer per module** — namespace shared appends (here: `-clientresearch-`).
3. **Raw-first** — dump raw to `_brain/_raw/` before distilling; no published number untraceable to raw + source.
4. **Human gates to Slack** `#agentic-org-requests`.

## 9. Definition of done
- The named account is researched in the chosen mode; every fact is sourced; every inference labelled.
- Requested deliverables (A/B/C) are produced, brand-compliant, saved to the user's chosen folder.
- Raw is captured first; the Spine account record + source-of-truth note + handoff are written; new
  competitive intel is appended namespaced.
- The dossier ends on a recommended next action with an owner, and is handed to the right downstream Hand.
- Nothing is fabricated; the Brain's registers are unrewritten; the user has signed off on accuracy.
