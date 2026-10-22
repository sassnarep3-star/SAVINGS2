# COORDINATION.md — Shared Task Board

This is the shared task board for the SAVINGS2 repository (savings account research +
GitHub Pages site). Any agent session working in this repo must read this file before
starting, claim tasks here, and keep it current.

- **Repo:** https://github.com/sassnarep3-star/SAVINGS2
- **Session count so far:** 1 (single-session repo as of board creation)
- **Protocol:** claim a task by writing your session ID + file scope, commit and push the
  claim immediately, then work only inside your claimed scope. `git pull --rebase` before
  every push. Log handoffs, conflicts, and completion notes in the log at the bottom.

## Session registry

| Session ID | Branch | Notes |
|---|---|---|
| `arena/24e1eb4e-savings2` | `arena/24e1eb4e-savings2` | Only active session. Arena fixes this branch name for this session, so all work (including final integration) happens on this branch rather than per-task `session-<id>/<task>` branches. Recorded here deliberately so any future session knows this scope is owned. |

## Task board

Status legend: `unclaimed` · `in progress` · `done` · `needs review`

| # | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T1 | Repo review + create COORDINATION.md | in progress | `arena/24e1eb4e-savings2` | `COORDINATION.md`, `README.md` |
| T2 | Research: FDIC insurance rules + security features (official sources) | in progress | `arena/24e1eb4e-savings2` | `docs/fdic.html`, `docs/security.html` |
| T3 | Research: big national brick-and-mortar banks (Chase, Bank of America, Wells Fargo, Citibank, U.S. Bank, PNC, Truist, Capital One) — rates, tiers, fees, bonuses, rules, apps | in progress | `arena/24e1eb4e-savings2` | `docs/banks-brick.html`, `docs/data/banks-brick.json` |
| T4 | Research: national online-first banks (Marcus by Goldman Sachs, Ally, Discover, American Express, Synchrony, SoFi) — rates, fees, bonuses, rules, apps | in progress | `arena/24e1eb4e-savings2` | `docs/banks-online.html`, `docs/data/banks-online.json` |
| T5 | Analysis: returns-by-deposit-size tables (incl. $250k FDIC max), rate competitiveness, promotions comparison | in progress | `arena/24e1eb4e-savings2` | `docs/returns.html`, `docs/bonuses.html`, `docs/data/returns.json` |
| T6 | Site build: landing page + category subpages + Flagged for Review page, static GitHub Pages site | in progress | `arena/24e1eb4e-savings2` | `docs/` (all html/css/js) |
| T7 | Final integration: line-by-line re-verification, link check, PR to main, merge, Pages deploy verification | in progress | `arena/24e1eb4e-savings2` | whole repo |

No task is `unclaimed` because this is a single-session repo: the same session owns all
tasks and executes them sequentially (T1→T7) on its single fixed branch. Any other
session that appears should propose scope changes in the log below rather than editing
another session's files.

## Verified-sources register

(Filled in as tasks complete. Every table row on the site carries a per-row source link;
this register records the date each official source was checked.)

| Date checked (UTC) | Source (official) | What was verified | Task |
|---|---|---|---|

## Irregularities / flagged items

(Items that could not be fully confirmed from an official source are also published on
the site's "Flagged for Review" page, `docs/flagged.html` — being flagged does not block
anything.)

| Date | Item | Task | Resolution |
|---|---|---|---|
| 2026-10-22 | Repo contained only `README.md` ("# SAVINGS2") — nothing to review line by line; no prior data, no irregularities in existing content. Recorded as baseline. | T1 | Resolved: baseline documented. |

## Log

- **2026-10-22 (arena/24e1eb4e-savings2):** Board created. Repo reviewed: single initial
  commit `e5a82d8` containing only `README.md` ("# SAVINGS2"). No existing site, no
  existing data, no branches besides `main`. Claimed T1–T7 (single session). Research
  starting with FDIC rules and the big national banks.
