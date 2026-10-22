# Savings account research — summary

Compiled 2026-10-22; account-opening date used for all projections: **2026-10-22**.

## Headline

- Highest fully verified savings APY: **3.75%** (CIT Bank Platinum Savings).
- FDIC national average savings rate: **0.38%** as of 2026-10-19.
- Verified accounts: **10 of 19**; unverified APY: **8**.
- On $250,000 for one year the best verified account earns **$9,375.00**,
  versus **$950.00** at the national average and **$25.00** at 0.01%.

## Ranked at $250,000, one year

| # | Bank / product | APY | Interest, year 1 | Balance | Source condition |
| --- | --- | --- | --- | --- | --- |
| 1 | CIT Bank — CIT Bank Platinum Savings | 3.75% | $9,375.00 | $259,375.00 | ≥$5,000 earns 3.75%; below $5,000 earns 0.25%. Rate sheet effective 2026-07-01. |
| 2 | Barclays — Barclays Tiered Savings | 3.65% | $9,125.00 | $259,125.00 | 3.50% below $250k; 3.65% for $250k–$1M. Max $1M per account. |
| 3 | Marcus by Goldman Sachs — Marcus Online Savings | 3.50% | $8,750.00 | $258,750.00 | Standard APY, no minimum, no fees. |
| 4 | U.S. Bank — U.S. Bank Bank Smartly Savings | 3.50% | $8,750.00 | $258,750.00 | Highest tier needs a Smartly Checking/Safe Debit/Smartly Visa plus $25k combined qualifying balance; without the relationship the standard APY is 0.05%. |
| 5 | SoFi — SoFi Savings (standard) | 3.30% | $8,250.00 | $258,250.00 | Standard APY with no direct deposit. The 4.40% headline needs a direct deposit and lasts 6 months. |
| 6 | American Express — American Express High Yield Savings | 3.20% | $8,000.00 | $258,000.00 | No minimum balance, no fees. |
| 7 | PNC — PNC High Yield Savings | 3.15% | $7,875.00 | $257,875.00 | Rate read from the official page title only; PNCl refused to serve the product page outside its area and gives no effective date. |
| 8 | HSBC — HSBC Premier Relationship Savings | 3.10% | $7,750.00 | $257,750.00 | Relationship APY requires an HSBC Premier checking account and monthly qualifying activity; otherwise 0.05%. |
| 9 | Ally Bank — Ally Savings | 3.10% | $7,750.00 | $257,750.00 | No minimum, no monthly fee; 10 withdrawals per statement cycle. |
| 10 | Truist — Truist One Savings | 0.01% | $25.00 | $250,025.00 | $50 to open, $5 fee (waivable), all tiers pay 0.01%. |
| 11 | Wells Fargo — Wells Fargo Way2Save Savings | 0.01% | $25.00 | $250,025.00 | $25 to open, $5 fee (waivable), 0.01% at all balances. |

## FDIC capacity

| Structure | Insured at one bank |
| --- | --- |
| Single ownership | $250,000 |
| Joint, two owners | $500,000 |
| Trust, 5 beneficiaries | $1,250,000 |

Source: FDIC, *Your Insured Deposits* and *Understanding Deposit Insurance*.

## Benchmark comparison

- 12-month Treasury: 4.54% (FDIC table, as of 2026-10-19)
- 3-year Treasury: 5.00%
- 5-year Treasury: 5.09%

The best verified savings APY is 0.79 points below the 12-month Treasury.

## Unverified items

- **Chase** — APY is ZIP-code gated: Chase's public rate page renders no table until a 5-digit ZIP is submitted, and states rates 'may vary by market'. No APY is recorded rather than inferred.
- **Bank of America** — APY is ZIP/location gated and not present in the served HTML. Not recorded.
- **Citibank** — Citi's savings APY pages return an empty shell to a non-JavaScript fetch; Citi's own disclosure states APY is 'determined by Rate Region, Relationship Tier and applicable promotion'. No single public APY exists to record.
- **PNC** — 3.15% APY appears in the official PNC page title ('High Yield Savings Account | 3.15% Annual Percentage Yield APY'), but the page body returned 'This Product Isn't Available in Your Area' and no rate table or 'as of' date is served. Recorded as partial evidence only.
- **TD Bank** — TD publishes savings APYs only after a location is selected; the served tables are empty and the page shows 'You are viewing info for .' with no location. Not recorded.
- **Capital One** — The official page states 'APY (Annual Percentage Yield) is variable and effective 10/21/2026' but the value renders as 'NaN APY' in the served HTML (client-side injection). Not recorded.
- **Citizens** — No APY appears on the Citizens savings page (rates are disclosed in account documents / at application). Not recorded.
- **Fifth Third** — No APY on the Fifth Third savings page; the bank directs customers to a branch or banker for promotional rates. Not recorded.
- **Discover** — Discover Bank's FDIC record shows ACTIVE = 0 (inactive) in the FDIC institution data. Discover savings deposits sit with Capital One, N.A. for insurance purposes, so there is no separate Discover $250k capacity.

Full detail with source links: `flagged.html`, `research/verification-log.md`.
