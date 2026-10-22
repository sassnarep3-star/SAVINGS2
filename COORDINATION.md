# COORDINATION — Savings Account Research (SAVINGS2)

Shared task board. Read this before doing any work. Last updated: **2026-10-22**.

## Session protocol

- Session IDs are prefixed `session-`. The active session for this repository is **`session-46ab1baa`**
  (Arena branch `arena/46ab1baa-savings2`, which is the branch this session is required to use;
  the generic `session-<id>/<task>` branch naming is therefore satisfied by this branch — see
  "Branch naming" below).
- Claim a task by writing your session ID + file scope in the table, then commit and push the claim
  **before** starting work.
- Never start a task another session has claimed and is actively committing to.
- Keep scopes non-overlapping. If you need a file owned by another session, log a request in
  "Cross-session requests" instead of editing it.
- A claim older than 60 minutes with no commits may be taken over; note the handoff in the log.
- `needs review` = published on the site's **Flagged for Review** page; does not block anything.

### Branch naming

| Session | Branch | Note |
| --- | --- | --- |
| session-46ab1baa | `arena/46ab1baa-savings2` | Arena-tracked session branch; must not be renamed. Serves as this session's working + integration branch. |
| session-46ab1baa (integration) | `arena/46ab1baa-savings2` | Final integration + Pages publish performed here, since it is the only branch this session may push to. |

## Task board

| ID | Task | Status | Owner | File scope | Updated |
| --- | --- | --- | --- | --- | --- |
| T1 | Bank roster + FDIC charter/insurance verification | in progress | session-46ab1baa | `data/banks.json`, `research/fdic.md` | 2026-10-22 |
| T2 | Official APY collection (dated, per bank) | in progress | session-46ab1baa | `data/rates.json`, `research/rates.md` | 2026-10-22 |
| T3 | Minimums, fees, opening rules, app, security | in progress | session-46ab1baa | `data/accounts.json`, `research/accounts.md` | 2026-10-22 |
| T4 | Bonuses / promotional offers | in progress | session-46ab1baa | `data/bonuses.json`, `research/bonuses.md` | 2026-10-22 |
| T5 | Return-on-deposit analysis + FDIC coverage model | in progress | session-46ab1baa | `analysis/*.md`, `data/analysis.json` | 2026-10-22 |
| T6 | Static site (landing + category subpages) | in progress | session-46ab1baa | `index.html`, `assets/**`, `*.html` | 2026-10-22 |
| T7 | Line-by-line verification pass + link check | in progress | session-46ab1baa | `research/verification-log.md` | 2026-10-22 |
| T8 | Integration, PR to `main`, Pages deploy | in progress | session-46ab1baa | `COORDINATION.md` | 2026-10-22 |

> Note: no other session has registered a claim in this repository as of 2026-10-22.
> `session-46ab1baa` is therefore the sole research session **and** the integration session.
> Shared outputs (the combined dataset, `index.html`, navigation) are edited only here.

## Claim log

| When (UTC) | Session | Action |
| --- | --- | --- |
| 2026-10-22 | session-46ab1baa | Created board; claimed T1–T8 with non-overlapping scopes. Repo was empty (initial commit only). |

## Verification rules used by this session

1. Every value in every table must trace to an **official** source: the bank's own domain, the FDIC,
   the CFPB, or a U.S. Treasury/Federal Reserve page. Aggregators are never used as a value source.
2. Each row records `source_url`, `source_quote` (or the page's own "as of" date), and `verified_at`
   (UTC timestamp of retrieval).
3. If a value cannot be confirmed from an official source it is left **blank** and listed on the
   **Flagged for Review** page. Values are never inferred, estimated, or copied from a third party.
4. APY is quoted exactly as the bank states it, together with the bank's own effective date when the
   page states one. Rates that are ZIP-gated or market-dependent are recorded as such.
5. FDIC insurance status is confirmed per legal entity via the FDIC BankFind API (api.fdic.gov).

## Cross-session requests

_(none)_

## Irregularities found (also published on the Flagged for Review page)

| # | Item | Detail | Source |
| --- | --- | --- | --- |
| I1 | Chase & Bank of America savings APYs are ZIP-gated | Public product pages refuse to render an APY without a ZIP code; the rate is market-dependent. Left blank in the APY column, flagged unverified. | chase.com, bankofamerica.com |
| I2 | Capital One 360 Performance Savings APY renders as `NaN` in the public HTML | The APY is injected client-side; the served HTML shows `NaN APY`. Cross-checked on Capital One's own rates endpoint where available, otherwise flagged. | capitalone.com |
| I3 | Bank of America Advantage Savings fee/minimum placeholders | The public page renders `$XXXX` placeholders for the monthly fee and fee-waiver balance (client-side injection). Not recorded; flagged. | bankofamerica.com |
| I4 | Discover Bank is now part of Capital One for FDIC purposes | Capital One's own disclosure: accounts opened on/after 2025-05-18 are aggregated with Capital One deposit accounts for FDIC coverage. Discover's savings product is therefore not a separate $250k capacity anymore. | capitalone.com |

_This table is mirrored to `flagged.html` on the site._
