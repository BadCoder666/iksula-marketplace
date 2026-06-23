# tools/ — execution toolkits for the iksula-agents

Runnable, safe-by-construction enforcement of the agent skill contracts. These make
the hard rules in the skills *structural* (code that cannot send/post/leak), not just
instructions the agent must remember. Nothing here sends email or posts publicly.

| Package | Enforces | For skill |
|---|---|---|
| `leadgen/` | Woodpecker **create-only** client (no send verbs; HTTP allow-list), pre-send guardrail gate (lawful basis · suppression · geo · mailbox · merge-preview · human approval), ownership ledger, audit | `skills/lead-gen` (`sending-stack.md`) |
| `growthhacker/` | publish gate (paid budget · named-byline voice · broadcast first-send), idempotent seam emitter (no score/ack, recursive forbidden-key scan, lawful-basis stamp, no PII to Brain), schema-locked aggregate-only Brain writer, audit | `skills/growth-hacker` (`seam-contract.md`) |

## Run the safety tests
From this `tools/` directory (so the packages import as top-level):
```bash
python -m unittest leadgen.tests.test_safety        # 24 tests
python -m unittest growthhacker.tests.test_safety   # 28 tests
```

## Dry-run the gates (no send/post)
```bash
python -m leadgen.preflight --prospects leads.csv --template body.txt --source clean_sheet --mailbox <warmed_id>
python -m growthhacker.preflight --action action.json --event event.json
```

## Status
Both toolkits were adversarially red-teamed (two independent passes each) and verified
SOUND. Live enroll (leadgen) and live distribution connectors (growthhacker) are
intentionally stubbed/HOLD — see each package README for the unblock order. Local
runtime state lives under each package's `_state/` (gitignored).
