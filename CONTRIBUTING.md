# Contributing to the Iksula Marketplace

This repo is how Iksula skills reach the whole team. To keep quality high and avoid
sprawl, every change goes through review. This document is the bar.

## The governance model (who can change what)

- **`main` is protected.** Nobody pushes to it directly.
- **Anyone can propose** a change by opening a pull request (or forking and PR-ing).
- **Only maintainers merge.** A maintainer reviews every PR against the standard below
  before it reaches anyone's Cowork.
- **Consumers cannot alter the shared source.** Installing the marketplace is read-only;
  local tweaks never propagate to others.

> This is the gate that prevents chaos: anyone proposes, maintainers approve.

### Two roles, do not conflate them

- **Maintainers (Tier 1)** — small, fixed group with **merge rights to `main`** and
  ownership of the release tag. They enforce the standard below and press merge. Their
  job is the bar, not subject-matter expertise in every skill. This list stays small.
- **Skill / vertical owners (Tier 2)** — the person **responsible for the content** of
  a given skill (usually its author or the vertical lead). They do **not** need merge
  rights; they are the required reviewer when *their* skill changes. Owners are declared
  in `CODEOWNERS` (auto-requested on any PR touching their path) and grow with the catalogue.

Flow for any change: contributor opens a PR → the skill's **owner** reviews for correctness
→ a **maintainer** confirms it meets the standard and merges.

### Maintainers (Tier 1)
- **DJ** — `@BadCoder666` — merge rights, release tag.

### Release process
1. PR approved and merged to `main`.
2. Bump `version` in the affected `plugin.json` (semver) and in `marketplace.json`.
3. Tag the release. Consumers pull the new version through their subscription.

### Approval notifications (automated, via Slack)
The iKshana bot (GitHub Action `.github/workflows/notify-slack.yml`) sends: a DM to **DJ** when a PR
opens; a DM to **you** when DJ approves it; and an announcement to **#ikshana-updates** (skill name +
what it does) when it merges and goes live. Add your `GitHub-login -> Slack-ID` to
`.github/slack-handles.json` to get your approval DM. Setup: `docs/SLACK-NOTIFY-SETUP.md`.

## The Iksula skill authoring standard

Every skill in this marketplace MUST follow these conventions. A PR that doesn't meet
them will be sent back.

### 1. Mandate structure
Every agent/skill mandate is written in two parts:
- **PART A — The Agent's Mandate** — what the agent is for, its scope, what it owns,
  and where it sits in the pipeline (which agents feed it, which it feeds).
- **PART B — The Deliverables** — the concrete artifacts it produces, with formats.

### 2. Fit the Agentic Organisation model
Skills must respect the Brain / Hands / Spine architecture and the two-loop design.
A new skill should declare which part of the org it serves and not duplicate an
existing agent's scope. Respect the commercial-stream boundaries (e.g. Demand Gen vs
Lead Gen) already defined.

### 3. Brand compliance
Any deck or document a skill produces must follow the canonical Iksula brand spec:
font **Carlito**, primary red **#9A0D15**, light cards. Read the brand spec before
building any deck-producing skill.

### 4. File & naming conventions
Outputs follow Iksula's folder and file conventions, including the date-suffix naming
rule (`Name - YYMMDD`, with `v1/v2` suffixes for same-day versions). Skills that save
files must ask the user which folder to save to rather than defaulting.

### 5. Skill mechanics
- `description` in SKILL.md frontmatter is **third person** and contains **specific
  trigger phrases** users would actually say.
- SKILL.md body is **instructions for Claude** (imperative, verb-first), not docs for
  a human reader. Keep it under ~3,000 words; push detail into `references/`.
- Use `${CLAUDE_PLUGIN_ROOT}` for any intra-plugin paths. Never hardcode absolute paths.
- kebab-case for all skill directory names.

### 5b. Run log (MANDATORY, CI-enforced)
Every skill MUST include a `## Run log (required)` section that logs each run to `_spine/_runs-log/` (time · skill · operator · output link). A GitHub Action (`validate-skill.yml`) **fails any PR** whose changed `SKILL.md` is missing this section.

### 5c. Human gate (declare if applicable)
If the skill produces output needing sign-off, it MUST declare each gate (`## Human gate(s)`: `gate: <id> — <what> → owner <name>(<slackid>)`). Hard-gated steps add a `## Precondition — hard gate` that refuses to run until the upstream gate is ✅.

### 6. PR checklist (maintainer verifies)
- [ ] SKILL.md has third-person description with trigger phrases
- [ ] Mandate uses PART A / PART B structure
- [ ] Declares its place in the Brain/Hands/Spine model; no scope overlap
- [ ] Any deck/doc output is brand-compliant (Carlito, #9A0D15)
- [ ] Follows file/naming conventions; asks before saving
- [ ] No hardcoded paths; uses `${CLAUDE_PLUGIN_ROOT}`
- [ ] `## Run log (required)` section present (CI-enforced)
- [ ] Human gate declared if the skill needs sign-off; hard-gate precondition added where applicable
- [ ] `version` bumped in plugin.json + marketplace.json

## Consuming vs. contributing (read this first)

Most work **consumes** the marketplace and needs no PR. Using a skill to produce a
deliverable — e.g. running `solutions-architect-create` to build a *Staffing Services*
solution — is consumption. The decks it produces are outputs that live in your normal
solution folders, **not** in this repo. Governance only applies when you change a
**shared skill** itself.

- **Consume (no governance):** install the marketplace, run a skill, save the output
  per Iksula conventions. Done.
- **Contribute (governance applies):** you want to add a new reusable skill, or change
  an existing one so the whole team benefits. Follow "Starting a new skill" below.

> Do not commit one-off solution deliverables (a specific client deck, a single
> Staffing Services output) into the marketplace. The marketplace holds **reusable
> capability**; instances of that capability live in solution folders.

## Starting a new skill
1. Branch (or fork) the repo — never work on `main`.
2. Copy `plugins/iksula-agents/SKILL-TEMPLATE.md` into a new `skills/<your-skill>/SKILL.md`
   and fill it in. It's pre-structured to the standard above.
3. Add yourself as the skill's owner in `CODEOWNERS`.
4. Bump `version` in `plugin.json` and `marketplace.json`.
5. Open a PR. The skill owner reviews; a maintainer merges.
