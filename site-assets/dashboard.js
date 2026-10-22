/* ==========================================================================
   Interactive Return, FDIC Coverage & Multi-Bank Optimizer Engine (SAVINGS2)
   Anchors strictly to Account Open Date: 2026-10-22 (UTC)
   Never fabricates values — unverified accounts always render explicit "—"
   ========================================================================== */

(function () {
  "use strict";

  const fmtUSD = (val) =>
    val === null || val === undefined || Number.isNaN(val)
      ? "—"
      : "$" + Number(val).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  const fmtPct = (val) =>
    val === null || val === undefined || Number.isNaN(val)
      ? "—"
      : Number(val).toFixed(2) + "%";

  function computeReturnForAccount(acct, principal, years, allowDirectDeposit, ownershipMultiplier) {
    if (acct.apy_percent === null || acct.apy_percent === undefined) {
      return { verified: false };
    }
    if (!allowDirectDeposit && acct.id === "sofi-checking-savings-dd") {
      // Without DD or $5k/31d qualifying deposits, SoFi drops to 0.80% per Oct 20, 2026 Rate Sheet PDF Table 5
      const endNoDD = principal * Math.pow(1 + 0.008, years);
      const baseInt = Math.round((endNoDD - principal) * 100) / 100;
      const cap = 3000000 * ownershipMultiplier;
      return {
        verified: true,
        appliedApy: 0.8,
        baseInterest: baseInt,
        promoBonus: 0,
        totalReturn: baseInt,
        endingBalance: Math.round((principal + baseInt) * 100) / 100,
        effApy: 0.8,
        fdicCap: cap,
        uninsured: Math.max(0, Math.round((principal + baseInt - cap) * 100) / 100),
        ddDowngraded: true,
      };
    }

    let baseApy = acct.apy_percent;
    if (acct.id === "cit-platinum-savings" && principal < 5000) {
      baseApy = 0.25;
    } else if (acct.id === "barclays-tiered-savings" && principal < 250000) {
      baseApy = 3.5;
    } else if (acct.id === "usbank-smartly-relationship" && principal < 25000) {
      baseApy = principal >= 5000 ? 2.0 : 1.0;
    } else if (acct.id === "wellsfargo-platinum-new" && principal < 25000) {
      baseApy = 0.01;
    }

    const baseEnding = principal * Math.pow(1 + baseApy / 100, years);
    const baseInterest = Math.round((baseEnding - principal) * 100) / 100;

    let promoExtra = 0;
    if (acct.id === "cit-platinum-savings") {
      const bYrs = Math.min(years, 0.5);
      const rYrs = Math.max(0, years - 0.5);
      const bRate = principal >= 5000 ? 0.0425 : 0.0075;
      const boosted = principal * Math.pow(1 + bRate, bYrs) * Math.pow(1 + baseApy / 100, rYrs);
      promoExtra = Math.round((boosted - baseEnding) * 100) / 100;
    } else if (acct.id === "capitalone-360-performance" && years >= 0.3) {
      if (principal >= 100000) promoExtra = 1500;
      else if (principal >= 50000) promoExtra = 750;
      else if (principal >= 20000) promoExtra = 300;
    } else if (acct.id === "barclays-tiered-savings" && principal >= 25000 && years >= 0.42) {
      promoExtra = 200;
    } else if (acct.id === "sofi-checking-savings-dd" && allowDirectDeposit) {
      const bYrs = Math.min(years, 0.5);
      const rYrs = Math.max(0, years - 0.5);
      const boosted = principal * Math.pow(1.044, bYrs) * Math.pow(1.033, rYrs);
      const cashBonus = years >= 0.25 ? 400 : 0;
      promoExtra = Math.round((boosted - baseEnding + cashBonus) * 100) / 100;
    } else if (acct.id === "marcus-online-savings") {
      const bYrs = Math.min(years, 0.25);
      const rYrs = Math.max(0, years - 0.25);
      const boosted = principal * Math.pow(1.045, bYrs) * Math.pow(1.035, rYrs);
      promoExtra = Math.round((boosted - baseEnding) * 100) / 100;
    } else if (acct.id === "bmo-savings-builder" && years >= 1.0) {
      promoExtra = 60;
    }

    const totalReturn = Math.round((baseInterest + promoExtra) * 100) / 100;
    const endingBalance = Math.round((principal + totalReturn) * 100) / 100;
    const effApy = Math.round((Math.pow(endingBalance / principal, 1 / years) - 1) * 10000) / 100;
    const rawCap = acct.fdic_sweep_max_usd || acct.fdic_insured_max_single_usd || 250000;
    const fdicCap = rawCap * ownershipMultiplier;
    const uninsured = Math.max(0, Math.round((endingBalance - fdicCap) * 100) / 100);

    return {
      verified: true,
      appliedApy: baseApy,
      baseInterest,
      promoBonus: promoExtra,
      totalReturn,
      endingBalance,
      effApy,
      fdicCap,
      uninsured,
      ddDowngraded: false,
    };
  }

  function initInteractiveCalculator() {
    const dataEl = document.getElementById("savings-embedded-accounts");
    const tbody = document.getElementById("calc-results-tbody");
    if (!dataEl || !tbody) return;

    const accounts = JSON.parse(dataEl.textContent);
    const depositInput = document.getElementById("calc-deposit");
    const horizonSelect = document.getElementById("calc-horizon");
    const ddSelect = document.getElementById("calc-dd");
    const ownerSelect = document.getElementById("calc-ownership");
    const summaryBox = document.getElementById("calc-live-summary");
    const presetBtns = document.querySelectorAll("[data-deposit-preset]");

    function render() {
      const principal = Math.max(100, Number(depositInput.value) || 250000);
      const years = Number(horizonSelect.value) || 1.0;
      const allowDD = ddSelect.value === "yes";
      const ownershipMult = Number(ownerSelect.value) || 1;

      const computed = accounts.map((acct) => ({
        acct,
        res: computeReturnForAccount(acct, principal, years, allowDD, ownershipMult),
      }));

      computed.sort((a, b) => {
        if (a.res.verified && !b.res.verified) return -1;
        if (!a.res.verified && b.res.verified) return 1;
        if (!a.res.verified && !b.res.verified) return 0;
        return b.res.totalReturn - a.res.totalReturn;
      });

      const bestInsured = computed.find((x) => x.res.verified && x.res.uninsured === 0);
      const bestAny = computed.find((x) => x.res.verified);
      const fdicAvgReturn = Math.round((principal * (Math.pow(1.0038, years) - 1)) * 100) / 100;

      if (summaryBox && bestAny) {
        const gainVsAvg = Math.round((bestAny.res.totalReturn - fdicAvgReturn) * 100) / 100;
        const overflowAlert =
          bestAny.res.uninsured > 0
            ? `<div style="margin-top:0.55rem;color:#991b1b;font-weight:700;">⚠️ Single-Charter FDIC Overflow Warning: At ${fmtUSD(principal)}, ending balance (${fmtUSD(bestAny.res.endingBalance)}) exceeds this account's ${fmtUSD(bestAny.res.fdicCap)} FDIC cap by ${fmtUSD(bestAny.res.uninsured)}! Split across 2+ independent charters (e.g., $100k Capital One Cert #4297 + remainder at CIT #11063 or Synchrony #27314) or add a joint owner / POD beneficiary for 100% FDIC protection.</div>`
            : `<div style="margin-top:0.45rem;color:#047857;font-weight:700;">✓ 100% Principal + Compounded Interest Insured (${fmtUSD(bestAny.res.endingBalance)} ending balance ≤ ${fmtUSD(bestAny.res.fdicCap)} FDIC limit).</div>`;

        summaryBox.innerHTML =
          `<strong>Live Projection from Account Open Date <code>2026-10-22</code> (${fmtUSD(principal)} over ${horizonSelect.options[horizonSelect.selectedIndex].text}):</strong> ` +
          `Top Single Account is <strong>${bestAny.acct.brand_name} — ${bestAny.acct.account_name}</strong> generating <strong>${fmtUSD(bestAny.res.totalReturn)}</strong> ` +
          `(${fmtPct(bestAny.res.effApy)} annualized; ending balance <strong>${fmtUSD(bestAny.res.endingBalance)}</strong>) — ` +
          `outperforming the FDIC National Savings Average (<code>0.38%</code> = ${fmtUSD(fdicAvgReturn)}) by <strong>+${fmtUSD(gainVsAvg)}</strong>.` +
          (bestInsured && bestInsured !== bestAny
            ? ` Best <em>Zero-Overflow Single Account</em> is <strong>${bestInsured.acct.brand_name}</strong> at <strong>${fmtUSD(bestInsured.res.totalReturn)}</strong>.`
            : "") +
          overflowAlert;
      }

      tbody.innerHTML = computed
        .map(({ acct, res }) => {
          const certLink = `<a href="${acct.fdic_source_url}" target="_blank" rel="noopener">Cert #${acct.fdic_cert}</a>`;
          const srcLink = `<a href="${acct.rate_source_url}" target="_blank" rel="noopener">Official Source ↗</a>`;
          const dateStr = acct.official_rate_as_of_date || '<span class="blank-cell">—</span>';
          if (!res.verified) {
            return `<tr class="row-unverified">
              <td><strong>${acct.brand_name}</strong><br><small>${acct.account_name} (${certLink})</small></td>
              <td class="num blank-cell">— <a href="flagged-review.html" class="badge badge-flagged">Flagged</a></td>
              <td class="mono">${dateStr}</td>
              <td class="num blank-cell">—</td>
              <td class="num blank-cell">—</td>
              <td class="num blank-cell">—</td>
              <td class="num blank-cell">—</td>
              <td class="num blank-cell">—</td>
              <td><span class="badge badge-flagged">Unverified APY</span></td>
              <td>${srcLink}</td>
            </tr>`;
          }
          const insBadge =
            res.uninsured > 0
              ? `<span class="badge badge-danger">${fmtUSD(res.uninsured)} Uninsured</span>`
              : `<span class="badge badge-verified">100% Insured (≤${fmtUSD(res.fdicCap)})</span>`;
          return `<tr class="${res.effApy >= 3.5 ? "row-top" : ""}">
            <td><strong>${acct.brand_name}</strong><br><small>${acct.account_name} (${certLink})${res.ddDowngraded ? ' · <em style="color:#b45309">0.80% non-DD tier</em>' : ""}</small></td>
            <td class="num"><span class="${res.appliedApy >= 3.0 ? "apy-big" : "apy-low"}">${fmtPct(res.appliedApy)}</span></td>
            <td class="mono">${dateStr}</td>
            <td class="num">${fmtUSD(res.baseInterest)}</td>
            <td class="num">${res.promoBonus > 0 ? "<strong>+" + fmtUSD(res.promoBonus) + "</strong>" : "$0.00"}</td>
            <td class="num"><strong>${fmtUSD(res.totalReturn)}</strong></td>
            <td class="num">${fmtUSD(res.endingBalance)}</td>
            <td class="num"><strong>${fmtPct(res.effApy)}</strong></td>
            <td>${insBadge}</td>
            <td>${srcLink}</td>
          </tr>`;
        })
        .join("");
    }

    presetBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        presetBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        depositInput.value = btn.getAttribute("data-deposit-preset");
        render();
      });
    });

    [depositInput, horizonSelect, ddSelect, ownerSelect].forEach((el) => {
      if (el) el.addEventListener("input", render);
      if (el) el.addEventListener("change", render);
    });

    render();
  }

  function initTableFilters() {
    const searchInput = document.getElementById("bank-search");
    const filterBtns = document.querySelectorAll("[data-bank-filter]");
    const rows = document.querySelectorAll("#master-banks-table tbody tr");
    if (!rows.length) return;

    let activeFilter = "all";

    function applyFilter() {
      const q = (searchInput ? searchInput.value : "").trim().toLowerCase();
      rows.forEach((tr) => {
        const tags = (tr.getAttribute("data-tags") || "").toLowerCase();
        const text = tr.textContent.toLowerCase();
        const matchTag = activeFilter === "all" || tags.indexOf(activeFilter) !== -1;
        const matchText = !q || text.indexOf(q) !== -1;
        tr.style.display = matchTag && matchText ? "" : "none";
      });
    }

    filterBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        filterBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        activeFilter = btn.getAttribute("data-bank-filter");
        applyFilter();
      });
    });

    if (searchInput) {
      searchInput.addEventListener("input", applyFilter);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    initInteractiveCalculator();
    initTableFilters();
  });
})();
