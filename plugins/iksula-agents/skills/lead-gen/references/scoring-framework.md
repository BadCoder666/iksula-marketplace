# Lead Qualification & Scoring Framework — Iksula Lead Gen Agent

*Adapted for the `lead-gen` skill from Iksula's deep lead-gen design. Qualification (MQL→SQL) is **Lead Gen's**; the Growth Hacker only surfaces interest and never scores.*

> **Status:** Review-ready spec. All thresholds, weights, bands, and ICP specifics are **founder-supplied placeholders** written as `<<PLACEHOLDER_NAME>>`. The agent ships the *machinery*; the founder (with Vishal) injects the *values*. The agent **never hardcodes a guessed value** in place of a placeholder — doing so contaminates every downstream brief, sequence, and score (see Failure Mode FM-1).
>
> **North-star binding:** Qualification exists to surface **buyers**, not records. Every score rolls up from contact → **buying group** → account. A lone champion's clicks must not manufacture an MQL while the economic buyer is dark. This framework is **buying-group-native** (Forrester 2021 B2B Revenue/Demand Waterfall), not contact-isolated.

---

## 0. Design principles (non-negotiable)

1. **Two axes, one gate.** Fit (who they are) and Intent/Engagement (what they're doing) are scored **separately** and gate **jointly**. Single-axis scoring is the #1 cause of MQL bloat (KB FM: *"engagement weighted over fit floods sales with low-fit leads"*). Never collapse them into one number for the MQL decision.
2. **Account-first, committee-aware.** Contacts inherit account-level fit. A contact-level score is meaningless until rolled into a **Buying-Group Score (BGS)** for the account (see §6). 87% of MQLs fail to convert largely because they're scored as isolated individuals.
3. **Lifecycle stage ≠ Lead status.** Stage = where in the funnel (Subscriber → … → Opportunity). Status = the operational disposition within a stage (New, Working, Recycled, Disqualified). Two fields, never conflated (RevOps best practice).
4. **Solution → buyer derivation drives the weights.** When the **Solutions Catalog input loop** changes (a service line added/retired), the ICP, persona map, intent topics, and trigger weights **re-derive** — the placeholders are *per-solution*, not global. See §8.
5. **Score must be explainable.** Every grade/score carries a **"why" breakdown** (contributing signals + points). A black-box score reps distrust is a dead score (KB FM: *score opacity*).
6. **Privacy-proxy hardening.** Apple MPP auto-fires opens; opens are **de-weighted to near-zero** for intent. Bot/security-scanner clicks are filtered before scoring. India DPDP 2025: tracked B2B work-emails are in scope — scoring/tracking requires a lawful basis (see Compliance gate).

---

## 1. Lifecycle stage spine (entry/exit instrumented)

Canonical spine (SiriusDecisions/Forrester-aligned), each transition with an explicit entry trigger, exit criterion, owner, and SLA:

| # | Stage | Definition (Iksula context) | Entry trigger | Exit / promotion criterion | Owner | SLA placeholder |
|---|-------|------------------------------|---------------|----------------------------|-------|-----------------|
| 0 | **Subscriber** | Known person, opted into a list/blog/webinar; not yet shown buying interest | Form-fill on non-gated asset; newsletter opt-in | Engages with a scored asset → Lead | Agent (auto) | n/a |
| 1 | **Lead** | Engaged contact attached to a (possibly thin) account; fit not yet graded | First scored engagement OR sourced into verified list & enriched | Fit grade computed AND in-ICP → continue scoring | Agent (auto) | `<<LEAD_ENRICH_SLA>>` |
| 2 | **MQL** | Buying-group passes **both** Fit-grade gate AND Engagement-score gate | BGS crosses `<<MQL_FIT_FLOOR>>` **and** `<<MQL_ENGAGEMENT_FLOOR>>` jointly | Inside sales accepts → SAL | Agent → HITL gate | `<<MQL_REVIEW_SLA>>` |
| 3 | **SAL** (Sales-Accepted Lead) | Inside sales (SDR/BDR) has **accepted** the MQL as worth working | SDR acceptance within SLA | Reached + SDR-level qual (Need/Authority-influence/Timeline) passes → SQL | Inside sales (HITL) | `<<SAL_ACCEPT_SLA>>` |
| 4 | **SQL** (Sales-Qualified Lead) | SDR-qualified, meeting booked/held, evidence-backed pain confirmed | SDR qual gate passed; meeting held | AE accepts + opportunity created | Inside sales → AE (HITL) | `<<SQL_HANDOFF_SLA>>` |
| 5 | **Opportunity** | AE-accepted; MEDDIC/MEDDPICC deepening begins | AE acceptance, opp record created | Closed-Won / Closed-Lost | AE / managed sales | n/a |
| — | **Customer** | (Out of Lead Gen scope — Sales owns the close; a suppression source) | Closed-Won | — | — | — |

**Recycle/Nurture loop:** any record that is right-fit-but-not-now exits to **Recycled** status (not Disqualified), re-enters nurture, and can re-MQL when engagement re-fires (track Recycle→re-MQL rate). **Hard-Disqualify** exits the lifecycle entirely with a reason code.

---

## 2. Fit grade (the WHO axis) — A/B/C/D

Fit is computed at the **account** level (firmographic + technographic) plus a **contact-level role/demographic** modifier, then graded.

### 2.1 Sub-score composition

```
FIT_SCORE(account) =
      <<W_FIRMO>>     * Firmographic_subscore      // industry/sub-vertical, size, GMV/revenue band, geo, business-model (brand|marketplace|distributor|retailer)
    + <<W_TECHNO>>    * Technographic_subscore      // ecommerce platform, marketplace presence, PIM/OMS/WMS stack signals
    + <<W_DEMO>>      * Demographic_role_subscore   // seniority/function fit of engaged contacts, buying-role coverage
    - <<W_NEG_FIT>>   * Negative_fit_penalty        // out-of-ICP vertical, sub-floor size, competitor/agency pattern

constraint: <<W_FIRMO>> + <<W_TECHNO>> + <<W_DEMO>> = 1.0   (negative penalty applied after)
```

### 2.2 Grade bands (placeholder ranges → letter)

| Grade | Score range | Meaning | Routing implication |
|-------|-------------|---------|---------------------|
| **A** | `<<FIT_A_MIN>>`–100 | Core ICP, multi-signal fit | Eligible for 1:1 / high-touch; lowest engagement floor to MQL |
| **B** | `<<FIT_B_MIN>>`–`<<FIT_A_MIN>>` | Strong fit, minor gaps | 1:few; standard engagement floor |
| **C** | `<<FIT_C_MIN>>`–`<<FIT_B_MIN>>` | Marginal fit | 1:many nurture only; high engagement floor required |
| **D** | 0–`<<FIT_C_MIN>>` | Out-of-ICP / poor fit | **No MQL regardless of engagement**; nurture or suppress |

> **Gate rule:** A grade **D never becomes an MQL**, no matter how hot the engagement — this is the structural defense against MQL inflation. Fit is the master gate.

---

## 3. Intent/Engagement score (the WHAT-THEY-DO axis)

Continuous, **time-decayed**, additive score from first-party behavior + third-party intent, computed **per contact** then **rolled up to the buying group** (§6).

### 3.1 Signal weight table (founder fills point values)

| Signal class | Example signals | Point variable |
|--------------|-----------------|----------------|
| **High-intent first-party** | Pricing-page view, services/solution-page view, demo/contact request, ROI-calculator completion | `<<PTS_PRICING_VIEW>>`, `<<PTS_DEMO_REQUEST>>`, `<<PTS_SERVICES_PAGE>>` |
| **Mid-intent first-party** | Gated-asset download, webinar attend, case-study view, multi-page session, reply to outbound | `<<PTS_GATED_DOWNLOAD>>`, `<<PTS_WEBINAR_ATTEND>>`, `<<PTS_POSITIVE_REPLY>>` |
| **Low-intent first-party** | Email click, LinkedIn post engagement, blog view | `<<PTS_EMAIL_CLICK>>`, `<<PTS_SOCIAL_ENGAGE>>` |
| **De-weighted / proxy** | Email **open** (MPP-inflated) | `<<PTS_EMAIL_OPEN>>` (default ≈ 0; never primary) |
| **Third-party intent** | Bombora Company Surge / 6sense / G2 buyer-intent on `<<INTENT_TOPIC_LIST>>` (e.g., "marketplace management", "catalog ops", "q-commerce", "returns management") | `<<PTS_INTENT_SURGE>>` (account-level) |
| **Trigger events** | Funding, leadership hire (Head of Ecommerce/CX), marketplace launch, replatform, hiring surge | `<<PTS_TRIGGER_<EVENT>>>` |

### 3.2 Time-decay (kills zombie MQLs)

```
DECAYED_PTS(signal, t) = raw_pts * (1 - <<DECAY_RATE>>) ^ floor( idle_days / <<DECAY_PERIOD>> )
   where decay begins only after <<DECAY_IDLE_GRACE>> days of inactivity
```

> **FM defense:** If decay is never configured, leads accumulate points forever and sit above MQL threshold long after going cold. Decay is **mandatory**, and "decay-firing rate" is a monitored metric.

---

## 4. Negative scoring & disqualification

Two tiers: **soft-negative** (subtract points, may still recover) and **hard-disqualify** (exit lifecycle, reason-coded). Negative scoring must be **conservative** — an over-aggressive web silently suppresses genuine buyers (KB FM: *negative-scoring overreach killing legitimate SMB founders*).

### 4.1 Soft-negative (point subtraction)

| Signal | Point variable |
|--------|----------------|
| Email hard-bounce | `<<NEG_BOUNCE>>` |
| Marked-spam / complaint | `<<NEG_SPAM>>` |
| Sustained inactivity past `<<INACTIVITY_N_DAYS>>` | `<<NEG_INACTIVITY>>` |
| Low-intent role/title (intern, junior, irrelevant function) | `<<NEG_LOW_ROLE>>` |
| Free-email domain on a B2B form | `<<NEG_FREE_DOMAIN>>` |
| Repeated form abandons / careers-page-only visits | `<<NEG_CAREERS_ONLY>>` |

### 4.2 Hard-disqualify rules (exit lifecycle) — reason-coded

| Rule | Variable | Reason code |
|------|----------|-------------|
| Out-of-ICP geography | `<<DQ_GEO_LIST>>` | `DQ_GEO` |
| Competitor / agency / job-seeker | `<<DQ_COMPETITOR_DOMAINS>>` | `DQ_COMPETITOR` |
| Below size/GMV floor | `<<DQ_SIZE_FLOOR>>` | `DQ_SUBSCALE` |
| Do-not-contact / opt-out / suppression | `<<DNC_SOURCE>>` | `DQ_DNC` |
| Existing customer / active open opp (channel-conflict) | `<<SUPPRESSION_CUSTOMER_SRC>>` | `DQ_CUSTOMER` |
| Unverifiable email (catch-all at-risk past policy) | `<<CATCHALL_POLICY>>` | `DQ_UNVERIFIED` |

**Reason-code vocabulary** is closed and shared with sales (so rejected leads correct the ICP/scoring model rather than dying silently — KB FM: *"no SAL-acceptance SLA, leads die with no reason code"*). HITL **weekly review of the hard-DQ batch** catches false-positives before good-fit leads are permanently burned.

---

## 5. The two-axis MQL gate (scoring-formula block)

```
# ---- AXIS 1: FIT (account-level, graded A/B/C/D) ----
FIT_GRADE = grade( FIT_SCORE(account), bands = {A:<<FIT_A_MIN>>, B:<<FIT_B_MIN>>, C:<<FIT_C_MIN>>} )

# ---- AXIS 2: ENGAGEMENT (rolled up to buying group) ----
ENGAGEMENT_SCORE(account) = BGS_ENGAGEMENT(account)            # see §6 roll-up
                          + <<PTS_INTENT_SURGE>> * intent_active(account)   # account-level intent
                          - soft_negative_total(account)

# ---- JOINT MQL GATE (BOTH must pass; fit is master) ----
IS_MQL(account) =
        FIT_GRADE in {A, B, C}                                 # D is excluded outright
    AND FIT_GRADE >= <<MQL_FIT_FLOOR>>                          # e.g. floor = B
    AND ENGAGEMENT_SCORE(account) >= engagement_floor(FIT_GRADE)
        where engagement_floor = {
            A: <<MQL_ENG_FLOOR_A>>,   # lower floor for best-fit
            B: <<MQL_ENG_FLOOR_B>>,
            C: <<MQL_ENG_FLOOR_C>>    # highest floor; marginal fit must work harder
        }
    AND NOT hard_disqualified(account)
    AND buying_group_coverage(account) >= <<MIN_COMMITTEE_COVERAGE>>   # §6: don't MQL a single-threaded account

# ---- SQL gate (deeper, evidence-backed; SDR + AE) ----
IS_SQL = SAL_accepted
     AND meeting_held
     AND qual_slots_filled( framework = <<SQL_FRAMEWORK>> ,   # BANT / CHAMP / MEDDIC-light
                            required = <<SQL_REQUIRED_SLOTS>> )
     AND evidence_backed( slots )            # cited snippets from transcript/email, not guesses
```

> **Anti-bloat invariant:** lowering an engagement floor without raising the fit floor is forbidden by policy; any threshold change is a **versioned, HITL-approved scoring-config change** (agent proposes, human approves).

---

## 6. Buying-group scoring (the North Star, made operational)

Iksula sells **managed services** into a committee. Score the **group**, not the loudest clicker.

### 6.1 Roll-up model

```
For each target account, instantiate a Buying-Group with role slots:
    [Economic Buyer, Champion, Influencer, End-User, Gatekeeper/Blocker]
    (titles per <<PERSONA_TITLE_MAP_BY_SEGMENT>>)

BGS_ENGAGEMENT(account) = Σ over contacts c in account:
        role_weight(role(c)) * contact_engagement(c)

role_weight = {
    Economic Buyer:     <<RW_ECONOMIC_BUYER>>,    # highest — their engagement is the prize
    Champion:           <<RW_CHAMPION>>,
    Influencer:         <<RW_INFLUENCER>>,
    End-User:           <<RW_END_USER>>,
    Gatekeeper/Blocker: <<RW_GATEKEEPER>>          # may be negative if actively blocking
}

buying_group_coverage(account) =
    (# distinct buying-roles with ≥1 engaged, verified contact) / (# roles required by <<REQUIRED_ROLES>>)
```

### 6.2 Committee-aware rules

- **Single-thread alarm:** if only one role is engaged (typically a Champion or End-User) the account is flagged **single-threaded** and is **capped below MQL** until coverage ≥ `<<MIN_COMMITTEE_COVERAGE>>`, OR routed to a multi-threading play to engage the Economic Buyer. This directly defeats the "champion's clicks promote a lead while the economic buyer is never engaged" failure mode.
- **Economic-buyer signal premium:** any high-intent signal from the Economic-Buyer role triggers an immediate priority bump and speed-to-lead timer, regardless of total score.
- **Blocker detection:** a Gatekeeper/Blocker's negative signals (e.g., "we handle this in-house") subtract from BGS and raise an objection-handling flag.
- **Job-change re-thread:** when UserGems/Champify detects a Champion left, suppress the stale record, re-prospect the vacated seat, and spin a warm lead at the Champion's new account (decay/hygiene loop).

---

## 7. Tiering scheme (priority for finite SDR/agent capacity)

Composite priority drives the **"work-now" queue**. Tiering blends fit, intent, buying-group coverage, and reachability (verified contactability).

```
PRIORITY(account) =
      <<TW_FIT>>          * normalized(FIT_SCORE)
    + <<TW_INTENT>>       * normalized(ENGAGEMENT_SCORE)
    + <<TW_COVERAGE>>     * buying_group_coverage
    + <<TW_REACHABILITY>> * verified_contactability     # % of committee with deliverable email/valid phone
    + <<TW_TRIGGER>>      * active_trigger_boost
```

| Tier | Condition | Treatment (ABM-style) | Speed-to-lead SLA |
|------|-----------|------------------------|-------------------|
| **P1 / 1:1** | A-fit + active intent + EB engaged | Human-led 1:1, personalized video, AE-shadowed | `<<STL_SLA_P1>>` (hot inbound target ≈ 5 min) |
| **P2 / 1:few** | A/B-fit + mid intent OR strong coverage | Semi-automated multichannel cadence + light personalization | `<<STL_SLA_P2>>` |
| **P3 / 1:many** | B/C-fit, low intent | Scaled automated nurture sequence | `<<STL_SLA_P3>>` |
| **Hold/Recycle** | Right-fit, not-now | Long-cycle nurture; re-score on signal | n/a |

---

## 8. Lead-to-account routing & speed-to-lead SLA

**Order of operations matters** — match to account *before* round-robin, or a strategic-account lead gets dealt to a random rep and fragments the buying-group view (KB FM).

```
1. LEAD-TO-ACCOUNT MATCH (first, always):
     exact-key on email-domain → fuzzy on company-name + normalized-domain
     if matches an OWNED / named / open-opp account → route to ACCOUNT OWNER (never round-robin)
     else → net-new → step 2

2. ROUTING (net-new):
     split by <<ROUTING_DIMENSIONS>>  (territory | segment | vertical | language | India-domestic vs export)
     within pool → weighted round-robin with per-rep active-cap <<REP_ACTIVE_CAP>>

3. START SPEED-TO-LEAD TIMER:
     timer = STL_SLA(tier)
     package qualification context (BGS breakdown, why-targeted, signals, verified contacts)
     instant-book path (Chili Piper / RevenueHero) on high-intent form-fill / identified visitor

4. SLA BREACH:
     if first-touch not logged within STL_SLA(tier) → auto-reassign to backup pool + alert
     (research: ~9x qualify-rate drop-off when hot inbound isn't touched in ~5 min)
```

**Routing/SLA placeholders:** `<<ROUTING_DIMENSIONS>>`, `<<REP_ACTIVE_CAP>>`, `<<STL_SLA_P1..P3>>`, `<<SAL_ACCEPT_SLA>>`, `<<AUTO_REASSIGN_TIMER>>`, `<<ROUND_ROBIN_WEIGHTS>>`.

---

## 9. Solution → buyer derivation (the Catalog input loop binds to scoring)

When the **Solutions Catalog** updates, the agent **re-derives** the placeholder *values* per solution (the founder ratifies):

| Per-solution derived artifact | Feeds which scoring variable |
|-------------------------------|------------------------------|
| Derived ICP firmographics for solution *S* | `<<ICP_FIRMOGRAPHICS>>` → Firmographic_subscore weights |
| Derived buyer personas / committee for *S* | `<<PERSONA_TITLE_MAP_BY_SEGMENT>>` → role slots & `role_weight` |
| Derived trigger signals for *S* | `<<PTS_TRIGGER_*>>` |
| Derived intent topics for *S* | `<<INTENT_TOPIC_LIST>>` → `<<PTS_INTENT_SURGE>>` |
| Derived messaging angle for *S* | hands to Content Creator brief (not a scoring var, but binds the channel cell) |

> **Invariant:** targeting and scoring **re-derive** on catalog change; stale solution→buyer maps are quarantined (parallels the content freshness/decay SLA).

---

## 10. Calibration & governance (keep the model honest)

- **Back-test:** correlate score bands against closed-won/closed-lost. Validate **model lift** (high scores actually predict conversion), not activity. Metric: *win-rate by lead-score band*.
- **Acceptance drift:** if MQL→SAL acceptance drops below `<<MQL_ACCEPT_FLOOR>>` or SAL→SQL below `<<SQL_CONV_FLOOR>>`, trigger a **recalibration cycle** (agent proposes new weights with before/after evidence; HITL approves).
- **Config versioning:** every weight/threshold/band/decay/disqualifier change is **versioned** and HITL-approved. No silent tuning.
- **Score explainability audit:** spot-check that every MQL carries a readable "why" (top contributing signals + points + buying-group coverage).

---

## 11. HITL gates specific to qualification

| Gate | What the human decides |
|------|------------------------|
| **MQL→SAL handoff** | Confirm borderline / strategic-account MQLs before they consume sales capacity (the core gate) |
| **Scoring-config change** | Approve any weight/threshold/band/decay/disqualifier change (versioned) |
| **Hard-DQ batch review** | Weekly — catch false-positives before good-fit leads are permanently burned |
| **SQL promotion** | Rep/manager confirms MEDDIC/BANT slots are evidence-backed, not guessed |
| **Recalibration** | Approve re-weighting after back-test / acceptance drift |
| **Routing & SLA change** | Approve territory/round-robin/SLA edits |
| **Compliance** | Confirm consent basis & opt-out honoring meet DPDP/GDPR/CAN-SPAM before scoring/tracking personal work data |

---

## 12. Metrics (the qualification rate-card)

Fit-grade distribution (watch A/B/C/D inflation) · Engagement distribution + **decay-firing rate** · MQL volume + **MQL→SAL acceptance rate** · SAL→SQL, SQL→Opp conversion vs waterfall benchmark · Stage velocity (days-in-stage) + lead→opp cycle time · **Speed-to-lead p50/p95 vs SLA** · Routing assignment success (≥99.5%) + time-to-assignment · Hot-MQL queue aging (goal zero >24h) + SLA-breach/auto-reassign rate · Disqualification rate + reason-code breakdown · **Buying-group coverage per account** + single-threaded-account rate · **Scoring model lift** (closed-won rate, high vs low band) · Recycle→re-MQL rate.

---

## 13. Placeholder register (variable | meaning | example)

| Variable | Meaning | Example value (illustrative — founder confirms) |
|----------|---------|--------------------------------------------------|
| `<<ICP_FIRMOGRAPHICS>>` | Target industries/sub-verticals, size, GMV/revenue band, geo, business-model | D2C brands + marketplaces; ₹50Cr–₹500Cr GMV; India + GCC; brand/marketplace/distributor/retailer |
| `<<PERSONA_TITLE_MAP_BY_SEGMENT>>` | Buying-role → titles per segment | EB = VP/Head Ecommerce; Champion = Ecommerce Manager; Influencer = CX Lead; End-User = Catalog Ops; Blocker = Procurement |
| `<<INTENT_TOPIC_LIST>>` | Bombora/6sense/G2 topics that map to Iksula intent | "marketplace management", "catalog management", "returns management", "q-commerce", "D2C ops" |
| `<<W_FIRMO>>` / `<<W_TECHNO>>` / `<<W_DEMO>>` | Fit sub-score weights (sum 1.0) | 0.5 / 0.3 / 0.2 |
| `<<W_NEG_FIT>>` | Negative-fit penalty weight | 0.25 |
| `<<FIT_A_MIN>>` / `<<FIT_B_MIN>>` / `<<FIT_C_MIN>>` | Grade-band score floors | 80 / 60 / 40 |
| `<<MQL_FIT_FLOOR>>` | Minimum fit grade to MQL | B |
| `<<MQL_ENG_FLOOR_A/B/C>>` | Per-grade engagement floor to MQL | 30 / 45 / 70 |
| `<<PTS_PRICING_VIEW>>` | Points: pricing-page view | +25 |
| `<<PTS_DEMO_REQUEST>>` | Points: demo/contact request | +40 |
| `<<PTS_SERVICES_PAGE>>` | Points: solution/services-page view | +15 |
| `<<PTS_GATED_DOWNLOAD>>` | Points: gated-asset download | +10 |
| `<<PTS_WEBINAR_ATTEND>>` | Points: webinar attendance | +12 |
| `<<PTS_POSITIVE_REPLY>>` | Points: positive reply to outbound | +20 |
| `<<PTS_EMAIL_CLICK>>` | Points: email click | +3 |
| `<<PTS_SOCIAL_ENGAGE>>` | Points: LinkedIn post engagement | +4 |
| `<<PTS_EMAIL_OPEN>>` | Points: email open (MPP-de-weighted) | 0 (or +1 max) |
| `<<PTS_INTENT_SURGE>>` | Points: third-party intent surge (account) | +20 |
| `<<PTS_TRIGGER_*>>` | Points per trigger event | funding +15; new Head-of-Ecomm hire +20; replatform +18 |
| `<<DECAY_RATE>>` | Per-period decay % | 0.15 |
| `<<DECAY_PERIOD>>` | Decay period length (days) | 14 |
| `<<DECAY_IDLE_GRACE>>` | Idle days before decay starts | 7 |
| `<<INACTIVITY_N_DAYS>>` | Inactivity window for soft-negative | 60 |
| `<<NEG_BOUNCE>>` / `<<NEG_SPAM>>` / `<<NEG_INACTIVITY>>` / `<<NEG_LOW_ROLE>>` / `<<NEG_FREE_DOMAIN>>` / `<<NEG_CAREERS_ONLY>>` | Soft-negative point subtractions | -15 / -25 / -10 / -8 / -5 / -5 |
| `<<DQ_GEO_LIST>>` | Hard-DQ geographies | (out-of-scope regions) |
| `<<DQ_COMPETITOR_DOMAINS>>` | Competitor/agency/job-seeker blocklist | (named rival agencies) |
| `<<DQ_SIZE_FLOOR>>` | Minimum size/GMV to qualify | < ₹10Cr GMV → DQ |
| `<<DNC_SOURCE>>` | Do-not-contact source of truth | global suppression list ID |
| `<<SUPPRESSION_CUSTOMER_SRC>>` | Existing-customer / open-opp suppression | CRM customer + open-opp lists |
| `<<CATCHALL_POLICY>>` | Catch-all risk-acceptance policy | exclude from primary pool; micro-test only |
| `<<RW_ECONOMIC_BUYER>>` … `<<RW_GATEKEEPER>>` | Buying-role roll-up weights | EB 1.0 / Champion 0.8 / Influencer 0.5 / End-User 0.3 / Blocker -0.4 |
| `<<REQUIRED_ROLES>>` / `<<MIN_COMMITTEE_COVERAGE>>` | Roles needed + min coverage for MQL | {EB, Champion} required; coverage ≥ 0.5 |
| `<<TW_FIT>>` / `<<TW_INTENT>>` / `<<TW_COVERAGE>>` / `<<TW_REACHABILITY>>` / `<<TW_TRIGGER>>` | Priority/tiering weights | 0.3 / 0.3 / 0.2 / 0.1 / 0.1 |
| `<<SQL_FRAMEWORK>>` / `<<SQL_REQUIRED_SLOTS>>` | SQL qual framework + mandatory slots | CHAMP; {Challenge, Authority-influence, Timeline} |
| `<<ROUTING_DIMENSIONS>>` / `<<ROUND_ROBIN_WEIGHTS>>` / `<<REP_ACTIVE_CAP>>` | Routing splits, weighting, per-rep cap | territory+segment; equal; 40 active leads/rep |
| `<<STL_SLA_P1>>` / `<<STL_SLA_P2>>` / `<<STL_SLA_P3>>` | Speed-to-lead first-touch SLA per tier | 5 min / 1 hr / 24 hr |
| `<<SAL_ACCEPT_SLA>>` / `<<SQL_HANDOFF_SLA>>` / `<<AUTO_REASSIGN_TIMER>>` | Acceptance & handoff SLAs, reassign timer | 4 hr / 24 hr / 30 min |
| `<<MQL_ACCEPT_FLOOR>>` / `<<SQL_CONV_FLOOR>>` | Drift floors that trigger recalibration | 70% / 25% |
| `<<LEAD_ENRICH_SLA>>` / `<<MQL_REVIEW_SLA>>` | Enrichment & MQL-review SLAs | 1 hr / 2 hr |

---

## 14. Failure modes this framework explicitly defends against

- **FM-1 Hardcoded placeholders** → all values are `<<...>>`; agent references, never bakes.
- **FM-2 MQL inflation** → two-axis joint gate + fit-as-master + grade-D exclusion.
- **FM-3 MPP open-inflation** → opens de-weighted to ~0; positive-reply/pricing-view are the real signals.
- **FM-4 Zombie MQLs** → mandatory time-decay + decay-firing-rate metric.
- **FM-5 Negative-scoring overreach** → conservative soft-negatives + weekly HITL hard-DQ review.
- **FM-6 Buying-group blindness** → BGS roll-up, single-thread cap, EB premium.
- **FM-7 Round-robin over account ownership** → lead-to-account match runs first.
- **FM-8 Speed-to-lead miss** → per-tier STL timer + auto-reassign on breach.
- **FM-9 Framework-as-checkbox** → SQL requires *evidence-backed* slots (cited snippets).
- **FM-10 Silent dead leads** → mandatory reason codes feed ICP/scoring correction.
- **FM-11 Score opacity** → every score carries a "why" breakdown.
- **FM-12 DPDP/GDPR exposure** → compliance gate before scoring/tracking personal work data.
