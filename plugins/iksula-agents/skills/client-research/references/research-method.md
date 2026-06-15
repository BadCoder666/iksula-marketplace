# Client Research — Method (source map, per-mode checklists, source-quality & scoring)

How to actually research one named company. Read this in phase 1. Capture **raw-first** to
`_brain/_raw/` as you go — every source, figure, quote, URL and access date — then distil.

## The source map (where the signal lives)
Search the public record and triangulate. Always verify present-day facts with search, not memory.

| Source | What it gives you | Watch-outs |
|--------|-------------------|------------|
| **Company website / product & pricing pages** | What they sell, positioning, segments, customers, public pricing | Marketing gloss — corroborate claims |
| **Annual report / 10-K / 20-F / investor deck / earnings call transcript** | Strategy, segments, margins, stated priorities, risks, capital allocation | Public companies only; the most authoritative source — anchor here |
| **Funding / ownership data (Crunchbase, PitchBook-style, press)** | Stage, investors, last round, valuation signal, PE/VC ownership | Private valuations are estimates — label as such |
| **Press releases & news (last 12–18 mo)** | Trigger events: leadership, M&A, expansion, restructuring, partnerships, launches | Recency matters; date every item |
| **Job postings (careers page, LinkedIn Jobs)** | The tech-stack & intent goldmine — named systems (SAP/Salesforce/ServiceNow/cloud/data platforms), AI/ML hiring, where they're scaling | Infers the stack; **always label "to-validate"** |
| **LinkedIn (company + people)** | Org shape, leadership, headcount trend, the stakeholder map, recent joiners/movers | Role/professional data only — no personal data |
| **Analyst / industry reports, trade press** | Where they sit vs. peers, industry shifts hitting them | Often paywalled — cite the public summary |
| **Competitor & incumbent footprints** | Who else is selling into this account; case studies naming this client | Cross-reference with `competitor-radar` |
| **Glassdoor / review sites (light touch)** | Culture, change signals, pain themes | Noisy and biased — corroborate, never lead with it |
| **Brain registers** | `competitor-radar`, `icp-audience`, `proof-catalogue`, `solutions-catalogue`, prior account record | Read first so you extend, not restart |

**Standard search set** (swap `<company>` and run for the company + its 2–3 closest competitors):
`<company> strategy`, `<company> annual report`, `<company> funding / acquisition`, `<company> leadership / CxO`,
`<company> hiring <SAP|Salesforce|ServiceNow|data|AI>`, `<company> AI / digital transformation`,
`<company> <core system>`, `<company> partner / vendor`, `<company> layoffs / restructuring`.

## Per-mode research checklists
Run the shared phases (snapshot → strategy → signals → account map → fit), but weight them by mode.

### Mode A — Prospect Dossier (emphasis: timeliness + the way in)
- Snapshot + strategy + recent performance.
- **Trigger events** — the timely hook for outreach (new exec, funding, M&A, market entry, a public
  problem, a hiring surge in a function Iksula serves). No live trigger = a weaker play; say so.
- Likely pain mapped to Iksula's `solutions-catalogue`; the **fit angle** and the **proof** to back it.
- **Buying signals & the way in** — RFPs, intent signals, the function under pressure, the likely entry
  point and the first stakeholder to reach.
- Stakeholder map: the economic buyer, the likely champion, the likely blocker.

### Mode B — Pre-Engagement Diligence (emphasis: walking in informed & de-risked)
- Deeper **org & stakeholder map** — who owns what, who sponsored the work, who'll resist.
- **Tech & system landscape** — inferred systems of record, data platforms, recent migrations, embedded
  AI they likely already own; flagged to-validate. This shapes delivery.
- **Incumbents & competitors in the account** — who else is delivering here; where we'll meet friction.
- **Delivery risks** — integration debt signals, change-fatigue signals, procurement/security posture,
  past failed initiatives if public.
- The **context pack** the team needs Monday: vocabulary, org chart, system names, sensitivities.

### Mode C — Account Expansion / Renewal (emphasis: growth + retention)
- **What's changed** since we started — new leadership, new strategy, new funding, reorg.
- **Whitespace** — functions/units we don't yet serve; adjacent `solutions-catalogue` offers; expansion plays.
- **Renewal-risk signals** — sponsor departure, budget pressure, competitor entry, satisfaction signals.
- **Relationship map** — current champions, at-risk relationships, who to cultivate next.
- **Compliance:** existing client — expansion through the relationship; **never a cold sequence** (suppression).

### Mode D — Buyer Profile (emphasis: the person, and how to pitch to them)
Person-level research on a specific named individual. Runs layered onto A/B/C or standalone. **Public,
professional, role-based information only** — never personal/private life; the goal is to pitch well to a
person, not to surveil one.
- **Who they are** — current role, exact title, tenure, scope/mandate, where they sit in the org.
- **Career arc** — prior roles/companies, how they got here, what that says about their lens (operator?
  technologist? finance? transformation?).
- **What they measure** — the KPIs and outcomes they're accountable for (infer from role + the company's
  stated priorities); this is what your pitch must move.
- **Public voice** — talks, interviews, posts, articles, panels: their stated views, the language they
  use, the themes they champion. Quote them; it's the sharpest tailoring signal.
- **Believer vs. skeptic** — their likely posture to AI / outsourcing / the change you're proposing,
  inferred and labelled.
- **How to pitch to them** — the angle, the proof point, the altitude and the language tuned to *this*
  person (e.g. a CFO-minded buyer → unit economics + payback; a transformation lead → ambition + roadmap).
- **Relationship signals** — shared connections, prior touchpoints, mutual context (public only).
**Person source map:** LinkedIn profile + activity · the company leadership/bio page · conference/webinar
speaker pages & recordings · podcast/interview transcripts · bylined articles & quotes in press · the
company's earnings call (if they speak on it). Date and cite each; label every inference.

## Tech stack → recommendation-ready mapping (do this, don't just list systems)
A bare "they run SAP and Salesforce" forces the Architect to re-derive the play. Instead, map each
inferred system to the **named Iksula offer + integration hook** it implies, flagged to-validate:

| Inferred system (signal) | Likely system of record | Named Iksula offer it implies | Integration hook | Confidence |
|---|---|---|---|---|
| e.g. S/4HANA postings | ERP / supply chain | `<solutions-catalogue offer>` | `<API / data layer / agent surface>` | inference — to validate |
| e.g. Salesforce + Agentforce | CRM / service | `<offer>` | `<hook>` | inference — to validate |

Pull the offer names from `solutions-catalogue` — never invent one. The mapping is research's output; the
Architect turns it into the actual recommendation in the pitch.

## Source-quality & inference rules
- **Tier the evidence.** Primary (filings, the company's own disclosures, named postings) > reputable
  secondary (established press, analyst notes) > soft (review sites, forums, social). Lead with the
  strongest; never let a soft source carry a load-bearing claim.
- **Every fact gets a source + access date** in raw. If you can't source it, it's TBD — not a fact.
- **Label every inference.** Anything you reasoned rather than read (systems, intent, politics, internal
  data quality) is flagged "(inference — to validate)". Labelled inference is the credibility move; false
  confidence is the failure mode.
- **Recency wins.** Prefer the last 12–18 months for signals; date everything; flag stale facts.
- **Triangulate big claims.** A material number (revenue, headcount, valuation) wants two independent
  sources or an explicit "single-source — unconfirmed" flag.
- **Public only.** No logged-in scraping, no personal data beyond professional/role information.

## Fit & priority scoring (use `method-vocab` — do not invent local scales)
Score the account so it's comparable with the rest of the firm's pipeline. Pull the exact scales from
`method-vocab`; the typical shape:
- **Fit** — how well the account's needs map to named Iksula solutions + real proof (Low/Med/High).
- **Priority / propensity** — strength and timeliness of buying signal + trigger events (Low/Med/High).
- **Value-lever & archetype** — tag with the controlled vocabulary so it rolls up consistently.
A High-fit / High-priority account with live proof is a "go now"; record the score and the reasoning in
the source-of-truth note. No fit score without proof behind it.
