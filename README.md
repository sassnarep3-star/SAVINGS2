# SAVINGS2 — savings account research

A verified, source-linked comparison of U.S. savings accounts at the largest national banks and the biggest national
digital banks, built to answer one question: **where does a large deposit earn the most while staying fully FDIC-insured?**

**Live site:** https://sassnarep3-star.github.io/SAVINGS2/

Account-opening date used for every projection: **2026-10-22**. All values retrieved **2026-10-22**.

## Headline result

| | |
| --- | --- |
| Highest fully verified savings APY | **3.75%** — CIT Bank Platinum Savings (balances ≥ $5,000, rate sheet dated 2026-07-01) |
| Best rate with no promotion and no gate | **3.50%** — Marcus Online Savings (as of 2026-10-21) |
| Highest APY on $250,000+ | **3.65%** — Barclays Tiered Savings (as of 2026-10-07) |
| Big-branch banks that publish a rate | **0.01%** — Truist (as of 2026-09-28) and Wells Fargo (no date published) |
| FDIC national average savings rate | **0.38%** (as of 2026-10-19) |
| 12-month Treasury | **4.54%** (as of 2026-10-19) |
| FDIC cover per bank | $250,000 single · $500,000 joint · $1,250,000 trust (5+ beneficiaries) |

On $250,000 for one year: **$9,375** at the best verified rate vs **$950** at the national average vs **$25** at 0.01%.

## What is in the repo

```
index.html               dashboard: headline answer, decision table, top-8 ranking, promotions
accounts.html            all 19 products: rates, minimums, fees, app, security, FDIC, opening rules
returns.html             return tables: $10k-$5M x 1/3/5 years, plus promotions converted to year-one dollars
fdic.html                coverage limits, how many banks a large deposit needs, traps that break coverage
competitiveness.html     rates vs FDIC national average and the Treasury curve
bonuses.html             every promotion with its exact conditions, plus opening rules
flagged.html             every unverified value and irregularity, with sources
methodology.html         how verification and arithmetic were done, and what the study cannot tell you

data/banks.json          the only place values are stored (each with source URLs, effective dates, flags)
data/analysis.json       computed output: every return figure, benchmark comparison and FDIC plan
analysis/summary.md      the analysis as plain markdown
research/verification-log.md   line-by-line audit trail: quoted evidence for every number
build.py                 regenerates every page from data/banks.json (includes a validation gate)
check_links.py           verifies local links; external source URLs are listed for manual review
COORDINATION.md          the shared task board for parallel sessions
```

## Rebuild

```bash
python3 build.py        # writes all HTML + data/analysis.json + analysis/summary.md
python3 check_links.py  # local links must resolve
```

`build.py` refuses to render a product marked as having a verified APY if it has no tier value or no source link, so the
site cannot silently drift from the dataset.

## Verification rules

1. A value comes from the bank's own domain, the FDIC, the CFPB or the U.S. Treasury — or it does not appear.
2. Aggregators, review sites and banks' own competitor comparison tables are never used as value sources.
3. If an official page will not disclose a value (ZIP gate, login wall, JavaScript-only table, 404), the field is left
   blank and the reason is published on the **Flagged for Review** page.
4. Every APY carries the bank's own effective date where one is published; where none is published, that is flagged.
5. FDIC charter status is confirmed per legal entity from `api.fdic.gov`.

## Known gaps (published, not hidden)

- 7 of the 18 active products have no APY a public official page will disclose: Chase, Bank of America, Citi, TD,
  Capital One, Citizens and Fifth Third. Discover is listed separately because its charter is now inactive.
- PNC's 3.15% exists only in the page title of a product that is geo-blocked from this location.
- CIT's rate sheet is dated 2026-07-01 — older than every other quote.
- CIT trust-account availability was **not** verified; the $1.25M single-bank trust structure is an FDIC rule, not a
  recommendation for CIT.

Full detail: [flagged.html](flagged.html) and [research/verification-log.md](research/verification-log.md).

## Disclaimer

Informational only, not financial, tax or legal advice. APYs are variable and can change at any time, including after an
account is opened. Confirm every rate and term with the bank before depositing.
