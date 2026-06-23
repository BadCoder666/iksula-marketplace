# prospect-outreach-research — Research method

The source map, the detection methods, the Sales Navigator method, and the confidence rules. Capture raw
(sources + URLs + access dates) **before** distilling; keep it local with the deliverable.

## Company basics
| Field | Where to look | Confidence note |
|-------|---------------|-----------------|
| Nature of business → vertical | Company site "about", the site's category nav; map to the **`method-vocab` / `vertical-mapping`** L1/L2/L3 labels | Use the shared rubric — don't invent labels |
| Key categories | Top-level site navigation / departments | Usually high |
| Public vs private limited | Company registry, "investors"/"about" page, news; suffix (Inc, plc, Pvt Ltd, GmbH) | High if a filing/registry confirms |
| Estimated revenue | Annual report / investor page (public cos); for private, reputable estimate sources, employee count + sector benchmarks | **Always an estimate** — give a range + source, or "not found". Never assert |
| News (last 12 mo) | News search, the company's press/newsroom, leadership posts | Date every item; prefer primary sources |

## Website / stack
- **eCommerce platform** — detect from page source signatures: cookies, asset paths, meta tags, JS
  globals (e.g. Shopify `cdn.shopify.com` / `Shopify.theme`; Magento/Adobe Commerce `Mage`/`/static/version`;
  Salesforce Commerce `demandware`/`/on/demandware`; SAP Commerce/Hybris; commercetools; BigCommerce;
  Shopware; custom). If the site is JavaScript-rendered and a plain fetch is thin, use the **browser**
  (Claude-in-Chrome) to load and read it. Report the signal you used. Mark "inconclusive" when signatures
  conflict.
- **PIM (Product Information Management)** — usually **not** visible on the storefront. Infer only from:
  job postings naming a PIM (Akeneo, Salsify, inriver, Pimcore, Stibo, Syndigo, SAP/Informatica), case
  studies, vendor logos/press, or partner directories. Most honest output is often **"unknown"**. Always
  flag confidence.
- **Approx. product count** — `sitemap.xml` product entries, the "all products" count, or summing category
  counts. Report as an approximation and say how it was derived.

## Prospect (LinkedIn Sales Navigator, paced)
Use the **logged-in Sales Navigator session** in the browser.
- **Role & responsibilities** — title, scope, tenure, prior roles from the lead page.
- **Online presence** — LinkedIn activity/posts; then X, Substack, YouTube via web search. **Published**
  articles are reachable; **comments** usually are not — say so rather than guessing.
- **Direct connect** — connection **degree** (1st/2nd/3rd) and **shared connections** (warm-intro paths).
- **Pacing/cap** — ≤10 profiles/run, pause between each. Public/professional only; no private detail.
- **Fallback** — if no browser session, use public web only and mark connection + activity "not available".

## Fit, angle & content
- Map needs → **named offers** in `solutions-catalogue` (never generic).
- Fit lens from `icp-audience`.
- **Content to forward** — pick real pieces from `voices` / recent content records relevant to the
  prospect's role and the company's situation.

## The 5 messages
Tune each to the person's role, a recent post or trigger, and any shared connection.
- **2 connect notes** — ≤300 characters each (LinkedIn connection-request limit). Short, specific, one hook.
- **2 warm InMails** — longer; lead with a shared connection / relevant content / a trigger event.
- **1 direct InMail** — longer; straight to the value/offer and a clear ask.
No fabricated familiarity; no claims that aren't supported by the research.

## Confidence rules
- Tag each finding: **confirmed** (primary source), **inferred** (signal-based, say the signal), or
  **not found**. Revenue is always a range/estimate. PIM is usually inferred or unknown.
- Never present an inference or a hoped-for fit as a confirmed fact (prospect-stage discipline).
- If a prospect clearly warrants deeper work, flag it for **`client-research`** rather than going deep here.
