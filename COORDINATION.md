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
| **TASK-02** | Big National Banks — High-Yield Savings Accounts (HYSA) Verification | `in progress` | `1024a045-savings2` | `arena/1024a045-savings2` | `data/national_banks_savings.json`, `high-yield-savings.html` |
| **TASK-03** | Big Four Brick-and-Mortar National Banks & Relationship Tiers Verification | `in progress` | `1024a045-savings2` | `arena/1024a045-savings2` | `data/big_four_banks.json`, `big-four-comparison.html` |
| **TASK-04** | Account Opening Bonuses, Promotions & Account Rules Verification | `unclaimed` | — | — | `data/promotions_and_rules.json`, `bonuses-and-promotions.html`, `account-rules-and-security.html` |
| **TASK-05** | Return on Size of Investment & Max FDIC ($250k / $500k / $1M) Projections (`2026-10-22`) | `unclaimed` | — | — | `data/investment_returns_matrix.json`, `investment-returns.html` |
| **TASK-06** | Irregularities, Regional Restrictions & Unverified Fields Audit (`Flagged for Review`) | `unclaimed` | — | — | `data/flagged_for_review.json`, `flagged-for-review.html` |
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
