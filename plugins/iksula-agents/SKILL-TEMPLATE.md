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
