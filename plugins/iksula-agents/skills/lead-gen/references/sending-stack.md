# Execution Layer — The Sending Stack (Woodpecker / Mailerlite)

The bridge from a *drafted* sequence to a *staged, non-sending* campaign. The agent **builds and stages**; it does **not** flip sending on. Read this in full before any create/enroll step — the prohibitions here are hard stops, not guidance.

> **SEND-MODE IS OFF BY DEFAULT.** Building a campaign and enrolling leads is *staging*, not sending. The **run / resume / start verb is NEVER the agent's to call — on ANY campaign, including one it created this run.** Creating a campaign grants no authority to start it. Sending turns on **per-segment, by a human**, and only when ALL hold: (1) lawful basis set on those exact records, (2) suppression scrub passed, (3) sending domain warmed, (4) a human approved the first send. Absent any one → stage only, leave it in a non-sending state.

> **THIS IS A LIVE PRODUCTION ACCOUNT — the agent is a guest.** Verified 19 Jun 2026: **97 campaigns** exist (3 RUNNING cold campaigns, 4 PAUSED, 8 DRAFT, 82 COMPLETED), sending from real Iksula mailboxes across `iksula.com` (primary), `us.iksula.com`, `in.iksula.com`, operated by several humans (vishal.s, vishal.sobti, pavan.k, sam, subhasan.d). The agent **creates new campaigns only.** A campaign is "the agent's own" **iff its id is in the agent's creation ledger** (below) — *never* inferred from a name. Every campaign **not in the ledger** is **strictly read-only**: never pause, run, resume, stop, edit, delete, or enroll into it. The 3 RUNNING and 4 PAUSED campaigns are live revenue work; touching them is the worst-case failure.

---

## 1. Which tool for which job
| Channel | Tool | Use |
|---|---|---|
| **Cold 1-to-1 outbound** | **Woodpecker** | prospecting sequences to identified, lawful-basis-cleared prospects. Linear campaigns + Router branching (below). |
| **Opted-in nurture / newsletter / promo** | **Mailerlite** | template/broadcast email to *consented* contacts only (blog digest, promos). Never cold. |
| **State of record** | **Zoho CRM** | lifecycle, scores, suppression, consent basis, the campaign-creation ledger, every campaign transition. The durable layer. |

Pick by **email type**, never mix a cold prospect into a Mailerlite opted-in list or vice versa.

---

## 2. Woodpecker — verified connector facts & hard constraints (design around these)
- **API access is verified ACTIVE** (the "API & Integrations" add-on; confirmed 19 Jun 2026). **Base URL `https://api.woodpecker.co`; all paths rooted at `/rest`.** Auth = the API key in header `x-api-key` (HTTP Basic with the key as username also works). The key is secret — it lives only in env `WOODPECKER_API_KEY` (MCP server) or a gitignored local file (REST); **never** hardcode, commit, ship, or paste it in Slack/WhatsApp.
- **READ** campaigns via `GET /rest/v1/campaign_list` (returns campaign **metadata only** — names, ids, status, sender; no prospect PII). `GET /rest/v2/campaigns` exposes no GET (returns **405**, observed 19 Jun 2026) — read via v1, do not infer endpoint behaviour from status codes at runtime.
- **CREATE-ONLY** on v2: `POST /rest/v2/campaigns` builds a whole linear campaign in ONE call (steps inline) — verified 19 Jun 2026 (HTTP 201 → DRAFT, then cleanly deleted). Required body: `name` + `email_account_ids` (**≥1 mailbox — there is NO sender-less create via API**) + `settings{timezone, daily_enroll}` + a `steps` `START`→`EMAIL` `followup` chain with copy in `body.versions[]`. `POST /rest/v2/campaigns/{id}/steps` adds steps to an existing **own** campaign. Operate **only against an id this run just created.** A 405 on a *POST create* is a real failure — surface it, never silently retry. **The agent MUST NOT call `/run`, `/pause`, `/resume`, `/stop`, `/delete`, or any state-changing endpoint on ANY campaign** — those are operated by humans only (DELETE works — verified — but is operator-only cleanup, never the agent's).
- **Prefer the official MCP server** (`Woodpeckerco/woodpecker-mcp-server`) over hand-rolled REST. **These rules are interface-agnostic** — they bind equally to MCP tools (`addStep`, `addProspectsToCampaign`, `runCampaign`, …) and to raw REST. The MCP path is not a loophole; if an MCP tool would write to / start a campaign the agent does not own, do not call it (`runCampaign`/`pauseCampaign`/`deleteCampaign` are never the agent's to call).
- **Branching is capped at ONE condition per campaign, UI-only — NOT API-configurable.** Do not try to build a decision tree inside one campaign (see §3).
- **Stop-on-reply is automatic.** Do not re-send after a reply.
- **The API rate limit is ACCOUNT-WIDE and SHARED** with Vishal's live campaigns and the Router (~1 request processed + 6 queued; HTTP 429 beyond). The agent must **serialize its calls** (max 1 in-flight), space them, and on any 429 **back off exponentially and yield** — never retry-storm. A burst of create/step/list calls that starves or delays the 3 RUNNING campaigns is a failure. If 429s persist, ABORT and Slack-flag rather than hammer.
- **Per-mailbox daily sending caps (~20–49/day) are SHARED across all campaigns on that mailbox** — a mailbox property, not a per-campaign send toggle, so "send-mode OFF" does **not** protect it. See the mailbox-isolation rule in §4.
- **Native warm-up is NOT a first-class feature** — treat warmed secondary domains as a separate infra need.

## 3. The branching model — multi-campaign routing (not in-campaign branching)
Because of the 1-condition limit, build **several small LINEAR campaigns** (building blocks) and let an **always-on Router** (n8n/Make/webhook service — infra, *outside* this agent) move prospects between them on activity webhooks.

Building blocks (all linear — buildable via create + `addStep`):
- **C0 — Cold Intro** (touch 1 relevance hook + soft CTA · touch 2 new angle) — entry.
- **C1-Hot** (sales-y follow-up · call/time CTA) — for **clickers**.
- **C1-Value** (case study · objection handle) — for **non-engagers**.
- **C2-Breakup** (permission-to-close) — final attempt.
- **C-Nurture** (slow drip) — post-breakup, stay warm.

Router rules (the agent does **not** run these — it documents them, and its ledger, for the Router):

| Webhook | Action |
|---|---|
| `link_clicked` | → enroll in **C1-Hot**; Zoho `intent=high`; Slack hot-lead alert |
| `campaign_completed` (C0, no click/reply) | → enroll in **C1-Value** |
| `campaign_completed` (C1-Value, no reply) | → enroll in **C2-Breakup** |
| `prospect_replied` / `prospect_interested` | auto-stop → Zoho `Replied`/SQL → **Slack: AE accepts the SQL** |
| `prospect_bounced` / `prospect_opted_out` | → Zoho suppression; never re-enroll |

**Branch on CLICKS + REPLIES only — NEVER opens.** Apple Mail Privacy fakes ~50% of opens; open-based branches misfire half the time.

**Router scoping (hard requirement):** the account-level webhook stream fires for **all 97 campaigns**, including Vishal's live ones. The Router must **filter events by `campaign_id` against the agent's creation ledger** and act ONLY on agent-created campaigns (and Vishal's tooling ignores those). An unscoped Router on this shared account is a hard no — it would cross-contaminate live prospects.

---

## 4. The agent's job in the execution layer (create-only, ledger-gated)

**0. Lawful basis is the gate — enrolling IS a PII write.** Creating a campaign and enrolling prospects writes prospect PII (emails, names, merge fields) into **Woodpecker's account-wide prospect database — a third-party store, NOT Zoho.** So enrollment runs the **same four pre-send checks AT ENROLL TIME** (`seam-and-compliance.md` §6), per record: (1) `Data_Processing_Basis ∈ {Legitimate Interests, Contract, Consent-Obtained}` — **re-read from Zoho at enroll, never cached**; (2) synchronous suppression scrub (opt-out + ECS/client union); (3) geo-gate (person-level US-only); (4) first-send human gate. A record failing any check is **not added to Woodpecker at all** — not added-then-paused. **With 100% of Zoho leads at null `Data_Processing_Basis` today, the correct number of prospects the agent writes into Woodpecker is ZERO.**

1. **Load the creation ledger first.** A durable record (a Zoho CRM custom record — preferred, since Zoho is system-of-record — or a `_spine` append-only log) of every campaign the agent has created: `{run_id, campaign_id, exact_name, sender_mailbox, segment, created_at_utc}`. **"Campaigns it owns" = exactly the `campaign_id`s in this ledger** — never the `[LG-AGENT]` name prefix. An `[LG-AGENT]`-named campaign **not** in the ledger is treated as **foreign / read-only** and flagged to Slack for human reconciliation (it may be a human's copy or an orphan).

2. **Build NEW linear campaigns (create-only) to Vishal's spec.** There is **no refresh/update path.** If a campaign for the intended segment already exists in the ledger from a prior run, do **not** edit, re-step, or re-enroll it — ABORT and surface to a human. Match the sequence spec Vishal defines (count, per-step copy type). Per-touch copy: touch 1 = relevance hook + soft CTA (~75–100 words); follow-ups = new value, 4+ sentences; break-up = permission close. **Soft/interest CTAs for cold** — no meeting-time ask until they engage.
   - **Namespacing + collision safety:** name every created campaign `[LG-AGENT] <segment> <region> <yymm> <run_id-short>` (run-scoped suffix → unique). Before create, `GET /rest/v1/campaign_list` and read **every** campaign across **all** statuses and **all** pages; ABORT if any name case-insensitively equals or starts with the intended name **and** is not in the ledger (never delete/edit it). If the list is truncated/un-enumerable, treat collision-detection as FAILED → abort. Concurrent operators exist → take a per-namespace lock (Zoho/Slack mutex) before create.
   - **Write only to your own id.** Operate (`addStep`, enroll) **only** on the id returned by your own create call / your ledger record. **NEVER** resolve a write target by name-matching `campaign_list` output — that endpoint is read-only metadata for collision-checking and reporting, never a source of ids to write to.
   - **Mailbox isolation.** Assign **only** an infra-provisioned, **warmed secondary-domain** mailbox (`us.iksula.com` / `in.iksula.com` / a dedicated warmed domain) from an out-of-band allow-list. **NEVER** the primary `iksula.com`, **never** `sam@`/`vishal.s@`/`vishal.sobti@`/`pavan.k@`/`subhasan.d@`, and **never** any mailbox already attached to a RUNNING/PAUSED campaign (shared daily caps → you'd steal live sending quota and spike primary-domain cold volume). **No isolated warmed mailbox → the agent CANNOT build at all** (v2 create requires ≥1 mailbox — verified, no sender-less create): ABORT and Slack-flag infra to provision one. Never borrow a live mailbox. *(As of 19 Jun 2026 only 2 secondary-domain mailboxes exist — both `vishal.sobti@us./in.iksula.com`; dedicated warmed cold-send mailboxes are still an open infra gap.)*
   - **Idempotent create:** after a successful `POST /campaigns`, append to the ledger **before** adding steps; if a step call 429s/fails mid-build, the next attempt **resumes** the ledgered half-built campaign — never creates a duplicate.

3. **Enroll the cleared segment — and only into a confirmed non-sending campaign.** Adding prospects to a **RUNNING** campaign **sends** to them on the next slot. So immediately before any add-prospects call, `GET` the target status and confirm it is **DRAFT or PAUSED**; if RUNNING, do **not** enroll — full stop. Enroll **only** the records that passed step 0, **only** via `addProspectsToCampaign` on a ledgered `[LG-AGENT]` campaign. Never bulk-import/update prospects at the account level; never modify or delete a prospect already in the global pool (it may back Vishal's running campaigns).

4. **Leave it in a NON-SENDING state (DRAFT or PAUSED) — never RUNNING.** Campaigns created via the API default to **DRAFT** (non-sending) — correct, leave it. After create and after every enroll, `GET` the status and assert DRAFT/PAUSED; if ever RUNNING, ABORT and alert a human. The agent never calls `/run` or sets status=RUNNING. The first send is always a human action via Slack.

5. **Write state to Zoho + announce.** Write enrollment, campaign, lifecycle/score to Zoho (system-of-record) so the next run sees reality. After the run, post **one Slack summary** to the agreed channel: each campaign created (name, id, mailbox, segment, count) + the `run_id` — **counts and metadata only, never prospect emails/PII** (to review who's enrolled, the human opens Woodpecker/Zoho directly).

**Caps & kill-switch:** create at most **N campaigns per run** (small, e.g. 5; set explicitly) — on hitting the cap, stop and Slack-flag. If env `WOODPECKER_AGENT_BUILD=off` (or a designated Slack stop keyword is seen), make **zero** write calls this run. Because delete is forbidden, re-list immediately before each create and abort if the `[LG-AGENT]` count already exceeds the expected ledger count (a runaway sign) pending human cleanup.

**Suppression freshness:** staged-but-paused is **not** send-safe forever. Before any first send is approved, the suppression scrub + lawful-basis check are **re-run against Zoho at that moment**; any record now suppressed/null-basis is removed first. The **one** permitted write to a campaign the agent created on a *prior* run is to **remove** (never add) a prospect to honour a fresh opt-out/suppression — and only on a ledgered `[LG-AGENT]` campaign.

### What the agent must NEVER do (absolute hard stops)
- **Never start a send.** No `/run`, `/resume`, `/start`, status=RUNNING — on ANY campaign, **its own included**. Creating ≠ permission to start.
- **Never touch a non-ledgered campaign.** No pause/run/resume/stop/edit/delete/enroll on any of the 3 RUNNING, 4 PAUSED, 8 DRAFT, or 82 COMPLETED campaigns — or any `[LG-AGENT]`-named campaign absent from the ledger.
- **Never enroll a record without lawful basis** on that exact Zoho record (re-read live, not cached) + a passed suppression scrub. Today that is **zero** records.
- **Never enroll into a RUNNING campaign** (that is sending) — including one it created this run.
- **Never reuse a live/primary-domain mailbox**, bulk-write the global prospect pool, or modify/delete an existing prospect.
- **Never resolve a write target by name** (only your own create-returned id / ledger).
- **Never write Woodpecker-sourced prospect PII** to the Brain, `_brain/_raw/`, Drive, Slack/WhatsApp, or the `performance-analytics-leadgen` feed (aggregates only, no PII; per-prospect state lives ONLY in Zoho). Don't pull prospect-list/stats/export/activity on campaigns you don't own.
- **Never put a cold prospect into Mailerlite** (opted-in only) or branch on opens.
- **Never invent the sequence structure** where Vishal owns it — build to the defined spec; flag if copy doesn't fit.

---

## 5. Pilot path (how the first real send happens safely)
1. Vishal locks the first sequence set (start with one branch: C0 → click→C1-Hot / no-click→C1-Value → C2-Breakup).
2. Infra warms a secondary sending domain (3–6 wks new domain) + provisions an **allow-listed, isolated** mailbox (not a live one).
3. Pick **one small, genuinely-consented segment**; set `Data_Processing_Basis` on just those Zoho records (until then, the agent stages **zero** prospects).
4. Agent builds new `[LG-AGENT]` campaigns + enrolls only the cleared records, leaves them non-sending, ledgers + announces.
5. Human re-scrubs, approves → **human** triggers the first send. The (scoped) Router takes over branching. State syncs to Zoho.
6. Prove deliverability (bounce <2%, spam <0.3%), then widen.

*Full background: the Woodpecker connector brief and the multi-campaign routing design (team docs, 260618). Connector verified + account inventory: `woodpecker_smoke.sh` (read-only).*
