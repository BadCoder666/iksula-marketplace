---
name: magento2-audit
description: Run a CEO-ready audit of a Magento / Adobe Commerce (or other) e-commerce site across five dimensions — Business & Conversion, Customer Experience & Merchandising, Technology & Platform Health (incl. measured performance + security), Operations & Risk, and Growth & Value-Add. Asks the user a short set of questions, MEASURES performance (PageSpeed Insights) and security from the URL, gathers evidence from whatever access is available (website URL, code/repo, backend/admin, analytics, New Relic/APM, infra), and when access is missing it outputs exact retrieval steps. Validates every suggestion against the live site before recommending it, scores each dimension 1–5, records the basis/coverage, and generates a presentable PowerPoint report. Use when the user asks to audit, assess, health-check, or review an e-commerce/Magento store and produce a report or deck.
---

# Magento / E-commerce Audit (self-contained)

Fully self-contained. Follow the steps in order. Two hard rules:
- **Measure, don't assume.** Performance and security ARE measurable from a URL — always do it.
- **Validate before you suggest.** Never recommend a feature that already exists on the site. Check first.

---

## PART A — The Agent's Mandate

**What this skill is for.** Produce a CEO-ready diagnostic audit of a Magento / Adobe Commerce (or other) e-commerce site — measured, evidence-based, and packaged as a presentable report. It diagnoses; it does not implement.

**Scope (what it owns).** The five audit dimensions (Business & Conversion, CX & Merchandising, Technology & Platform Health, Operations & Risk, Growth & Value-Add); measuring performance (PageSpeed Insights) and security (response headers) from the URL; gathering evidence from whatever access is provided; validating every recommendation against the live site; scoring each dimension 1–5 with a stated confidence/basis; and generating the report deck plus a Data Request Pack for gaps.

**Out of scope.** Writing the fixes it recommends (that is the **`magento2-coding`** skill's job), and any go-to-market / research / content work owned by the eleven agentic-org skills. No scope overlap.

**Place in the org model (Brain / Hands / Spine).** A **Hands** skill — diagnostic/delivery. It is self-contained: it does not read or write the shared Brain. Its output (findings + roadmap) is a clean hand-off point — implementation can flow to `magento2-coding`, and a productized offering can flow to `solutions-architect-create` — but it wires to neither automatically.

**Engagement rule.** Honour the mandatory question gate in STEP 1 (never assume access and proceed silently), and ask the user which folder to save the deck to rather than defaulting (STEP 5).

## PART B — The Deliverables

- **`audit_data.json`** — the structured audit (coverage, `tech_snapshot`, five scored dimensions with findings, risks/blockers/opportunities, roadmap). Shape defined in STEP 4.
- **A brand-compliant PowerPoint report** — Iksula brand (Carlito, primary red `#9A0D15`, light cards), named `<Client> Audit - YYMMDD.pptx`, saved to a user-chosen folder. Deck flow defined in STEP 5.
- **A Data Request Pack** — exact retrieval steps + paste-back templates for every source marked *Not assessed*, so the team can supply data for a deeper v2.

---

## STEP 1 — Ask the user these questions

> **MANDATORY GATE — do not skip.** You MUST ask these questions and WAIT for answers before doing
> any evidence-gathering, scoring, or deck generation. Never assume "URL only" and proceed silently.
> If the user offers code / New Relic / GA4 / admin / infra access, then **request the specific
> artifacts** (repo path or git URL; the exact NRQL exports listed in 2.4; the GA4/admin reports) and
> **wait for them** before scoring those dimensions. Only proceed without a source after the user has
> explicitly said they will not provide it — and then mark it "Not assessed" and include the Data
> Request Pack so they can supply it for a v2.

Ask in plain text:
1. **Website URL** to audit.
2. **Brand / client name** (for the cover).
3. **Representative page URLs** (so the scan covers all key templates, not just the homepage):
   a **category / product-listing (PLP)** URL, a **product-detail (PDP)** URL, and the **cart** and
   **checkout** URLs (or search results). If they only give the homepage, proceed but ask for these
   the moment the homepage doesn't reveal PLP/PDP/cart behaviour.

Then use **AskUserQuestion**:

**A — "Which access can you provide?"** (multi-select): Code/repo · Backend/Magento admin ·
Analytics (GA4) · New Relic/APM · Server/infra · Only the public website.

**B — "What are your biggest priorities?"** (multi-select): Conversion & sales · Performance & speed ·
Security & stability · Operations & support · Growth & modernization.

Access answer → coverage & confidence. Priorities → what to lead with.

**After the access answer, explicitly follow up for each source the user selected:**
- *Code* → "Share the repo path or git URL (or run `! git clone <url>` here)."
- *New Relic* → paste the 4 NRQL exports in §2.4. *GA4* → the funnel/AOV/device exports.
- *Admin* → the Reports listed in §2.4. *Infra* → the `bin/magento` status + env.php settings.
Wait for these before scoring those dimensions. Do not generate the deck until the user has either
provided the access they offered or told you to proceed without it.

---

## STEP 2 — Gather evidence

### 2.1 Performance — ALWAYS measure (URL is enough)
Run Google PageSpeed Insights (public, no key needed) for the homepage AND the PLP/PDP, mobile + desktop:
```
URL="<page-url>"
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$URL&strategy=mobile&category=performance&category=accessibility&category=best-practices&category=seo" -o /tmp/psi_m.json
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$URL&strategy=desktop&category=performance" -o /tmp/psi_d.json
python3 - <<'PY'
import json
for f,lab in [("/tmp/psi_m.json","MOBILE"),("/tmp/psi_d.json","DESKTOP")]:
    d=json.load(open(f)); lh=d.get("lighthouseResult",{}); cat=lh.get("categories",{}); a=lh.get("audits",{})
    def s(k): 
        v=cat.get(k,{}).get("score"); return round(v*100) if v is not None else None
    print(lab,"Perf",s("performance"),"SEO",s("seo"),"A11y",s("accessibility"),"BestPr",s("best-practices"))
    for k in ["largest-contentful-paint","interactive","total-blocking-time","cumulative-layout-shift","speed-index","server-response-time"]:
        print("  ",k,a.get(k,{}).get("displayValue"))
    cx=d.get("loadingExperience",{}).get("metrics",{})
    if cx: print("  CrUX field:",{k:v.get("category") for k,v in cx.items()})
PY
```
Capture into `tech_snapshot.performance`: PSI Performance score (mobile + desktop), LCP, INP/TBT, CLS,
TTFB (server-response-time), Speed Index, and total page weight. Rate each: good / avg / poor
(PSI ≥90 good, 50–89 avg, <50 poor; LCP ≤2.5s good ≤4s avg; CLS ≤0.1 good ≤0.25 avg; INP ≤200ms good ≤500ms avg).

**If the keyless PSI call fails (HTTP 429 "Quota exceeded", or error)** — do NOT skip performance. Try in order:
1. Add a free API key: append `&key=<PSI_API_KEY>` to the URL (get one free at Google Cloud → enable
   "PageSpeed Insights API"). Ask the user for a key if they have one.
2. Run Lighthouse locally: `npx --yes lighthouse "<url>" --only-categories=performance --quiet --chrome-flags="--headless" --output=json --output-path=/tmp/lh.json` then read `categories.performance.score` and the same audits.
3. Ask the user to open **https://pagespeed.web.dev**, run their URL (mobile + desktop), and paste the
   scores + LCP/INP/CLS — give them this exact instruction.
4. Last resort: derive directional signals from the HTML (`curl -sL <url> -o /tmp/p.html`): total bytes,
   number of `<script>`/render-blocking tags, image formats (WebP/AVIF vs JPEG/PNG), lazy-loading, CDN
   usage — and mark `tech_snapshot.note` to say performance is *estimated* (lower confidence).

Always also `curl -sL <url> -o /tmp/p.html` and check image formats (WebP/AVIF), script count, render-blocking, lazy-loading, CDN.

**ALWAYS verify caching by BEHAVIOUR, never from the `cache-control` header.** A CDN (Fastly/Varnish)
commonly caches HTML via VCL/surrogate even when the origin sends `cache-control: no-store` - so seeing
`no-store` does NOT mean the page is uncached. Check the response headers for the real signal:
```
curl -sIL -A "Mozilla/5.0" "<home / PLP / PDP url>" | grep -iE "x-cache|^age:|x-served-by|surrogate|x-cache-hits|cache-control"
```
If you see `x-cache: HIT` with a non-trivial `age` (e.g. thousands of seconds), edge caching IS working -
record it as a STRENGTH (not a gap). Only flag a caching problem if cacheable page types show consistent
`MISS` / `age: 0` / pass-through. Cart & Checkout are correctly uncacheable - never flag those as a cache gap.

### 2.2 Security — ALWAYS check (URL is enough; deeper with code)
```
curl -sIL -A "Mozilla/5.0" "<url>" | grep -iE "strict-transport-security|content-security-policy|x-content-type-options|x-frame-options|referrer-policy|permissions-policy|set-cookie|server|x-magento"
```
Record into `tech_snapshot.security` (check / status / rating) for: **HTTPS+HSTS**, **CSP**,
**X-Content-Type-Options**, **X-Frame-Options/frame-ancestors**, **Referrer-Policy**, **Permissions-Policy**,
**cookies Secure/HttpOnly/SameSite**, **version/tech disclosure** (Server/X-Magento headers leaking version),
**TLS validity**. Passive only — do NOT brute-force admin paths or scan intrusively.
With **code access** also: detect Magento edition/version (`composer.json`, `bin/magento --version`),
**security patch level** (how many quarterly patches behind), run `composer audit` for vulnerable
dependencies, grep for hardcoded secrets/keys, check 2FA & admin-URL config, ACL/roles.
Flag known-CVE exposure for the detected version (verify against Adobe security bulletins).

### 2.3 Code (if provided)
Edition & version, custom-module count (`app/code/*`), overrides/preferences (`di.xml`), theme
(Luma/PWA/headless), third-party extensions (`composer.lock`), app mode, indexer/cron config, core hacks.

### 2.4 Missing access → output a DATA REQUEST PACK (do not skip)
If admin / analytics / New Relic / infra were NOT provided, do not silently drop those areas. Instead,
**give the user exact retrieval steps + an example output template** so they can fetch real data. Examples:

**New Relic** — "Open New Relic → Query your data → run, paste results back as a table:"
- `SELECT count(*), percentile(duration,50,95,99) FROM Transaction FACET name SINCE 14 days ago`
- Slow crons: `SELECT count(*), average(duration), max(duration), sum(duration) FROM Transaction WHERE transactionType='Other' FACET name SINCE 7 days ago`
- CWV (RUM): `SELECT percentile(largestContentfulPaint,75), percentile(interactionToNextPaint,75), percentile(cumulativeLayoutShift,75) FROM PageViewTiming SINCE 14 days ago`
- Errors: `SELECT count(*) FROM TransactionError FACET error.message SINCE 14 days ago`
- *Example to paste:* `| name | p50 | p95 | p99 | count |` … rows.

**GA4** — "Reports → Monetization → Ecommerce purchases (AOV, revenue); Explore → Funnel exploration
with steps session_start → view_item → add_to_cart → begin_checkout → purchase (export drop-off %);
Reports → Tech → Device for CR by device; Reports → Acquisition for channel mix. Date range: last 90 days."
- *Example to paste:* `| step | users | drop-off % |` … and `Mobile CR %, Desktop CR %, AOV`.

**Magento admin** — "Reports → Products Ordered (category/product revenue); Reports → Sales → Orders
(orders, AOV); Marketing → Cart Price Rules (active promos); Reports → Abandoned Carts; Stores →
Configuration for payment/shipping/checkout setup. Export CSV or screenshot."

**Server / infra** — "Run & paste: `bin/magento cache:status`, `bin/magento indexer:status`,
`bin/magento cron:status` (or crontab), Redis/Varnish/search settings from `app/etc/env.php`,
and your backup + DR policy (frequency, last restore test, RTO/RPO)."

Put each requested-but-missing item in the deck's coverage slide as **Not assessed**, and include the
Data Request Pack in your message so the team can fill the gaps for a v2.

---

## STEP 3 — Score, capture findings, and build opportunities

### Five dimensions & checklists
1. **Business & Conversion:** funnel, add-to-cart, checkout completion/drop-off, abandonment, repeat
   purchase, AOV, category revenue, promo usage/margin, mobile vs desktop, peak-season, analytics integrity.
2. **CX & Merchandising:** homepage clarity, taxonomy, search relevance & zero-results, filters, sort,
   PDP depth, images/zoom/video, delivery/returns messaging, trust signals, upsell/cross-sell, wishlist,
   guest checkout, **accessibility (WCAG 2.1 AA)**, mobile UX, localization/multi-store.
3. **Technology & Platform Health:** edition/version + **EOL/support**, **security patch level**,
   custom-module count/quality, overrides/core hacks, theme complexity, extension risk,
   **Core Web Vitals + PSI scores (measured in 2.1)**, Varnish/Redis caching, Elasticsearch/OpenSearch,
   indexers, RabbitMQ/cron, DB health, API/integration latency, composer/deploy, app mode,
   **SEO technical** (structured data, canonicals, hreflang, sitemap, redirects),
   **security (measured in 2.2)**, CDN/image optimization, infra scalability.
4. **Operations & Risk:** exception trends, uptime/alerting, backup frequency + **restore testing**,
   **DR (RTO/RPO)**, deploy process, rollback, incident history, recurring-issue ownership, ticket
   patterns, **key-person/single-vendor dependency**, **data privacy & compliance** (GDPR/local PDP law,
   cookie consent, retention).
5. **Growth & Value-Add:** see the Opportunity Library below.

### Scoring & 2×2
Per dimension 1–5 (1 critical … 5 strong). Optional overall = avg (weighted: Bus 25/CX 25/Tech 20/Ops 15/Growth 15).
Set each dimension's **confidence** (High/Medium/Low) from access. Tag findings Risk·Effort·Impact for the
matrix: High-impact+Low-effort=Do first · High+High=Plan next · Low+Low=Quick win · Low+High=Deprioritize.

### Findings fields
`id, title, category, current_state, business_impact, evidence, recommendation, effort, priority, risk, impact, owner, expected_outcome, confidence`.

### Value-Add Opportunity Library (be RICH, not basic)
Work through EVERY item below and recommend all that fit the brand AND are confirmed not already live (see
Validation). Aim for a substantial set (typically 8-12 opportunities), not 2-3 - this is the growth story.
**MANDATORY: every opportunity must state its business value** in `business_impact` + `expected_outcome`
(revenue / conversion / AOV / retention / cost / risk) - never list a feature without why it matters.
If most of the library is already live, say so and pivot to *enhancing* what exists (basic related-products
-> AI personalization; keyword search -> semantic) plus platform/perf/SEO/accessibility - keep it rich.
- **Conversion / payments:** Express / one-click checkout (Midtrans Snap / Xendit / GoKwik-style, bypass checkout page);
  local payment-first (UPI; GoPay/OVO/DANA/ShopeePay/QRIS; wallets); BNPL / EMI; Login with OTP + Google One Tap / social login; guest-checkout optimization.
- **Discovery / merchandising:** AI / semantic / typo-tolerant search; AI product recommendations & personalization;
  shoppable Look Book; product bundles; size/fit finder; ratings, reviews & UGC; wishlist / save-for-later; shoppable Instagram feed & social proof.
- **Premium / brand:** product customizer (e.g. "By You"); AR virtual try-on.
- **Retention / revenue:** gift cards (purchase + redemption); loyalty / rewards; subscriptions / replenishment;
  automated returns & exchange (OMS/ERP integrated, real-time, auto-refund); verified-group discounts (student / teacher / healthcare / military).
- **Engagement / channels:** WhatsApp commerce & re-engagement (cart recovery, order/restock alerts);
  live / social commerce (TikTok Shop, livestream); AI chatbot / shopping assistant.
- **Platform / ops:** performance & CWV programme; accessibility remediation; headless / PWA; better analytics & event tracking;
  CRO experiment backlog; ops & merchandising automation; modern payment orchestration.

### VALIDATION (mandatory before recommending anything)
For every opportunity you intend to suggest, first confirm it is **NOT already live**:
- Scan the homepage + PLP/PDP/cart/checkout/footer/search and the code (if available) for the feature
  (e.g. don't suggest "add wishlist" if a wishlist exists; don't suggest "add reviews" if PDP shows reviews;
  don't suggest "express checkout" if checkout is already one-step).
- Only list **confirmed gaps**. In each opportunity's `evidence`, note how you validated
  (e.g. "No wishlist control found on PDP/header as of <date>"). If you can't verify from available pages,
  mark `confidence: Low` and ask for the relevant URL rather than assuming.
- Validate by exact module name + live site, not loose grep (e.g. "customiz" matches "customer").

### ALWAYS-INCLUDE rules
- **Accessibility:** always run an accessibility pass and surface it as **named CX findings with specifics**
  (pinch-zoom disabled, missing alt text, unlabeled icon controls, contrast, heading order) - never omit it,
  even on a URL-only audit. Tie to business value (reach, SEO, legal/compliance).
- **Analytics integrity (when GA4/admin given):** verify ecommerce events actually fire. If purchase/revenue
  or checkout-step events are missing (e.g. item revenue = 0, checkout steps show 0%), that is a HIGH finding
  in Business & Conversion - the client cannot measure money. Report it explicitly.
- **Empty-state honesty:** if a dimension has too little data to give insight, set `"not_assessed": true`,
  set `confidence` to Low/"Not assessed", and write a `summary` that states exactly what is missing. The deck
  will render a clear "INSUFFICIENT DATA - this slide can be ignored" notice instead of a hollow table. Never
  ship a near-empty slide that implies analysis was done. Phrase a missing source as **"data / access not
  provided"** (and include it in the Data Request Pack) - do NOT say "out of scope".

### Expected outcomes - REALISTIC, range-based, project-specific (REQUIRED)
Clients only approve work when they see where it lands. So for performance/conversion fixes, give the
**expected result as a RANGE tied to the measured baseline** - never a fantasy single number.
- **Be realistic.** A 7s uncacheable checkout realistically reaches ~2.5-4.5s, NOT "<1s". Uncacheable
  pages (cart/checkout/account) can never hit cached-page speeds - keep targets honest.
- **Calibrate headroom to the project.** If FPC/CDN cache is already working, gains are modest (tune the
  uncached/uncacheable path). If there is NO cache/CDN, the gains are large - you can project bigger
  improvements (e.g. category 8s -> <0.5s once FPC is added). Always base the target on what you measured.
- **Stage it** (Sprint 1 / Sprint 2 / all-sprints) where useful, and state the basis/assumption.
- Provide a `perf_outcomes` array where each row is traceable end-to-end:
  `[{"metric","current","target","tasks","verify"}]` -
  `current` = the measured value + the TOOL it came from (e.g. "6.31 s (New Relic)"),
  `target` = a realistic RANGE, `tasks` = the specific work that delivers it (link to the engineering
  sprints), `verify` = the tool/metric that will confirm it (New Relic transaction/Apdex, staging
  profiler, Lighthouse, EXPLAIN). The deck renders an "Expected outcomes" slide with columns
  Metric | Current | Expected | Key tasks | Verify in. Keep every finding's `expected_outcome` realistic too.

### Competitive benchmark (vs category peers - REQUIRED)
Benchmark the site against 3-4 well-known competitors **in the same vertical**, auto-selected from the brand's
category (detect it from the catalogue/nav):
- Footwear / sportswear -> Nike, Adidas, Puma, New Balance
- Fashion / apparel -> Zara, H&M, Uniqlo, Mango
- Luxury / premium -> the relevant luxury houses for that segment
- Jewelry -> Pandora, Tiffany, Swarovski, Mejuri
- Beauty -> Sephora, Sephora-tier peers; Electronics -> category leaders; etc.
Pick peers that match the brand's tier (premium vs mass) and region where possible. Benchmark URL-observable
commerce features & experience (reviews, video, express checkout, customizer, AR, loyalty, BNPL, search,
gift cards, accessibility, performance). **Competitor sites usually block crawling / are JS-rendered**, so this
is an *indicative* benchmark: use spot-checks where reachable + well-established public capability otherwise,
and set `benchmark.note` to say so and that figures should be validated before external quoting. The SELF
column is the audited truth; color it green for strengths, red for gaps. Put it in `audit_data.json` as:
```json
"benchmark": {
  "category": "Premium lifestyle footwear & sportswear",
  "note": "Indicative benchmark vs category peers - validate before external use.",
  "peers": ["Nike","Adidas","Puma"],
  "rows": [
    {"feature":"PDP ratings & reviews","self":"No","peers":["No","Yes","Yes"]},
    {"feature":"Loyalty / membership","self":"Yes (MAPCLUB)","peers":["Yes","Yes","Yes"]}
  ]
}
```

### Coverage rule (mandatory on deck)
Full primary access → High confidence; indirect signals → Medium; no access → Low / Not assessed (state it).

---

## STEP 4 — Write `audit_data.json`

Use this shape (note the new `tech_snapshot`):
```json
{
  "meta": {"client":"","site_url":"","platform":"","audit_date":"YYYY-MM-DD","auditor":"","overall_score":3.0},
  "summary": "2–3 line executive summary.",
  "coverage": [
    {"source":"Public website URL","available":true,"confidence":"High","note":"Homepage + PLP + PDP scanned"},
    {"source":"Code / repo access","available":false,"confidence":"Low","note":"not provided"},
    {"source":"Backend / admin","available":false,"confidence":"Low","note":"data requested - see pack"},
    {"source":"Analytics (GA4)","available":false,"confidence":"Low","note":"data requested - see pack"},
    {"source":"New Relic / APM","available":false,"confidence":"Low","note":"data requested - see pack"},
    {"source":"Server / infra","available":false,"confidence":"Low","note":"data requested - see pack"}
  ],
  "tech_snapshot": {
    "note": "Measured via PageSpeed Insights + response headers on <date>.",
    "performance": [
      {"label":"PSI Performance (Mobile)","value":"42","rating":"poor"},
      {"label":"PSI Performance (Desktop)","value":"78","rating":"avg"},
      {"label":"LCP (mobile)","value":"4.1 s","rating":"poor"},
      {"label":"INP / TBT","value":"260 ms","rating":"avg"},
      {"label":"CLS","value":"0.04","rating":"good"},
      {"label":"TTFB","value":"0.9 s","rating":"avg"}
    ],
    "security": [
      {"check":"HTTPS + HSTS","status":"Missing HSTS","rating":"poor"},
      {"check":"Content-Security-Policy","status":"Absent","rating":"poor"},
      {"check":"X-Content-Type-Options","status":"nosniff","rating":"good"},
      {"check":"X-Frame-Options","status":"SAMEORIGIN","rating":"good"},
      {"check":"Cookies Secure/HttpOnly","status":"Partial","rating":"avg"},
      {"check":"Version disclosure","status":"Magento version leaked in headers","rating":"avg"}
    ]
  },
  "dimensions": [
    {"name":"Business & Conversion","score":3,"confidence":"Medium","summary":"","findings":[]},
    {"name":"Customer Experience & Merchandising","score":3,"confidence":"High","summary":"","findings":[]},
    {"name":"Technology & Platform Health","score":3,"confidence":"High","summary":"","findings":[]},
    {"name":"Operations & Risk","score":3,"confidence":"Low","summary":"","findings":[]},
    {"name":"Growth & Value-Add Opportunities","score":3,"confidence":"Medium","summary":"","findings":[]}
  ],
  "top_risks":[{"title":"","impact":""}],
  "top_blockers":[{"title":"","impact":""}],
  "top_opportunities":[{"title":"","impact":""}],
  "quick_wins":["",""],
  "roadmap":[{"phase":"Wave 1 - Stabilise","effort":"Low-Med","items":["",""]}],
  "next_steps":["",""]
}
```
A finding object: `{"id":"TECH-01","title":"","category":"","current_state":"","business_impact":"","evidence":"","recommendation":"","effort":"Medium","priority":"High","risk":"High","impact":"High","owner":"","expected_outcome":"","confidence":"High"}`.

---

## STEP 5 — Generate the PowerPoint
1. `python3 -c "import pptx" 2>/dev/null || pip install python-pptx`
2. **Ask the user which folder to save the deck to** — never default silently. Name the file
   `<Client> Audit - YYMMDD.pptx` (Iksula date-suffix convention; use `v2`/`v3` on same-day re-runs).
3. Run the shipped generator (it lives in this skill, no need to write it out):
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/magento2-audit/scripts/build_audit_ppt.py <audit_data.json> "<chosen-folder>/<Client> Audit - YYMMDD.pptx"`

The generator (`scripts/build_audit_ppt.py`) is brand-compliant by construction — Carlito + primary red `#9A0D15` + light cards.

Deck flow: Cover → Basis/coverage → Scorecard → **Performance & security snapshot** → Top 5 risks →
Top 5 conversion blockers → Top 5 opportunities → Impact/Effort matrix → per-dimension findings →
Quick wins vs roadmap → Next steps.

## STEP 6 — Report back
Give the file path + overall score, restate the **coverage basis** (High vs Low confidence dimensions),
and include the **Data Request Pack** for anything Not assessed so the team can produce a deeper v2.
Keep everything business-framed. State that effort bands assume Claude-assisted implementation.

---

## Conventions (do not remove)
- Brand: **Carlito**, primary red **`#9A0D15`**, light cards — for any deck/doc output. The shipped `scripts/build_audit_ppt.py` already enforces this.
- File naming: `<Client> Audit - YYMMDD.pptx` (`v2`/`v3` for same-day). **Ask the user which folder to save to** — never default.
- Use `${CLAUDE_PLUGIN_ROOT}` for intra-plugin paths (e.g. the deck generator at `${CLAUDE_PLUGIN_ROOT}/skills/magento2-audit/scripts/build_audit_ppt.py`).
- The full deck generator ships in `scripts/build_audit_ppt.py` — run it directly; do not paste it inline.
