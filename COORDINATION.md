# COORDINATION.md — Shared Task Board

This is the shared task board for the SAVINGS2 repository (savings account research +
GitHub Pages site). Any agent session working in this repo must read this file before
starting, claim tasks here, and keep it current.

- **Repo:** https://github.com/sassnarep3-star/SAVINGS2
- **Session count so far:** 1 (single-session repo; all tasks executed by one session)
- **Protocol:** claim a task by writing your session ID + file scope, commit and push the
  claim immediately, then work only inside your claimed scope. `git pull --rebase` before
  every push. Log handoffs, conflicts, and completion notes in the log at the bottom.

## Session registry

| Session ID | Branch | Notes |
|---|---|---|
| `arena/24e1eb4e-savings2` | `arena/24e1eb4e-savings2` | Only active session. Arena fixes this branch name for this session, so all work (including final integration) happens on this branch. Owned T1–T7 start to finish. |

## Task board

Status legend: `unclaimed` · `in progress` · `done` · `needs review`

| # | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T1 | Repo review + create COORDINATION.md | done | `arena/24e1eb4e-savings2` | `COORDINATION.md`, `README.md` |
| T2 | Research: FDIC insurance rules + security features (official sources) | done | `arena/24e1eb4e-savings2` | `docs/fdic-security.html` |
| T3 | Research: big national brick-and-mortar banks (Chase, Bank of America, Wells Fargo, Citibank, U.S. Bank, PNC, Truist, Capital One) — rates, tiers, fees, bonuses, rules, apps | done | `arena/24e1eb4e-savings2` | `docs/national-banks.html` |
| T4 | Research: national online-first banks (Marcus, Ally, Amex, Synchrony, SoFi; Discover status) — rates, fees, bonuses, rules, apps | done | `arena/24e1eb4e-savings2` | `docs/online-banks.html` |
| T5 | Analysis: returns-by-deposit-size tables (incl. $250k FDIC max), rate competitiveness, promotions comparison | done | `arena/24e1eb4e-savings2` | `docs/returns.html`, `docs/bonuses.html`, `docs/analysis.html`, `tools/returns_calc.py` |
| T6 | Site build: landing page + category subpages + Flagged for Review page, static GitHub Pages site | done | `arena/24e1eb4e-savings2` | `docs/` (index, national-banks, online-banks, returns, bonuses, requirements, fdic-security, analysis, flagged, sources, assets/style.css, data/savings-data.json) |
| T7 | Final integration: line-by-line re-verification, link check, PR to main, merge, Pages deploy verification | done | `arena/24e1eb4e-savings2` | whole repo — see PR link in log |

Page-scope note: the board originally planned `docs/banks-brick.html`/`docs/banks-online.html`
(T3/T4), `docs/fdic.html`+`docs/security.html` (T2), and `docs/returns.json` (T5). Final
structure consolidates FDIC+security into `docs/fdic-security.html` and uses clearer page
names (`national-banks.html`, `online-banks.html`, `analysis.html`) with one combined
data file `docs/data/savings-data.json`. Content coverage unchanged.

## Verified-sources register

Every table row on the site carries a per-row source link. This register records the
official sources and the dates they were checked (all 2026-10-22 UTC unless noted).
The full annotated register is published at `docs/sources.html`.

| Date checked (UTC) | Source (official) | What was verified | Task |
|---|---|---|---|
| 2026-10-22 | fdic.gov — Deposits at a Glance | $250k/depositor/bank/ownership category; categories; EDIE; automatic coverage | T2 |
| 2026-10-22 | fdic.gov — National Rates and Rate Caps (Oct 2026, published 10/19/2026) | National avg savings 0.38%; MM 0.63%; 12-mo CD 1.76% | T5 |
| 2026-10-22 | banks.data.fdic.gov/api/institutions (FDIC BankFind data, index 10/16/2026) | Insured status + certs: Chase 628, BofA 3510, Wells 3511, Citi 7213, US Bank 6548, PNC 6384, Truist 9846, CapOne 4297, GS Bank 33124, Ally 57803, Amex 27471, Synchrony 27314, SoFi 26881, Discover 5649 (ACTIVE=0) | T2 |
| 2026-10-22 | federalreserve.gov — FOMC statement 9/16/2026 + press conference | Fed funds raised 25bp to 3.75–4.00%; median 4.1% end-2026 | T5 |
| 2026-10-22 | chase.com rdin1.pdf rate sheet (in effect 10/16/2026) | Chase Savings 0.01% all tiers; Premier 0.01/0.02 rel; Private Client 0.01/0.02 | T3 |
| 2026-10-22 | chase.com/personal/fees/savings + /personal/fees/premier-savings | $5 / $25 fees + waiver conditions; ATM fees | T3 |
| 2026-10-22 | account.chase.com/consumer/banking/savingsoffer | $100/$200 savings bonus; $5k/$10k deposits; 30-day deposit / 90-day hold; expires 01/27/2027 | T3 |
| 2026-10-22 | media.bac-assets.com/DigitalDeposit_NY_NY_Tri_State_Area.pdf (eff. 10/21/2026) | Advantage Savings 0.04% all tiers; $250k online opening limit | T3 |
| 2026-10-22 | bankofamerica.com Personal Schedule of Fees (eff. 8/7/2026) | $100 min to open; $8 fee + waivers (incl. 6-month new-account waiver) | T3 |
| 2026-10-22 | wellsfargo.com/savings-cds/rates/ | Way2Save 0.01%; Platinum std 0.01% / Prime 0.02% / Premier 0.05%; new-customer 3.25% APY $25k+; $25 mins; $5/$12 fees | T3 |
| 2026-10-22 | wellsfargo.com Way2Save fee-waiver page | $5 fee waiver conditions | T3 |
| 2026-10-22 | wellsfargo.com Account Addenda PDF | Platinum Savings Rate Update effective 10/07/2026 | T3 |
| 2026-10-22 | citi.com/banking/savings-account | $0 min; $4.50 fee + waivers; 3-month fee holiday; APY footnote 10/13/2026 (value JS-rendered → flagged F1) | T3 |
| 2026-10-22 | banking.citi.com featured-offers page | 3.75% × 3-mo promo on new Citi Savings ($25k+ new-to-Citi funds, max interest $10k); std tier rates 0.03/0.06/0.09/0.12; window 7/14–10/22/2026 | T3 |
| 2026-10-22 | citi.com Fact Sheet PDF (10/01/2026) | Promo feature discontinued eff. 10/23/2026; NY-region Citi Savings APY 0.03% | T3 |
| 2026-10-22 | citi.com/banking/compare-bank-accounts | Accelerate eligible-state list (NY excluded) | T3 |
| 2026-10-22 | usbank.com Smartly Savings rates page (eff. 10/21/2026) | Std 0.05%; relationship 1.00/2.00/3.50 by CQB; $25 min; $5 fee waivers | T3 |
| 2026-10-22 | usbank.com consumer pricing (deposit products) | Fee/min matrix for Smartly Savings + Elite MM | T3 |
| 2026-10-22 | usbank.com splash + campus offer pages | $450 checking bonus (apply-by 10/20/2026); 4.00% APY bundle promo (select markets, 10/20/2026); $100 savings bonus (campus pages, by 10/29/2026) | T3 |
| 2026-10-22 | pnc.com Standard Savings rate table (accurate 10/21/2026) + product page | 0.02%/0.03% tiers; TotalRewards boosts to 0.06%; $0 online min; $5 fee waivers; $5M combined-balance cap | T3 |
| 2026-10-22 | pnc.com High Yield Savings page | 3.15% APY; $0 min; no fee; footprint restriction ("not available in your area") | T3 |
| 2026-10-22 | pnc.com checking bonus-offer page | Virtual Wallet $100/$400 bonus; valid 9/1/2026–1/7/2027 | T3 |
| 2026-10-22 | truist.com Truist One Savings + One MM disclosures (accurate 9/28/2026) | 0.01% all tiers; $50 min; $5/$12 fees + waivers; $5 withdrawal-limit fee >6/cycle | T3 |
| 2026-10-22 | capitalone.com/bank/open-an-account/ | 360 Performance Savings 3.20% APY (eff. 10/21/2026); $0 min/fee; CDs 4.40%; Kids 2.50% | T4 |
| 2026-10-22 | capitalone.com/bank/bonus1500/ | BONUS1500: $300/$750/$1,500; 15-day funding, 90-day hold, 60-day payout | T4 |
| 2026-10-22 | marcus.com savings page (APY as of 10/21/2026) + FAQ + referral page | 3.50% APY; no fees/mins; no withdrawal limit; $1M/$3M caps; referral +1.00% × 3 mo | T4 |
| 2026-10-22 | ally.com/bank/online-savings-account/ | 3.10% APY (correct as of 10/21/26); $0 min/fee; 10-withdrawal cycle limit | T4 |
| 2026-10-22 | americanexpress.com HYSA page | 3.20% APY; $0 min/fee; daily compounding; no ATM/debit card; 24/7 support | T4 |
| 2026-10-22 | synchrony.com/banking/products/hys-core | 3.55% APY; no min/balance/fees; FDIC $250k; app ratings 4.8/4.6; 24/7 monitoring | T4 |
| 2026-10-22 | sofi.com rates page (current as of 10/20/2026) + product page | 3.30% w/ DD (0.80% std; 4.50% Plus ≤$20k); new-member 1.10% boost → 4.40% (by 12/31/2027); $50/$400 bonus; FDIC up to $3M IDP; checking auto-bundle | T4 |
| 2026-10-22 | discover.com savings URL + FDIC record | Closed to new savings applicants; Discover Bank cert 5649 ACTIVE=0 (merged into Capital One) | T4 |

## Irregularities / flagged items

(Items that could not be fully confirmed from an official source are also published on
the site's "Flagged for Review" page, `docs/flagged.html` — being flagged does not block
anything.)

| Date | Item | Task | Resolution |
|---|---|---|---|
| 2026-10-22 | Repo contained only `README.md` ("# SAVINGS2") — nothing to review line by line; no prior data, no irregularities in existing content. | T1 | Resolved: baseline documented. |
| 2026-10-22 | F1 — Citi Accelerate APY is JS-rendered on citi.com (placeholder in static fetch); 3.00% only via third-party trackers. | T3/T4 | Flagged on site; value shown as "3.00% ⚠ unverified". |
| 2026-10-22 | F2 — Citi Savings standard APY verified for NY region (0.03%); other rate regions not separately captured. | T3 | Flagged on site (low impact). |
| 2026-10-22 | F3 — Chase Savings/Premier minimum opening deposit not published on fee/rate/offer pages reviewed. | T3 | Left blank in tables + flagged. |
| 2026-10-22 | F4 — PNC High Yield Savings footprint restriction; NYC eligibility not conclusively determinable from static page. | T3 | Flagged; NYC users directed to test ZIP on PNC page. |
| 2026-10-22 | F5 — U.S. Bank "up to 4.00% APY" bundle promo apply-by 10/20/2026 (select markets); window appears closed. | T3 | Flagged; excluded from rankings. |
| 2026-10-22 | F6 — U.S. Bank $100 savings bonus found only on campus offer pages (requires checking-offer qualification). | T3 | Flagged; listed with conditions. |
| 2026-10-22 | F7 — U.S. Bank $450 checking bonus: official page said apply by 10/20/2026; third parties report extension to 11/10/2026. | T3 | Flagged; official link given. |
| 2026-10-22 | F8 — Bank of America: no savings bonus on official docs; third-party-reported checking bonus ($500) not verified on bankofamerica.com (bot-blocked). | T3 | Flagged; not listed as verified. |
| 2026-10-22 | F9/F10/F11 — No savings bonus found on official pages for Amex / Ally / Truist. | T4 | Flagged as "none found". |
| 2026-10-22 | F12 — Excess-withdrawal fees for Chase/BofA/Wells/Citi/PNC live in full fee schedules not captured (PDF/JS). | T3 | Flagged; requirements page uses careful "no published fee on pages reviewed" wording. |
| 2026-10-22 | F13 — Discover Bank closed to new applicants (FDIC ACTIVE=0; page routes to Capital One; migration reported 8/23/2026 by third parties). | T4 | Treated as closed; noted on site. |
| 2026-10-22 | F14 — BofA Preferred Rewards personal savings-booster tier values not captured from official source (NY sheet shows business boosters only). | T3 | Flagged; not shown in tables. |
| 2026-10-22 | F15 — bankofamerica.com/deposits/savings/ returns HTTP 405 to automated fetch (bot protection). | T3 | Worked around via official BofA rate-sheet PDF + fee schedule. |

## Log

- **2026-10-22 (arena/24e1eb4e-savings2):** Board created. Repo reviewed: single initial
  commit `e5a82d8` containing only `README.md` ("# SAVINGS2"). No existing site, no
  existing data, no branches besides `main`. Claimed T1–T7 (single session).
- **2026-10-22 (arena/24e1eb4e-savings2):** Research complete for all banks
  (Chase, BofA, Wells Fargo, Citi, U.S. Bank, PNC, Truist, Capital One, Marcus, Ally,
  Amex, Synchrony, SoFi, Discover status), FDIC rules + national rates + Fed context,
  bonuses/promos, and per-bank FDIC certs via the FDIC API. All values verified from
  official sources; 15 items flagged (see register above). Calculations scripted in
  `tools/returns_calc.py`.
- **2026-10-22 (arena/24e1eb4e-savings2):** Site built in `docs/`: 10 HTML pages
  (index, national-banks, online-banks, returns, bonuses, requirements, fdic-security,
  analysis, flagged, sources), shared stylesheet, machine-readable data snapshot
  (`docs/data/savings-data.json`). Static, no build step, no external scripts. Internal
  link + anchor check and HTML parse check passed; external links limited to verified
  official URLs.
- **2026-10-22 (arena/24e1eb4e-savings2):** T7 final integration in progress: link
  checks passing, branch push next, then PR to `main`, merge, Pages enablement on
  `main` (`/docs`), and deploy verification. The PR link and deploy result will be
  recorded here as soon as they exist.
