# COORDINATION.md — Shared Task Board

This is the shared coordination board for all agent sessions working on this repo.
Read this before starting any work. Claim a task here (session ID + file scope),
commit and push the claim, and never start a task another session has claimed.

## Branch / session rules

- This session (`session-5cd0e98a`) works on branch **`arena/5cd0e98a-savings2`**.
  That branch name is fixed by the Arena platform and cannot be changed, so it
  serves as both the working branch and the final integration branch for this session.
- Other parallel sessions must work on their own branch, claim tasks here first,
  and keep file scopes non-overlapping. If you need a file owned by another
  session, log the request in the "Requests / handoffs" section instead of editing it.
- Run `git pull --rebase` before every push. Make small, frequent commits.
- If a session's claim is more than 60 minutes old with no commits, another
  session may take over and must note the handoff below.
- `needs review` = the item is published on the site's "Flagged for Review" page
  and does **not** block merge/deploy.

## Task board

| ID | Task | Status | Owner session | Files touched | Claimed (UTC) |
|----|------|--------|---------------|---------------|----------------|
| T1 | Repo review + create COORDINATION.md | done | session-5cd0e98a | COORDINATION.md | 2026-10-22 |
| T2 | Define scope of "big national banks" from an official ranking (FDIC/Federal Reserve) + methodology notes | in progress | session-5cd0e98a | research/scope-and-method.md | 2026-10-22 |
| T3 | FDIC insurance rules research from fdic.gov (standard limit, ownership categories, joint/POD coverage) | in progress | session-5cd0e98a | data/fdic.json, research/fdic-notes.md | 2026-10-22 |
| T4 | Bank-by-bank verified data collection from official bank sites (account, APY + as-of date, minimums, fees, bonuses, opening rules, app, security, FDIC membership) | in progress | session-5cd0e98a | data/accounts.json, research/bank-notes.md | 2026-10-22 |
| T5 | Returns modeling: deposits $1k/$10k/$50k/$100k/$250k (max standard FDIC) from account-open date 2026-10-22 for 1/3/5 years | unclaimed | session-5cd0e98a (reserved) | tools/build_site.py, data/accounts.json | 2026-10-22 |
| T6 | Build GitHub Pages site (landing + category subpages + Flagged for Review) | unclaimed | session-5cd0e98a (reserved) | docs/ | 2026-10-22 |
| T7 | Verification pass: re-check every table row vs official source; link-check site; confirm build | unclaimed | session-5cd0e98a (reserved) | docs/, data/ | 2026-10-22 |
| T8 | Open PR `arena/5cd0e98a-savings2` → `main`, merge, enable + verify GitHub Pages deploy | unclaimed | session-5cd0e98a (reserved) | COORDINATION.md (log PR) | 2026-10-22 |

## Verification rules (all sessions)

- Every value must come from an **official** source (the bank's own site,
  fdic.gov, federalreserve.gov, CFPB). Aggregators (NerdWallet, Bankrate, etc.)
  may be used only to *find* official URLs — never as a data source.
- Every table row must carry a source link to the official page where the value
  was seen, plus the date checked.
- If a value cannot be confirmed on an official page, leave it **blank** and add
  it to the Flagged for Review list. Never infer or fill in values.
- Computed values (returns) must come only from verified APYs and clearly state
  assumptions (variable rates, no fees/withdrawals, compound at stated APY).

## Requests / handoffs

_(none yet)_

## Log

- 2026-10-22 — session-5cd0e98a: Reviewed repo (initial commit only, README stub).
  Created COORDINATION.md, claimed T2–T4, reserved T5–T8. Branch
  `arena/5cd0e98a-savings2` is this session's fixed working/integration branch.

## Results (sources, verification, irregularities)

_(filled in as tasks complete)_

## Pull request & deploy

_(PR link and merge result recorded here by T8)_
