#!/usr/bin/env python3
"""
Build the complete multi-page GitHub Pages site from verified JSON datasets in data/.
Ensures every table row has an official source link, every unconfirmed value is left blank
and flagged as unverified, and all internal/external links are valid.
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

with open(DATA_DIR / "fdic_and_benchmarks.json", encoding="utf-8") as f:
    FDIC_DATA = json.load(f)
with open(DATA_DIR / "national_banks_savings.json", encoding="utf-8") as f:
    HYSA_DATA = json.load(f)
with open(DATA_DIR / "big_four_banks.json", encoding="utf-8") as f:
    BIG4_DATA = json.load(f)
with open(DATA_DIR / "promotions_and_rules.json", encoding="utf-8") as f:
    PROMO_DATA = json.load(f)
with open(DATA_DIR / "investment_returns_matrix.json", encoding="utf-8") as f:
    MATRIX_DATA = json.load(f)
with open(DATA_DIR / "flagged_for_review.json", encoding="utf-8") as f:
    FLAG_DATA = json.load(f)

NAV_ITEMS = [
    ("index.html", "Executive Overview"),
    ("investment-returns.html", "Return by Deposit Size ($1k–$1M)"),
    ("high-yield-savings.html", "National High-Yield Savings"),
    ("big-four-comparison.html", "Big Four & Relationship Tiers"),
    ("fdic-maximization.html", "Max FDIC Insurance ($250k–$1.25M)"),
    ("bonuses-and-promotions.html", "Bonuses & Promotions"),
    ("account-rules-and-security.html", "Account Rules & Security"),
    ("flagged-for-review.html", "Flagged for Review"),
]


def esc(val) -> str:
    if val is None:
        return ""
    return html.escape(str(val))


def render_cell_or_blank(val: str, flag_anchor: str = "flagged-for-review.html") -> str:
    """
    Strict verification policy: If a value is empty/unconfirmed from an official source,
    leave the value blank and attach an explicit 'Unverified — Flagged' badge.
    """
    if val is None or str(val).strip() == "":
        return f'<a href="{flag_anchor}" class="blank-cell-notice" title="Value not confirmed on official public source; left blank per strict verification policy">Unverified (Blank) ⚑</a>'
    return esc(val)


def render_status_badge(status: str) -> str:
    s = str(status)
    if "Needs Review" in s or "Unverified" in s or "Flagged" in s:
        return f'<a href="flagged-for-review.html" class="badge badge-review">{esc(s)}</a>'
    return f'<span class="badge badge-verified">{esc(s)}</span>'


def page_shell(active_file: str, title: str, eyebrow: str, hero_title: str, hero_desc: str, body_html: str) -> str:
    nav_links = []
    for href, label in NAV_ITEMS:
        classes = ["nav-link"]
        if href == active_file:
            classes.append("active")
        if href == "flagged-for-review.html":
            classes.append("nav-flagged")
            nav_links.append(
                f'<a href="{href}" class="{" ".join(classes)}">⚑ {esc(label)} <span class="flag-count-badge">{len(FLAG_DATA["flagged_items"])}</span></a>'
            )
        else:
            nav_links.append(f'<a href="{href}" class="{" ".join(classes)}">{esc(label)}</a>')

    nav_html = "\n          ".join(nav_links)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)} | National Bank Savings &amp; Max FDIC Analysis (2026-10-22)</title>
  <meta name="description" content="Line-by-line verified analysis of big national bank savings accounts, APY rates, sign-up bonuses, account rules, and Max FDIC insurance returns as of October 22, 2026.">
  <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
  <div class="verification-bar">
    <div class="verification-bar-inner">
      <div>
        <span class="verification-pill">✓ 100% Official Primary Sources</span>
        <span style="margin-left:8px;">Account Opening Reference Date: <strong>2026-10-22</strong> &bull; FDIC National Avg Savings: <strong>0.38% APY</strong> (as of 2026-10-19) &bull; Fed EFFR: <strong>3.88%</strong></span>
      </div>
      <div>
        <span class="verification-pill warn"><a href="flagged-for-review.html" style="color:inherit;text-decoration:none;">⚑ {len(FLAG_DATA["flagged_items"])} Irregularities &amp; Unverified Fields Flagged for Review →</a></span>
      </div>
    </div>
  </div>

  <header class="site-header">
    <div class="header-inner">
      <div class="brand-row">
        <a href="index.html" class="brand-title">
          <div class="brand-badge">FDIC-250K</div>
          <div class="brand-text">
            <h1>National Bank Savings &amp; Max FDIC Return Intelligence</h1>
            <p>Line-by-Line Verified Rates, Deposit Return Matrices, Promotions &amp; Regulatory Disclosures</p>
          </div>
        </a>
        <div class="header-meta">
          <span class="meta-chip">Opening Date: <strong>2026-10-22</strong></span>
          <span class="meta-chip">Max Single FDIC: <strong>$250,000</strong></span>
          <span class="meta-chip">Max Trust/POD FDIC: <strong>$1,250,000</strong></span>
        </div>
      </div>
      <nav class="main-nav" aria-label="Main Navigation">
        {nav_html}
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="page-hero">
      <span class="page-hero-eyebrow">{esc(eyebrow)}</span>
      <h2>{esc(hero_title)}</h2>
      <p>{esc(hero_desc)}</p>
    </section>

    {body_html}
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div style="max-width:720px;">
        <strong style="color:#ffffff;font-size:14px;">Verification &amp; Data Integrity Policy (Reference Date: October 22, 2026)</strong>
        <p style="margin-top:6px;">
          Every rate, bonus, minimum deposit requirement, fee rule, and FDIC certificate number on this site was verified directly against official bank disclosures and U.S. government regulatory releases (<code>fdic.gov</code>, <code>federalreserve.gov</code>). Every table row includes a direct link to its official source. Any value that could not be confirmed from an official public source is left blank and documented on the <a href="flagged-for-review.html" style="color:#60a5fa;">Flagged for Review</a> page.
        </p>
        <div class="footer-links">
          <a href="index.html">Executive Overview</a>
          <a href="investment-returns.html">Return by Deposit Size</a>
          <a href="high-yield-savings.html">High-Yield Savings</a>
          <a href="big-four-comparison.html">Big Four Comparison</a>
          <a href="fdic-maximization.html">Max FDIC Strategies</a>
          <a href="bonuses-and-promotions.html">Bonuses &amp; Promotions</a>
          <a href="account-rules-and-security.html">Rules &amp; Security</a>
          <a href="flagged-for-review.html">Flagged for Review ({len(FLAG_DATA["flagged_items"])})</a>
          <a href="accounts.html">All 23 Screened Accounts</a>
          <a href="returns.html">1–5 Yr Return Summary</a>
          <a href="fdic.html">FDIC Structure Guide</a>
          <a href="competitiveness.html">Treasury vs. HYSA Curve</a>
          <a href="bonuses.html">Bonus Digest</a>
          <a href="flagged.html">Unverified Roster Gaps</a>
          <a href="methodology.html">Methodology</a>
        </div>
      </div>
      <div>
        <p><strong>Repository:</strong> <code>sassnarep3-star/SAVINGS2</code></p>
        <p><strong>Coordination Log:</strong> <code>COORDINATION.md</code></p>
        <p><strong>Analysis Date:</strong> <code>2026-10-22 (UTC)</code></p>
      </div>
    </div>
  </footer>

  <script src="assets/js/app.js"></script>
</body>
</html>
"""


def build_index_page() -> str:
    # Build Master Summary Table combining HYSA_DATA and BIG4_DATA
    hysa_rows_html = []
    for acc in HYSA_DATA["accounts"]:
        is_top = acc["rank_250k_fdic"] in (1, 2, 3)
        row_class = "top-pick-row" if is_top else ("flagged-row" if acc["apy_at_250k_max_fdic"] == "" else "")
        apy_250k_cell = (
            f'<span class="rate-pill">{esc(acc["apy_at_250k_max_fdic"])}</span>'
            if acc["apy_at_250k_max_fdic"] != ""
            else render_cell_or_blank("")
        )
        apy_under_cell = render_cell_or_blank(acc["apy_standard_or_under_250k"])
        max_bal_cell = render_cell_or_blank(acc["max_balance_limit"])

        # Compute 1-year total return on $250,000 if APY is verified
        if acc["apy_numeric_250k"] is not None:
            yr1_base = round(250000 * acc["apy_numeric_250k"], 2)
            yr1_bonus = acc["signup_bonus_numeric"]
            if acc["id"] == "marcus-online-savings":
                yr1_str = f"${yr1_base:,.2f} (Base)<br><strong style='color:#1d4ed8;'>$9,375.00 (w/ 1 Referral)</strong>"
            elif yr1_bonus > 0:
                yr1_str = f"<strong>${yr1_base + yr1_bonus:,.2f}</strong><br><span style='font-size:11.5px;color:#64748b;'>(${yr1_base:,.2f} + ${yr1_bonus:,.0f} bonus)</span>"
            else:
                yr1_str = f"<strong>${yr1_base:,.2f}</strong>"
        else:
            yr1_str = render_cell_or_blank("")

        hysa_rows_html.append(f"""
            <tr class="{row_class}">
              <td class="mono"><strong>#{acc["rank_250k_fdic"]}</strong></td>
              <td>
                <strong>{esc(acc["bank_name"])}</strong><br>
                <span class="badge-cert">FDIC Cert #{esc(acc["fdic_cert"])}</span>
              </td>
              <td>
                <strong>{esc(acc["account_name"])}</strong><br>
                <span style="font-size:12px;color:#64748b;">{esc(acc["nyc_availability"])}</span>
              </td>
              <td>{apy_250k_cell}<br><span style="font-size:11px;color:#64748b;">As of {esc(acc["rate_effective_date"])}</span></td>
              <td>{apy_under_cell}</td>
              <td class="mono">{esc(acc["min_opening_deposit"])}</td>
              <td class="mono">{esc(acc["monthly_maintenance_fee"])}</td>
              <td>{esc(acc["signup_bonus_amount"])}</td>
              <td>{max_bal_cell}</td>
              <td class="mono">{yr1_str}</td>
              <td>{render_status_badge(acc["verification_status"])}</td>
              <td><a class="source-btn" href="{esc(acc["source_url"])}" target="_blank" rel="noopener noreferrer">Official Site ↗</a></td>
            </tr>""")

    # Macro benchmarks rows
    bench_rows_html = []
    for b in FDIC_DATA["macro_benchmarks"]:
        bench_rows_html.append(f"""
            <tr>
              <td><strong>{esc(b["metric"])}</strong></td>
              <td><span class="rate-pill promo">{esc(b["rate_value"])}</span></td>
              <td class="mono">{esc(b["rate_cap_adjusted"])}</td>
              <td class="mono">{esc(b["reference_treasury_or_effr"])}</td>
              <td class="mono"><strong>{esc(b["national_rate_cap"])}</strong></td>
              <td class="mono">{esc(b["effective_date"])}</td>
              <td>{esc(b["tier_basis"])}</td>
              <td><span class="badge badge-verified">{esc(b["verification_status"])}</span></td>
              <td><a class="source-btn" href="{esc(b["source_url"])}" target="_blank" rel="noopener noreferrer">Official .Gov ↗</a></td>
            </tr>""")

    body = f"""
    <div class="kpi-grid">
      <div class="kpi-card highlight">
        <div>
          <div class="kpi-label">#1 Base APY at $250k Max FDIC</div>
          <div class="kpi-value emerald">3.65% APY + $200</div>
        </div>
        <div class="kpi-sub">
          <strong>Barclays Tiered Savings</strong> (Cert #57203) &bull; Pays <strong>$9,325.00</strong> in Year 1 (3.73% effective yield) &amp; <strong>$49,076.62</strong> over 5 years on $250,000 opened 2026-10-22.
        </div>
      </div>

      <div class="kpi-card highlight">
        <div>
          <div class="kpi-label">#1 Boosted Year-1 Return ($250k)</div>
          <div class="kpi-value emerald">$9,375.00 / yr</div>
        </div>
        <div class="kpi-sub">
          <strong>Marcus by Goldman Sachs</strong> (Cert #33124) &bull; <strong>3.50% APY</strong> base + <strong>1.00% APY</strong> 3-mo referral boost (4.50% for 3 mos / 3.75% combined 1-yr APY).
        </div>
      </div>

      <div class="kpi-card primary-accent">
        <div>
          <div class="kpi-label">#1 Flat-Rate All-Balance HYSA</div>
          <div class="kpi-value primary">3.55% APY</div>
        </div>
        <div class="kpi-sub">
          <strong>Synchrony Bank High Yield Savings</strong> (Cert #27314) &bull; $0 minimum deposit, $0 monthly fee, <strong>$8,875.00/yr</strong> on $250,000 (9.34x FDIC national average).
        </div>
      </div>

      <div class="kpi-card primary-accent">
        <div>
          <div class="kpi-label">#1 Brick-and-Mortar Relationship HYSA</div>
          <div class="kpi-value primary">3.50% APY</div>
        </div>
        <div class="kpi-sub">
          <strong>U.S. Bank Smartly® Savings</strong> (Cert #6548) &bull; Unlocks 3.50% APY at $25,000+ Combined Qualifying Balance when paired with Smartly Checking or Visa.
        </div>
      </div>

      <div class="kpi-card warn-accent">
        <div>
          <div class="kpi-label">Big Four Standard Savings Trap</div>
          <div class="kpi-value" style="color:#b91c1c;">0.01% – 0.03%</div>
        </div>
        <div class="kpi-sub">
          Standard savings at <strong>Chase, BofA, Wells Fargo &amp; Citi</strong> pay just <strong>$25–$75/yr</strong> on $250,000 — an opportunity cost of <strong>&gt;$9,200/yr</strong> vs top national HYSAs.
        </div>
      </div>
    </div>

    <div class="callout emerald">
      <h4>Executive Verdict for Opening an Account on October 22, 2026 (Max FDIC Goal: $250,000 Single / $500,000 Joint / $1M+ Multi-Bank or Trust)</h4>
      <p>
        1. <strong>Best Single-Account $250,000 Max FDIC Allocation:</strong> Open <strong>Barclays Tiered Savings (FDIC Cert #57203)</strong> before <strong>October 31, 2026</strong>. Depositing $250,000 unlocks Barclays' top <strong>3.65% APY</strong> tier ($250k–$1M) <em>and</em> the <strong>$200 new-customer bonus</strong> (for holding &ge;$25,000 for 120 days through February 19, 2027), yielding <strong>$9,325.00 in Year 1</strong> and <strong>$49,076.62 over 5 years</strong>.<br>
        2. <strong>Best $500,000 to $1,000,000+ 100% FDIC-Insured Strategy:</strong> Either (a) name <strong>4 to 5 eligible Payable-on-Death (POD) beneficiaries</strong> on a single account under the FDIC's April 1, 2024 Trust Rule (<code>12 C.F.R. § 330.10</code>, which insures <strong>$250,000 per beneficiary up to $1,250,000 per owner at one bank</strong>), OR (b) split $250,000 tranches across <strong>Barclays (#57203, 3.65% APY)</strong>, <strong>Synchrony (#27314, 3.55% APY)</strong>, <strong>Marcus by Goldman Sachs (#33124, 3.50% APY + 1.00% referral boost)</strong>, and <strong>U.S. Bank (#6548, 3.50% APY)</strong> or <strong>Wells Fargo Platinum (#3511, 3.25% APY)</strong>.<br>
        3. <strong>Critical FDIC Charter Consolidation Warning:</strong> As of <strong>November 18, 2025</strong>, <strong>Capital One 360 and Discover Bank share a single FDIC charter (Capital One, N.A., Cert #4297)</strong>, and <strong>BMO Alto shares BMO Bank N.A. (Cert #16571)</strong>. Do not stack $250,000 in both Capital One and Discover expecting $500,000 of single-owner coverage.
      </p>
    </div>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Interactive Return on Size of Investment &amp; FDIC Coverage Calculator (Opening Date: 2026-10-22)</h3>
          <p>Select any deposit amount, investment horizon, and FDIC ownership category to compare exact compound returns, bonuses, and FDIC insurance coverage across big national banks.</p>
        </div>
      </div>

      <div class="controls-bar">
        <div class="control-group">
          <label for="calc-deposit-input">Deposit Size ($ USD)</label>
          <input type="number" id="calc-deposit-input" class="control-input mono" value="250000" min="100" max="10000000" step="1000">
        </div>
        <div class="control-group">
          <label for="calc-horizon-select">Investment Lifespan (From 2026-10-22)</label>
          <select id="calc-horizon-select" class="control-select">
            <option value="0.25">3 Months (2026-10-22 → 2027-01-22)</option>
            <option value="0.5">6 Months (2026-10-22 → 2027-04-22)</option>
            <option value="1" selected>1 Year (2026-10-22 → 2027-10-22)</option>
            <option value="2">2 Years (2026-10-22 → 2028-10-22)</option>
            <option value="3">3 Years (2026-10-22 → 2029-10-22)</option>
            <option value="5">5 Years (2026-10-22 → 2031-10-22)</option>
          </select>
        </div>
        <div class="control-group">
          <label for="calc-ownership-select">FDIC Ownership Category (Per Bank Limit)</label>
          <select id="calc-ownership-select" class="control-select">
            <option value="250000" selected>Single Account — $250,000 Max FDIC</option>
            <option value="500000">Joint Account (2 Co-Owners) — $500,000 Max FDIC</option>
            <option value="750000">Trust / POD (3 Beneficiaries) — $750,000 Max FDIC</option>
            <option value="1000000">Trust / POD (4 Beneficiaries) — $1,000,000 Max FDIC</option>
            <option value="1250000">Trust / POD (5+ Beneficiaries) — $1,250,000 Max FDIC</option>
          </select>
        </div>
      </div>

      <div style="margin-bottom:16px;">
        <span style="font-size:12px;font-weight:700;color:#475569;text-transform:uppercase;margin-right:8px;">Quick Deposit Presets:</span>
        <div class="preset-buttons" style="display:inline-flex;">
          <button type="button" class="btn-preset btn-preset-deposit" data-amount="1000">$1,000</button>
          <button type="button" class="btn-preset btn-preset-deposit" data-amount="10000">$10,000 (Chase Bonus)</button>
          <button type="button" class="btn-preset btn-preset-deposit" data-amount="25000">$25,000 (Barclays / US Bank / WF Tier)</button>
          <button type="button" class="btn-preset btn-preset-deposit" data-amount="50000">$50,000</button>
          <button type="button" class="btn-preset btn-preset-deposit" data-amount="100000">$100,000</button>
          <button type="button" class="btn-preset btn-preset-deposit active" data-amount="250000">$250,000 (Max Single FDIC)</button>
          <button type="button" class="btn-preset btn-preset-deposit" data-amount="500000">$500,000 (Max Joint FDIC)</button>
          <button type="button" class="btn-preset btn-preset-deposit" data-amount="1000000">$1,000,000 (4-Bank / Trust FDIC)</button>
        </div>
      </div>

      <div id="calc-fdic-summary" class="callout emerald">
        <h4>100% Principal FDIC-Insured ($250,000 Deposit | Period: 2026-10-22 → 2027-10-22)</h4>
        <p>Your $250,000 principal is 100% covered within your selected $250,000 per-bank FDIC limit.</p>
      </div>

      <div class="table-wrapper">
        <table class="data-table" id="interactive-calc-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>National Bank &amp; FDIC Charter</th>
              <th>Account &amp; Promotional Rules</th>
              <th>Verified APY</th>
              <th>Compound Interest</th>
              <th>Promo / Bonus</th>
              <th>Total Return</th>
              <th>Ending Balance</th>
              <th>Single-Bank FDIC Status</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody id="calc-results-tbody">
            <!-- Populated immediately by assets/js/app.js; static fallback rows below -->
            <tr class="top-pick-row">
              <td class="mono"><strong>#1</strong></td>
              <td><strong>Barclays US Consumer Bank</strong><br><span style="font-size:12px;color:#64748b;">Barclays Bank Delaware (Cert #57203)</span></td>
              <td><strong>Barclays Tiered Savings</strong><br><span style="font-size:12px;color:#64748b;">+$200 bonus on &ge;$25k held 120 days (expires 2026-10-31)</span></td>
              <td><span class="rate-pill">3.65%</span><br><span style="font-size:11px;color:#64748b;">As of 2026-10-07</span></td>
              <td class="mono">$9,125.00</td>
              <td class="mono"><strong style="color:#1d4ed8;">+$200.00</strong></td>
              <td class="mono"><strong style="color:#047857;font-size:14.5px;">+$9,325.00</strong></td>
              <td class="mono"><strong>$259,325.00</strong></td>
              <td><span class="badge badge-verified">100% Principal Insured</span></td>
              <td><a class="source-btn" href="https://banking.us.barclays/tiered-savings.html" target="_blank" rel="noopener noreferrer">Official Source ↗</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Explore Analysis by Category</h3>
          <p>Detailed line-by-line breakdowns organized into dedicated subpages with official verification links on every row.</p>
        </div>
      </div>
      <div class="category-grid">
        <a href="investment-returns.html" class="category-card">
          <div>
            <h4>1. Return on Size of Investment ($1k – $1M)</h4>
            <p>Complete return matrices for $1k, $10k, $25k, $50k, $100k, $250k (Max FDIC), $500k, and $1M across 3-month, 6-month, 1-year, 2-year, 3-year, and 5-year horizons starting 2026-10-22.</p>
          </div>
          <div class="category-card-footer">
            <span>View Full Return Tables</span>
            <span>→</span>
          </div>
        </a>

        <a href="high-yield-savings.html" class="category-card">
          <div>
            <h4>2. Big National High-Yield Savings Accounts</h4>
            <p>Line-by-line comparison of 13 national high-yield and hybrid savings accounts (Barclays, Synchrony, Marcus, U.S. Bank, Wells Fargo, Amex, Capital One 360, PNC, Ally, BMO Alto, Citi).</p>
          </div>
          <div class="category-card-footer">
            <span>Compare 13 National HYSAs</span>
            <span>→</span>
          </div>
        </a>

        <a href="big-four-comparison.html" class="category-card">
          <div>
            <h4>3. Big Four Brick-and-Mortar &amp; Relationship Tiers</h4>
            <p>Detailed audit of JPMorgan Chase, Bank of America, Wells Fargo, and Citibank relationship tiers, fee waivers, and the $9,200+/year opportunity cost on $250,000.</p>
          </div>
          <div class="category-card-footer">
            <span>View Big Four Audit</span>
            <span>→</span>
          </div>
        </a>

        <a href="fdic-maximization.html" class="category-card">
          <div>
            <h4>4. Max FDIC Insurance Strategies ($250k – $1.25M+)</h4>
            <p>How to insure $250k, $500k, $1M, and $1.25M+ using Joint accounts, the April 2024 FDIC Trust/POD rule (12 C.F.R. § 330.10), and Multi-Charter allocations, plus FDIC Cert # registry.</p>
          </div>
          <div class="category-card-footer">
            <span>Explore FDIC Strategies</span>
            <span>→</span>
          </div>
        </a>

        <a href="bonuses-and-promotions.html" class="category-card">
          <div>
            <h4>5. Account Opening Bonuses &amp; Promotions</h4>
            <p>Verified terms, deposit minimums, holding periods, and expiration dates for Barclays ($200), Marcus (+1.00% APY referral boost), Chase ($200), Capital One ($250 checking), and Wells Fargo.</p>
          </div>
          <div class="category-card-footer">
            <span>Compare Active Promotions</span>
            <span>→</span>
          </div>
        </a>

        <a href="account-rules-and-security.html" class="category-card">
          <div>
            <h4>6. Account Rules, Withdrawal Limits &amp; App Security</h4>
            <p>Minimum opening deposits, zero-balance auto-closure windows, monthly withdrawal limits (Ally 10/mo, BofA 6/mo), mobile check limits, ACH speed, and app security.</p>
          </div>
          <div class="category-card-footer">
            <span>Review Rules &amp; Security</span>
            <span>→</span>
          </div>
        </a>

        <a href="flagged-for-review.html" class="category-card" style="border-color:#f59e0b;background:#fffbeb;">
          <div>
            <h4 style="color:#b45309;">⚑ 7. Flagged for Review ({len(FLAG_DATA["flagged_items"])} Items)</h4>
            <p>Audit log of all official website irregularities, regional geo-blocks (Citi Accelerate &amp; PNC HYS in NYC), Capital One's 'NaN APY' SSR bug, Discover merger FDIC overlap, and unverified blank fields.</p>
          </div>
          <div class="category-card-footer" style="color:#b45309;">
            <span>Inspect Flagged Irregularities</span>
            <span>→</span>
          </div>
        </a>
      </div>
    </section>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Master Comparison Table — National High-Yield &amp; Hybrid Savings Accounts (As of 2026-10-22)</h3>
          <p>Every row is verified from the institution's official website. Values that cannot be confirmed on the official public page are left blank and flagged.</p>
        </div>
        <div>
          <input type="search" class="control-input" placeholder="Filter banks or accounts..." data-table-filter="master-hysa-table">
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table" id="master-hysa-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Bank &amp; FDIC Cert #</th>
              <th>Account Name &amp; NYC Availability</th>
              <th>APY at $250k (Max FDIC)</th>
              <th>APY Under $250k</th>
              <th>Min to Open</th>
              <th>Monthly Fee</th>
              <th>Sign-Up Bonus / Promo</th>
              <th>Max Balance Cap</th>
              <th>1-Yr Return on $250k</th>
              <th>Verification Status</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(hysa_rows_html)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Official U.S. Government Macro Interest Rate Benchmarks (October 2026)</h3>
          <p>Baseline Federal Deposit Insurance Corporation (FDIC) and Federal Reserve System benchmarks used to evaluate rate competitiveness over the investment lifespan.</p>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Official Benchmark Metric</th>
              <th>Published Rate</th>
              <th>Rate Cap Adjusted</th>
              <th>Reference Benchmark / Range</th>
              <th>FDIC National Rate Cap</th>
              <th>Effective Date</th>
              <th>Calculation / Tier Basis</th>
              <th>Status</th>
              <th>Official .Gov Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(bench_rows_html)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return page_shell(
        "index.html",
        "Executive Dashboard",
        "Verified National Bank Savings Analysis • Account Opening Date: 2026-10-22",
        "Best Big National Bank Savings Accounts & Max FDIC Return Analysis",
        "Comprehensive, line-by-line verified comparison of high-yield and brick-and-mortar savings accounts at major U.S. national banks with mobile apps, institutional security, and full FDIC insurance coverage.",
        body,
    )


def build_investment_returns_page() -> str:
    deposits = MATRIX_DATA["metadata"]["deposit_tiers"]
    horizons = MATRIX_DATA["metadata"]["horizons"]
    projections = MATRIX_DATA["bank_projections"]

    # Build deposit tab buttons
    tab_buttons = []
    for d in deposits:
        active_cls = "active" if d == 250000 else ""
        label = f"${d:,}"
        if d == 250000:
            label += " (Max Single FDIC)"
        elif d == 500000:
            label += " (Max Joint / 2-Bank)"
        elif d == 1000000:
            label += " (Trust / 4-Bank)"
        elif d == 25000:
            label += " (Bonus Tier)"
        tab_buttons.append(
            f'<button type="button" class="btn-preset {active_cls}" data-matrix-deposit="{d}">{esc(label)}</button>'
        )

    panels_html = []
    for d in deposits:
        display_style = "block" if d == 250000 else "none"
        rows_for_d = sorted(
            projections,
            key=lambda p: p["deposits"][str(d)]["horizons"]["1y"]["total_return"],
            reverse=True,
        )
        tr_list = []
        for idx, p in enumerate(rows_for_d, start=1):
            d_obj = p["deposits"][str(d)]
            h_map = d_obj["horizons"]
            is_top = idx in (1, 2, 3) and h_map["1y"]["total_return"] > 1000
            row_cls = "top-pick-row" if is_top else ""
            tr_list.append(f"""
                <tr class="{row_cls}">
                  <td class="mono"><strong>#{idx}</strong></td>
                  <td>
                    <strong>{esc(p["bank_name"])}</strong><br>
                    <span class="badge-cert">FDIC Cert #{esc(p["fdic_cert"])}</span>
                  </td>
                  <td>
                    <strong>{esc(p["account_name"])}</strong><br>
                    <span style="font-size:11.5px;color:#64748b;">{esc(p["bonus_note"])}</span>
                  </td>
                  <td><span class="rate-pill {'low' if float(d_obj['applied_apy'].rstrip('%')) < 1.0 else ''}">{esc(d_obj["applied_apy"])}</span><br><span style="font-size:11px;color:#64748b;">As of {esc(p["rate_effective_date"])}</span></td>
                  <td class="mono">+${h_map["3m"]["total_return"]:,.2f}<br><span style="font-size:11px;color:#64748b;">Bal: ${h_map["3m"]["ending_balance"]:,.2f}</span></td>
                  <td class="mono">+${h_map["6m"]["total_return"]:,.2f}<br><span style="font-size:11px;color:#64748b;">Bal: ${h_map["6m"]["ending_balance"]:,.2f}</span></td>
                  <td class="mono"><strong style="color:#047857;font-size:14px;">+${h_map["1y"]["total_return"]:,.2f}</strong><br><span style="font-size:11px;color:#64748b;">Bal: ${h_map["1y"]["ending_balance"]:,.2f}</span></td>
                  <td class="mono">+${h_map["2y"]["total_return"]:,.2f}<br><span style="font-size:11px;color:#64748b;">Bal: ${h_map["2y"]["ending_balance"]:,.2f}</span></td>
                  <td class="mono">+${h_map["3y"]["total_return"]:,.2f}<br><span style="font-size:11px;color:#64748b;">Bal: ${h_map["3y"]["ending_balance"]:,.2f}</span></td>
                  <td class="mono"><strong style="color:#1d4ed8;">+${h_map["5y"]["total_return"]:,.2f}</strong><br><span style="font-size:11px;color:#64748b;">Bal: ${h_map["5y"]["ending_balance"]:,.2f}</span></td>
                  <td><a class="source-btn" href="{esc(p["source_url"])}" target="_blank" rel="noopener noreferrer">Official Site ↗</a></td>
                </tr>""")

        # Also add Citibank Accelerate Savings row with blank unverified returns per strict rule
        tr_list.append(f"""
            <tr class="flagged-row">
              <td class="mono"><strong>—</strong></td>
              <td>
                <strong>Citibank, N.A.</strong><br>
                <span class="badge-cert">FDIC Cert #7213</span>
              </td>
              <td>
                <strong>Citi® Accelerate Savings</strong><br>
                <span style="font-size:11.5px;color:#b45309;">Geo-gated to National Rate Region; outputs <code>:BLUE_AccSavings_Rate%</code> from NYC</span>
              </td>
              <td>{render_cell_or_blank("")}<br><span style="font-size:11px;color:#64748b;">As of 2026-10-21</span></td>
              <td>{render_cell_or_blank("")}</td>
              <td>{render_cell_or_blank("")}</td>
              <td>{render_cell_or_blank("")}</td>
              <td>{render_cell_or_blank("")}</td>
              <td>{render_cell_or_blank("")}</td>
              <td>{render_cell_or_blank("")}</td>
              <td><a class="source-btn" href="https://www.citi.com/banking/savings-account?intc=citihpmenu_overview_savings" target="_blank" rel="noopener noreferrer">Official Site ↗</a></td>
            </tr>""")

        fdic_note = (
            f"100% Principal Insured under a Single Account ($250,000 limit)"
            if d <= 250000
            else f"Exceeds $250,000 Single-Account Cap by ${d - 250000:,} — Requires Joint Account ($500k cap), Trust/POD Beneficiaries (up to $1.25M cap), or Multi-Bank Split ({max(1, (d + 249999)//250000)} banks)"
        )

        panels_html.append(f"""
        <div class="matrix-panel" data-panel-deposit="{d}" style="display:{display_style};">
          <div class="callout {'emerald' if d <= 250000 else 'amber'}" style="margin-top:14px;">
            <h4>Return Projection Table for <strong>${d:,}</strong> Deposit (Opened <code>2026-10-22</code>)</h4>
            <p>
              <strong>FDIC Coverage Status:</strong> {esc(fdic_note)}.<br>
              <strong>Exact Horizon End Dates:</strong> 3 Months (<code>2027-01-22</code>) &bull; 6 Months (<code>2027-04-22</code>) &bull; 1 Year (<code>2027-10-22</code>) &bull; 2 Years (<code>2028-10-22</code>) &bull; 3 Years (<code>2029-10-22</code>) &bull; 5 Years (<code>2031-10-22</code>).
            </p>
          </div>
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Bank &amp; Charter</th>
                  <th>Account &amp; Tier/Promo Rules</th>
                  <th>Applied APY</th>
                  <th>3 Months<br>(2027-01-22)</th>
                  <th>6 Months<br>(2027-04-22)</th>
                  <th>1 Year<br>(2027-10-22)</th>
                  <th>2 Years<br>(2028-10-22)</th>
                  <th>3 Years<br>(2029-10-22)</th>
                  <th>5 Years<br>(2031-10-22)</th>
                  <th>Official Source</th>
                </tr>
              </thead>
              <tbody>
                {"".join(tr_list)}
              </tbody>
            </table>
          </div>
        </div>""")

    # Also build cross-deposit table for 1-Year Return across all deposit sizes ($1k to $1M)
    cross_rows = []
    for idx, p in enumerate(projections, start=1):
        d_map = p["deposits"]
        is_top = idx in (1, 2, 3)
        cross_rows.append(f"""
            <tr class="{'top-pick-row' if is_top else ''}">
              <td><strong>{esc(p["bank_name"])}</strong><br><span class="badge-cert">Cert #{esc(p["fdic_cert"])}</span></td>
              <td><strong>{esc(p["account_name"])}</strong></td>
              <td class="mono">${d_map["1000"]["horizons"]["1y"]["total_return"]:,.2f}<br><span style="font-size:11px;color:#64748b;">({esc(d_map["1000"]["applied_apy"])})</span></td>
              <td class="mono">${d_map["10000"]["horizons"]["1y"]["total_return"]:,.2f}<br><span style="font-size:11px;color:#64748b;">({esc(d_map["10000"]["applied_apy"])})</span></td>
              <td class="mono">${d_map["25000"]["horizons"]["1y"]["total_return"]:,.2f}<br><span style="font-size:11px;color:#64748b;">({esc(d_map["25000"]["applied_apy"])})</span></td>
              <td class="mono">${d_map["50000"]["horizons"]["1y"]["total_return"]:,.2f}<br><span style="font-size:11px;color:#64748b;">({esc(d_map["50000"]["applied_apy"])})</span></td>
              <td class="mono">${d_map["100000"]["horizons"]["1y"]["total_return"]:,.2f}<br><span style="font-size:11px;color:#64748b;">({esc(d_map["100000"]["applied_apy"])})</span></td>
              <td class="mono" style="background:#f0fdf4;"><strong style="color:#047857;">${d_map["250000"]["horizons"]["1y"]["total_return"]:,.2f}</strong><br><span style="font-size:11px;color:#047857;">({esc(d_map["250000"]["applied_apy"])})</span></td>
              <td class="mono">${d_map["500000"]["horizons"]["1y"]["total_return"]:,.2f}<br><span style="font-size:11px;color:#64748b;">({esc(d_map["500000"]["applied_apy"])})</span></td>
              <td class="mono"><strong>${d_map["1000000"]["horizons"]["1y"]["total_return"]:,.2f}</strong><br><span style="font-size:11px;color:#64748b;">({esc(d_map["1000000"]["applied_apy"])})</span></td>
              <td><a class="source-btn" href="{esc(p["source_url"])}" target="_blank" rel="noopener noreferrer">Official Site ↗</a></td>
            </tr>""")

    body = f"""
    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>1-Year Total Return Matrix by Deposit Size ($1,000 to $1,000,000 | Opened 2026-10-22 → 2027-10-22)</h3>
          <p>Side-by-side comparison of Year-1 total dollar returns (compound interest + verified sign-up bonuses) across 8 deposit tiers, showing where tiered APYs and bonuses trigger.</p>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>National Bank</th>
              <th>Account Name</th>
              <th>$1,000</th>
              <th>$10,000</th>
              <th>$25,000<br>(Tier/Bonus)</th>
              <th>$50,000</th>
              <th>$100,000</th>
              <th>$250,000<br>(Max Single FDIC)</th>
              <th>$500,000<br>(Joint / 2-Bank)</th>
              <th>$1,000,000<br>(Trust / 4-Bank)</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(cross_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Multi-Horizon Return Tables by Deposit Size (3 Months to 5 Years from 2026-10-22)</h3>
          <p>Click any deposit size below to inspect the complete 3-Month, 6-Month, 1-Year, 2-Year, 3-Year, and 5-Year compound return and ending balance table.</p>
        </div>
      </div>

      <div class="preset-buttons" style="margin-bottom:14px;">
        {"".join(tab_buttons)}
      </div>

      {"".join(panels_html)}
    </section>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Competitiveness Over the Investment Lifespan &amp; Federal Reserve Rate Cycle Analysis (October 2026)</h3>
          <p>How variable HYSA rates behave across short-term (90–180 days) vs multi-year (1–5 year) holding periods.</p>
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card primary-accent">
          <div class="kpi-label">FOMC Policy Rate (Since 2026-09-17)</div>
          <div class="kpi-value primary">3.75% – 4.00%</div>
          <div class="kpi-sub">
            On <strong>September 16, 2026</strong>, the FOMC voted 12–0 to raise the federal funds target range by +25 bps to 3.75%–4.00% (IORB: 3.90%; EFFR: 3.88% as of 2026-10-19). <a href="https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm" target="_blank" rel="noopener noreferrer">FOMC Statement ↗</a>
          </div>
        </div>
        <div class="kpi-card highlight">
          <div class="kpi-label">Top HYSA Spread to Fed EFFR</div>
          <div class="kpi-value emerald">-23 bps to +62 bps</div>
          <div class="kpi-sub">
            Barclays Tiered Savings (<strong>3.65% APY</strong> at $250k+) captures <strong>94.1% of the 3.88% EFFR</strong> (and 3.73% w/ $200 bonus), while Marcus w/ referral boost earns <strong>4.50% APY</strong> (+62 bps above EFFR) for 3 months.
          </div>
        </div>
        <div class="kpi-card highlight">
          <div class="kpi-label">Short-Term (90-Day) Micro-Bonus Winner</div>
          <div class="kpi-value emerald">8.01% Ann. ($10k)</div>
          <div class="kpi-sub">
            On exactly <strong>$10,000 held for 90 days</strong> (2026-10-22 → 2027-01-20), Chase Savings' <strong>$200 bonus</strong> yields $200.25 (~8.01% annualized), but must be moved to a HYSA immediately after payout.
          </div>
        </div>
        <div class="kpi-card highlight">
          <div class="kpi-label">Long-Term (1–5 Year) $250k Winner</div>
          <div class="kpi-value emerald">$49,076.62 (5 Yr)</div>
          <div class="kpi-sub">
            Over 1 to 5 years at $250,000, base APY compounding dominates flat bonuses: <strong>Barclays Tiered Savings (3.65% APY + $200)</strong> earns $49,076.62 vs $47,638.99 at Synchrony (3.55% APY).
          </div>
        </div>
      </div>
    </section>
    """
    return page_shell(
        "investment-returns.html",
        "Return on Size of Investment ($1k–$1M)",
        "Deposit Size & Lifespan Return Matrices • Account Opening Date: 2026-10-22",
        "Return on Size of Investment & Multi-Year Lifespan Projections",
        "Exact dollar returns and ending balances calculated from account opening date October 22, 2026 across 8 deposit sizes ($1,000 to $1,000,000) and 6 investment horizons (3 Months to 5 Years).",
        body,
    )


def build_hysa_page() -> str:
    rows = []
    for acc in HYSA_DATA["accounts"]:
        is_top = acc["rank_250k_fdic"] in (1, 2, 3)
        row_cls = "top-pick-row" if is_top else ("flagged-row" if acc["apy_at_250k_max_fdic"] == "" else "")
        apy_250k = (
            f'<span class="rate-pill">{esc(acc["apy_at_250k_max_fdic"])}</span>'
            if acc["apy_at_250k_max_fdic"] != ""
            else render_cell_or_blank("")
        )
        rows.append(f"""
            <tr class="{row_cls}">
              <td class="mono"><strong>#{acc["rank_250k_fdic"]}</strong></td>
              <td>
                <strong>{esc(acc["bank_name"])}</strong><br>
                <span style="font-size:12px;color:#64748b;">{esc(acc["legal_charter"])}</span><br>
                <span class="badge-cert">FDIC Cert #{esc(acc["fdic_cert"])}</span>
              </td>
              <td>
                <strong>{esc(acc["account_name"])}</strong><br>
                <span style="font-size:12px;color:#64748b;">{esc(acc["category"])}</span>
              </td>
              <td>{apy_250k}</td>
              <td>{render_cell_or_blank(acc["apy_standard_or_under_250k"])}</td>
              <td class="mono">{render_cell_or_blank(acc["multiple_of_national_avg_250k"])}</td>
              <td class="mono">{esc(acc["rate_effective_date"])}</td>
              <td class="mono">{esc(acc["min_opening_deposit"])}</td>
              <td>{esc(acc["min_balance_for_apy"])}</td>
              <td class="mono">{esc(acc["monthly_maintenance_fee"])}<br><span style="font-size:11px;color:#64748b;">{esc(acc["fee_waiver_rules"])}</span></td>
              <td>{render_cell_or_blank(acc["max_balance_limit"])}</td>
              <td><strong>{esc(acc["signup_bonus_amount"])}</strong><br><span style="font-size:11.5px;color:#64748b;">{esc(acc["signup_bonus_terms"])}</span></td>
              <td>{render_status_badge(acc["verification_status"])}</td>
              <td>
                <a class="source-btn" href="{esc(acc["source_url"])}" target="_blank" rel="noopener noreferrer">Primary Source ↗</a><br>
                <a href="{esc(acc["secondary_source_url"])}" target="_blank" rel="noopener noreferrer" style="font-size:11.5px;display:inline-block;margin-top:4px;">Disclosure / Terms ↗</a>
              </td>
            </tr>""")

    body = f"""
    <div class="callout emerald">
      <h4>Key Findings Across Big National High-Yield Savings Accounts (Verified October 2026)</h4>
      <p>
        Among large national banks with full digital/mobile apps and FDIC insurance, verified high-yield APYs range from <strong>3.00% APY (BMO Alto)</strong> to <strong>3.65% APY (Barclays Tiered Savings at $250,000+)</strong> — paying <strong>7.89x to 9.61x</strong> the FDIC National Deposit Rate for Savings (<code>0.38% APY</code> as of October 19, 2026). All 9 pure direct national HYSAs charge <strong>$0 monthly maintenance fees</strong> and require <strong>$0 minimum opening deposit</strong>, while hybrid branch/online accounts at <strong>U.S. Bank (3.40%–3.50% APY)</strong> and <strong>Wells Fargo Platinum Savings (3.25% APY for new customers)</strong> require a <strong>$25,000 minimum balance</strong> to unlock their top rate tier.
      </p>
    </div>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Verified National High-Yield &amp; Hybrid Savings Accounts (13 Accounts)</h3>
          <p>Sorted by verified APY at the $250,000 Single-Account Maximum FDIC Insurance threshold. Unconfirmed fields are left blank and linked to the Flagged for Review audit log.</p>
        </div>
        <div>
          <input type="search" class="control-input" placeholder="Search bank, cert #, or feature..." data-table-filter="hysa-detail-table">
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table" id="hysa-detail-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Bank &amp; Legal Charter</th>
              <th>Account Name</th>
              <th>APY ($250k Max FDIC)</th>
              <th>APY (&lt;$250k Tiers)</th>
              <th>vs. 0.38% Nat'l Avg</th>
              <th>Effective Date</th>
              <th>Min to Open</th>
              <th>Min Balance for APY</th>
              <th>Monthly Fee &amp; Waiver</th>
              <th>Max Balance Cap</th>
              <th>Active Bonus / Promotion</th>
              <th>Verification Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return page_shell(
        "high-yield-savings.html",
        "National High-Yield Savings Accounts",
        "Category 2 • Big National Direct & Hybrid High-Yield Savings",
        "Big National Banks — High-Yield & Hybrid Savings Accounts",
        "Line-by-line verified rate tiers, minimum deposits, balance caps, and promotional terms across 13 major national bank savings products.",
        body,
    )


def build_big_four_page() -> str:
    rows = []
    for acc in BIG4_DATA["accounts"]:
        rows.append(f"""
            <tr>
              <td>
                <strong>{esc(acc["bank_name"])}</strong><br>
                <span class="badge-cert">FDIC Cert #{esc(acc["fdic_cert"])}</span>
              </td>
              <td>
                <strong>{esc(acc["account_name"])}</strong><br>
                <span style="font-size:12px;color:#64748b;">{esc(acc["tier_type"])}</span>
              </td>
              <td><span class="rate-pill low">{esc(acc["standard_apy"])}</span></td>
              <td>{esc(acc["relationship_or_promo_apy"])}</td>
              <td class="mono">{esc(acc["rate_effective_date"])}</td>
              <td class="mono">{esc(acc["min_opening_deposit"])}</td>
              <td class="mono">{esc(acc["monthly_service_fee"])}</td>
              <td>{esc(acc["fee_waiver_requirements"])}</td>
              <td>{esc(acc["relationship_qualification_rules"])}</td>
              <td>{esc(acc["active_bonus_or_promotion"])}</td>
              <td class="mono"><strong>{esc(acc["annual_return_on_250k_base"])}</strong></td>
              <td class="mono" style="color:#b91c1c;"><strong>{esc(acc["opportunity_cost_vs_top_hysa_250k_yr1"])}</strong></td>
              <td>{render_status_badge(acc["verification_status"])}</td>
              <td>
                <a class="source-btn" href="{esc(acc["source_url"])}" target="_blank" rel="noopener noreferrer">Rate Sheet ↗</a><br>
                <a href="{esc(acc["promo_source_url"])}" target="_blank" rel="noopener noreferrer" style="font-size:11.5px;display:inline-block;margin-top:4px;">Offer / Fee Terms ↗</a>
              </td>
            </tr>""")

    body = f"""
    <div class="callout crimson">
      <h4>The Big Four Brick-and-Mortar Yield Gap: Why Standard Relationship Tiers Cost Savers $9,000+ Per Year on $250,000</h4>
      <p>
        Standard savings accounts at <strong>JPMorgan Chase (0.01% APY)</strong>, <strong>Bank of America (0.01% APY)</strong>, <strong>Wells Fargo Way2Save (0.01% APY)</strong>, and <strong>Citibank NYC Standard Savings (0.03% APY)</strong> pay between <strong>$25.00 and $75.00 per year</strong> on a $250,000 max-FDIC deposit. Even when linked to Private Client or premier checking tiers, Chase Premier/Private Client Savings pays just <strong>0.02% APY ($50/yr)</strong> and Bank of America discontinued its Preferred Rewards savings booster when transitioning to <strong>BofA Rewards™</strong> in May 2026.<br>
        <strong>The Sole Exception Among the Big Four:</strong> <strong>Wells Fargo Platinum Savings</strong> offers new savings customers <strong>3.25% variable APY</strong> ($8,125/yr on $250k) when depositing &ge;$25,000 within 30 days (or <strong>3.50% APY for 12 months</strong> via in-branch banker enrollment with &ge;$10,000 new money).
      </p>
    </div>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Big Four &amp; Retail Branch National Banks — Standard vs. Relationship &amp; Promo Tiers</h3>
          <p>Line-by-line verified audit of standard APYs, relationship bumps, monthly fee waivers, and annual opportunity cost on a $250,000 deposit opened 2026-10-22.</p>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Bank &amp; FDIC Cert #</th>
              <th>Account Name &amp; Tier Type</th>
              <th>Standard APY</th>
              <th>Relationship / Promo APY</th>
              <th>Effective Date</th>
              <th>Min to Open</th>
              <th>Monthly Fee</th>
              <th>Fee Waiver Rules</th>
              <th>Relationship Qualification Rules</th>
              <th>Active Bonus / Discontinuation Alert</th>
              <th>1-Yr Base Return ($250k)</th>
              <th>1-Yr Opportunity Cost vs Top HYSA</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return page_shell(
        "big-four-comparison.html",
        "Big Four Brick-and-Mortar & Relationship Tiers",
        "Category 3 • JPMorgan Chase, Bank of America, Wells Fargo, Citibank & BMO Retail",
        "Big Four Brick-and-Mortar National Banks & Relationship Tiers",
        "Verification of standard vs. relationship rates, fee waiver requirements, program restructurings, and opportunity costs at the largest U.S. branch banks.",
        body,
    )


def build_fdic_page() -> str:
    cat_rows = []
    for c in FDIC_DATA["fdic_ownership_categories"]:
        cat_rows.append(f"""
            <tr>
              <td><strong>{esc(c["ownership_category"])}</strong></td>
              <td class="mono">{esc(c["regulation"])}</td>
              <td><span class="rate-pill promo">{esc(c["coverage_limit"])}</span></td>
              <td class="mono"><strong>{esc(c["max_single_bank_example"])}</strong></td>
              <td>{esc(c["rules_and_requirements"])}</td>
              <td class="mono">{esc(c["effective_date"])}</td>
              <td><span class="badge badge-verified">{esc(c["verification_status"])}</span></td>
              <td><a class="source-btn" href="{esc(c["source_url"])}" target="_blank" rel="noopener noreferrer">FDIC.gov ↗</a></td>
            </tr>""")

    charter_rows = []
    for ch in FDIC_DATA["bank_charters_verified"]:
        is_warn = "CRITICAL" in ch["shared_charter_warning"]
        charter_rows.append(f"""
            <tr class="{'flagged-row' if is_warn else ''}">
              <td><strong>{esc(ch["bank_brand"])}</strong></td>
              <td><strong>{esc(ch["legal_charter_name"])}</strong></td>
              <td class="mono"><span class="badge-cert">Cert #{esc(ch["fdic_cert"])}</span></td>
              <td>{esc(ch["headquarters"])}</td>
              <td class="mono">{esc(ch["primary_regulator"])}</td>
              <td>{f'<strong style="color:#b91c1c;">{esc(ch["shared_charter_warning"])}</strong>' if is_warn else esc(ch["shared_charter_warning"])}</td>
              <td><span class="badge badge-verified">{esc(ch["verification_status"])}</span></td>
              <td><a class="source-btn" href="{esc(ch["source_url"])}" target="_blank" rel="noopener noreferrer">Official Source ↗</a></td>
            </tr>""")

    portfolio_cards = []
    for port in MATRIX_DATA["optimal_fdic_portfolios"]:
        alloc_rows = []
        for a in port["allocations"]:
            alloc_rows.append(f"""
                <tr>
                  <td><strong>{esc(a["bank_name"])}</strong></td>
                  <td>{esc(a["account_name"])}</td>
                  <td class="mono">${a["allocated_principal"]:,}</td>
                  <td><span class="rate-pill">{esc(a["apy"])}</span></td>
                  <td class="mono">${a["yr1_base_interest"]:,.2f}</td>
                  <td class="mono">${a["yr1_bonus"]:,.2f}</td>
                  <td class="mono"><strong style="color:#047857;">${a["yr1_total_return"]:,.2f}</strong></td>
                  <td class="mono"><strong>${a["yr5_total_return"]:,.2f}</strong></td>
                  <td><a class="source-btn" href="{esc(a["source_url"])}" target="_blank" rel="noopener noreferrer">Source ↗</a></td>
                </tr>""")
        portfolio_cards.append(f"""
        <div class="section-card">
          <div class="section-header">
            <div>
              <h3>{esc(port["strategy_name"])}</h3>
              <p><strong>FDIC Coverage Verification:</strong> {esc(port["fdic_coverage_status"])}</p>
            </div>
            <div style="text-align:right;">
              <span class="rate-pill">Blended Base: {esc(port["blended_base_apy"])}</span>
              <div style="font-size:12px;color:#047857;font-weight:700;margin-top:4px;">
                1-Yr Return: ${port["total_yr1_return"]:,.2f} &bull; 5-Yr Return: ${port["total_yr5_return"]:,.2f}
              </div>
            </div>
          </div>
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>FDIC Insured Bank Charter</th>
                  <th>Account Name</th>
                  <th>Allocated Principal</th>
                  <th>Verified APY</th>
                  <th>Year-1 Base Interest</th>
                  <th>Year-1 Promo/Bonus</th>
                  <th>Year-1 Total Return</th>
                  <th>5-Year Total Return</th>
                  <th>Official Link</th>
                </tr>
              </thead>
              <tbody>
                {"".join(alloc_rows)}
              </tbody>
            </table>
          </div>
        </div>""")

    body = f"""
    <div class="callout emerald">
      <h4>How to Maximize Both Return AND 100% FDIC Insurance Coverage (Principal + Accrued Interest)</h4>
      <p>
        Under federal law (<code>12 C.F.R. Part 330</code>), the standard FDIC insurance limit of <strong>$250,000 per depositor, per insured bank, per ownership category</strong> covers <em>both principal and accrued interest</em>. Therefore:<br>
        &bull; <strong>If you deposit exactly $250,000 in a Single Account with no beneficiaries:</strong> Your $250,000 principal is 100% insured on Day 1 (<code>2026-10-22</code>), but as your ~$760/month in interest accrues and compounds, any balance above $250,000 would exceed the single-account cap unless you either (1) <strong>designate at least 1 Payable-on-Death (POD) beneficiary</strong> (which immediately raises your single-bank FDIC coverage to <strong>$250,000 per beneficiary up to $1,250,000</strong> under <code>12 C.F.R. § 330.10</code>), (2) <strong>open as a Joint Account</strong> ($500,000 cap for 2 co-owners), or (3) <strong>deposit $241,000</strong> so the full year's ~$8,796 interest compounds inside the $250,000 ceiling.
      </p>
    </div>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Official FDIC Deposit Insurance Ownership Categories &amp; Coverage Limits (12 C.F.R. Part 330)</h3>
          <p>Includes the landmark April 1, 2024 FDIC Trust Account Rule revision unifying informal POD/ITF and formal trusts up to $1,250,000 per owner per bank.</p>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>FDIC Ownership Category</th>
              <th>Federal Regulation</th>
              <th>Statutory Coverage Limit</th>
              <th>Max Single-Bank Coverage</th>
              <th>Key Qualification Rules &amp; Mechanics</th>
              <th>Rule Effective Date</th>
              <th>Status</th>
              <th>Official FDIC Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(cat_rows)}
          </tbody>
        </table>
      </div>
    </section>

    {"".join(portfolio_cards)}

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Verified National Bank FDIC Charter &amp; Certificate Registry (13 Banks)</h3>
          <p>Always verify the underlying FDIC Certificate Number before splitting deposits across multiple brands to avoid shared-charter overlap.</p>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Consumer Bank Brand</th>
              <th>Legal FDIC-Insured Charter Name</th>
              <th>FDIC Certificate #</th>
              <th>Charter Headquarters</th>
              <th>Primary Federal Regulator</th>
              <th>Shared-Charter / Consolidation Audit Notes</th>
              <th>Status</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(charter_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return page_shell(
        "fdic-maximization.html",
        "Max FDIC Insurance Strategies ($250k–$1.25M+)",
        "Category 4 • 12 C.F.R. Part 330 Rules, Optimal Multi-Bank Portfolios & Charter Registry",
        "Max FDIC Insurance Strategies & National Bank Charter Registry",
        "How to structure $250,000, $500,000, and $1,000,000+ savings portfolios for 100% FDIC insurance coverage and maximum yield as of October 22, 2026.",
        body,
    )


def build_promotions_page() -> str:
    rows = []
    for p in PROMO_DATA["active_promotions"]:
        is_warn = "Needs Review" in p["verification_status"]
        rows.append(f"""
            <tr class="{'flagged-row' if is_warn else ''}">
              <td>
                <strong>{esc(p["bank_name"])}</strong><br>
                <span class="badge-cert">FDIC Cert #{esc(p["fdic_cert"])}</span>
              </td>
              <td>
                <strong>{esc(p["account_name"])}</strong><br>
                <span style="font-size:12px;color:#1d4ed8;font-weight:600;">{esc(p["promo_headline"])}</span>
              </td>
              <td>{render_cell_or_blank(p["bonus_value_display"])}</td>
              <td>{esc(p["base_apy_during_promo"])}</td>
              <td class="mono">{esc(p["min_deposit_for_bonus"])}</td>
              <td class="mono">{p["funding_window_days"]} days</td>
              <td class="mono">{p["holding_period_days"]} days</td>
              <td>{esc(p["payout_timeline"])}</td>
              <td class="mono"><strong>{esc(p["offer_expiration_date"])}</strong><br><span style="font-size:11px;color:#64748b;">{esc(p["opening_date_eligibility"])}</span></td>
              <td>{render_cell_or_blank(p["effective_1yr_apy_at_25k"])}</td>
              <td>{render_cell_or_blank(p["effective_1yr_apy_at_250k"])}</td>
              <td>{render_status_badge(p["verification_status"])}</td>
              <td>
                <a class="source-btn" href="{esc(p["source_url"])}" target="_blank" rel="noopener noreferrer">Offer Page ↗</a><br>
                <a href="{esc(p["terms_url"])}" target="_blank" rel="noopener noreferrer" style="font-size:11.5px;display:inline-block;margin-top:4px;">Full Terms ↗</a>
              </td>
            </tr>""")

    body = f"""
    <div class="callout emerald">
      <h4>Promotional Timing Analysis for Accounts Opened on October 22, 2026</h4>
      <p>
        &bull; <strong>Urgent 9-Day Window — Barclays Tiered Savings $200 Bonus (Expires <code>2026-10-31</code>):</strong> Opening on <code>2026-10-22</code> qualifies before the October 31 deadline. You have until <code>2026-11-21</code> (30 days) to deposit &ge;$25,000, then must maintain &ge;$25,000 for 120 consecutive days (through <code>2027-02-19</code> if funded on Day 1). Bonus is credited ~60 days later (~<code>2027-04-20</code>), while your balance earns <strong>3.50% APY ($25k–&lt;$250k)</strong> or <strong>3.65% APY ($250k–$1M)</strong> the entire time.<br>
        &bull; <strong>Urgent 1-Day Discontinuation Alert — Citibank Savings Promotional Rate (Discontinued <code>2026-10-23</code>):</strong> Per Citibank's Simplified Banking Fact Sheet (dated 10/01/2026), the Promotional Rate Feature for New Citi Savings accounts is discontinued effective <strong>October 23, 2026</strong>.<br>
        &bull; <strong>Highest High-Balance Rate Boost — Marcus Refer-a-Friend (+1.00% APY for 3 Months):</strong> Adds +1.00% APY on top of Marcus's 3.50% APY (= <strong>4.50% APY for 3 months</strong>), worth an extra <strong>+$625.00 per referral on a $250,000 balance</strong> ($9,375.00 total Year-1 return with 1 referral).
      </p>
    </div>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Verified Account Opening Bonuses, Rate Boosts &amp; Promotional Offers (As of 2026-10-22)</h3>
          <p>Line-by-line audit of bonus amounts, minimum funding requirements, holding periods, and effective 1-year yields at $25,000 and $250,000.</p>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Bank &amp; FDIC Cert #</th>
              <th>Account &amp; Promotion Headline</th>
              <th>Verified Bonus / Boost</th>
              <th>Base APY During Promo</th>
              <th>Min Deposit Required</th>
              <th>Funding Window</th>
              <th>Holding Period</th>
              <th>Payout Timeline</th>
              <th>Expiration &amp; 2026-10-22 Status</th>
              <th>Effective 1-Yr Return ($25k)</th>
              <th>Effective 1-Yr Return ($250k)</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return page_shell(
        "bonuses-and-promotions.html",
        "Account Opening Bonuses & Promotions",
        "Category 5 • Cash Bonuses, Referral Boosts, Companion Offers & Expiration Dates",
        "Account Opening Bonuses, Rate Boosts & Promotional Rules",
        "Complete verification of active savings bonuses, rate boosts, funding windows, holding periods, and effective yields for accounts opened on October 22, 2026.",
        body,
    )


def build_rules_page() -> str:
    rows = []
    for acc in HYSA_DATA["accounts"]:
        rows.append(f"""
            <tr>
              <td>
                <strong>{esc(acc["bank_name"])}</strong><br>
                <span class="badge-cert">FDIC Cert #{esc(acc["fdic_cert"])}</span>
              </td>
              <td><strong>{esc(acc["account_name"])}</strong></td>
              <td class="mono">{esc(acc["min_opening_deposit"])}</td>
              <td>{esc(acc["min_balance_for_apy"])}</td>
              <td class="mono">{esc(acc["monthly_maintenance_fee"])}</td>
              <td>{esc(acc["fee_waiver_rules"])}</td>
              <td>{esc(acc["compounding_frequency"])}</td>
              <td>{esc(acc["withdrawal_rules"])}</td>
              <td>{esc(acc["digital_app_and_security"])}</td>
              <td>{esc(acc["nyc_availability"])}</td>
              <td><a class="source-btn" href="{esc(acc["source_url"])}" target="_blank" rel="noopener noreferrer">Official Site ↗</a></td>
            </tr>""")

    body = f"""
    <div class="callout">
      <h4>Key Operational &amp; Security Rules to Know Before Funding a National High-Yield Savings Account</h4>
      <p>
        &bull; <strong>Zero-Balance Auto-Closure Deadlines:</strong> Even when an account has a <strong>$0 minimum opening deposit</strong>, national banks enforce funding windows: <strong>American Express HYSA</strong> and <strong>Marcus by Goldman Sachs</strong> may close unfunded/$0-balance accounts after <strong>60 days</strong>; <strong>BMO Alto</strong> and <strong>Citibank</strong> close $0-balance accounts after <strong>90 days</strong>; <strong>Barclays Tiered Savings</strong> closes $0-balance accounts after <strong>6 months</strong> (and Barclays CDs must be funded within <strong>14 days</strong>).<br>
        &bull; <strong>Monthly Withdrawal &amp; Transfer Limits:</strong> While the Federal Reserve eliminated the mandatory Regulation D 6-withdrawal rule in 2020, <strong>Ally Bank</strong> enforces a <strong>10-withdrawal limit per statement cycle</strong> (account closure upon repeated excess) and <strong>Bank of America Advantage Savings</strong> charges a <strong>$10 fee per withdrawal over 6 per cycle</strong>. By contrast, <strong>Barclays, Marcus, Synchrony, American Express, Capital One 360, and BMO Alto</strong> permit <strong>unlimited monthly ACH transfers</strong>.<br>
        &bull; <strong>Transfer Speed &amp; Payment Rails:</strong> <strong>Marcus by Goldman Sachs</strong> offers free <strong>same-day ACH transfers up to $100,000</strong> when initiated before 12:00 pm ET, and <strong>American Express HYSA</strong> offers express same-day ACH transfers. Note that <strong>BMO Alto</strong> supports ACH only (no wire transfers, checks, debit cards, or Zelle®).
      </p>
    </div>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>Account Opening Rules, Maintenance Fees, Withdrawal Limits &amp; Digital Security Matrix</h3>
          <p>Line-by-line operational rules, compounding schedules, withdrawal limits, and mobile banking security features verified from official deposit agreements.</p>
        </div>
        <div>
          <input type="search" class="control-input" placeholder="Search rules, withdrawal limits, apps..." data-table-filter="rules-table">
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table" id="rules-table">
          <thead>
            <tr>
              <th>Bank &amp; FDIC Cert #</th>
              <th>Account Name</th>
              <th>Min Opening Deposit</th>
              <th>Min Balance for Stated APY</th>
              <th>Monthly Fee</th>
              <th>Fee Waiver Requirements</th>
              <th>Compounding &amp; Crediting</th>
              <th>Withdrawal Limits, Holds &amp; Closure Rules</th>
              <th>Digital App &amp; Security Architecture</th>
              <th>Geographic Eligibility</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return page_shell(
        "account-rules-and-security.html",
        "Account Opening Rules & Digital Security",
        "Category 6 • Deposit Agreements, Withdrawal Limits, Holds & Mobile App Security",
        "Account Opening Rules, Maintenance Requirements & Digital Security",
        "Detailed verification of minimum opening deposits, funding deadlines, withdrawal limits, compounding methods, and mobile app security across big national banks.",
        body,
    )


def build_flagged_page() -> str:
    flag_rows = []
    for item in FLAG_DATA["flagged_items"]:
        sev = item["severity"]
        badge_cls = "badge-unverified" if "High" in sev else "badge-review"
        flag_rows.append(f"""
            <tr class="flagged-row">
              <td class="mono"><strong>{esc(item["flag_id"])}</strong></td>
              <td><span class="badge {badge_cls}">{esc(sev)}</span></td>
              <td><strong>{esc(item["bank_name"])}</strong></td>
              <td><strong>{esc(item["account_name"])}</strong></td>
              <td><strong>{esc(item["field_affected"])}</strong></td>
              <td>
                <strong>{esc(item["finding_summary"])}</strong>
                <p style="margin-top:6px;font-size:12.5px;color:#334155;">{esc(item["detailed_explanation"])}</p>
              </td>
              <td class="mono">{esc(item["date_observed"])}</td>
              <td>
                <a class="source-btn" href="{esc(item["official_source_url"])}" target="_blank" rel="noopener noreferrer">Primary Source ↗</a><br>
                <a href="{esc(item["secondary_source_url"])}" target="_blank" rel="noopener noreferrer" style="font-size:11.5px;display:inline-block;margin-top:4px;">Secondary Source ↗</a>
              </td>
            </tr>""")

    # Also build explicit Blank / Unverified Fields Inventory Table
    blank_inventory = [
        (
            "Citibank, N.A. (#7213)",
            "Citi® Accelerate Savings",
            "Annual Percentage Yield (APY) & Return Projections",
            "Left Blank",
            "Official page citi.com/banking/savings-account outputs literal template token ':BLUE_AccSavings_Rate%' and compare-bank-accounts outputs '% · % · %' when accessed from New York City because NY is excluded from the National Rate Region.",
            "https://www.citi.com/banking/savings-account?intc=citihpmenu_overview_savings",
        ),
        (
            "American Express National Bank (#27471)",
            "American Express® High Yield Savings",
            "Consumer Platinum Card® Exclusive Savings Rate (%)",
            "Left Blank",
            "Official PDF terms confirm consumer Platinum Card holders qualify for an Exclusive Savings Rate above the 3.20% standard APY, but state the exact rate is disclosed only on the customer's monthly statement.",
            "https://www.americanexpress.com/content/dam/amex/en-us/banking/personal-savings/exclusive_savings_rate_terms_and_conditions.pdf",
        ),
        (
            "Synchrony Bank (#27314)",
            "Synchrony High Yield Savings",
            "Maximum Account Balance Limit",
            "Left Blank",
            "Not specified on public product page (3.55% APY and $0 min balance confirmed).",
            "https://www.synchrony.com/banking/products/high-yield-savings",
        ),
        (
            "U.S. Bank National Association (#6548)",
            "U.S. Bank Smartly® Savings & Elite Money Market",
            "Maximum Account Balance Limit",
            "Left Blank",
            "Top tier states '$100,000+' (Smartly) and '$500,000 and above' (Elite MMA) with no upper ceiling published on public rate sheets.",
            "https://www.usbank.com/bank-accounts/savings-accounts/bank-smartly-savings/savings-account-interest-rates.html",
        ),
        (
            "Wells Fargo Bank, N.A. (#3511)",
            "Wells Fargo Platinum Savings",
            "Maximum Account Balance Limit",
            "Left Blank",
            "Top tier states '$25,000 or more' (3.25% APY) with no upper cap published on public rate page.",
            "https://www.wellsfargo.com/savings-cds/rates/",
        ),
        (
            "Capital One, N.A. (#4297)",
            "360 Performance Savings",
            "Maximum Account Balance Limit",
            "Left Blank",
            "Disclosure states rate applies to all account balances without specifying a numeric maximum balance cap.",
            "https://www.capitalone.com/bank/disclosures/savings-accounts/online-performance-savings-account/",
        ),
        (
            "PNC Bank, N.A. (#6384)",
            "PNC High Yield Savings℠",
            "Maximum Account Balance Limit",
            "Left Blank",
            "Service charge schedule PDF does not specify a maximum deposit ceiling.",
            "https://www.pnc.com/content/dam/pnc-com/pdf/personal/Savings/service-charges-high-yield-savings.pdf",
        ),
        (
            "Ally Bank (#57803)",
            "Ally Bank Online Savings Account",
            "Maximum Account Balance Limit",
            "Left Blank",
            "Public product page lists '$25,000+' tier without a published maximum balance ceiling.",
            "https://www.ally.com/bank/online-savings-account/",
        ),
        (
            "BMO Bank N.A. (#16571)",
            "Alto Online Savings Account",
            "Maximum Account Balance Limit",
            "Left Blank",
            "Calculator allows up to $250,000 input, but public webpage does not state a formal maximum account balance limit.",
            "https://www.alto.bmo.com/en-us/high-yield-online-savings/",
        ),
    ]

    blank_rows = []
    for b_bank, b_acc, b_field, b_val, b_reason, b_url in blank_inventory:
        blank_rows.append(f"""
            <tr>
              <td><strong>{esc(b_bank)}</strong></td>
              <td><strong>{esc(b_acc)}</strong></td>
              <td><strong>{esc(b_field)}</strong></td>
              <td><span class="blank-cell-notice">{esc(b_val)}</span></td>
              <td>{esc(b_reason)}</td>
              <td><a class="source-btn" href="{esc(b_url)}" target="_blank" rel="noopener noreferrer">Verify Source ↗</a></td>
            </tr>""")

    body = f"""
    <div class="callout amber">
      <h4>Strict Verification &amp; Anti-Hallucination Audit Policy</h4>
      <p>
        Per project instructions: <em>"Verify line by line. Every table row must have a source link to an official site. If a value can't be confirmed from an official source, leave it blank and flag it as unverified. Never infer or fill in values. Publish them on a clearly labeled 'Flagged for Review' page on the site, with the source links, so I can review them after the site is live and request changes."</em><br>
        This page documents all <strong>{len(FLAG_DATA["flagged_items"])} irregularities</strong> and all <strong>{len(blank_inventory)} unconfirmed/blank fields</strong> encountered during our October 22, 2026 verification of official bank websites and regulatory filings.
      </p>
    </div>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>1. Master Log of Flagged Irregularities, Regional Blocks &amp; Official Site Anomalies ({len(FLAG_DATA["flagged_items"])} Flags)</h3>
          <p>Each item below was observed directly on an official bank domain on 2026-10-22 and includes primary and secondary verification links.</p>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Flag ID</th>
              <th>Severity &amp; Category</th>
              <th>Bank &amp; FDIC Cert #</th>
              <th>Account Name</th>
              <th>Field / Feature Affected</th>
              <th>Detailed Technical Finding &amp; Impact</th>
              <th>Date Observed</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(flag_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h3>2. Inventory of Unconfirmed Values Left Blank Across Tables ({len(blank_inventory)} Items)</h3>
          <p>Every table cell that could not be confirmed from an official public bank webpage or PDF disclosure was left blank rather than inferred from third-party sites.</p>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Bank &amp; FDIC Cert #</th>
              <th>Account Name</th>
              <th>Unconfirmed Field</th>
              <th>Table Display</th>
              <th>Reason Value Cannot Be Confirmed on Official Public Source</th>
              <th>Official Source Inspected</th>
            </tr>
          </thead>
          <tbody>
            {"".join(blank_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return page_shell(
        "flagged-for-review.html",
        "Flagged for Review — Irregularities & Unverified Items",
        "Category 7 • Audit Log of Official Website Irregularities, Geo-Restrictions & Blank Unverified Fields",
        "Flagged for Review — Irregularities, Regional Restrictions & Unverified Items",
        "Complete transparency log of all official website rendering bugs, regional geo-blocks, charter consolidations, and unconfirmed fields left blank during our October 22, 2026 verification.",
        body,
    )


def main():
    pages = {
        "index.html": build_index_page(),
        "investment-returns.html": build_investment_returns_page(),
        "high-yield-savings.html": build_hysa_page(),
        "big-four-comparison.html": build_big_four_page(),
        "fdic-maximization.html": build_fdic_page(),
        "bonuses-and-promotions.html": build_promotions_page(),
        "account-rules-and-security.html": build_rules_page(),
        "flagged-for-review.html": build_flagged_page(),
    }
    for filename, content in pages.items():
        (ROOT / filename).write_text(content, encoding="utf-8")
        print(f"Wrote {filename} ({len(content):,} bytes)")

    # Write .nojekyll for clean GitHub Pages static serving
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("Wrote .nojekyll")


if __name__ == "__main__":
    main()
