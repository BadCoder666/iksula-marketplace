# The Seam — `publishing-calendar` (Content Creator → Growth Hacker)

*The single handoff from the Content Creator to the Growth Hacker. One seam, one direction, one object: the **publishing calendar** (a queue/table of spoke rows). The Content Creator **authors and plans** every row; the Growth Hacker **executes** it. The authoritative field schema lives in `${CLAUDE_PLUGIN_ROOT}/skills/content-creator/references/content-build-spec.md` §5 and is mirrored in `mandate.md` §6 — this file is the boundary, the ownership discipline, the idempotency contract, and the justification for why it is a **Spine record, not a Brain feed**. If this file and `content-build-spec.md` §5 ever disagree, they are wrong — re-sync them (content-build-spec is authoritative).*

**Version:** 1.0 · **Owner of the object's author side:** Content Creator. **Owner of execution:** Growth Hacker. *(The Growth Hacker then emits a **separate** `content-sourced-lead` seam to Lead Gen — see `${CLAUDE_PLUGIN_ROOT}/skills/growth-hacker/references/seam-contract.md`; do not conflate the two.)*

---

## 1. The boundary (memorise this)

The Content Creator **packages and plans**: it atomizes the hero asset into channel-native spokes, sets `channel · format · publish_as · funnel_stage · planned_window · variant · depends_on · approval_status`, produces the asset bundle, and lands the calendar on the Spine. The Growth Hacker **executes**: it advances `status` (Planned → Scheduled → Published), applies `tracked_cta_utm` at instrument-time, finalises exact timing within `planned_window`, and may reshape to native form (length, aspect ratio) — but **never re-argues the thesis, reassigns the voice, or changes the channel/format/message.**

**The calendar carries NO instrumentation and NO publish state from the Content Creator** — `status` starts at `Planned` and `tracked_cta_utm` starts empty; both are the Growth Hacker's to set.

---

## 2. Payload schema (one row per produced spoke)

The authoritative definition is `content-build-spec.md` §5. Restated here with the **ownership split** (who sets each field):

| Field | Set by | Note |
|---|---|---|
| `row_id` | **CC** | **ULID** — stable, unique; the dedupe key + the join key the GH execution-log and `performance-analytics-growth` use. |
| `hero_asset_ref` | CC | source thesis/solution. |
| `spoke_asset_ref` | CC | id of the produced product (resolves into the asset bundle GH publishes). **Stable ULID.** |
| `channel` | CC | closed channel set; must be in the plan's `<<CHANNEL_SET>>`. |
| `format` | CC | closed format set. |
| `publish_as` | CC | named byline persona (authority) **or** `"Iksula"` (promo/proof). **Voice governance — immutable downstream.** |
| `funnel_stage` | CC | `TOFU` \| `MOFU` \| `BOFU`. |
| `planned_window` | CC | scheduled window; GH finalises exact time within it. |
| `status` | **GH advances** | `Planned` → `Scheduled` → `Published`. CC sets initial `Planned` only. |
| `tracked_cta_utm` | **GH applies** | UTM + tracked-CTA tag at instrument-time; CC leaves empty. |
| `variant` | CC bounds / GH runs | A/B cell within plan bounds (hook/time/audience/CTA only). |
| `depends_on` | CC | `row_id`(s) that must publish first; GH honours the order. |
| `approval_status` | CC (step-3 gate) | `approved` \| `revise` \| `hold` — only `approved` rows are handed off. |
| `notes` | CC | free text GH needs to publish faithfully without re-strategising. |

---

## 3. Idempotency & keys (CC's lane vs GH's)

- **CC's key obligation:** `row_id` and `spoke_asset_ref` are **ULIDs, unique and stable on retry/revision** — never regenerated on a revise (carry the same id, bump the asset's `vN`). GH's execution-log and the Brain's `performance-analytics-growth` join on them, so a regenerated id orphans the performance trail.
- **At-least-once handoff + idempotent execute:** re-delivering the same `row_id` is a **no-op** for the Growth Hacker (it does not double-publish).
- **GH does NOT author rows or change CC-owned fields** — it only advances `status`, applies `tracked_cta_utm`, runs the `variant` test, and reshapes native form.

---

## 4. The approval gate (only `approved` rows cross the seam)

- The Content Creator's **step-3 human gate** sets each row's `approval_status`. **Only `approved` rows enter the handoff bundle**; `revise`/`hold` rows stay back until cleared.
- **Paid rows carry the Media Planner's budget-approval state** — the Growth Hacker honours the paid-approval gate (Media Planner mandate §6) and does not spend on a row whose paid approval is unmet.
- **First-send of any NEW email sequence is human-gated** on the GH side — flag new sequences in `notes` so the gate is honoured.

---

## 5. Why a Spine record, NOT a Brain feed (do not route this through brain_io)

The calendar is **per-row, mutable-on-execute** (the Growth Hacker advances `status` and writes `tracked_cta_utm` back onto the row) — exactly the live mutable state the append-only Brain **cannot hold**. The Brain's `performance-analytics` is **append-only AGGREGATES, one writer, no per-row mutation** — there is nowhere to advance a row's status. **Therefore** the calendar is a `publishing-calendar` **queue/table in `_spine/`** that the Growth Hacker polls/executes. **Aggregate** performance (engagement by asset × format × channel) flows to the Brain via `performance-analytics-growth-YYMMDD` as **numbers** — never the calendar rows themselves.

---

## 6. Field discipline (the failure modes)

**Content Creator must NOT:** set `status` or `tracked_cta_utm` (pre-filling them corrupts the seam); publish or instrument anything; invent a `channel` outside `<<CHANNEL_SET>>`; author a message/claim/channel "variant" (out of bounds); hand off a `revise`/`hold` row.

**Growth Hacker must NOT:** re-argue the thesis or rewrite the claim; reassign `publish_as`, `funnel_stage`, `channel`, or `format`; regenerate `row_id`/`spoke_asset_ref`; publish a paid row without budget approval; auto-send a new email sequence without the first-send human gate.

---

## 7. Pilot reality

The conductor (`iksh`) isn't live. In the pilot, the Content Creator **writes the calendar record by convention** to `_spine/`, and an operator / the Growth Hacker polls it; the Growth Hacker advances `status` and applies `tracked_cta_utm` by hand. The skill **proposes and drafts** — it does not publish or send autonomously. Aggregate counts to the Brain are fine; the mutable calendar rows stay in the Spine.
