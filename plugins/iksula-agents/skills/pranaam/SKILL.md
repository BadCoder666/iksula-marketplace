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
- **Scope (in):** check Drive connectivity; resolve the Brain/Spine by **fixed folder ID** (no
  discovery search); load only the two startup contracts (`brain_io-howto` + `_brain-contract`) in
  parallel — **lazy-load** `raw-capture-howto`/`_spine-howto` on demand; state the module inventory;
  print a readiness report; set the session's operating conventions.
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
| Session readiness report | chat message | States: connected account; `_brain/` + `_spine/` reachable (fixed IDs); the two startup contracts loaded; the module inventory; the active rules (incl. plain Grade 6–8 US English). Read-only except the required run-log line. |

## Workflow

Imperative steps for Claude. **Startup must be FAST — the fewest Drive round-trips possible.** Resolve
by **fixed folder ID** (don't re-discover), load only what's needed at startup, batch reads in
**parallel**, and **always** pass `excludeContentSnippets: true` so searches don't drag big payloads.
`search_files` / `download_file_content` are the Drive-connector calls behind `brain_io`.

**Fixed store IDs — use directly, do NOT search to discover them:**
- `_brain/` = `1EnymnhLIo-6hqqo_YuKQHpXd87E9NSzu`
- `_spine/` = `1dxOnoCsysiP1nEUGrAakbeDNBtM2ewrc`

0. **Check the connector.** Confirm the Google Drive connector is connected, signed in with the
   **@iksula.com Workspace account — not a personal Gmail** (a personal Gmail cannot see the company
   Shared Drive). If not, stop and tell the user to connect it (`/mcp` → "claude.ai Google Drive").
   Don't fabricate Brain content; ask and wait.
1. **One scoped search for the two startup files.** `search_files` with
   `query: parentId = '1EnymnhLIo-6hqqo_YuKQHpXd87E9NSzu' and (title contains 'brain_io-howto' or title contains '_brain-contract')`
   and **`excludeContentSnippets: true`**. From the result, pick the **newest `brain_io-howto-*`** and
   the **newest `_brain-contract*`** by `modifiedTime` (same-day revisions carry a `-vN` suffix). This
   single scoped call replaces the old whole-Drive seed searches.
2. **Load those two files in PARALLEL.** Issue both `download_file_content` calls in one batch (raw
   base64 — **never** `read_file_content`, which corrupts CSV): the newest **`brain_io-howto`** (the
   folder IDs, the `get`/`list`/`write` verbs, the four non-negotiables, the module list) and the
   newest **`_brain-contract`** (the session output rules — including the **plain Grade 6–8 US English**
   rule). Internalize both.
3. **Lazy-load the rest — do NOT load it now.** `raw-capture-howto` and `_spine-howto` are read **only
   when a skill actually writes raw data, or the conductor runs.** Loading them at startup only adds
   latency.
4. **Module inventory — state it, don't query Drive.** The set is stable; name it from the contract:
   `voices`, `competitor-radar`, `icp-audience`, `proof-catalogue`, `channel-intel`,
   `performance-analytics`, `method-vocab`, `solutions-catalogue`. Each is read on demand by the skill
   that needs it.
5. **Announce readiness (short).** The @iksula.com account; `_brain/` + `_spine/` reachable (fixed
   IDs); the two contracts loaded; the module inventory; and the active rules — **including plain Grade
   6–8 US English for the whole session.** End: *"iKshana online — Brain connected. Skills read the
   Brain on demand."*
6. **Set the session conventions.** read via `brain_io` (never raw paths) · append-only, one-writer-
   per-module, namespace shared feeds · raw-first to `_brain/_raw/` (never publish a number not
   traceable to raw + source) · **verify a write by LISTING the folder (`parentId`,
   `excludeContentSnippets: true`), not by name-searching** (the index lags for fresh files) · human
   gates to Slack `#agentic-org-requests` (✅ / ✍️ / ⏸) · **reply in plain Grade 6–8 US English** ·
   brand outputs Carlito + `#9A0D15` + light cards · name deliverables `Name - YYMMDD` · ask which
   folder to save to.

**Fallback (only if a fixed-ID read errors):** the folder may have moved — resolve by seed file
(`search_files: title contains 'brain_io-howto'` → its `parentId` is `_brain/`; `title contains
'_spine-howto'` → `_spine/`), then surface that the IDs changed so this skill can be updated.

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
