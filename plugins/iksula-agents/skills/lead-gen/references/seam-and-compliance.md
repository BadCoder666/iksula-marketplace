# The seam (consume side) + the compliance playbook — Lead Gen

*Lead Gen's companion to the Growth Hacker's `seam-contract.md`. Same object, same fields, same Spine-not-Brain rule — read from the consume side — plus the Lead-Gen-owned enforcement (geo-gate, lawful basis, suppression scrub, routing). If this and the GH `seam-contract.md` ever disagree, they are wrong; re-sync them.*

> **CRM = Zoho CRM** (US DC, org `29004087`), the system-of-record for the mutable per-prospect state. The generic "CRM" references below resolve to it; the verified field-level bindings are in **§6**.

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

---

## 6. Zoho CRM field bindings (the system-of-record)

*Verified against the live Iksula production org (US DC, org `29004087`) on 2026-06-09. The CRM is mature and organically grown — match on the specific field/API name, never on raw display strings, and treat unmapped values as fail-closed where a gate depends on them.*

**Already present — reuse as-is (the agent reads these; do not rename/delete):**

| Gate / function | Zoho binding | Rule |
|---|---|---|
| **Lawful-basis gate** | `Data_Processing_Basis` (Leads + Contacts) | Permit send only when value ∈ {`Legitimate Interests`, `Contract`, `Consent - Obtained`}. {`Consent - Pending`, `Consent - Waiting`, `Consent - Not Responded`} → `ON_HOLD`. |
| **DNC / opt-out (`<<DNC_SOURCE>>`)** | `Leads.Email_Opt_Out` (standard) **and** `Contacts.Email_Opt_out1` (custom api_name) — bind **per module** | Hard-block send when the module-appropriate boolean = true. `Unsubscribed_Mode` is the opt-out *reason* (audit only), never the gate. |
| **Existing-client suppression + KAM routing (`<<SUPPRESSION_CUSTOMER_SRC>>`)** | OR-union: `Contacts.Customer_Type ∈ {EC, Past}` · `Contacts.Contact_Type1 = Customer` · `Customer_Classification ∈ {ECN, ECS, ECH}` (Contacts/Accounts) · linked `Account.Customer_Type ∈ {EC, ECS}` · linked `Deal.Type ∈ {Existing Business (ECS), New Business in Existing (ECN)}` | Any hit → suppress cold + route **KAM**. Eligible-cold cohort = `Customer_Type ∈ {Prospect, Suspect}` / `Deals.Type = New Business (NC)`. **"ECS" is overloaded** (a tier in `*_Classification`, a relationship type in `Customer_Type`/Deals) — match by field. |
| **Lifecycle (mid/late)** | `Contacts.Contact_Type1` (already has `MQL`, `SQL`, `Customer`); `Deals.Stage` | `OPPORTUNITY` is **derived** from an open linked Deal (`Stage` ∈ open set), not stored. `CUSTOMER` = `Deals.Stage = Closed Won` (authoritative), cascaded to `Contact_Type1 = Customer`. |
| **Geo gate** | canonical `Accounts.Region` {`INDIA`, `AMERICAS`, `MENA`, `ASEAN`, `ROW`, `EUROPE`} | **`AMERICAS` ≠ US** → US-only person-level de-anon also needs a country check (e.g. `Region1 = USA`). Prohibit when region ∈ {`EUROPE` (GDPR), `INDIA` (DPDP)}. **Fail-closed** on the messy `Leads.Region_Geography` until normalized. |
| **Enrichment state** | `Enrich_Status__s` (`Available`/`Enriched`/`Data not found`) | Feeder signal → derive `ENRICHING` lead status. |

**To be created by Vishal (see `Zoho CRM Config for Lead-Gen Agent - 260609`) — bind the exact API names once they exist:**

| Vocabulary | New Zoho field |
|---|---|
| Lead Status (NEW…SUPPRESSED) | `Leads.LG_Lead_Status` (agent-owned, parallel to the SDR-owned standard `Lead_Status`). |
| DQ/Recycle reason codes (`DQ_*`/`RC_*`) | `Leads.LG_Disqualify_Recycle_Reason`. (Do **not** key DQ off `Deals.Lost_Reason` — that's opportunity-level.) |
| Buyer Role (Economic Buyer…Gatekeeper) | `Contacts.Buyer_Role` — **but first verify native Deals Contact Roles in Setup** (API can't see it); native roles are the correct per-deal home. Lossy conversion heuristics only: `Are_we_connected_to_Decision_Maker=Yes → Economic Buyer`, `_Influencer=Yes → Influencer`, `_Recommender=Yes → Champion`. |
| SAL lifecycle stage | add value `SAL` to `Contacts.Contact_Type1`. |

> **Standard `Leads.Lead_Status` is ACTIVE / SDR-owned** (`Fresh`/`Contacted`/`Qualified Lead`/`Meeting Scheduled`/`Junk`…) — never silently repurpose it. Whether to keep the funnel split (agent `LG_Lead_Status` ∥ SDR `Lead_Status`, synced at hand-offs) or unify onto one spine is the open DJ + Vishal decision.
