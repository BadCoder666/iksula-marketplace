# The seam (consume side) + the compliance playbook — Lead Gen

*Lead Gen's companion to the Growth Hacker's `seam-contract.md`. Same object, same fields, same Spine-not-Brain rule — read from the consume side — plus the Lead-Gen-owned enforcement (geo-gate, lawful basis, suppression scrub, routing). If this and the GH `seam-contract.md` ever disagree, they are wrong; re-sync them.*

---

## 1. The seam object — `content-sourced-lead` (GH → Lead Gen)

One seam, one direction, one object. The **Growth Hacker emits raw interest events**; **Lead Gen owns everything after**. The seam carries **NO score and NO account-status decision**. Reference-channel leads do **NOT** come through this seam — they enter Lead Gen pre-qualified (MQL-bypassed) from delivery touchpoints.

**Payload (one record per detected interest event):**

| Field | Meaning (set by GH unless noted) |
|---|---|
| `correlation_id` | **ULID** — the dedupe/idempotency key for this handoff event. Re-delivery is a **no-op**. |
| `contact_identity` | Whatever GH observed, **unqualified + unenriched** (`{platform_handle, display_name, profile_url, and/or volunteered email}`); may be partial/anonymous (a `click_id` only). |
| `source_asset_ref` | The asset/post/campaign that surfaced the interest (resolves to the content package + `performance-analytics-growth`). |
| `source_channel` | The GH online/organic surface (`LinkedIn-post`, `LinkedIn-DM`, `Blog-form`, `YouTube-comment`, `tracked-CTA-click`…) → tags as the **Online** channel in Lead Gen's four-channel funnel. |
| `intent_signal` | The raw observed action, verbatim (`{signal_type ∈ [comment, reply, dm, form_fill, content_download, cta_click, connection_accept, mention], verbatim_text, observed_at}`). **No score.** |
| `region` | Best-known region of the contact (IP/locale/profile), mapped against `icp-audience` geography. |
| `lawful_basis_tag` | Derived from `region`: `US → person-level de-anon permitted` vs `EU/India/other → company-level ONLY (GDPR/DPDP)`. **GH stamps it; Lead Gen ENFORCES it.** |
| `captured_at` | ISO-8601 UTC timestamp of the detection event. |
| `emitted_by` | `'growth-hacker'` (provenance). |
| `consent_context` | Any consent/opt-in observed at capture (form checkbox, newsletter opt-in) or `null`; feeds lawful-basis sign-off. |
| `ack_status` | **Written back BY Lead Gen** on consume (`received` / `de-duped` / `rejected` + `reason_code`). GH never sets it. |

## 2. Idempotent consume + the canonical key (Lead Gen's lane)

- Treat delivery as **at-least-once**: consume is **idempotent**, keyed on `correlation_id` — a re-delivered event is a no-op.
- Resolve the **canonical CRM record** on **normalized email** (lowercased, trimmed) when an email exists. When none yet (anonymous click / handle-only), resolve on the deterministic composite (`platform + handle/profile_url`, else `click_id`) and **promote to the email key** once de-anon/enrichment yields one — merging duplicates into one record.
- Write the **ACK** back onto each consumed seam record (`received` / `de-duped` / `rejected` + `reason_code`).

## 3. Why a Spine record, NOT a Brain feed

The payload is **per-prospect, mutable-on-consume, PII-bearing**, and drives **de-dup + suppression lookups** — exactly the live mutable state the append-only Brain **cannot hold**. `performance-analytics` is append-only **aggregates**, one writer, **no PII** — nowhere to write `ack_status` or the de-dup verdict. So the seam is a `content-sourced-lead` **queue/table in `_spine/`** that Lead Gen polls; the durable de-duped/suppression/score record lives **CRM/Spine-side**. Aggregate counts (how many content-sourced leads, by channel) flow to the Brain as **numbers** via `performance-analytics-leadgen-YYMMDD`, never as lead rows.

---

## 4. The compliance playbook (Lead Gen ENFORCES — non-negotiable)

These are DJ's hard lines. Lead Gen owns enforcement; the gates run **synchronously before** any de-anon or send, never async/stale.

- **Geo-gate (person-level de-anon).** Person-level web de-anonymization (reverse-IP / visitor-intel → a named person) is **US-IP-only**. For **EU / India / other non-US** regions it is **company-level ONLY** (GDPR / India DPDP). Honour the seam's `lawful_basis_tag`; re-check region before acting. An automated test should assert **zero** person-level resolution fires on an EU/India IP.
- **Lawful-basis sign-off (human gate).** Before any person-level de-anon or any outbound, a human signs off the lawful basis for this contact/region. No basis → `ON_HOLD` or suppress; never proceed.
- **Synchronous suppression scrub (before EVERY send).** Check the canonical suppression store at send time (never a cached/stale copy): block unsubscribe/DNC, opt-outs, competitors, **and any existing client / open opportunity**. A seeded test must block a known client and a known opt-out before any real send is allowed.
- **Never cold-email an existing client.** Route by account status: **new/target → Sales / New Client Acquisition**; **existing ECS → Key Account Management** as an expansion signal (never a cold pitch). The authoritative existing-client / ECS watchlist is the **CRM / Master-Data client master** (read synchronously before outreach and before routing).
- **Reference bypasses MQL.** Reference leads are pre-qualified — never apply MQL metrics to them (a structural error, not a low score).
- **First-send human gate.** The first send of any new sequence is human-approved. In the pilot the agent **proposes/drafts**; a human approves the send — it does **not** autonomously send at scale.
- **No PII in the Brain.** Only aggregates go to `performance-analytics-leadgen`; the per-prospect record stays in CRM/Spine.

**Pre-send order (any failure → `ON_HOLD`, do not send):** lawful-basis present → synchronous suppression scrub → geo-gate re-check → first-send approval → send.

---

## 5. Reaching the Brain (brain_io — the two error-prone steps)

- **Resolve `_brain/` via a SEED FILE's `parentId`, not a folder-name search.** A search for a folder titled `_brain` returns **empty** on this connector. Instead `search_files: title contains 'brain_io-howto'` → take the newest result's `parentId` → that **is** the `_brain/` folder; reuse it. (The live `brain_io-howto` is authoritative for the exact IDs/recipe.)
- **Read feeds with `download_file_content`, NEVER `read_file_content`** — the latter reformats/escapes and **corrupts CSV**. Pick the newest module file by `modifiedTime` (same-day revisions carry a `-vN` suffix).
- Append-only; namespace this skill's writes `-leadgen-`; raw-first to `_brain/_raw/`.
