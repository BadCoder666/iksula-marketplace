# Growth Hacker execution toolkit (`growthhacker/`)

Runnable enforcement of `skills/growth-hacker/SKILL.md` + `references/seam-contract.md`.
The Growth Hacker executes an *approved* plan on the organic / 1-to-many channel,
surfaces content-sourced interest to Lead Gen, and returns aggregate performance to
the Brain. This package makes the rails **structural** — nothing here posts publicly
or sends email.

## Modules
| Module | Job | Posts / writes PII? |
|---|---|---|
| `publish_gate.py` | ALLOW/HOLD a publish action — paid needs budget approval, named-byline reply needs a human voice-gate, broadcast email needs human first-send approval, organic must be instrumented + Scheduled | no (decides only) |
| `seam_emitter.py` | emit `content-sourced-lead` to the Spine queue — idempotent ULID, region→lawful-basis stamp, **rejects any score/ack/enrichment**, `ack_status` left null | Spine queue only, never Brain |
| `brain_metrics.py` | write `performance-analytics-growth` — schema-locked, **rejects PII rows**, aggregate-only, raw-first | aggregates only |
| `ulid.py` | the seam's idempotency key | no |
| `audit.py` | who published/emitted what + gate decisions, PII/secret-scrubbed | metadata only |
| `preflight.py` | dry-run a publish action + a seam emit (temp queue) | no |

## The three gates GH cannot bypass
1. **Paid spend** → `budget_approved` (inherited from the Media Planner). No approval → HOLD.
2. **Named-byline community reply** → a human `approval_token` owns the voice. No token → HOLD.
3. **Broadcast / BOFU email** → human first-send approval. No token → HOLD.

Organic posts have *no* separate human gate (the calendar + plan were already approved)
but still must be **instrumented** (UTM + tracked CTA) and executing a **Scheduled** row,
with the `GROWTH_PUBLISH` kill-switch on.

## The seam (GH → Lead Gen) is the PII boundary
- One record per interest event, keyed on a **ULID** (`correlation_id`); re-emit is a no-op.
- GH stamps `region` → `lawful_basis_tag` (**fail-safe**: anything not clearly US → company-level only).
- GH **never** qualifies/enriches/acks — any `score`/`grade`/`mql`/`ack_status`/`account_status` field is rejected.
- The record goes to the **Spine queue**, never the Brain. The Brain gets **counts**, never lead rows.

## Run it
```bash
python -m unittest growthhacker.tests.test_safety
python -m growthhacker.preflight --action action.json --event event.json
```

## Env
- `GROWTH_PUBLISH` — `on` to permit publish actions; anything else = HOLD everything.

## What is intentionally NOT built yet (blocked / next)
- **Live distribution connectors** (LinkedIn / Telegram / X) behind the gate — `telegram_publish.sh` exists as a manual helper; wiring it through `publish_gate` is the next slice.
- **Real Spine/Brain transport** — this package writes local mirrors under `_state/`; production resolves Drive `_spine/` + `_brain/` via `brain_io`.
- **Voices register integration** — the named-byline approval token is the gate; matching a reply to its `voices` persona is a follow-up.

Mirrors the `leadgen/` toolkit pattern (safe-by-construction, adversarially verified).
