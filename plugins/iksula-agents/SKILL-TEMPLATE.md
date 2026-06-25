---
name: your-skill-name
description: >-
  Third-person summary of what this skill does. Include the SPECIFIC phrases a user
  would say to trigger it — e.g. "run the X", "build the Y", "map the Z". Triggering
  accuracy depends on these phrases being concrete.
---

# Your Skill Name

One-line statement of purpose.

## PART A — The Agent's Mandate

- **Purpose:** what this agent is for.
- **Scope:** what is in and explicitly out of scope.
- **Owns:** the standing registers/artifacts this agent is writer-of-record for.
- **Place in the pipeline (Brain/Hands/Spine):** which agents feed it, which it feeds.

## PART B — The Deliverables

| Deliverable | Format | Notes |
|-------------|--------|-------|
| ... | .xlsx / .pptx / .docx / .md | brand-compliant where applicable |

## Workflow

Imperative, verb-first instructions for Claude. Keep under ~3,000 words; move detailed
schemas, taxonomies, and specs into `references/`.

## Conventions (do not remove)
- Brand: Carlito, primary red #9A0D15, light cards — for any deck/doc output.
- File naming: `Name - YYMMDD` (v1/v2 for same-day). Ask the user which folder to save to.
- Use ${CLAUDE_PLUGIN_ROOT} for intra-plugin paths.

## Human gate(s)
*If this skill produces output that needs human sign-off (external/spend/attributed), declare each gate here — one line:*
`- gate: <id> — <what's approved> → owner <name> (<slack_id>)`
*Omit this section only if the skill genuinely needs no gate.*

## Run log (required)  — MANDATORY for every skill
On finish, create one file in `_spine/_runs-log/` named `<YYMMDD-HHMM>-<skill>-<operator>.md` with one line: `timestamp · skill · operator · output-link`. Create-only. CI rejects any skill PR missing this section.

## On finish — open your gate (if gated; Drive only)
A gated skill, on finish, writes the `OPEN-<run>-<gate>-<YYMMDDHHMM>` record to `_spine/_gates/` (run · gate · owner · link) — it does **NOT** post to Slack. The central **iKshana listener** detects the new OPEN record and posts it to #ikshana-approvals as the @iKshana bot, and writes the RESOLVED record when the gatekeeper approves. Skills need only the **Drive** connector.
