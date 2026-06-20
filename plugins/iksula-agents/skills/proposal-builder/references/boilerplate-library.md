# Proposal Boilerplate Library — Standard vs Project-Specific

**Why this file exists.** Claude's failure mode is rewriting a whole section when only a few lines are
project-specific — which destroys firm-standard wording and legal boilerplate. This library splits the
four "standard" sections into two buckets so Claude edits **lines, not sections**:

- 🔒 **STANDARD** — firm-wide, reused **verbatim**. **Never edited, never deleted, never reworded.** Copy
  byte-for-byte from the reference.
- ✏️ **PROJECT-SPECIFIC** — the **only** editable content, written as `⟪…⟫` slots. The TBZ sample values
  have been stripped; each slot says what to put and where the value comes from. Fill from the
  dossier / solution record / **project plan (PP)** / effort workbook — or leave the `⟪…⟫` **highlighted**
  for the user if not sourced.

**Editing rule.** Match each line in the reference against this library. STANDARD lines pass through
untouched. PROJECT-SPECIFIC lines are the only ones that change. If a line is not in either bucket, treat
it as project-specific and **ask** before assuming.

---

## §9 Payment Terms — *T&C locked; only the milestone split is project-specific*

### 🔒 STANDARD (verbatim - do not change wording)
- **Prerequisites:** Advance payment as per schedule; scope sign-off, requested access and documents.
- **Support** - Quarterly advance. For hours consumed above the monthly allocation, an overuse invoice is
  raised at the end of each month.
- **Taxes** - As applicable by the Government (including withholding tax), over and above the commercials.
- **Invoice generation** - As per the breakdown. **Invoice payment duration** - As per MSA.
- **Other T&C:** Project kickstarts ~2 weeks after contract sign-off · third-party license/infra/domain/
  hosting/PG/LSP/eKYC/etc. costs borne by the client directly, over and above this price · client POC is
  authorized to take decisions, clarifications, UAT, sign-offs and approve commercial invoices in a timely
  manner · **Proposal validity - 3 months**.

### ✏️ PROJECT-SPECIFIC (edit only these)
- **Milestone split** under *Implementation charges* - **MUST match the project plan (PP)**; the week labels
  and percentages change per engagement and must total 100%:
  `⟪Contract Signing - N%⟫ · ⟪Milestone/Week - N%⟫ · ⟪Milestone/Week - N%⟫ · ⟪Go Live - N%⟫`
  *(TBZ sample, removed from template: Contract Signing 40 / Week 3 25 / Week 6 25 / Go Live 10.)*
- **CR / enhancement / version-upgrade rate** - `⟪SET - Rs NNNN / per person hour⟫` (editable per deal;
  TBZ sample was Rs 2000/hr).
- **Additional-hours / Infra-support rate** - `⟪SET - Rs NNNN / per person hour⟫` (editable per deal;
  TBZ sample was Rs 1600/hr).
- **Named third-party services** in the "Other T&C" cost clause - `⟪list this project's third parties⟫`.

---

## Appendix A3 — Support & AMS

### 🔒 STANDARD (verbatim — incl. A3.2 Engagement Structure, kept entirely as-is)
- A3.1 **BAU Task Scope** list (uptime/job monitoring/bug fixes/ad-hoc data fixes/config/deployment/basic
  user support) — keep verbatim.
- A3.2 **Engagement Structure** — **no change** (blended/shared support pod model and terms).

### ✏️ PROJECT-SPECIFIC (highlight these four for the user — do not silently set)
- `⟪SET — support hours / month⟫` (and the matching figure in §8 Commercials support table).
- `⟪SET — support timezone / coverage window⟫`.
- `⟪SET — SLA (response/resolution targets)⟫`.
- `⟪SET — level/scope of support included vs on-demand⟫`.

---

## §11 Assumptions — *standard frame, project-specific specifics*

### §11.1 To Be Provided by Client
🔒 **STANDARD category lines** (keep the categories + framing):
- ERP / integration access · brand guidelines & content (master data, images, videos, PDFs, CMS) ·
  third-party accounts · infrastructure (cloud + managed DB + monitoring) · a single empowered POC.

✏️ **PROJECT-SPECIFIC fills:**
- `⟪ERP name⟫` + the `⟪reused endpoints⟫` · `⟪cloud provider⟫` · `⟪monitoring tool⟫` ·
  `⟪list of third-party accounts for this project⟫` · `⟪POC SLA — N working days⟫`.
- *(Strip TBZ specifics: Oracle ERP, AWS, Datadog, DigiLocker, the TBZ 3rd-party list.)*

### §11.2 Technical & Integration
🔒 **STANDARD principles** (keep verbatim):
- ERP is the single source of truth for product/inventory/pricing/customer/financial calc · payments &
  logistics via config-driven abstraction layers (names/credentials by client) · accessibility WCAG 2.1 AA
  limited to customer-facing templates developed under this project · KYC validation/approval performed by
  the client's system of record.

✏️ **PROJECT-SPECIFIC fills:**
- `⟪ERP name⟫` · `⟪scheme/module names owned by ERP⟫` · `⟪dependency clause⟫` (e.g. "if <prerequisite
  engagement> is not implemented, pricing may change due to additional effort") · `⟪KYC method⟫`.
- *(Strip TBZ specifics: Oracle, Kalpavruksha, the e-Catalog dependency, Aadhaar/DigiLocker.)*

### §11.3 Delivery Assumptions — **KEPT-AS-IS (locked)**
🔒 **STANDARD (verbatim):** brand assets by client · 1 design iteration before approval, changes after =
CR · dev commences only on receipt of all prerequisites · hybrid-agile methodology · detailed project plan
at kickoff · only Appendix-A scope eligible for development · all 3rd-party licensing/plugin/cloud costs by
client · client coordinates with third-party vendors for integration/testing · POC authorized · timely UAT
sign-offs · project docs in Jira only · test-case repo / user guide out of scope · monitoring tool provided
by client (Iksula configures alerts) · any license/recurring monitoring fee by client.

✏️ **PROJECT-SPECIFIC fills (the only edits in 11.3):**
- `⟪project timeline — N weeks⟫` (must match the PP) · `⟪design-parity clause⟫` (e.g. "design identical for
  web and app") if applicable · `⟪named third parties / ERP⟫` where referenced.

---

## §12 Exclusions — *standard exclusions stay; project ones swap*

### 🔒 STANDARD exclusions (firm-wide — reuse verbatim unless the deal explicitly includes one)
VAPT / penetration / performance-load testing · A/B testing · UX research · user interviews · prototyping ·
WCAG 2.1 AA *testing* · content & creative (copywriting, product descriptions, photography, image/video
editing, on-page SEO) · refund processing & PG-side PCI/compliance · model training & accuracy SLAs for AI
features (visual search / AR-VTO) and 3D/per-SKU asset prep · multi-language (English-only) / multi-country
/ multi-currency · third-party costs (hosting, libraries, PG, LSP, eKYC, AR/visual-search, WhatsApp/CRM,
CDN, SMS/email, stock imagery).

### ✏️ PROJECT-SPECIFIC exclusions (edit per project)
- `⟪business logic owned by client's ERP⟫` (price/making-charge/tax/financial calc; scheme/wallet/instalment
  logic — name the scheme) · `⟪out-of-scope modules/channels⟫` (e.g. a sibling engagement's UI) ·
  `⟪feature-specific carve-outs⟫` (e.g. Video KYC, PWA variants) · `⟪loyalty/accrual source⟫` if owned
  elsewhere.
- *(Strip TBZ specifics: Kalpavruksha, endless-aisle / e-Catalog design, Video KYC, the TBZ PWA lines.)*

---

## How Claude applies this (line-level, not section-level)
1. Copy the reference section unchanged.
2. For each line, find its match here. 🔒 STANDARD → leave it. ✏️ PROJECT-SPECIFIC → fill the `⟪…⟫` slot
   from the dossier / solution record / **project plan** / effort workbook; if unsourced, leave it
   **highlighted** for the user.
3. **Delete the prior proposal's sample project-specific lines** (they were that client's, not boilerplate)
   and replace with this project's. Never carry another client's specifics forward.
4. Reconcile cross-references: payment milestones ↔ project plan; support hours in §8 ↔ Appendix A3;
   numbers consistent everywhere.
5. Anything not classifiable as STANDARD or PROJECT-SPECIFIC → **stop and ask**.
