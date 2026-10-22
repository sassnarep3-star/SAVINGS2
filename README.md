# SAVINGS2

Verified savings-account research for large U.S. national banks (October 2026), plus a
static dashboard site published on GitHub Pages.

This repository contains the work of **two parallel research sessions** that ran on
2026-10-22 and was integrated the same day:

- **Session A** (`arena/46ab1baa-savings2`, board ID `session-46ab1baa`) — bank roster
  (19 products incl. TD, Citizens, Fifth Third, HSBC, Barclays US, CIT), FDIC charter
  verification for all entities, security/app research, return analysis, and a static
  site generated at the repository root by `build.py` (PRs #1–#3, merged).
- **Session B** (`arena/24e1eb4e-savings2`) — official-source verification of
  Chase/Bank of America/Citibank/Capital One/Synchrony rates (via rate-sheet PDFs and
  product pages where session A hit JavaScript/ZIP gates), bonuses/promotions, FDIC
  rules + Fed context, returns-by-deposit-size calculations, and a hand-built static
  site in `docs/`.

The **integrated, canonical site served by GitHub Pages is `docs/`** (source:
`main` / `/docs`). Session A's generated site remains in the repository at the root
and its data/research under `data/` and `research/` — all of its verified values are
incorporated into the `docs/` site (bank-by-bank, with sources), and its unique banks
are published there on `docs/other-national-banks.html`.

## Layout

- **`docs/`** — canonical site (GitHub Pages):
  - `index.html` — dashboard: headline comparison, key findings
  - `national-banks.html` — Chase, Bank of America, Wells Fargo, Citibank, U.S. Bank, PNC, Truist
  - `online-banks.html` — Capital One, Marcus (Goldman Sachs), SoFi, American Express, Synchrony, Ally + Discover merger status
  - `other-national-banks.html` — TD, Citizens, Fifth Third, HSBC, Barclays US, CIT (session A data)
  - `returns.html` — interest at $10k/$50k/$100k/$250k, 1-yr & 5-yr projections, fee drag, first-year value with bonuses
  - `bonuses.html` — verified new-account bonuses and promo rates, with terms and deadlines
  - `requirements.html` — minimums, fees and waivers, withdrawal rules, eligibility
  - `fdic-security.html` — FDIC rules, $250k-maximization strategies, per-bank FDIC certificates (API-verified), security/app features
  - `analysis.html` — rate competitiveness over the deposit's life + recommendations by deposit size
  - `flagged.html` — every item that could not be fully verified from an official source, with review links
  - `sources.html` — annotated register of official sources with check dates
  - `data/savings-data.json` — machine-readable snapshot of session B's verified data
- **Root** — session A's generated site (`index.html`, `*.html`, `assets/`, generated
  by `build.py` from `data/banks.json`); kept intact as delivered
- **`data/banks.json`, `data/analysis.json`** — session A's verified dataset and analysis
- **`research/verification-log.md`** — session A's quoted-evidence verification log
- **`tools/returns_calc.py`** — session B's reproducible projection script
- **`tools/site_check.py`** — link/anchor/host checks for the `docs/` site
- **`build.py`, `check_links.py`** — session A's site generator and link checker
- **`COORDINATION.md`** — shared task board, both sessions' claims, merged sources register and irregularities, PR/deploy record

## Verification policy

Every rate, fee, minimum and bonus published on the site was read from an official bank
page/PDF or a government source (fdic.gov, federalreserve.gov) on **October 21–22, 2026**
by one of the two sessions, with quoted evidence. Values that could not be confirmed
from official sources are left blank or explicitly flagged (never inferred), and each
flagged item is documented on `docs/flagged.html` with links for manual review. Savings
APYs are variable; confirm current terms at the linked official pages before acting.
This project is research, not financial advice.
