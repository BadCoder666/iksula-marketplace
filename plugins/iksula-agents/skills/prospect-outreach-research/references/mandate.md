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
| **BULK** | a shortlist (any length) | `.xlsx`, one row/prospect (company · site · LinkedIn) | new `Prospect Research` worksheet in a **dated copy** of the input file | **batches of 10, paced; auto-loops with a short break between batches; HARD STOP at 200/run; max 200 per rolling 4h** |

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

## Account-safety rule (LinkedIn) + bulk limits
Process bulk in **batches of 10 profiles**, pacing visits with a pause between each profile, and a short
break (default **5 minutes**) between batches. **Auto-loop** until the file is exhausted (the user never
pre-splits it), writing each batch into the output as it completes (incremental save). Enforce two hard
limits: a **HARD STOP at 200 prospects per run**, and **no more than 200 prospects per rolling 4-hour
window** — tracked in a small **local run-log** (timestamp + count per batch). At intake, sum the last
4 hours from the run-log: if ≥200, do not run and give the earliest resume time; if a partial budget
remains, process only up to it. The run-log is an agent-side guardrail, not a system lock — honour it and
never bypass it to finish faster. If LinkedIn shows a checkpoint or rate/security warning, STOP, save
progress, and tell the user. Throughput never beats account standing. Public/professional information only.

## Gate
One human gate at intake (scope/mode/inputs/batch). Routes to Slack `#agentic-org-requests`
(✅ / ✍️ / ⏸) inside the conductor; standalone, confirm in-session.

## Definition of done
- Mode and inputs confirmed; entity/market unambiguous.
- Every fact sourced; estimates (revenue) and inferences (PIM, stack) flagged; nothing fabricated.
- Single: dossier + brief + 5 messages rendered; folder confirmed. Bulk: dated copy written with the new
  worksheet (written incrementally, batch by batch, until the whole file is processed); original untouched.
- No Brain/Spine writes performed. Warm prospects flagged for `client-research`.
