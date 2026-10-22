# COORDINATION — Savings Account Research (SAVINGS2)

Shared task board. Read this before doing any work. Last updated: **2026-10-22 (integration complete)**.

## Session protocol

- Session IDs are prefixed `session-`. The active session for this repository is **`session-46ab1baa`**
  (Arena branch `arena/46ab1baa-savings2`, the branch this session is required to use; it therefore also serves as the
  integration branch — see "Branch naming").
- Claim a task by writing your session ID + file scope in the table, then commit and push the claim **before** starting work.
- Never start a task another session has claimed and is actively committing to.
- Keep scopes non-overlapping. If you need a file owned by another session, log a request in
  "Cross-session requests" instead of editing it.
- A claim older than 60 minutes with no commits may be taken over; note the handoff in the log.
- `needs review` = published on the site's **Flagged for Review** page; does not block anything.

### Branch naming

| Session | Branch | Note |
| --- | --- | --- |
| session-46ab1baa | `arena/46ab1baa-savings2` | Arena-tracked session branch; must not be renamed. Serves as this session's working **and** integration branch. |
| session-46ab1baa (integration) | `arena/46ab1baa-savings2` | Final integration, PR and Pages publish performed here, because it is the only branch this session may push to. |

## Task board

| ID | Task | Status | Owner | File scope | Updated |
| --- | --- | --- | --- | --- | --- |
| T1 | Bank roster + FDIC charter/insurance verification | **done** | session-46ab1baa | `data/banks.json`, `research/fdic.md` | 2026-10-22 |
| T2 | Official APY collection (dated, per bank) | **done** | session-46ab1baa | `data/banks.json`, `research/rates.md` | 2026-10-22 |
| T3 | Minimums, fees, opening rules, app, security | **done** | session-46ab1baa | `data/banks.json`, `research/accounts.md` | 2026-10-22 |
| T4 | Bonuses / promotional offers | **done** | session-46ab1baa | `data/banks.json`, `research/bonuses.md` | 2026-10-22 |
| T5 | Return-on-deposit analysis + FDIC coverage model | **done** | session-46ab1baa | `analysis/`, `data/analysis.json`, `build.py` | 2026-10-22 |
| T6 | Static site (landing + category subpages) | **done** | session-46ab1baa | `index.html`, `assets/**`, `*.html` | 2026-10-22 |
| T7 | Line-by-line verification pass + link check | **done** | session-46ab1baa | `research/verification-log.md`, `check_links.py` | 2026-10-22 |
| T8 | Integration, PR to `main`, Pages deploy | **done** | session-46ab1baa | `COORDINATION.md` | 2026-10-22 |

> Only `session-46ab1baa` has ever claimed work in this repository. No other session registered a claim between
> 2026-10-22 00:02 UTC and 2026-10-22 00:20 UTC, so there is no duplicate work and no overlap to resolve.
> Scopes T1–T4 were consolidated into one dataset file (`data/banks.json`) because they share a single schema;
> the research notes for each are sections of `research/verification-log.md`.

## Claim log

| When (UTC) | Session | Action |
| --- | --- | --- |
| 2026-10-22 00:03 | session-46ab1baa | Created board; claimed T1–T8. Repo was empty apart from the initial commit. |
| 2026-10-22 00:20 | session-46ab1baa | Marked T1–T7 done after the verification pass; kept T8 (integration) in progress. |
| 2026-10-22 00:12 | session-46ab1baa | Opened PR #1, merged it, confirmed the Pages build, fetched all 8 live pages. T8 done. |
| 2026-10-22 00:35 | session-46ab1baa | Post-merge corrections on the branch: per-size tier APYs on `returns.html` (Barclays was showing the $250k tier at $10k), removed a duplicated Marcus promotion row, "Big Four" wording corrected (Truist/Wells Fargo are not Big Four), footer counts split into verified / partial / no-usable-APY, `flagged.html` intro re-stated as 8 of 18 active. |

## Verification performed (T7)

- **19 products** in `data/banks.json`; **10** with a fully verified APY, **1** partial (PNC), **8** unverified.
- Every value checked against the bank's own page on 2026-10-22. Quoted evidence for each field is in
  `research/verification-log.md`.
- FDIC charter status and certificate number checked for all 19 entities via `api.fdic.gov` (data index 2026-10-16).
  Discover Bank (cert 5649) returns `ACTIVE: 0` and is recorded as inactive/merged.
- FDIC limits checked against three FDIC pages (Deposit Insurance; Understanding Deposit Insurance; Your Insured
  Deposits + the Trust Accounts section of the FDIC employee guide).
- Benchmarks checked against the FDIC National Rates and Rate Caps table (October 2026, revised 2026-10-19):
  savings 0.38%, Treasury 12m 4.54%, 24m 4.88%, 36m 5.00%, 60m 5.09%.
- `python3 build.py`: 8 pages generated, **0 validation errors**, 3 documented warnings.
- `python3 check_links.py`: all local links resolve. External URLs cannot be HTTP-checked from this sandbox's shell
  (no general egress); each source URL was instead opened and read individually during research, and the pages that
  failed are listed in section 5 of the verification log.

## Sources used (primary only)

| Domain | Used for |
| --- | --- |
| api.fdic.gov | institution/charter status, certificate numbers |
| fdic.gov | insurance limits, trust rules, national average rate, Treasury yields, BankFind, EDIE |
| chase.com, bankofamerica.com, web.bankofamerica.com, citi.com, wellsfargo.com | Big Four product/rate/security pages |
| usbank.com, pnc.com, truist.com, td.com, capitalone.com, citizensbank.com, 53.com, us.hsbc.com | national & regional bank pages |
| ally.com, americanexpress.com, marcus.com, sofi.com, banking.us.barclays, cit.com | national digital bank pages |
| home.treasury.gov | attempted for daily yields (HTTP 500); yields taken from the FDIC table instead |

Aggregators, review sites and the banks' own competitor comparison tables were not used as value sources.

## Irregularities found (also published on the site's Flagged for Review page)

| # | Item | Detail |
| --- | --- | --- |
| I1 | Chase & Bank of America APYs are ZIP-gated | No rate table is served without a ZIP; `?zipCode=10001` did not render one. Left blank. |
| I2 | Capital One renders `NaN APY` | Page says the APY is "effective 10/21/2026" then prints `NaN APY`. Left blank. |
| I3 | Bank of America `$XXXX` placeholders | Public page renders literal `$XXXX` for the monthly fee and fee-waiver balance. |
| I4 | Discover Bank is inactive (cert 5649) | Merged into Capital One; Capital One states accounts opened on/after 2025-05-18 are aggregated for FDIC coverage. Not a separate $250k capacity. |
| I5 | CIT Bank is a division of First Citizens Bank | CIT deposits combine with First Citizens for coverage; the 3.75% does not add FDIC capacity. |
| I6 | CIT rate sheet dated 2026-07-01 | Three to eleven weeks older than every other verified quote. |
| I7 | PNC 3.15% is title-only | Product page refuses to render outside its area; no effective date. Marked partial. |
| I8 | Wells Fargo and HSBC publish no rate effective date | Values recorded as shown, but not tied to a day. |
| I9 | SoFi's $3M FDIC claim | Bank marketing statement about a partner-bank network, not an FDIC rule. Flagged. |
| I10 | Synchrony and Schwab dropped | Official savings URLs 404'd; excluded rather than populated from a third party. |

## Cross-session requests

_None. No other session is active in this repository._

## PR and merge record (T8)

| Item | Value |
| --- | --- |
| PR | [#1](https://github.com/sassnarep3-star/SAVINGS2/pull/1) — "Verified savings-account research + GitHub Pages dashboard (19 products, sourced line by line)" · [#2](https://github.com/sassnarep3-star/SAVINGS2/pull/2) — post-merge corrections |
| Merge result | **PR 1 merged** 2026-10-22T00:12:46Z → `e474bfc`. **PR 2 merged** 2026-10-22T00:14:15Z → `6601f69`. Both via `gh pr merge <n> --merge`, no review requested (per instruction). |
| Pages build | `pages/builds` → status **built**, latest commit `6601f69`, no error. `pages` status `built`, source `main` / root, `build_type` legacy, `https_enforced` true. |
| Deploy verification | All 8 pages plus `assets/style.css` fetched live from the Pages host and read: correct `<title>` on each, headline figures render (3.75% / 0.38% / 9.9× / $9,375.00). Shell `curl` has no egress in this sandbox, so the check was done with the page-fetch tool rather than `curl` exit codes. |
| Live URL | https://sassnarep3-star.github.io/SAVINGS2/ |

## Notes for a future session

- Start from `data/banks.json`; do not edit the HTML by hand, it is generated by `build.py`.
- Re-verify ZIP-gated banks by opening their rate page in a browser with a ZIP entered; if the rate can then be read
  from an official page, add it with `apy_as_of` and delete the corresponding flag.
- The largest open questions are: Chase/BofA/Citi/TD APYs (all gate-able with a ZIP), CIT trust-account availability,
  and a public rate-history source for any bank (none found).
