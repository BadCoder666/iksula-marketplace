#!/usr/bin/env python3
"""Canonical Economic-Buyer mapping for the vertical process-mapping series.

Drop this into scripts/ and `from economic_buyer import economic_buyer, BUYER_FILL`.
Keeps buyer assignment consistent across every vertical workbook so the series
stays comparable and the Solution-Shortlist tab is sellable by buying centre.

Four buying centres (one buyer = one budget + one signature):
  CFO / Finance           - leakage recovery, working capital, statutory/close  (LAND, self-funding)
  COO / Operations        - cost-to-serve, fulfilment, planning, support, returns/trust
  CRO/CMO / Commercial    - revenue growth: search, content, pricing, retention, quoting
  CIO/CDO / Tech & Data   - shared horizontals (doc-extraction, NL-analytics, master-data)
"""

# colour band per buying centre (matches group-fill palette family)
BUYER_FILL = {
    "CFO / Finance":         "FCE4D6",
    "COO / Operations":      "E2EFDA",
    "CRO/CMO / Commercial":  "DDEBF7",
    "CIO/CDO / Tech & Data": "FFF2CC",
}

def economic_buyer(name, lever=""):
    """Map a solution to the single economic buyer who owns the budget & signature.
    Keyword-match on the solution name first; fall back to the value lever."""
    n = (name or "").lower()
    lev = (lever or "").lower()

    # CIO / tech horizontals (sold once, beneath everything)
    if any(k in n for k in ["doc-extraction platform", "nl-analytics", "nl analytics",
                            "master-data", "master data", "catalog spine", "taxonomy spine",
                            "config & address", "price spine", "unit-economics",
                            "cost-to-serve cockpit", "take-rate & subsidy", "profitability &",
                            "p&l & ", "mdm spine"]):
        return "CIO/CDO / Tech & Data"

    # CFO / finance (cash, margin recovery, statutory)
    if any(k in n for k in ["recovery", "leakage", "settlement", "cash application", "deduction",
                            "collections", "co-op", "rebate", "freight", "bank-charge",
                            "carrier-invoice", "fuel audit", "weight-dispute", "markdown",
                            "margin", "pos, payment", "scheme", "contract-price", "close",
                            "tax", "compliance & document", "compliance & tax", "itc",
                            "price-list"]):
        return "CFO / Finance"

    # CRO/CMO / commercial (growth, demand creation)
    if any(k in n for k in ["search", "content", "listing", "pdp", "retention", "lifecycle",
                            "next-best", "seller growth", "rfq-to-quote", "quote-analytics",
                            "repricing", "discovery", "creative", "semantic catalog",
                            "channel-shift", "growth copilot"]):
        return "CRO/CMO / Commercial"

    # COO / operations & supply chain (cost-to-serve, fulfilment, planning, support, returns/trust)
    if any(k in n for k in ["fulfilment", "last-mile", "logistics", "allocation", "edd",
                            "demand", "replenish", "inventory", "s&op", "dead-stock",
                            "order capture", "po-to-order", "tender", "onboarding",
                            "support agent", "support", "deflection", "wismo", "consumer care",
                            "customer-service", "customer service", "merchant", "returns",
                            "rto", "trust", "fraud", "chargeback", "exception", "ndr", "planner"]):
        return "COO / Operations"

    # fallback by value lever
    if lev in ("leakage recovery", "working capital", "risk/compliance", "risk / compliance"):
        return "CFO / Finance"
    if lev == "revenue growth":
        return "CRO/CMO / Commercial"
    if lev == "cost-to-serve":
        return "COO / Operations"
    return "COO / Operations"


# ---- Tab 6 build snippet (header now 12 columns; buyer inserted after Value Lever) ----
# SH = ["#","Solution","What it does","Functions served","Primary Value Lever",
#       "Economic Buyer","Archetype","Indic. Composite","Reuse","Productizable","Phase",
#       "Iksula rationale / GTM angle"]
# SW = [4,30,44,26,17,22,18,11,8,13,9,44]
# ... for each solution tuple (num,sol,what,served,lever,arch,comp,reuse,prod,phase,rat):
#     buyer = economic_buyer(sol, lever)
#     cell(ws6.cell(rr,5), lever, align="center")
#     cell(ws6.cell(rr,6), buyer, align="center", bold=True, fill=BUYER_FILL.get(buyer))
#     cell(ws6.cell(rr,7), arch, align="center")
#     cell(ws6.cell(rr,8), comp, align="center", bold=True)
#     cell(ws6.cell(rr,9), reuse, align="center", ...)
#     cell(ws6.cell(rr,10), prod, align="center")
#     cell(ws6.cell(rr,11), phase, align="center", bold=True, fill=PF.get(phase))
#     cell(ws6.cell(rr,12), rat)
# ws6.auto_filter.ref = f"A1:L{rr-1}"

if __name__ == "__main__":
    tests = [
        ("Scheme Claim-Leakage Engine", "Leakage Recovery"),
        ("Cash Application & Deductions Engine", "Working Capital"),
        ("Search & Discovery Intelligence", "Revenue Growth"),
        ("Support & WISMO Agent", "Cost-to-Serve"),
        ("Doc-Extraction Platform (horizontal)", "Cost-to-Serve"),
        ("NL-Analytics & GTN Insight", "Revenue Growth"),
        ("Master-Data Spine", "Cost-to-Serve"),
        ("Fulfilment & Last-mile Optimiser", "Cost-to-Serve"),
    ]
    for nm, lev in tests:
        print(f"{nm:42} [{lev:16}] -> {economic_buyer(nm, lev)}")
