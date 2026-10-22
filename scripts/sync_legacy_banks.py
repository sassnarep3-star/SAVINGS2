#!/usr/bin/env python3
"""
Synchronizes `data/banks.json` (created by `session-46ab1baa`) with all verified
primary-source bugfixes and disclosures audited line-by-line by `session-6ce52089` on 2026-10-22,
without deleting any existing product record.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANKS_JSON = ROOT / "data" / "banks.json"


def main() -> None:
    data = json.loads(BANKS_JSON.read_text())
    products = data["products"]
    by_id = {p["id"]: p for p in products}

    # 1. CRITICAL BUGFIX (IRREG-AUDIT-01): SoFi passive non-DD APY is 0.80% (Table 5 of Oct 20, 2026 Rate Sheet PDF), NOT 3.30%!
    sofi = by_id["sofi-savings"]
    sofi["tiers"] = [
        {
            "min": 0,
            "apy": 0.80,
            "condition": "Standard savings APY WITHOUT eligible direct deposit or $5,000/31-day qualifying deposits (0.79708% rate — Table 5, Oct 20, 2026 Rate Sheet PDF)"
        },
        {
            "min": 0,
            "apy": 3.30,
            "condition": "Ongoing APY WITH eligible direct deposit OR $5,000+ in qualifying deposits every 31 days (Table 4; 4.70% up to $20k w/ SoFi Plus)"
        },
        {
            "min": 0,
            "apy": 4.40,
            "condition": "New-member promo APY with eligible direct deposit or $5,000/31d qualifying deposits: 3.30% + 1.10% boost for up to 6 months"
        }
    ]
    sofi["sources"]["rate_sheet_pdf"] = "https://d32ijn7u0aqfv4.cloudfront.net/wp/wp-content/uploads/raw/SoFi-Bank-Rate-Sheet-October-20-2026.pdf"
    sofi["bonus"] = "Up to $400 cash bonus ($50 for $1,000–$4,999.99 DD; $400 for $5,000+ DD within 25 days) + 1.10% APY boost (to 4.40% APY) for up to 6 months; valid through 2027-12-31."
    sofi["bonus_source"] = "https://www.sofi.com/banking/high-yield-savings-account/"

    # 2. UPGRADE Capital One 360 Performance Savings via official Truth-in-Savings Disclosure + BONUS1500
    cap = by_id["capital-one-360-performance"]
    cap["apy_status"] = "verified"
    cap["tiers"] = [{"min": 0, "apy": 3.20, "condition": "All balances (3.1540% interest rate; monthly compounding per official Truth-in-Savings disclosure)"}]
    cap["apy_as_of"] = "2026-10-21"
    cap["apy_note"] = "Hero marketing page rendered client-side `NaN APY`, but official Capital One Truth-in-Savings Disclosure page confirms `3.1540% Interest Rate / 3.20% APY` across all balances effective `10/21/2026`."
    cap["bonus"] = "Promo code BONUS1500 (NO direct deposit required): $300 bonus on $20,000–$49,999.99, $750 bonus on $50,000–$99,999.99, or $1,500 bonus on $100,000+ deposited within 15 days and held 90 days."
    cap["bonus_source"] = "https://www.capitalone.com/bank/bonus1500/"
    cap["sources"]["disclosure"] = "https://www.capitalone.com/bank/disclosures/savings-accounts/online-performance-savings-account/"
    cap["flags"] = [
        "Marketing hero page rendered `NaN APY` to non-JS client; exact `3.20% APY` verified from official Capital One Truth-in-Savings Disclosure page.",
        "Shares single $250,000 charter limit (CERT #4297) with Discover deposits post-2025-05-18 merger."
    ]

    # 3. UPGRADE Bank of America Advantage Savings min_open ($100) and monthly_fee ($8 / $500 waiver) from Aug 7, 2026 Fee Schedule PDF
    bofa = by_id["bofa-advantage-savings"]
    bofa["min_open"] = 100
    bofa["min_open_note"] = "$100.00 minimum opening deposit confirmed in official Personal Schedule of Fees (Effective August 7, 2026)."
    bofa["monthly_fee"] = 8
    bofa["fee_note"] = "$8.00 monthly fee (waived first 6 months on new accounts; $0 thereafter with $500+ minimum daily balance, Advantage Relationship Banking, age under 25, or BofA Rewards Preferred Plus/Honors/Premier)."
    bofa["sources"]["fee_schedule_pdf"] = "https://www.bankofamerica.com/salesservices/deposits/resources/personal-schedule-fees/?request_locale=en_US"
    bofa["flags"] = [
        "APY not published without interactive ZIP submission — APY left strictly blank.",
        "Public HTML shows `$XXXX` placeholders, resolved for fee/minimum via official Aug 7, 2026 Personal Schedule of Fees PDF."
    ]

    # 4. UPGRADE Chase Savings bonus ($200 standalone / $900 combo exp. 2027-01-27)
    chase = by_id["chase-savings"]
    chase["bonus"] = "$200 Chase Savings℠ bonus ($15,000 new money within 30 days, held 90 days) OR $900 combo bonus when opened with Chase Total Checking® + direct deposit (expires 2027-01-27)."
    chase["bonus_source"] = "https://www.chase.com/personal/offers/checking-and-savings"
    chase["sources"]["fee_schedule_pdf"] = "https://www.chase.com/content/dam/chase-ux/documents/personal/checking/ABSF-en.pdf"

    # 5. UPGRADE Citibank details + NYC exclusion warning
    citi = by_id["citi-savings"]
    citi["min_open"] = 0
    citi["min_open_note"] = "$0 minimum deposit required to open/obtain APY; zero-balance accounts close after 90 days."
    citi["fee_note"] = "Monthly service fee waived with $500+ Average Monthly Balance, linked Citi Checking account, or Relationship Tier ($30k+ Citi Priority / $200k+ Citigold)."
    citi["app"] = "Yes — Citi Mobile® App (iOS/Android) + 65,000+ fee-free ATMs."
    citi["app_source"] = "https://www.citi.com/banking/savings-account"
    citi["security"] = "Biometric login, real-time fraud alerts, 24/7 monitoring, FDIC Certificate #7213."
    citi["security_source"] = "https://www.citi.com/banking/savings-account"
    citi["opening_rules"] = "CRITICAL GEOGRAPHIC RESTRICTION: Residential addresses in NY, CA, NJ, CT, FL, IL, MD, DC, NV, and select VA markets are INELIGIBLE for Citi® Accelerate Savings per official comparison disclosure."
    citi["sources"]["comparison"] = "https://www.citi.com/banking/compare-bank-accounts"
    citi["flags"] = [
        "Public page renders `:BLUE_AccSavings_Rate%` placeholder until residential address is entered — APY left strictly blank.",
        "New York (NY) residents are excluded from Citi® Accelerate Savings per official Citi disclosure."
    ]

    # 6. Append newly verified national charters if not yet present in data/banks.json (Synchrony 3.55%, Wells Fargo Platinum 3.25%, BMO Savings Builder 0.01% + $60)
    extra_products = [
        {
            "id": "synchrony-high-yield-savings",
            "brand": "Synchrony Bank",
            "bank": "Synchrony Bank",
            "fdic_cert": "27314",
            "fdic_active": True,
            "product": "High Yield Savings Account",
            "kind": "National online",
            "tiers": [{"min": 0, "apy": 3.55, "condition": "All balances ($0 minimum; unconditional)"}],
            "apy_status": "verified",
            "apy_note": "3.55% APY accurate as of 10/21/2026 on live product page `/banking/products/hys-core` ($115.2B assets). Interactive calculator widget defaults to stale `2.85%` — flagged.",
            "apy_as_of": "2026-10-21",
            "min_open": 0,
            "min_open_note": "$0 minimum opening deposit.",
            "monthly_fee": 0,
            "fee_note": "$0 monthly maintenance fee.",
            "withdrawal_note": "Unlimited ACH transfers; optional ATM card ($0 Synchrony fee at Plus/Accel ATMs + up to $5/cycle domestic ATM fee refund); $25 outgoing wire.",
            "app": "Yes — Synchrony Bank Mobile App (iOS & Android, mobile check deposit up to $2,000/day).",
            "app_source": "https://www.synchrony.com/banking/products/hys-core",
            "security": "Multi-factor authentication, 24/7 fraud monitoring, custom alerts, TLS encryption, FDIC Certificate #27314.",
            "security_source": "https://www.synchrony.com/banking/products/hys-core",
            "fdic_note": "FDIC insured up to $250,000 per depositor, per ownership category.",
            "bonus": "",
            "bonus_source": "",
            "opening_rules": "Apply online or in Synchrony app with SSN/ITIN and U.S. address; fund via ACH, mobile check, direct deposit, or wire.",
            "sources": {
                "product": "https://www.synchrony.com/banking/products/hys-core",
                "rates": "https://www.synchrony.com/banking/products/hys-core",
                "fdic_lookup": "https://banks.data.fdic.gov/bankfind-suite/bankfind/details/27314"
            },
            "flags": [
                "Legacy `/banking/high-yield-savings.html` URL returns 404; live product page `/banking/products/hys-core` confirms 3.55% APY as of 2026-10-21, while embedded JS calculator shows stale 2.85%."
            ]
        },
        {
            "id": "wells-fargo-platinum-savings",
            "brand": "Wells Fargo",
            "bank": "Wells Fargo Bank, National Association",
            "fdic_cert": "3511",
            "fdic_active": True,
            "product": "Platinum Savings (New Customer Offer)",
            "kind": "Big Four",
            "tiers": [
                {"min": 0, "apy": 0.01, "condition": "Standard variable rate below $25,000 or non-promo accounts"},
                {"min": 25000, "apy": 3.25, "condition": "New-customer special interest rate offer on $25,000+ new money (branch appointment enrollment, ZIP 94105 table)"}
            ],
            "apy_status": "verified",
            "apy_note": "3.25% APY new-customer $25,000+ rate verified on official `wellsfargo.com/savings-cds/rates/` table (standard non-promo APY is 0.01%). Requires branch banker enrollment.",
            "apy_as_of": None,
            "min_open": 25,
            "min_open_note": "$25 minimum opening deposit ($25,000+ new money required for 3.25% special rate).",
            "monthly_fee": 12,
            "fee_note": "$12 monthly service fee; $0 with $3,500+ minimum daily balance.",
            "withdrawal_note": "Up to 6 withdrawals/transfers per monthly fee period; checks included.",
            "app": "Yes — Wells Fargo Mobile® App (iOS & Android).",
            "app_source": "https://www.wellsfargo.com/savings-cds/platinum/",
            "security": "24/7 fraud monitoring, biometric login, card lock, 4,108 U.S. branches, FDIC Certificate #3511.",
            "security_source": "https://www.wellsfargo.com/privacy-security/",
            "fdic_note": "Shares single $250,000 charter cap with Way2Save under Wells Fargo Bank, N.A. (CERT #3511).",
            "bonus": "3.25% APY special new-customer rate on $25,000+ new money (requires in-branch enrollment).",
            "bonus_source": "https://www.wellsfargo.com/savings-cds/rates/",
            "opening_rules": "$25 online for standard 0.01% tier; branch appointment required to enroll in 3.25% new-customer offer.",
            "sources": {
                "product": "https://www.wellsfargo.com/savings-cds/platinum/",
                "rates": "https://www.wellsfargo.com/savings-cds/rates/",
                "fdic_lookup": "https://banks.data.fdic.gov/bankfind-suite/bankfind/details/3511"
            },
            "flags": [
                "Public rate table omits a specific effective date and requires branch appointment for the 3.25% new-customer rate."
            ]
        },
        {
            "id": "bmo-savings-builder",
            "brand": "BMO Bank",
            "bank": "BMO Bank National Association",
            "fdic_cert": "16571",
            "fdic_active": True,
            "product": "Savings Builder Account",
            "kind": "National branch",
            "tiers": [{"min": 0, "apy": 0.01, "condition": "All balances ($0.01+; accurate as of 10/21/2026)"}],
            "apy_status": "verified",
            "apy_note": "0.01% APY across all balances (accurate as of 10/21/2026) plus $5/month reward in Year 1 ($60 max) when growing balance by >= $200/month.",
            "apy_as_of": "2026-10-21",
            "min_open": 25,
            "min_open_note": "$25 minimum deposit to open.",
            "monthly_fee": 0,
            "fee_note": "$0 monthly maintenance fee.",
            "withdrawal_note": "Unlimited ACH transfers; 40,000+ fee-free BMO & Allpoint® ATMs.",
            "app": "Yes — BMO Digital Banking App (iOS & Android).",
            "app_source": "https://www.bmo.com/en-us/main/personal/savings-and-cds/savings-builder/",
            "security": "Multi-factor authentication, Total Look®, biometric login, 986 U.S. branches, FDIC Certificate #16571.",
            "security_source": "https://www.bmo.com/en-us/main/personal/savings-and-cds/savings-builder/",
            "fdic_note": "FDIC insured up to $250,000 per depositor under BMO Bank N.A. (CERT #16571).",
            "bonus": "Up to $60 Year-1 Savings Reward ($5/month each month balance grows by >= $200 during first 12 months).",
            "bonus_source": "https://www.bmo.com/en-us/main/personal/savings-and-cds/savings-builder/",
            "opening_rules": "Apply online in ~5 minutes; age 18+, SSN, U.S. address, and $25 opening transfer.",
            "sources": {
                "product": "https://www.bmo.com/en-us/main/personal/savings-and-cds/savings-builder/",
                "rates": "https://www.bmo.com/en-us/main/personal/savings-and-cds/savings-builder/",
                "fdic_lookup": "https://banks.data.fdic.gov/bankfind-suite/bankfind/details/16571"
            },
            "flags": [
                "Legacy `alto.bmo.com/en-us/online-savings-account/` URL returns HTTP 404; verified live `BMO Savings Builder` instead."
            ]
        }
    ]
    for ep in extra_products:
        if ep["id"] not in by_id:
            products.append(ep)

    BANKS_JSON.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Updated data/banks.json -> {len(products)} total products.")


if __name__ == "__main__":
    main()
