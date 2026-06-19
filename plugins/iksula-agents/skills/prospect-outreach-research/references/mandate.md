# prospect-outreach-research — Mandate (authoritative spec)

The full contract for the skill. The SKILL.md is the operating summary; this file is the source of truth
for scope, lane, modes and the I/O rules.

## Purpose
From three inputs — **company name, (country-specific) website URL, prospect LinkedIn URL** — produce a
fast, sourced, *basic* read of a **cold prospect** and their company, ending in **5 ready-to-send LinkedIn
messages**. Goal: let a seller decide *is this worth pursuing* and *how do I open the conversation*, today.

## Lane — vs `client-research` (the defining boundary)
- **This skill = PRE-engagement.** Cold prospect. Basic depth. Output = outreach. Runs on LinkedIn Sales
  Navigator. **Writes nothing back** to the Brain/Spine.
- **`client-research` = POST-engagement / deep pre-pitch.** Decision-grade account intelligence once the
  account is engaged or about to be pitched seriously (diligence, expansion, renewal, buyer profile). It
  **owns the Brain/Spine write-back.** It supersedes this skill the moment the prospect warms up.
- The GTM value chain order (recorded in the Agentic Org Vision doc, owner DJ):
  **prospect-outreach-research → client-research → Solutions Architect / Lead Gen.**

## Modes
| Mode | Trigger | Input | Output | Cap |
|------|---------|-------|--------|-----|
| **SINGLE** | one named prospect | company · site · LinkedIn URL | `.docx` dossier + 1-page brief + 5 messages | — |
| **BULK** | a shortlist | `.xlsx`, one row/prospect (company · site · LinkedIn) | new `Prospect Research` worksheet in a **dated copy** of the input file | **≤10 per run, paced** |

## Scope
**In:**
- Company: nature of business (mapped to the vertical rubric), key categories, public vs private limited,
  estimated revenue (range + source), last-12-month news.
- Website: eCommerce platform, PIM system (best-effort), approx. product count.
- Prospect: role & responsibilities, public online presence (LinkedIn/X/Substack/YouTube), direct
  LinkedIn connect + shared connections.
- Outreach: named Iksula solutions to pitch, content to forward, 5 LinkedIn messages.

**Out (downstream or sibling-owned):** deep/engagement diligence (`client-research`); the pitch deck
(`solutions-architect-create`); funnel/sequence execution and sending (`lead-gen`); market sizing
(`research-solutions`); any Brain/Spine write.

## I/O contract
**Reads (brain_io get / Drive read, @iksula.com):** `method-vocab`, `vertical-mapping/` (latest),
`solutions-catalogue`, `icp-audience`, `voices` + recent content records.

**Writes:** NONE — no register, no Spine record, no `_brain/_raw/`. Raw evidence is kept locally with the
deliverable. Rationale: top-of-funnel, high-frequency; writing every prospect would overload the Brain.
The warm-up handoff to `client-research` is where account memory gets written.

**External:** LinkedIn **Sales Navigator** via the logged-in browser session (role, activity,
connection-degree, shared connections); public web for company/site/news/platform.

## Account-safety rule (LinkedIn)
Cap bulk at ~10 profiles/run; pace visits with a pause between each. High-volume rapid visits risk a
LinkedIn warning/restriction on the user's real account. Throughput never beats account standing.
Public/professional information only.

## Gate
One human gate at intake (scope/mode/inputs/batch). Routes to Slack `#agentic-org-requests`
(✅ / ✍️ / ⏸) inside the conductor; standalone, confirm in-session.

## Definition of done
- Mode and inputs confirmed; entity/market unambiguous.
- Every fact sourced; estimates (revenue) and inferences (PIM, stack) flagged; nothing fabricated.
- Single: dossier + brief + 5 messages rendered; folder confirmed. Bulk: dated copy written with the new
  worksheet; original untouched.
- No Brain/Spine writes performed. Warm prospects flagged for `client-research`.
