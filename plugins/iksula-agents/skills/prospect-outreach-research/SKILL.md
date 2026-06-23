---
name: prospect-outreach-research
description: >-
  Iksula's pre-engagement prospecting Hand — a fast, basic research pass on a COLD prospect and their
  company that ends in ready-to-send LinkedIn outreach. Sits BEFORE client-research in the GTM value
  chain: cold/basic here, engaged/deep there. Runs in two modes — (SINGLE) one prospect → a Word
  dossier + a one-page brief + 5 outreach messages; (BULK) an .xlsx list of up to 10, paced → the full
  dossier written back as a new worksheet (one row per prospect) in a dated copy of the input file.
  Reads the prospect's role, activity and connection-degree from a logged-in LinkedIn Sales Navigator
  session in the browser, and company / platform / news from the public web. Brain-aware via brain_io
  (method-vocab, vertical-mapping, solutions-catalogue, icp-audience, voices) — READ-ONLY, no Brain or
  Spine write-back. Owns no register. Use when the user says "research this prospect", "prep outreach for
  this person", "run prospect-outreach-research", "bulk prospect research", or "draft LinkedIn outreach
  for a prospect".
---

# Prospect Outreach Research (pre-engagement prospecting — Brain-aware)

# Overview
The first research touch on a **cold prospect** — a named buyer at a named company we are **not yet
working with** — that ends in outreach you can actually send. It does a fast, basic read of the company,
their website/stack, and the person, then maps that to named Iksula offers and drafts five LinkedIn
messages. It is deliberately light: a first-pass to decide *is this worth pursuing, and how do I open the
conversation* — not a full account dossier.

It is **research → outreach prep, not selling and not diligence**. It does not run the funnel (`lead-gen`),
write the pitch deck (`solutions-architect-create`), or do the deep, engagement-grade account work
(`client-research`). It reads the Brain for context but **writes nothing back** — by design, to keep the
Brain and Spine lean.

**Where it sits — read this, it defines the lane:**
- **`prospect-outreach-research` (this skill) = PRE-engagement.** Cold prospect, basic research, goal is
  the first outreach. Runs against LinkedIn Sales Navigator.
- **`client-research` = POST-engagement (and deep pre-pitch).** Decision-grade account intelligence once
  we're engaged or about to pitch seriously — diligence, expansion, renewal, buyer profile. It supersedes
  this skill the moment the account warms up. Cold/basic = here; engaged/deep = there.
- `research-solutions` researches a **market / vertical**, not a single prospect.

## Help mode (print instructions, don't research)
If the user runs the skill with **"help"** (e.g. "prospect-outreach-research help" or "run
prospect-outreach-research help"), do NOT start any research. Print the help below in **plain English**,
then stop and wait:

> **Prospect Outreach Research — quick help**
>
> **What it does:** a fast, basic read of a cold prospect and their company, ending in 5 ready-to-send
> LinkedIn messages.
>
> **What you give it — one prospect:**
> - Company name
> - Website URL (use the country page if the company sells in more than one country)
> - The prospect's LinkedIn profile link
>
> **What you give it — many at once (bulk):** an Excel file (`.xlsx`), **one prospect per row**, with
> three columns: **Company**, **Website URL**, **LinkedIn URL**. Up to **10 rows** per run.
>
> **Before you run:** log in to **LinkedIn Sales Navigator** in your browser. The skill reads each
> profile through your logged-in session.
>
> **Limit:** **10 prospects per run**, paced with short pauses to keep your Sales Navigator account safe.
> Got more than 10? Split them into batches and run each batch.
>
> **What you get — one prospect:** a Word dossier, a one-page brief, and 5 LinkedIn messages (2 short
> connect notes, 2 warm, 1 direct).
>
> **What you get — bulk:** a dated copy of your Excel file with a new **"Prospect Research"** tab — one
> row per prospect, all the findings plus the 5 messages in columns. Your original file is left unchanged.

## The two modes (pick one at intake)
| Mode | When | Input | Output |
|------|------|-------|--------|
| **SINGLE** | Prepping outreach to one named prospect | company name · website URL · prospect LinkedIn URL | Word dossier + one-page brief + 5 outreach messages (copy-ready) |
| **BULK** | A shortlist to work through | an `.xlsx` with one row per prospect (company · website URL · LinkedIn URL), **up to 10 per run** | a **dated copy of the input file** with a new **`Prospect Research`** worksheet — full dossier as a table, one row per prospect, including 5 message columns |

If the mode isn't obvious from the input (a single prospect vs. a file of many), ASK (AskUserQuestion).
**Bulk is capped at 10 prospects per run and paced** (a pause between LinkedIn visits) — see the
account-safety rule below; if the list is longer, split into batches.

## Inputs (all mandatory)
- **Company name.**
- **Website URL** — the **country-specific** URL when the company is multi-country (so platform, product
  count and categories reflect the right market).
- **Prospect's LinkedIn profile URL.**

If any of the three is missing, ASK before researching — don't guess the entity, the market, or the person.

## LinkedIn via Sales Navigator (account-safety — non-negotiable)
This skill assumes a **logged-in LinkedIn Sales Navigator session in the browser** (the Claude-in-Chrome
tools), used to read the prospect's lead/account page: role, responsibilities, recent activity/posts, and
**connection degree + shared connections**. Public web search is the fallback when the browser session
isn't available, and it then marks the connection check and activity as "not available".

- **Pace and cap.** In BULK, visit at most ~10 profiles per run with a deliberate pause between each.
  Rapid, high-volume profile visits look like automation to LinkedIn and can get the account warned or
  restricted. Protect the user's real Sales Navigator account over throughput.
- **Public / professional only.** Role, tenure, posts, shared connections — yes. No private data, no
  scraping behind anything the logged-in user can't normally see, no personal-life detail.

## Brain I/O (READ-ONLY — no write-back)
**Reads (brain_io get / Drive read):**
- `method-vocab` — the controlled vocabulary + the vertical process-mapping rubric, so "nature of
  business" maps to the **same** L1/L2/L3 labels every other Iksula skill uses. Do NOT redefine locally.
- `vertical-mapping/` (Brain folder) — the latest vertical process-mapping outputs / solution shortlist,
  to place the prospect's business and surface likely automation opportunities.
- `solutions-catalogue` — Iksula's packaged, sellable solutions; map the prospect's needs to **named**
  offers, never invented generic ones.
- `icp-audience` — buyer / fit lens; how well this prospect matches who we sell to.
- `voices` + recent content records — the thought-leadership pieces and posts to forward to the prospect.

Read `brain_io-howto` in `_brain/` for the exact verbs. Brain-reachable-at-runtime (Drive connector,
signed in @iksula.com) is the precondition.

**Writes: NONE.** This skill **does not write to the Brain or the Spine** — no register append, no Spine
record, no `_brain/_raw/` dump. Raw evidence (sources, URLs, access dates) is kept **with the deliverable**
(in the local working folder / alongside the output), not in the Brain. This is intentional: the skill is
a high-frequency, top-of-funnel tool and writing every prospect back would overload the Brain. If a
prospect warms into a real opportunity, hand it to **`client-research`**, which owns the Brain/Spine
write-back.

### Graceful fallback (works cold)
If the Brain isn't reachable, **degrade to standalone**: do the public web + Sales Navigator research, flag
solutions / fit / content-to-forward as provisional pending Brain access, and never fabricate Brain content
to fill the gap.

## PART A — The Agent's Mandate (summary)
- **Purpose:** turn three inputs (company, site, person) into a fast, sourced, basic read of a cold
  prospect and **five ready-to-send LinkedIn messages**, so a seller can open the conversation today.
- **Scope (in):** company basics (nature of business mapped to our vertical, key categories, public vs
  private, estimated revenue, last-12-month news); website (eCommerce platform, PIM if detectable,
  approx. product count); prospect (role & responsibilities, public online presence, direct-connect +
  shared connections); outreach approach (named Iksula solutions to pitch, content to forward, 5 drafted
  messages). **(out):** deep/engagement-grade diligence, the pitch deck, the funnel/sequence execution,
  sending the messages, market sizing — all downstream or sibling-owned.
- **Owns:** nothing standing. Writer-of-record for no Brain module; writes nothing back.
- **Place in the pipeline:** **prospect-outreach-research (pre-engagement)** → (if it warms)
  `client-research` (post-engagement) → Solutions Architect / Lead Gen. Owner: **DJ**.

## PART B — The Deliverables
| Deliverable | Format | Notes |
|-------------|--------|-------|
| **SINGLE — Prospect dossier** | `.docx` (Iksula brand) | The full basic read, sourced. Every fact carries a source; estimates and low-confidence items (revenue, PIM) flagged. Built with the **docx** skill. |
| **SINGLE — One-page brief** | `.docx`/`.md`, 1 page | The read-ahead: who, the hook, the fit, the angle — plus the 5 messages inline. |
| **SINGLE — Outreach messages** | copy-ready block | 5 drafts: **2 connect notes** (≤300 chars), **2 warm InMails**, **1 direct InMail**. |
| **BULK — Results worksheet** | new tab in a **dated copy** of the input `.xlsx` | One row per prospect; columns = the full dossier fields + **5 message columns** (Connect note 1, Connect note 2, Warm InMail 1, Warm InMail 2, Direct InMail). Built with the **xlsx** skill. Original file is never overwritten. |
| (always) — Raw evidence | local, with the deliverable | Sources + URLs + access dates captured **before** distilling; every published fact traces back here. **Not** written to the Brain. |

Tell the user which deliverables you're producing and **ask which folder to save the rendered files to**.

## Workflow (5 phases, 1 human gate)
0. **Intake & scope** *(gate)* — confirm the **mode** (single vs bulk), the **three inputs** per prospect,
   and for bulk the **batch size (≤10)**. `brain_io get` `method-vocab`, the latest `vertical-mapping`
   output, `solutions-catalogue`, `icp-audience`, and the `voices`/content records. Confirm the entity and
   the country/market (which site, which subsidiary) — **never guess**. Restate scope; confirm before
   researching.
1. **Capture (raw-first, kept local)** — run the research and record every source, figure, quote, URL and
   access date as you go, alongside the deliverable. Nothing is distilled until it exists as raw. **Verify
   present-day facts with search, not memory** — leadership, ownership, financials and tech change.
2. **Company & website read** — nature of business mapped to the **vertical rubric** (`method-vocab` /
   `vertical-mapping`); key categories; public vs private limited; **estimated revenue** (range + source,
   or "not found" — always an estimate, never asserted); last-12-month news; **eCommerce platform**
   (from site code signatures; use the browser if the site is JavaScript-rendered); **PIM** system
   (best-effort, inferred from job posts / case studies / press — often "unknown", flag low-confidence);
   **approx. product count** (sitemap / category counts). See `references/research-method.md`.
3. **Prospect read (Sales Navigator)** — role & responsibilities; public presence across LinkedIn / X /
   Substack / YouTube (articles published; comments only if reachable); **direct LinkedIn connect?**
   (degree + shared connections). Public/professional only; paced per the account-safety rule.
4. **Fit, angle & messages** — map needs to **named `solutions-catalogue` offers**; pick **content to
   forward** from `voices`/content; check fit against `icp-audience`. Draft the **5 messages** tuned to
   the person and the hook (2 connect notes ≤300 chars, 2 warm, 1 direct). Then **verify**: every fact
   traces to raw + a source; estimates and inferences labelled; **prospect-stage discipline — never
   present an inference or a hoped-for fit as a confirmed fact.** Produce the deliverables (single docs,
   or the bulk worksheet write-back) and show the user the headline findings + sources.

**Human gate** routes to Slack `#agentic-org-requests` (✅ proceed / ✍️ revise / ⏸ hold) when running
inside the conductor; standalone, confirm with the user in-session.

## Operating principles
- **Pre-engagement, basic by design** — this is a fast first read to open a conversation, not a deep
  dossier. When the account warms, hand off to `client-research`.
- **Protect the LinkedIn account** — pace and cap profile visits; throughput never beats keeping the
  user's Sales Navigator account in good standing.
- **Sourced over asserted** — present-day facts come from search, not memory; keep a defensible source
  list. Mark unverified items TBD.
- **Estimate honestly** — revenue is a range with a source or "not found"; PIM is usually "unknown".
  Label every inference ("postings mention Akeneo → possible PIM, to validate"). False confidence is the
  enemy.
- **Reuse the Brain, own nothing, write nothing** — score and label with `method-vocab`; map to named
  offers from `solutions-catalogue`; forward real content from `voices`. Never fabricate Brain content;
  never write back. Fall back to standalone when the Brain is dark.
- **Fit must be earned** — every "why Iksula" angle names a real, catalogued offer; no offer, no claim.
- **Five messages, ready to send** — 2 connect notes (≤300 chars), 2 warm, 1 direct; specific to this
  person, not boilerplate.
- **Privacy & propriety** — public, professional information only; never cold-research private life;
  never treat an existing client as a cold prospect (that's `client-research`'s lane).

## Anti-patterns to avoid
- Treating this like `client-research` — over-researching a cold prospect into a 20-page dossier.
- Hammering LinkedIn: visiting dozens of profiles fast and risking the user's Sales Navigator account.
- Stating estimated revenue, inferred PIM, or the tech stack as confirmed fact with no flag.
- Writing the pitch deck or a full outreach sequence (that's the Architect / Lead Gen).
- Writing anything back to the Brain or Spine (this skill is read-only by design).
- Generic, copy-paste outreach that ignores the person's role, posts and shared connections.
- Researching the whole market when the ask was one prospect (that's `research-solutions`).
- In bulk, overwriting the user's input file instead of writing a dated copy with a new worksheet.

## Conventions (do not remove)
- Brand: Carlito, primary red `#9A0D15`, light cards — for the dossier / one-pager when rendered as
  documents. Brand assets via `proof-catalogue` / `Iksula FY27/Brand Template/`.
- File naming: `Name - YYMMDD` (v1/v2 for same-day). Ask the user which folder to save rendered files to.
  In bulk, the output is a dated copy of the input workbook — never overwrite the original.
- Plain US English (grade 6–8) in chat replies and plain-language explanations.
- Use `${CLAUDE_PLUGIN_ROOT}` for intra-plugin paths; never hardcode absolute paths.
- Do the research first; then read the relevant format skill (`docx`/`xlsx`) and build.

## Resources
- `brain_io-howto` (in `_brain/`) — the read verbs (authoritative).
- `${CLAUDE_PLUGIN_ROOT}/skills/prospect-outreach-research/references/mandate.md` — the authoritative spec
  (scope, lane vs. `client-research`, the value-chain placement, modes, batch cap, I/O contract).
- `${CLAUDE_PLUGIN_ROOT}/skills/prospect-outreach-research/references/research-method.md` — the source map,
  the platform/PIM/product-count detection method, the Sales Navigator method + pacing, confidence rules.
- `${CLAUDE_PLUGIN_ROOT}/skills/prospect-outreach-research/references/deliverable-templates.md` — the
  dossier outline, one-pager, the bulk results-table column spec, and the 5-message templates.
- **Sibling iksula-agents (reuse, don't re-derive):** `client-research` (deep, post-engagement account
  intelligence — the warm-up handoff) · `solutions-architect-create` (turns fit into a pitch) · `lead-gen`
  (works the prospect as a funnel/ABM target).
