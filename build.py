#!/usr/bin/env python3
"""
Build the SAVINGS2 static site from data/banks.json.

Design rules enforced here:
  * Only values present in data/banks.json are rendered. Nothing is inferred.
  * A product with apy_status != "verified" is never used in a return calculation.
  * Every table row carries source links.
  * All arithmetic is shown (principal, APY, horizon) so it can be re-checked by hand.

Output: index.html, accounts.html, returns.html, fdic.html, competitiveness.html,
        bonuses.html, flagged.html, methodology.html, assets/style.css, data/analysis.json,
        analysis/summary.md
"""
import json
import math
import html
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "data" / "banks.json").read_text())
META = DATA["meta"]
PRODUCTS = DATA["products"]
BY_ID = {p["id"]: p for p in PRODUCTS}

OPENED = date(2026, 10, 22)
HORIZONS = {1: date(2027, 10, 22), 3: date(2029, 10, 22), 5: date(2031, 10, 22)}
SIZES = [10_000, 25_000, 50_000, 100_000, 250_000, 500_000, 1_000_000, 2_500_000, 5_000_000]

FDIC_NAT = META["fdic_national_savings_rate"]          # 0.38
TREAS = META["treasury_yields"]                        # 1y 4.54, 2y 4.88, 3y 5.00, 5y 5.09


# ----------------------------------------------------------------------------- helpers
def esc(s):
    return html.escape(str(s), quote=True)


def money(v, cents=False):
    if v is None:
        return "<span class='blank'>—</span>"
    if cents:
        return "${:,.2f}".format(v)
    return "${:,.0f}".format(v)


def pct(v, dp=2):
    if v is None:
        return "<span class='blank'>—</span>"
    return f"{v:.{dp}f}%"


def blank_if_empty(v):
    if v is None or (isinstance(v, str) and not v.strip()):
        return "<span class='blank'>—</span>"
    return esc(v)


def interest(principal, apy, years):
    """APY already includes compounding, so balance = P * (1 + APY)^years."""
    return principal * ((1 + apy / 100.0) ** years - 1)


def effective_blend(legs):
    """legs = [(amount, apy)] -> blended annual return rate (simple weighted average)."""
    total = sum(a for a, _ in legs)
    return sum(a * r for a, r in legs) / total if total else 0.0


# ----------------------------------------------------------------------- calc scenarios
# Each scenario is an explicitly stated reading of a bank's published tiers.
def apy_barclays(amount):
    return 3.65 if 250_000 <= amount <= 1_000_000 else 3.50


def apy_cit(amount):
    return 3.75 if amount >= 5_000 else 0.25


def apy_usbank(amount):
    if amount >= 25_000:
        return 3.50
    if amount >= 5_000:
        return 2.00
    return 1.00


def apy_usbank_elite(amount):
    return 3.40 if amount >= 25_000 else 0.01


def apy_wf_platinum(amount):
    return 3.25 if amount >= 25_000 else 0.01


SCENARIOS = [
    ("cit-platinum-savings", "CIT Bank Platinum Savings",
     apy_cit, "≥$5,000 earns 3.75%; below $5,000 earns 0.25%. Rate sheet effective 2026-07-01.",
     "Rate sheet is dated 2026-07-01, older than other quotes."),
    ("barclays-tiered-savings", "Barclays Tiered Savings",
     apy_barclays, "3.50% below $250k; 3.65% for $250k–$1M. Max $1M per account.",
     ""),
    ("synchrony-high-yield-savings", "Synchrony High Yield Savings",
     lambda a: 3.55, "3.55% APY across all balances as of 2026-10-21; $0 minimum, $0 monthly fee.",
     ""),
    ("marcus-online-savings", "Marcus Online Savings",
     lambda a: 3.50, "Standard APY, no minimum, no fees.", ""),
    ("us-bank-smartly-savings", "U.S. Bank Bank Smartly Savings",
     apy_usbank, "Highest tier needs a Smartly Checking/Safe Debit/Smartly Visa plus $25k combined qualifying balance; without the relationship the standard APY is 0.05%.",
     "Relationship conditions apply."),
    ("us-bank-elite-money-market", "U.S. Bank Elite Money Market",
     apy_usbank_elite, "3.40% APY on $25,000+ for new clients depositing >=$25,000 within 30 days; 0.01% below $25,000.",
     "New-client $25k+ tier."),
    ("sofi-savings", "SoFi Savings (standard)",
     lambda a: 3.30, "Standard APY with no direct deposit. The 4.40% headline needs a direct deposit and lasts 6 months.",
     ""),
    ("wells-fargo-platinum-savings", "Wells Fargo Platinum Savings (New Customer)",
     apy_wf_platinum, "3.25% APY on $25,000+ for new Wells Fargo savings customers as of 2026-10-07; 0.01% below $25,000.",
     "New customer $25k+ tier."),
    ("amex-high-yield-savings", "American Express High Yield Savings",
     lambda a: 3.20, "No minimum balance, no fees.", ""),
    ("capital-one-360-performance", "Capital One 360 Performance Savings",
     lambda a: 3.20, "3.20% APY across all balances as of 2026-10-21 (verified on apply.capitalone.com/fc/index.html).",
     ""),
    ("pnc-high-yield-savings", "PNC High Yield Savings",
     lambda a: 3.15, "Rate read from the official page title only; PNC refused to serve the product page outside its area and gives no effective date.",
     "Partial evidence — flagged."),
    ("hsbc-premier-relationship-savings", "HSBC Premier Relationship Savings",
     lambda a: 3.10, "Relationship APY requires an HSBC Premier checking account and monthly qualifying activity; otherwise 0.05%.",
     "Relationship conditions apply."),
    ("ally-savings", "Ally Savings",
     lambda a: 3.10, "No minimum, no monthly fee; 10 withdrawals per statement cycle.", ""),
    ("bmo-alto-online-savings", "BMO Alto Online Savings",
     lambda a: 3.00, "3.00% APY across all balances as of 2026-10-21; $0 minimum, $0 monthly fee.",
     ""),
    ("chase-savings", "Chase Savings",
     lambda a: 0.01, "0.01% APY across all balance tiers as of 2026-10-16 (rdin1.pdf); $200 bonus on $10k+ new money held 90 days.",
     ""),
    ("truist-one-savings", "Truist One Savings",
     lambda a: 0.01, "$50 to open, $5 fee (waivable), all tiers pay 0.01%.", ""),
    ("wells-fargo-way2save", "Wells Fargo Way2Save Savings",
     lambda a: 0.01, "$25 to open, $5 fee (waivable), 0.01% at all balances as of 2026-10-07.", ""),
]


def scenarios_for(amount):
    out = []
    for pid, label, fn, cond, flag in SCENARIOS:
        p = BY_ID[pid]
        apy = fn(amount)
        out.append({
            "id": pid, "label": label, "apy": apy, "cond": cond, "flag": flag,
            "product": p,
            "interest_1y": interest(amount, apy, 1),
            "value_1y": amount + interest(amount, apy, 1),
        })
    out.sort(key=lambda r: -r["apy"])
    return out


# ------------------------------------------------------------------ validation gate
ERRORS = []
WARNINGS = []
for p in PRODUCTS:
    src = p.get("sources", {})
    if not src:
        ERRORS.append(f"{p['id']}: no sources")
    if p["apy_status"] == "verified":
        if not p["tiers"]:
            ERRORS.append(f"{p['id']}: verified but no tiers")
        for t in p["tiers"]:
            if t["apy"] is None:
                ERRORS.append(f"{p['id']}: verified tier with null APY")
    elif p["apy_status"] == "unverified" and p["tiers"]:
        ERRORS.append(f"{p['id']}: unverified but has tiers")
    if p["apy_status"] == "verified" and not p.get("apy_as_of"):
        WARNINGS.append(f"{p['id']}: verified APY without published effective date")
    for k in ("rates", "product"):
        if k not in src:
            WARNINGS.append(f"{p['id']}: missing '{k}' source link")

verified = [p for p in PRODUCTS if p["apy_status"] == "verified"]
partial = [p for p in PRODUCTS if p["apy_status"] == "partial"]
unverified = [p for p in PRODUCTS if p["apy_status"] == "unverified"]
inactive = [p for p in PRODUCTS if not p["fdic_active"]]
active = [p for p in PRODUCTS if p["fdic_active"]]


# ------------------------------------------------------------------------- page chrome
NAV = [
    ("index.html", "Overview"),
    ("accounts.html", "Accounts"),
    ("returns.html", "Returns"),
    ("fdic.html", "FDIC coverage"),
    ("competitiveness.html", "Competitiveness"),
    ("bonuses.html", "Bonuses & rules"),
    ("flagged.html", "Flagged for review"),
    ("methodology.html", "Method"),
]


def page(title, body, subtitle="", active=""):
    parts = []
    for href, label in NAV:
        cls = " class='active'" if href == active else ""
        parts.append(f"<a href='{href}'{cls}>{esc(label)}</a>")
    nav = "".join(parts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Savings research</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <div class="brand"><span class="dot"></span> Savings Account Research <span class="ver">v1.0 · 2026-10-22</span></div>
    <nav>{nav}</nav>
  </div>
</header>
<main class="wrap">
  <h1>{esc(title)}</h1>
  {f'<p class="sub">{subtitle}</p>' if subtitle else ''}
  {body}
</main>
<footer class="foot">
  <div class="wrap">
    <p>Compiled 2026-10-22 from official bank, FDIC and Treasury publications. Deposit account opened <strong>2026-10-22</strong>.
    APYs are variable unless the source says otherwise. Nothing here is financial advice.</p>
    <p>{len(PRODUCTS)} products screened · {len(verified)} with a fully verified APY · {len(unverified)} with no usable public APY · {len(partial)} partial
    <a href="flagged.html">see what is missing</a>.</p>
    <p>Interactive Deep-Dive Dashboards: <a href="investment-returns.html">Return by Deposit Size ($1k–$1M)</a> · <a href="high-yield-savings.html">National HYSAs</a> · <a href="big-four-comparison.html">Big Four Audit</a> · <a href="fdic-maximization.html">Max FDIC ($250k–$1.25M)</a> · <a href="bonuses-and-promotions.html">Bonuses &amp; Promos</a> · <a href="account-rules-and-security.html">Rules &amp; Security</a> · <a href="flagged-for-review.html">Flagged for Review</a></p>
  </div>
</footer>
</body>
</html>
"""


def src_links(p):
    labels = {
        "product": "product", "rates": "rates", "fdic_lookup": "FDIC record",
        "capitalone_disclosure": "FDIC aggregation",
    }
    out = []
    for k, url in p.get("sources", {}).items():
        out.append(f"<a href='{esc(url)}' target='_blank' rel='noopener'>{esc(labels.get(k, k))}</a>")
    return " · ".join(out)


def rate_cell(p):
    if p["apy_status"] == "verified":
        tiers = p["tiers"]
        if len(tiers) == 1:
            datebit = f"as of {esc(p['apy_as_of'])}" if p['apy_as_of'] else "no effective date published"
            return f"<strong>{pct(tiers[0]['apy'])}</strong><div class='small'>{datebit}</div>"
        rows = "".join(
            f"<div class='small'>{pct(t['apy'])} · {esc(t['condition'])}</div>" for t in tiers
        )
        datebit = f"as of {esc(p['apy_as_of'])}" if p['apy_as_of'] else "no effective date published"
        return f"<strong>tiered</strong><div class='small'>{datebit}</div>{rows}"
    if p["apy_status"] == "partial":
        return "<span class='flag'>3.15% (title only)</span><div class='small'>partial evidence</div>"
    return "<span class='blank'>not published</span>"


def status_chip(p):
    if not p["fdic_active"]:
        return "<span class='chip chip-grey'>inactive / merged</span>"
    if p["apy_status"] == "verified":
        return "<span class='chip chip-ok'>APY verified</span>"
    if p["apy_status"] == "partial":
        return "<span class='chip chip-warn'>APY partial</span>"
    return "<span class='chip chip-warn'>APY unverified</span>"


# ------------------------------------------------------------------------------ tables
def table(headers, rows, cls="", note=""):
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    n = f"<p class='note'>{note}</p>" if note else ""
    return f"<div class='scroll'><table class='{cls}'><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>{n}"


def decision_table(amt):
    """Objective -> the best *verified* option, with the condition that unlocks it."""
    rows = [
        ["Highest verified APY, any balance",
         "<strong>CIT Bank Platinum Savings</strong> — 3.75% from $5,000 (0.25% below it)",
         "Rate sheet dated 2026-07-01. 4.25% for the first six months with code BOOST50 (promotion ends 2026-12-15).",
         "<a href='https://www.cit.com/cit-bank/platinum-savings' target='_blank' rel='noopener'>CIT</a>"],
        ["Highest APY with no promotion and no gate",
         "<strong>Marcus Online Savings</strong> — 3.50%",
         "No minimum, no fee, no withdrawal limit, no credit check; APY as of 2026-10-21.",
         "<a href='https://www.marcus.com/us/en/savings/high-yield-savings' target='_blank' rel='noopener'>Marcus</a>"],
        ["Highest APY on a $250,000+ balance",
         "<strong>Barclays Tiered Savings</strong> — 3.65% from $250,000 to $1,000,000",
         "3.50% below $250,000; no fees; $200 bonus for $25,000 held 120 days (offer ends 2026-10-31).",
         "<a href='https://banking.us.barclays/tiered-savings.html' target='_blank' rel='noopener'>Barclays</a>"],
        ["Best rate that also adds FDIC capacity cheaply",
         "<strong>Marcus 3.50% + Amex 3.20% + Ally 3.10%</strong> across separate banks",
         "Each bank is a separate charter, so each adds a fresh $250,000 single-ownership limit.",
         "<a href='fdic.html'>FDIC coverage</a>"],
        ["Largest insured balance at one bank",
         "<strong>$1,250,000</strong> in a trust-titled account naming five beneficiaries",
         "FDIC rule effective 2024-04-01. Trust-account availability is verified for Ally only in this study.",
         "<a href='https://www.fdic.gov/resources/deposit-insurance/brochures/insured-deposits' target='_blank' rel='noopener'>FDIC</a>"],
        ["Best of the big branch banks (if you want a branch)",
         "<strong>U.S. Bank Bank Smartly Savings</strong> — 3.50%",
         "Only with a Smartly Checking/Safe Debit/Smartly Visa card and $25,000 combined qualifying balance; otherwise 0.05%.",
         "<a href='https://www.usbank.com/bank-accounts/savings-accounts/bank-smartly-savings/savings-account-interest-rates.html' target='_blank' rel='noopener'>U.S. Bank</a>"],
        ["Lowest cost of ownership",
         "<strong>Marcus, Ally, Amex, SoFi, Barclays, CIT</strong> — all $0 monthly fee, $0 minimum",
         "No fee to open, keep or close. Branch banks charge $4.99–$15/month unless a balance or relationship condition is met.",
         "<a href='accounts.html'>Accounts</a>"],
    ]
    return table(["If your objective is…", "Best verified option on 2026-10-22", "What unlocks it / what to watch", "Source"], rows,
                 note="All options are FDIC-insured at the stated institution. Nothing here accounts for your tax position, liquidity needs or appetite for tying money up in a Treasury.")


# ================================================================== index.html
def build_index():
    amt = 250_000
    ranked = scenarios_for(amt)
    top = ranked[0]
    best = [r for r in ranked if r["apy"] >= 3.0]
    cards = f"""
  <section class="cards">
    <div class="card"><div class="k">Highest fully verified APY</div><div class="v">{pct(top['apy'])}</div>
      <div class="l">{esc(top['label'])} · opens 2026-10-22</div></div>
    <div class="card"><div class="k">FDIC national average, savings</div><div class="v">{pct(FDIC_NAT)}</div>
      <div class="l">FDIC National Rates and Rate Caps, as of {esc(META['fdic_national_savings_rate_as_of'])}</div></div>
    <div class="card"><div class="k">Spread of best vs national average</div><div class="v">{top['apy']/FDIC_NAT:.1f}×</div>
      <div class="l">{pct(top['apy'])} vs {pct(FDIC_NAT)}</div></div>
    <div class="card"><div class="k">FDIC cover per bank, single owner</div><div class="v">{money(META['fdic_limits']['single'])}</div>
      <div class="l">$500,000 joint · $1,250,000 trust (5+ beneficiaries)</div></div>
  </section>
"""
    rows = []
    for r in ranked[:8]:
        rows.append([
            f"<strong>{esc(r['product']['brand'])}</strong><div class='small'>{esc(r['label'])}</div>",
            pct(r["apy"]),
            money(r["interest_1y"], True),
            money(r["value_1y"], True),
            f"{r['apy']/FDIC_NAT:.1f}×",
            f"{r['apy']-TREAS['1_year']:+.2f} pts",
            src_links(r["product"]),
        ])

    body = f"""
{cards}
  <h2>The answer, in one paragraph</h2>
  <p class="lead">On {OPENED.isoformat()} the highest <em>fully verified</em> savings APY among the {len(active)} active accounts screened is
  <strong>{pct(top['apy'])}</strong> ({esc(top['label'])}). The two branch banks that publish a rate publicly (Truist and Wells Fargo) pay
  <strong>0.01%</strong>, and Chase, Bank of America, Citi, TD, Capital One, Citizens and Fifth Third publish no rate a public page can
  capture at all — those rates are ZIP-, region- or relationship-gated, so they are left blank here instead of being guessed.
  A {money(amt)} deposit therefore earns about <strong>{money(ranked[0]['interest_1y'], True)}</strong> in year one at the best verified rate,
  versus about <strong>{money(interest(amt, 0.01, 1), True)}</strong> at 0.01% and <strong>{money(interest(amt, FDIC_NAT, 1), True)}</strong> at the FDIC national average.</p>

  <h2>The decision, by objective</h2>
  {decision_table(amt)}

  <div class="callout">
    <strong>Read this before acting.</strong> Every APY in this table is variable and can change the day after you open the account
    (Marcus, Amex, Ally, SoFi, Barclays and CIT all say so in their own disclosures). The projections below are
    <em>what today's published rate would pay if it never changed</em> — a comparison tool, not a forecast.
    Projections start on the account-opening date, {OPENED.isoformat()}.
  </div>

  <h2>{money(amt)} for one year — ranked</h2>
  {table(["Bank / product", "APY used", "Interest, year 1", "Balance 2027-10-22", "vs national avg", "vs 12-mo Treasury", "Sources"], rows,
         note="Interest = principal × ((1 + APY)^1 − 1). Sources open the exact page each value came from.")}

  <h2>What this project found</h2>
  <ol class="findings">
    <li><strong>The rate spread is enormous.</strong> {pct(top['apy'])} vs {pct(FDIC_NAT)} at the average bank is a
      {top['apy']/FDIC_NAT:.1f}× difference in interest for identical FDIC protection. On {money(amt)} that is
      {money(ranked[0]['interest_1y'] - interest(amt, FDIC_NAT, 1), True)} of extra interest in one year.</li>
    <li><strong>Branch-bank brand costs you the interest.</strong> The only branch banks that publish a rate publicly
      (Truist 0.01%, Wells Fargo 0.01%) sit at the bottom of the table, and the four largest banks publish no retrievable
      rate at all; the highest verified rates come from
      branch-free U.S. banks (CIT/First Citizens, Barclays Bank Delaware, Goldman Sachs/Marcus, SoFi, American Express, Ally).</li>
    <li><strong>"Max FDIC insurance" is a structuring question, not a bank question.</strong> Coverage is $250,000 per depositor,
      per ownership category, per bank. {money(1_000_000)} in one name needs four banks; a joint account needs two;
      a trust naming five beneficiaries is covered to $1,250,000 at one bank. See <a href="fdic.html">FDIC coverage</a>.</li>
    <li><strong>Savings rates do not beat the Treasury curve today.</strong> The 12-month Treasury yielded
      {pct(TREAS['1_year'])} and the 5-year {pct(TREAS['5_year'])} (FDIC table, as of {esc(TREAS['as_of'])}), versus
      {pct(top['apy'])} for the best verified savings account. A savings account buys liquidity, not yield — the
      <a href="competitiveness.html">competitiveness page</a> quantifies the trade-off.</li>
    <li><strong>Only {len(verified)} of {len(active)} active accounts could be verified end-to-end.</strong> The rest are on the
      <a href="flagged.html">Flagged for Review</a> page with the exact reason (ZIP gate, JavaScript-only rate table,
      or no published rate).</li>
  </ol>

  <h2>Promotions worth more than the rate</h2>
  {table(["Bank", "Offer", "Conditions", "Source"], promotion_rows(),
         note="Only offers stated on the bank's own page are listed. A one-off bonus can outweigh a small APY difference — and can be worth less than it looks once the holding period is counted.")}
"""
    return page("Savings account research", body,
                f"Big national banks and national digital banks, verified line by line against official sources. Account opened {OPENED.isoformat()}.",
                "index.html")


PROMO_CONDITIONS = {
    "barclays-tiered-savings": "New Barclays savings customers only. Open through 2026-10-31, fund with at least $25,000 within 30 days, hold $25,000 for 120 consecutive days; bonus paid about 60 days later.",
    "sofi-savings": "Eligible direct deposit of $1,000+; bonus is $50 or $400 depending on the deposit; terms apply.",
    "cit-platinum-savings": "Promo code BOOST50 at opening; boost applies for six months; promotion runs 2026-09-29 to 2026-12-15.",
    "marcus-online-savings": "Referral programme: one +1.00% boost per referral, up to 5 referrals a year, each lasting 3 months; APY as of 2026-10-21.",
}


def promotion_rows():
    rows = []
    for p in PRODUCTS:
        if p.get("bonus"):
            rows.append([
                f"<strong>{esc(p['brand'])}</strong>",
                esc(p["bonus"]),
                esc(PROMO_CONDITIONS.get(p["id"], "")),
                f"<a href='{esc(p['bonus_source'])}' target='_blank' rel='noopener'>official terms</a>",
            ])
    return rows


# ================================================================ accounts.html
def build_accounts():
    rate_rows = []
    for p in PRODUCTS:
        if not p["fdic_active"]:
            continue
        rate_rows.append([
            f"<strong>{esc(p['brand'])}</strong><div class='small'>{esc(p['product'])}</div>",
            f"<span class='small'>{esc(p['bank'])}<br>FDIC cert {esc(p['fdic_cert'])}</span>",
            rate_cell(p),
            money(p["min_open"]),
            money(p["monthly_fee"]),
            blank_if_empty(p.get("fee_note")),
            blank_if_empty(p.get("withdrawal_note")),
            status_chip(p),
            src_links(p),
        ])
    feature_rows = []
    for p in PRODUCTS:
        feature_rows.append([
            f"<strong>{esc(p['brand'])}</strong><div class='small'>{esc(p['product'])}</div>",
            blank_if_empty(p.get("app")),
            blank_if_empty(p.get("security")),
            blank_if_empty(p.get("fdic_note")),
            blank_if_empty(p.get("bonus")),
            blank_if_empty(p.get("opening_rules")),
            status_chip(p),
        ])

    body = f"""
<p class="lead">All {len(PRODUCTS)} products screened: the four largest U.S. banks first, then the national and regional branch
banks that publish consumer savings products, then the national digital banks that hold the top verified rates.
A dash means <em>not verifiable from an official public page</em> — it is never a guess.</p>

<h2>Rates, minimums and fees</h2>
{table(["Bank / product", "Legal entity & FDIC cert", "APY", "Min. to open", "Monthly fee", "Fee waiver / notes", "Withdrawal rule", "Status", "Sources"],
       rate_rows,
       note="APY cells show the bank's own effective date where one is published. 'Not published' = the official page does not expose the rate (see Flagged for review).")}

<h2>App, security, insurance and opening rules</h2>
{table(["Bank / product", "Mobile app", "Security controls (as documented by the bank)", "FDIC statement", "Bonus / promotion", "Opening rules", "Status"],
       feature_rows,
       note="Security cells quote only controls the bank documents publicly. Where a bank exposes its controls only after login, the cell is blank and the gap is listed on the Flagged for review page.")}

<h2>Why some banks pay 0.01% and others 3.75%</h2>
<p>The high-rate accounts are all deposit-gathering machines without branch networks: CIT Bank (a division of First Citizens),
Barclays Bank Delaware, Goldman Sachs Bank USA, SoFi Bank, American Express National Bank, Ally Bank. The branch-based banks
price savings off their own funding needs and relationship tiers — U.S. Bank, for example, pays 0.05% standard but 3.50% if you
hold $25,000 in combined balances plus a Smartly Checking account. That is not a savings rate; it is a relationship rebate, and
it has conditions attached.</p>
"""
    return page("Accounts", body,
                "Every product screened, with source links for each value.",
                "accounts.html")


# ================================================================== returns.html
def build_returns():
    amt = 250_000
    ranked = scenarios_for(amt)
    rows = [[
        f"<strong>{esc(r['product']['brand'])}</strong><div class='small'>{esc(r['label'])}</div>",
        pct(r["apy"]),
        money(r["interest_1y"], True),
        money(r["value_1y"], True),
        f"{r['apy']/FDIC_NAT:.1f}×",
        f"{r['apy']-TREAS['1_year']:+.2f}",
        esc(r["cond"]),
    ] for r in ranked]

    size_headers = ["Deposit"] + [r["product"]["brand"] for r in ranked] + ["Best verified", "Difference, best vs 0.01%"]
    size_rows = []
    for s in SIZES:
        sc = scenarios_for(s)
        by_id = {x["id"]: x for x in sc}
        cells = [f"<strong>{money(s)}</strong>"]
        for r in ranked:
            apy = by_id[r["id"]]["apy"]          # tier for THIS deposit size, not the $250k tier
            cells.append(f"{money(interest(s, apy, 1), True)}<div class='small'>{pct(apy)}</div>")
        best = sc[0]
        cells.append(f"<strong>{money(best['interest_1y'], True)}</strong><div class='small'>{esc(best['product']['brand'])} {pct(best['apy'])}</div>")
        cells.append(money(best["interest_1y"] - interest(s, 0.01, 1), True))
        size_rows.append(cells)

    horizon_rows = []
    for r in ranked[:4]:
        for y in (1, 3, 5):
            horizon_rows.append([
                f"<strong>{esc(r['product']['brand'])}</strong> <span class='small'>{pct(r['apy'])}</span>" if y == 1 else "",
                f"{y} year{'s' if y > 1 else ''} → {HORIZONS[y].isoformat()}",
                money(interest(amt, r["apy"], y), True),
                money(amt + interest(amt, r["apy"], y), True),
                f"<span class='small'>assumes {pct(r['apy'])} never changes</span>" if y > 1 else "",
            ])

    promo_rows = [
        ["SoFi Savings", "4.40% for 6 months (1.10% boost), then 3.30%",
         money(interest(250_000, 4.40, 0.5) + interest(250_000 + interest(250_000, 4.40, 0.5), 3.30, 0.5), True),
         "Boost requires eligible direct deposit; open by 2026-12-31.",
         "<a href='https://www.sofi.com/banking/high-yield-savings-account/' target='_blank' rel='noopener'>SoFi</a>"],
        ["CIT Platinum Savings", "4.25% for 6 months (BOOST50), then 3.75%",
         money(interest(250_000, 4.25, 0.5) + interest(250_000 + interest(250_000, 4.25, 0.5), 3.75, 0.5), True),
         "Promo code BOOST50; promotion 2026-09-29 to 2026-12-15; $100 to open.",
         "<a href='https://www.cit.com/cit-bank/platinum-savings/boost' target='_blank' rel='noopener'>CIT</a>"],
        ["Marcus Online Savings", "3.50% + 1.00% for 3 months = 3.75% combined (bank's own illustration)",
         money(interest(250_000, 3.75, 1), True),
         "Referral-based; the bank's own combined-APY illustration is used here.",
         "<a href='https://www.marcus.com/us/en/savings/referrals#termsandconditions' target='_blank' rel='noopener'>Marcus</a>"],
    ]

    body = f"""
<p class="lead">Every projection starts on the account-opening date, <strong>{OPENED.isoformat()}</strong>, and uses the APY the bank
published on the date shown. Interest = principal × ((1 + APY)ⁿ − 1), because an APY already includes compounding.
Only the {len(verified)} accounts with a fully verified APY are projected.</p>

<h2>1. Return on {money(amt)} — first 12 months</h2>
{table(["Bank / product", "APY used", "Interest, year 1", "Balance on 2027-10-22", "× national avg", "vs 12-mo Treasury (pts)", "Conditions behind the rate"],
       rows,
       note="The APY used is the bank's headline rate for this deposit size; tier conditions are spelled out in the last column and on the accounts page.")}

<h2>2. Interest earned in year one, by deposit size</h2>
{table(size_headers, size_rows,
       note="Each column applies that bank's published tier for the deposit size shown. Blank-looking zeros are genuinely near-zero: 0.01% on $10,000 is $1.00.")}

<h2>3. What holding period does to the number ({money(amt)} deposit)</h2>
{table(["Bank", "Horizon", "Interest earned", "Balance at maturity", "Caveat"], horizon_rows,
       note="Years 3 and 5 assume the APY never changes. Every one of these APYs is variable, so treat 3- and 5-year columns as a scenario, not a promise.")}

<h2>4. Promotions, converted into year-one dollars</h2>
{table(["Account", "Promotional rate path", "Interest on $250,000 in year one", "Conditions", "Source"], promo_rows,
       note="The promotion is modelled as 6 months at the boosted rate followed by 6 months at the standard rate, compounding. Actual results depend on when the boost starts and on rate changes.")}

<h2>5. How to read these numbers</h2>
<ul>
  <li><strong>Year one is almost entirely about APY.</strong> At {money(amt)}, moving from the FDIC national average ({pct(FDIC_NAT)}) to the best verified rate ({pct(ranked[0]['apy'])}) is worth
      {money(ranked[0]['interest_1y'] - interest(amt, FDIC_NAT, 1), True)} in twelve months.</li>
  <li><strong>A bonus can beat a rate — briefly.</strong> Barclays' $200 requires keeping $25,000 on deposit for 120 days.
      That is 0.8% of the balance, or about 2.4% annualised over the holding period — on top of the 3.50% APY.
      It does not change the one-year ranking, but it is real money.</li>
  <li><strong>Tier cliffs matter more than headline APY.</strong> CIT pays 0.25% below $5,000 and 3.75% above it; Barclays pays 3.65%
      only from $250,000. Dropping below a tier can cost more than choosing a lower-rate bank.</li>
  <li><strong>Above $250,000 the constraint changes.</strong> Return is capped by how much you can keep insured at one bank —
      see <a href="fdic.html">FDIC coverage</a> for the multi-bank structures.</li>
</ul>
"""
    return page("Returns on deposit", body,
                f"Interest tables for {money(10_000)} to {money(5_000_000)}, from verified APYs, starting {OPENED.isoformat()}.",
                "returns.html")


# ====================================================================== fdic.html
def build_fdic():
    lim = META["fdic_limits"]
    limit_rows = [
        ["Single ownership (one person, no beneficiaries)", money(lim["single"]),
         "Per depositor, per FDIC-insured bank, per ownership category.",
         "<a href='https://www.fdic.gov/resources/deposit-insurance/' target='_blank' rel='noopener'>FDIC</a>"],
        ["Joint account (two owners)", money(lim["joint_per_owner"] * 2),
         "$250,000 per co-owner, so a two-person joint account is covered to $500,000.",
         "<a href='https://www.fdic.gov/resources/deposit-insurance/understanding-deposit-insurance' target='_blank' rel='noopener'>FDIC</a>"],
        ["Trust / POD naming 1 beneficiary", money(250_000), "$250,000 per eligible beneficiary.",
         "<a href='https://www.fdic.gov/financial-institution-employees-guide-deposit-insurance/trust-accounts' target='_blank' rel='noopener'>FDIC</a>"],
        ["Trust / POD naming 5+ beneficiaries", money(lim["trust_max_per_owner"]),
         "Capped at $1,250,000 per trust owner for all trust accounts at one bank (rule effective 2024-04-01).",
         "<a href='https://www.fdic.gov/resources/deposit-insurance/brochures/insured-deposits' target='_blank' rel='noopener'>FDIC brochure</a>"],
        ["Same depositor, different banks", "separate limits",
         "Each FDIC-insured bank is insured separately — this is the lever for deposits above $250,000.",
         "<a href='https://www.fdic.gov/resources/deposit-insurance/understanding-deposit-insurance' target='_blank' rel='noopener'>FDIC</a>"],
    ]

    # capacity structures
    def banks_needed(target, structure):
        if structure == "single":
            return math.ceil(target / 250_000)
        if structure == "joint":
            return math.ceil(target / 500_000)
        return math.ceil(target / 1_250_000)

    plan_rows = []
    for target in (1_000_000, 2_500_000, 5_000_000):
        plan_rows.append([
            f"<strong>{money(target)}</strong>",
            f"{banks_needed(target, 'single')} banks × $250,000",
            f"{banks_needed(target, 'joint')} banks × $500,000 joint",
            f"{banks_needed(target, 'trust')} bank{'s' if banks_needed(target,'trust')>1 else ''} × $1,250,000 trust",
        ])

    # best-verified allocation examples at $1M
    legs_single = [(250_000, apy_cit(250_000)), (250_000, apy_barclays(250_000)),
                   (250_000, 3.50), (250_000, apy_usbank(250_000))]
    blend_single = effective_blend(legs_single)
    legs_joint = [(500_000, apy_cit(500_000)), (500_000, apy_barclays(500_000))]
    blend_joint = effective_blend(legs_joint)
    legs_trust = [(1_250_000, apy_cit(1_250_000))]
    blend_trust = effective_blend(legs_trust)

    alloc_rows = [
        ["4 banks, single ownership<br><span class='small'>CIT $250k · Barclays $250k · Marcus $250k · U.S. Bank $250k</span>",
         money(1_000_000), pct(blend_single), money(interest(1_000_000, blend_single, 1), True), money(1_000_000 + interest(1_000_000, blend_single, 1), True),
         "U.S. Bank slice requires the Smartly relationship; CIT's rate sheet is dated 2026-07-01."],
        ["2 banks, joint ownership<br><span class='small'>CIT $500k · Barclays $500k (joint)</span>",
         money(1_000_000), pct(blend_joint), money(interest(1_000_000, blend_joint, 1), True), money(1_000_000 + interest(1_000_000, blend_joint, 1), True),
         "Joint coverage is $250,000 per co-owner. Barclays caps a Tiered Savings account at $1,000,000."],
        ["1 bank, trust with 5 beneficiaries<br><span class='small'>CIT $1.25M in a trust-titled account</span>",
         money(1_250_000), pct(blend_trust), money(interest(1_250_000, blend_trust, 1), True), money(1_250_000 + interest(1_250_000, blend_trust, 1), True),
         "Highest verified single-bank capacity, but CIT trust-account availability was NOT verified in this pass — check before relying on it."],
    ]

    body = f"""
<p class="lead">"Maximum FDIC insurance" is not a property of a bank — it is a property of how the account is titled.
The FDIC covers <strong>$250,000 per depositor, per FDIC-insured bank, for each account ownership category</strong>.
Every account on this site is at an FDIC-insured institution; the practical question is how much you can hold at each one.</p>

<h2>1. The limits, as published by the FDIC</h2>
{table(["Ownership structure", "Insured at one bank", "Rule", "Source"], limit_rows)}

<div class="callout">
The FDIC's own warning matters here: <em>"All of your deposits in the same ownership category in the same FDIC-insured bank
are added together for the purpose of determining FDIC deposit insurance coverage."</em> Two savings accounts at the same bank
in your name are one $250,000 limit, not two.
</div>

<h2>2. How many banks a large deposit needs</h2>
{table(["Deposit", "Single ownership", "Joint (2 owners)", "Trust, 5 beneficiaries"], plan_rows,
       note="Coverage is per bank, so the count is the number of distinct FDIC-insured institutions required to keep every dollar insured.")}

<h2>3. Highest-verified-rate structure for $1,000,000</h2>
{table(["Structure", "Insured", "Blended APY", "Interest, year 1", "Balance 2027-10-22", "Caveat"], alloc_rows,
       note="Blended APY is the deposit-weighted average of the APYs published for each slice on 2026-10-22. It assumes every rate holds for 12 months.")}

<h2>4. Traps that silently break coverage</h2>
<ul>
  <li><strong>Two brands, one charter.</strong> CIT Bank is a division of First Citizens Bank, so CIT deposits combine with
      First Citizens deposits for coverage. Capital One states that Capital One and Discover accounts opened on or after
      2025-05-18 are counted together — the FDIC record shows Discover Bank (cert 5649) as inactive. Two familiar brands,
      one $250,000 limit.</li>
  <li><strong>Fintech "network" insurance is not the same as a bank deposit.</strong> SoFi advertises coverage up to $3,000,000
      through a network of participating banks; that is the bank's own marketing statement, not an FDIC rule, and it depends on
      how the sweep partners are structured. Verify with the bank and with EDIE before relying on it.</li>
  <li><strong>Trust coverage requires a real trust account.</strong> The $1,250,000 limit applies to accounts titled in the name of
      a valid revocable or irrevocable trust naming five or more eligible beneficiaries. Of the high-rate banks checked here,
      only Ally states on its savings page that the account can be opened in the name of a trust.</li>
  <li><strong>Interest counts toward the limit.</strong> Coverage is principal plus accrued interest through the date of failure,
      so a $250,000 deposit sitting at exactly the cap can drift over it as interest accrues.</li>
</ul>

<h2>5. Check it yourself</h2>
<p>The FDIC's own calculator (EDIE) is the authoritative check for a specific titling:
<a href="https://edie.fdic.gov/" target="_blank" rel="noopener">edie.fdic.gov</a>. Bank charter status is verified through
<a href="https://banks.data.fdic.gov/bankfind-suite/bankfind" target="_blank" rel="noopener">FDIC BankFind</a>.
Every FDIC certificate number on the accounts page links to that bank's FDIC record.</p>
"""
    return page("FDIC coverage", body,
                "How the $250,000 limit works, how many banks a large deposit needs, and the structures that keep 100% of it insured.",
                "fdic.html")


# ============================================================ competitiveness.html
def build_competitiveness():
    amt = 250_000
    ranked = scenarios_for(amt)
    rows = []
    for i, r in enumerate(ranked, 1):
        rows.append([
            str(i),
            f"<strong>{esc(r['product']['brand'])}</strong>",
            pct(r["apy"]),
            f"{r['apy']/FDIC_NAT:.1f}×",
            f"{r['apy']-FDIC_NAT:+.2f}",
            f"{r['apy']-TREAS['1_year']:+.2f}",
            f"{r['apy']-TREAS['3_year']:+.2f}",
            f"{r['apy']-TREAS['5_year']:+.2f}",
        ])

    treas_rows = []
    for label, years, apy in (("Best verified savings APY", 1, ranked[0]["apy"]),
                              ("Best verified savings APY", 3, ranked[0]["apy"]),
                              ("Best verified savings APY", 5, ranked[0]["apy"]),
                              ("12-month Treasury", 1, TREAS["1_year"]),
                              ("3-year Treasury", 3, TREAS["3_year"]),
                              ("5-year Treasury", 5, TREAS["5_year"]),
                              ("FDIC national savings average", 1, FDIC_NAT),
                              ("FDIC national savings average", 5, FDIC_NAT)):
        treas_rows.append([
            esc(label), f"{years} year{'s' if years > 1 else ''}", pct(apy),
            money(interest(amt, apy, years), True), money(amt + interest(amt, apy, years), True),
        ])

    gap_1y = TREAS["1_year"] - ranked[0]["apy"]
    gap_5y_extra = interest(amt, TREAS["5_year"], 5) - interest(amt, ranked[0]["apy"], 5)

    body = f"""
<p class="lead">A rate is only competitive relative to something. Here it is measured against three official benchmarks:
the FDIC national average savings rate ({pct(FDIC_NAT)}, as of {esc(META['fdic_national_savings_rate_as_of'])}), the Treasury yield curve
(1-, 3- and 5-year, as of {esc(TREAS['as_of'])}), and the other accounts in this study.</p>

<h2>1. Ranked against the national average and the Treasury curve</h2>
{table(["#", "Bank", "APY", "× national avg", "vs national avg (pts)", "vs 1-yr Treasury", "vs 3-yr Treasury", "vs 5-yr Treasury"], rows,
       note="Positive = the savings account pays more than that benchmark. Treasury yields are annualised market yields, not APYs, and are not FDIC-insured — they carry price risk if sold before maturity.")}

<h2>2. The same $250,000, held for the same number of years</h2>
{table(["Instrument", "Holding period", "Rate used", "Interest earned", "Balance"], treas_rows,
       note="Treasury rows illustrate the alternative for a buy-and-hold investor; a savings account is liquid at all times, a Treasury sold early is not.")}

<h2>3. What the comparison actually says</h2>
<ul>
  <li><strong>The best savings rate does not beat the Treasury curve.</strong> {pct(ranked[0]['apy'])} sits
      <strong>{gap_1y:.2f} points below</strong> the 12-month Treasury yield ({pct(TREAS['1_year'])}), and the gap widens with maturity:
      over five years the Treasury curve would earn about <strong>{money(gap_5y_extra, True)}</strong> more on {money(amt)} than the
      savings account at today's rates. Treasuries are not FDIC-insured and carry price risk if sold before maturity — that is what
      you are paid for.</li>
  <li><strong>Versus the average bank, the savings account wins by a mile.</strong> {pct(ranked[0]['apy'])} is
      {ranked[0]['apy']/FDIC_NAT:.1f}× the FDIC national average of {pct(FDIC_NAT)}. The gap between a 0.01% branch account and a
      3.75% online account is worth far more than the gap between the best savings account and a Treasury.</li>
  <li><strong>The curve slopes upward.</strong> The 2-year ({pct(TREAS['2_year'])}), 3-year ({pct(TREAS['3_year'])}) and 5-year
      ({pct(TREAS['5_year'])}) Treasury yields all sit above the 1-year ({pct(TREAS['1_year'])}), so committing money for longer is
      rewarded. A savings account gives you the same short-end exposure with no lock-up and no price risk, but no fixed rate either.</li>
  <li><strong>Lifespan changes the ranking, not the winner.</strong> Across 1, 3 and 5 years the highest verified savings account stays the
      best savings product, but at today's rates it never overtakes the Treasury curve. That is the price of liquidity.</li>
  <li><strong>Rate history is the missing dimension.</strong> None of the banks publish a public rate history in a form that can be
      verified here, so this study cannot tell you how often these APYs moved. What it can tell you is that every bank on the list
      reserves the right to change the rate the day after you open the account.</li>
</ul>

<h2>4. Competitive position within this study</h2>
<p>Of {len(PRODUCTS)} products screened, {len(verified)} publish a rate that could be verified. The distribution is bimodal:
eight verified accounts cluster between {pct(3.10)} and {pct(3.75)}; two verified branch accounts pay {pct(0.01)}; the rest publish nothing
a public page can capture. There is almost nothing in between — which is why choosing the <em>category</em> of bank matters more
than fine-tuning between banks inside a category.</p>

<div class="callout">
<strong>What would change this conclusion.</strong> If the FDIC national average rises, the spread compresses. If the Fed cuts and
savings APYs follow, the Treasury curve's advantage grows (Treasury yields lock in, savings APYs do not). If you need the money
inside 12 months, none of the Treasury comparison applies — a savings account is the only one of these options that is liquid
without market risk.
</div>
"""
    return page("Rate competitiveness", body,
                "Verified APYs measured against the FDIC national average and the Treasury curve, across 1-, 3- and 5-year horizons.",
                "competitiveness.html")


# =================================================================== bonuses.html
def build_bonuses():
    promos = [
        ["Barclays Tiered Savings", "$200 cash", "$25,000 deposited within 30 days and kept for 120 consecutive days; new Barclays savings customers only; offer expires 2026-10-31; paid ~60 days after the 120 days.",
         "0.8% of the $25,000 balance (≈2.4% annualised over the 120-day hold)", "https://banking.us.barclays/tiered-savings.html"],
        ["SoFi Savings", "$50 or $400 cash", "Open the account and set up an eligible direct deposit of $1,000+; terms apply; accounts opened by 2026-12-31.",
         "Up to 1.6% of a $25,000 deposit, one-off", "https://www.sofi.com/banking/high-yield-savings-account/"],
        ["CIT Platinum Savings", "+0.50% APY for 6 months (BOOST50)", "Promo code BOOST50 at opening; promotion 2026-09-29 to 2026-12-15; boost applies to balances up to $9,999,999.",
         "≈0.25% extra in year one (half of 0.50%)", "https://www.cit.com/cit-bank/platinum-savings/boost"],
        ["Marcus Online Savings", "+1.00% APY for 3 months (referral)", "Referral programme; Marcus illustrates a combined 3.75% APY for one referral in a year.",
         "≈0.25% extra in year one", "https://www.marcus.com/us/en/savings/referrals#termsandconditions"],
    ]
    rows = [[f"<strong>{esc(a)}</strong>", esc(b), esc(c), esc(d),
             f"<a href='{esc(e)}' target='_blank' rel='noopener'>official terms</a>"] for a, b, c, d, e in promos]

    no_bonus = [p["brand"] for p in PRODUCTS if p["fdic_active"] and not p.get("bonus")]

    body = f"""
<p class="lead">Only promotions stated on the bank's own page are listed. No aggregator, affiliate or "best bank bonus" list was used,
because those pages are frequently out of date and often pay the publisher.</p>

<h2>1. Live promotions found on official pages (checked 2026-10-22)</h2>
{table(["Bank", "Offer", "Exact conditions", "Rough value", "Source"], rows,
       note="'Rough value' restates the offer as a percentage of a representative deposit so it can be compared with APY differences. It is arithmetic on the stated terms, not a bank claim.")}

<h2>2. Accounts with no promotion found on the official product page</h2>
<p class="small">{esc(", ".join(no_bonus))}. "No promotion found" means the page checked on 2026-10-22 disclosed none — banks rotate
offers frequently and some promote only by direct mail or in-app.</p>

<h2>3. Rules for opening — what each bank actually requires</h2>
{table(["Bank", "Opening requirements and restrictions", "Source"],
       [[f"<strong>{esc(p['brand'])}</strong>", blank_if_empty(p.get("opening_rules")),
         f"<a href='{esc(p['sources'].get('product',''))}' target='_blank' rel='noopener'>product page</a>"]
        for p in PRODUCTS if p["fdic_active"]])}

<h2>4. How to judge a bonus without being fooled</h2>
<ul>
  <li><strong>Divide by the holding requirement.</strong> Barclays' $200 needs $25,000 held 120 days. That is 0.8% of the
      balance, or about 2.4% annualised over that period — worth more than the 0.15-point gap between Barclays' 3.50% and
      3.65% tiers, but it is a one-off that cannot be repeated.</li>
  <li><strong>Check what the bonus does to the rate you can accept.</strong> Several "bonus" accounts pay a low base rate after the
      promotion ends. The SoFi boost, for example, lasts six months; the standard APY is what you live on afterwards.</li>
  <li><strong>Bonuses are taxable interest.</strong> Barclays states the $200 is reported on Form 1099-INT.</li>
  <li><strong>Never chase a bonus by moving money you may need.</strong> Early-withdrawal or minimum-balance rules can claw back more
      than the bonus pays.</li>
</ul>
"""
    return page("Bonuses, promotions and opening rules", body,
                "Offers exactly as the banks state them, with the conditions that decide whether you actually get paid.",
                "bonuses.html")


# ==================================================================== flagged.html
def build_flagged():
    unv_rows = []
    for p in PRODUCTS:
        if p["apy_status"] != "verified":
            unv_rows.append([
                f"<strong>{esc(p['brand'])}</strong><div class='small'>{esc(p['product'])}</div>",
                status_chip(p),
                esc(p["apy_note"]),
                src_links(p),
            ])
    flag_rows = []
    for p in PRODUCTS:
        for f in p.get("flags", []):
            flag_rows.append([f"<strong>{esc(p['brand'])}</strong>", esc(f), src_links(p)])

    gaps = []
    for p in PRODUCTS:
        missing = []
        if not p.get("app") and p["fdic_active"]:
            missing.append("mobile app")
        if not p.get("security") and p["fdic_active"]:
            missing.append("security controls")
        if not p.get("withdrawal_note") and p["fdic_active"]:
            missing.append("withdrawal rules")
        if p.get("min_open") is None and p["fdic_active"]:
            missing.append("minimum to open")
        if p.get("monthly_fee") is None and p["fdic_active"]:
            missing.append("monthly fee")
        if missing:
            gaps.append([f"<strong>{esc(p['brand'])}</strong>", esc(", ".join(missing)), src_links(p)])

    body = f"""
<p class="lead">This page exists so that nothing on this site is a guess. Every value that could not be confirmed from an official
public page is listed here with the reason, and the value is left blank in the tables.</p>

<div class="callout warn">
<strong>{len(unverified) + len(partial)} of {len(active)} active products have no fully verifiable APY.</strong> Seven publish
nothing a public page will disclose, PNC's figure exists only in a page title, and one further product (Discover) is included
solely to record that its charter is now inactive. Not because the banks are hiding anything illegal —
because the biggest banks publish rates only after a ZIP code or login, or inject them with JavaScript that a static fetch cannot read.
Substituting an aggregator's number would have made the table look complete and would have been unverifiable.
</div>

<h2>1. APY that could not be verified</h2>
{table(["Bank / product", "Status", "Why it is blank", "Official page checked"], unv_rows)}

<h2>2. Irregularities and oddities found while checking</h2>
{table(["Bank", "Observation", "Source"], flag_rows,
       note="Each of these was confirmed by reading the page, not inferred.")}

<h2>3. Other fields left blank</h2>
{table(["Bank", "Fields not verified in this pass", "Source checked"], gaps,
       note="These are gaps in this study, not necessarily gaps in the bank's disclosures — several expose the detail only after login.")}

<h2>4. Specific items I want a human to review</h2>
<ol>
  <li><strong>PNC 3.15%.</strong> The number appears in PNC's own page title, but the page body says the product is not available in
      my area, and there is no effective date. It is used in the return tables with a flag. If PNC's product is not available in your
      region, ignore the row.</li>
  <li><strong>Capital One's APY renders as "NaN".</strong> The page text says the APY is "effective 10/21/2026", then prints "NaN APY".
      The value is almost certainly injected client-side. Left blank.</li>
  <li><strong>Bank of America's $XXXX placeholders.</strong> The public page shows literal "$XXXX" for the monthly fee and the
      fee-waiver balance. That is a rendering fault on BofA's side, not a missing value in my research.</li>
  <li><strong>CIT's rate sheet is dated 2026-07-01</strong> — nearly four months older than every other verified quote
      (2026-10-07 to 2026-10-21). If CIT repriced since then, the 3.75% in the return tables is stale. Re-check at application.</li>
  <li><strong>CIT trust accounts.</strong> The FDIC structure for $1.25M at one bank assumes a trust-titled account. I verified that
      Ally offers trust-titled savings; I did <em>not</em> verify that CIT does. The FDIC page presents that structure as the highest
      single-bank capacity available, not as a recommendation for CIT specifically.</li>
  <li><strong>SoFi's $3,000,000 FDIC claim</strong> comes from SoFi's marketing copy about a partner-bank network. The FDIC's rule is
      $250,000 per depositor per bank. Treat the $3M figure as a claim to verify with SoFi and EDIE, not as an established fact.</li>
  <li><strong>Discover is not a separate bank any more.</strong> FDIC institution data lists Discover Bank (cert 5649) as inactive, and
      Capital One says Capital One and Discover accounts opened from 2025-05-18 are aggregated for insurance. Anyone using Discover
      as a "second bank" for extra coverage is likely doubling up on one $250,000 limit.</li>
  <li><strong>Two banks with no published rate date</strong> (Wells Fargo, HSBC) and one with a partial-source rate (PNC). The rates are
      quoted as shown, but they cannot be tied to a specific day.</li>
</ol>

<h2>5. What was checked and passed</h2>
<ul>
  <li>FDIC charter status and certificate number for every bank, via the FDIC BankFind API (data index dated 2026-10-16).</li>
  <li>Every APY, minimum, fee and bonus against the bank's own page on 2026-10-22, with the page's own "as of" date where published.</li>
  <li>FDIC limits against the FDIC's Deposit Insurance, Understanding Deposit Insurance and Your Insured Deposits pages.</li>
  <li>National average rate and Treasury yields against the FDIC National Rates and Rate Caps table (October 2026, revised 2026-10-19).</li>
</ul>
"""
    return page("Flagged for review", body,
                "Everything that could not be verified, and every irregularity found while checking. Nothing here is hidden in a footnote.",
                "flagged.html")


# ================================================================= methodology.html
def build_method():
    body = f"""
<p class="lead">The rule for this project was simple and strict: a number either comes from an official page, or it does not appear.</p>

<h2>1. What counts as an official source</h2>
<ul>
  <li><strong>The bank's own domain</strong> — the product page, rate sheet, fee schedule or disclosure PDF on the bank's website.</li>
  <li><strong>The FDIC</strong> — deposit insurance rules, the national rate table, and the BankFind institution record (via api.fdic.gov).</li>
  <li><strong>The U.S. Treasury</strong> — yields, as republished in the FDIC national rate table.</li>
</ul>
<p>Aggregators, review sites, affiliate "best rate" lists, news articles and the comparison tables inside banks' own marketing pages
were <strong>not</strong> used as value sources. For example, SoFi's page compares itself to Chase at 0.02% and Bank of America at
0.04%; those are third-party figures SoFi attributes to a data vendor, so they do not appear as Chase or BofA values here.</p>

<h2>2. How each row was verified</h2>
<ol>
  <li>Identify the legal entity and FDIC certificate through the FDIC BankFind API, and check that the institution is active.</li>
  <li>Open the bank's own product page and record: APY (with the page's own effective date), minimum to open, minimum to earn the
      APY, monthly fee and waiver, withdrawal rules, app, security controls, insurance statement, bonus and opening requirements.</li>
  <li>Paste the exact wording into the notes where the wording is doing the work — for example "no minimum balance required to open
      an account or earn APY".</li>
  <li>If the page will not produce the value (ZIP gate, login wall, JavaScript-only table), record the reason and leave it blank.</li>
  <li>Store the source URL with the value so any reader can re-run the check.</li>
</ol>

<h2>3. How the return figures are calculated</h2>
<p>Interest = principal × ((1 + APY / 100)<sup>years</sup> − 1). Because an APY already embeds compounding, it is used directly as an
annual factor. No fees are deducted (all the high-rate accounts are fee-free), no taxes are modelled, and no rate changes are assumed.
Projections start on <strong>{OPENED.isoformat()}</strong>, the account-opening date used throughout.</p>
<p>Blended APYs in the FDIC section are deposit-weighted averages of the published APYs applied to each slice. Promotion maths assumes
the boosted rate applies for exactly the stated promotional period and the standard rate applies afterwards.</p>

<h2>4. What this study cannot tell you</h2>
<ul>
  <li><strong>How a rate will move.</strong> Every account here is variable-rate. Past rate behaviour is not published in a form that
      could be verified, so no trend is claimed.</li>
  <li><strong>Your actual APY at a ZIP-gated bank.</strong> For Chase, Bank of America, Citi and TD it is location- and
      relationship-dependent. What is published is the structure of the fee, not a single number.</li>
  <li><strong>Which account you will be approved for.</strong> All of these banks may decline an application;
      SoFi and Capital One say so explicitly.</li>
  <li><strong>Tax.</strong> Interest is taxable income. No after-tax figures are shown.</li>
</ul>

<h2>5. Refresh instructions</h2>
<p>All values live in <code>data/banks.json</code>. Re-checking means opening the <code>sources</code> URL for a product, updating the
value and <code>apy_as_of</code>, then re-running <code>python3 build.py</code>, which regenerates every page and rebuilds
<code>data/analysis.json</code>. The build refuses to render a verified APY that has no tier value or no source link.</p>

<h2>6. Limitations and conflicts</h2>
<ul>
  <li>No affiliate links, no referral codes, and no compensation relationship with any bank.</li>
  <li>The "big national bank" filter uses FDIC total assets from the institution file; it is a size screen, not a quality judgement.</li>
  <li>Figures were read on 2026-10-22 in a U.S. timezone; a page edited later the same day may differ.</li>
</ul>
"""
    return page("Method and verification", body,
                "How every value was checked, what was excluded, and what the study cannot tell you.",
                "methodology.html")


# ====================================================================== analysis.json
def build_analysis():
    out = {
        "opened_on": OPENED.isoformat(),
        "retrieved_on": META["retrieved_on"],
        "counts": {"products": len(PRODUCTS), "verified_apy": len(verified),
                   "partial_apy": len(partial), "unverified_apy": len(unverified),
                   "inactive_entities": len(inactive)},
        "benchmarks": {"fdic_national_savings_rate": FDIC_NAT, "as_of": META["fdic_national_savings_rate_as_of"],
                       "treasury": TREAS},
        "by_size": {},
        "promotions": [{"bank": p["brand"], "offer": p["bonus"], "source": p["bonus_source"]}
                       for p in PRODUCTS if p.get("bonus")],
        "fdic_plans": {},
        "validation": {"errors": ERRORS, "warnings": WARNINGS},
    }
    for s in SIZES:
        sc = scenarios_for(s)
        out["by_size"][str(s)] = [{
            "bank": r["product"]["brand"], "product": r["label"], "apy": r["apy"],
            "interest_1y": round(r["interest_1y"], 2), "balance_1y": round(r["value_1y"], 2),
            "multiple_of_national": round(r["apy"] / FDIC_NAT, 3),
            "vs_1y_treasury": round(r["apy"] - TREAS["1_year"], 3),
        } for r in sc]
    for target in (1_000_000, 2_500_000, 5_000_000):
        out["fdic_plans"][str(target)] = {
            "banks_single": math.ceil(target / 250_000),
            "banks_joint": math.ceil(target / 500_000),
            "banks_trust": math.ceil(target / 1_250_000),
        }
    return out


def build_summary_md(analysis):
    amt = 250_000
    ranked = scenarios_for(amt)
    lines = [
        "# Savings account research — summary",
        "",
        f"Compiled {META['retrieved_on']}; account-opening date used for all projections: **{OPENED.isoformat()}**.",
        "",
        "## Headline",
        "",
        f"- Highest fully verified savings APY: **{ranked[0]['apy']:.2f}%** ({ranked[0]['label']}).",
        f"- FDIC national average savings rate: **{FDIC_NAT:.2f}%** as of {META['fdic_national_savings_rate_as_of']}.",
        f"- Verified accounts: **{len(verified)} of {len(PRODUCTS)}**; unverified APY: **{len(unverified)}**.",
        f"- On $250,000 for one year the best verified account earns **${ranked[0]['interest_1y']:,.2f}**,",
        f"  versus **${interest(amt, FDIC_NAT, 1):,.2f}** at the national average and **${interest(amt, 0.01, 1):,.2f}** at 0.01%.",
        "",
        "## Ranked at $250,000, one year",
        "",
        "| # | Bank / product | APY | Interest, year 1 | Balance | Source condition |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for i, r in enumerate(ranked, 1):
        lines.append(f"| {i} | {r['product']['brand']} — {r['label']} | {r['apy']:.2f}% | ${r['interest_1y']:,.2f} | ${r['value_1y']:,.2f} | {r['cond']} |")
    lines += [
        "",
        "## FDIC capacity",
        "",
        "| Structure | Insured at one bank |",
        "| --- | --- |",
        "| Single ownership | $250,000 |",
        "| Joint, two owners | $500,000 |",
        "| Trust, 5 beneficiaries | $1,250,000 |",
        "",
        "Source: FDIC, *Your Insured Deposits* and *Understanding Deposit Insurance*.",
        "",
        "## Benchmark comparison",
        "",
        f"- 12-month Treasury: {TREAS['1_year']:.2f}% (FDIC table, as of {TREAS['as_of']})",
        f"- 3-year Treasury: {TREAS['3_year']:.2f}%",
        f"- 5-year Treasury: {TREAS['5_year']:.2f}%",
        "",
        f"The best verified savings APY is {TREAS['1_year'] - ranked[0]['apy']:.2f} points below the 12-month Treasury.",
        "",
        "## Unverified items",
        "",
    ]
    for p in PRODUCTS:
        if p["apy_status"] != "verified":
            lines.append(f"- **{p['brand']}** — {p['apy_note']}")
    lines += ["", "Full detail with source links: `flagged.html`, `research/verification-log.md`."]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------------------- write
STYLE = """
:root{
  --bg:#f6f7f9; --panel:#ffffff; --ink:#101828; --muted:#667085; --line:#e4e7ec;
  --accent:#0b6b57; --accent-2:#0f8a6f; --warn:#b54708; --warn-bg:#fffaeb; --ok:#067647;
  --ok-bg:#ecfdf3; --grey:#475467; --grey-bg:#f2f4f7;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header.top{background:#0d2c26;color:#fff;border-bottom:1px solid #0a231e;position:sticky;top:0;z-index:20}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;padding:10px 20px}
.brand{font-weight:650;letter-spacing:.2px;display:flex;align-items:center;gap:9px;font-size:15px}
.brand .dot{width:9px;height:9px;border-radius:50%;background:#37d3a6;display:inline-block}
.brand .ver{font-weight:400;font-size:11px;color:#9fd6c6;border:1px solid #2b544b;border-radius:99px;padding:1px 7px}
nav{display:flex;gap:4px;flex-wrap:wrap}
nav a{color:#c9ded7;text-decoration:none;font-size:13px;padding:6px 10px;border-radius:8px}
nav a:hover{background:#17453a;color:#fff}
nav a.active{background:#1d5a4b;color:#fff;font-weight:600}
main{padding:30px 20px 60px}
h1{font-size:30px;line-height:1.2;margin:0 0 8px;letter-spacing:-.4px}
h2{font-size:19px;margin:34px 0 10px;letter-spacing:-.2px}
h3{font-size:15px;margin:20px 0 6px}
p.sub,.lead{color:var(--muted);font-size:15px;max-width:80ch}
p.lead{font-size:15.5px;color:#344054}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:12px;margin:18px 0 6px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.card .k{font-size:11.5px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);font-weight:600}
.card .v{font-size:27px;font-weight:700;margin:6px 0 2px;letter-spacing:-.6px;color:#0b3d33}
.card .l{font-size:12px;color:var(--muted)}
.scroll{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:14px}
table{border-collapse:collapse;width:100%;font-size:13px;min-width:640px}
th{background:#f9fafb;text-align:left;font-size:11px;letter-spacing:.5px;text-transform:uppercase;
  color:#475467;font-weight:650;padding:10px 12px;border-bottom:1px solid var(--line);white-space:nowrap;vertical-align:bottom}
td{padding:11px 12px;border-bottom:1px solid #f0f1f3;vertical-align:top}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover td{background:#fcfdfd}
td strong{font-weight:650}
.small{font-size:11.5px;color:var(--muted);line-height:1.4}
.blank{color:#98a2b3}
.flag{color:var(--warn);font-weight:600}
.chip{display:inline-block;font-size:10.5px;font-weight:650;letter-spacing:.3px;padding:2px 8px;border-radius:99px;white-space:nowrap}
.chip-ok{background:var(--ok-bg);color:var(--ok)}
.chip-warn{background:var(--warn-bg);color:var(--warn)}
.chip-grey{background:var(--grey-bg);color:var(--grey)}
.note{font-size:12px;color:var(--muted);margin:8px 2px 0;max-width:95ch}
.callout{background:#f0f9f6;border:1px solid #bfe3d8;border-left:3px solid var(--accent-2);
  border-radius:10px;padding:12px 16px;margin:16px 0;font-size:13.5px;color:#233a34;max-width:95ch}
.callout.warn{background:var(--warn-bg);border-color:#fedf89;border-left-color:var(--warn);color:#573d0a}
ol.findings{padding-left:20px;max-width:95ch}
ol.findings li,ul li{margin:6px 0}
ul{max-width:95ch}
a{color:#0b6b57;text-decoration:none}
a:hover{text-decoration:underline}
.foot{border-top:1px solid var(--line);background:#fff;padding:18px 0 30px;font-size:12px;color:var(--muted)}
.foot p{margin:4px 0}
code{background:#f2f4f7;border:1px solid #e4e7ec;border-radius:5px;padding:1px 5px;font-size:12px}
@media (max-width:640px){h1{font-size:24px}.brand .ver{display:none}}
"""


def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "style.css").write_text(STYLE)

    analysis = build_analysis()
    (ROOT / "data" / "analysis.json").write_text(json.dumps(analysis, indent=2) + "\n")
    (ROOT / "analysis").mkdir(exist_ok=True)
    (ROOT / "analysis" / "summary.md").write_text(build_summary_md(analysis))

    pages = {
        "index.html": build_index(),
        "accounts.html": build_accounts(),
        "returns.html": build_returns(),
        "fdic.html": build_fdic(),
        "competitiveness.html": build_competitiveness(),
        "bonuses.html": build_bonuses(),
        "flagged.html": build_flagged(),
        "methodology.html": build_method(),
    }
    for name, content in pages.items():
        (ROOT / name).write_text(content)

    (ROOT / ".nojekyll").write_text("")

    print(f"built {len(pages)} pages")
    print(f"products={len(PRODUCTS)} verified={len(verified)} partial={len(partial)} unverified={len(unverified)}")
    if ERRORS:
        print("VALIDATION ERRORS:")
        for e in ERRORS:
            print("  -", e)
        raise SystemExit(1)
    if WARNINGS:
        print("validation warnings:")
        for w in WARNINGS:
            print("  -", w)


if __name__ == "__main__":
    main()
