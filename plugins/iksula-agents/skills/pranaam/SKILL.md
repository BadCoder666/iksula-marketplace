---
name: pranaam
description: >-
  Opens an iKshana working session: connects this Claude instance to the Iksula Agentic Org
  Google Drive (the Brain + Spine), loads the access contract and operating rules, and confirms
  readiness — so every skill and solution built afterwards reads the Brain's guidance on demand.
  Use when the user says "pranaam", "namaste", "namaste iKshana", "jago", "invoke iKshana",
  "connect to the brain", "wake up the brain", or "start an iKshana session".
---

# Pranaam — connect this session to the iKshana Brain

The session opener. Run me first. I connect this Claude instance to the iKshana Brain/Spine and
load the operating contract, so everything you build next is Brain-aware by default.

## PART A — The Agent's Mandate

- **Purpose:** make the current session *Brain-aware*. Verify the Google Drive connector is live,
  confirm the `_brain/` and `_spine/` stores are reachable, load the access contract + the
  non-negotiable rules, and announce readiness. After this runs, any skill or solution work in the
  session reads standing context from the Brain via `brain_io` instead of guessing.
- **Scope (in):** check/establish Drive connectivity; verify the Brain and Spine folders; read the
  contract files (`_brain-contract`, `brain_io-howto`, `raw-capture-howto`, `_spine-howto`);
  inventory the available Brain modules; print a readiness report; set the session's operating
  conventions.
- **Scope (out):** does no craft work — no content, no scoring, no research, no outreach. Does **not
  write** to the Brain or Spine (read-only). Does **not** approve gates. Does **not** download every
  module (context stays lean — modules are read on demand by the skills that need them).
- **Owns:** nothing standing. It is not the writer-of-record for any Brain module.
- **Place in the pipeline (Brain/Hands/Spine):** not a value-stream Hand — a **cross-cutting session
  primer**. Runs before any Hand or solution skill. *Reads:* the `_brain` contracts + `_spine` how-to.
  *Feeds forward:* the loaded contract, the module inventory, and the active rules to whatever skill
  runs next. *Writes:* nothing.

## PART B — The Deliverables

| Deliverable | Format | Notes |
|-------------|--------|-------|
| Session readiness report | chat message | States: connected account; `_brain/` + `_spine/` reachable (folder IDs verified); contracts loaded; the module inventory; the four non-negotiables now active. No files are written — this skill is read-only. |

## Workflow

Imperative steps for Claude. `search_files` and `download_file_content` are the Drive-connector calls
behind `brain_io`; the recipe is in `${CLAUDE_PLUGIN_ROOT}/references/brain-access.md`, and the live
`brain_io-howto` in `_brain/` is authoritative for the exact folder IDs and call signatures.

0. **Check the connector.** Confirm the Google Drive connector is connected. If it is **not**, stop
   and tell the user to connect it in **Cowork's connector settings** (in this CLI runtime: `/mcp` →
   "claude.ai Google Drive"), signed in with their **@iksula.com Workspace account — not a personal
   Gmail** (a personal Gmail cannot see the company Shared Drive). Do not fabricate Brain content;
   ask and wait.
1. **Verify the Brain.** Find it via a known **seed file**, not a folder-name search — the connector
   returns files but does **not** return the `_brain/` folder by its title. Run `search_files: title
   contains 'brain_io-howto'` and take the newest result (e.g. `brain_io-howto-260606-v4`). Its
   **`parentId` IS the `_brain/` folder ID — reuse that ID for every later read.** Confirm `voices-*`
   shares the same parent. If the search returns nothing, the connector is almost certainly on the
   wrong account — surface that and stop.
2. **Verify the Spine.** Same trick: `search_files: title contains '_spine-howto'`; its `parentId` is
   the `_spine/` folder (which also holds `assets/` and `runs/`).
3. **Load the contract.** `download_file_content` (raw base64 — **never** `read_file_content`, which
   corrupts CSV) the live contracts in `_brain/`: the **newest `brain_io-howto`** (pick by latest
   `modifiedTime` — same-day revisions carry a `-vN` suffix, e.g. `-v4`), plus **`raw-capture-howto`**,
   **`_brain-contract`**, and the `_spine/` **`_spine-howto`**. Internalize the `get`/`list`/`write`
   verbs and the four non-negotiables.
4. **Inventory, don't ingest.** `list` the available modules so the session knows what exists —
   `voices`, `competitor-radar`, `icp-audience`, `proof-catalogue`, `channel-intel`,
   `performance-analytics`, `method-vocab`, `solutions-catalogue`. Do **not** download their contents
   now; they are read on demand by the skill that needs them (this keeps context lean).
5. **Announce readiness.** Print the readiness report (PART B): the @iksula.com account in use, the
   verified folder IDs, the contracts loaded, the module inventory, and the four active rules. End
   with one line: *"iKshana online — Brain connected. Subsequent skills and solutions will read the
   Brain on demand."*
6. **Set the session conventions.** From here, all work follows Brain/Hands/Spine: read via
   `brain_io` (never raw paths); append-only writes; one writer per module (namespace shared feeds);
   raw-first (dump raw to `_brain/_raw/` before synthesizing, never publish a number not traceable to
   raw + source); route human gates to Slack `#agentic-org-requests` (✅ / ✍️ / ⏸); brand outputs
   Carlito + primary red `#9A0D15` + light cards; name deliverables `Name - YYMMDD`; ask which folder
   to save to.

## Operating principles

- **Connect, don't fabricate.** If the Brain is unreachable, stop and ask — never invent its content.
- **Read on demand, not all at once.** Load the contract + an inventory, not every module — keep
  context lean (the Brain is deliberately not auto-loaded).
- **Read-only.** This skill writes nothing and owns nothing.
- **Verbs, not paths.** Reach the Brain only through `brain_io` so the backend can swap to an MCP
  server later without changing any skill.
- **Workspace account only.** Always the @iksula.com Workspace login, never a personal Gmail.

## Conventions (do not remove)
- Brand: Carlito, primary red `#9A0D15`, light cards — for any deck/doc output (none here).
- File naming: `Name - YYMMDD` (v1/v2 for same-day). Ask the user which folder to save to.
- Use `${CLAUDE_PLUGIN_ROOT}` for intra-plugin paths; never hardcode absolute paths.

## Resources
- `${CLAUDE_PLUGIN_ROOT}/references/brain-access.md` — how to resolve the Brain/Spine folders by
  name, the `brain_io` verb recipe, the module→writer table, and the four non-negotiables.
- Live contracts (authoritative — read, don't duplicate): `brain_io-howto` and `raw-capture-howto`
  in `_brain/` (and `_brain-contract` / `_spine-howto` if present).

## Run log (required)
On finish, log this run: create one file in the Spine `_spine/_runs-log/` (folder ID `1pfZ1UKFvE4BHW2Vold8S75lx1g0bLHvs`) named `<YYMMDD-HHMM>-<skill>-<operator>.md`, with one line — `timestamp · skill · operator · output-link`. Create-only; never skip. This is how iKshana sees which flows are being used.
