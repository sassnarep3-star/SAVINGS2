# SAVINGS2

Verified savings-account research for large U.S. national banks (October 2026), plus a
static dashboard site published on GitHub Pages.

## What's here

- **`docs/`** — the published site (GitHub Pages, served from `/docs` on `main`):
  - `index.html` — dashboard: headline comparison of every bank, key findings
  - `national-banks.html` — Chase, Bank of America, Wells Fargo, Citibank, U.S. Bank,
    PNC, Truist: rates, tiers, fees, notes
  - `online-banks.html` — Capital One, Marcus by Goldman Sachs, SoFi, American Express,
    Synchrony, Ally (and the Discover/Capital One merger status)
  - `returns.html` — interest earned at $10k / $50k / $100k / $250k deposits, 1-year
    and 5-year projections, fee drag, first-year value with bonuses
  - `bonuses.html` — new-account cash bonuses and promotional rates, with terms and
    deadlines
  - `requirements.html` — minimum deposits, monthly fees and waivers, withdrawal rules
  - `fdic-security.html` — FDIC rules and $250k-maximization strategies, per-bank FDIC
    certificate verification, security/app features
  - `analysis.html` — rate competitiveness over the deposit's life (Fed policy context,
    FDIC national averages) and recommendations by deposit size
  - `flagged.html` — every item that could not be fully verified from an official
    source, with review links
  - `sources.html` — the full register of official sources with check dates
  - `data/savings-data.json` — machine-readable snapshot of the verified data
- **`tools/returns_calc.py`** — reproducible script that computes every projection on
  the returns page
- **`COORDINATION.md`** — shared task board, verified-sources register, irregularities
  log, session protocol

## Verification policy

Every rate, fee, minimum and bonus published on the site was read from an official bank
page/PDF or a government source (fdic.gov, federalreserve.gov) on **October 21–22, 2026**.
Values that could not be confirmed from official sources are left blank or explicitly
flagged (never inferred), and each flagged item is documented on `docs/flagged.html`
with links for manual review. Savings APYs are variable; confirm current terms at the
linked official pages before acting. This project is research, not financial advice.
