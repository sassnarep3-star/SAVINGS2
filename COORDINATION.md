# COORDINATION — Savings Account Research (SAVINGS2)

Shared task board. Read this before doing any work. Last updated: **2026-10-22
(cross-session integration complete)**.

## Session protocol

- Session IDs are prefixed `session-`. Two Arena sessions worked in this repository on
  2026-10-22. Each was required to use its own Arena-tracked branch name, so each served
  as its own working/integration branch:
  - **session-46ab1baa** — branch `arena/46ab1baa-savings2` (Session A)
  - **arena/24e1eb4e-savings2** — branch `arena/24e1eb4e-savings2` (Session B; this ID
    is both board ID and branch name)
- Claim a task by writing your session ID + file scope, then commit and push the claim
  **before** starting work. Keep scopes non-overlapping; if you need a file owned by
  another session, log a request instead of editing it.
- `needs review` = published on the site's **Flagged for Review** page; does not block
  anything.
- Neither session saw the other's claim before starting: both began from the repo's
  initial state within minutes of each other, and the boards were merged afterwards.
  The work turned out complementary (see "Integration record" below).

## Session registry

| Session | Branch | Status | Scope |
| --- | --- | --- | --- |
| session-46ab1baa | `arena/46ab1baa-savings2` | done (T1–T8 complete; PRs #1–#3 merged; Pages enabled) | Root site (`index.html`, `*.html`, `assets/`), `data/banks.json`, `data/analysis.json`, `research/verification-log.md`, `build.py`, `check_links.py`, `analysis/` |
| arena/24e1eb4e-savings2 | `arena/24e1eb4e-savings2` | done (T1–T7 complete; performed cross-session integration; PR #4 updated with the integration and merged) | `docs/` site + `docs/data/`, `tools/returns_calc.py`, `tools/site_check.py`, `README.md`, this board |

## Task boards (both sessions)

### Session A — session-46ab1baa

| ID | Task | Status | File scope |
| --- | --- | --- | --- |
| T1 | Bank roster + FDIC charter/insurance verification | **done** | `data/banks.json`, `research/fdic.md` |
| T2 | Official APY collection (dated, per bank) | **done** | `data/banks.json`, `research/rates.md` |
| T3 | Minimums, fees, opening rules, app, security | **done** | `data/banks.json`, `research/accounts.md` |
| T4 | Bonuses / promotional offers | **done** | `data/banks.json`, `research/bonuses.md` |
| T5 | Return-on-deposit analysis + FDIC coverage model | **done** | `analysis/`, `data/analysis.json`, `build.py` |
| T6 | Static site (landing + category subpages) | **done** | `index.html`, `assets/**`, `*.html` |
| T7 | Line-by-line verification pass + link check | **done** | `research/verification-log.md`, `check_links.py` |
| T8 | Integration, PR to `main`, Pages deploy | **done** | `COORDINATION.md` (PRs #1–#3 merged; Pages from root of `main`) |

Scope note (A): T1–T4 consolidated into one dataset file (`data/banks.json`) because they
share a single schema; research notes are sections of `research/verification-log.md`.

### Session B — arena/24e1eb4e-savings2

| # | Task | Status | File scope |
|---|---|---|---|
| T1 | Repo review + create COORDINATION.md | **done** | `COORDINATION.md`, `README.md` |
| T2 | Research: FDIC insurance rules + security features | **done** | `docs/fdic-security.html` |
| T3 | Research: big national brick-and-mortar banks | **done** | `docs/national-banks.html` |
| T4 | Research: national online-first banks | **done** | `docs/online-banks.html` |
| T5 | Analysis: returns by deposit size, competitiveness, promotions | **done** | `docs/returns.html`, `docs/bonuses.html`, `docs/analysis.html`, `tools/returns_calc.py` |
| T6 | Site build: landing + subpages + Flagged page | **done** | `docs/` (11 pages + assets + data) |
| T7 | Final integration: re-verification, link check, PR, merge, Pages | **done** | whole repo (this file records the outcome) |

Page-scope note (B): planned `docs/banks-brick.html`/`docs/banks-online.html` became
`docs/national-banks.html`/`docs/online-banks.html`; `docs/fdic.html`+`docs/security.html`
consolidated into `docs/fdic-security.html`; one combined data file
`docs/data/savings-data.json`. Content coverage unchanged.

## Integration record (2026-10-22, performed by Session B)

1. **Discovery:** PR #4 (Session B → main) could not merge cleanly because Session A had
   merged PRs #1–#3 to `main` in parallel. Session B reviewed Session A's board, dataset
   and verification log (`research/verification-log.md`), then performed the
   cross-session integration.
2. **Complementarity:**
   - Session A left **Chase, Bank of America, Citibank (APY), Capital One and Synchrony
     unverified** (JavaScript/ZIP/NaN gating, 404s). Session B verified all of these from
     official sources: Chase rate sheet PDF (0.01% all tiers, in effect 10/16/2026), BofA
     NY Tri-State rate sheet PDF (0.04% all tiers, eff. 10/21/2026, $250k online opening
     limit), Citi Fact Sheet + promo pages (Citi Savings 0.03% NY, tier rates
     0.06/0.09/0.12, 3.75% promo ended 10/22/2026), Capital One open-an-account page
     (360 Performance Savings 3.20% APY, eff. 10/21/2026) and Synchrony product page
     (3.55% APY; Session A's `synchronybank.com` URL 404'd — the working canonical URL is
     `synchrony.com/banking/products/hys-core`).
   - Session B did not cover **TD, Citizens, Fifth Third, HSBC, Barclays US, CIT**.
     Session A verified these (Barclays Tiered Savings 3.50%/3.65% as of 10/07/2026;
     CIT Platinum Savings 0.25%/3.75% as of 07/01/2026; HSBC 0.05%/3.10% no date;
     TD/Citizens/Fifth Third APYs blank on official pages). Session A's values are now
     published on `docs/other-national-banks.html` and reflected in the returns/bonus
     tables, with Session A's evidence links.
   - Both sessions independently verified: U.S. Bank Smartly tiers (0.05/1.00/2.00/3.50,
     eff. 10/21/2026), Truist One Savings 0.01% (as of 9/28/2026), Ally 3.10%
     (10/21/2026), Amex 3.20% (10/21/2026), Marcus 3.50% (10/21/2026), SoFi
     0.80/3.30/4.40 (10/20/2026), Wells Fargo Way2Save 0.01%, FDIC limits, FDIC national
     average 0.38% (10/19/2026), Discover Bank inactive (cert 5649). No conflicts found.
   - Security research merged: Session A captured per-bank security pages (chase.com
     privacy-security, capitalone.com security-fraud-protection, etc.); Session B
     captured product-page security statements. The `docs/` FDIC & security page
     references both.
3. **Site decision:** GitHub Pages now serves **`docs/`** from `main` (the integrated
   site with both sessions' data). Session A's root site is retained in the repository
   untouched, with its own dataset and log; nothing of Session A's was deleted.
4. **Flagged items:** Session A's irregularities I1–I10 and Session B's F1–F15 are both
   published on `docs/flagged.html`, with resolution notes where the other session's
   verification filled the gap.

## Verification summaries

### Session A (19 products; full quoted evidence in `research/verification-log.md`)
- 10 products with a fully verified APY, 1 partial (PNC HYS), 8 unverified-blank.
- FDIC charter status + cert number for all 19 entities via api.fdic.gov (index 2026-10-16).
- FDIC limits from three FDIC pages; benchmarks from the FDIC National Rates table
  (Oct 2026): savings 0.38%, Treasury 12m 4.54%.
- `build.py`: 8 pages, 0 validation errors; `check_links.py`: local links resolve.

### Session B (14 banks in `docs/`; register on `docs/sources.html`)
- 30 official sources checked 2026-10-21/22 (bank rate pages, fee schedules, offer
  pages, FDIC API records for 14 certs, FOMC statement + press conference).
- `tools/returns_calc.py`: reproducible projections; `tools/site_check.py`: internal
  links/anchors OK, external hosts allow-listed (bank + government domains only).

## Irregularities / flagged items (merged register)

All items are published on the site's Flagged for Review page (`docs/flagged.html`).
Being flagged does not block anything.

| ID | Session | Item | Resolution / status |
| --- | --- | --- | --- |
| I1 | A | Chase & BofA APYs ZIP-gated on public pages | **Resolved by B:** Chase rate-sheet PDF (0.01% all tiers, 10/16/2026); BofA NY Tri-State PDF (0.04% all tiers, 10/21/2026) |
| I2 | A | Capital One renders “NaN APY” on the product page | **Resolved by B:** open-an-account page shows 3.20% APY eff. 10/21/2026 (the bonus1500 offer page also renders NaN — footnote kept on flagged page) |
| I3 | A | BofA public page shows `$XXXX` fee placeholders | **Resolved by B:** Personal Schedule of Fees (eff. 8/7/2026): $100 min, $8 fee + waivers |
| I4 | A | Discover inactive; Capital One aggregates Discover accounts (opened on/after 2025-05-18) for FDIC coverage | Confirmed by both sessions; note incorporated on `docs/fdic-security.html` |
| I5 | A | CIT Bank is a division of First Citizens — deposits combine for coverage | Incorporated on `docs/other-national-banks.html` |
| I6 | A | CIT rate sheet dated 2026-07-01 (older than every other quote) | Kept with explicit date + flag on `docs/other-national-banks.html` |
| I7 | A | PNC 3.15% HYS is title-only; no effective date; footprint-restricted | Matches B's F4; PNC Standard rates verified by B (0.02%/0.03%, accurate 10/21/2026) |
| I8 | A | Wells Fargo & HSBC publish no rate effective date | WF promo effective date documented by B via account addenda (10/07/2026); HSBC kept with “no date published” note |
| I9 | A | SoFi's “up to $3M FDIC” is marketing about a partner-bank network | Kept as bank statement with that framing on `docs/fdic-security.html` |
| I10 | A | Synchrony & Schwab official savings URLs 404'd; dropped | **Synchrony resolved by B:** 3.55% APY verified at `synchrony.com/banking/products/hys-core`; Schwab remains excluded (no working official page found by either session) |
| F1 | B | Citi Accelerate APY JS-rendered (3.00% per trackers only) | Still flagged; shown as unverified |
| F2 | B | Citi Savings standard APY verified for NY region only | Kept flagged (low impact) |
| F3 | B | Chase savings minimum opening deposit not published on pages reviewed | Still flagged; blank in tables |
| F4 | B | PNC HYS NYC availability undeterminable from static page | Same as I7 |
| F5 | B | U.S. Bank 4.00% bundle promo window closed (apply-by 10/20/2026) | Kept flagged |
| F6 | B | U.S. Bank $100 savings bonus only on campus offer pages | Kept flagged |
| F7 | B | U.S. Bank $450 checking bonus expiry conflict (official page 10/20/2026 vs trackers 11/10/2026) | Kept flagged |
| F8 | B | BofA: no savings bonus on official docs | Kept flagged |
| F9–F11 | B | No savings bonus found: Amex / Ally / Truist | Kept flagged as “none found” |
| F12 | B | Excess-withdrawal fees (5 banks) in uncaptured PDF/JS schedules | Kept flagged; careful wording |
| F13 | B | Discover closed to new applicants | Same conclusion as I4 |
| F14 | B | BofA Preferred Rewards personal savings-booster values not captured | Kept flagged |
| F15 | B | bankofamerica.com blocks automated fetches (HTTP 405) | Method note; official PDFs used |

## Cross-session requests

None outstanding. (Both sessions worked blind in parallel; integration was performed
after the fact by Session B, as recorded above.)

## PR and merge record

| PR | From | Title | Result |
| --- | --- | --- | --- |
| #1 | `arena/46ab1baa-savings2` | Session A: dataset, analysis, static site | Merged (e474bfc) |
| #2 | `arena/46ab1baa-savings2` | Session A: post-merge corrections | Merged (6601f69) |
| #3 | `arena/46ab1baa-savings2` | Session A: README/known-gaps alignment | Merged (792cba6) |
| #4 | `arena/24e1eb4e-savings2` | Session B: verified research + `docs/` site, then updated with the cross-session merge (main integrated into the branch; session A's banks published on `docs/other-national-banks.html`; boards/README combined) | Merged — see log below for the final status |

## Log

- **2026-10-22 00:03 (A):** board created; T1–T8 claimed; repo empty.
- **2026-10-22 (A):** T1–T7 done; PR #1 opened/merged; Pages enabled from root of
  `main`; all 8 pages fetched live. T8 done.
- **2026-10-22 (A):** post-merge corrections (PRs #2–#3): per-size tier APYs, duplicate
  promo row, wording, footer counts, README/known-gaps alignment.
- **2026-10-22 (B):** board created in parallel (single session visible at the time);
  T1–T7 executed: official-source research for 14 banks + FDIC/Fed context + bonuses;
  `docs/` site built; link/anchor checks passing; pushed; PR #4 opened.
- **2026-10-22 (B, integration):** PR #4 initially conflicted with A's merged work.
  Reviewed A's board, dataset and verification log; merged `main` into the branch
  (conflicts in `COORDINATION.md`/`README.md` resolved by combining); published A's
  unique banks on `docs/other-national-banks.html`; merged A's irregularities (I1–I10)
  into `docs/flagged.html` with resolutions; added A's six certs to
  `docs/fdic-security.html`; extended the returns and bonuses tables with A's verified
  Barclays/CIT values; combined README; added A's sources to `docs/sources.html` and
  A's dataset snapshot to `docs/data/savings-data.json`. Pushed the integration to PR
  #4 and merged it. Pages source switched from root to `main` `/docs`; deploy verified
  live. **Final PR: #4 (merged). Site: https://sassnarep3-star.github.io/SAVINGS2/**
