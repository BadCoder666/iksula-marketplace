# Registers & Weighting Playbook — Content Creator

*Authoritative spec for the Content Creator's two standing research registers, the B2B influence-weighting formula, quarterly recalibration, and the monthly Influence Analysis. The `SKILL.md` holds the runnable workflow (step 1 refresh, step 6 re-score + ship the analysis); this file is the schema, the math, the recalibration rules, and the Brain contract. Sibling spec: `content-build-spec.md` (the publishing-calendar schema + per-product builds) — kept consistent with this file.*

**Version:** 1.0 · **Owner:** Content Creator (writer-of-record for Brain `voices`). **Scope:** influence research only — who/what is worth atomizing-toward and amplifying-with. Not lead scoring (Lead Gen), not channel-reward intel (`channel-intel`, GH/Media-Planner), not engagement capture (`performance-analytics`, GH).

---

## 0. The one rule that governs this file

**Influence ≠ reach.** In B2B, engagement *quality* and *audience-fit* beat raw follower count and impression volume. A 4k-follower account whose comment section is the actual ICP outweighs a 400k-follower account whose audience is peers and bots. Every score here is computed by the §3 weighting formula — **never sorted on follower count, never on raw reach**. If a row's rank would change by swapping in a follower number, the row is wrong.

Founder ratifies every weight. The **formula shape is fixed**; the per-Iksula weights are `<<W_...>>` placeholders set once, ratified, and versioned — never guessed inline.

---

## 1. The two registers (what they are, who reads them)

| Register | Holds | Granularity | Primary consumers |
|---|---|---|---|
| **Top 100 Voices** | the ranked people/accounts whose audience *is* Iksula's ICP and whose engagement is high-quality | one row per voice | CC (atomization targets, hook bank, who-to-tag); seeds Brain `voices` for TL bylines + GH community engagement |
| **Top Content** | the ranked individual content products (theirs and ours) that earned high-quality B2B engagement | one row per asset | CC (format/angle evidence for the What's-Working playbook); informs `content-build-spec.md` planning |

Both are **living, undated files** in the engine's working memory (the exception in the SKILL naming rule — registers are kept current, not snapshotted). Their *distilled, no-PII* synthesis is what flows to the Brain (§5). Raw scrapes/exports go to `_brain/_raw/` first; the register cites them. **Never a score not traceable to raw + a dated source.**

---

## 2. Register schemas (fixed field names)

### 2.1 Top 100 Voices

| Field | Meaning |
|---|---|
| `voice_id` | ULID — stable row key; survives a handle change |
| `handle` | platform handle (e.g. `@name`) |
| `name` | display name |
| `platform` | LinkedIn \| X \| YouTube \| Podcast \| Blog \| Substack \| ... (closed channel set, per `content-build-spec.md`) |
| `role_persona_fit` | the ICP role this voice's audience maps to (Economic Buyer \| Champion \| Influencer \| End-User \| Analyst \| Peer-Operator) — fit to `icp-audience`, **not** topical adjacency |
| `s_audience_fit` | sub-score 0–100 — how much of their audience IS the ICP (§3) |
| `s_engagement_quality` | sub-score 0–100 — depth/substance of replies, not volume (§3) |
| `s_relevance` | sub-score 0–100 — topical overlap with Iksula's theses/solutions (§3) |
| `s_velocity` | sub-score 0–100 — consistency + recency of in-ICP activity (§3) |
| `s_credibility` | sub-score 0–100 — earned authority, verifiable (§3) |
| `s_reach` | sub-score 0–100 — audience SIZE, capped + heavily de-weighted (§3) |
| `weighted_score` | the §3 composite; the **only** ranking field |
| `byline_candidate` | true/false — flagged for TL to consider as a named-voice persona (voice still human-owned before any post) |
| `source` | where each sub-score's evidence came from (URL/export in `_brain/_raw/`) |
| `verified` | true/false — a human or deterministic check confirmed the account is real and the audience claim holds |
| `as_of` | ISO date the row was last scored (drives staleness, §4) |
| `notes` | free-text caveats (suspected bot inflation, audience drift, etc.) |

### 2.2 Top Content

| Field | Meaning |
|---|---|
| `content_id` | ULID — stable row key |
| `asset` | title + canonical URL of the individual content product |
| `author_voice` | the `voice_id` (if a tracked voice) or `"Iksula"` for our own assets |
| `channel` | the publishing channel (closed set) |
| `format` | post \| carousel \| document \| thread \| blog-edition \| short-video \| podcast-brief \| ... (mirrors `content-build-spec.md` `format`) |
| `q_save_share_ratio` | engagement-quality signal — saves+shares ÷ impressions (intent-to-keep, not vanity likes) |
| `q_substantive_replies` | quality signal — share of comments that are substantive (questions/POV) vs reactions |
| `q_icp_engager_share` | quality signal — share of engagers who match `role_persona_fit`/ICP |
| `q_dwell_completion` | quality signal — read/watch completion or document expand-rate (channel-appropriate) |
| `weighted_score` | the §3 content composite; the **only** ranking field |
| `is_ours` | true/false — partitions our assets (feeds the What's-Working playbook) from external exemplars (feeds the hook/idea bank) |
| `source` | raw export reference in `_brain/_raw/` |
| `as_of` | ISO date last scored |
| `notes` | what made it work / what NOT to copy |

> **No-PII line:** registers hold public handles + aggregate engagement, never private contact data, never a prospect identity. Per-prospect interest is the GH→Lead-Gen seam, not these registers.

---

## 3. The B2B influence-weighting formula (founder-ratified weights)

Quality + fit beat raw reach. Sub-scores are normalised 0–100; weights sum to 1.0; reach is capped and the smallest term by design.

### 3.1 Voice score

```
weighted_score(voice) =
    <<W_AUDIENCE_FIT>>        * s_audience_fit
  + <<W_ENGAGEMENT_QUALITY>>  * s_engagement_quality
  + <<W_RELEVANCE>>           * s_relevance
  + <<W_VELOCITY>>            * s_velocity
  + <<W_CREDIBILITY>>         * s_credibility
  + <<W_REACH>>              * min(s_reach, <<REACH_CAP>>)
```

Constraint: `<<W_AUDIENCE_FIT>> + <<W_ENGAGEMENT_QUALITY>> + <<W_RELEVANCE>> + <<W_VELOCITY>> + <<W_CREDIBILITY>> + <<W_REACH>> = 1.0`, and **`<<W_REACH>>` is the smallest term** (the B2B inversion of B2C scoring). `<<REACH_CAP>>` clamps how much pure size can ever contribute.

Sub-score definitions (each must be sourced + dated):
- **s_audience_fit** — % of the followers/engagers who match the ICP `role_persona_fit`. The dominant term.
- **s_engagement_quality** — substance + depth of the conversation they provoke (saves/shares, substantive replies, ICP-engager share) — *not* like volume.
- **s_relevance** — topical overlap with Iksula's live theses/solutions (read from Brain `solutions-catalogue` + the TL editorial log).
- **s_velocity** — consistency and recency of in-ICP posting; decays a once-relevant, now-dormant voice.
- **s_credibility** — earned, verifiable authority (operator track record, named results) — **never** fabricated; if unverifiable, score low and flag in `notes`.
- **s_reach** — audience size, capped and de-weighted; present only so a large + high-fit account isn't penalised, never so size alone ranks.

### 3.2 Content score

```
weighted_score(content) =
    <<W_SAVE_SHARE>>      * q_save_share_ratio_norm
  + <<W_SUBSTANTIVE>>     * q_substantive_replies
  + <<W_ICP_ENGAGER>>     * q_icp_engager_share
  + <<W_DWELL>>           * q_dwell_completion
```

Constraint: terms sum to 1.0. **No raw-impressions term** — impressions are the denominator inside the quality ratios, never a score on their own.

### 3.3 Defaults

The skill ships with **no baked numbers** — it presents the formula with `<<W_...>>` placeholders and **stops to ask** for founder-ratified values at first run, then persists them in the engine's memory (versioned) so subsequent runs are reproducible. A weight change is a governance event (§4), not an ad-hoc edit.

---

## 4. Quarterly recalibration

Scores drift; weights shouldn't move casually. Two cadences:

**Every cycle (cheap, at step 1/step 6):** re-score existing rows against fresh raw, add/retire rows, refresh `as_of`. A row whose `as_of` is older than `<<STALENESS_DAYS>>` is flagged stale and re-verified or dropped — never silently trusted.

**Quarterly (the real recalibration):**
1. **Back-test** — did high-`weighted_score` voices/content actually correlate with what worked (the What's-Working playbook + Brain `performance-analytics`)? Where score and outcome disagree, the formula is suspect, not the outcome.
2. **Propose weight deltas** — if a sub-score over/under-predicted, propose a `<<W_...>>` adjustment with the back-test as evidence.
3. **Founder ratifies** — weight changes are **HITL-gated** (route to Slack `#agentic-org-requests`), versioned with the date + rationale. The formula shape stays fixed; only ratified values change.
4. **Re-rank + churn the Top 100** — promote climbers, retire decayed/low-velocity voices, re-verify the survivors. The "100" is a soft cap; quality threshold beats hitting a count.
5. **Reconcile Brain `voices`** — push the recalibrated synthesis (§5).

> Recalibration **never** invents data to justify a weight. If the back-test is inconclusive, weights hold and the question is logged for next quarter.

---

## 5. Relationship to Brain `voices` (CC owns the deep register; TL reads the synthesis)

The Content Creator is **writer-of-record** for the Brain `voices` module. The split:

- **CC owns the deep Top-100 register** (full §2.1 schema, all sub-scores, raw citations) in the engine's working memory — the operational source.
- The Brain `voices` module holds the **distilled, no-PII synthesis** CC publishes from it: the ranked roster, `weighted_score`, `role_persona_fit`, `byline_candidate` flags, and the monthly Influence Analysis — the cross-agent truth layer.
- **Thought Leadership reads `voices`** (not the deep register) to inherit/confirm named-byline personas; **Growth Hacker reads `voices`** for community-engagement voice governance. Both read; only CC writes.
- Write via `brain_io.write('voices', ...)` — **append-only, dated** (`voices-YYMMDD`, `-vN` for same-day). Never raw Drive paths; never overwrite. CC seeds and maintains; downstream agents consume.

> Voice governance line: a `byline_candidate=true` flag is a *suggestion to TL*, not authorization. A named-byline voice is **human-owned and approved** before any content posts as it (set at the CC step-3 gate / TL byline governance) — the register never auto-promotes a person into a publishing persona.

---

## 6. The monthly Influence Analysis (the output that compounds)

Shipped at step 6 each month; the read-out that keeps the engine pointed at what works.

**Reports:**
- **Top movers** — voices/content that climbed or fell this month, with the sub-score that drove the move (e.g. "ranked up on `s_audience_fit`, not reach").
- **Audience-fit map** — which ICP `role_persona_fit` segments are well-covered by high-quality voices vs under-covered (where Iksula has no resonant amplifier yet).
- **What's resonating** — the formats/angles/channels whose `weighted_score(content)` is rising (our assets vs external exemplars, split on `is_ours`).
- **Decay watch** — stale (`as_of` past `<<STALENESS_DAYS>>`) or velocity-dropping rows flagged for re-verify/retire.
- **Byline-candidate shortlist** — new high-credibility, high-fit voices worth TL's attention (flag only; human owns).
- **Recalibration signal** — when quarterly is near, the running back-test of score-vs-outcome.

**How it feeds forward:**
- Updates the **What's-Working playbook** — the resonating formats/angles become planning inputs for `content-build-spec.md` (step 2 of the next cycle), so the calendar tilts toward proven cuts.
- Refreshes the **hook/idea bank** from high-scoring external Top Content (`is_ours=false`) — never copied, mined for the *shape* that worked.
- Publishes the synthesis to Brain `voices` (§5) so TL and GH read the same current truth.

**Format:** agent-readable (structured tables + a tight narrative). Any rendered version for humans follows the brand: **Carlito**, primary red **`#9A0D15`**, light cards. Saved as `Influence Analysis - YYMMDD` (`v1`/`v2` on same-day collision). Use `${CLAUDE_PLUGIN_ROOT}` for any intra-plugin path; never hardcode a Drive ID.

---

## 7. Guardrails (the failure modes)

- **No follower-count ranking.** Any sort or shortlist that would change if you swapped in a raw follower/impression number is broken. Rank on `weighted_score` only.
- **No unsourced score.** Every sub-score cites raw in `_brain/_raw/` + a dated source. `verified=false` rows are flagged, never silently ranked.
- **No fabricated credibility.** `s_credibility` is earned + verifiable or it scores low. Never invent a track record, a result, or an audience claim.
- **No PII in the registers or in `voices`.** Public handles + aggregate engagement only. Prospect identity is the GH→Lead-Gen Spine seam, never here.
- **No silent weight changes.** `<<W_...>>` values move only via the quarterly HITL gate, versioned with rationale. The formula shape is fixed.
- **No auto-promotion to a byline.** `byline_candidate` is a flag to TL; a human owns/approves any named voice before it posts.
- **Stop-and-ask beats guessing.** Missing weights, unverifiable audience claim, or stale raw → halt and ask; do not bake a guessed number.
