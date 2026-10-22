# U.S. National Bank Savings Intelligence & Max-FDIC Optimizer (`SAVINGS2`)

**Live GitHub Pages Dashboard:** <https://sassnarep3-star.github.io/SAVINGS2/>  
**Account Opening Date Anchor:** `2026-10-22` (UTC) · **Primary Verification Date:** `2026-10-22` (UTC)

---

## Executive Summary (`2026-10-22` Open Date Anchor)

This repository investigates and verifies the best U.S. **large national commercial and national direct bank** consumer savings accounts — screening strictly for **major national scale (`$43.5B` to `$4.09T` consolidated assets, zero small local banks)**, **mobile banking apps**, **multi-factor authentication & security**, and **maximum `$250,000+` FDIC insurance engineering**.

| Strategy / Benchmark (`$250,000` Principal Opened `2026-10-22`) | Year-1 Net Return (`2027-10-22`) | Effective Year-1 APY | Uninsured Overflow | Primary Official Sources |
| --- | ---: | ---: | ---: | --- |
| **Optimal 3-Charter Active Stack (With Direct Deposit)** — `$15k` Chase (`$900` Combo) + `$100k` Capital One (`BONUS1500`) + `$135k` SoFi (`4.40%` 6M Boost + `$400` DD, `$3M` Sweep) | **$11,684.64** | **4.67%** *(Beats 1Y Treasury `4.52%`!)* | **$0.00** (`$3.50M` cap) | [Chase](https://www.chase.com/personal/offers/checking-and-savings) · [CapOne](https://www.capitalone.com/bank/bonus1500/) · [SoFi PDF](https://d32ijn7u0aqfv4.cloudfront.net/wp/wp-content/uploads/raw/SoFi-Bank-Rate-Sheet-October-20-2026.pdf) |
| **Optimal 2-Charter Zero-DD Split (No Direct Deposit)** — `$100k` Capital One (`BONUS1500`) + `$150k` CIT Platinum (`BOOST50` `4.25%` 6M -> `3.75%`) | **$10,699.55** | **4.28%** *(Beats 3M T-Bill `4.25%`!)* | **$0.00** (`$500k` cap) | [CapOne](https://www.capitalone.com/bank/bonus1500/) · [CIT Boost](https://www.cit.com/cit-bank/platinum-savings/boost) |
| **Optimal 2-Charter Oct-Dated Split (No Direct Deposit)** — `$100k` Capital One (`BONUS1500`) + `$150k` Synchrony HYSA (`3.55%` Oct 21 rate) | **$10,025.00** | **4.01%** | **$0.00** (`$500k` cap) | [CapOne](https://www.capitalone.com/bank/disclosures/savings-accounts/online-performance-savings-account/) · [Synchrony](https://www.synchrony.com/banking/products/hys-core) |
| **Best Single-Account With DD (`$3M` Sweep)** — SoFi Checking & Savings (`4.40%` 6M -> `3.30%` + `$400` DD) | **$10,021.36** | **4.01%** | **$0.00** (`$3.00M` sweep) | [SoFi Rate Sheet PDF](https://d32ijn7u0aqfv4.cloudfront.net/wp/wp-content/uploads/raw/SoFi-Bank-Rate-Sheet-October-20-2026.pdf) |
| **Best Pure Unconditional `$0`-Min Base Rate** — Synchrony Bank HYSA (`3.55%` as of `2026-10-21`; use `$240k` single cap or Joint/POD) | **$8,875.00** | **3.55%** | `$8,875`* if Single | [Synchrony](https://www.synchrony.com/banking/products/hys-core) |
| **FDIC National Average Savings Benchmark (`2026-10-19`)** | **$950.00** | **0.38%** | **$0.00** | [FDIC National Rates](https://www.fdic.gov/national-rates-and-rate-caps) |
| **Standard Megabank Branch Tier** — Wells Fargo Way2Save / Truist One (`0.01%`) | **$25.00** | **0.01%** | **$0.00** | [Wells Fargo](https://www.wellsfargo.com/savings-cds/way2save/) · [Truist](https://www.truist.com/savings/truist-one-savings/disclosures-and-fees) |

---

## Live Multi-Page Site Architecture

- **[`index.html`](https://sassnarep3-star.github.io/SAVINGS2/)** — Executive Dashboard, SVG Yield/Return Visualizations, Live Custom Return & FDIC Coverage Calculator, and Searchable 25-Account Master Table
- **[`national-banks.html`](https://sassnarep3-star.github.io/SAVINGS2/national-banks.html)** — All 25 National Bank Products + Federal Reserve Consolidated Assets & FDIC Certificate Registry
- **[`returns-by-deposit.html`](https://sassnarep3-star.github.io/SAVINGS2/returns-by-deposit.html)** — `$1,000`–`$1,000,000` Deposit Matrix × 6 Horizons (`3M`–`5Y`) & 5 Multi-Charter Max-FDIC Portfolios
- **[`rate-competitiveness.html`](https://sassnarep3-star.github.io/SAVINGS2/rate-competitiveness.html)** — Macro Spread Table (`FDIC`, `Fed H.15 EFFR`, `U.S. Treasury Par Curve`) & 5-Year Yield Decay Curve
- **[`promotions-bonuses.html`](https://sassnarep3-star.github.io/SAVINGS2/promotions-bonuses.html)** — All 9 Primary-Verified Cash Bonuses & Promotional Rate Boosts (`BOOST50`, `BONUS1500`, `Chase $900`, `SoFi $400`, `Barclays $200` exp. `2026-10-31`)
- **[`opening-rules.html`](https://sassnarep3-star.github.io/SAVINGS2/opening-rules.html)** — Minimum Opening Deposits, Exact Monthly Fee Waivers, Withdrawal Caps & Regional Eligibility Rules (incl. NYC Citibank Exclusion)
- **[`fdic-security.html`](https://sassnarep3-star.github.io/SAVINGS2/fdic-security.html)** — Statutory FDIC Coverage Categories, Shared-Charter Merger Traps (`CapOne/Discover`, `CIT/First Citizens`, `Citizens Access`), and App Security Audit
- **[`flagged-review.html`](https://sassnarep3-star.github.io/SAVINGS2/flagged-review.html)** — All 24 Flagged Unverified Values (`—`), Bank CMS Bugs, and Line-by-Line Repo Audit Catches (including `IRREG-AUDIT-01` fixing the `$6,250/yr` non-DD SoFi APY bug)
- **Preserved Multi-Session Reference Pages:** `accounts.html`, `returns.html`, `competitiveness.html`, `bonuses.html`, `fdic.html`, `flagged.html`, `methodology.html`

---

## Reproducible Build & Automated Audit Pipeline

```bash
python3 scripts/generate_datasets.py   # Regenerate primary-verified JSON datasets & ledger
python3 scripts/sync_legacy_banks.py   # Sync primary fixes into data/banks.json
python3 build.py                       # Build preserved v1 reference pages
python3 scripts/build_site.py          # Build Executive Dashboard + 7 deep-dive subpages
python3 check_links.py                 # Run preserved link auditor
python3 scripts/verify_all.py          # Run full data, math, blank-cell & local HTTP audit
```
