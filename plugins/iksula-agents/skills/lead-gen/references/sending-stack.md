# Execution Layer — The Sending Stack (Woodpecker / Mailerlite)

The bridge from a *drafted* sequence to a *staged, ready-to-send* campaign. The agent **builds and stages**; it does **not** flip sending on. Read this before any enroll/trigger step.

> **SEND-MODE IS OFF BY DEFAULT.** Building campaigns and enrolling leads is *staging*, not sending. Sending only turns on **per-segment**, and only when ALL hold: (1) lawful basis set on those exact records, (2) suppression scrub passed, (3) sending domain warmed, (4) a human approved the first send. Absent any one → stage only, leave paused.

---

## 1. Which tool for which job
| Channel | Tool | Use |
|---|---|---|
| **Cold 1-to-1 outbound** | **Woodpecker** | prospecting sequences to identified, lawful-basis-cleared prospects. Linear campaigns + Router branching (below). |
| **Opted-in nurture / newsletter / promo** | **Mailerlite** | template/broadcast email to *consented* contacts only (blog digest, promos). Never cold. |
| **State of record** | **Zoho CRM** | lifecycle, scores, suppression, every campaign transition. The durable layer. |

Pick by **email type**, never mix a cold prospect into a Mailerlite opted-in list or vice versa.

---

## 2. Woodpecker — the hard constraints (design around these)
- **API access is gated** behind Woodpecker's "API & integrations" add-on. Confirm it's active before any API call.
- Prefer the **official MCP server** (`Woodpeckerco/woodpecker-mcp-server`) over hand-rolled REST; fall back to **v2 REST** (`/v2/campaigns`, `/v2/campaigns/{id}/steps`, `/run`, `/pause`) where the MCP tool set falls short.
- **Branching is capped at ONE condition per campaign, UI-only — NOT API-configurable.** Do not try to build a decision tree inside one campaign.
- **Stop-on-reply is automatic.** Do not re-send after a reply.

## 3. The branching model — multi-campaign routing (not in-campaign branching)
Because of the 1-condition limit, build **several small LINEAR campaigns** and let an **always-on Router** (n8n/Make/webhook service — infra, *outside* this agent) move prospects between them on activity webhooks.

Campaign building blocks (all linear — buildable via `addStep`):
- **C0 — Cold Intro** (touch 1 relevance hook + soft CTA · touch 2 new angle) — entry.
- **C1-Hot** (sales-y follow-up · call/time CTA) — for **clickers**.
- **C1-Value** (case study · objection handle) — for **non-engagers**.
- **C2-Breakup** (permission-to-close) — final attempt.
- **C-Nurture** (slow drip) — post-breakup, stay warm.

Router rules (the agent does NOT run these — it documents them for the Router):

| Webhook | Action |
|---|---|
| `link_clicked` | → enroll in **C1-Hot**; Zoho `intent=high`; Slack hot-lead alert |
| `campaign_completed` (C0, no click/reply) | → enroll in **C1-Value** |
| `campaign_completed` (C1-Value, no reply) | → enroll in **C2-Breakup** |
| `prospect_replied` / `prospect_interested` | auto-stop → Zoho `Replied`/SQL → **Slack: AE accepts the SQL** |
| `prospect_bounced` / `prospect_opted_out` | → Zoho suppression; never re-enroll |

**Branch on CLICKS + REPLIES only — NEVER opens.** Apple Mail Privacy fakes ~50% of opens; open-based branches misfire half the time. Opens are noise.

---

## 4. The agent's job in the execution layer (and its hard stops)
1. **Confirm the cleared segment.** Only leads that passed the lawful-basis gate + synchronous suppression scrub (see `seam-and-compliance.md` §6) are eligible. No basis → not enrolled. Full stop.
2. **Build/refresh the linear campaigns + steps + copy** via the Woodpecker MCP/API, matching the sequence spec Vishal defines (count, per-step copy type). Use the per-touch copy structure: touch 1 = relevance hook + soft CTA (~75–100 words); follow-ups = new value, 4+ sentences; break-up = permission close. **Soft/interest CTAs for cold** — no meeting-time ask until they engage.
3. **Enroll the cleared segment** into C0 via `addProspectsToCampaign`.
4. **Leave it PAUSED / first-send manual.** The agent does not auto-run the campaign. Surface a Slack approval for the first send; a human triggers it. Subsequent campaign-to-campaign moves are the Router's job once live.
5. **Write state to Zoho** — enrollment, campaign, lifecycle/score — so the next agent run sees current reality.

### What the agent must NOT do
- Must not enroll a lead without lawful basis on that record.
- Must not flip send-mode on or auto-run a campaign at scale — first send is human-gated.
- Must not put a cold prospect into Mailerlite (opted-in only) or branch on opens.
- Must not invent the sequence structure where Vishal owns it — build to the defined spec; flag if copy doesn't fit the sequence.

---

## 5. Pilot path (how the first real send happens safely)
1. Vishal locks the first sequence set (start with one branch: C0 → click→C1-Hot / no-click→C1-Value → C2-Breakup).
2. Infra warms a secondary sending domain (3–6 wks new domain).
3. Pick **one small, genuinely-consented segment**; set lawful basis on just those records.
4. Agent builds + enrolls that segment, leaves paused.
5. Human approves → first send. Router takes over branching. State syncs to Zoho.
6. Prove deliverability (bounce <2%, spam <0.3%), then widen.

*Full background: the Woodpecker connector brief and the multi-campaign routing design (team docs, 260618).*
