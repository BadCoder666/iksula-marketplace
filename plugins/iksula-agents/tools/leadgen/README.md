# Lead Gen execution toolkit (`leadgen/`)

Runnable enforcement of the `skills/lead-gen/references/sending-stack.md` +
`seam-and-compliance.md` contract. The point of this package is to make the
safety rails **structural** — not a promise the agent must remember, but code
that physically cannot send.

**Nothing here starts a send.** There is no `run`/`start`/`resume`/`pause`/`stop`/
`delete` method anywhere; attempting one raises `ForbiddenAction`.

## Modules
| Module | Job | Sends / writes PII? |
|---|---|---|
| `config.py` | secrets (env only), kill-switch, mailbox allow-list, hard constants | no |
| `merge_preview.py` | catch `{{token}}` leaks before they render to 1,000 people | no (local) |
| `presend_gate.py` | **the wall** — lawful basis · suppression · geo · source · mailbox · merge · approval | no (decides only) |
| `ledger.py` | append-only creation ledger = the ONLY definition of "owned" | metadata only |
| `audit.py` | append-only "who ran what" log (accountability) | metadata only |
| `wp_client.py` | Woodpecker READ + CREATE-ONLY; dry-run by default | create-only, gated |
| `preflight.py` | dry-run the gate over a cohort; prints PASS/HALT | no |

## The wall (why it HALTs today)
A send/enroll is allowed only if **all** hold:
1. `WOODPECKER_AGENT_BUILD=on` (kill switch)
2. source is a **clean Sheet**, never raw Zoho
3. sending mailbox is **allow-listed + warmed** (never primary/live) — none provisioned yet
4. merge-preview is **clean** (no token leaks)
5. **human approval** token present
6. **≥1 record** passes lawful-basis + suppression + geo + B2B-domain

With 100% of Zoho leads at null `Data_Processing_Basis`, **#6 = 0 → HALT**. That is correct and intended.

## Run it
```bash
# safety tests (no network, no live account)
python -m unittest leadgen.tests.test_safety

# dry-run the gate over a cohort (never creates/sends)
python -m leadgen.preflight --prospects leads.csv --template body.txt \
    --subject subj.txt --source clean_sheet --mailbox <warmed_id> --approved <token>
```
`preflight` exits 0 only on ALLOW, 2 on HALT — so a wrapper can gate on it.

## Secrets & env
- `WOODPECKER_API_KEY` — Woodpecker key (from gitignored `_woodpecker.local`; never committed).
- `WOODPECKER_AGENT_BUILD` — `on` to permit write calls; anything else = zero writes.
- `WOODPECKER_ALLOWED_MAILBOX_IDS` — comma-sep warmed mailbox ids the agent may use (empty = cannot build).

## What is intentionally NOT built yet (blocked on others)
- **Live enroll** — stays disabled (stage-zero today: zero lawful basis). `add_prospects` refuses live writes.
- **Zoho dedup query** — `is_existing_client`/`already_contacted` are inputs here; the live read is via the Zoho MCP / a reviewed follow-up.
- **Already-contacted suppression feed** — needs the dialer call-report (flowchart 1b).
- **Router** — infra, outside this agent.

Maps to: flowchart segments 4 (campaign build) + 6 (governance gate), and the
`sending-stack.md` §4 create-only / ledger-gated / never-run rules.
