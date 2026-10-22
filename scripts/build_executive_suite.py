#!/usr/bin/env python3
"""
Deterministic Static Site & SVG Visualization Builder for SAVINGS2.
Consumes strictly primary-verified datasets in `datasets/` and generates:
  - `index.html` (Executive Dashboard & Interactive Return/FDIC Decision Hub)
  - `national-banks.html`
  - `returns-by-deposit.html`
  - `rate-competitiveness.html`
  - `promotions-bonuses.html`
  - `opening-rules.html`
  - `fdic-security.html`
  - `flagged-review.html`
  - `.nojekyll` and comprehensive `README.md`
Also preserves all `session-46ab1baa` reference subpages (`accounts.html`, `returns.html`,
`competitiveness.html`, `bonuses.html`, `fdic.html`, `flagged.html`, `methodology.html`)
and adds a clean cross-suite banner link so every page in the repository is 100% reachable.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASETS = ROOT / "datasets"


def esc(val: object) -> str:
    return html.escape(str(val)) if val is not None else ""


def fmt_usd(val: float | int | None, decimals: int = 2) -> str:
    if val is None:
        return '<span class="blank-cell">—</span>'
    return f"${val:,.{decimals}f}"


def fmt_pct(val: float | None) -> str:
    if val is None:
        return '<span class="blank-cell">—</span>'
    return f"{val:.2f}%"


def fmt_assets(mil: float | int | None) -> str:
    if mil is None:
        return '<span class="blank-cell">—</span>'
    if mil >= 1_000_000:
        return f"${mil / 1_000_000:.2f}T"
    return f"${mil / 1_000:.1f}B"


NAV_ITEMS = [
    ("index.html", "Executive Hub", None, False),
    ("national-banks.html", "National Banks", "26", False),
    ("returns-by-deposit.html", "Returns & Max-FDIC", "$1k–$1M", False),
    ("rate-competitiveness.html", "Lifespan & Spreads", "3M–5Y", False),
    ("promotions-bonuses.html", "Promos & Bonuses", "9", False),
    ("opening-rules.html", "Rules, Min & Fees", None, False),
    ("fdic-security.html", "FDIC & Security", "$250k–$3.5M", False),
    ("flagged-review.html", "Flagged for Review", "25", True),
]

PRESERVED_REFERENCE_PAGES = [
    ("investment-returns.html", "Returns Matrix (v2)"),
    ("high-yield-savings.html", "HYSA Roster (v2)"),
    ("big-four-comparison.html", "Big Four (v2)"),
    ("fdic-maximization.html", "FDIC Guide (v2)"),
    ("bonuses-and-promotions.html", "Promos (v2)"),
    ("account-rules-and-security.html", "Rules & Security (v2)"),
    ("flagged-for-review.html", "Flags (v2)"),
    ("accounts.html", "Directory (v1)"),
    ("returns.html", "Returns (v1)"),
    ("competitiveness.html", "Benchmarks (v1)"),
    ("bonuses.html", "Bonuses (v1)"),
    ("fdic.html", "FDIC (v1)"),
    ("flagged.html", "Flags (v1)"),
    ("methodology.html", "Methodology"),
]


def page_shell(active_href: str, title: str, subtitle: str, eyebrow: str, body_html: str, hero_stats_html: str = "") -> str:
    nav_parts = []
    for href, label, cnt, is_flag in NAV_ITEMS:
        cls = "nav-link" + (" active" if href == active_href else "") + (" flagged-nav" if is_flag else "")
        badge_span = f'<span class="nav-count">{esc(cnt)}</span>' if cnt else ""
        nav_parts.append(f'<a class="{cls}" href="{href}">{esc(label)}{badge_span}</a>')
    nav_html = "\n".join(nav_parts)
    ref_links_html = " · ".join(
        f'<a href="{href}">{esc(lbl)}</a>'
        for href, lbl in PRESERVED_REFERENCE_PAGES
        if (ROOT / href).exists()
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} — U.S. National Bank Savings &amp; Max-FDIC Research</title>
  <link rel="stylesheet" href="site-assets/styles.css">
</head>
<body>
  <div class="telemetry-bar">
    <div class="telemetry-inner">
      <div class="telemetry-group">
        <span class="telemetry-pill"><span class="dot-live"></span> Primary-Source Verified Research</span>
        <span>Account Open Date Anchor: <strong style="color:#fff">2026-10-22 (UTC)</strong></span>
        <span>FDIC Savings Avg: <strong style="color:#fff">0.38%</strong> (2026-10-19)</span>
        <span>Fed EFFR: <strong style="color:#fff">3.88%</strong> · 3M T-Bill: <strong style="color:#fff">4.25%</strong> · 1Y T-Note: <strong style="color:#fff">4.52%</strong> (2026-10-21)</span>
      </div>
      <div class="telemetry-group">
        <span>Zero Third-Party Aggregators · Unconfirmed Values Left Blank (<code>—</code>)</span>
      </div>
    </div>
  </div>

  <header class="site-header">
    <div class="header-inner">
      <div class="brand-row">
        <a class="brand-title" href="index.html">
          <span class="brand-mark">FDIC $250K+</span>
          <span class="brand-text">
            <strong>U.S. National Bank Savings Intelligence &amp; Max-FDIC Optimizer</strong>
            <span>Line-by-Line Verified Against Official Bank Disclosures, FDIC BankFind, Federal Reserve &amp; U.S. Treasury</span>
          </span>
        </a>
        <div class="header-meta-badges">
          <span class="hdr-badge">25 Accounts · 20 National Charters</span>
          <span class="hdr-badge">Open Date: 2026-10-22</span>
          <span class="hdr-badge gold">Zero Hallucination Policy</span>
        </div>
      </div>
      <nav class="main-nav" aria-label="Primary category navigation">
        {nav_html}
      </nav>
    </div>
  </header>

  <main class="page-wrap">
    <section class="hero-card">
      <div class="hero-eyebrow">{esc(eyebrow)}</div>
      <h1>{esc(title)}</h1>
      <p>{subtitle}</p>
      {hero_stats_html}
    </section>

    {body_html}
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div><strong style="color:#fff">U.S. National Bank Savings &amp; Max-FDIC Research Suite (`sassnarep3-star/SAVINGS2`)</strong> — Account Opening Anchor Date: <code>2026-10-22</code> · All primary sources verified on <code>2026-10-22</code>.</div>
      <div class="footer-links">
        <strong style="color:#e2e8f0">Primary Suite Pages:</strong>
        {" · ".join(f'<a href="{h}">{esc(l)}</a>' for h, l, _, _ in NAV_ITEMS)}
      </div>
      <div class="footer-links">
        <strong style="color:#e2e8f0">Preserved Multi-Session Reference Pages:</strong>
        {ref_links_html}
      </div>
      <div style="margin-top:0.55rem;color:#64748b">
        Strict Primary-Source Verification Rule: Every numeric rate, fee, bonus, asset total, and charter limit links directly to an official bank domain or U.S. government agency (`fdic.gov`, `api.fdic.gov`, `federalreserve.gov`, `home.treasury.gov`). Any ZIP-gated or unhydrated CMS value is intentionally left blank (`—`) and documented on <a href="flagged-review.html">Flagged for Review</a>. Savings APYs are variable unless otherwise stated.
      </div>
    </div>
  </footer>
  <script src="site-assets/dashboard.js"></script>
</body>
</html>
"""


def build_svg_yield_comparison() -> str:
    bars = [
        ("Capital One 360 ($100k w/ BONUS1500)", 4.70, "#059669", "4.70% Eff. Yr-1 (No DD)"),
        ("3-Charter Active Stack ($250k Total)", 4.67, "#047857", "4.67% Eff. Yr-1 ($11,685)"),
        ("U.S. Treasury 1-Year Note (2026-10-21)", 4.52, "#475569", "4.52% Par Yield (Taxable)"),
        ("2-Charter Zero-DD Split ($250k Total)", 4.28, "#0d9488", "4.28% Eff. Yr-1 ($10,700)"),
        ("U.S. Treasury 3-Month Bill (2026-10-21)", 4.25, "#64748b", "4.25% Par Yield"),
        ("SoFi Savings ($250k w/ DD + Boost)", 4.01, "#2563eb", "4.01% Eff. Yr-1 ($10,021)"),
        ("CIT Platinum w/ BOOST50 ($250k, No DD)", 4.00, "#1d4ed8", "4.00% Eff. Yr-1 ($10,000)"),
        ("Effective Fed Funds Rate (2026-10-20)", 3.88, "#64748b", "3.88% EFFR Benchmark"),
        ("CIT Platinum Standard Base (≥$5k)", 3.75, "#3b82f6", "3.75% Base APY (2026-07-01)"),
        ("Barclays Tiered Top Tier ($250k–$1M)", 3.65, "#3b82f6", "3.65% Base APY (Joint/POD)"),
        ("Synchrony Bank HYSA ($0 Min, Oct Date)", 3.55, "#2563eb", "3.55% Base APY (2026-10-21)"),
        ("Marcus / U.S. Bank Smartly ($25k+ Rel.)", 3.50, "#3b82f6", "3.50% Base APY (2026-10-21)"),
        ("FDIC National Avg Savings (2026-10-19)", 0.38, "#f59e0b", "0.38% National Avg ($950)"),
        ("Legacy Megabank Std (Wells/Truist/BMO)", 0.01, "#dc2626", "0.01% Standard ($25/yr)"),
    ]
    row_h = 28
    height = 56 + len(bars) * row_h
    lines = [
        f'<svg viewBox="0 0 680 {height}" role="img" aria-label="Year-1 Effective Yield vs Federal Benchmarks">',
        '<rect x="0" y="0" width="680" height="' + str(height) + '" fill="#ffffff" rx="8"/>',
        '<text x="16" y="26" font-size="13.5" font-weight="800" fill="#0f172a">Year-1 Effective APY vs. Official Federal Benchmarks (Open Date: 2026-10-22)</text>',
    ]
    max_pct = 5.0
    bar_x = 248
    max_w = 270
    for i, (label, val, color, note) in enumerate(bars):
        y = 44 + i * row_h
        w = max(3.0, (val / max_pct) * max_w)
        lines.append(f'<text x="16" y="{y + 15}" font-size="11" font-weight="600" fill="#1e293b">{esc(label)}</text>')
        lines.append(f'<rect x="{bar_x}" y="{y + 3}" width="{max_w}" height="16" fill="#f1f5f9" rx="3"/>')
        lines.append(f'<rect x="{bar_x}" y="{y + 3}" width="{w:.1f}" height="16" fill="{color}" rx="3"/>')
        lines.append(f'<text x="{bar_x + max_w + 8}" y="{y + 15}" font-size="10.8" font-weight="700" fill="#0f172a">{esc(note)}</text>')
    lines.append("</svg>")
    return "\n".join(lines)


def build_svg_dollar_returns_250k() -> str:
    items = [
        ("3-Charter Active Stack (CapOne+Chase+SoFi)", 11684.64, "#047857", "$0 Uninsured · With DD"),
        ("2-Charter Zero-DD Split (CapOne+CIT BOOST50)", 10699.55, "#059669", "$0 Uninsured · No DD"),
        ("2-Charter Oct-Dated Split (CapOne+Synchrony)", 10025.00, "#0d9488", "$0 Uninsured · No DD"),
        ("SoFi Single Account ($3M Sweep, w/ DD)", 10021.36, "#2563eb", "$0 Uninsured · Sweep"),
        ("CIT Platinum Single w/ BOOST50 ($250k)", 9999.25, "#1d4ed8", "$10k Over Cap if Single"),
        ("Capital One 360 Single w/ BONUS1500", 9500.00, "#2563eb", "$9.5k Over Cap if Single"),
        ("Marcus Single w/ 1 Referral Boost", 9372.75, "#3b82f6", "Joint/POD Recommended"),
        ("Barclays Tiered Single ($250k @ 3.65%+$200)", 9325.00, "#3b82f6", "Requires Joint/POD Cap"),
        ("Synchrony HYSA Single (3.55% Base)", 8875.00, "#3b82f6", "$240k Safe Single Cap"),
        ("SoFi WITHOUT Direct Deposit (0.80% PDF)", 2000.00, "#d97706", "Caught $6,250 Bug on main!"),
        ("FDIC National Savings Avg (0.38%)", 950.00, "#f59e0b", "FDIC Benchmark"),
        ("Wells Way2Save / Truist One (0.01%)", 25.00, "#dc2626", "-$11,659 Opportunity Loss"),
    ]
    row_h = 31
    height = 56 + len(items) * row_h
    lines = [
        f'<svg viewBox="0 0 680 {height}" role="img" aria-label="Year-1 Dollar Return on $250,000 Deposit">',
        f'<rect x="0" y="0" width="680" height="{height}" fill="#ffffff" rx="8"/>',
        '<text x="16" y="26" font-size="13.5" font-weight="800" fill="#0f172a">Exact Year-1 Dollar Return on $250,000 Deposit (2026-10-22 → 2027-10-22)</text>',
    ]
    max_v = 12000.0
    bar_x = 258
    max_w = 240
    for i, (label, val, color, tag) in enumerate(items):
        y = 44 + i * row_h
        w = max(3.0, (val / max_v) * max_w)
        lines.append(f'<text x="16" y="{y + 16}" font-size="10.8" font-weight="600" fill="#1e293b">{esc(label)}</text>')
        lines.append(f'<rect x="{bar_x}" y="{y + 4}" width="{max_w}" height="17" fill="#f1f5f9" rx="3"/>')
        lines.append(f'<rect x="{bar_x}" y="{y + 4}" width="{w:.1f}" height="17" fill="{color}" rx="3"/>')
        lines.append(f'<text x="{bar_x + max_w + 8}" y="{y + 16}" font-size="10.6" font-weight="700" fill="#0f172a">${val:,.2f} · {esc(tag)}</text>')
    lines.append("</svg>")
    return "\n".join(lines)


def build_svg_5yr_trajectory() -> str:
    # 5-Year cumulative return on $250,000 across Years 0..5
    series = [
        ("CIT Platinum w/ BOOST50 (4.25% 6M -> 3.75%)", [0, 9999.25, 19749.69, 29865.30, 40360.25, 51248.76], "#047857"),
        ("Barclays Tiered ($250k Joint/POD @ 3.65%+$200)", [0, 9325.00, 18983.06, 28993.64, 39369.61, 50124.30], "#2563eb"),
        ("Synchrony HYSA (3.55% Unconditional)", [0, 8875.00, 18065.06, 27581.37, 37435.51, 47639.47], "#0ea5e9"),
        ("Capital One 360 w/ BONUS1500 ($1,500 + 3.20%)", [0, 9500.00, 17756.00, 26276.19, 35069.03, 44143.24], "#7c3aed"),
        ("FDIC National Savings Avg (0.38%)", [0, 950.00, 1903.61, 2860.84, 3821.71, 4786.24], "#f59e0b"),
        ("Legacy Branch 0.01% (Wells/Truist)", [0, 25.00, 50.00, 75.01, 100.01, 125.03], "#dc2626"),
    ]
    lines = [
        '<svg viewBox="0 0 820 340" role="img" aria-label="5-Year Cumulative Return Trajectory on $250,000">',
        '<rect x="0" y="0" width="820" height="340" fill="#ffffff" rx="8"/>',
        '<text x="20" y="26" font-size="13.5" font-weight="800" fill="#0f172a">5-Year Cumulative Dollar Earnings Trajectory on $250,000 (2026-10-22 → 2031-10-22)</text>',
    ]
    ox, oy, pw, ph = 72, 285, 450, 225
    for step in range(6):
        gy = oy - (step / 5.0) * ph
        gv = step * 11000
        lines.append(f'<line x1="{ox}" y1="{gy:.1f}" x2="{ox + pw}" y2="{gy:.1f}" stroke="#e2e8f0" stroke-width="1"/>')
        lines.append(f'<text x="{ox - 8}" y="{gy + 4:.1f}" text-anchor="end" font-size="10.5" fill="#64748b">${gv // 1000}k</text>')
    years_lbl = ["Open\n2026", "Yr 1\n2027", "Yr 2\n2028", "Yr 3\n2029", "Yr 4\n2030", "Yr 5\n2031"]
    for yr in range(6):
        gx = ox + (yr / 5.0) * pw
        lines.append(f'<text x="{gx:.1f}" y="{oy + 20}" text-anchor="middle" font-size="10.5" font-weight="600" fill="#475569">Yr {yr}</text>')

    for idx, (name, pts, color) in enumerate(series):
        coords = []
        for yr, val in enumerate(pts):
            px = ox + (yr / 5.0) * pw
            py = oy - (val / 55000.0) * ph
            coords.append(f"{px:.1f},{py:.1f}")
        lines.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.8" points="{" ".join(coords)}"/>')
        lx, ly = 540, 62 + idx * 38
        lines.append(f'<rect x="{lx}" y="{ly - 9}" width="12" height="12" rx="2" fill="{color}"/>')
        lines.append(f'<text x="{lx + 18}" y="{ly + 1}" font-size="10.8" font-weight="700" fill="#0f172a">{esc(name)}</text>')
        lines.append(f'<text x="{lx + 18}" y="{ly + 15}" font-size="10.2" fill="#475569">Yr 1: ${pts[1]:,.2f} → Yr 5: +${pts[5]:,.2f}</text>')
    lines.append("</svg>")
    return "\n".join(lines)


def render_calculator_section(accounts: list[dict], matrices_by_id: dict[str, dict]) -> str:
    # Pre-render static rows for default $250,000, 1 Year, With Direct Deposit, Single Account ($250k cap)
    sorted_accts = sorted(
        accounts,
        key=lambda a: (
            0 if a["apy_percent"] is not None else 1,
            -(matrices_by_id[a["id"]]["projections"]["250000"]["1y"]["total_return_usd"] or -1),
        ),
    )
    static_rows = []
    for a in sorted_accts:
        p = matrices_by_id[a["id"]]["projections"]["250000"]["1y"]
        cert_link = f'<a href="{esc(a["fdic_source_url"])}" target="_blank" rel="noopener">Cert #{a["fdic_cert"]}</a>'
        src_link = f'<a href="{esc(a["rate_source_url"])}" target="_blank" rel="noopener">Official Source ↗</a>'
        dt = esc(a["official_rate_as_of_date"]) if a["official_rate_as_of_date"] else '<span class="blank-cell">—</span>'
        if not p["verified"]:
            static_rows.append(
                f'<tr class="row-unverified">'
                f'<td><strong>{esc(a["brand_name"])}</strong><br><small>{esc(a["account_name"])} ({cert_link})</small></td>'
                f'<td class="num blank-cell">— <a href="flagged-review.html" class="badge badge-flagged">Flagged</a></td>'
                f'<td class="mono">{dt}</td>'
                f'<td class="num blank-cell">—</td><td class="num blank-cell">—</td>'
                f'<td class="num blank-cell">—</td><td class="num blank-cell">—</td><td class="num blank-cell">—</td>'
                f'<td><span class="badge badge-flagged">Unverified APY</span></td>'
                f'<td>{src_link}</td></tr>'
            )
        else:
            unins = p["ending_uninsured_overflow_usd"]
            ins_badge = (
                f'<span class="badge badge-danger">${unins:,.2f} Uninsured</span>'
                if unins > 0
                else f'<span class="badge badge-verified">100% Insured (≤${p["fdic_single_cap_usd"]:,.0f})</span>'
            )
            promo_str = f'<strong>+${p["promo_bonus_usd"]:,.2f}</strong>' if p["promo_bonus_usd"] > 0 else "$0.00"
            static_rows.append(
                f'<tr class="{"row-top" if p["effective_annualized_pct"] >= 3.5 else ""}">'
                f'<td><strong>{esc(a["brand_name"])}</strong><br><small>{esc(a["account_name"])} ({cert_link})</small></td>'
                f'<td class="num"><span class="{"apy-big" if p["applied_base_apy_percent"] >= 3.0 else "apy-low"}">{p["applied_base_apy_percent"]:.2f}%</span></td>'
                f'<td class="mono">{dt}</td>'
                f'<td class="num">${p["base_interest_usd"]:,.2f}</td>'
                f'<td class="num">{promo_str}</td>'
                f'<td class="num"><strong>${p["total_return_usd"]:,.2f}</strong></td>'
                f'<td class="num">${p["ending_balance_usd"]:,.2f}</td>'
                f'<td class="num"><strong>{p["effective_annualized_pct"]:.2f}%</strong></td>'
                f'<td>{ins_badge}</td>'
                f'<td>{src_link}</td></tr>'
            )

    presets = [
        (5000, "$5,000"),
        (10000, "$10,000"),
        (15000, "$15,000"),
        (25000, "$25,000"),
        (50000, "$50,000"),
        (100000, "$100,000"),
        (240000, "$240,000 (Safe Single Cap)"),
        (250000, "$250,000 (Max Single FDIC)"),
        (500000, "$500,000 (Max Joint)"),
        (1000000, "$1,000,000"),
    ]
    preset_btns = "\n".join(
        f'<button type="button" class="preset-btn{" active" if val == 250000 else ""}" data-deposit-preset="{val}">{esc(lbl)}</button>'
        for val, lbl in presets
    )
    embedded_json = json.dumps(accounts)
    return f"""
    <section class="section-card" id="interactive-calculator">
      <div class="section-header">
        <div>
          <h2>Interactive Return &amp; Maximum-FDIC Insurance Calculator (Open Date: <code>2026-10-22</code>)</h2>
          <p>Select any deposit amount, investment horizon, direct-deposit eligibility, and FDIC ownership structure. All 25 national accounts recompute live while keeping unverified bank rates strictly blank (<code>—</code>).</p>
        </div>
        <a class="badge badge-info" href="returns-by-deposit.html">Full $1k–$1M Matrix →</a>
      </div>

      <div class="preset-row">
        <strong style="font-size:0.78rem;color:#334155;margin-right:0.35rem;">Quick Deposit Presets:</strong>
        {preset_btns}
      </div>

      <div class="calc-controls">
        <div class="ctrl-group">
          <label for="calc-deposit">Investment Deposit Amount (USD)</label>
          <input type="number" id="calc-deposit" value="250000" min="100" max="5000000" step="1000">
        </div>
        <div class="ctrl-group">
          <label for="calc-horizon">Investment Lifespan (From 2026-10-22)</label>
          <select id="calc-horizon">
            <option value="0.25">3 Months / 90 Days (→ 2027-01-22)</option>
            <option value="0.5">6 Months (→ 2027-04-22)</option>
            <option value="1" selected>1 Year (→ 2027-10-22)</option>
            <option value="2">2 Years (→ 2028-10-22)</option>
            <option value="3">3 Years (→ 2029-10-22)</option>
            <option value="5">5 Years (→ 2031-10-22)</option>
          </select>
        </div>
        <div class="ctrl-group">
          <label for="calc-dd">Payroll Direct Deposit Available?</label>
          <select id="calc-dd">
            <option value="yes" selected>Yes — Include Direct Deposit Offers (SoFi 4.40%+$400)</option>
            <option value="no">No — Pure Cash / Zero Direct Deposit Required</option>
          </select>
        </div>
        <div class="ctrl-group">
          <label for="calc-ownership">FDIC Ownership Category (Per Charter)</label>
          <select id="calc-ownership">
            <option value="1" selected>Single Account ($250,000 / charter)</option>
            <option value="2">Joint Account — 2 Co-Owners ($500,000 / charter)</option>
            <option value="3">Revocable POD Trust — 3 Beneficiaries ($750,000 / charter)</option>
            <option value="5">Revocable POD Trust — 5+ Beneficiaries ($1,250,000 / charter)</option>
          </select>
        </div>
      </div>

      <div class="callout ok" id="calc-live-summary">
        <strong>Default Anchor Projection (`2026-10-22` → `2027-10-22`, `$250,000` Single Account):</strong>
        Single-account With-DD leader is <strong>SoFi Bank Checking &amp; Savings</strong> at <strong>$10,021.36</strong> (`4.01%` eff. APY, 100% insured via `$3M` sweep);
        Zero-DD single-account leader is <strong>CIT Bank Platinum Savings (`BOOST50`)</strong> at <strong>$9,999.25</strong> (`4.00%` eff. APY; note `$9,999.25` single-owner interest overflow unless held jointly or split across 2 charters -> <strong>$10,699.55 / 4.28% APY</strong>!).
      </div>

      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>National Institution &amp; Account</th>
              <th class="num">Applied Base APY</th>
              <th>Official Rate Date</th>
              <th class="num">Compounded Base Interest</th>
              <th class="num">Verified Promo / Boost</th>
              <th class="num">Total Net Return</th>
              <th class="num">Ending Balance</th>
              <th class="num">Effective APY</th>
              <th>FDIC Coverage Status</th>
              <th>Primary Source</th>
            </tr>
          </thead>
          <tbody id="calc-results-tbody">
            {"".join(static_rows)}
          </tbody>
        </table>
      </div>
      <script type="application/json" id="savings-embedded-accounts">{embedded_json}</script>
    </section>
    """


def render_master_accounts_table(accounts: list[dict], matrices_by_id: dict[str, dict]) -> str:
    rows = []
    for a in accounts:
        tags = ["all"]
        if a["apy_percent"] is not None:
            tags.append("verified")
        else:
            tags.append("unverified")
        if "Big Four" in a["category"]:
            tags.append("bigfour")
        if a["us_branches"] > 0:
            tags.append("branch")
        else:
            tags.append("direct")
        if a["has_active_promo"]:
            tags.append("promo")

        apy_cell = (
            f'<span class="{"apy-big" if a["apy_percent"] >= 3.0 else "apy-low"}">{a["apy_percent"]:.2f}%</span>'
            if a["apy_percent"] is not None
            else '<span class="blank-cell">—</span><br><a class="badge badge-flagged" href="flagged-review.html">Flagged</a>'
        )
        r250 = matrices_by_id[a["id"]]["projections"]["250000"]["1y"]
        ret250_cell = (
            f'<strong>${r250["total_return_usd"]:,.2f}</strong><br><small>{r250["effective_annualized_pct"]:.2f}% eff.</small>'
            if r250["verified"]
            else '<span class="blank-cell">—</span>'
        )
        fee_cell = f'${a["monthly_fee_usd"]}' if a["monthly_fee_usd"] is not None else '<span class="blank-cell">—</span>'
        dt_cell = f'<code>{esc(a["official_rate_as_of_date"])}</code>' if a["official_rate_as_of_date"] else '<span class="blank-cell">—</span>'
        rank_str = f'Fed #{a["fed_rank"]}' if a["fed_rank"] else "FDIC Charter"
        flags_html = " ".join(
            f'<a class="badge badge-flagged" href="flagged-review.html#{esc(fid)}">{esc(fid)}</a>'
            for fid in a["flagged_ids"]
        )
        rows.append(
            f'<tr class="{"row-unverified" if a["apy_percent"] is None else ("row-top" if a["apy_percent"] >= 3.5 else "")}" data-tags="{" ".join(tags)}">'
            f'<td><strong>{esc(a["brand_name"])}</strong><br><small>{esc(a["institution_name"])}</small><br>'
            f'<span class="badge badge-info">{rank_str} · {fmt_assets(a["consolidated_assets_mil_usd"])}</span></td>'
            f'<td><strong>{esc(a["account_name"])}</strong><br><small style="color:#475569">{esc(a["rate_condition_summary"])}</small></td>'
            f'<td class="num">{apy_cell}</td>'
            f'<td>{dt_cell}<br><small style="color:#64748b">Checked {esc(a["verified_date"])}</small></td>'
            f'<td class="num">{fmt_usd(a["min_opening_deposit_usd"], 0)}</td>'
            f'<td class="num">{fee_cell}</td>'
            f'<td class="num">{ret250_cell}</td>'
            f'<td><small>{esc(a["bonus_summary"])}</small></td>'
            f'<td><code>#{a["fdic_cert"]}</code><br><small>${(a["fdic_sweep_max_usd"] or a["fdic_insured_max_single_usd"]) // 1000:,}k cap</small>{("<br>" + flags_html) if flags_html else ""}</td>'
            f'<td class="src-links">'
            f'<a href="{esc(a["rate_source_url"])}" target="_blank" rel="noopener">Rate Sheet ↗</a>'
            f'<a href="{esc(a["disclosure_source_url"])}" target="_blank" rel="noopener">Disclosures ↗</a>'
            f'<a href="{esc(a["fdic_source_url"])}" target="_blank" rel="noopener">FDIC #{a["fdic_cert"]} ↗</a>'
            f"</td></tr>"
        )

    return f"""
    <div class="filter-bar">
      <div class="filter-pills">
        <button type="button" class="preset-btn active" data-bank-filter="all">All 25 Accounts</button>
        <button type="button" class="preset-btn" data-bank-filter="verified">Verified APY (18)</button>
        <button type="button" class="preset-btn" data-bank-filter="direct">Direct High-Yield</button>
        <button type="button" class="preset-btn" data-bank-filter="bigfour">Big Four Megabanks</button>
        <button type="button" class="preset-btn" data-bank-filter="branch">Branch Network Banks</button>
        <button type="button" class="preset-btn" data-bank-filter="promo">Active Bonus / Boost (9)</button>
        <button type="button" class="preset-btn" data-bank-filter="unverified">Blank / ZIP-Gated (7)</button>
      </div>
      <input type="search" id="bank-search" class="search-input" placeholder="Search bank, Cert #, promo code, rule...">
    </div>
    <div class="table-scroll">
      <table class="data-table" id="master-banks-table">
        <thead>
          <tr>
            <th>Institution &amp; Scale</th>
            <th>Savings Product &amp; Rate Terms</th>
            <th class="num">Verified Base APY</th>
            <th>Official As-Of Date</th>
            <th class="num">Min Open</th>
            <th class="num">Monthly Fee</th>
            <th class="num">Yr-1 Return ($250k)</th>
            <th>Account Opening Bonus / Boost</th>
            <th>FDIC Cert &amp; Flags</th>
            <th>Official Links</th>
          </tr>
        </thead>
        <tbody>
          {"".join(rows)}
        </tbody>
      </table>
    </div>
    """


def render_portfolios_html(portfolios: list[dict]) -> str:
    cards = []
    for p in portfolios:
        s = p["summary"]
        legs_rows = "".join(
            f'<tr>'
            f'<td><strong>{esc(l["bank"])}</strong> (<code>#{l["fdic_cert"]}</code>)</td>'
            f'<td class="num">${l["allocation_usd"]:,.0f}</td>'
            f'<td class="num">${l["year1_interest_usd"]:,.2f}</td>'
            f'<td class="num">+${l["year1_bonus_usd"]:,.2f}</td>'
            f'<td class="num"><strong>${l["year1_total_return_usd"]:,.2f}</strong></td>'
            f'<td class="num">${l["year1_ending_balance_usd"]:,.2f}</td>'
            f'<td><a href="{esc(l["source_url"])}" target="_blank" rel="noopener">Source ↗</a></td>'
            f"</tr>"
            for l in p["legs"]
        )
        cards.append(
            f"""
            <div class="portfolio-card">
              <span class="badge badge-verified">0% Uninsured Overflow · {esc(p["ownership_assumption"])}</span>
              <h3>{esc(p["strategy_name"])}</h3>
              <div class="portfolio-metrics">
                <div><strong>${s["year1_total_return_usd"]:,.2f}</strong><span>Year-1 Net Return (`2026-10-22` → `2027-10-22`)</span></div>
                <div><strong>{s["year1_effective_apy_pct"]:.2f}%</strong><span>Effective Year-1 APY</span></div>
                <div><strong>${s["aggregate_fdic_capacity_usd"]:,.0f}</strong><span>Aggregate FDIC Insurance (`$0` Uninsured)</span></div>
              </div>
              <div class="table-scroll">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th>Charter Allocation Leg</th>
                      <th class="num">Principal</th>
                      <th class="num">Yr-1 Interest</th>
                      <th class="num">Bonus/Boost</th>
                      <th class="num">Total Return</th>
                      <th class="num">Yr-1 Ending</th>
                      <th>Link</th>
                    </tr>
                  </thead>
                  <tbody>{legs_rows}</tbody>
                </table>
              </div>
              <p style="margin:0.6rem 0 0;font-size:0.79rem;color:#047857;font-weight:700;">
                Outperforms FDIC National Average (`0.38%`) by +${s["vs_fdic_national_savings_avg_gain_usd"]:,.2f} in Year 1 with 100% federal deposit insurance on principal + interest.
              </p>
            </div>
            """
        )
    return f'<div class="portfolio-grid">{"".join(cards)}</div>'


def inject_banner_into_preserved_pages() -> None:
    banner = (
        '<div style="background:#071322;color:#e2e8f0;padding:10px 18px;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;'
        'font-size:13px;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;justify-content:space-between;border-bottom:2px solid #10b981;">'
        '<span><strong style="color:#6ee7b7">SAVINGS2 Unified Multi-Session Suite:</strong> Preserved reference page synced with primary-source fixes (`2026-10-22`).</span>'
        '<span>'
        '<a href="index.html" style="color:#93c5fd;margin-right:12px;font-weight:700">Executive Dashboard Hub →</a>'
        '<a href="national-banks.html" style="color:#cbd5e1;margin-right:12px">25 National Banks</a>'
        '<a href="returns-by-deposit.html" style="color:#cbd5e1;margin-right:12px">Max-FDIC Portfolios</a>'
        '<a href="promotions-bonuses.html" style="color:#cbd5e1;margin-right:12px">9 Promos</a>'
        '<a href="flagged-review.html" style="color:#fde68a;font-weight:700">24 Flagged &amp; Repo Audit Catches</a>'
        "</span></div>"
    )
    marker = "SAVINGS2 Unified Multi-Session Suite:"
    for href, _ in PRESERVED_REFERENCE_PAGES:
        p = ROOT / href
        if p.exists():
            txt = p.read_text()
            if marker not in txt and "<body" in txt:
                idx = txt.find(">", txt.find("<body"))
                if idx != -1:
                    p.write_text(txt[: idx + 1] + "\n" + banner + txt[idx + 1 :])


def main() -> None:
    fdic_bench = json.loads((DATASETS / "fdic-and-benchmarks.json").read_text())
    banks_data = json.loads((DATASETS / "national-banks.json").read_text())
    promos_data = json.loads((DATASETS / "promotions.json").read_text())
    returns_data = json.loads((DATASETS / "returns-matrix.json").read_text())
    flags_data = json.loads((DATASETS / "flagged-items.json").read_text())

    accounts = banks_data["accounts"]
    promos = promos_data["promotions"]
    portfolios = returns_data["optimal_fdic_portfolios"]
    flags = flags_data["items"]
    matrices_by_id = {m["account_id"]: m for m in returns_data["accounts"]}

    master_table_html = render_master_accounts_table(accounts, matrices_by_id)
    calc_html = render_calculator_section(accounts, matrices_by_id)
    portfolios_html = render_portfolios_html(portfolios)

    # 1. Build `index.html` (Executive Hub)
    hero_stats = """
      <div class="hero-meta-grid">
        <div class="hero-stat">
          <div class="lbl">Best Zero-DD $250k Split</div>
          <div class="val num">$10,699.55 <span style="font-size:0.86rem;color:#6ee7b7">(4.28% APY)</span></div>
          <div class="sub">$100k CapOne (`BONUS1500`) + $150k CIT (`BOOST50`) · 100% Insured</div>
        </div>
        <div class="hero-stat">
          <div class="lbl">Best Active-DD $250k Stack</div>
          <div class="val num">$11,684.64 <span style="font-size:0.86rem;color:#6ee7b7">(4.67% APY)</span></div>
          <div class="sub">Chase ($900) + CapOne ($1,500) + SoFi (4.40%+$400) · Beats 1Y Treasury!</div>
        </div>
        <div class="hero-stat">
          <div class="lbl">Top Ongoing Base APYs</div>
          <div class="val num">3.75% / 3.65% / 3.55%</div>
          <div class="sub">CIT Platinum (Jul 1) · Barclays $250k+ · Synchrony $0-Min (Oct 21)</div>
        </div>
        <div class="hero-stat">
          <div class="lbl">Line-by-Line Audit Protection</div>
          <div class="val num">+$6,250/yr Saved</div>
          <div class="sub">Caught false `SoFi 3.30% no-DD` bug (`0.80%` PDF Table 5) + NYC Citi Rule</div>
        </div>
      </div>
    """

    kpis_html = """
    <section class="kpi-grid">
      <div class="kpi-card highlight-emerald">
        <div>
          <div class="kpi-label">Winner #1 · Zero Direct Deposit ($250k Portfolio)</div>
          <div class="kpi-val">$10,699.55 / yr (4.28%)</div>
          <div class="kpi-title">$100k Capital One `BONUS1500` + $150k CIT `BOOST50`</div>
          <p class="kpi-desc">Beats both 1M (`4.09%`) and 3M (`4.25%`) U.S. Treasury bills with zero payroll direct deposit required and $500,000 aggregate single-owner FDIC insurance (`$0.00` uninsured overflow).</p>
        </div>
        <div class="kpi-foot"><span>Open Date: `2026-10-22`</span><a href="returns-by-deposit.html">See Exact Split →</a></div>
      </div>

      <div class="kpi-card highlight-emerald">
        <div>
          <div class="kpi-label">Winner #2 · With Direct Deposit ($250k Stack)</div>
          <div class="kpi-val">$11,684.64 / yr (4.67%)</div>
          <div class="kpi-title">Chase `$900` Combo + CapOne `$1,500` + SoFi `4.40%`+`$400`</div>
          <p class="kpi-desc">Outperforms the 1-Year U.S. Treasury Note (`4.52%`) and earns <strong>+$10,734.64 more</strong> in Year 1 than the FDIC National Average (`0.38%`), backed by $3.50M aggregate FDIC coverage.</p>
        </div>
        <div class="kpi-foot"><span>3 Independent Charters</span><a href="promotions-bonuses.html">View All 9 Promos →</a></div>
      </div>

      <div class="kpi-card highlight-blue">
        <div>
          <div class="kpi-label">Winner #3 · Pure Unconditional Base APY ($0 Min)</div>
          <div class="kpi-val">3.55% APY ($8,875 / yr)</div>
          <div class="kpi-title">Synchrony Bank HYSA (Oct 21, 2026) · CIT 3.75% ($5k+, Jul 1)</div>
          <p class="kpi-desc">Synchrony (`CERT #27314`, `$115.2B` assets) leads fresh October-2026 unconditional `$0`-minimum accounts at `3.55%`, while CIT Platinum (`CERT #11063`, `$236.3B` assets) leads `$5k+` accounts at `3.75%` (`4.25%` w/ `BOOST50`).</p>
        </div>
        <div class="kpi-foot"><span>9.3x–9.9x FDIC Avg</span><a href="national-banks.html">Compare All 25 →</a></div>
      </div>

      <div class="kpi-card highlight-amber">
        <div>
          <div class="kpi-label">Critical FDIC &amp; Regional Audit Warnings</div>
          <div class="kpi-val">$240,000 Safe Ceiling</div>
          <div class="kpi-title">Single-Charter Cap Overflow + NYC Citibank Exclusion</div>
          <p class="kpi-desc">Depositing a full `$250,000` in one single-owner account leaves `$8,875–$10,000` of Year-1 interest uninsured! Also: NY residents are ineligible for Citi Accelerate Savings, and Capital One + Discover share `CERT #4297`.</p>
        </div>
        <div class="kpi-foot"><span>24 Documented Flags</span><a href="flagged-review.html">Inspect Audit Log →</a></div>
      </div>
    </section>
    """

    hub_cards_html = """
    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Explore Deep-Dive Research Modules</h2>
          <p>Every category is structured into its own self-contained analytical page with full primary-source citations and dates.</p>
        </div>
      </div>
      <div class="hub-grid">
        <a class="hub-card" href="national-banks.html">
          <span class="badge badge-info">25 Accounts · Top 25 Banks</span>
          <h3>National Banks Master Directory →</h3>
          <p>Full institutional screening excluding small local banks: Fed asset rankings (`$43B–$4.09T`), branch counts, FDIC certificates, mobile apps, and security controls.</p>
        </a>
        <a class="hub-card" href="returns-by-deposit.html">
          <span class="badge badge-verified">$1,000 to $1,000,000</span>
          <h3>Returns by Deposit Size &amp; Max-FDIC Splits →</h3>
          <p>Exact returns anchored to `2026-10-22` across 10 deposit sizes and 6 horizons (`3M` to `5Y`), plus 5 multi-charter portfolios with `$0.00` uninsured overflow.</p>
        </a>
        <a class="hub-card" href="rate-competitiveness.html">
          <span class="badge badge-info">Macro Spreads &amp; Lifespan</span>
          <h3>Lifespan Rate Competitiveness (3M–5Y) →</h3>
          <p>Why cash bonuses dominate 90d–1Y while base rate leaders (`3.55%–3.75%`) win Years 3–5, benchmarked against EFFR (`3.88%`) and U.S. Treasuries (`4.09%–5.13%`).</p>
        </a>
        <a class="hub-card" href="promotions-bonuses.html">
          <span class="badge badge-verified">9 Active Offers Verified</span>
          <h3>Account Opening Bonuses &amp; Boosts →</h3>
          <p>Promo codes (`BOOST50`, `BONUS1500`), hold locks, direct-deposit rules, and Barclays' urgent 9-day `2026-10-31` bonus deadline.</p>
        </a>
        <a class="hub-card" href="opening-rules.html">
          <span class="badge badge-info">Fees, Waivers &amp; Limits</span>
          <h3>Minimum Deposits, Fees &amp; Opening Rules →</h3>
          <p>Side-by-side fee waivers, monthly transaction caps (`6/cycle` vs `10/cycle` vs unlimited), wire fees, and NY state eligibility exclusions.</p>
        </a>
        <a class="hub-card" href="fdic-security.html">
          <span class="badge badge-verified">$250k → $3.5M Coverage</span>
          <h3>FDIC Insurance Engineering &amp; Security →</h3>
          <p>Single (`$250k`), Joint (`$500k`), POD Trust (`$1.25M`), and SoFi Sweep (`$3M`) structures, plus shared-charter collision traps (`CapOne/Discover`, `CIT/First Citizens`).</p>
        </a>
        <a class="hub-card" href="flagged-review.html" style="border-left:4px solid #f59e0b;">
          <span class="badge badge-flagged">24 Audit Flags</span>
          <h3>Flagged for Review &amp; Repo Audit Log →</h3>
          <p>Every unverified/ZIP-gated blank cell (`—`), broken bank CMS token (`NaN APY`, `:BLUE_AccSavings_Rate%`), and factual bug caught during line-by-line repo review.</p>
        </a>
      </div>
    </section>
    """

    index_body = (
        kpis_html
        + f"""
        <div class="callout danger">
          <strong>Line-by-Line Repository Audit Highlight (`IRREG-AUDIT-01` — Saved `$6,250.00/yr` Error):</strong>
          During line-by-line primary-source verification of existing files on <code>main</code>, we caught a critical error where <code>SoFi Savings</code> was listed at <code>3.30% APY ("Standard savings APY, no direct deposit")</code>.
          Per <strong>Table 5</strong> of <a href="https://d32ijn7u0aqfv4.cloudfront.net/wp/wp-content/uploads/raw/SoFi-Bank-Rate-Sheet-October-20-2026.pdf" target="_blank" rel="noopener">SoFi Bank's Official Rate Sheet PDF (Effective October 20, 2026) ↗</a>, accounts <strong>without</strong> Eligible Direct Deposit or `$5,000`/31-day Qualifying Deposits earn only <strong><code>0.80% APY</code></strong> (`$2,000/yr` on `$250k`, NOT `$8,250/yr`). Both datasets and the interactive calculator below enforce this exact rule.
        </div>
        <div class="chart-grid">
          <div class="section-card svg-wrap" style="margin-bottom:0">{build_svg_yield_comparison()}</div>
          <div class="section-card svg-wrap" style="margin-bottom:0">{build_svg_dollar_returns_250k()}</div>
        </div>
        """
        + calc_html
        + hub_cards_html
        + f"""
        <section class="section-card">
          <div class="section-header">
            <div>
              <h2>Master Comparison Table — All 25 Audited National Bank Savings Accounts</h2>
              <p>Filter by bank type or verification status, or search by institution, promo code, or FDIC certificate number. Unconfirmed values are strictly left blank (<code>—</code>).</p>
            </div>
            <a class="badge badge-flagged" href="flagged-review.html">7 Unconfirmed APYs Documented →</a>
          </div>
          {master_table_html}
        </section>
        """
    )

    (ROOT / "index.html").write_text(
        page_shell(
            "index.html",
            "Executive U.S. National Bank Savings & Max-FDIC Dashboard",
            "Comprehensive primary-source investigation of 25 consumer savings products across 20 major U.S. national bank charters — engineered around maximum $250,000+ FDIC deposit insurance, verified digital apps, enterprise security, and exact compound returns anchored to opening date 2026-10-22.",
            "Executive Decision Hub · Open Date 2026-10-22",
            index_body,
            hero_stats,
        )
    )

    # 2. Build `national-banks.html` (deduplicated charter registry sorted by consolidated assets)
    seen_certs: set[int] = set()
    unique_charters = []
    for a in sorted(accounts, key=lambda x: -(x["consolidated_assets_mil_usd"] or 0)):
        if a["fdic_cert"] not in seen_certs:
            seen_certs.add(a["fdic_cert"])
            unique_charters.append(
                {
                    "legal_name": a["institution_name"],
                    "brand": a["brand_name"],
                    "fdic_cert": a["fdic_cert"],
                    "fed_rank": a["fed_rank"],
                    "assets": a["consolidated_assets_mil_usd"],
                    "branches": a["us_branches"],
                    "active": True,
                    "note": a["shared_charter_warning"] or "Independent active FDIC charter.",
                    "src": a["fdic_source_url"],
                }
            )
    unique_charters.append(
        {
            "legal_name": "Discover Bank (Merged into Capital One, N.A.)",
            "brand": "Discover Online Savings (Legacy)",
            "fdic_cert": 5649,
            "fed_rank": None,
            "assets": None,
            "branches": 0,
            "active": False,
            "note": "INACTIVE IN FDIC BANKFIND (`ACTIVE: 0`) — Merged into Capital One, N.A. (`CERT #4297`, `2025-05-18`). Do NOT treat as separate $250k capacity!",
            "src": "https://banks.data.fdic.gov/bankfind-suite/bankfind/details/5649",
        }
    )
    charter_rows = "".join(
        f'<tr>'
        f'<td><strong>{esc(c["legal_name"])}</strong><br><small>{esc(c["brand"])}</small></td>'
        f'<td class="mono">#{c["fdic_cert"]}</td>'
        f'<td>{("#" + str(c["fed_rank"])) if c["fed_rank"] else "Thrift / DE Bank"}</td>'
        f'<td class="num">{fmt_assets(c["assets"])}</td>'
        f'<td class="num">{c["branches"]:,}</td>'
        f'<td><span class="badge {"badge-verified" if c["active"] else "badge-danger"}">{"ACTIVE" if c["active"] else "INACTIVE / MERGED"}</span></td>'
        f'<td><small>{esc(c["note"])}</small></td>'
        f'<td><a href="{esc(c["src"])}" target="_blank" rel="noopener">FDIC Lookup ↗</a></td>'
        f"</tr>"
        for c in unique_charters
    )
    nat_body = f"""
    <div class="callout">
      <strong>Institutional Size Screening Rule (Why Zero Small Local Banks Appear Here):</strong>
      Every institution audited is either a top-25 U.S. commercial bank ranked on the <a href="https://www.federalreserve.gov/releases/lbr/current/" target="_blank" rel="noopener">Federal Reserve Large Commercial Banks Release (2026-06-30) ↗</a> or a nationally operating direct FDIC-insured bank with <strong>$43.5B to $4.09T in consolidated assets</strong> verified directly via <a href="https://banks.data.fdic.gov/bankfind-suite/bankfind" target="_blank" rel="noopener">FDIC BankFind (`2026-10-16` index) ↗</a>, a full-featured iOS/Android mobile app, and multi-factor security.
    </div>
    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>All 25 National Bank Savings Accounts — Full Comparison &amp; Source Links</h2>
          <p>Every row links directly to the bank's official rate page, Truth-in-Savings / fee disclosure, and federal charter record.</p>
        </div>
      </div>
      {master_table_html}
    </section>
    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Federal Reserve Asset Rankings &amp; Active FDIC Charter Registry</h2>
          <p>Verified against Federal Reserve Statistical Release H.8 / LBR (`2026-06-30`) and `api.fdic.gov/banks/institutions` (`2026-10-16`).</p>
        </div>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Legal Bank Charter Name</th>
              <th>FDIC Cert</th>
              <th>Fed Rank</th>
              <th class="num">Consolidated Assets</th>
              <th class="num">U.S. Branches</th>
              <th>Charter Status</th>
              <th>Shared-Brand / Merger Coverage Note</th>
              <th>Federal Source</th>
            </tr>
          </thead>
          <tbody>{charter_rows}</tbody>
        </table>
      </div>
    </section>
    """
    (ROOT / "national-banks.html").write_text(
        page_shell(
            "national-banks.html",
            "National Banks Master Directory (25 Accounts Across Major U.S. Charters)",
            "Institutional roster screening exclusively large national commercial and direct banks ($43.5B–$4.09T assets) with verified mobile apps, multi-factor authentication, and active FDIC certificates.",
            "Category 1 · Institutional Screening & Master Directory",
            nat_body,
        )
    )

    # 3. Build `returns-by-deposit.html`
    tier_cols = [10000, 25000, 50000, 100000, 240000, 250000, 500000]
    matrix_1y_rows = []
    for a in accounts:
        proj = matrices_by_id[a["id"]]["projections"]
        cells = []
        for dep in tier_cols:
            c = proj[str(dep)]["1y"]
            if not c["verified"]:
                cells.append('<td class="num blank-cell">—</td>')
            else:
                overflow_flag = ' <span title="Exceeds single-owner $250k FDIC cap" style="color:#b91c1c">*</span>' if c["ending_uninsured_overflow_usd"] > 0 else ""
                cells.append(f'<td class="num"><strong>${c["total_return_usd"]:,.2f}</strong>{overflow_flag}<br><small>{c["effective_annualized_pct"]:.2f}%</small></td>')
        matrix_1y_rows.append(
            f'<tr class="{"row-unverified" if a["apy_percent"] is None else ""}">'
            f'<td><strong>{esc(a["brand_name"])}</strong> — {esc(a["account_name"])}<br><small>Cert #{a["fdic_cert"]} · As of {esc(a["official_rate_as_of_date"] or "—")}</small></td>'
            f'{"".join(cells)}'
            f'<td><a href="{esc(a["rate_source_url"])}" target="_blank" rel="noopener">Source ↗</a></td>'
            f"</tr>"
        )

    horizon_250k_rows = []
    for a in accounts:
        proj = matrices_by_id[a["id"]]["projections"]["250000"]
        hcells = []
        for hkey in ["3m", "6m", "1y", "2y", "3y", "5y"]:
            c = proj[hkey]
            if not c["verified"]:
                hcells.append('<td class="num blank-cell">—</td>')
            else:
                hcells.append(f'<td class="num"><strong>${c["total_return_usd"]:,.2f}</strong><br><small>{c["effective_annualized_pct"]:.2f}%</small></td>')
        horizon_250k_rows.append(
            f'<tr class="{"row-unverified" if a["apy_percent"] is None else ""}">'
            f'<td><strong>{esc(a["brand_name"])}</strong> — {esc(a["account_name"])}</td>'
            f'{"".join(hcells)}'
            f'<td><a href="{esc(a["rate_source_url"])}" target="_blank" rel="noopener">Source ↗</a></td>'
            f"</tr>"
        )

    ret_body = (
        f"""
        <div class="callout warn">
          <strong>Why `$240,000` (or a Multi-Charter Split) Beats Depositing `$250,000` in One Single-Owner Account:</strong>
          FDIC insurance (`$250,000` per depositor, per charter, per ownership category) covers <strong>principal PLUS accrued interest combined</strong> (<a href="https://www.fdic.gov/resources/deposit-insurance/understanding-deposit-insurance" target="_blank" rel="noopener">FDIC Official Rule ↗</a>).
          Opening a single-owner account with `$250,000.00` on `2026-10-22` pushes your Year-1 ending balance to `$258,875–$259,999.25` — leaving <strong>$8,875 to $9,999.25 uninsured</strong> unless you either (1) split across 2+ charters below, (2) cap single-charter principal at `$240,000`, (3) open a Joint Account (`$500,000` limit), or (4) use SoFi's `$3M` sweep network. Cells marked <code>*</code> below exceed the single-owner `$250k` cap.
        </div>
        <section class="section-card">
          <div class="section-header">
            <div>
              <h2>Optimal Multi-Charter Maximum-FDIC Portfolios (`$250k`, `$500k` &amp; `$1,000,000`)</h2>
              <p>Engineered using strictly independent FDIC bank charters so principal + all Year-1 compounded interest + bonuses have <strong>$0.00 uninsured overflow</strong>.</p>
            </div>
          </div>
          {portfolios_html}
        </section>
        """
        + calc_html
        + f"""
        <section class="section-card">
          <div class="section-header">
            <div>
              <h2>Year-1 Net Return Matrix Across Deposit Sizes (`2026-10-22` → `2027-10-22`)</h2>
              <p>Includes base compounded interest plus verified cash bonuses and promotional APY boosts where deposit &amp; hold thresholds are satisfied. <code>*</code> indicates ending balance exceeds single-owner $250k cap unless titled Joint/POD.</p>
            </div>
          </div>
          <div class="table-scroll">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Institution &amp; Account</th>
                  <th class="num">$10,000</th>
                  <th class="num">$25,000</th>
                  <th class="num">$50,000</th>
                  <th class="num">$100,000</th>
                  <th class="num">$240k (Safe Single)</th>
                  <th class="num">$250k (FDIC Cap)</th>
                  <th class="num">$500k (Joint Cap)</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>{"".join(matrix_1y_rows)}</tbody>
            </table>
          </div>
        </section>

        <section class="section-card">
          <div class="section-header">
            <div>
              <h2>Lifespan Cumulative Return Matrix at $250,000 (`2026-10-22` Through `2031-10-22`)</h2>
              <p>Assumes current verified ongoing APYs remain unchanged after any initial 3- or 6-month promotional boost expires. Savings APYs are variable.</p>
            </div>
          </div>
          <div class="table-scroll">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Institution &amp; Account</th>
                  <th class="num">3 Mos (`2027-01-22`)</th>
                  <th class="num">6 Mos (`2027-04-22`)</th>
                  <th class="num">1 Yr (`2027-10-22`)</th>
                  <th class="num">2 Yrs (`2028-10-22`)</th>
                  <th class="num">3 Yrs (`2029-10-22`)</th>
                  <th class="num">5 Yrs (`2031-10-22`)</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>{"".join(horizon_250k_rows)}</tbody>
            </table>
          </div>
        </section>
        """
    )
    (ROOT / "returns-by-deposit.html").write_text(
        page_shell(
            "returns-by-deposit.html",
            "Return by Investment Deposit Size & Maximum-FDIC Portfolio Allocations",
            "Exact dollar and effective annualized returns from $1,000 to $1,000,000 anchored to account opening date 2026-10-22, paired with zero-overflow multi-bank FDIC insurance splits.",
            "Category 2 · Deposit Return Matrix & Max-FDIC Optimization",
            ret_body,
        )
    )

    # 4. Build `rate-competitiveness.html`
    bench_rows = [
        ("FDIC National Average — Savings", "0.38% APY", "2026-10-19", "+317 to +337 bps below top HYSAs", "https://www.fdic.gov/national-rates-and-rate-caps"),
        ("FDIC National Average — Money Market", "0.63% APY", "2026-10-19", "+292 to +312 bps below top HYSAs", "https://www.fdic.gov/national-rates-and-rate-caps"),
        ("FDIC National Average — 12-Month CD", "1.76% APY", "2026-10-19", "Top liquid HYSAs beat avg 1Y CD by +179–199 bps", "https://www.fdic.gov/national-rates-and-rate-caps"),
        ("FDIC National Rate Cap — Savings", "4.63% APY", "2026-10-19", "Regulatory cap for less-than-well-capitalized banks", "https://www.fdic.gov/national-rates-and-rate-caps"),
        ("Federal Reserve Effective Fed Funds Rate (EFFR)", "3.88%", "2026-10-20", "Top base HYSAs track within -13 to -33 bps of EFFR", "https://www.federalreserve.gov/releases/h15/"),
        ("Federal Reserve Bank Prime Loan Rate", "7.00%", "2026-10-21", "Macro lending benchmark", "https://www.federalreserve.gov/releases/h15/"),
        ("U.S. Treasury 1-Month Par Yield", "4.09%", "2026-10-21", "Beaten by SoFi 4.40% boost, CIT BOOST50 4.25%, & CapOne 4.70% eff.", "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=202610"),
        ("U.S. Treasury 3-Month Par Yield", "4.25%", "2026-10-21", "Matched by CIT BOOST50 (4.25%); beaten by 2-Charter Split (4.28%)", "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=202610"),
        ("U.S. Treasury 1-Year Par Yield", "4.52%", "2026-10-21", "Beaten by CapOne $100k BONUS1500 (4.70%) & 3-Charter Stack (4.67%)", "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=202610"),
        ("U.S. Treasury 2Y / 3Y / 5Y / 10Y Par Yields", "4.81% / 4.89% / 4.95% / 5.13%", "2026-10-21", "Upward-sloping curve rewards fixed duration over 3–5Y", "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=202610"),
    ]
    bench_tr = "".join(
        f'<tr><td><strong>{esc(n)}</strong></td><td class="num"><strong>{esc(v)}</strong></td><td class="mono">{esc(d)}</td><td>{esc(note)}</td><td><a href="{esc(u)}" target="_blank" rel="noopener">Official .gov ↗</a></td></tr>'
        for n, v, d, note, u in bench_rows
    )

    comp_rows = []
    for a in accounts:
        if a["apy_percent"] is None:
            continue
        mult = a["apy_percent"] / 0.38
        vs_effr = (a["apy_percent"] - 3.88) * 100
        vs_1y = (a["apy_percent"] - 4.52) * 100
        p250 = matrices_by_id[a["id"]]["projections"]["250000"]
        comp_rows.append(
            f'<tr>'
            f'<td><strong>{esc(a["brand_name"])}</strong> — {esc(a["account_name"])}</td>'
            f'<td class="num"><strong>{a["apy_percent"]:.2f}%</strong></td>'
            f'<td class="num">{mult:.1f}×</td>'
            f'<td class="num">{vs_effr:+.0f} bps</td>'
            f'<td class="num">{vs_1y:+.0f} bps</td>'
            f'<td class="num">{p250["6m"]["effective_annualized_pct"]:.2f}%</td>'
            f'<td class="num"><strong>{p250["1y"]["effective_annualized_pct"]:.2f}%</strong></td>'
            f'<td class="num">{p250["3y"]["effective_annualized_pct"]:.2f}%</td>'
            f'<td class="num">{p250["5y"]["effective_annualized_pct"]:.2f}%</td>'
            f'<td><a href="{esc(a["rate_source_url"])}" target="_blank" rel="noopener">Source ↗</a></td>'
            f"</tr>"
        )

    comp_body = f"""
    <div class="callout">
      <strong>Key Lifespan Finding (`2026-10-22` Curve Regime):</strong>
      Because all savings APYs are variable while the October 2026 U.S. Treasury par curve slopes upward (`4.09%` 1M → `4.52%` 1Y → `4.95%` 5Y),
      <strong>promotional cash bonuses and 6-month rate boosts dominate the 3-month to 1-year horizon</strong> (`Capital One BONUS1500` achieves `4.70%` at `$50k`/`$100k`; our 3-Charter Stack hits `4.67%` on `$250k`),
      whereas <strong>pure ongoing APY leaders (`CIT 3.75%`, `Barclays 3.65%`, `Synchrony 3.55%`, `Marcus 3.50%`) win hands-down across Years 2–5</strong> as one-time cash bonuses amortize!
    </div>

    <div class="section-card svg-wrap">{build_svg_5yr_trajectory()}</div>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Official Federal Macro Rate Benchmarks (`fdic.gov`, `federalreserve.gov`, `home.treasury.gov`)</h2>
          <p>Every benchmark below was retrieved directly from U.S. government primary tables on `2026-10-22`.</p>
        </div>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Federal Benchmark Series</th>
              <th class="num">Official Rate / Yield</th>
              <th>Official As-Of Date</th>
              <th>Savings Competitiveness Takeaway</th>
              <th>Primary Source</th>
            </tr>
          </thead>
          <tbody>{bench_tr}</tbody>
        </table>
      </div>
    </section>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Effective Annualized Yield Decay Across Lifespan (`6M`, `1Y`, `3Y`, `5Y` on `$250,000`)</h2>
          <p>Shows exact basis-point spread versus Effective Fed Funds (`3.88%`) and 1Y Treasury (`4.52%`) plus effective CAGR across holding horizons.</p>
        </div>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Account</th>
              <th class="num">Base APY</th>
              <th class="num">× FDIC Avg</th>
              <th class="num">Spread vs EFFR</th>
              <th class="num">Spread vs 1Y T-Note</th>
              <th class="num">6-Mo Eff. APY</th>
              <th class="num">1-Yr Eff. APY</th>
              <th class="num">3-Yr Eff. CAGR</th>
              <th class="num">5-Yr Eff. CAGR</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>{"".join(comp_rows)}</tbody>
        </table>
      </div>
    </section>
    """
    (ROOT / "rate-competitiveness.html").write_text(
        page_shell(
            "rate-competitiveness.html",
            "Rate Competitiveness & Lifespan Yield Decay Analysis (3 Months to 5 Years)",
            "Benchmarking all verified national bank savings yields against the FDIC National Average (0.38%), Federal Reserve EFFR (3.88%), and U.S. Treasury Par Curve (4.09%–5.13%) over the full investment lifespan.",
            "Category 3 · Macro Spreads & Investment Lifespan Analysis",
            comp_body,
        )
    )

    # 5. Build `promotions-bonuses.html`
    promo_rows = []
    for pr in promos:
        tiers_txt = "<br>".join(
            f'• <strong>${t["min_deposit_usd"]:,.0f}+</strong> → '
            + (f'<strong>${t["bonus_usd"]:,.0f} cash</strong>' if t.get("bonus_usd") else "")
            + (f' ({t["effective_1yr_apy_at_min_pct"]:.2f}% Yr-1 eff. APY)' if t.get("effective_1yr_apy_at_min_pct") else "")
            + (f' {esc(t["note"])}' if t.get("note") else "")
            for t in pr["bonus_tiers"]
        )
        dd_badge = (
            '<span class="badge badge-flagged">Yes — Direct Deposit Req.</span>'
            if pr["direct_deposit_required"]
            else '<span class="badge badge-verified">No — Pure Cash Eligible</span>'
        )
        exp_str = f'<code>{esc(pr["expiration_date"])}</code>' if pr["expiration_date"] else '<span class="blank-cell">—</span> (Open-ended)'
        promo_rows.append(
            f'<tr>'
            f'<td><strong>{esc(pr["bank_name"])}</strong><br><small>{esc(pr["account_name"])}</small></td>'
            f'<td><code>{esc(pr["promo_code"])}</code></td>'
            f'<td><strong>{esc(pr["offer_headline"])}</strong><br><small>{tiers_txt}</small></td>'
            f'<td>{dd_badge}</td>'
            f'<td class="num">{pr["funding_window_days"]}d fund / {pr["hold_period_days"]}d hold</td>'
            f'<td>{exp_str}<br><small style="color:#64748b">{esc(pr["expiration_note"])}</small></td>'
            f'<td><a href="{esc(pr["official_source_url"])}" target="_blank" rel="noopener">Official Offer ↗</a></td>'
            f"</tr>"
        )
    promo_body = f"""
    <div class="callout warn">
      <strong>Urgent Calendar Alert Relative to Account Open Date `2026-10-22`:</strong>
      <strong>Barclays Tiered Savings `$200` Cash Bonus</strong> expires <strong>`2026-10-31` (9 days remaining!)</strong>;
      <strong>CIT Bank Platinum Savings `BOOST50` (`4.25%` 6-month boost, no DD)</strong> runs through <strong>`2026-12-15`</strong>;
      <strong>Chase `$200` Savings / `$900` Combo Coupon</strong> runs through <strong>`2027-01-27`</strong>; and
      <strong>SoFi `4.40%` Boost + `$400` DD Bonus</strong> runs through <strong>`2027-12-31`</strong>.
    </div>
    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>All 9 Primary-Source Verified Account Opening Bonuses &amp; Rate Boosts</h2>
          <p>Every promo code, funding deadline, hold requirement, direct-deposit condition, and expiration date confirmed directly from official bank offer pages on `2026-10-22`.</p>
        </div>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Bank &amp; Eligible Product</th>
              <th>Promo Code</th>
              <th>Verified Bonus Tiers &amp; Effective Yield</th>
              <th>Direct Deposit?</th>
              <th class="num">Funding &amp; Hold Window</th>
              <th>Official Expiration Date</th>
              <th>Primary Link</th>
            </tr>
          </thead>
          <tbody>{"".join(promo_rows)}</tbody>
        </table>
      </div>
    </section>
    """
    (ROOT / "promotions-bonuses.html").write_text(
        page_shell(
            "promotions-bonuses.html",
            "Verified Account Opening Bonuses & Promotional Rate Boosts (9 Offers)",
            "Line-by-line audit of cash bonuses ($60 to $1,500) and introductory rate boosts (+0.50% to +1.10% APY) across major national banks as of 2026-10-22.",
            "Category 4 · Verified Promotions & Bonus Arbitrage",
            promo_body,
        )
    )

    # 6. Build `opening-rules.html`
    rules_rows = "".join(
        f'<tr class="{"row-unverified" if a["monthly_fee_usd"] is None else ""}">'
        f'<td><strong>{esc(a["brand_name"])}</strong><br><small>{esc(a["account_name"])}</small></td>'
        f'<td class="num">{fmt_usd(a["min_opening_deposit_usd"], 2 if a["min_opening_deposit_usd"] == 0.01 else 0)}</td>'
        f'<td class="num">{fmt_usd(a["min_balance_for_apy_usd"], 0)}</td>'
        f'<td class="num">{("$" + str(a["monthly_fee_usd"])) if a["monthly_fee_usd"] is not None else "<span class=blank-cell>—</span>"}</td>'
        f'<td><small>{esc(a["fee_waiver_rules"])}</small></td>'
        f'<td><small>{esc(a["withdrawal_rules"])}</small></td>'
        f'<td><small>{esc(a["opening_rules"])}</small></td>'
        f'<td><a href="{esc(a["disclosure_source_url"])}" target="_blank" rel="noopener">Fee/Rule Source ↗</a></td>'
        f"</tr>"
        for a in accounts
    )
    rules_body = f"""
    <div class="callout danger">
      <strong>Critical Geographic &amp; Fee Traps Verified from Official Disclosures:</strong>
      (1) <strong>Citibank NY Exclusion:</strong> Official `citi.com/banking/compare-bank-accounts` disclosures explicitly exclude residential addresses in <strong>New York (NY)</strong>, CA, NJ, CT, FL, IL, MD, DC, NV, and select VA markets from opening <strong>Citi® Accelerate Savings</strong>.
      (2) <strong>Bank of America Fee PDF (`Effective Aug 7, 2026`):</strong> Confirms `$100` minimum opening deposit and `$8/mo` fee (waived 6 mos for new accounts, then `$0` at `$500` daily balance).
      (3) <strong>Withdrawal Caps:</strong> Ally enforces `10/cycle` (closes account on repeated excess); Wells Fargo, Truist (`$5` excess fee), and PNC enforce `6/cycle`; Marcus, Synchrony, Capital One, Amex, and CIT allow unlimited ACH transfers.
    </div>
    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Complete Minimum Deposit, Monthly Fee Waiver, Withdrawal &amp; Opening Rules Matrix</h2>
          <p>All 25 national bank accounts compared side-by-side from official Truth-in-Savings and Personal Schedule of Fees documents.</p>
        </div>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Institution &amp; Account</th>
              <th class="num">Min to Open</th>
              <th class="num">Min for APY</th>
              <th class="num">Monthly Fee</th>
              <th>Exact Fee Waiver Conditions</th>
              <th>Withdrawal Limits, ATMs &amp; Wires</th>
              <th>Eligibility &amp; Account Opening Rules</th>
              <th>Official Disclosure</th>
            </tr>
          </thead>
          <tbody>{rules_rows}</tbody>
        </table>
      </div>
    </section>
    """
    (ROOT / "opening-rules.html").write_text(
        page_shell(
            "opening-rules.html",
            "Minimum Deposits, Fee Waivers, Withdrawal Caps & Account Opening Rules",
            "Operational due diligence across all 25 national bank savings products: minimum opening balances, exact fee waiver paths, Reg D style cycle limits, wire costs, and regional eligibility rules.",
            "Category 5 · Operational Rules, Minimums & Fee Waivers",
            rules_body,
        )
    )

    # 7. Build `fdic-security.html`
    cat_rows = "".join(
        f'<tr><td><strong>{esc(c["category"])}</strong></td><td class="num"><strong>${c["coverage_limit_per_charter_usd"]:,.0f}</strong></td><td>{esc(c["coverage_formula"])}</td><td><a href="{esc(c["source_url"])}" target="_blank" rel="noopener">FDIC Rule ↗</a></td></tr>'
        for c in fdic_bench["fdic_coverage_rules"]["ownership_categories"]
    )
    trap_rows = "".join(
        f'<tr><td><code>{esc(t["trap_id"])}</code></td><td><strong>{esc(" + ".join(t["brands_sharing_charter"]))}</strong></td><td><code>#{t["active_fdic_cert"]}</code></td><td>{esc(t["merger_aggregation_rule"])}</td><td><a href="{esc(t["primary_sources"][0])}" target="_blank" rel="noopener">Verify ↗</a></td></tr>'
        for t in fdic_bench["same_charter_merger_traps"]
    )
    sec_rows = "".join(
        f'<tr><td><strong>{esc(a["brand_name"])}</strong> — {esc(a["account_name"])}</td><td><code>#{a["fdic_cert"]}</code></td><td>{esc(a["digital_app_name"])}</td><td><small>{esc(a["security_features"])}</small></td><td><small>{esc(a["shared_charter_warning"] or "Independent charter — standard $250k/owner rule applies.")}</small></td><td><a href="{esc(a["rate_source_url"])}" target="_blank" rel="noopener">Source ↗</a></td></tr>'
        for a in accounts
    )
    fdic_body = f"""
    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Official FDIC Deposit Insurance Ownership Categories (`12 CFR Part 330`)</h2>
          <p>How to legally structure `$250,000` to `$5,000,000+` across ownership categories and independent bank charters without exposing a single dollar of principal or accrued interest.</p>
        </div>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>FDIC Ownership Category</th>
              <th class="num">Statutory Coverage Limit (Per Charter)</th>
              <th>Official Coverage Rule &amp; Trust Consolidation Effective 2024-04-01</th>
              <th>Official `.gov` Link</th>
            </tr>
          </thead>
          <tbody>{cat_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Critical Shared-Charter &amp; Post-Merger Coverage Traps</h2>
          <p>Never split >$250,000 across two brands that share a single FDIC Certificate number — combined balances above $250,000 are uninsured!</p>
        </div>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Trap ID</th>
              <th>Brands Sharing Coverage</th>
              <th>Shared Cert #</th>
              <th>Coverage Collision Explanation</th>
              <th>Official Proof</th>
            </tr>
          </thead>
          <tbody>{trap_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>Digital Banking App &amp; Security Controls Audit — All 25 Accounts</h2>
          <p>Confirming mobile banking app availability, passkeys/biometrics/MFA, fraud monitoring, and charter-specific warnings.</p>
        </div>
      </div>
      <div class="table-scroll">
        <table class="data-table">
          <thead>
            <tr>
              <th>Institution &amp; Product</th>
              <th>FDIC Cert</th>
              <th>Verified Mobile App</th>
              <th>Security &amp; Authentication Features</th>
              <th>Charter-Specific Coverage Warning</th>
              <th>Official Page</th>
            </tr>
          </thead>
          <tbody>{sec_rows}</tbody>
        </table>
      </div>
    </section>
    """
    (ROOT / "fdic-security.html").write_text(
        page_shell(
            "fdic-security.html",
            "Maximum FDIC Insurance Engineering, Charter Traps & Digital Security Audit",
            "Complete statutory guide to $250,000 Single, $500,000 Joint, $1,250,000 Revocable POD Trust, and $3,000,000 Sweep coverage — plus shared-charter traps and mobile app security across all 20 national charters.",
            "Category 6 · Deposit Insurance Law & Cybersecurity Due Diligence",
            fdic_body,
        )
    )

    # 8. Build `flagged-review.html`
    flag_cards = "".join(
        f"""
        <div class="flag-card{" critical" if ("CRITICAL" in f["severity"] or "HIGH" in f["severity"]) else ""}" id="{esc(f["flag_id"])}">
          <div class="flag-head">
            <div>
              <span class="badge {"badge-danger" if ("CRITICAL" in f["severity"] or "HIGH" in f["severity"]) else "badge-flagged"}">{esc(f["flag_id"])} · {esc(f["severity"])}</span>
              <strong style="margin-left:0.45rem;font-size:0.96rem">{esc(f["institution"])}</strong>
            </div>
            <span class="mono" style="color:#475569">Checked: {esc(f["date_checked"])} · Status: <strong>{esc(f["status"])}</strong></span>
          </div>
          <div style="font-size:0.84rem;margin:0.35rem 0"><strong>Affected Field:</strong> {esc(f["field_affected"])}</div>
          <div style="font-size:0.84rem;color:#334155;margin:0.35rem 0"><strong>Primary-Source Observation:</strong> {esc(f["observation"])}</div>
          <div style="font-size:0.83rem;color:#0f172a;margin-top:0.35rem">
            <strong>Resolution / Action Taken:</strong> {esc(f["action_taken"])} ·
            <a href="{esc(f["source_url"])}" target="_blank" rel="noopener">Inspect Primary Official URL ↗</a>
          </div>
        </div>
        """
        for f in flags
    )
    flag_body = f"""
    <div class="callout warn">
      <strong>Strict Zero-Hallucination &amp; Transparency Mandate:</strong>
      Whenever an official bank page gated its APY behind a client-side ZIP modal (`Chase`, `Bank of America`, `Citibank`, `PNC`, `TD Bank`, `Fifth Third`), rendered a broken server token (`Capital One hero NaN APY`, `Citibank :BLUE_AccSavings_Rate%`, `Citizens Access #ProductLine=cax...#`), omitted an effective date (`Wells Fargo`, `HSBC`), or contained an error on <code>main</code> (`SoFi 0.80% vs 3.30% non-DD bug`), we <strong>never guessed or used third-party aggregator numbers</strong>. Every single item is documented below with a direct primary link for manual verification. Per project protocol, flagged items are transparently published here and do not block PR creation or merge.
    </div>
    <section class="section-card">
      <div class="section-header">
        <div>
          <h2>All {len(flags)} Flagged Unverified Values, Bank Website Bugs &amp; Repo Audit Findings</h2>
          <p>Click any primary source link below to inspect the exact official bank page or PDF disclosure verified on `2026-10-22`.</p>
        </div>
      </div>
      {flag_cards}
    </section>
    """
    (ROOT / "flagged-review.html").write_text(
        page_shell(
            "flagged-review.html",
            "Flagged for Review — Unverified Values, Bank CMS Anomalies & Line-by-Line Repo Audit",
            "Complete transparency log of all 24 unconfirmed/ZIP-gated blank fields, broken bank CMS tokens, charter ceiling traps, and critical factual bugs caught and fixed during line-by-line repository verification.",
            "Category 7 · Strict Audit Log & Manual Review Queue",
            flag_body,
        )
    )

    # Inject cross-suite top banner into preserved `session-46ab1baa` reference subpages
    inject_banner_into_preserved_pages()
    (ROOT / ".nojekyll").write_text("")

    # Update comprehensive README.md preserving full overview of both suites & exact findings
    readme = """# U.S. National Bank Savings Intelligence & Max-FDIC Optimizer (`SAVINGS2`)

**Live GitHub Pages Dashboard:** <https://sassnarep3-star.github.io/SAVINGS2/>  
**Account Opening Date Anchor:** `2026-10-22` (UTC) · **Primary Verification Date:** `2026-10-22` (UTC)

---

## Executive Summary (`2026-10-22` Open Date Anchor)

This repository investigates and verifies the best U.S. **large national commercial and national direct bank** consumer savings accounts — screening strictly for **major national scale (`$43.5B` to `$4.09T` consolidated assets, zero small local banks)**, **mobile banking apps**, **multi-factor authentication & security**, and **maximum `$250,000+` FDIC insurance engineering**.

| Strategy / Benchmark (`$250,000` Principal Opened `2026-10-22`) | Year-1 Net Return (`2027-10-22`) | Effective Year-1 APY | Uninsured Overflow | Primary Official Sources |
| --- | ---: | ---: | ---: | --- |
| **Optimal 3-Charter Active Stack (With Direct Deposit)** — `$15k` Chase (`$900` Combo) + `$100k` Capital One (`BONUS1500`) + `$135k` SoFi (`4.40%` 6M Boost + `$400` DD, `$3M` Sweep) | **$11,684.64** | **4.67%** *(Beats 1Y Treasury `4.52%`!)* | **$0.00** (`$3.50M` cap) | [Chase](https://www.chase.com/personal/offers/checking-and-savings) · [CapOne](https://www.capitalone.com/bank/bonus1500/) · [SoFi PDF](https://d32ijn7u0aqfv4.cloudfront.net/wp/wp-content/uploads/raw/SoFi-Bank-Rate-Sheet-October-20-2026.pdf) |
| **Optimal 2-Charter Zero-DD Split (No Direct Deposit)** — `$100k` Capital One (`BONUS1500`) + `$150k` CIT Platinum (`BOOST50` `4.25%` 6M -> `3.75%`) | **$10,699.55** | **4.28%** *(Beats 3M T-Bill `4.25%`!)* | **$0.00** (`$500k` cap) | [CapOne](https://www.capitalone.com/bank/bonus1500/) · [CIT Boost](https://www.cit.com/cit-bank/platinum-savings/boost) |
| **Optimal 2-Charter Oct-Dated Split (No Direct Deposit)** — `$100k` Capital One (`BONUS1500`) + `$150k` Synchrony HYSA (`3.55%` Oct 21 rate) | **$10,025.00** | **4.01%** | **$0.00** (`$500k` cap) | [CapOne](https://www.capitalone.com/bank/disclosures/savings-accounts/online-performance-savings-account/) · [Synchrony](https://www.synchrony.com/banking/products/hys-core) |
| **Best Single-Account With DD (`$3M` Sweep)** — SoFi Checking & Savings (`4.40%` 6M -> `3.30%` + `$400` DD) | **$10,021.36** | **4.01%** | **$0.00** (`$3.00M` sweep) | [SoFi Rate Sheet PDF](https://d32ijn7u0aqfv4.cloudfront.net/wp/wp-content/uploads/raw/SoFi-Bank-Rate-Sheet-October-20-2026.pdf) |
| **Best Pure Unconditional `$0`-Min Base Rate** — Synchrony Bank HYSA (`3.55%` as of `2026-10-21`; use `$240k` single cap or Joint/POD) | **$8,875.00** | **3.55%** | `$8,875`* if Single | [Synchrony](https://www.synchrony.com/banking/products/hys-core) |
| **FDIC National Average Savings Benchmark (`2026-10-19`)** | **$950.00** | **0.38%** | **$0.00** | [FDIC National Rates](https://www.fdic.gov/national-rates-and-rate-caps) |
| **Standard Megabank Branch Tier** — Wells Fargo Way2Save / Truist One (`0.01%`) | **$25.00** | **0.01%** | **$0.00** | [Wells Fargo](https://www.wellsfargo.com/savings-cds/way2save/) · [Truist](https://www.truist.com/savings/truist-one-savings/disclosures-and-fees) |

---

## Live Multi-Page Site Architecture

- **[`index.html`](https://sassnarep3-star.github.io/SAVINGS2/)** — Executive Dashboard, SVG Yield/Return Visualizations, Live Custom Return & FDIC Coverage Calculator, and Searchable 25-Account Master Table
- **[`national-banks.html`](https://sassnarep3-star.github.io/SAVINGS2/national-banks.html)** — All 25 National Bank Products + Federal Reserve Consolidated Assets & FDIC Certificate Registry
- **[`returns-by-deposit.html`](https://sassnarep3-star.github.io/SAVINGS2/returns-by-deposit.html)** — `$1,000`–`$1,000,000` Deposit Matrix × 6 Horizons (`3M`–`5Y`) & 5 Multi-Charter Max-FDIC Portfolios
- **[`rate-competitiveness.html`](https://sassnarep3-star.github.io/SAVINGS2/rate-competitiveness.html)** — Macro Spread Table (`FDIC`, `Fed H.15 EFFR`, `U.S. Treasury Par Curve`) & 5-Year Yield Decay Curve
- **[`promotions-bonuses.html`](https://sassnarep3-star.github.io/SAVINGS2/promotions-bonuses.html)** — All 9 Primary-Verified Cash Bonuses & Promotional Rate Boosts (`BOOST50`, `BONUS1500`, `Chase $900`, `SoFi $400`, `Barclays $200` exp. `2026-10-31`)
- **[`opening-rules.html`](https://sassnarep3-star.github.io/SAVINGS2/opening-rules.html)** — Minimum Opening Deposits, Exact Monthly Fee Waivers, Withdrawal Caps & Regional Eligibility Rules (incl. NYC Citibank Exclusion)
- **[`fdic-security.html`](https://sassnarep3-star.github.io/SAVINGS2/fdic-security.html)** — Statutory FDIC Coverage Categories, Shared-Charter Merger Traps (`CapOne/Discover`, `CIT/First Citizens`, `Citizens Access`), and App Security Audit
- **[`flagged-review.html`](https://sassnarep3-star.github.io/SAVINGS2/flagged-review.html)** — All 24 Flagged Unverified Values (`—`), Bank CMS Bugs, and Line-by-Line Repo Audit Catches (including `IRREG-AUDIT-01` fixing the `$6,250/yr` non-DD SoFi APY bug)
- **Preserved Multi-Session Reference Pages:** `accounts.html`, `returns.html`, `competitiveness.html`, `bonuses.html`, `fdic.html`, `flagged.html`, `methodology.html`

---

## Reproducible Build & Automated Audit Pipeline

```bash
python3 scripts/generate_datasets.py   # Regenerate primary-verified JSON datasets & ledger
python3 scripts/sync_legacy_banks.py   # Sync primary fixes into data/banks.json
python3 build.py                       # Build preserved v1 reference pages
python3 scripts/build_site.py          # Build Executive Dashboard + 7 deep-dive subpages
python3 check_links.py                 # Run preserved link auditor
python3 scripts/verify_all.py          # Run full data, math, blank-cell & local HTTP audit
```
"""
    (ROOT / "README.md").write_text(readme)
    print("Built all 8 Executive Suite pages + synced 7 preserved reference pages + updated README.md cleanly.")


if __name__ == "__main__":
    main()
