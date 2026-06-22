# The Seam — `content-sourced-lead` (GH → Lead Gen)

*The single handoff from the Growth Hacker to Lead Gen. One seam, one direction, one object. GH emits **raw interest events**; Lead Gen owns everything after. This file is the payload schema, the region/lawful-basis stamping rule, the idempotency contract, and the justification for why it is a **Spine record, not a Brain feed**.*

**Version:** 1.0 · **Owner of the object's emit side:** Growth Hacker (provenance `emitted_by = 'growth-hacker'`). **Owner of everything downstream:** Lead Gen.

---

## 1. The boundary (memorise this)

GH **surfaces interest at the event level and hands it over verbatim**. Lead Gen owns: de-anonymization (geo-gated), enrichment, de-dupe into the canonical CRM record, lawful-basis sign-off, the synchronous suppression scrub, MQL→SQL qualification, nurture, ABM, and route-by-account-status. **The seam carries NO score and NO account-status decision.**

Reference-channel leads do **NOT** come through this seam — they enter Lead Gen pre-qualified, MQL-bypassed, from delivery touchpoints. **This seam is the Online/organic feed only.**

---

## 2. Payload schema (one record per detected interest event)

| Field | What GH puts in it |
|---|---|
| `correlation_id` | **ULID** — the dedupe/idempotency key for THIS handoff event (re-delivery is a no-op). Also ties back to the campaign chain (SoT → package → calendar → performance). **Unique + stable on retry.** |
| `contact_identity` | Whatever GH **actually observed**, UNqualified + UNenriched: e.g. `{platform_handle, display_name, profile_url, and/or email IF the contact volunteered it via a form/CTA}`. May be partial/anonymous (a tracked click with only a `click_id`). **GH does NOT de-anonymize.** |
| `source_asset_ref` | The `asset_ref` / post / campaign that surfaced the interest (resolves into the content package + `performance-analytics-growth`). |
| `source_channel` | The distribution channel + surface, e.g. `LinkedIn-post`, `LinkedIn-DM`, `Blog-form`, `YouTube-comment`, `X-thread`, `tracked-CTA-click`. Always a GH online/organic surface → tags this as the **Online** channel in Lead Gen's four-channel funnel. |
| `intent_signal` | The raw observed action, verbatim: `{signal_type ∈ [comment, reply, dm, form_fill, content_download, cta_click, connection_accept, mention], verbatim_text (anonymised, provenance kept), observed_at}`. **NO score** — GH surfaces, never qualifies. |
| `region` | Observed/best-known region of the contact (from IP/locale/profile), mapped against `icp-audience` geography. |
| `lawful_basis_tag` | **Derived from `region`** (see §3): `US → person-level de-anon permitted` vs `EU/India/other → company-level ONLY (GDPR/DPDP)`. **Stamped by GH** so Lead Gen's geo-gate + synchronous suppression scrub run correctly **before** any contact. |
| `captured_at` | ISO-8601 UTC timestamp of the detection event. |
| `emitted_by` | `'growth-hacker'` (provenance / one-writer attribution). |
| `consent_context` | Any consent/opt-in observed at capture (form checkbox, newsletter opt-in) or `null`; feeds Lead Gen's lawful-basis sign-off. |
| `ack_status` | **Written back BY Lead Gen** on consume (`received` / `de-duped` / `rejected` + `reason_code`). **GH does not set it.** |

---

## 3. Region → lawful-basis stamping (GH stamps; Lead Gen enforces)

GH has the IP/locale at capture, so **GH stamps** `region` + `lawful_basis_tag` using the `icp-audience` geography map:

- **US** → `person-level de-anon permitted` (Lead Gen may de-anonymize to a person downstream).
- **EU / India / other non-US** → `company-level ONLY` (GDPR / India DPDP) — person-level de-anon is prohibited.

The tag is **advisory provenance**. **Lead Gen ENFORCES** it — geo-gate + a SYNCHRONOUS suppression scrub before any send, never sending without re-checking. GH never de-anonymizes and never sends person-level outreach off the back of this — it only stamps the tag so the downstream gate runs correctly.

---

## 4. Idempotency & the canonical key (GH's lane vs Lead Gen's)

- **GH's only key obligation:** the per-event `correlation_id` (ULID) is **unique and stable on retry**. At-least-once delivery + idempotent consume → re-delivery is a no-op.
- **GH does NOT own or compute the canonical person/account key.** Lead Gen resolves the canonical record on **normalized email** (lowercased, trimmed) when an email exists; when none yet (anonymous click / handle-only) it resolves on a deterministic composite (`platform + platform_handle/profile_url`, else `click_id`) and **promotes** to the email key once de-anon/enrichment yields one — merging duplicates into the single CRM record. **All of that is Lead Gen's**, not GH's.

---

## 5. Why a Spine record, NOT a Brain feed (do not route this through brain_io)

This payload is **per-prospect, mutable-on-consume, PII-bearing**, and feeds **de-dup + suppression lookups** — exactly the live mutable per-prospect state the append-only Brain **cannot hold** (the honest pilot limit). Putting lead rows in the Brain would break the contract:

- The Brain's `performance-analytics` is **append-only AGGREGATES**, one writer per namespace, **no per-row mutation, no PII** — there is **nowhere to write the `ack_status` or the de-dup verdict**.
- Lead rows are per-prospect PII → violate the no-PII / raw-first contract.
- The Spine is the assets + run-records layer, and the CRM seam + human gates already live there; the **canonical durable record** (de-dup, suppression, scoring, account graph) resides **CRM/Spine-side**.

**Therefore:** the seam is a `content-sourced-lead` **queue/table in `_spine/`** that Lead Gen polls/consumes. In the pilot it is written by **convention** and an operator / Lead Gen polls it; at the MCP-wrap it becomes a real queue/topic. **Aggregate counts** (how many content-sourced leads, by channel) DO flow to the Brain — but via `performance-analytics-growth-YYMMDD` as **numbers**, never as the lead rows themselves.

---

## 6. What GH must NOT do on the seam (the failure modes)

- **No score / no grade / no MQL-SQL label.** If GH stamps any fit/intent score you get two incompatible funnels. The seam carries the raw signal only; qualification is owned ONCE, in Lead Gen.
- **No de-anonymization / no enrichment / no CRM de-dupe.** Lead Gen's job, downstream.
- **No account-status routing.** GH cannot see CRM account state; new-vs-ECS (new → Sales/NCA; existing ECS → KAM, never cold-pitch a current client) is Lead Gen-only.
- **No Reference leads through this seam.** Reference is a separate Lead Gen channel, MQL-bypassed; never route it here.
- **No Brain-as-lead-store.** Never route the per-prospect handoff through a namespaced brain_io feed (no per-row mutation, no ACK, no de-dup verdict, no PII allowed).
- **No autonomous send at scale.** If GH ever broadcasts a BOFU/owned email itself, **first-send of any new sequence is human-gated** — propose/draft; a human approves.

---

## 7. Pilot reality

The conductor isn't live. In the pilot, GH **writes the seam record by convention** and an operator / Lead Gen polls the Spine queue; real outbound is human-gated. The skill **proposes and drafts** — it does not autonomously qualify or send. Aggregate counts to the Brain are fine; lead rows stay in the Spine/CRM.

---

**Runnable enforcement:** the iksula-agents plugin's `tools/growthhacker/seam_emitter.py` implements this contract — ULID idempotency, region → `lawful_basis_tag` (fail-safe to company-level for non-US), recursive rejection of any score/grade/MQL/ack/account-status field (incl. nested in `intent_signal`/`contact_identity`), `ack_status` left null, Spine-only (never the Brain). Use `seam_emitter.emit(event)`; never hand-build the record. Tests (from `tools/`): `python -m unittest growthhacker.tests.test_safety`.
