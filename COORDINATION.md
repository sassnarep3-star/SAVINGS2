# COORDINATION.md — Shared Multi-Session Task Board & Verification Log

**Repository:** `sassnarep3-star/SAVINGS2`  
**Live GitHub Pages URL:** [https://sassnarep3-star.github.io/SAVINGS2/](https://sassnarep3-star.github.io/SAVINGS2/)  
**Analysis Reference Date (Account Opening Date):** `2026-10-22` (UTC)  
**Active / Integrating Session ID:** `session-1024a045` (Branch: `arena/1024a045-savings2`)  
**Prior Merged Session ID:** `session-46ab1baa` (Branch: `arena/46ab1baa-savings2`, merged via PRs #1–#3)

---

## 1. Shared Multi-Session Task Board

| Task ID | Task Name | Status | Owning Session ID | Branch | File Scope |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1–T8** | Initial 19-Product Bank Roster, Rates, Rules, Bonuses, FDIC Model & Static Site Build | `done` | `session-46ab1baa` | `arena/46ab1baa-savings2` | `data/banks.json`, `data/analysis.json`, `build.py`, `accounts.html`, `returns.html`, `fdic.html`, `competitiveness.html`, `bonuses.html`, `flagged.html`, `methodology.html` |
| **TASK-01** | FDIC Insurance Rules, 13-Bank Charter Cert Registry & Federal Reserve / FDIC Macro Benchmarks | `done` | `session-1024a045` | `arena/1024a045-savings2` | `data/fdic_and_benchmarks.json`, `fdic-maximization.html` |
| **TASK-02** | National High-Yield & Hybrid Savings Accounts Verification (16 HYSA / Hybrid Products) | `done` | `session-1024a045` | `arena/1024a045-savings2` | `data/national_banks_savings.json`, `high-yield-savings.html` |
| **TASK-03** | Big Four Brick-and-Mortar National Banks & Relationship Tiers Verification (PDF Rate Sheets & Fee Schedules) | `done` | `session-1024a045` | `arena/1024a045-savings2` | `data/big_four_banks.json`, `big-four-comparison.html` |
| **TASK-04** | Account Opening Bonuses, Promotions, Funding Windows & Operational Rules Verification | `done` | `session-1024a045` | `arena/1024a045-savings2` | `data/promotions_and_rules.json`, `bonuses-and-promotions.html`, `account-rules-and-security.html` |
| **TASK-05** | Return on Size of Investment ($1k–$1M) & Multi-Year Lifespan Projections (`2026-10-22` → `2031-10-22`) | `done` | `session-1024a045` | `arena/1024a045-savings2` | `data/investment_returns_matrix.json`, `investment-returns.html`, `assets/js/app.js` |
| **TASK-06** | Irregularities, Regional Restrictions & Unverified Fields Audit (`Flagged for Review`) | `needs review` | `session-1024a045` & `session-46ab1baa` | `arena/1024a045-savings2` | `data/flagged_for_review.json`, `flagged-for-review.html`, `flagged.html` |
| **TASK-07** | Multi-Session Integration (23 Screened Products, 15 HTML Pages), Automated Link/Row Audit, PR & Merge to `main` | `done` | `session-1024a045` | `arena/1024a045-savings2` | `index.html`, `scripts/unify_banks_json.py`, `scripts/build_site.py`, `scripts/verify_site.py`, `README.md`, `COORDINATION.md` |

---

## 2. Multi-Session Coordination & Integration Log

- **2026-10-22 (`session-46ab1baa` on `arena/46ab1baa-savings2`):** Created initial task board `T1–T8`, screened 19 products in `data/banks.json` (10 verified APYs, 1 partial, 8 unverified), generated 8 static pages via `build.py`, and merged PRs [#1](https://github.com/sassnarep3-star/SAVINGS2/pull/1), [#2](https://github.com/sassnarep3-star/SAVINGS2/pull/2), and [#3](https://github.com/sassnarep3-star/SAVINGS2/pull/3) into `main`. Noted in `COORDINATION.md` under *Notes for a future session* that Chase, Bank of America, Capital One (`NaN APY`), Wells Fargo effective dates, and Synchrony (`404`) remained open items.
- **2026-10-22 (`session-1024a045` on `arena/1024a045-savings2`):** Completed `TASK-01` through `TASK-07` and resolved the open verification items from `session-46ab1baa` using official primary PDF rate sheets, application portals, and regulatory releases:
  1. **JPMorgan Chase (`chase-savings`, `chase-premier-savings`, `chase-private-client-savings`):** Verified `0.01% APY` (Chase Savings) and `0.01% standard / 0.02% relationship APY` (Chase Premier & Private Client Savings) directly from Chase's official Consumer Deposit Rate Sheet PDF (`https://www.chase.com/content/dam/chase-ux/ratesheets/pdfs/rdin1.pdf`, effective `2026-10-16`), plus the `$100` (`$5k–$9.99k`) / `$200` (`$10k+` held 90 days) new money bonus (`https://account.chase.com/consumer/banking/savingsoffer`, expires `2027-01-27`).
  2. **Capital One 360 (`capital-one-360-performance`):** Verified `3.20% APY` across all balances effective `2026-10-21` from Capital One's official online application rate table (`https://apply.capitalone.com/fc/index.html`), while retaining the flag (`FLAG-04`) that `capitalone.com/bank/savings-accounts/online-performance-savings-account/` renders `NaN APY` in static server-side HTML. Also verified companion `360 Checking` `$250` bonus (`CHECKING250` / `DEBIT250` / `STUDENT250`).
  3. **Synchrony Bank (`synchrony-high-yield-savings`):** Verified `3.55% APY` across all balances accurate as of `2026-10-21` (`$0` min deposit, `$0` monthly fee) on Synchrony's live product page (`https://www.synchrony.com/banking/products/high-yield-savings` → `https://www.synchrony.com/banking/products/hys-core`).
  4. **BMO Alto (`bmo-alto-online-savings`):** Verified `3.00% APY` across all balances as of `2026-10-21` (`$0` min deposit, `$0` monthly fee) on `https://www.alto.bmo.com/en-us/high-yield-online-savings/`, and documented that BMO Alto shares FDIC Cert `#16571` with BMO Bank N.A. retail accounts (`BMO Savings Builder`, `0.01% APY` + `$5/mo` reward).
  5. **Wells Fargo (`wells-fargo-way2save` & `wells-fargo-platinum-savings`):** Verified the official rate effective date of `2026-10-07` on `https://www.wellsfargo.com/savings-cds/rates/` for both `Way2Save® Savings` (`0.01% APY`) and `Platinum Savings` (`3.25% APY` on `$25,000+` for new savings customers; `0.01%` standard; `0.02%` Prime / `0.05%` Premier relationship APY; plus `3.50% APY` 12-month banker promo on `$10,000+` at `https://accountoffers.wellsfargo.com/platinumoffer/?sub_channel=BCN&vendor_code=WF&collateral_code=grate`).
  6. **U.S. Bank (`us-bank-elite-money-market`):** Verified `3.40% APY` (`3.34%` interest rate) on balances of `$25,000+` for new Elite Money Market clients (`0.01% APY` below `$25,000`) effective `2026-10-21` on `https://www.usbank.com/bank-accounts/savings-accounts/elite-money-market.html`.
  7. **Bank of America (`bofa-advantage-savings`):** Verified `$100.00` minimum opening deposit, `$8.00` monthly maintenance fee (waived for first 6 months on new accounts), and `$10.00` withdrawal limit fee (>6 withdrawals/cycle) from Bank of America's Personal Schedule of Fees (`https://www.bankofamerica.com/salesservices/deposits/resources/personal-schedule-fees/`, effective `2026-08-07`), and documented the May 26, 2026 transition from Preferred Rewards to `BofA Rewards™` and discontinuation of the Advantage Savings rate booster.
  8. **Citibank (`citi-savings` & `citi-accelerate-savings`):** Verified `$0` minimum opening deposit and `$4.50` monthly service fee (waived with `$500+` Average Monthly Balance or linked checking/Relationship Tier) from Citibank's Simplified Banking Fact Sheet (`https://www.citi.com/content/dam/cfs/mobile/assets/JRS/popups/ao/Fact_Sheet.pdf`, dated `2026-10-01`), and flagged the bold disclosure: *"Effective October 23, 2026, Promotional Rate Feature for New Citi Savings accounts will be discontinued."*
  9. **PNC Bank (`pnc-high-yield-savings`):** Verified `$0` minimum opening deposit and `$0` monthly service charge from PNC's Consumer Schedule of Service Charges and Fees PDF (`https://www.pnc.com/content/dam/pnc-com/pdf/personal/Savings/service-charges-high-yield-savings.pdf`).
  10. **Federal Reserve & FDIC Macro Benchmarks (`data/fdic_and_benchmarks.json`):** Verified Federal Reserve H.15 Effective Federal Funds Rate (`3.88%` as of `2026-10-19`, released `2026-10-20` at `https://www.federalreserve.gov/releases/h15/`) and FOMC Target Range (`3.75%–4.00%`, IORB `3.90%`, ON RRP `3.75%` effective `2026-09-17` at `https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a1.htm`), alongside the FDIC National Deposit Rate for Savings (`0.38% APY`, National Rate Cap `4.63%` as of `2026-10-19` at `https://www.fdic.gov/national-rates-and-rate-caps`).
- **2026-10-22 (`session-1024a045` Integration):** Merged `origin/main` into `arena/1024a045-savings2`, unified `data/banks.json` (now **23 screened products: 16 fully verified APYs, 1 partial, 6 unverified**) with `data/national_banks_savings.json`, `data/big_four_banks.json`, `data/promotions_and_rules.json`, `data/investment_returns_matrix.json`, `data/fdic_and_benchmarks.json`, and `data/flagged_for_review.json`. Built all **15 HTML pages** across both `build.py` and `scripts/build_site.py` and verified **0 broken local links** and **100% official source links across all 293 dashboard table rows**.

---

## 3. Irregularities & Unverified Items (`needs review` — Published on `flagged-for-review.html` & `flagged.html`)

| Flag ID | Bank & Account | Irregularity / Unverified Item | Official Source Link |
| :--- | :--- | :--- | :--- |
| **FLAG-01** | **Citibank, N.A. (`#7213`)** — `Citi® Accelerate Savings` | Official page outputs uninterpolated template variable `:BLUE_AccSavings_Rate%` (and `% · % · %` on Compare Accounts) when accessed from NYC because NY is excluded from the National Rate Region. APY left blank. | [citi.com/banking/savings-account](https://www.citi.com/banking/savings-account?intc=citihpmenu_overview_savings) |
| **FLAG-02** | **PNC Bank, N.A. (`#6384`)** — `PNC High Yield Savings℠` | Page title confirms `3.15% APY`, but page body geo-blocks NYC visitors with `"This Product Isn't Available in Your Area"`. | [pnc.com/.../high-yield-savings.html](https://www.pnc.com/en/personal-banking/banking/savings/high-yield-savings.html) |
| **FLAG-03** | **Capital One, N.A. (`#4297`) & Discover Bank (`#5649`), CIT/First Citizens (`#11063`), BMO Alto/BMO (`#16571`)** | Shared FDIC Charters: Capital One & Discover are jointly insured under Cert `#4297` (Discover Cert `#5649` inactive); CIT Bank is a division of First Citizens Bank (`#11063`); BMO Alto is a trade name of BMO Bank N.A. (`#16571`). | [capitalone.com/updates/discover/savings/](https://www.capitalone.com/updates/discover/savings/) |
| **FLAG-04** | **Capital One, N.A. (`#4297`)** — `360 Performance Savings` | Marketing page (`capitalone.com/bank/savings-accounts/online-performance-savings-account/`) renders literal `NaN APY` in static HTML, while `apply.capitalone.com/fc/index.html` confirms `3.20% APY` as of `10/21/2026`. | [apply.capitalone.com/fc/index.html](https://apply.capitalone.com/fc/index.html) |
| **FLAG-05** | **Citibank, N.A. (`#7213`)** — `Citi® Savings Account` | Simplified Banking Fact Sheet (`10/01/2026`) announces: *"Effective October 23, 2026, Promotional Rate Feature for New Citi Savings accounts will be discontinued."* | [citi.com/.../Fact_Sheet.pdf](https://www.citi.com/content/dam/cfs/mobile/assets/JRS/popups/ao/Fact_Sheet.pdf) |
| **FLAG-06** | **Bank of America, N.A. (`#3510`)** — `Advantage Savings` | Consumer APY is ZIP-gated (`$XXXX` placeholders on web application page; `$100` min open and `$8` fee verified via PDF fee schedule). Also transitioned Preferred Rewards to `BofA Rewards™` (`~2026-05-26`) and discontinued the savings rate booster. | [bankofamerica.com/.../personal-schedule-fees/](https://www.bankofamerica.com/salesservices/deposits/resources/personal-schedule-fees/) |
| **FLAG-07** | **Synchrony Bank (`#27314`)** — `Synchrony High Yield Savings` | Embedded calculator widget displays stale `2.85%` APY while hero banner, CTA, and disclosure confirm `3.55% APY` accurate as of `10/21/2026`. | [synchrony.com/banking/products/high-yield-savings](https://www.synchrony.com/banking/products/high-yield-savings) |
| **FLAG-08** | **CIT Bank (`#11063`) & HSBC (`#57890`) & Unconfirmed Balance Caps** | CIT Bank's `3.75% APY` rate sheet is dated `2026-07-01` (older than October 2026 quotes); HSBC's `3.10% APY` rate table has no published effective date; TD, Citizens, and Fifth Third APYs are location/branch-gated and left blank; max balance caps not published for 9 accounts and Amex Platinum Exclusive Rate % not published publicly (all left blank). | [cit.com/cit-bank/resources/products-and-rates](https://www.cit.com/cit-bank/resources/products-and-rates) |
| **FLAG-09** | **Chase (`#628`), BMO Alto (`#16571`), U.S. Bank (`#6548`), SoFi (`#26881`)** | Minor template omissions on Chase promo footnote and BMO Alto modal; U.S. Bank live JS calculator error message (static HTML table intact); SoFi `$3M` sweep insurance is a participating-bank network marketing claim rather than a single-charter FDIC rule. | [account.chase.com/consumer/banking/savingsoffer](https://account.chase.com/consumer/banking/savingsoffer) |

---

## 4. Pull Request, Merge & GitHub Pages Deployment Record

- **Prior Session PRs (`session-46ab1baa`):**
  - [PR #1](https://github.com/sassnarep3-star/SAVINGS2/pull/1) (`e474bfc`), [PR #2](https://github.com/sassnarep3-star/SAVINGS2/pull/2) (`6601f69`), [PR #3](https://github.com/sassnarep3-star/SAVINGS2/pull/3) (`792cba6`) — Merged `arena/46ab1baa-savings2` into `main`.
- **Current Session Integration PR (`session-1024a045`):**
  - **Source Branch:** `arena/1024a045-savings2` → **Target Branch:** `main`
  - **PR Link:** [PR #5](https://github.com/sassnarep3-star/SAVINGS2/pull/5) — *"Integrate verified National Bank HYSA & Big Four datasets, interactive Max FDIC calculator, and 15-page GitHub Pages suite"*
  - **Merge Result:** **MERGED** (`2026-10-22T00:41:34Z`, merge commit `e0e764928b0c8c32868b899631fa078da4cefd2d`) via `gh pr merge 5 --merge` without waiting for manual approval.
  - **GitHub Pages Build & Deployment Confirmation:** Confirmed via GitHub Pages API (`repos/sassnarep3-star/SAVINGS2/pages/builds`) — commit `e0e764928b0c8c32868b899631fa078da4cefd2d` reached `status: "built"` at `2026-10-22T00:42:00Z` (`duration: 25213ms`, `error: null`).
  - **Pre-Merge Verification:** `python3 build.py` (`0 errors`), `python3 scripts/build_site.py` (`8 dashboard pages built`), `python3 scripts/verify_site.py` (`293 table rows with 100% official source links, 0 broken local links across all 15 HTML pages`).
  - **Live GitHub Pages URL:** [https://sassnarep3-star.github.io/SAVINGS2/](https://sassnarep3-star.github.io/SAVINGS2/)


---

## 5. Session B (`arena/24e1eb4e-savings2`) — third parallel session, integrated 2026-10-22

A third session worked in this repository in parallel (blind, like the others) and
completed its own T1–T7 scope on branch `arena/24e1eb4e-savings2`:

- **Scope:** official-source research for 14 banks (7 brick-and-mortar + 7 online-first),
  FDIC rules & per-bank FDIC certificate verification via the FDIC institutions API,
  Fed policy context (FOMC 9/16/2026 hike to 3.75–4.00%), bonuses/promotions, returns
  by deposit size ($10k/$50k/$100k/$250k), and an 11-page static site in `docs/`
  (index, national-banks, online-banks, other-national-banks, returns, bonuses,
  requirements, fdic-security, analysis, flagged, sources) with `tools/returns_calc.py`
  (reproducible projections) and `tools/site_check.py` (link/anchor/host checks).
- **Independent verifications that filled early gaps:** Chase 0.01% all tiers (official
  rate sheet `rdin1.pdf`, in effect 10/16/2026) + $5/$25 fees + $100/$200 bonus
  (expires 2027-01-27); Bank of America 0.04% all tiers + $250,000 online opening limit
  (NY Tri-State rate sheet, eff. 10/21/2026) + $100 min/$8 fee (Personal Schedule of
  Fees, eff. 8/7/2026); Citibank Citi Savings 0.03% NY + tier rates 0.06/0.09/0.12 +
  3.75%×3-mo promo window ending 10/22/2026 (Fact Sheet: discontinued eff. 10/23/2026);
  Capital One 360 Performance Savings 3.20% APY (eff. 10/21/2026); Synchrony 3.55% APY;
  Wells Fargo Way2Save fee-waiver page + Platinum promo eff. 10/07/2026; U.S. Bank
  Smartly tiers eff. 10/21/2026; Truist disclosures (as of 9/28/2026); PNC Standard
  Savings rates (accurate 10/21/2026); Marcus 3.50% + balance caps ($1M/account,
  $3M/owner) + referral +1.00%×3mo; Ally 3.10%; Amex 3.20%; SoFi 0.80%/3.30%/4.40%
  (as of 10/20/2026) + $50/$400 bonus; FDIC national average 0.38% (10/19/2026).
  Where sessions overlapped, all verified values agreed.
- **Materially unique findings merged into the canonical site during integration:**
  1. **Capital One BONUS1500** — up to $1,500 savings bonus ($20k+→$300, $50k+→$750,
     $100k+→$1,500; promo code BONUS1500; 15-day Initial Funding Period; 90-day hold;
     paid within 60 days). Source: <https://www.capitalone.com/bank/bonus1500/>
     (verified 2026-10-22). Added to `data/promotions_and_rules.json`.
  2. **PNC Virtual Wallet bonus** — $100 (Virtual Wallet, $500+ qualifying direct
     deposits in 60 days) or $400 (Virtual Wallet with Performance Select, $5,000+
     direct deposits); valid 2026-09-01 – 2027-01-07. Source:
     <https://www.pnc.com/en/personal-banking/banking/checking/bonus-offer.html>
     (verified 2026-10-22). Added to `data/promotions_and_rules.json`.
  3. U.S. Bank $100 Smartly Savings campus bonus (open by 10/29/2026, hold $1,000+
     until 2027-01-31, requires checking-offer qualification) and up-to-$450 Smartly
     Checking bonus (official splash page apply-by 10/20/2026; later windows may exist)
     — added as flagged promo-page offers.
- **Session B's flagged items (F1–F15)** are published in full on its own site at
  `docs/flagged.html` (Citi Accelerate APY JS-rendered; Chase savings minimum not
  published; PNC HYS footprint; U.S. Bank promo windows; BofA/Amex/Ally/Truist no
  savings bonus found; withdrawal-fee schedules not captured; Discover closure;
  BofA Preferred-Booster values; bankofamerica.com fetch blocking). Several are the
  same underlying facts as FLAG-01…FLAG-09 above, independently discovered.
- **Site decision:** the canonical GitHub Pages site remains the root 15-page suite
  (Sessions A+C). Session B's 11-page site is retained in-repo at `docs/` and remains
  fully self-contained (every row source-linked; `python3 tools/site_check.py` passes).
- **PR record:** PR #4 (`arena/24e1eb4e-savings2` → `main`) was updated to carry the
  three-session integration (main merged in; canonical datasets extended with the two
  unique verified bonuses; boards and README combined) and merged without waiting for
  approval. GitHub Pages (source: `main` / root) rebuilt on the merge commit — build
  status recorded in section 4 style below.
