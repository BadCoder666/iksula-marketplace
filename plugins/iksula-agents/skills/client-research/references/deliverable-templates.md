# Client Research — Deliverable templates

Templates for the four outputs. Shape each by mode (A prospect / B diligence / C expansion) — sections
marked *(A)* *(B)* *(C)* are mode-weighted; the rest are shared. Do the research first, then read the
`docx` / `pptx` format skill and build. Brand: Carlito, primary red `#9A0D15`, light cards.

---

## A. Research dossier (docx narrative or .md)
Exec-grade, tight, every fact sourced, every inference labelled "(inference — to validate)".

1. **Executive summary** — the punchline in 5–6 lines: who they are, what's changing, the fit, the
   recommended next action. Answer first.
2. **Company snapshot** — what they do, segments, scale (revenue/headcount), geography, ownership,
   recent performance.
3. **Strategy & priorities** — stated strategic agenda (growth bets, cost/margin pressure, customer,
   ESG) from filings/calls/press. This is what any Iksula offer must serve.
4. **What's changing — trigger events** — the timely hooks: leadership moves, funding, M&A,
   restructuring, new initiatives, hiring surges. Dated. *(A: the reason to reach out now.)*
5. **Tech & system landscape (inferred) — recommendation-ready** — systems of record, data platforms,
   cloud, embedded AI; each flagged to-validate AND mapped to the **named Iksula offer + integration
   hook** it implies (use the mapping table in `research-method.md`). *(B: the centre of the diligence.)*
6. **Competitor & incumbent presence** — who else is selling/delivering in this account; where Iksula
   is advantaged or will meet friction. Extends `competitor-radar`.
7. **Stakeholder / buyer map** — likely decision-makers (economic buyer, champion, blocker), what each
   cares about (grounded in `icp-audience`), source for each name/role.
8. **Iksula-fit angle** — the account's needs mapped to **named `solutions-catalogue` offers** and the
   **`proof-catalogue` proof** that backs each. No claim without proof.
9. **Mode-specific section** — *(A)* the way in + buying signals · *(B)* delivery risks + the Monday
   context pack · *(C)* whitespace, renewal-risk signals, relationship map.
10. **Fit & priority score** — the `method-vocab` scores with the one-line reasoning behind each.
11. **Recommended next action** — the decision + owner + timing. Never end on a shrug.
12. **Open questions to validate** — the explicit list of assumptions to confirm.
13. **Sources** — the defensible source list (title · URL · access date), tiered.

---

## B. Internal account deck (pptx, 8–12 slides, Iksula brand)
A briefing for the seller / delivery lead / account team — internal, so blunt and decision-oriented.

- **Cover** — Account · mode · date · "prepared by Iksula Client Research".
- **The account in one slide** — snapshot + the one-line "so what".
- **Why now** — trigger events; the timeliness of the play.
- **Strategy & priorities** — what they're trying to do (their words).
- **System & competitive landscape** — inferred stack + who else is in the account.
- **Stakeholder map** — the buying-group chart (buyer / champion / blocker).
- **The Iksula fit** — needs → named solutions → proof, on one slide.
- **Score & recommendation** — fit/priority + the next action and owner.
- **Open questions** — what we still must validate.
- **Appendix** — sources, detail tables.

Dark/red cover & section dividers, light content cards, real wordmark (per the Iksula PPT brand spec via
`proof-catalogue` / `Iksula FY27/Brand Template/`).

---

## C. One-page meeting brief (.md/.docx, strictly 1 page)
The read-ahead for a specific meeting. Ruthlessly short.

- **Account · meeting · date · attendees (theirs & ours).**
- **Who they are** — 2 lines.
- **What's changing** — the 2–3 trigger events that make this timely.
- **Who's in the room** — each attendee: role + what they care about + (believer/skeptic).
- **The angle** — the one Iksula-fit thesis for this meeting, with the proof point.
- **3 talking points** — the three things to land.
- **The ask** — the specific next step we want out of the meeting.
- **Watch-outs** — 1–2 sensitivities / things not to say.

---

## D. Buyer profile (Mode D — .md/.docx, 1–2 pp per person)
One per named individual you'll pitch/meet. Public, professional, role-based only — never private life.
Layer it onto the account dossier or ship standalone.

- **Name · title · company · tenure · where they sit** (org context).
- **Mandate & scope** — what they own; what success looks like in their seat.
- **Career arc** — prior roles/companies and the lens that implies (operator / technologist / finance /
  transformation), sourced.
- **What they measure** — the KPIs/outcomes the pitch must move (inferred from role + company priorities).
- **Public voice** — their stated views, themes and language, with quotes + source/date.
- **Posture** — believer / pragmatist / skeptic toward the change you're proposing (inference — labelled).
- **How to pitch to them** — the angle, the altitude, the one proof point, the language to use and the
  traps to avoid for *this* person. (Hands the Architect the "how"; the Architect writes the pitch.)
- **Relationship signals** — shared connections / prior touchpoints / mutual context (public only).
- **Sources** — profile, talks, articles, with access dates.

## E. Spine account record (source-of-truth note + handoff)
Written to `_spine/assets/` (append-only, versioned). The single source of truth for the account.

```
# Account record — <Company> — <mode> — YYMMDD
## Source-of-truth note
- Snapshot: <one line>
- Strategy & priorities: <bullets, sourced>
- Trigger events (dated): <bullets>
- System landscape (inferred, to-validate) → offer + hook map: <system → named offer → integration hook>
- Competitive/incumbent presence: <bullets> [extends competitor-radar]
- Stakeholder map: <buyer / champion / blocker, sourced>
- Buyer profiles (Mode D, if done): <name → mandate → how to pitch to them; link the 1–2pp profile>
- Iksula-fit angle: <needs → named solutions → proof>
- Fit/priority score (method-vocab): <fit> / <priority> — <reasoning>
- Recommended next action: <action> — owner <name> — by <date>
- Open questions: <list>
- Raw: _brain/_raw/client-research-raw-<company>-YYMMDD.md
- Sources: <tiered list with access dates>

## Handoff
- To: <Lead Gen | Solutions Architect | AI-Transformation Consultant>
- What they get: <the validated fit, the entry point, the named solutions, the open questions>
- New competitive intel appended: competitor-radar-clientresearch-YYMMDD
- New proof appended (if any): proof-catalogue-YYMMDD
```

**Write order (raw-first, append-only):** (1) raw to `_brain/_raw/` → (2) distil dossier/deck/one-pager
→ (3) gate-2 accuracy sign-off → (4) `brain_io write` namespaced competitive append + proof append →
(5) write the Spine account record + handoff. Never overwrite; every file is a new dated version.
