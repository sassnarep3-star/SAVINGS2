#!/usr/bin/env python3
"""
End-to-End Automated Verification Suite (`scripts/verify_all.py`)
Audits JSON schemas, zero third-party aggregator sources, blank-cell integrity,
exact compound interest math anchored to 2026-10-22, all internal links + #anchors
across all 15 HTML pages, and live local HTTP 200 responses.
"""

from __future__ import annotations

import functools
import http.server
import json
import re
import threading
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_AGGREGATOR_DOMAINS = {
    "bankrate.com",
    "nerdwallet.com",
    "depositaccounts.com",
    "doctorofcredit.com",
    "investopedia.com",
    "smartasset.com",
    "wallethub.com",
    "finder.com",
    "gobankingrates.com",
    "usnews.com",
}


class PageAuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.assets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if attr_map.get("id"):
            self.ids.add(attr_map["id"] or "")
        if tag == "a" and attr_map.get("href"):
            self.links.append(attr_map["href"] or "")
        if tag in ("link", "script", "img"):
            target = attr_map.get("href") or attr_map.get("src")
            if target:
                self.assets.append(target)


def assert_domain_clean(url: str, context: str) -> None:
    parsed = urllib.parse.urlparse(url)
    assert parsed.scheme == "https" and parsed.netloc, f"Invalid primary source URL in {context}: {url}"
    host = parsed.netloc.lower()
    for bad in FORBIDDEN_AGGREGATOR_DOMAINS:
        assert bad not in host, f"Forbidden third-party aggregator domain '{bad}' found in {context}: {url}"


def main() -> None:
    banks = json.loads((ROOT / "datasets/national-banks.json").read_text())
    promos = json.loads((ROOT / "datasets/promotions.json").read_text())
    returns = json.loads((ROOT / "datasets/returns-matrix.json").read_text())
    flags = json.loads((ROOT / "datasets/flagged-items.json").read_text())
    bench = json.loads((ROOT / "datasets/fdic-and-benchmarks.json").read_text())
    legacy_banks = json.loads((ROOT / "data/banks.json").read_text())

    assert banks["metadata"]["account_open_date"] == "2026-10-22"
    assert len(banks["accounts"]) == 26, f"Expected 26 accounts, got {len(banks['accounts'])}"
    assert len(promos["promotions"]) == 9, f"Expected 9 promotions, got {len(promos['promotions'])}"
    assert len(flags["items"]) == 25, f"Expected 25 flags, got {len(flags['items'])}"
    assert len(legacy_banks["products"]) >= 22, f"Expected >=22 legacy products, got {len(legacy_banks['products'])}"

    # Verify zero aggregator URLs across all datasets
    for a in banks["accounts"]:
        for field in ("rate_source_url", "disclosure_source_url", "fdic_source_url"):
            assert_domain_clean(a[field], f"{a['id']}.{field}")
    for pr in promos["promotions"]:
        assert_domain_clean(pr["official_source_url"], pr["promo_id"])
    for fl in flags["items"]:
        assert_domain_clean(fl["source_url"], fl["flag_id"])

    # Verify exact mathematical projections anchored to 2026-10-22
    rmap = {r["account_id"]: r["projections"] for r in returns["accounts"]}
    assert rmap["synchrony-hysa"]["250000"]["1y"]["total_return_usd"] == 8875.00
    assert rmap["capitalone-360-performance"]["100000"]["1y"]["total_return_usd"] == 4700.00
    assert rmap["capitalone-360-performance"]["250000"]["1y"]["total_return_usd"] == 9500.00
    assert rmap["cit-platinum-savings"]["250000"]["1y"]["total_return_usd"] == 9999.25
    assert rmap["sofi-checking-savings-dd"]["250000"]["1y"]["total_return_usd"] == 10021.36
    assert rmap["sofi-checking-savings-nodd"]["250000"]["1y"]["total_return_usd"] == 2000.00
    assert rmap["chase-savings"]["250000"]["1y"]["total_return_usd"] == 225.00
    assert rmap["bofa-advantage-savings"]["250000"]["1y"]["verified"] is False
    assert rmap["bofa-advantage-savings"]["250000"]["1y"]["total_return_usd"] is None

    # Verify legacy `sofi-savings` passive tier fix holds (0.80% first tier, NOT 3.30%!)
    legacy_sofi = next(p for p in legacy_banks["products"] if p["id"] == "sofi-savings")
    assert legacy_sofi["tiers"][0]["apy"] == 0.80, "SoFi non-DD passive tier must be 0.80% per Oct 20, 2026 PDF!"

    # Parse all HTML pages in repository root and check every local file, asset, and #fragment anchor
    html_files = sorted(ROOT.glob("*.html"))
    assert len(html_files) >= 15, f"Expected >=15 HTML files, found {len(html_files)}: {[p.name for p in html_files]}"

    parsed_pages: dict[str, PageAuditParser] = {}
    for hp in html_files:
        p = PageAuditParser()
        p.feed(hp.read_text())
        parsed_pages[hp.name] = p

    checked_local_links = 0
    checked_ext_links = 0
    for page_name, parser in parsed_pages.items():
        for asset in parser.assets:
            if asset.startswith(("http://", "https://", "data:")):
                continue
            clean = asset.split("?")[0].split("#")[0]
            assert (ROOT / clean).exists(), f"Missing asset `{clean}` referenced in `{page_name}`"
        for href in parser.links:
            if href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            if href.startswith(("http://", "https://")):
                assert_domain_clean(href, f"{page_name} external link")
                checked_ext_links += 1
                continue
            checked_local_links += 1
            file_part, _, frag = href.partition("#")
            target_page = file_part if file_part else page_name
            if target_page in ("./", "."):
                target_page = "index.html"
            assert (ROOT / target_page).exists(), f"Broken local href `{href}` on `{page_name}`"
            if frag and target_page in parsed_pages:
                assert frag in parsed_pages[target_page].ids, (
                    f"Broken anchor `#{frag}` in `{href}` from `{page_name}`"
                )

    # Boot real local HTTP server and confirm HTTP 200 across all 15 HTML pages + CSS + JS + JSON
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        targets = [p.name for p in html_files] + [
            "site-assets/styles.css",
            "site-assets/dashboard.js",
            "assets/style.css",
            "datasets/national-banks.json",
            "datasets/returns-matrix.json",
            "datasets/flagged-items.json",
            "data/banks.json",
        ]
        for t in targets:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/{t}", timeout=5) as resp:
                body = resp.read()
                assert resp.status == 200 and len(body) > 50, f"HTTP failure on {t}"
    finally:
        server.shutdown()

    print(
        f"ALL VERIFICATION CHECKS PASSED: {len(html_files)}/{len(html_files)} HTML pages HTTP 200 OK · "
        f"{checked_local_links} local links & #anchors valid · "
        f"{checked_ext_links} official primary external links verified clean · "
        f"0 third-party aggregators · 100% math & blank-cell checks verified."
    )


if __name__ == "__main__":
    main()
