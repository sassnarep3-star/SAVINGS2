#!/usr/bin/env python3
"""
Unify data/banks.json with the newly verified official primary sources from session-1024a045:
- Chase Rate Sheet PDF (rdin1.pdf, effective 2026-10-16: 0.01% APY on Chase Savings, 0.02% on Premier/Private Client) + $100/$200 bonus
- Bank of America Personal Schedule of Fees (effective 2026-08-07: $100 min open, $8 monthly fee, $10 withdrawal limit fee >6/cycle, BofA Rewards transition)
- Citibank Simplified Banking Fact Sheet (effective 2026-10-01: $0 min open, $4.50 monthly fee waived at $500 AMB, promotional rate feature discontinued 2026-10-23)
- Wells Fargo Savings Rates (effective 2026-10-07 for 0.01% Way2Save and 3.25% New Customer Platinum Savings on >=$25k)
- Capital One 360 Application Rate Table (apply.capitalone.com/fc/index.html: 3.20% APY as of 2026-10-21, while keeping the NaN APY marketing page flag)
- PNC High Yield Savings Fee Schedule PDF ($0 min open, $0 monthly fee)
- Synchrony Bank High Yield Savings (3.55% APY as of 2026-10-21)
- BMO Alto Online Savings (3.00% APY as of 2026-10-21)
- U.S. Bank Elite Money Market (3.40% APY on >=$25k for new clients as of 2026-10-21)
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANKS_PATH = ROOT / "data" / "banks.json"

data = json.loads(BANKS_PATH.read_text(encoding="utf-8"))
data["meta"]["federal_reserve_effr"] = 3.88
data["meta"]["federal_reserve_effr_as_of"] = "2026-10-19"
data["meta"]["federal_reserve_target_range"] = "3.75% - 4.00%"
data["meta"]["federal_reserve_source"] = "https://www.federalreserve.gov/releases/h15/"

by_id = {p["id"]: p for p in data["products"]}

# 1. Update Chase Savings
chase = by_id["chase-savings"]
chase["apy_status"] = "verified"
chase["apy_as_of"] = "2026-10-16"
chase["tiers"] = [
    {"min": 0, "apy": 0.01, "condition": "All balance tiers ($0–$9,999; $10,000–$24,999; $25,000–$49,999; $50,000+)"}
]
chase["apy_note"] = (
    "0.01% interest rate / 0.01% APY across all balance tiers, verified from Chase's official Consumer Deposit Rates sheet "
    "(rdin1.pdf, effective 2026-10-16). Chase Premier Savings and Chase Private Client Savings pay 0.01% standard / 0.02% relationship APY."
)
chase["bonus"] = (
    "Up to $200 New Chase Savings Customer Bonus: Earn $100 when depositing $5,000–$9,999.99 or $200 when depositing $10,000+ "
    "in new money within 30 days and maintaining for 90 days (offer expires 2027-01-27)."
)
chase["bonus_source"] = "https://account.chase.com/consumer/banking/savingsoffer"
chase["sources"]["rates"] = "https://www.chase.com/content/dam/chase-ux/ratesheets/pdfs/rdin1.pdf"
chase["flags"] = [
    "Interactive HTML rate page (chase.com/personal/savings/savings-account/interest-rates) is ZIP-gated, but official Chase rate sheet PDF (rdin1.pdf, effective 2026-10-16) confirms 0.01% APY.",
    "On the Chase Savings bonus offer page (account.chase.com/consumer/banking/savingsoffer), the footnote omits the numeric APY ('effective as of 09/18/2026, is  for all balances')."
]

# 2. Update Bank of America Advantage Savings
bofa = by_id["bofa-advantage-savings"]
bofa["min_open"] = 100
bofa["min_open_note"] = "$100.00 minimum amount to open (verified in Personal Schedule of Fees, effective August 7, 2026)."
bofa["monthly_fee"] = 8
bofa["fee_note"] = (
    "$8.00 monthly maintenance fee, waived for the first 6 months on new accounts; thereafter waived with $500+ minimum daily balance, "
    "linked Advantage Relationship Banking/Checking, enrollment in Preferred Rewards / BofA Rewards™, or owner under age 25."
)
bofa["withdrawal_note"] = "6 free withdrawals/transfers per monthly statement cycle; $10.00 Withdrawal Limit Fee for each additional withdrawal."
bofa["sources"]["rates"] = "https://www.bankofamerica.com/salesservices/deposits/resources/personal-schedule-fees/"
bofa["flags"] = [
    "Consumer APY is ZIP-gated on the web page (Business Advantage Savings publishes 0.01% standard / 0.02%–0.04% Preferred Rewards).",
    "Official disclosures state that effective on or about May 26, 2026, Preferred Rewards transitioned to BofA Rewards™ and the Advantage Savings interest rate booster was discontinued."
]

# 3. Update Citibank Citi Savings
citi = by_id["citi-savings"]
citi["min_open"] = 0
citi["min_open_note"] = "$0 minimum opening deposit; accounts with a zero balance for 90 calendar days are subject to closure."
citi["monthly_fee"] = 4.5
citi["fee_note"] = (
    "$4.50 monthly service fee; waived with $500+ Average Monthly Balance, a linked Citibank checking account, or membership in "
    "Citi Priority ($30k+), Citigold ($200k+), or Citigold Private Client ($1M+)."
)
citi["app"] = "Yes — Citi Mobile® App (mobile check deposit, real-time transfers, 65,000+ fee-free ATMs)."
citi["app_source"] = "https://www.citi.com/banking/savings-account?intc=citihpmenu_overview_savings"
citi["opening_rules"] = "Apply online, via Citi Mobile App, or in branch; zero balance for 90 days subject to closure."
citi["sources"]["product"] = "https://www.citi.com/banking/savings-account?intc=citihpmenu_overview_savings"
citi["sources"]["rates"] = "https://www.citi.com/content/dam/cfs/mobile/assets/JRS/popups/ao/Fact_Sheet.pdf"
citi["flags"] = [
    "Citi Accelerate Savings renders uninterpolated placeholder ':BLUE_AccSavings_Rate%' from NYC because NY is excluded from the National Rate Region — left blank.",
    "Per Citibank's Simplified Banking Fact Sheet (dated 10/01/2026), 'Effective October 23, 2026, Promotional Rate Feature for New Citi Savings accounts will be discontinued.'"
]

# 4. Update Wells Fargo Way2Save
wf = by_id["wells-fargo-way2save"]
wf["apy_as_of"] = "2026-10-07"
wf["apy_note"] = "Standard interest rate 0.01% / APY 0.01% for balances of $0 or more (verified on wellsfargo.com/savings-cds/rates/, accurate as of 10/7/2026)."
wf["sources"]["rates"] = "https://www.wellsfargo.com/savings-cds/rates/"
wf["flags"] = []

# 5. Update Capital One 360 Performance Savings
capone = by_id["capital-one-360-performance"]
capone["apy_status"] = "verified"
capone["apy_as_of"] = "2026-10-21"
capone["tiers"] = [
    {"min": 0, "apy": 3.20, "condition": "All account balances (verified on apply.capitalone.com/fc/index.html)"}
]
capone["apy_note"] = (
    "3.20% variable APY across all balances, effective 10/21/2026, verified on Capital One's official application comparison page "
    "(apply.capitalone.com/fc/index.html). Marketing page capitalone.com/bank/savings-accounts/online-performance-savings-account/ "
    "renders 'NaN APY' in server-side HTML."
)
capone["bonus"] = "Companion 360 Checking offers $250 bonus with code CHECKING250 (2x $500+ direct deposits in 75 days) or DEBIT250/STUDENT250 (20x $10+ debit transactions in 75 days)."
capone["bonus_source"] = "https://www.capitalone.com/bank/choose-your-offer/"
capone["sources"]["rates"] = "https://apply.capitalone.com/fc/index.html"
capone["flags"] = [
    "Marketing page (capitalone.com/bank/savings-accounts/online-performance-savings-account/) renders 'NaN APY' in static HTML, while Capital One's application portal (apply.capitalone.com/fc/index.html) confirms 3.20% APY as of 10/21/2026.",
    "Capital One and Discover Bank share FDIC Cert #4297 (jointly insured since 2025-11-18)."
]

# 6. Update PNC High Yield Savings
pnc = by_id["pnc-high-yield-savings"]
pnc["min_open"] = 0
pnc["min_open_note"] = "$0 minimum deposit to open online; $1.00 minimum balance to earn interest."
pnc["monthly_fee"] = 0
pnc["fee_note"] = "$0 monthly service charge (verified in PNC Consumer Schedule of Service Charges and Fees PDF)."
pnc["sources"]["rates"] = "https://www.pnc.com/content/dam/pnc-com/pdf/personal/Savings/service-charges-high-yield-savings.pdf"
pnc["flags"] = [
    "PNC's High Yield Savings page (3.15% APY in title/meta) refuses to render in NYC branch footprint ('This Product Isn't Available in Your Area'); marked partial."
]

# 7. Add Synchrony Bank, Wells Fargo Platinum Savings, U.S. Bank Elite Money Market, and BMO Alto if not present
new_products = [
    {
        "id": "synchrony-high-yield-savings",
        "brand": "Synchrony",
        "bank": "Synchrony Bank",
        "fdic_cert": "27314",
        "fdic_active": True,
        "product": "Synchrony High Yield Savings",
        "kind": "National digital",
        "tiers": [
            {"min": 0, "apy": 3.55, "condition": "All balances ($0 minimum deposit, $0 minimum balance)"}
        ],
        "apy_status": "verified",
        "apy_note": "3.55% APY across all balances, accurate as of 10/21/2026 (verified on synchrony.com/banking/products/high-yield-savings).",
        "apy_as_of": "2026-10-21",
        "min_open": 0,
        "min_open_note": "No minimum deposit to open.",
        "monthly_fee": 0,
        "fee_note": "No monthly fees and no minimum balance requirement.",
        "withdrawal_note": "Unlimited electronic transfers and ATM withdrawals; optional ATM card with up to $5/statement cycle domestic ATM fee refund (unlimited for Perks Diamond); $25 outgoing wire fee.",
        "app": "Yes — Synchrony Bank Mobile App (4.8★ App Store / 4.6★ Google Play as of 09/01/2026; mobile check deposit up to $2,000/day).",
        "app_source": "https://www.synchrony.com/banking/products/high-yield-savings",
        "security": "24/7 fraud monitoring; custom account alerts; biometric login; FDIC insurance up to $250,000 per ownership category.",
        "security_source": "https://www.synchrony.com/banking/products/high-yield-savings",
        "fdic_note": "Synchrony Bank is an FDIC-insured institution (FDIC certificate 27314).",
        "bonus": "",
        "bonus_source": "",
        "opening_rules": "Open online or in the Synchrony Bank app with SSN/Tax ID; personal non-IRA accounts only; $0 minimum deposit.",
        "sources": {
            "product": "https://www.synchrony.com/banking/products/high-yield-savings",
            "rates": "https://www.synchrony.com/banking/products/high-yield-savings",
            "fdic_lookup": "https://banks.data.fdic.gov/bankfind-suite/bankfind/details/27314"
        },
        "flags": [
            "Embedded savings calculator widget on synchrony.com/banking/products/high-yield-savings displays a stale '2.85%' default while the hero banner, footer CTA, and disclosure confirm '3.55% APY' accurate as of 10/21/2026."
        ]
    },
    {
        "id": "us-bank-elite-money-market",
        "brand": "U.S. Bank (Elite MMA)",
        "bank": "U.S. Bank National Association",
        "fdic_cert": "6548",
        "fdic_active": True,
        "product": "Elite Money Market Account",
        "kind": "National",
        "tiers": [
            {"min": 0, "apy": 0.01, "condition": "Balances under $25,000 ($0 to $24,999.99)"},
            {"min": 25000, "apy": 3.40, "condition": "Balances $25,000+ (new Elite Money Market clients depositing >=$25,000 within 30 days)"}
        ],
        "apy_status": "verified",
        "apy_note": "3.40% APY (3.34% interest rate) on balances of $25,000+ for new Elite Money Market clients who deposit >=$25,000 within 30 days and maintain >=$25,000 daily; 0.01% APY below $25,000. Effective 2026-10-21 for ZIP 55402.",
        "apy_as_of": "2026-10-21",
        "min_open": 100,
        "min_open_note": "$100 minimum opening deposit.",
        "monthly_fee": 10,
        "fee_note": "$10 monthly maintenance fee; waived with a $10,000 minimum daily balance or a U.S. Bank Smartly Checking account.",
        "withdrawal_note": "Includes ATM card, debit card, and check-writing access.",
        "app": "Yes — U.S. Bank Mobile App (#1 ranked mobile banking app on product page).",
        "app_source": "https://www.usbank.com/bank-accounts/savings-accounts/elite-money-market.html",
        "security": "FDIC insured; encryption, biometric login, card lock/unlock.",
        "security_source": "https://www.usbank.com/online-mobile-banking/mobile-banking.html",
        "fdic_note": "FDIC insured under U.S. Bank National Association (certificate 6548; shared with U.S. Bank Smartly Savings).",
        "bonus": "",
        "bonus_source": "",
        "opening_rules": "Open online with $100 minimum deposit; must be a new U.S. Bank savings/MMA client and deposit >=$25,000 within 30 days to earn 3.40% APY.",
        "sources": {
            "product": "https://www.usbank.com/bank-accounts/savings-accounts/elite-money-market.html",
            "rates": "https://www.usbank.com/bank-accounts/savings-accounts/elite-money-market.html",
            "fdic_lookup": "https://banks.data.fdic.gov/bankfind-suite/bankfind/details/6548"
        },
        "flags": [
            "3.40% APY applies only to new savings/MMA clients who deposit >=$25,000 within 30 days; existing accounts open >=30 days earn standard rates (0.01%–0.05% APY)."
        ]
    },
    {
        "id": "wells-fargo-platinum-savings",
        "brand": "Wells Fargo (Platinum)",
        "bank": "Wells Fargo Bank, National Association",
        "fdic_cert": "3511",
        "fdic_active": True,
        "product": "Platinum Savings (New Customer Offer)",
        "kind": "Big Four",
        "tiers": [
            {"min": 0, "apy": 0.01, "condition": "Standard rate ($0 to $24,999.99, or existing customers; 0.02% Prime / 0.05% Premier relationship)"},
            {"min": 25000, "apy": 3.25, "condition": "New Wells Fargo savings customers depositing and maintaining >=$25,000 within 30 days"}
        ],
        "apy_status": "verified",
        "apy_note": "3.25% variable APY (3.20% interest rate) on balances of $25,000+ for new Wells Fargo savings customers (accurate as of 10/7/2026 on wellsfargo.com/savings-cds/rates/). Separate banker-enrolled offer pays 3.50% APY for 12 months on $10,000+ new money.",
        "apy_as_of": "2026-10-07",
        "min_open": 25,
        "min_open_note": "$25 minimum opening deposit.",
        "monthly_fee": 12,
        "fee_note": "$12 monthly service fee; waived with a $3,500 minimum daily balance each fee period.",
        "withdrawal_note": "Includes check-writing option; if daily collected balance drops below $25,000, rate reverts to Standard (0.01%) or Relationship (0.02%–0.05%) APY.",
        "app": "Yes — Wells Fargo Mobile® app.",
        "app_source": "https://www.wellsfargo.com/mobile-online-banking/",
        "security": "Zero-liability protection; 24/7 fraud monitoring; Security Center.",
        "security_source": "https://www.wellsfargo.com/privacy-security/fraud/",
        "fdic_note": "FDIC insured under Wells Fargo Bank, N.A. (certificate 3511).",
        "bonus": "3.25% APY New Customer variable rate on >=$25,000 (online/branch, excludes CO); or 3.50% APY 12-Month Promotional Interest Rate when enrolled with a banker with >=$10,000 new money.",
        "bonus_source": "https://accountoffers.wellsfargo.com/platinumoffer/?sub_channel=BCN&vendor_code=WF&collateral_code=grate",
        "opening_rules": "Must not have owned a Wells Fargo consumer savings account within the past 30 days; deposit >=$25,000 within 30 days of opening.",
        "sources": {
            "product": "https://www.wellsfargo.com/savings-cds/platinum/",
            "rates": "https://www.wellsfargo.com/savings-cds/rates/",
            "fdic_lookup": "https://banks.data.fdic.gov/bankfind-suite/bankfind/details/3511"
        },
        "flags": [
            "3.25% APY is restricted to new Wells Fargo savings customers maintaining >=$25,000 daily (excludes Colorado); Cook, DuPage, and Lake counties (IL) show 4.00% APY on the banker promo page."
        ]
    },
    {
        "id": "bmo-alto-online-savings",
        "brand": "BMO Alto",
        "bank": "BMO Bank National Association",
        "fdic_cert": "16571",
        "fdic_active": True,
        "product": "Alto Online Savings Account",
        "kind": "National digital",
        "tiers": [
            {"min": 0, "apy": 3.00, "condition": "All balances ($0 minimum deposit, $0 minimum balance)"}
        ],
        "apy_status": "verified",
        "apy_note": "3.00% variable APY across all balances as of October 21, 2026 (verified on alto.bmo.com/en-us/high-yield-online-savings/).",
        "apy_as_of": "2026-10-21",
        "min_open": 0,
        "min_open_note": "$0 minimum opening deposit (must fund within 90 days or account closes automatically).",
        "monthly_fee": 0,
        "fee_note": "No monthly maintenance fees.",
        "withdrawal_note": "Unlimited ACH transfers and withdrawals; no checks, debit cards, wire transfers, or Zelle® supported.",
        "app": "Yes — BMO Alto Online & Mobile Banking.",
        "app_source": "https://www.alto.bmo.com/en-us/high-yield-online-savings/",
        "security": "FDIC-insured through BMO Bank N.A.; encrypted online/mobile access.",
        "security_source": "https://www.alto.bmo.com/en-us/high-yield-online-savings/",
        "fdic_note": "BMO Alto is a trade name of BMO Bank N.A. (certificate 16571); deposits combine with retail BMO Bank N.A. accounts for FDIC coverage.",
        "bonus": "",
        "bonus_source": "",
        "opening_rules": "Available in all 50 states; open online in minutes; fund via ACH within 90 days.",
        "sources": {
            "product": "https://www.alto.bmo.com/en-us/high-yield-online-savings/",
            "rates": "https://www.alto.bmo.com/en-us/high-yield-online-savings/",
            "fdic_lookup": "https://banks.data.fdic.gov/bankfind-suite/bankfind/details/16571"
        },
        "flags": [
            "BMO Alto is a division of BMO Bank N.A. (cert 16571) and shares the same $250,000 FDIC limit as BMO retail accounts (such as BMO Savings Builder, which pays 0.01% APY + $5/mo reward)."
        ]
    }
]

for np in new_products:
    if np["id"] not in by_id:
        # Insert before discover-online-savings so inactive stays last
        data["products"].insert(-1, np)
    else:
        idx = next(i for i, x in enumerate(data["products"]) if x["id"] == np["id"])
        data["products"][idx] = np

BANKS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Updated data/banks.json: total products = {len(data['products'])}")
