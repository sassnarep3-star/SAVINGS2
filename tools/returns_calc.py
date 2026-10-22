#!/usr/bin/env python3
"""
SAVINGS2 returns calculator.

Computes 1-year and 5-year interest projections for the savings accounts
verified from official bank sources on 2026-10-22 (see docs sources register).

Method:
- 1-year interest = balance * APY  (APY is the effective annual yield, which
  already includes the effect of compounding, assuming the rate is held
  constant and interest stays in the account).
- 5-year interest = balance * ((1 + APY)^5 - 1)  (APY held constant).
- Monthly average = 1-year interest / 12.
- APYs are variable; projections are illustrations, not guarantees.

All APY inputs below are the values verified from official sources
(see SOURCE strings). Tiered accounts use the tier applicable to each
deposit level.
"""

BALANCES = [10_000, 50_000, 100_000, 250_000]

# bank key -> (label, {balance: APY% used}, source note)
CONFIGS = [
    ("synchrony", "Synchrony Bank High Yield Savings", {b: 3.55 for b in BALANCES},
     "3.55% APY, all balances (synchrony.com, checked 2026-10-22)"),
    ("marcus", "Marcus by Goldman Sachs Online Savings", {b: 3.50 for b in BALANCES},
     "3.50% APY, all balances (marcus.com, as of 2026-10-21)"),
    ("usbank_rel", "U.S. Bank Smartly Savings (with qualifying product, CQB >= $25k)",
     {10_000: 2.00, 50_000: 3.50, 100_000: 3.50, 250_000: 3.50},
     "Relationship rates by CQB tier (usbank.com, effective 2026-10-21)"),
    ("wells_promo", "Wells Fargo Platinum Savings - new savings customer promo ($25k+)",
     {10_000: 0.01, 50_000: 3.25, 100_000: 3.25, 250_000: 3.25},
     "3.25% APY promo on $25,000+ balances, new savings customers (wellsfargo.com, effective 2026-10-07)"),
    ("capone", "Capital One 360 Performance Savings", {b: 3.20 for b in BALANCES},
     "3.20% APY, all balances (capitalone.com, effective 2026-10-21)"),
    ("amex", "American Express High Yield Savings", {b: 3.20 for b in BALANCES},
     "3.20% APY, all balances (americanexpress.com, checked 2026-10-22)"),
    ("sofi_dd", "SoFi Savings with Eligible Direct Deposit", {b: 3.30 for b in BALANCES},
     "3.30% APY with eligible direct deposit or $5,000+ qualifying deposits per 31 days (sofi.com, as of 2026-10-20)"),
    ("ally", "Ally Bank Savings", {b: 3.10 for b in BALANCES},
     "3.10% APY, all balances (ally.com, correct as of 2026-10-21)"),
    ("citi_accel", "Citi Accelerate Savings (NOT available to NY residents)",
     {b: 3.00 for b in BALANCES},
     "3.00% APY reported by independent trackers 2026-10; official page renders rate dynamically - FLAGGED"),
    ("usbank_std", "U.S. Bank Smartly Savings (standard, no linked product)",
     {b: 0.05 for b in BALANCES},
     "0.05% standard APY (usbank.com, effective 2026-10-21)"),
    ("bofa", "Bank of America Advantage Savings", {b: 0.04 for b in BALANCES},
     "0.04% APY, all tiers (Bank of America NY Tri-State rate sheet, effective 2026-10-21)"),
    ("pnc_std", "PNC Standard Savings ($2,500+ tier)", {b: 0.03 for b in BALANCES},
     "0.03% APY on $2,500+ (pnc.com, accurate as of 2026-10-21)"),
    ("citi_std", "Citi Savings (standard, NY rate region)",
     {b: 0.03 for b in BALANCES},
     "0.03% standard APY in NY (Citi official PDF: 'in the states of NY, CT, MD, VA, DC, CA, NV, NJ and select markets in FL or IL, the APY for Citi Savings Accounts is 0.03%')"),
    ("wells_rel", "Wells Fargo Platinum Savings (linked Premier Checking)",
     {b: 0.05 for b in BALANCES},
     "0.05% relationship APY (wellsfargo.com, checked 2026-10-22)"),
    ("chase_premier_rel", "Chase Premier Savings (relationship rate)",
     {b: 0.02 for b in BALANCES},
     "0.02% relationship APY (Chase rate sheet, in effect 2026-10-16)"),
    ("chase", "Chase Savings", {b: 0.01 for b in BALANCES},
     "0.01% APY, all tiers (Chase rate sheet, in effect 2026-10-16)"),
    ("bofa_fee", "BofA Advantage Savings WITH $8/mo fee NOT waived (net)",
     {10_000: -0.44, 50_000: -0.30, 100_000: -0.26, 250_000: -0.24},
     "0.04% APY minus $96/yr fee: net negative on every balance (illustration)"),
    ("chase_fee", "Chase Savings WITH $5/mo fee NOT waived (net)",
     {10_000: -0.59, 50_000: -0.55, 100_000: -0.54, 250_000: -0.53},
     "0.01% APY minus $60/yr fee: net negative on every balance (illustration)"),
]


def money(x):
    return f"${x:,.0f}" if x >= 0 else f"-${abs(x):,.0f}"


def main():
    print(f"{'Account':62s} {'Rate':>6s} {'Deposit':>10s} {'1-yr int':>10s} {'5-yr int':>10s} {'Value@5y':>12s}")
    for key, label, tiers, src in CONFIGS:
        for b in BALANCES:
            apy = tiers[b]
            one = b * apy / 100.0
            five = b * ((1 + apy / 100.0) ** 5 - 1)
            print(f"{label:62s} {apy:5.2f}% {money(b):>10s} {money(one):>10s} {money(five):>10s} {money(b + five):>12s}")
        print()

    # First-year value at $250,000 including verified new-account bonuses
    print("\n=== First-year value at $250,000 (interest + bonus, bonus requires qualifying deposit) ===")
    rows = [
        ("Capital One 360 Performance Savings + BONUS1500", 3.20, 1500,
         "$100,000+ external deposit within 15 days, hold 90 days"),
        ("Synchrony High Yield Savings", 3.55, 0, "no bonus"),
        ("Marcus Online Savings", 3.50, 0, "no new-account bonus (referral boost exists)"),
        ("U.S. Bank Smartly (relationship 3.50%)", 3.50, 0, "requires Bank Smartly Checking/Safe Debit/Smartly card + $25k CQB"),
        ("SoFi Savings (3.30% + 6-mo 1.10% boost) + $400 bonus", 3.30, 400,
         "eligible direct deposit; boost = 1.10% x ~6 months ~= $1,375 extra at $250k"),
        ("Wells Fargo Platinum promo 3.25% (new savings customer)", 3.25, 0, "$25,000+ balance, new savings customers"),
        ("American Express HYSA", 3.20, 0, "no bonus"),
        ("Ally Savings", 3.10, 0, "no bonus"),
    ]
    for label, apy, bonus, note in rows:
        one = 250_000 * apy / 100.0
        extra = 0
        if "boost" in label:
            extra = 250_000 * 0.011 * 0.5  # 1.10% for half a year
        print(f"{label:65s} interest={money(one+extra):>9s} bonus={money(bonus):>7s} total={money(one+extra+bonus):>10s}  [{note}]")

    # SoFi Plus blended at 250k (4.50% on first 20k, 3.30% rest, minus $120/yr sub)
    one = (20_000 * 0.045 + 230_000 * 0.033) - 120
    print(f"\nSoFi Plus (4.50% on first $20k + 3.30% on rest - $10/mo sub), 1-yr at $250k: {money(one)}")

    # FDIC overage illustration
    print("\n=== FDIC coverage at a single bank (single ownership category) ===")
    for b in [250_000, 500_000, 1_000_000]:
        cov = min(b, 250_000)
        print(f"Deposit {money(b):>11s} -> insured {money(cov):>11s} -> uninsured {money(b - cov):>11s}")

    # 5-year at 250k for top options, and comparison of brick standard vs online
    print("\n=== 5-year value at $250k (rate held constant) ===")
    for label, apy in [("Synchrony 3.55%", 3.55), ("Marcus 3.50%", 3.50), ("Capital One 3.20%", 3.20),
                       ("Chase 0.01%", 0.01), ("FDIC natl avg 0.38%", 0.38)]:
        five = 250_000 * ((1 + apy / 100.0) ** 5 - 1)
        print(f"{label:22s} -> 5-yr interest {money(five):>10s}")

    # Monthly interest at 250k
    print("\n=== Approximate monthly interest at $250,000 ===")
    for label, apy in [("Synchrony 3.55%", 3.55), ("Marcus 3.50%", 3.50), ("Capital One 3.20%", 3.20),
                       ("Chase 0.01%", 0.01)]:
        print(f"{label:22s} -> ~{money(250_000 * apy / 100.0 / 12)} per month")


if __name__ == "__main__":
    main()
