# Brain access — the `brain_io` recipe and the rules

Quick reference for the `pranaam` skill. The **authoritative** version is the live `brain_io-howto`
inside the Shared Drive `_brain/` folder (currently `brain_io-howto-260606-v4`) — read it at runtime
and treat it as source of truth if anything here ever disagrees. This file is the offline contract so
the skill is buildable against a local stub before the live Brain is reached.

## The store

The Brain and Spine are files in the Google Shared Drive **"Iksula Agentic Org"**, reached through
the Google Drive connector signed in as an **@iksula.com** Workspace account (never a personal
Gmail). They are read on demand — never auto-loaded into a session.

**Resolve folders via a seed file, NOT by folder name.** A folder-name search (`title = '_brain'`)
returns nothing on this connector. Instead, `search_files: title contains 'brain_io-howto'` and read
the newest result's **`parentId`** — that *is* the `_brain/` folder ID; reuse it for every later read.
Resolve `_spine/` the same way via `title contains '_spine-howto'`. (The live `brain_io-howto` text
also states both folder IDs, so don't hardcode them here.)

Access-confirming seeds present in `_brain/`: `voices-260606.md`, `brain_io-howto-*` (newest `-v4`),
`_brain-contract.md`, `raw-capture-howto-260606.md`.

## The `brain_io` verbs (never touch raw paths)

- **`get(module)`** — read the latest version of a register: `search_files` with
  `parentId = '<resolved _brain id>' and title contains '<module>-'` → pick the **newest by
  `modifiedTime`** (same-day revisions carry a `-vN` suffix, so don't sort on the date alone) →
  **`download_file_content(fileId)`** (returns raw base64). Use `download_file_content`, **not**
  `read_file_content` (which reformats/escapes and corrupts CSV).
- **`list(module)`** — list all dated versions (audit/history).
- **`write(module, data)`** — publish a new dated version, append-only. *(Contract reference only —
  `pranaam` is **read-only** and never writes; the writer-of-record skills use this.)*

`pranaam` uses only `get` / `list` / `search_files`.

## The four non-negotiables

1. **Append-only.** The connector has no update/delete; a new dated file *is* the new latest. History is free.
2. **One writer per module, many readers.** Each module names its owning skill; everyone else is
   read-only. Shared-writer feeds are namespaced by source — e.g. `performance-analytics-growth-YYMMDD`
   vs `-leadgen-YYMMDD` vs `-media-YYMMDD`.
3. **Raw-first.** Write raw research/performance to `_brain/_raw/` first; the distilled register cites
   it. Never publish a number not traceable to raw + a source.
4. **Verbs, not paths.** Reach the Brain only through the `brain_io` verbs so the backend can later
   swap from Drive to an MCP server without changing any skill.

## Brain modules and their writer-of-record

*(Reference inventory — the live `brain_io-howto` / module headers are authoritative if they differ.
All eight are seeded in `_brain/` as of 8 Jun 2026.)*

| Module | Holds | Writer of record |
|---|---|---|
| `voices` | top-voices roster, influence scores, monthly analysis | content-creator |
| `competitor-radar` | competitor offers, positioning, teardowns | research-solutions |
| `icp-audience` | ICP, personas, audience & firmographic signals | shared reference |
| `proof-catalogue` | real named wins, metrics, approved proof, Iksula IP | solutions-architect |
| `channel-intel` | what each channel rewards this quarter; benchmarks | growth-hacker / media-planner (namespaced) |
| `performance-analytics` | engagement + funnel + margin signals (the feedback return) | growth-hacker / lead-gen / media-planner (namespaced) |
| `method-vocab` | scoring rubric + controlled vocabularies | vertical-process-mapping |
| `solutions-catalogue` | the full offering portfolio = productization queue | shared (DJ curates) |

## Spine (read-only here)

`_spine/` holds `assets/` (one record per hero idea — solution / article / campaign), `runs/` (one per
cycle), and `_spine-howto`. The conductor (a scheduled task) fires Hands and routes gates to Slack
`#agentic-org-requests`; in the pilot this is operator-run.

> **Architecture note (from the live howto, 6 Jun 2026):** the Brain is being reframed as the record
> registers (the truth layer) *plus* a federation of domain-native reasoning brains on top. This is an
> internal-shape change only — the `brain_io` verb contract is unchanged, so skills are unaffected.
