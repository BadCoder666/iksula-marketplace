# Distribution Playbook — Growth Hacker

*Authoritative execution detail for the organic/online, 1-to-many channel. The `SKILL.md` holds the runnable workflow; this is the channel-by-channel catalog, the native-reshaping rules, posting windows, social listening, employee advocacy, and the raw-performance schema. Mined from the deep Growth Hacker mandate §6 — DISTRIBUTION/PUBLISHING/COMMUNITY scope only. Everything outreach-, qualification-, de-anon-, CRM- or nurture-shaped in that mandate belongs to Lead Gen and is deliberately omitted here.*

**Version:** 1.0 · **Owner:** DJ / Iksula Demand Gen · **Scope:** Online/organic publish + distribute + community + capture. Not Events / Inside Sales / Reference (Lead Gen).

---

## 0. The one rule that governs this whole file

GH **executes the approved plan and reshapes for native form** — it does not plan channels, set budget, set cadence, create content, re-argue a thesis, qualify a lead, or do 1-to-1 outreach. Everything below is *how to ship and capture what the Spine handed you*, never *what to ship or whom to chase*.

Brand-facing posting windows, cadence, audience cuts, retargeting budgets and channel mix are **placeholders the plan sets** — referenced here as `<<POSTING_WINDOWS>>`, `<<POSTING_CADENCE>>`, `<<RETARGETING_BUDGET_CAPS>>`. GH reads them from the media plan + `channel-intel`; it never hardcodes them.

---

## 1. Native publishing — the spine of the job

For each calendar row: finalise timing per channel/timezone, honour dependencies, **reshape to native form**, instrument, publish, advance `status`, log.

| Surface | Native form GH reshapes to | Publish-as | Window / cadence | Instrument | Do NOT |
|---|---|---|---|---|---|
| **LinkedIn company page** | single image / document (carousel) / text+link; hook in first 1–2 lines (survive the "see more" cut) | company | `<<POSTING_WINDOWS>>` (e.g. business-day 8–10am local); ~1 page post/business-day | UTM + tracked CTA; pull official Member Post Analytics | re-write the thesis; ship missing CTA/tracked link |
| **LinkedIn profile (byline leader)** | first-person POV post / short thread; reshaped from the same asset | the named leader (voice-gated, §5) | per persona, `<<POSTING_CADENCE>>` | UTM + tracked CTA | invent the voice; post as a leader without human approval |
| **X / Threads** | thread vs single; tighten to platform length; lead with the hook | company or byline | per `<<POSTING_WINDOWS>>` | per-post tracked link | bulk-template; generic filler |
| **Blog / owned site** | full edition + on-page CTA / form | company | per calendar slot | UTM on every outbound CTA; form instrumented for capture | alter claims |
| **YouTube / short-video** | reshape storyline beats to aspect ratio + length; title = 5-second hook | company or byline | per calendar slot | tracked description links; capture views/saves | re-script the argument |
| **Newsletter / owned email (broadcast)** | issue layout; subject = hook | company | per calendar | one-click List-Unsubscribe; capture opens/CTOR | treat as 1-to-1; **first-send of any NEW sequence is human-gated** |

**Reshape, never rewrite (hard line).** GH may change length, aspect ratio, thread-vs-carousel, hook placement, and platform formatting. GH may **not** change the claim, the proof, the thesis, the funnel intent, the target audience, or the message — those are the Content Creator's and the plan's. If an asset can't go native without changing its argument → **flag to the Spine**, don't fix it yourself.

**Status discipline.** Advance one row at a time: Planned → Scheduled → Published. Write each transition (channel, timestamp, deviation) to the **execution-log** Spine record. A deviation is surfaced, never silently absorbed.

---

## 2. Paid distribution + retargeting (plan-bounded, budget-gated)

- Run paid distribution **exactly as the media plan specifies** — GH does not set the budget, the channels, or the split.
- **GATE:** paid go-live **inherits the Media Planner's budget approval**. The Spine confirms approval is in place **before any spend**. No separate organic gate.
- Retargeting / audience sync runs within `<<RETARGETING_BUDGET_CAPS>>` from the plan. GH pushes audiences and runs the buy; it does not de-anonymize, build person-level audiences, or suppress by account status (Lead Gen owns CRM state). Suppression of obvious non-targets follows the plan's instruction, not GH judgement on account status.

---

## 3. Posting windows, cadence & whitespace

- **Windows + cadence come from the plan + `channel-intel`** (what each platform rewards this quarter) — placeholders `<<POSTING_WINDOWS>>` / `<<POSTING_CADENCE>>`. Finalise the *exact* timing per channel/timezone; GH owns the clock, not the calendar.
- Use `competitor-radar` for **timing whitespace** — post into gaps rivals leave, avoid saturated windows. This is timing only; GH does not pick topics or channels.
- Randomise/jitter automated actions to stay native and within platform norms; respect per-platform action norms. GH protects the accounts that carry distribution (auto-throttle on anomaly), and **flags** any channel anomaly to the Spine.

---

## 4. Social listening (surface, route — never qualify)

Always-on listening across the online surfaces to **surface content-sourced interest**, not to qualify it.

- Monitor replies, comments, mentions, DMs on 1-to-many posts, hashtag/keyword/pain threads, and engagement on owned content.
- Classify only enough to detect an **interest event** (the seam's `signal_type`): comment, reply, dm, form_fill, content_download, cta_click, connection_accept, mention.
- For each interest event → emit **one** `content-sourced-lead` Spine record (see `seam-contract.md`). **Raw + verbatim + unscored.**
- Distinguish buyer-interest from noise/troll/competitor only to avoid junk events — **never to grade or score**. GH does not promote, qualify, or route by account status.
- GH does **not** scrape published posts on Lead Gen's behalf and does **not** re-detect interest Lead Gen already consumed. One emit per event; idempotent on `correlation_id`.

---

## 5. Community engagement (VOICE-GOVERNED)

Replies, proactive comments, monitoring — native to each platform, **1-to-many community**, never 1-to-1 outreach.

- Any reply/comment posted **as a named byline leader** is **drafted against that leader's persona in the Brain `voices` module**. A human **owns and approves** that voice before it posts (**GATE**). The skill **drafts, never invents** the voice.
- Company-account replies follow the company voice; same draft-then-human-approve discipline for sensitive/branded threads.
- No generic "Great insights!" bot-tells; ground every reply in the actual thread; keep it value-first and brand-safe; no public competitor disparagement (battlecard/competitive call-outs are gated and not GH's to author).
- A **personalised DM to an identified prospect is NOT GH** — that is Lead Gen's 1-to-1 motion. A reply on a public post is GH. Keep the line hard.

---

## 6. Employee advocacy

- On a high-value publish, offer **pre-approved reshare variants** to opted-in employees; extend the solution POV into staff networks adjacent to buyers.
- **Opt-in only.** No auto-posting from a staff account without consent; no identical-copy mass reshare (looks like a bot, and platforms penalise it).
- Capture reshare lift + participation into the raw-performance feed as aggregate engagement.

---

## 7. Raw-performance capture (the feedback return)

**Instrument before publish; capture is the job.** Aggregate engagement by **asset × format × channel × time** and return it.

Brain feed `performance-analytics-growth-YYMMDD` (append, namespaced) — fixed schema, **AGGREGATE only, never per-prospect PII**:

```
period | source | asset_or_campaign | channel | metric | value | audience_type | notes
```

- **Metrics GH owns (engagement/distribution):** impressions, reach, reactions, comments, shares, saves, clicks, views, watch-time, opens/CTOR for owned email it broadcasts, reshare lift, experiment lift.
- **`audience_type`** = new vs retargeting — **always stamped**, so performance is read honestly (control for audience type before reading email/engagement performance; CTOR over CTR for owned email).
- **`source`** namespaces shared feeds (one writer per namespace).
- **GH does NOT report funnel conversion** (MQL→SQL→meeting) — that is Lead Gen's `performance-analytics-leadgen-YYMMDD`. Don't double-write; don't cross the namespace.
- **Raw-first:** dump raw exports to `_brain/_raw/` before synthesising; never publish a number not traceable to raw + source.
- Aggregate **counts** of content-sourced leads (how many, by channel) flow here as numbers — **never the lead rows themselves** (those are Spine seam records, see `seam-contract.md`).

`channel-intel-growth-YYMMDD` (append, namespaced) — the synthesis: **what each distribution channel rewarded this cycle** + experiment winners (from `experiment-design.md`). Raw-first; traceable.

---

## 8. What lives in the deep mandate but is NOT GH (omitted on purpose)

These appear in the deep Growth Hacker mandate §6 but were reassigned in the split — they are **Lead Gen's**, not GH's, and must not leak into this playbook or the skill:

- Visitor de-anonymization (reverse-IP / RB2B / Warmly / Dealfront), person/account enrichment, CRM de-dupe, identity resolution.
- 1-to-1 outreach: cold email sequences, personalised LinkedIn DMs/InMail, connection-request outreach to identified prospects, phone/SDR dialing.
- Lead qualification, fit/intent scoring, MQL→SQL, lead grading, buying-group scoring.
- Nurture / drip / lifecycle sequences; ABM orchestration; account-status routing (new → Sales/NCA; ECS → KAM).
- The other three channels (Events, Inside Sales, Reference).
- Couriering inputs to the Content Creator (that is the Spine's orchestration).
- Owning analytics / the performance register / channel-ROI trends (the Brain owns analytics; GH feeds raw up).

If a request lands in any of these, GH **declines and routes it** (to Lead Gen, the Media Planner, the Content Creator, or the Spine as appropriate) — it does not silently absorb the scope.
