# COORDINATION.md — Shared Task Board & Verification Log

**Repository:** `sassnarep3-star/SAVINGS2`  
**Active Session ID:** `1024a045-savings2`  
**Active Branch:** `arena/1024a045-savings2` (Note: Arena session branch name is fixed by platform policy to `arena/1024a045-savings2`)  
**Analysis Reference Date (Account Opening Date):** `2026-10-22` (UTC)

---

## 1. Shared Task Board

| Task ID | Task Name | Status | Owning Session ID | Branch | File Scope |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TASK-01** | FDIC Insurance Rules, Cert Numbers & Macro Benchmarks Verification | `done` | `1024a045-savings2` | `arena/1024a045-savings2` | `data/fdic_and_benchmarks.json`, `fdic-maximization.html` |
| **TASK-02** | Big National Banks — High-Yield Savings Accounts (HYSA) Verification | `done` | `1024a045-savings2` | `arena/1024a045-savings2` | `data/national_banks_savings.json`, `high-yield-savings.html` |
| **TASK-03** | Big Four Brick-and-Mortar National Banks & Relationship Tiers Verification | `done` | `1024a045-savings2` | `arena/1024a045-savings2` | `data/big_four_banks.json`, `big-four-comparison.html` |
| **TASK-04** | Account Opening Bonuses, Promotions & Account Rules Verification | `in progress` | `1024a045-savings2` | `arena/1024a045-savings2` | `data/promotions_and_rules.json`, `bonuses-and-promotions.html`, `account-rules-and-security.html` |
| **TASK-05** | Return on Size of Investment & Max FDIC ($250k / $500k / $1M) Projections (`2026-10-22`) | `in progress` | `1024a045-savings2` | `arena/1024a045-savings2` | `data/investment_returns_matrix.json`, `investment-returns.html` |
| **TASK-06** | Irregularities, Regional Restrictions & Unverified Fields Audit (`Flagged for Review`) | `in progress` | `1024a045-savings2` | `arena/1024a045-savings2` | `data/flagged_for_review.json`, `flagged-for-review.html` |
| **TASK-07** | Final Integration, Dashboard Site Build, Link Verification, PR & Merge to `main` | `unclaimed` | — | — | `index.html`, `assets/css/styles.css`, `assets/js/app.js`, `scripts/verify_site.py`, `README.md`, `.nojekyll` |

---

## 2. Session Coordination Log

- **2026-10-22 (Session `1024a045-savings2`):** Initialized `COORDINATION.md` in repo root. Inspected repository (`README.md` only at initial commit `e5a82d8aadbfe96134b997e746e1098ff8ec03bc`). Claimed `TASK-01` to begin official source verification of FDIC insurance rules, bank charter cert numbers, and Federal Reserve / FDIC national rate benchmarks.
- **2026-10-22 (Session `1024a045-savings2`):** Completed `TASK-01` (`data/fdic_and_benchmarks.json`).
  - **Sources Verified:**
    - FDIC National Rates and Rate Caps (as of October 19, 2026): https://www.fdic.gov/national-rates-and-rate-caps (Savings National Rate: 0.38% APY; Money Market: 0.63% APY; 12-Month CD: 1.76% APY; National Rate Cap for Savings: 4.63%).
    - Federal Reserve Board H.15 Selected Interest Rates (Released October 20, 2026; data as of October 19, 2026): https://www.federalreserve.gov/releases/h15/ (Effective Federal Funds Rate: 3.88%).
    - Federal Reserve FOMC Statement & Implementation Note (Effective September 17, 2026): https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a1.htm (Fed Funds Target Range: 3.75%–4.00%; IORB: 3.90%; ON RRP: 3.75%).
    - FDIC Deposit Insurance Brochures & Trust Rule (12 C.F.R. § 330.10, effective April 1, 2024): https://www.fdic.gov/resources/deposit-insurance/brochures/insured-deposits and https://www.fdic.gov/financial-institution-employees-guide-deposit-insurance/trust-accounts ($250,000 per owner per category; up to $1,250,000 per owner for Trust/POD accounts with 5+ unique beneficiaries).
    - FDIC Charter Certificates Verified for all 13 major national banks: JPMorgan Chase (#628), Bank of America (#3510), Wells Fargo (#3511), Citibank (#7213), U.S. Bank (#6548), PNC Bank (#6384), Capital One N.A. (#4297), Goldman Sachs Bank USA (#33124), American Express National Bank (#27471), Ally Bank (#57803), Barclays Bank Delaware (#57203), Synchrony Bank (#27314), BMO Bank N.A. (#16571).
  - **Irregularities Flagged during TASK-01:**
    - Capital One + Discover Bank Charter Consolidation: Per https://www.capitalone.com/updates/discover/savings/, as of November 18, 2025, Capital One and Discover deposit accounts are jointly insured under Capital One, N.A. (Cert #4297), meaning depositors cannot receive separate $250,000 single-account FDIC limits across both brands.
    - BMO Alto + BMO Bank N.A. Shared Charter: Per https://www.alto.bmo.com/en-us/high-yield-online-savings/, BMO Alto is a trade name of BMO Bank N.A. (Cert #16571) and shares the same $250,000 FDIC limit as BMO retail accounts.
  - Claimed `TASK-02` and `TASK-03`.
- **2026-10-22 (Session `1024a045-savings2`):** Completed `TASK-02` (`data/national_banks_savings.json`) and `TASK-03` (`data/big_four_banks.json`).
  - **Sources Verified (`TASK-02`):**
    - Barclays Tiered Savings (3.65% APY on $250k–$1M; 3.50% APY on <$250k; +$200 bonus on $25k+ held 120 days; effective 2026-10-07): https://banking.us.barclays/tiered-savings.html
    - Barclays Online Savings (3.20% APY; effective 2026-10-07): https://banking.us.barclays/online-savings.html
    - Synchrony Bank High Yield Savings (3.55% APY; effective 2026-10-21): https://www.synchrony.com/banking/products/high-yield-savings
    - Marcus by Goldman Sachs Online Savings (3.50% APY + 1.00% 3-month referral boost; effective 2026-10-21; max $1M/account, $3M total): https://www.marcus.com/us/en/savings/high-yield-savings and https://www.marcus.com/content/dam/marcus/us/en/pdfs/Marcus_Deposit_Account_Agreement.pdf
    - U.S. Bank Smartly Savings (0.05% standard APY; 3.50% relationship APY at $25k+ CQB with eligible account; effective 2026-10-21): https://www.usbank.com/bank-accounts/savings-accounts/bank-smartly-savings/savings-account-interest-rates.html
    - U.S. Bank Elite Money Market (3.40% APY on $25k+ for new clients <30 days; 0.01%–0.05% standard APY; effective 2026-10-21): https://www.usbank.com/bank-accounts/savings-accounts/elite-money-market.html
    - American Express High Yield Savings (3.20% APY; $5M max balance; effective 2026-10-21): https://www.americanexpress.com/en-us/banking/online-savings/high-yield-savings-account/ and https://www.americanexpress.com/content/dam/amex/en-us/banking/personal-savings/Savings-Schedule.pdf
    - Capital One 360 Performance Savings (3.20% APY; effective 2026-10-21): https://apply.capitalone.com/fc/index.html and https://www.capitalone.com/bank/disclosures/savings-accounts/online-performance-savings-account/
    - PNC High Yield Savings (3.15% APY; geo-restricted out of NYC): https://www.pnc.com/en/personal-banking/banking/savings/high-yield-savings.html
    - Ally Bank Online Savings (3.10% APY; 10 withdrawals/cycle limit; effective 2026-10-21): https://www.ally.com/bank/online-savings-account/
    - BMO Alto Online Savings (3.00% APY; effective 2026-10-21): https://www.alto.bmo.com/en-us/high-yield-online-savings/
    - Citi Accelerate Savings (Geo-gated to National Rate Region; renders `:BLUE_AccSavings_Rate%` from NYC): https://www.citi.com/banking/savings-account?intc=citihpmenu_overview_savings
  - **Sources Verified (`TASK-03`):**
    - JPMorgan Chase Consumer Deposit Rates (Effective 2026-10-16; Chase Savings 0.01% APY; Chase Premier Savings & Private Client Savings 0.01% standard / 0.02% relationship APY): https://www.chase.com/content/dam/chase-ux/ratesheets/pdfs/rdin1.pdf and https://account.chase.com/consumer/banking/savingsoffer ($100/$200 new money bonus).
    - Bank of America Advantage Savings (Effective 2026-08-07; 0.01% standard APY; transition of Preferred Rewards to BofA Rewards™ on 2026-05-26 and discontinuation of savings booster): https://www.bankofamerica.com/salesservices/deposits/resources/personal-schedule-fees/ and https://promotions.bankofamerica.com/preferredrewards/es?subCampCode=94362&nmls=481151
    - Wells Fargo Savings Rates (Effective 2026-10-07; Way2Save 0.01% APY; Platinum Savings 0.01% standard / 0.02% Prime / 0.05% Premier / 3.25% New Customer >=$25k / 3.50% 12-mo banker promo >=$10k): https://www.wellsfargo.com/savings-cds/rates/ and https://accountoffers.wellsfargo.com/platinumoffer/?sub_channel=BCN&vendor_code=WF&collateral_code=grate
    - Citibank Simplified Banking Fact Sheet (Effective 2026-10-01; Citi Savings 0.03%–0.12% standard/tier APY; Promotional Rate Feature for New Citi Savings discontinued effective October 23, 2026): https://www.citi.com/content/dam/cfs/mobile/assets/JRS/popups/ao/Fact_Sheet.pdf
    - BMO Retail Savings Builder (0.01% APY + $5/mo reward up to $60/yr): https://www.bmo.com/en-us/main/personal/bank-accounts/savings-and-cds/ and https://www.bmo.com/en-us/pdf/disclosures/savings_builder_reg_dd.pdf
  - Claimed `TASK-04`, `TASK-05`, and `TASK-06`.
