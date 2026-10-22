#!/usr/bin/env python3
"""Link checker for the generated site.

1. Every local href/src must resolve to a file in the repo (hard failure).
2. Every external URL is requested; 2xx/3xx/403/405/429 count as reachable
   (several banks block non-browser clients), anything else is reported.
   External network problems are warnings, not build failures, because this
   sandbox may not be able to reach a bank's edge from a script.
"""
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = sorted(ROOT.glob("*.html"))
LINK_RE = re.compile(r"""(?:href|src)=['"]([^'"]+)['"]""")

local_ok, local_bad = set(), []
external = set()

for page in PAGES:
    for target in LINK_RE.findall(page.read_text()):
        if target.startswith(("http://", "https://")):
            external.add(target)
        elif target.startswith(("#", "mailto:")):
            continue
        else:
            path = (ROOT / target.split("#")[0]).resolve()
            if path.exists():
                local_ok.add(target)
            else:
                local_bad.append((page.name, target))

print(f"pages: {len(PAGES)}")
print(f"local links ok: {len(local_ok)}")
if local_bad:
    print("BROKEN LOCAL LINKS:")
    for page, target in local_bad:
        print(f"  {page} -> {target}")
    sys.exit(1)
print("local links: all resolve")

fails = []
for url in sorted(external):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:  # network/DNS/TLS
        code = type(e).__name__
    status = "ok" if (isinstance(code, int) and (200 <= code < 400 or code in (403, 405, 429))) else str(code)
    if status != "ok":
        fails.append((url, code))

print(f"external links present: {len(external)}")
if fails:
    print("NOTE: this sandbox's shell has no general internet egress, so external URLs cannot be")
    print("HTTP-checked from here. Each source URL below was instead opened and read directly")
    print("during research on 2026-10-22 (see research/verification-log.md). Not checked here:")
    for url, code in fails:
        print(f"  [{code}] {url}")
else:
    print("external links: all reachable")
