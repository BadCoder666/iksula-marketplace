# Controlled Vocabularies — Iksula Lead Gen Agent

*Adapted for the `lead-gen` skill. These closed enumerations are shared across the org (the same set is seeded to the Brain `method-vocab`); Lead Gen binds every CRM field, queue, and event to them.*

> **Purpose:** These are the **closed, identical-across-runs enumerations** the mandate, the scoring framework (A), the activity layer, and the Content-Creator interface all bind to. They are deliberately crisp so that two different runs of the agent — or the agent and a human — never disagree on what a term means. Where a value is founder-supplied it is shown as `<<PLACEHOLDER>>`; the **vocabulary itself (the allowed set of terms) is fixed**, only the per-Iksula values vary.
>
> **Rule:** No free-text where a controlled vocabulary exists. Every CRM field, queue, and event that uses one of these dimensions must validate against the enumerated set. New term = governance change (HITL-approved, versioned) — not an ad-hoc string.

---

## 1. Lifecycle Stages (where in the funnel)

Fixed spine, SiriusDecisions/Forrester-aligned. **One ordered enumeration, never conflated with Lead Status (§2).**

| Code | Stage | One-line definition |
|------|-------|---------------------|
| `SUBSCRIBER` | Subscriber | Known, opted-in; no buying interest yet |
| `LEAD` | Lead | Engaged contact attached to an account; fit not yet graded |
| `MQL` | Marketing-Qualified Lead | Buying group passed both Fit-grade and Engagement gates |
| `SAL` | Sales-Accepted Lead | Inside sales accepted the MQL as worth working |
| `SQL` | Sales-Qualified Lead | SDR-qualified, evidence-backed, meeting held |
| `OPPORTUNITY` | Opportunity | AE-accepted; deal in MEDDIC/MEDDPICC motion |
| `CUSTOMER` | Customer | Closed-Won (out of Lead Gen scope — Sales owns; becomes a suppression source) |

> Transitions are one-directional forward except via explicit **Recycle** (status, not stage). Demotion requires a reason code.

---

## 2. Lead Statuses (operational disposition *within* a stage)

Orthogonal to stage. A record always has exactly one stage **and** one status.

| Code | Status | Meaning |
|------|--------|---------|
| `NEW` | New | Created/sourced; not yet actioned |
| `ENRICHING` | Enriching | In verification/enrichment waterfall |
| `WORKING` | Working | Actively in a sequence / being touched |
| `ENGAGED` | Engaged | Replied / clicked high-intent / meeting in motion |
| `NURTURE` | Nurture | Long-cycle drip; not actively worked |
| `RECYCLED` | Recycled | Right-fit, not-now; returned to nurture with reason code |
| `ON_HOLD` | On Hold | Paused (compliance check, dedupe adjudication, deliverability freeze) |
| `DISQUALIFIED` | Disqualified | Hard-DQ; exited lifecycle with reason code |
| `SUPPRESSED` | Suppressed | Opt-out / DNC / customer / competitor — never contact |

**Disqualification / recycle reason codes (closed set):** `DQ_GEO`, `DQ_COMPETITOR`, `DQ_SUBSCALE`, `DQ_DNC`, `DQ_CUSTOMER`, `DQ_UNVERIFIED`, `RC_TIMING`, `RC_NO_BUDGET`, `RC_NO_NEED_NOW`, `RC_WRONG_PERSON`, `RC_REFERRED_OUT`.

**Reply-classification vocabulary (for inbound triage):** `INTERESTED`, `NOT_NOW`, `REFERRAL`, `OBJECTION`, `UNSUBSCRIBE`, `OOO`, `WRONG_CONTACT`, `HARD_NO`.

---

## 3. Channels (where the agent acts)

Closed enumeration; each channel carries an **autonomy default** (§7) and risk posture. This is the spine of the activity layer.

| Code | Channel | Autonomy default | Notes / risk |
|------|---------|------------------|--------------|
| `COLD_EMAIL` | Cold email + follow-ups | Autonomous (within volume governor) | Secondary domains only; bulk-sender + deliverability guardrails |
| `BEHAVIORAL_EMAIL` | Visitor-triggered auto-email (de-anon → behavioral send) | Autonomous | Fired on site engagement; consent/footer-gated |
| `LINKEDIN` | Connection / DM / InMail / post engagement / social-listen | **Approve-before-act** | ToS + rate-limit + ban risk; human-paced, HITL-gated |
| `INSTAGRAM` | Engagement / social-listen / DM | Approve-before-act | Brand handle; manual-heavy |
| `TWITTER_X` | Engagement / social-listen / DM | Approve-before-act | Brand handle; manual-heavy |
| `PHONE` | Cold calls / dials | Human-led (agent assists) | Agent schedules/logs/mines; human talks; TRAI DND/DLT |
| `WEBSITE` | Visitor tracking / de-anonymization / form capture | Autonomous (capture) | RB2B/Warmly/Koala; feeds behavioral email + scoring |
| `PAID` | LinkedIn Ads / Google Ads / programmatic ABM / retargeting | Approve-before-act (spend) | Budget-gated |
| `WEBINAR_EVENT` | Webinars, field/industry events | Approve-before-act | Registration → scoring pipe |
| `CONTENT_SYNDICATION` | Gated syndication (Pipeline360/NetLine/Foundry) | Approve-before-act | Junk-lead validation required |
| `SEO_CONTENT` | Organic/SEO + GEO/AEO discoverability | Autonomous (publish from approved assets) | Consumes Content Creator output |
| `REVIEW_SITES` | G2 / TrustRadius presence + intent | Approve-before-act | Intent capture + reputation |
| `PARTNER_REFERRAL` | Partner / referral / co-marketing | Human-led | List-sharing consent gates |
| `DEAD_LEAD_REENGAGE` | Recycled/dead-lead re-engagement | Autonomous (within suppression) | Re-MQL motion |

---

## 4. Automation / Solution Archetypes (adapted for growth)

How each capability is *implemented* — the build-pattern vocabulary (reused from the KB's archetype tags, growth-scoped).

| Code | Archetype | Growth meaning |
|------|-----------|----------------|
| `AUTONOMOUS_AGENT` | Autonomous Agent | Agent decides + acts end-to-end within guardrails (e.g., deliverability autopilot, verified-list pipeline, sequence dispatch) |
| `RPA_LLM_HYBRID` | RPA + LLM Hybrid | Deterministic flow + LLM judgment (waterfall enrichment, dedupe/survivorship, routing) |
| `COPILOT_ASSIST` | Copilot / Agent-Assist | Agent drafts/suggests, human decides (per-row personalization, reply drafting, SQL pre-qual) |
| `PREDICTIVE_MODEL` | Predictive Model | Scoring/ranking/forecasting (fit grade, intent prioritization, model-lift back-test) |
| `DOC_EXTRACTION` | Doc-Extraction Pipeline | Structured pull from unstructured (MEDDIC slots from transcripts, list parsing) |
| `NL_ANALYTICS` | NL-Analytics | Natural-language interrogation of the funnel ("where is the funnel leaking?") + auto-narratives |
| `SEMANTIC_SEARCH` | Semantic Search | Retrieval over corpora (objection library, win/loss notes, verified-contact list) |

---

## 5. Value Levers (adapted for growth) — *why* a capability matters

Closed set. Every activity, automation, and metric must map to ≥1 lever (so effort ties to value, not vanity).

| Code | Lever | Definition | Primary metrics it moves |
|------|-------|------------|--------------------------|
| `PIPELINE_CREATION` | Pipeline Creation | Net-new qualified pipeline generated for Iksula | Pipeline sourced ($/#), SQL count, meetings held, coverage ratio |
| `SPEED_TO_LEAD` | Speed-to-Lead | Latency from intent signal → first human/agent touch | First-touch p50/p95, STL-SLA adherence, no-show recovery |
| `CPQL` | Cost-per-Qualified-Lead | Efficiency of producing an MQL/SQL incl. tool credits | Cost-per-MQL, cost-per-SQL, cost-per-meeting, CAC, waterfall credit-efficiency |
| `CONVERSION_LIFT` | Conversion-Rate Lift | Improving stage-to-stage conversion (MQL→SAL→SQL→Opp) | MQL→SAL acceptance, SAL→SQL, SQL→Opp, A/B test lift, scoring model-lift |
| `BRAND_RISK` | Brand / Risk | Protecting domain reputation, compliance posture, brand trust | Spam-complaint rate, bounce, deliverability/inbox-placement, LinkedIn account health, DPDP/GDPR/CAN-SPAM consent coverage, blocklist incidents |

---

## 6. Buyer Roles (the buying committee — the North Star vocabulary)

Closed set. Every contact in a target account is tagged with **exactly one primary role**; the role drives roll-up weight (§A.6), messaging angle, and play selection. Titles per `<<PERSONA_TITLE_MAP_BY_SEGMENT>>`.

| Code | Role | What they control | Engagement implication for Iksula |
|------|------|-------------------|-----------------------------------|
| `ECONOMIC_BUYER` | Economic Buyer | Budget + final yes/no | Highest roll-up weight; their signal triggers priority bump + STL timer; ROI/business-case messaging |
| `CHAMPION` | Champion | Internal selling + access | High weight; arm with internal-sell assets; track job-change (re-thread) |
| `INFLUENCER` | Influencer | Shapes criteria/requirements | Mid weight; technical/peer-proof, analyst/benchmark content |
| `END_USER` | End-User | Operates the service day-to-day | Lower weight; usability/efficiency proof; signal of real need |
| `GATEKEEPER` | Gatekeeper / Blocker | Controls access OR resists change | Weight may be **negative**; gatekeeper-as-ally play; blocker → objection-handling flag, multi-thread around |

> **Coverage rule:** an account cannot MQL while single-threaded below `<<MIN_COMMITTEE_COVERAGE>>`. `<<REQUIRED_ROLES>>` (typically Economic Buyer + Champion) must be present and engaged.

---

## 7. Autonomy Levels (who is in the loop, per action)

Three fixed levels. Every channel, play, and automation declares its default level; HITL gates can raise (never silently lower) the level for a specific action.

| Code | Level | Meaning | Examples (default) |
|------|-------|---------|--------------------|
| `AUTONOMOUS` | Autonomous | Agent decides + executes within guardrails; human sees in digest, pinged only on breach | Verified-list enrichment/verification, fit/intent scoring, deliverability throttle/rotate, behavioral auto-email, sequence dispatch within approved campaign + volume governor, reply triage of unsubscribes |
| `APPROVE_BEFORE_ACT` | Approve-before-act | Agent prepares + recommends; human approves before execution | New campaign go-live (copy + list + volume), LinkedIn touches, paid spend, net-new target list, scoring-config change, MQL→SAL borderline, positive-reply/booking handoff, new sending-domain activation, DMARC enforcement move |
| `HUMAN_LED` | Human-led | Human performs; agent assists/logs/mines only | Live phone/discovery calls, SQL→AE final qualification, partner/co-marketing negotiation, blocklist remediation, DSR (DPDP/GDPR) handling, list-provenance approval |

---

## 8. Reusability (how shareable each artifact is across runs/agents)

Closed set, mirroring the example rubric — tags every produced artifact (schema, list, sequence template, scoring config, brief) so the agent and Content Creator know what is portable vs one-off.

| Code | Tier | Meaning |
|------|------|---------|
| `CORE_REUSABLE` | Core / Reusable | Stable cross-run asset reused by default (canonical brief schema, scoring-config object, verified-list pipeline, suppression engine, controlled vocabularies themselves) |
| `TEMPLATE_PARAMETERIZED` | Template / Parameterized | Reusable skeleton with per-segment/solution placeholders (cadence templates, message blocks, persona maps, ICP rule-sets) |
| `SEGMENT_SPECIFIC` | Segment-Specific | Reused only within a vertical/persona/solution cell (segment audiences, vertical battlecards, tier-1 1:1 research) |
| `RUN_SPECIFIC` | Run / One-off | Single-campaign artifact, not reused (a specific A/B test cell, a one-time event list, a dated offer) |

---

## 9. Cross-vocabulary binding (how these interlock — quick reference)

```
Channel  --has default-->  Autonomy Level
Activity --maps to-->      ≥1 Value Lever  AND  ≥1 Automation Archetype
Contact  --tagged-->       exactly 1 Buyer Role  --> roll-up weight in Buying-Group Score
Record   --carries-->      exactly 1 Lifecycle Stage  AND  exactly 1 Lead Status
Artifact --tagged-->       exactly 1 Reusability tier
Reason   --drawn from-->   closed DQ/Recycle reason-code set
```

> All eight vocabularies are **versioned together** as the mandate's controlled-term registry. Adding/renaming a term is a HITL-approved governance change — never an inline free-text string in CRM, queue, or event payload.
