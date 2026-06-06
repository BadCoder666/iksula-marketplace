# Excel Build Spec (exact structure for every vertical workbook)

Build with openpyxl. Match `assets/B2B Distribution.xlsx` for look and depth. Font Arial throughout. Navy `1F3864` headers, blue `2E5496` sub-headers, group fills (Commercial `DDEBF7`, Supply Chain `E2EFDA`, Finance `FCE4D6`, Enabling `FFF2CC`). Freeze panes and auto-filter on data tabs. Recalculate with `scripts/recalc.py` and confirm ZERO errors before delivering.

## Tab order (exactly six)
1. ReadMe & Rubric
2. Coverage Map
3. Function Narratives
4. Task Matrix
5. Cross-Cutting Horizontals
6. Iksula Solution Shortlist

## Tab 1 — ReadMe & Rubric
Title + subtitle; a metadata block (Vertical, Organisation archetype, Prepared by, Date, Eventual purpose, Economic lens); a tab guide; the scoring rubric; the controlled vocabularies (including the Economic Buyer buying-centres). Do NOT start any cell text with "=" (Excel reads it as a formula) — rephrase rubric lines.

## Tab 2 — Coverage Map
Columns: Group · Function · Status · # L3 Tasks Mapped · Notes. The task count uses `=COUNTIF('Task Matrix'!B:B, B<row>)`. End with a TOTAL row `=SUM(...)`. Status cells green-filled "Done". This is the mandatory self-audit, made visible — every function in the taxonomy must appear.

## Tab 3 — Function Narratives
Columns: Group · Function · Process Spine (L1→L2→L3 hotspots) · Typical Tools · Obvious Automation · Non-Obvious High-Value Plays. One row per function. This preserves the chat-level prose depth. Row height ~96.

## Tab 4 — Task Matrix (the engine — one row per L3 task)
23 columns, in order:
1 Group · 2 Function · 3 L1 Sub-process · 4 L2 Process · 5 L3 Task · 6 Current Tools · 7 Manual Hotspot/Pain · 8 AI/Automation Opportunity · 9 Obvious/Non-obvious · 10 Solution Archetype · 11 Value Lever · 12 Driver Metric · 13 Impact · 14 Data Readiness · 15 Integration Ease · 16 Accuracy Tolerance · 17 Feasibility · 18 Composite Priority · 19 Priority Tier · 20 Quick Win · 21 Reusability · 22 Productizable · 23 Economic Buyer.

Formulas (row r):
- Feasibility (Q): `=ROUND(AVERAGE(N{r}:P{r}),1)`
- Composite (R): `=ROUND((M{r}+Q{r})/2,1)`
- Tier (S): `=IF(R{r}>=3.8,"P1",IF(R{r}>=3,"P2","P3"))`
- Quick Win (T): `=IF(AND(M{r}>=4,Q{r}>=3.5),"Yes","No")`

Conditional formatting: color-scale on Composite (R) red→yellow→green; green fill where Tier="P1"; amber fill where Quick Win="Yes". Auto-filter the whole range. Aim for ~100–120 L3 rows for a full vertical; ensure tiers discriminate (don't let everything collapse into one tier — if so, revisit Impact spread).

Column 9 "Non-obvious" rows: bold + red text to make them pop. Column 13–16 are the only hand-entered scores; keep them honest and varied. Column 23 Economic Buyer at the task level names the role-owner of that specific process.

## Tab 5 — Cross-Cutting Horizontals
Columns: Theme/Horizontal · What it is · Functions it spans · Why build once · Solution Archetype · Reuse value for Iksula. Cover at least: unstructured-document understanding, NL-analytics, master-data spine, the recovery & leakage THEME, and a conversational/agent interface layer.

## Tab 6 — Iksula Solution Shortlist
Columns (12, in order): # · Solution · What it does · Functions served · Primary Value Lever · **Economic Buyer** · Archetype · Indic. Composite · Reuse · Productizable · Phase · Iksula rationale/GTM angle. ~10–12 solutions sequenced into Phase 1/2/3, phase-colored. Lead with leakage-recovery + working-capital plays for thin-margin verticals.

**Economic Buyer (NEW, required).** Every shortlisted solution is tagged with the single buying centre that owns the budget and signature, colour-banded for scannability. This is what makes the shortlist sellable: value levers are NOT buyers (one lever scatters across many signatures), so packaging by buyer turns the portfolio into "one buyer, one ROI conversation per bundle". Use the four canonical buying centres:

- **CFO / Finance** (fill `FCE4D6`) — leakage recovery, working capital, statutory/close. The self-funding LAND motion.
- **COO / Operations** (fill `E2EFDA`) — cost-to-serve, fulfilment, planning, support, returns/trust.
- **CRO/CMO / Commercial** (fill `DDEBF7`) — revenue growth: search, content, pricing, retention, quoting.
- **CIO/CDO / Tech & Data** (fill `FFF2CC`) — the shared horizontals (doc-extraction, NL-analytics, master-data); sold once, beneath everything.

Derive the buyer with the canonical `economic_buyer(name, lever)` helper in `build_template.py` (keyword-on-name first, fall back to lever) so assignments stay consistent across verticals. Recommended GTM narrative: LAND with the CFO's self-funding recovery bundle → EXPAND to COO (cost-to-serve) and Commercial (growth) → CIO horizontals as shared substrate.

## Build approach
Adapt the build scripts (the scaffold in `scripts/build_template.py` shows the helper functions, the `economic_buyer()` mapping, and the tab patterns). Practical method: build tabs 1–2 in one script, tabs 3–4 in a second (the big content), tabs 5–6 in a third, each `load_workbook` + delete-if-exists for idempotency, then recalc. Keep the controlled vocabularies, rubric and Economic-Buyer taxonomy identical to this spec so verticals stay comparable.
