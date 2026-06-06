# Iksula Agentic Organisation — Colleague Guide

The complete guide to working inside Iksula's agentic architecture: how it's built, how
to plug into it, and how to create, update, and use skills. This supersedes the earlier
"Colleague Onboarding Pack — Building Your Agent."

---

## 0. Who this is for, and how to read it

You're joining as one of two kinds of contributor:

- **Skill creators** — you build or improve the agents (skills) themselves. Read everything,
  but §3.3, §3.4 and §2 (the Brain) are your core.
- **Solution creators** — you *use* the skills to produce sellable outputs (e.g. productize a
  Staffing Services solution, run a content cycle). §3.1, §3.2, §3.5 and §4 are your core;
  you can skim the build-side sections.

Two rules will save you the most confusion, so read them first:

1. **Using a skill to make a deliverable is not the same as changing a skill.** Producing a
   Staffing Services solution by running `solutions-architect-create` is *consumption* — no
   pull request, the output goes to a solution folder, not a repo. Only changing a *shared
   skill* triggers the governance flow. (Full detail in §3.5 and §5.)
2. **Solutions are not skills.** A "solution" (e.g. PC2, Staffing Services) is a sellable
   offering produced *by* the skills. A "skill" is a reusable agent. Don't commit solution
   deliverables into the marketplace.

---

## 1. The vision and architecture

Iksula's agentic organisation is a *decomposed* operating system: instead of a few large,
do-everything agents, it is many **thin** agents that each do one craft, read shared context,
and hand off cleanly. The whole design rests on three layers — **Brain, Hands, Spine** — and
two **loops**.

### The three layers

**The Brain — shared, standing intelligence, built once and read by every Hand.** A single
repository of context that *outlives any one cycle*: who the influential voices are, what
competitors are shipping, who the ideal customer is, what proof we can cite, what each channel
rewards, what's working in performance data, the scoring vocabulary, and the solutions
portfolio. No agent keeps private copies of this; they all read the one Brain. The governing
principle: **"when two Hands would duplicate a concern, promote it up into the Brain — the
duplication you find is the build order."**

**The Hands — the production agents, grouped by value stream.** Each Hand *makes or does*
something and is deliberately thin: it carries no private research or analytics. Hands are
organised into value-stream columns; two streams are live in the current pilot:

- **Product / Offering Development** (the *slow loop*) — shapes what we sell. Vertical
  process-mapping → research-solutions → solutions-architect → proof.
- **Commercial / Revenue** (the *fast loop*) — sells it. Thought leadership → media planner →
  content creator → growth hacker → lead gen → sales.

(Delivery, Finance/RMG, and People streams exist in the target state but are out of scope for
this pilot.)

**The Spine — orchestration and the human surface.** A persistent layer that coordinates the
Hands and routes approvals to people. It holds an **asset record** per hero idea (a solution,
an article, a campaign) so context accumulates instead of degrading at each handoff, a **run
record** per cycle that logs what fired and who approved what, and a **conductor** (a scheduled
task) that fires the right Hand when its inputs are ready. **Human gates sit only where a real
decision lives.**

### The two loops

- **Fast loop (Commercial, monthly):** Thought Leadership writes the monthly article → Media
  Planner briefs distribution → Content Creator atomizes it into channel-native posts → Media
  Planner sets the plan and budget → Growth Hacker publishes and runs distribution → Lead Gen
  captures and qualifies → Sales closes. Fires on a monthly metronome.
- **Slow loop (Product/Offering, episodic):** Vertical Mapping → research-solutions →
  Solutions Architect → proof catalogue → feeds the fast loop. Fires on a business decision
  ("map this vertical," "productize this opportunity").

### The feedback returns (why it compounds)

Performance and market signal flow *back*, not just forward:

- **Fast-loop return:** Growth Hacker and Lead Gen write performance data to the Brain, which
  re-points next month's content and channel decisions.
- **Slow-loop return:** that same performance data, plus what the top voices and competitors
  are doing, flows up to the Product/Offering stream's portfolio review to decide which
  solutions to scale, which to let emerge, and which to retire.

The core insight to hold onto: **separating the making/distributing from the
capturing/converting, giving each a thin single-craft mandate, and defining the seam where
they hand off — that principle is the whole structure.**

---

## 2. Connecting to the Brain

Skill creators must connect to the Brain; solution creators usually don't need to (the skills
do it for them). This section is the contract.

### Where the Brain lives

The Brain and Spine are data files in a **Google Shared Drive: "Iksula Agentic Org"**, under a
`_brain/` folder (registers) and a `_spine/` folder (asset and run records). They are *not*
auto-loaded into any session — they're read on demand by the skills, which is what keeps
context from bloating.

### Step 1 — Get access (the workspace-auth boundary)

1. Ask DJ/IT to add your **@iksula.com** account to the `Iksula Agentic Org` Shared Drive as
   **Content manager**.
2. In Cowork's connector settings, connect **Google Drive signed in as your @iksula.com
   Workspace account** — **not** a personal Gmail. A personal Gmail cannot see a Workspace
   Shared Drive; this is the single most common setup failure.
3. Verify: search the Drive for the `_brain/` folder and confirm you see files such as
   `voices-260606.md` and `brain_io-howto-260606.md`.

You also need the **Slack** connector for gate approvals (see §4) — channel
`#agentic-org-requests`.

### Step 2 — Read and write only through `brain_io`

Skills never touch Brain file paths directly. They call a thin helper, `brain_io`, with three
stable verbs:

- **`get(module)`** — read the latest version of a register (e.g. `get('voices')` returns the
  newest `voices-YYMMDD.md`).
- **`list(module)`** — list all versions (audit/history).
- **`write(module, data)`** — publish a *new dated version* (append-only; never overwrites).

The full implementation recipe (which Drive connector calls to use, including using
`download_file_content` rather than `read_file_content` so CSVs aren't corrupted) is in
`brain_io-howto` inside `_brain/`. Read it before writing any Brain-touching skill.

### Step 3 — The four non-negotiable rules

1. **Append-only.** The connector has no update/delete; a new dated file *is* the new latest.
   You get version history for free.
2. **One writer per module, many readers.** Each module names its owning skill; everyone else
   is read-only. This prevents two skills fighting over the same register. Shared-writer
   modules are **namespaced** (e.g. `performance-analytics-growth-YYMMDD` vs.
   `performance-analytics-leadgen-YYMMDD`).
3. **Raw-capture first.** Every research or performance pass writes raw data to `_brain/_raw/`
   first; the distilled register then cites that raw. **Never publish a number that isn't
   traceable to raw plus a source.**
4. **Call the verbs, never raw paths.** This lets the backend swap from Drive to an MCP server
   later without changing a single skill.

### Step 4 — Build against stubs, integrate against the live store

You do **not** need the Brain fully seeded to start building. Develop your skill against the
*contract* (the verbs and the file formats) using a small local stub Brain, then point at the
live Shared Drive at integration time. **Build ≠ run:** colleagues build independently on their
own machines; the shared Brain is only needed when skills run together.

### The Brain modules at a glance

| Module | Holds | Writer of record |
|---|---|---|
| `voices` | Top-voices roster, influence scores, monthly Influence Analysis | content-creator |
| `competitor-radar` | Competitor offers, positioning, teardowns | research-solutions |
| `icp-audience` | ICP, personas, audience & firmographic signals | shared reference |
| `proof-catalogue` | Real named wins, metrics, approved proof, Iksula IP | solutions-architect |
| `channel-intel` | What each channel rewards this quarter; benchmarks | growth-hacker / media-planner (namespaced) |
| `performance-analytics` | Engagement + funnel + margin signals (the feedback return) | growth-hacker / lead-gen (namespaced) |
| `method-vocab` | Scoring rubric + controlled vocabularies | vertical-process-mapping |
| `solutions-catalogue` | The full offering portfolio = productization queue | shared (DJ curates) |

---

## 3. Using skills

### 3.1 Plugging into the skills marketplace

Iksula shares its skills through a git-based **plugin marketplace** named
`iksula-marketplace`. You subscribe once and receive every skill plus future updates — no
re-sharing files.

**To subscribe and install (each colleague, once):**

1. The marketplace repo is `https://github.com/BadCoder666/iksula-marketplace.git`
   (private — ask DJ to add your GitHub account as a collaborator first).
2. Add the marketplace:
   ```
   /plugin marketplace add https://github.com/BadCoder666/iksula-marketplace.git
   ```
3. Install the plugin:
   ```
   /plugin install iksula-agents@iksula-marketplace
   ```
   …or pick it from the `/plugin` menu. The four skills appear in your session.

When maintainers publish a new version, you receive it through this same subscription.

**Downloadable asset (no-git option).** If you can't reach the git remote yet, DJ can hand you
the packaged marketplace as a single file: **`Iksula Marketplace - YYMMDD.zip`** (in the
`Agentic Org` folder). Unzip it and install the `.plugin` it contains via **Settings →
Capabilities**. The git subscription is preferred because it auto-updates; the zip is a
point-in-time snapshot.

### 3.2 Available skills — high-level notes

The `iksula-agents` plugin currently bundles four skills; more are in flight (status as of the
build tracker, 6 Jun 2026).

**In the marketplace now:**

- **`vertical-process-mapping`** — maps an industry vertical's functions at L1/L2/L3 and scores
  automation opportunities into a 6-tab workbook plus an Iksula solution shortlist. Start of the
  slow loop. *Trigger: "map this vertical."*
- **`solutions-architect-create`** — turns a shortlisted opportunity into a named, sellable
  solution: internal intro deck + client pitch deck. Owns differentiation, value prop, and proof
  anchoring. *Trigger: "package this solution."*
- **`thought-leadership`** — writes the monthly opinion-led byline article that builds authority
  with senior buyers. Start of the fast loop. *Trigger: "write this month's article."*
- **`content-creator`** — the central production engine: atomizes a hero asset into channel-native
  posts, carousels, threads, emails, video and podcast briefs, and sequences a publishing calendar.
  *Trigger: "atomize this article / build the content calendar."*

**In flight (drafted, not yet in the marketplace):** `research-solutions` and `media-planner`
(DJ), and `growth-hacker` and `lead-gen` (colleague-built). These are being finished as
Brain-aware skills before install.

### 3.3 Creating a skill

This is the contributor path. Follow it whenever you want a *new reusable skill* or a change to
a *shared* one.

1. **Branch the marketplace repo** — never work on `main`.
2. **Start from the template.** Copy `plugins/iksula-agents/SKILL-TEMPLATE.md` into a new
   `skills/<your-skill>/SKILL.md`. It is pre-structured to the Iksula standard.
3. **Write it to the standard** (the full bar is in `CONTRIBUTING.md`):
   - Mandate in two parts: **PART A — The Agent's Mandate** (purpose, scope, what it owns, where
     it sits in the pipeline) and **PART B — The Deliverables** (the artifacts it produces, with
     formats).
   - Declare its place in the Brain / Hands / Spine model and don't duplicate an existing Hand's
     scope. If you find duplication, that concern probably belongs in the Brain, not your skill.
   - Make it **Brain-aware**: read context via `brain_io.get(...)`, write via
     `brain_io.write(...)`, respect one-writer-per-module and namespacing.
   - Any deck or document it produces must be brand-compliant (Carlito, primary red `#9A0D15`,
     light cards).
   - Follow file/naming conventions and **ask the user which folder to save to** rather than
     defaulting.
   - `description` frontmatter is third-person with specific trigger phrases; the body is
     imperative instructions for Claude, under ~3,000 words, with detail pushed to `references/`.
     Use `${CLAUDE_PLUGIN_ROOT}` for intra-plugin paths.
4. **Add yourself as the skill's owner** in `CODEOWNERS`.
5. **Bump the version** in `plugin.json` and `marketplace.json` (semver).
6. **Validate, then open a PR.** A maintainer checks it against the standard and merges. For a
   skill that will also be installed standalone (outside the marketplace), package it as a
   `.skill` file and install via **Settings → Capabilities** — you can't edit an installed skill
   in-session, so changes always ship as a new installable version.

> **Canary discipline.** When you change a skill that's already live, validate the new version on
> one real run *before* retiring the old one. (Content-creator is the standing canary for the
> Brain-aware rewrites.)

### 3.4 Updating a skill

Updating is the same governed flow as creating, scaled down:

1. Branch; make the change from the current `SKILL.md`.
2. Re-validate against the `CONTRIBUTING.md` checklist.
3. **Bump the version** in `plugin.json` and `marketplace.json` — this is how subscribers know an
   update shipped.
4. Open a PR. The skill's **owner** (via `CODEOWNERS`) reviews for correctness; a **maintainer**
   merges. Subscribers pull the new version automatically.

Keep changes append-friendly: don't silently change a Brain module's schema that other skills
read. If a register format must change, coordinate with its writer-of-record and the readers
first.

### 3.5 Using a skill (consuming)

This is the everyday path and it has **no governance overhead**:

1. Make sure you've installed the marketplace (§3.1).
2. Trigger the skill in plain language (e.g. "package the Staffing Services solution," "build
   this month's content calendar"). The skill loads and runs.
3. **Save the output per Iksula conventions** — date-suffixed filename (`Name - YYMMDD`, with
   `v1/v2` for same-day versions), brand-compliant, into the relevant **solution or campaign
   folder** — never into the marketplace repo.

That's it. You did not change anything shared, so there's no PR. The decks, calendars, and
articles you produce are *outputs of* the capability, and they live with your normal work.

---

## 4. Using the skills — an extended walkthrough

Two worked examples show how the pieces compose. Both assume you've installed the marketplace and
(for skill creators) connected the Brain.

### Walkthrough A — Productize a new solution (slow loop)

Say a colleague is asked to stand up **Staffing Services** as a sellable solution.

1. **(Optional) Map the space.** If there's no shortlist yet, run `vertical-process-mapping` on
   the relevant vertical to produce the 6-tab workbook and an opportunity shortlist. Leadership
   (DJ) gates *which* vertical to map.
2. **Research the opportunity.** `research-solutions` runs a deep dive — market sizing,
   competitor teardown, buyer evidence — reading `competitor-radar`, `icp-audience`, and `voices`
   from the Brain, and writing competitive intel back to `competitor-radar`.
3. **Package it.** `solutions-architect-create` turns the researched opportunity into the internal
   intro deck and the client pitch deck, anchoring claims in real `proof-catalogue` evidence
   (never invented). The SME/solution owner gates the deck for accuracy; then Leadership.
4. **Save the decks** into the Staffing Services solution folder, date-suffixed and
   brand-compliant. **They do not go into the marketplace** — Staffing Services is a solution
   instance, not a skill.

If, during this, you find a genuinely reusable new capability (say, a repeatable
"staffing-vertical sizing" method), *that* could become a new skill — which then follows the
§3.3 contributor path.

### Walkthrough B — Run a monthly content cycle (fast loop)

1. **Thought Leadership** writes the month's byline article, reading `voices`, `competitor-radar`,
   `icp-audience`, and `proof-catalogue`. Gate: byline leader + editor approve the voice/thesis.
2. **Media Planner** reads the article and writes a **Distribution Brief** (which channels,
   segments, formats to build for). Gate: content lead.
3. **Content Creator** reads the brief and atomizes the article into channel-native posts,
   carousels, threads, emails, and briefs, plus a publishing calendar. Gate: growth/marketing lead
   approves the calendar and key messages.
4. **Media Planner** returns with the **Media Plan + Budget** across channels. Gate: budget owner.
5. **Growth Hacker** publishes and runs distribution, captures raw performance, and surfaces
   content-sourced interest to **Lead Gen**, which captures, qualifies (MQL→SQL), nurtures, and
   routes SQLs — *new accounts to Sales, existing ECS accounts to Key Account Management*.
6. Both write performance back to `performance-analytics` (namespaced), which re-points next
   month's decisions.

### How gates work (the human surface)

When a Hand reaches a gate, the Spine posts to the private Slack channel
**`#agentic-org-requests`**, @mentioning the owner, with an asset summary and the decision needed.
The owner replies in-thread — **✅ approve · ✍️ revise: \<note\> · ⏸ hold: \<reason\>** — and the
conductor reads the reply and either releases the next step, re-runs the Hand with the note, or
pauses. Every decision is logged in the run record with who decided and when. There are six gates
across the two loops (vertical/solution choice, deck accuracy, TL voice, distribution brief, media
budget, SQL acceptance).

> **Current status (6 Jun 2026):** the Brain is seeded, the four marketplace skills' Brain-aware
> rewrites are drafted and awaiting gated install (content-creator first, as canary), the Spine is
> designed and scaffolded but not yet running live, and the Slack gate channel exists. Treat the
> fast loop as **operator-run** for now: you fire each Hand and route gates manually. The monthly
> scheduled "conductor" is the graduation step once a manual cycle proves out.

---

## 5. Other instructions for effective use

A checklist of the things that most affect whether your work composes cleanly with everyone
else's.

**Before you start (skill creators):**

- @iksula.com Workspace account added to the `Iksula Agentic Org` Shared Drive as Content manager.
- Google Drive connector connected *as that workspace account* (not personal Gmail).
- Slack connector connected; you're in `#agentic-org-requests` if you own a gate.
- You've read `brain_io-howto` and `raw-capture-howto` in `_brain/`, and the thin mandate for the
  Hand you're building.

**The non-negotiables (so agents stay composable):**

- Reach the Brain only through `brain_io` verbs — never raw file paths.
- Append-only writes; namespace shared-writer feeds; respect one-writer-per-module.
- Capture raw to `_brain/_raw/` first; never publish a number not traceable to raw + source.
- Keep each Hand thin and single-craft. If two Hands need the same thing, it belongs in the Brain.
- Voice-governed output (e.g. byline replies) uses the Brain's personas; a human owns the voice —
  the skill drafts, it doesn't invent the voice.

**Conventions:**

- **Naming:** deliverables use `Name - YYMMDD` (with `v1/v2` for same-day versions). Repo source
  files (skills, manifests, this guide) stay un-dated — git tracks their versions.
- **Brand:** any deck/doc output uses Carlito, primary red `#9A0D15`, light cards.
- **Saving:** skills ask which folder to save to; they never default. Solution outputs go to
  solution folders, never the marketplace.

**Governance recap (who can change what):**

- Anyone can *propose* a change via pull request; only **maintainers** merge to a protected `main`
  (currently DJ, `@BadCoder666`).
- **Skill/vertical owners** (in `CODEOWNERS`) review their own skill; they don't need merge rights
  and they grow with the catalogue.
- Consuming a skill needs no PR. Changing a shared skill does.

**Where to get help / source of truth:**

- `README.md` — install + what's inside the marketplace.
- `CONTRIBUTING.md` — the full authoring standard and governance.
- `SKILL-TEMPLATE.md` — a compliant starting point for a new skill.
- The `Agentic Org` folder — the vision doc, Brain-Spine contract, build tracker (living status),
  go-live runbook, and the per-Hand thin mandates and Brain-aware drafts.
- DJ — for Drive access, the marketplace URL, gate-owner assignments, and merges.
