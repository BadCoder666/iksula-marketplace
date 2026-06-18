# Content Build Spec — Content Creator

*The build rubric for the central content engine: the **format × channel × message** map, the **funnel lens**, **voice-governance routing**, the **5-second headline test**, the **PUBLISHING-CALENDAR FIXED SCHEMA** (the handoff contract the Growth Hacker executes), and a **per-product build checklist** for every content product the engine ships. The `SKILL.md` holds the runnable workflow and operating principles; this is the authoritative build detail. Read it at step 2 (Plan) and step 4 (Produce). The deep governing spec is `${CLAUDE_PLUGIN_ROOT}/skills/content-creator/references/mandate.md`.*

**Version:** 1.0 · **Owner:** DJ / Iksula Content Engine · **Scope:** atomization → planning → production. The Content Creator **packages, it does not re-argue, instrument, or publish** — it never rewrites a thesis, invents proof, applies a UTM, or advances a publish status. Those belong to Thought-Leadership (the argument), the Media Planner (channel mix + windows + budget), and the Growth Hacker (instrumentation + publishing).

---

## 0. The one rule that governs this whole file

Take a **hero asset** (the monthly thought-leadership article, or an approved solution intro-deck handoff) and produce channel-native **spokes** — each carrying one strong idea, native to its surface, tagged to a funnel stage, owned by a governed voice — then sequence every spoke into the **publishing calendar** (§5). The calendar IS the deliverable; the products are its payload. **Nothing the Content Creator produces is published, scored, or instrumented here** — it is handed to the Spine for the Growth Hacker to execute.

Founder-/plan-supplied values are **placeholders**, never guessed: `<<ICP_SEGMENTS>>`, `<<CHANNEL_SET>>` (the closed channel list the Media Planner approves), `<<POSTING_WINDOWS>>`, `<<APPROVED_PROOF_POINTS>>`, `<<BYLINE_PERSONAS>>` (the named leaders defined in Brain `voices`). The Content Creator reads channels + windows from the **media plan**; it never invents a channel that isn't in `<<CHANNEL_SET>>`.

---

## 1. The format × channel × message rubric

One idea travels across formats without diluting. Map each hero asset to the **message types** it can carry, then route each message type to the **channel × format** that rewards it. Map only into channels present in the plan's `<<CHANNEL_SET>>`.

| Message type | What it does | Native channel × format | Default funnel | Default `publish_as` |
|---|---|---|---|---|
| **Thesis / POV** | the core argument, stated to provoke the right reader | LinkedIn `document`/`carousel`, Blog `blog-edition`, X `thread` | TOFU | **byline persona** |
| **Reframe / contrarian take** | flips a category assumption | LinkedIn `post`, X `thread` | TOFU | **byline persona** |
| **How-it-works / mechanism** | the defensible "how", not features | LinkedIn `carousel`, Blog `blog-edition`, YouTube `short-video` | MOFU | byline or Iksula |
| **Proof / outcome** | a real, approved client outcome | LinkedIn `post`, Blog `blog-edition` | MOFU/BOFU | **Iksula** (promo/proof) |
| **Buyer-pain / cost-of-status-quo** | names the KPI the buyer owns | Email `nurture-email`, LinkedIn `post`, Blog | MOFU | byline or Iksula |
| **Offer / next-step** | a low-friction first step (pilot/assessment) | Email `leadgen-email`, Blog on-page CTA | BOFU | **Iksula** (promo) |
| **Original data / research** | a defensible stat the engine owns | `research-brief` → Blog `blog-edition`, LinkedIn `carousel` | TOFU/MOFU | byline persona |
| **Conversation / interview** | a leader in dialogue | `podcast-brief`, YouTube `short-video` | TOFU | **byline persona** |
| **Visual explainer** | one idea as an asset | `visual-brief` → LinkedIn `document`, Blog | TOFU/MOFU | byline or Iksula |

**Channel set** (closed; the only legal `channel` values): `LinkedIn` · `Blog` · `X` · `Email` · `YouTube` · `Podcast` · `…` — exactly as the Media Planner's `<<CHANNEL_SET>>` defines. Never introduce a channel the plan didn't approve.

**Format set** (closed; the only legal `format` values): `post` · `carousel` · `document` · `thread` · `blog-edition` · `nurture-email` · `leadgen-email` · `short-video` · `podcast-brief` · `research-brief` · `visual-brief`.

**Reshape budget.** The Content Creator authors the *native* cut per channel (a thread is written as a thread, not a chopped blog). The Growth Hacker may further reshape for native form (length, aspect ratio) but **may not re-argue** — so the cut you hand over must already be correct in message and claim.

---

## 2. The funnel lens (every row is tagged)

Every calendar row carries a `funnel_stage`. Never ship an all-TOFU pile; sequence a deliberate spread.

- **TOFU** — attract the right reader: thesis, reframe, original data, conversation. Authority voice. No ask beyond "read/follow."
- **MOFU** — build conviction: mechanism, buyer-pain, proof. Mixed voice; introduces the Iksula angle without selling.
- **BOFU** — convert intent to a step: offer/next-step, lead-gen email, on-page CTA. Iksula voice; one concrete low-friction ask.

A campaign that derives from one hero asset must produce a **funnel ladder**, not a flat layer — typically TOFU thesis cuts → MOFU mechanism/proof → one BOFU step, chained via `depends_on` so BOFU never fires before its TOFU/MOFU runway exists.

---

## 3. Voice-governance routing (`publish_as`)

Every row names exactly one `publish_as` owner. The routing rule is fixed:

- **Authority / thought-leadership content publishes AS a named leader** — a **byline persona** inherited from Thought-Leadership and defined in the Brain `voices` module (`<<BYLINE_PERSONAS>>`). This is the voice for thesis, reframe, mechanism-as-POV, research, and conversation content.
- **Promotional / proof content publishes as the company — `"Iksula"`** — proof/outcome, offer/next-step, lead-gen email, the company-page promo cut.

**The human gate (step 3) owns the voice.** A named-byline voice is **drafted against its persona, never invented**, and a human owns/approves that voice before anything is produced for it to post as — the same governance the Growth Hacker honours on community replies. If a row needs a byline persona that does not exist in `voices`, **stop and ask** — do not invent a leader.

`publish_as` is set by the Content Creator at plan time and is **immutable downstream** — the Growth Hacker honours it, never reassigns it.

---

## 4. The 5-second headline test (gate every product)

Every product leads with a **headline** — the post's first line, the blog/article title, the carousel cover, the email subject, the video title, the thread hook. It passes only if a target reader (a busy CXO in `<<ICP_SEGMENTS>>`) can tell **in ~5 seconds** what they'll get and whether to click.

Pass criteria — concrete + specific; the value or tension legible without reading the body; survives the LinkedIn "see more" cut and the inbox subject-line truncation. **Fail** — vague cleverness, curiosity-gap that needs decoding, jargon, or an Iksula-centric framing instead of a buyer-KPI framing. If it fails, **rewrite the headline before the body exists** — never produce a body under a failing headline.

---

## 5. THE PUBLISHING-CALENDAR FIXED SCHEMA (the handoff contract)

**This is the centerpiece and the authoritative definition.** The calendar is the **Content-Creator → Growth-Hacker handoff contract**: the Content Creator authors every row and sets every field *except the three the Growth Hacker advances*; the Growth Hacker then **advances `status`** and **applies `tracked_cta_utm`** as it instruments and publishes. One row = one produced spoke. The schema is **fixed** — use these field names exactly; do not rename, drop, or invent fields.

| Field | Owner / who sets it | Definition |
|---|---|---|
| `row_id` | **Content Creator** | **ULID** — stable, unique; the dedupe key for the row and the join key the Growth Hacker advances against. |
| `hero_asset_ref` | Content Creator | the source thesis/solution this spoke derives from (the TL article id, or the solution intro-deck handoff id). |
| `spoke_asset_ref` | Content Creator | the id of the specific produced content product (resolves into the asset bundle the Growth Hacker publishes). |
| `channel` | Content Creator | one value from the closed **channel set** (§1): `LinkedIn` \| `Blog` \| `X` \| `Email` \| `YouTube` \| `Podcast` \| `…`. Must be in the plan's `<<CHANNEL_SET>>`. |
| `format` | Content Creator | one value from the closed **format set** (§1): `post` \| `carousel` \| `document` \| `thread` \| `blog-edition` \| `nurture-email` \| `leadgen-email` \| `short-video` \| `podcast-brief` \| `research-brief` \| `visual-brief`. |
| `publish_as` | Content Creator | a named **byline persona** (authority content) **OR** `"Iksula"` (promo/proof) — §3. Voice governance; immutable downstream. |
| `funnel_stage` | Content Creator | `TOFU` \| `MOFU` \| `BOFU` — §2. Every row tagged. |
| `planned_window` | Content Creator (from the plan) | the scheduled date/time window, aligned to the channel's posting-window intel (`<<POSTING_WINDOWS>>` from the media plan + `channel-intel`). The Growth Hacker finalises exact timing within it. |
| `status` | **Growth Hacker advances** | `Planned` \| `Scheduled` \| `Published`. The Content Creator sets the initial `Planned`; **the Growth Hacker advances it — the Content Creator NEVER does.** |
| `tracked_cta_utm` | **Growth Hacker applies** | the UTM + tracked-CTA tag the Growth Hacker attaches at instrument-time so interest is attributable to `spoke_asset_ref`. The Content Creator leaves it empty; it is not the Content Creator's to fill. |
| `variant` | Content Creator (bounds) / Growth Hacker (runs) | A/B cell id, optional — **within plan bounds only** (hook / time / audience / CTA). The Content Creator may pre-author variant cuts; the Growth Hacker runs the test. Never a thesis/claim/channel variant. |
| `depends_on` | Content Creator | `row_id`(s) that must publish first (e.g. a BOFU step depends on its TOFU runway). The Growth Hacker honours the order. |
| `approval_status` | Content Creator (at the step-3 gate) | `approved` \| `revise` \| `hold` — set at the mandatory human gate (SKILL step 3). Only `approved` rows go to production and handoff. |
| `notes` | Content Creator | free text — key message, hook intent, asset dependencies, anything the Growth Hacker needs to publish faithfully without re-strategising. |

**Field-discipline rules (do not violate):**
- The Content Creator **never** touches `status` or `tracked_cta_utm` — those are the Growth Hacker's; pre-filling them corrupts the seam.
- The Growth Hacker **never** touches `publish_as`, `funnel_stage`, `channel`, `format`, or the message — those are the plan's and the Content Creator's; reshaping is native-form only.
- `variant` stays within plan bounds (hook/time/audience/CTA). A message/claim/channel "variant" is out of bounds → flag, don't author.
- Only `approval_status = approved` rows are handed off. `revise`/`hold` rows stay back until cleared.
- `row_id` and `spoke_asset_ref` are ULIDs and **stable** — the Growth Hacker's execution-log and the Brain's `performance-analytics-growth` join on them; never regenerate them on revision (carry the same id, bump the asset's `vN`).

**Schema consistency.** These exact field names are the single source of truth shared with any CC→GH seam note. The Growth Hacker then emits a **separate** `content-sourced-lead` seam to Lead Gen — that object is defined authoritatively in `${CLAUDE_PLUGIN_ROOT}/skills/growth-hacker/references/seam-contract.md` and is **not** redefined here. Do not conflate the calendar (CC→GH) with the lead seam (GH→Lead Gen).

---

## 6. Per-product build checklists

One checklist per content product the engine ships (SKILL → Outputs). Every product: passes the **5-second headline test** (§4), is tagged `funnel_stage`, names its `publish_as`, draws proof **only** from `<<APPROVED_PROOF_POINTS>>`, and emits exactly one calendar row per spoke (§5). **Package, don't re-argue.**

### 6.1 Edited TL article — Blog + LinkedIn editions
- Edit the approved thesis for the surface; **do not re-argue or invent** — packaging only.
- **Blog edition** (`blog-edition`): title passes 5-sec test; lede states the buyer tension in their KPI; one on-page CTA placeholder for the Growth Hacker to instrument; `publish_as` = byline persona.
- **LinkedIn edition** (`document` or long `post`): hook in the first 1–2 lines (survive "see more"); reshaped to the platform's rhythm, same claim; byline persona.
- Two rows (one per channel), same `hero_asset_ref`, distinct `spoke_asset_ref`.

### 6.2 Follow-up post sequence
- A short ladder of posts (`post`) extending the article's one idea across days; each post one beat, not a recap.
- Sequence via `depends_on` so the ladder runs in order; spread `funnel_stage` (TOFU openers → a MOFU mechanism/proof beat).
- Each post earns its own headline; byline persona unless it's a proof beat (then `"Iksula"`).

### 6.3 LinkedIn carousels / document posts
- `carousel`/`document`: cover slide = the headline (5-sec test on the cover alone); one idea per slide; last slide a soft CTA placeholder.
- Brand any rendered slide deck to the Iksula brand — **Carlito**, primary red **`#9A0D15`**, light cards.
- TOFU/MOFU; byline persona for POV/mechanism, `"Iksula"` only for a proof carousel.

### 6.4 X threads
- `thread`: tweet 1 = the hook (must stand alone); one claim per post; tightened to platform length; no chopped-blog feel.
- Reshaped native, same thesis; byline persona; TOFU/MOFU.

### 6.5 Blog posts (non-article)
- `blog-edition`: original SEO-aware posts off a hero asset — mechanism, buyer-pain, or proof; title passes 5-sec test and the buyer's search intent.
- One on-page CTA placeholder (Growth Hacker instruments); MOFU default; voice per message type.

### 6.6 Email — nurture + lead-gen
- **Nurture** (`nurture-email`): MOFU; value-first, subject = hook (5-sec test against the inbox truncation); one idea, one soft CTA. Authored as a **broadcast/newsletter cut** for the Growth Hacker's 1-to-many motion — **not** 1-to-1 outreach (that is Lead Gen).
- **Lead-gen** (`leadgen-email`): BOFU; one concrete low-friction next step (pilot/assessment/workshop); `publish_as = "Iksula"`.
- Note in `notes`: the Growth Hacker's **first-send of any NEW sequence is human-gated** — flag new sequences so the gate is honoured.

### 6.7 Short-video ideas / storylines
- `short-video`: a storyline brief (hook → 3–5 beats → CTA), title = the 5-sec hook; aspect-ratio/length left to the Growth Hacker's native reshape, **the argument is not** — pin the claim and the beats.
- TOFU/MOFU; byline persona for POV, `"Iksula"` for proof.

### 6.8 Podcast briefs
- `podcast-brief`: guest/host framing, the through-line thesis, 5–8 question beats, the one takeaway, do-not-say list (no fabricated proof, no competitor disparagement).
- TOFU; `publish_as` = byline persona (the named leader who appears).

### 6.9 Research / report briefs
- `research-brief`: the question, the (real, sourced) data the engine actually has or can defensibly gather, the angle, the headline finding (5-sec test), and downstream cuts (a `blog-edition` + a `carousel`).
- **Never fabricate a stat** — if the data isn't there, the brief says so and scopes what's needed; stop-and-ask if a number is asserted without a source.
- TOFU/MOFU; byline persona.

### 6.10 Visual / asset briefs
- `visual-brief`: one idea to render (diagram, framework, before/after) — the concept, the labels, the data behind it (sourced), the target format (LinkedIn `document`, blog inline).
- Brand any rendered output — **Carlito**, primary red **`#9A0D15`**, light cards.
- TOFU/MOFU; voice per host message.

---

## 7. Pre-handoff checklist (run before step 6 handoff)

- [ ] Every row uses **only** legal `channel` (in `<<CHANNEL_SET>>`) and `format` values (§1).
- [ ] Every row is tagged `funnel_stage`; the campaign is a **ladder**, not an all-TOFU pile (§2).
- [ ] Every row names a `publish_as` owner; every byline persona exists in `voices` and is human-approved (§3).
- [ ] Every product's headline passes the **5-second test** (§4).
- [ ] `status = Planned`, `tracked_cta_utm` **empty** on every row — those are the Growth Hacker's (§5).
- [ ] `row_id` + `spoke_asset_ref` are stable ULIDs; `depends_on` chains BOFU behind its runway.
- [ ] Only `approval_status = approved` rows are in the handoff bundle; `revise`/`hold` held back.
- [ ] Zero fabricated proof, stat, client, or quote anywhere; all proof traces to `<<APPROVED_PROOF_POINTS>>`.
- [ ] Any rendered deck/doc is on-brand (Carlito, `#9A0D15`, light cards) and saved `Name - YYMMDD` (v1/v2 same-day).

---

## Conventions (do not remove)
- Brand: Carlito, primary red `#9A0D15`, light cards — for any rendered deck/doc output.
- File naming: `Name - YYMMDD` (v1/v2 for same-day). Confirm the save folder with the user; standing registers/playbook live with the engine's memory.
- Use `${CLAUDE_PLUGIN_ROOT}` for intra-plugin paths; never hardcode Drive folder IDs — resolve at runtime via `brain_io` (defer to the live `brain_io-howto` in `_brain/`).
- Founder-/plan-supplied values are `<<PLACEHOLDERS>>` — never bake a guessed number, channel, window, or persona.
- The Content Creator reads from and writes to the Brain only via `brain_io` (get/list/write); it reads channels/windows from the **media plan** and hands the calendar + asset bundle to the **Spine** for the Growth Hacker. It never publishes, instruments, or advances a status itself.

## Related contracts (read, don't duplicate)
- `${CLAUDE_PLUGIN_ROOT}/skills/content-creator/references/mandate.md` — the full governing mandate.
- `${CLAUDE_PLUGIN_ROOT}/skills/content-creator/references/registers-and-weighting-playbook.md` — the two registers, the influence-weighting formula, the monthly Influence Analysis.
- `${CLAUDE_PLUGIN_ROOT}/skills/growth-hacker/references/seam-contract.md` — the GH → Lead Gen `content-sourced-lead` seam (the *downstream* object; not the calendar).
- `${CLAUDE_PLUGIN_ROOT}/skills/growth-hacker/references/distribution-playbook.md` — how the Growth Hacker reshapes + publishes the rows this spec produces.
