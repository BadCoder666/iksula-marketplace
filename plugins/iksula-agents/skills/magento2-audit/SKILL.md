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
2. Write the **Appendix** Python block verbatim to `/tmp/build_audit_ppt.py`.
3. **Ask the user which folder to save the deck to** — never default silently. Name the file
   `<Client> Audit - YYMMDD.pptx` (Iksula date-suffix convention; use `v2`/`v3` on same-day re-runs).
4. `python3 /tmp/build_audit_ppt.py <audit_data.json> "<chosen-folder>/<Client> Audit - YYMMDD.pptx"`

The deck is brand-compliant by construction (the Appendix generator uses Carlito + primary red `#9A0D15` + light cards).

Deck flow: Cover → Basis/coverage → Scorecard → **Performance & security snapshot** → Top 5 risks →
Top 5 conversion blockers → Top 5 opportunities → Impact/Effort matrix → per-dimension findings →
Quick wins vs roadmap → Next steps.

## STEP 6 — Report back
Give the file path + overall score, restate the **coverage basis** (High vs Low confidence dimensions),
and include the **Data Request Pack** for anything Not assessed so the team can produce a deeper v2.
Keep everything business-framed. State that effort bands assume Claude-assisted implementation.

---

## APPENDIX — PPT generator (write verbatim to /tmp/build_audit_ppt.py)

```python
#!/usr/bin/env python3
import sys, json, os, re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

INK=RGBColor(0x15,0x15,0x18); RED=RGBColor(0x9A,0x0D,0x15); WHITE=RGBColor(0xFF,0xFF,0xFF)
LGRAY=RGBColor(0xF4,0xF4,0xF6); MGRAY=RGBColor(0x5E,0x5E,0x66); HAIR=RGBColor(0xDD,0xDD,0xE2)
AMBER=RGBColor(0xD9,0x8A,0x1F); GREEN=RGBColor(0x2E,0x7D,0x32); FONT="Carlito"

def score_color(s):
    try: s=float(s)
    except: return MGRAY
    return RED if s<=2 else (AMBER if s<3.5 else GREEN)
def rating_color(r): return {"good":GREEN,"avg":AMBER,"poor":RED}.get(str(r).strip().lower(),MGRAY)
def pcolor(v): return {"high":RED,"medium":AMBER,"low":MGRAY}.get(str(v).strip().lower(),MGRAY)
def lat_color(v):
    m=re.search(r'([\d.]+)',str(v)); s='s' in str(v).lower()
    if not m: return MGRAY
    x=float(m.group(1))
    if s and x>=10: return RED
    if s and x>=3: return AMBER
    return GREEN
def apdex_color(v):
    try: x=float(re.search(r'([\d.]+)',str(v)).group(1))
    except: return MGRAY
    return RED if x<0.5 else (AMBER if x<0.85 else GREEN)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height; BLANK=prs.slide_layouts[6]
data=json.load(open(sys.argv[1],encoding="utf-8")); meta=data.get("meta",{}); dims=data.get("dimensions",[])
out=sys.argv[2] if len(sys.argv)>2 else os.path.splitext(sys.argv[1])[0]+".pptx"
CLIENT=meta.get("client","Audit"); PAGE=[0]
ML=Inches(0.62); CW=Inches(12.1)   # left margin, content width

def slide(): return prs.slides.add_slide(BLANK)
def rect(s,x,y,w,h,fill=None,line=None,shape=MSO_SHAPE.RECTANGLE):
    sp=s.shapes.add_shape(shape,x,y,w,h); sp.shadow.inherit=False
    if fill is None: sp.fill.background()
    else: sp.fill.solid(); sp.fill.fore_color.rgb=fill
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(1)
    return sp
def tbox(s,x,y,w,h,anchor=MSO_ANCHOR.TOP):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    tf.margin_left=0;tf.margin_right=0;tf.margin_top=0;tf.margin_bottom=0; return tf
def _nb(p): p._p.get_or_add_pPr().append(p._p.get_or_add_pPr().makeelement(qn('a:buNone'),{}))
def _bu(p,c):
    pPr=p._p.get_or_add_pPr()
    pPr.insert(0,pPr.makeelement(qn('a:buChar'),{'char':'•'}))
    pPr.insert(0,pPr.makeelement(qn('a:buFont'),{'typeface':'Carlito'}))
    cl=pPr.makeelement(qn('a:buClr'),{}); cl.append(cl.makeelement(qn('a:srgbClr'),{'val':'%02X%02X%02X'%(c[0],c[1],c[2])})); pPr.insert(0,cl)
def para(tf,text,size,color=INK,bold=False,first=False,align=PP_ALIGN.LEFT,sa=6,italic=False,bullet=False,spc=None):
    p=tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment=align; p.space_after=Pt(sa); p.space_before=Pt(0)
    if spc is not None: p.line_spacing=spc
    r=p.add_run(); r.text=str(text); f=r.font; f.name=FONT; f.size=Pt(size); f.bold=bold; f.italic=italic; f.color.rgb=color
    _bu(p,color) if bullet else _nb(p); return p
def chip(s,x,y,w,text,fill,fg=WHITE,size=10):
    c=rect(s,x,y,w,Inches(0.32),fill=fill,shape=MSO_SHAPE.ROUNDED_RECTANGLE); c.adjustments[0]=0.5
    tf=c.text_frame; tf.word_wrap=False
    tf.margin_left=Pt(7);tf.margin_right=Pt(7);tf.margin_top=Pt(0);tf.margin_bottom=Pt(0)
    p=tf.paragraphs[0]; p.alignment=PP_ALIGN.CENTER
    r=p.add_run(); r.text=str(text); r.font.name=FONT; r.font.size=Pt(size); r.font.bold=True; r.font.color.rgb=fg
    return c
def footer(s):
    PAGE[0]+=1
    rect(s,ML,Inches(7.06),CW,Pt(0.75),fill=HAIR)
    para(tbox(s,ML,Inches(7.12),Inches(9),Inches(0.3)),CLIENT+"   |   E-commerce Audit   |   Confidential",8.5,MGRAY,first=True)
    para(tbox(s,Inches(10.0),Inches(7.12),Inches(2.73),Inches(0.3)),str(PAGE[0]),8.5,MGRAY,first=True,align=PP_ALIGN.RIGHT)
def H(s,kicker,title,sub=None):
    rect(s,0,0,SW,Inches(1.28),fill=INK); rect(s,0,Inches(1.28),SW,Inches(0.05),fill=RED)
    para(tbox(s,ML,Inches(0.26),CW,Inches(0.3)),kicker.upper(),12,RED,bold=True,first=True)
    para(tbox(s,ML,Inches(0.57),CW,Inches(0.62)),title,26,WHITE,bold=True,first=True)
    footer(s)
    if sub: para(tbox(s,ML,Inches(1.46),CW,Inches(0.6)),sub,12,MGRAY,first=True)
    return Inches(1.46) if not sub else Inches(2.05)

# ---------- table helper (striped, padded, readable) ----------
def table(s,x,y,w,colw,rows,header_h=0.46,row_h=0.4,fs=10.5,hfs=10):
    nC=len(colw); nR=len(rows)
    t=s.shapes.add_table(nR,nC,x,y,w,Inches(header_h+row_h*(nR-1))).table
    t._tbl.tblPr.set('firstRow','0'); t._tbl.tblPr.set('bandRow','0')
    for i,cw in enumerate(colw): t.columns[i].width=cw
    t.rows[0].height=Inches(header_h)
    for ri in range(1,nR): t.rows[ri].height=Inches(row_h)
    return t
def cell(c,blocks,fill,va=MSO_ANCHOR.MIDDLE):
    c.margin_left=Inches(0.1);c.margin_right=Inches(0.08);c.margin_top=Inches(0.05);c.margin_bottom=Inches(0.05)
    c.vertical_anchor=va; c.fill.solid(); c.fill.fore_color.rgb=fill
    tf=c.text_frame; tf.word_wrap=True
    for i,b in enumerate(blocks):
        txt,sz,col,bold,al=b[0],b[1],b[2],b[3],(b[4] if len(b)>4 else PP_ALIGN.LEFT)
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=al; p.space_after=Pt(2); p.space_before=Pt(0)
        r=p.add_run(); r.text=str(txt); f=r.font; f.name=FONT; f.size=Pt(sz); f.bold=bold; f.color.rgb=col
        _nb(p)

# ============================== 1. COVER ==============================
s=slide(); rect(s,0,0,SW,SH,fill=INK)
rect(s,ML,Inches(2.05),Inches(0.85),Inches(0.09),fill=RED)
para(tbox(s,ML,Inches(0.85),CW,Inches(0.4)),"E-COMMERCE PLATFORM AUDIT",14,RED,bold=True,first=True)
para(tbox(s,ML,Inches(2.4),CW,Inches(1.3)),CLIENT,46,WHITE,bold=True,first=True,sa=2)
para(tbox(s,ML,Inches(3.55),CW,Inches(0.5)),meta.get("site_url",""),20,RGBColor(0xC8,0xC8,0xD0))
tf=tbox(s,ML,Inches(5.5),CW,Inches(1.4))
para(tf,"Platform:  "+meta.get("platform","-"),14,RGBColor(0xC8,0xC8,0xD0),first=True,sa=6)
para(tf,"Date:  "+meta.get("audit_date","")+("      Prepared by:  "+meta.get("auditor","") if meta.get("auditor") else ""),13,MGRAY)

# ============================== 2. COVERAGE ==============================
s=slide(); H(s,"01  Basis of audit","Coverage & confidence",
  "The audit depth matches the access provided. Items without access are marked Not assessed - never assumed.")
cov=data.get("coverage",[])
rows=[["ACCESS SOURCE","AVAILABLE","CONFIDENCE","NOTES"]]+[[c.get("source",""),"Yes" if c.get("available") else "No",c.get("confidence","-"),c.get("note","")] for c in cov]
t=table(s,ML,Inches(2.35),CW,[Inches(3.0),Inches(1.5),Inches(1.9),Inches(5.7)],rows,row_h=0.62)
for ri,row in enumerate(rows):
    for ci,val in enumerate(row):
        if ri==0: cell(t.cell(ri,ci),[(val,10,WHITE,True)],INK)
        else:
            fl=WHITE if ri%2 else LGRAY
            if ci==1: cell(t.cell(ri,ci),[(val,11,GREEN if val=="Yes" else RED,True,PP_ALIGN.CENTER)],fl)
            elif ci==2: cell(t.cell(ri,ci),[(val,11,score_color({"high":4,"medium":3,"low":1}.get(str(val).lower(),3)),True,PP_ALIGN.CENTER)],fl)
            elif ci==0: cell(t.cell(ri,ci),[(val,11,INK,True)],fl)
            else: cell(t.cell(ri,ci),[(val,9.5,MGRAY,False)],fl)

# ============================== 3. SCORECARD ==============================
s=slide(); H(s,"02  Executive summary","Maturity scorecard")
scs=[d.get("score") for d in dims if isinstance(d.get("score"),(int,float))]
overall=meta.get("overall_score") or (round(sum(scs)/len(scs),1) if scs else None)
summ=data.get("summary") or meta.get("summary")
if summ: para(tbox(s,ML,Inches(1.5),Inches(9.2),Inches(1.45)),summ,11.5,MGRAY,first=True,spc=1.15)
if overall is not None:
    rect(s,Inches(10.1),Inches(1.5),Inches(2.62),Inches(1.5),fill=INK)
    para(tbox(s,Inches(10.1),Inches(1.66),Inches(2.62),Inches(0.3)),"OVERALL MATURITY",10,RED,bold=True,first=True,align=PP_ALIGN.CENTER)
    para(tbox(s,Inches(10.1),Inches(1.98),Inches(2.62),Inches(0.9),MSO_ANCHOR.MIDDLE),str(overall)+" / 5",32,score_color(overall),bold=True,first=True,align=PP_ALIGN.CENTER)
by=Inches(3.35); bh=Inches(0.5); gap=Inches(0.28)
for i,d in enumerate(dims):
    y=by+i*(bh+gap)
    para(tbox(s,ML,y-Inches(0.04),Inches(3.4),bh,MSO_ANCHOR.MIDDLE),str(i+1)+".  "+d.get('name',''),12,INK,bold=True,first=True)
    sc=d.get("score",0) or 0
    rect(s,Inches(4.2),y+Inches(0.06),Inches(6.6),Inches(0.34),fill=LGRAY)
    try: fr=max(0.0,min(1.0,float(sc)/5.0))
    except: fr=0
    if fr>0: rect(s,Inches(4.2),y+Inches(0.06),Inches(6.6*fr),Inches(0.34),fill=score_color(sc))
    para(tbox(s,Inches(10.95),y-Inches(0.04),Inches(0.7),bh,MSO_ANCHOR.MIDDLE),str(sc)+"/5",12,score_color(sc),bold=True,first=True)
    if d.get("confidence"): para(tbox(s,Inches(11.6),y-Inches(0.04),Inches(1.1),bh,MSO_ANCHOR.MIDDLE),str(d["confidence"]),8.5,MGRAY,first=True)
# legend
ly=Inches(6.6)
for j,(lab,c) in enumerate([("1-2  Critical/Weak",RED),("3  Acceptable",AMBER),("4-5  Good/Strong",GREEN)]):
    rect(s,ML+j*Inches(2.6),ly,Inches(0.22),Inches(0.22),fill=c)
    para(tbox(s,ML+j*Inches(2.6)+Inches(0.3),ly-Inches(0.02),Inches(2.3),Inches(0.3)),lab,9.5,MGRAY,first=True)

# ============================== 4. PLATFORM HEALTH ==============================
ts=data.get("tech_snapshot")
if ts:
    s=slide(); H(s,"03  Platform health","Performance & security snapshot", ts.get("note"))
    para(tbox(s,ML,Inches(2.25),Inches(6),Inches(0.3)),"PERFORMANCE",12,INK,bold=True,first=True)
    perf=ts.get("performance",[]); cw=Inches(2.9); ch=Inches(1.0); gx=Inches(0.16)
    for i,m in enumerate(perf[:8]):
        r=i//2; c=i%2; x=ML+c*(cw+gx); y=Inches(2.68)+r*(ch+Inches(0.16)); col=rating_color(m.get("rating"))
        rect(s,x,y,cw,ch,fill=LGRAY); rect(s,x,y,Inches(0.09),ch,fill=col)
        para(tbox(s,x+Inches(0.28),y+Inches(0.12),cw-Inches(0.4),Inches(0.35)),m.get("label",""),10,MGRAY,first=True)
        para(tbox(s,x+Inches(0.28),y+Inches(0.42),cw-Inches(0.4),Inches(0.5)),m.get("value",""),19,col,bold=True,first=True)
    sx=Inches(7.05)
    para(tbox(s,sx,Inches(2.25),Inches(5.4),Inches(0.3)),"SECURITY",12,INK,bold=True,first=True)
    sec=ts.get("security",[])
    rows=[["CHECK","STATUS"]]+[[x.get("check",""),x.get("status","")] for x in sec]
    t=table(s,sx,Inches(2.68),Inches(5.5),[Inches(2.7),Inches(2.8)],rows,row_h=0.52,header_h=0.42)
    for ri,row in enumerate(rows):
        for ci,val in enumerate(row):
            if ri==0: cell(t.cell(ri,ci),[(val,10,WHITE,True)],INK)
            else:
                fl=WHITE if ri%2 else LGRAY
                if ci==1: cell(t.cell(ri,ci),[(val,9.5,rating_color(sec[ri-1].get("rating")),True)],fl)
                else: cell(t.cell(ri,ci),[(val,10,INK,True)],fl)

# ============================== 5/6/7 TOP-5 ==============================
def top5(num,kicker,title,items,accent=RED):
    s=slide(); H(s,kicker,title)
    if not items: para(tbox(s,ML,Inches(1.7),CW,Inches(1)),"(none recorded)",13,MGRAY,first=True,italic=True); return
    y0=Inches(1.75); rh=Inches(0.98)
    for i,it in enumerate(items[:5]):
        y=y0+i*rh
        lead=it.get("title") if isinstance(it,dict) else str(it)
        body=(it.get("impact") or it.get("detail") or "") if isinstance(it,dict) else ""
        rect(s,ML,y,Inches(0.62),Inches(0.62),fill=INK)
        para(tbox(s,ML,y,Inches(0.62),Inches(0.62),MSO_ANCHOR.MIDDLE),str(i+1),22,WHITE,bold=True,first=True,align=PP_ALIGN.CENTER)
        para(tbox(s,Inches(1.45),y+Inches(0.02),Inches(11.2),Inches(0.45)),lead,15,INK,bold=True,first=True)
        if body: para(tbox(s,Inches(1.45),y+Inches(0.46),Inches(11.2),Inches(0.45)),body,11.5,MGRAY,first=True)
top5(5,"04  Key risks","Top 5 risks",data.get("top_risks",[]))
top5(6,"05  Conversion","Top 5 conversion blockers",data.get("top_blockers",[]))
top5(7,"06  Growth","Top 5 modernization opportunities",data.get("top_opportunities",[]))

# ============================== 9. DIMENSION FINDINGS ==============================
HDR=[("FINDING & CURRENT STATE",),("RECOMMENDATION",),("PRIORITY / IMPACT / EFFORT",)]
CW3=[Inches(5.1),Inches(4.4),Inches(2.6)]
for i,d in enumerate(dims):
    fs=d.get("findings",[])
    if d.get("not_assessed") or not fs:
        s=slide(); H(s,"Dimension "+str(i+1),d.get("name",""))
        if d.get("confidence"): chip(s,Inches(11.0),Inches(0.62),Inches(1.7),"Confidence: "+str(d["confidence"]),MGRAY)
        rect(s,ML,Inches(2.7),CW,Inches(2.0),fill=LGRAY); rect(s,ML,Inches(2.7),Inches(0.1),Inches(2.0),fill=RED)
        tf=tbox(s,Inches(1.1),Inches(3.0),Inches(10.6),Inches(1.5))
        para(tf,"INSUFFICIENT DATA - THIS SLIDE CAN BE IGNORED",15,RED,bold=True,first=True,sa=10)
        para(tf,d.get("summary") or "Not assessed. Provide the access on the Basis-of-audit slide to populate it.",13,MGRAY,spc=1.15)
        continue
    chunks=[fs[k:k+4] for k in range(0,len(fs),4)]
    for ci,chunk in enumerate(chunks):
        s=slide(); H(s,"Dimension "+str(i+1)+("  ·  cont." if ci else ""),d.get("name",""), d.get("summary") if ci==0 else None)
        sc=d.get("score","-")
        chip(s,Inches(9.5),Inches(0.62),Inches(1.0),str(sc)+"/5",score_color(sc) if sc!="-" else MGRAY)
        if d.get("confidence"): chip(s,Inches(10.65),Inches(0.62),Inches(2.05),"Confidence: "+str(d["confidence"]),MGRAY)
        y=Inches(2.25) if ci==0 and d.get("summary") else Inches(1.6)
        rows=[[h[0] for h in HDR]]
        for f in chunk:
            rows.append([f,None,None])  # placeholder; fill below
        t=table(s,ML,y,CW,CW3,rows,header_h=0.42,row_h=1.18 if (ci==0 and d.get("summary")) else 1.25)
        for ci2,h in enumerate(HDR): cell(t.cell(0,ci2),[(h[0],10,WHITE,True)],INK)
        for ri,f in enumerate(chunk,start=1):
            fl=WHITE if ri%2 else LGRAY
            cell(t.cell(ri,0),[ (f.get("title",""),11,INK,True), (f.get("current_state",""),9.5,MGRAY,False) ],fl,va=MSO_ANCHOR.TOP)
            cell(t.cell(ri,1),[ (f.get("recommendation",""),10,RGBColor(0x2A,0x2A,0x30),False) ],fl,va=MSO_ANCHOR.TOP)
            cell(t.cell(ri,2),[
                ("Priority:  "+str(f.get("priority","-")),9.5,pcolor(f.get("priority")),True),
                ("Impact:  "+str(f.get("impact","-")),9.5,INK,False),
                ("Effort:  "+str(f.get("effort","-")),9.5,MGRAY,False),
            ],fl,va=MSO_ANCHOR.TOP)

# ============================== 10. NEW RELIC SLOWEST TRANSACTIONS ==============================
tx=data.get("transactions")
if tx:
    s=slide(); H(s,"07  Performance evidence","Page performance (New Relic, production)",
      "Fastly cache serves ~80-85% of catalog in <0.3s. Apdex reflects uncached/first-hit + uncacheable pages (Cart/Checkout). Lower Apdex = more frustrated users.")
    rows=[["PAGE / TRANSACTION","MONTHLY","AVG LOAD","APDEX"]]+[[t.get("name",""),t.get("visits",t.get("count","-")),t.get("avg",t.get("p50","-")),str(t.get("apdex",t.get("p95","-")))] for t in tx]
    tb=table(s,ML,Inches(2.4),CW,[Inches(5.9),Inches(1.9),Inches(2.1),Inches(2.2)],rows,row_h=0.46,header_h=0.44)
    for ri,row in enumerate(rows):
        for ci,val in enumerate(row):
            if ri==0: cell(tb.cell(ri,ci),[(val,10,WHITE,True,PP_ALIGN.LEFT if ci==0 else PP_ALIGN.CENTER)],INK)
            else:
                fl=WHITE if ri%2 else LGRAY
                if ci==0: cell(tb.cell(ri,ci),[(val,10.5,INK,True)],fl)
                elif ci==3: cell(tb.cell(ri,ci),[(val,10.5,apdex_color(val),True,PP_ALIGN.CENTER)],fl)
                else: cell(tb.cell(ri,ci),[(val,10.5,MGRAY,False,PP_ALIGN.CENTER)],fl)

# ============================== 11. ENGINEERING PLAN (perf + code quality) ==============================
ep=data.get("engineering_plan")
if ep:
    s=slide(); H(s,"08  Engineering plan","Performance & code-quality tasks")
    n=len(ep[:3]); cw=Inches((12.1-(n-1)*0.25)/max(1,n))
    for i,sec in enumerate(ep[:3]):
        x=ML+i*(cw+Inches(0.25))
        rect(s,x,Inches(1.85),cw,Inches(4.8),fill=LGRAY); rect(s,x,Inches(1.85),cw,Inches(0.6),fill=INK)
        para(tbox(s,x+Inches(0.22),Inches(1.96),cw-Inches(0.4),Inches(0.4),MSO_ANCHOR.MIDDLE),sec.get("area",""),12.5,WHITE,bold=True,first=True)
        tf=tbox(s,x+Inches(0.28),Inches(2.65),cw-Inches(0.5),Inches(3.8))
        for j,it in enumerate(sec.get("items",[])): para(tf,it,11,INK,first=(j==0),bullet=True,sa=8,spc=1.05)

# ============================== 9b. EXPECTED OUTCOMES ==============================
po=data.get("perf_outcomes")
if po:
    s=slide(); H(s,"09  Expected outcomes","Projected result, the tasks that deliver it, and how to verify",
      "CURRENT measured in New Relic APM (production) + staging Magento profiler / Lighthouse. EXPECTED is a realistic range, achieved by the listed tasks, and confirmed in the named tool.")
    rows=[["METRIC / PAGE","CURRENT","EXPECTED","KEY TASKS (what delivers it)","VERIFY IN"]]+[[r.get("metric",""),r.get("current","-"),r.get("target","-"),r.get("tasks",r.get("note","")),r.get("verify","-")] for r in po[:8]]
    tb=table(s,ML,Inches(2.35),CW,[Inches(2.3),Inches(1.6),Inches(1.6),Inches(4.1),Inches(2.5)],rows,row_h=0.54,header_h=0.46)
    for ri,row in enumerate(rows):
        for ci,val in enumerate(row):
            if ri==0: cell(tb.cell(ri,ci),[(val,9,WHITE,True,PP_ALIGN.LEFT if ci in (0,3,4) else PP_ALIGN.CENTER)],INK)
            else:
                fl=WHITE if ri%2 else LGRAY
                if ci==0: cell(tb.cell(ri,ci),[(val,9.5,INK,True)],fl,va=MSO_ANCHOR.TOP)
                elif ci==1: cell(tb.cell(ri,ci),[(val,9.5,RED,True,PP_ALIGN.CENTER)],fl,va=MSO_ANCHOR.TOP)
                elif ci==2: cell(tb.cell(ri,ci),[(val,9.5,GREEN,True,PP_ALIGN.CENTER)],fl,va=MSO_ANCHOR.TOP)
                elif ci==3: cell(tb.cell(ri,ci),[(val,8.5,INK,False)],fl,va=MSO_ANCHOR.TOP)
                else: cell(tb.cell(ri,ci),[(val,8.5,MGRAY,False)],fl,va=MSO_ANCHOR.TOP)

# ============================== 12. ACTION PLAN ==============================
s=slide(); H(s,"10  Action plan","Quick wins vs roadmap")
qw=data.get("quick_wins",[]); rm=data.get("roadmap",[])
rect(s,ML,Inches(1.7),Inches(5.85),Inches(5.0),fill=LGRAY); rect(s,ML,Inches(1.7),Inches(5.85),Inches(0.55),fill=GREEN)
para(tbox(s,ML+Inches(0.25),Inches(1.8),Inches(5.4),Inches(0.4),MSO_ANCHOR.MIDDLE),"QUICK WINS",13,WHITE,bold=True,first=True)
tf=tbox(s,ML+Inches(0.3),Inches(2.45),Inches(5.3),Inches(4.0))
for j,it in enumerate(qw): para(tf,str(it),12,INK,first=(j==0),bullet=True,sa=10,spc=1.05)
rx=Inches(6.85)
rect(s,rx,Inches(1.7),Inches(5.85),Inches(5.0),fill=LGRAY); rect(s,rx,Inches(1.7),Inches(5.85),Inches(0.55),fill=RED)
para(tbox(s,rx+Inches(0.25),Inches(1.8),Inches(5.4),Inches(0.4),MSO_ANCHOR.MIDDLE),"ROADMAP",13,WHITE,bold=True,first=True)
tf=tbox(s,rx+Inches(0.3),Inches(2.45),Inches(5.3),Inches(4.0))
for j,ph in enumerate(rm):
    if isinstance(ph,dict):
        para(tf,ph.get("phase","")+("   ("+ph.get('effort')+")" if ph.get("effort") else ""),12,INK,bold=True,first=(j==0),sa=2,bullet=True)
        for it in ph.get("items",[]): para(tf,it,10.5,MGRAY,sa=2)
        para(tf," ",6,MGRAY,sa=2)
    else: para(tf,str(ph),12,INK,first=(j==0),bullet=True,sa=8)

# ============================== 13. BENCHMARK ==============================
bm=data.get("benchmark")
if bm and bm.get("rows"):
    s=slide(); H(s,"11  Competitive benchmark",bm.get("category","Category peers"), bm.get("note"))
    peers=bm.get("peers",[]); selfn=CLIENT.split(" - ")[0].split("(")[0].strip()[:14]
    hdr=["FEATURE / EXPERIENCE",selfn]+peers
    pw=Inches(round((12.1-3.8-1.9)/max(1,len(peers)),2)); widths=[Inches(3.8),Inches(1.9)]+[pw]*len(peers)
    rows=[hdr]+[[r.get("feature","")]+[r.get("self","")]+[str(x) for x in r.get("peers",[])] for r in bm["rows"]]
    tb=table(s,ML,Inches(2.5),CW,widths,rows,row_h=0.38,header_h=0.42)
    for ri,row in enumerate(rows):
        for ci,val in enumerate(row):
            if ri==0: cell(tb.cell(ri,ci),[(val,9.5,WHITE,True,PP_ALIGN.LEFT if ci==0 else PP_ALIGN.CENTER)],INK)
            else:
                fl=WHITE if ri%2 else LGRAY
                if ci==0: cell(tb.cell(ri,ci),[(val,9.5,INK,True)],fl)
                elif ci==1:
                    sv=str(val).strip().lower(); col=GREEN if sv.startswith(("yes","strong","best","good")) else (RED if sv.startswith(("no","broken","weak","absent","missing","none","off")) else INK)
                    cell(tb.cell(ri,ci),[(val,9.5,col,True,PP_ALIGN.CENTER)],fl)
                else: cell(tb.cell(ri,ci),[(val,9,MGRAY,False,PP_ALIGN.CENTER)],fl)

# ============================== 12. MATRIX (moved to bottom) ==============================
s=slide(); H(s,"12  Prioritisation","Impact vs Effort")
m=data.get("matrix")
if not m:
    m={"do_first":[],"plan_next":[],"quick_wins":[],"deprioritize":[]}
    for d in dims:
        for f in d.get("findings",[]):
            imp=str(f.get("impact","")).lower(); eff=str(f.get("effort","")).lower(); lbl=f.get("id") or f.get("title","")
            if imp=="high" and eff=="low": m["do_first"].append(lbl)
            elif imp=="high": m["plan_next"].append(lbl)
            elif eff=="low": m["quick_wins"].append(lbl)
            else: m["deprioritize"].append(lbl)
quad=[("DO FIRST","high impact / low effort","do_first",GREEN,ML,Inches(1.85)),
      ("PLAN NEXT","high impact / high effort","plan_next",AMBER,Inches(6.78),Inches(1.85)),
      ("QUICK WINS","low impact / low effort","quick_wins",INK,ML,Inches(4.5)),
      ("DEPRIORITISE","low impact / high effort","deprioritize",MGRAY,Inches(6.78),Inches(4.5))]
for lab,subl,key,col,x,y in quad:
    rect(s,x,y,Inches(5.95),Inches(2.5),fill=LGRAY); rect(s,x,y,Inches(5.95),Inches(0.5),fill=col)
    para(tbox(s,x+Inches(0.22),y+Inches(0.08),Inches(5.5),Inches(0.34),MSO_ANCHOR.MIDDLE),lab+"   -   "+subl,11.5,WHITE,bold=True,first=True)
    tf=tbox(s,x+Inches(0.3),y+Inches(0.62),Inches(5.4),Inches(1.8)); its=m.get(key,[])
    if not its: para(tf,"-",11,MGRAY,first=True)
    for j,it in enumerate(its[:7]): para(tf,str(it),11,INK,first=(j==0),bullet=True,sa=3)

# ============================== 14. CLOSE ==============================
s=slide(); rect(s,0,0,SW,SH,fill=INK); rect(s,ML,Inches(2.85),Inches(0.85),Inches(0.09),fill=RED)
para(tbox(s,ML,Inches(1.9),CW,Inches(0.9)),"Expected impact & next steps",36,WHITE,bold=True,first=True)
tf=tbox(s,ML,Inches(3.2),CW,Inches(3.2))
ns=data.get("next_steps")
if isinstance(ns,list):
    for j,it in enumerate(ns): para(tf,str(it),15,RGBColor(0xD0,0xD0,0xD6),first=(j==0),bullet=True,sa=12,spc=1.1)
elif ns: para(tf,str(ns),16,RGBColor(0xD0,0xD0,0xD6),first=True)

prs.save(out)
print("Saved:",out,"| slides:",len(prs.slides._sldIdLst))
```
