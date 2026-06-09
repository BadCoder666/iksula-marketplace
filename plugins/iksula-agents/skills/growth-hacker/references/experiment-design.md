# Experiment Design — Growth Hacker

*How GH runs growth experiments **within the plan's bounds**. Mined from the deep mandate §6.7 (experiment design, A/B orchestration, winner declaration) and the audience-type-control rule. GH tests the distribution of an approved asset; it never tests the strategy, the channel mix, or the message — those are the plan's and the Content Creator's.*

**Version:** 1.0 · **Owner:** DJ / Iksula Demand Gen

---

## 1. What GH may vary (and may NOT)

| GH MAY A/B test (distribution variables) | GH may NOT test (someone else owns it) |
|---|---|
| **Hooks** — first line / headline framing of the *same* asset | The thesis / argument / claims (Content Creator) |
| **Post times** — within the plan's window | The channel mix or budget split (Media Planner) |
| **Audience cuts** — segments/cuts the plan + `icp-audience` already allow | The target ICP / who to chase (the plan) |
| **CTAs** — wording/placement of the tracked call-to-action | Funnel intent (TOFU/MOFU/BOFU — the plan) |
| **Native format** — thread vs carousel, length, aspect ratio | The cadence / loop sequencing (the Spine) |

If a hypothesis requires changing the message, the channel, or the audience definition itself → it is **out of bounds**: flag it to the Spine; do not run it.

---

## 2. The method (no peeking, one winner)

For every experiment, **pre-register before launch**:

1. **Hypothesis** — one falsifiable statement (e.g. "a question-hook lifts saves vs a stat-hook for the same carousel, new audience").
2. **Variants** — A vs B (cap concurrent experiments to avoid confounds; isolate one variable at a time).
3. **Primary metric** — one, chosen up front (saves / CTOR / click-through / share rate — the engagement metric the asset is for). **No metric-shopping after the fact.**
4. **Audience-type control** — hold `audience_type` constant within a comparison (**new vs retargeting must not be mixed** — it is the #1 confounder; CTOR over CTR for owned email).
5. **Sample size + stop-rule** — define the minimum sample and the stop condition up front. **No peeking; no multiple-comparison fishing.** Declare a winner **only** at the stop-rule.
6. **Provenance pin** — every variant tied to `asset_ref` + variant id so the result is traceable to raw + source.

---

## 3. Declaring & returning the winner

- A winner is declared **only** when the stop-rule is met at the pre-registered primary metric. No winner on noise.
- Write the **experiment-results** record to the **Spine**: hypothesis · variants · primary metric · sample · winner + lift · audience_type · `asset_ref`. This informs the **next cadence** (the Spine decides cadence; GH supplies the evidence).
- Synthesise the winner into the Brain feed `channel-intel-growth-YYMMDD` ("what rewarded this cycle" + experiment winners), **raw-first**, traceable to the raw capture.
- Feed the raw variant engagement into `performance-analytics-growth-YYMMDD` (aggregate, `audience_type` stamped, no PII).

---

## 4. Guardrails

- **Within plan bounds only** — never silently re-strategise; an out-of-bounds idea is a Spine flag, not an experiment.
- **One variable per test** — isolate confounds; cap concurrent tests.
- **Audience-type controlled** — never read a result that mixed new + retargeting audiences.
- **No vanity winners** — judge by the engagement metric the asset exists to drive, not impressions for their own sake.
- **GH supplies evidence, the Spine decides cadence** — the experiment result informs the next plan; GH does not change the plan itself.
