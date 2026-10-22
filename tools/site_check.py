#!/usr/bin/env python3
"""Site integrity checks for the SAVINGS2 docs/ site.

1. Every internal href/src target exists (file present, anchor present).
2. Every HTML file parses cleanly (tag balance via html.parser).
3. External links are http(s) and point only at allow-listed official domains
   (bank domains + fdic.gov + federalreserve.gov) — no CDNs, no trackers.
4. Reports any page not reachable via nav from index.html.
"""

import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

ALLOWED_EXTERNAL = {
    "www.chase.com", "account.chase.com", "personal.chase.com", "secure.chase.com",
    "www.bankofamerica.com", "media.bac-assets.com", "newsroom.bankofamerica.com",
    "www.wellsfargo.com", "www.citi.com", "banking.citi.com", "online.citi.com",
    "www.usbank.com", "www.pnc.com", "www.truist.com",
    "www.capitalone.com", "apply.capitalone.com", "ecm.capitalone.com",
    "www.marcus.com", "www.ally.com", "www.americanexpress.com",
    "www.synchrony.com", "www.sofi.com", "www.discover.com",
    "www.fdic.gov", "banks.data.fdic.gov", "api.fdic.gov", "edie.fdic.gov",
    "www.federalreserve.gov",
    # second-session sources (additional banks) + this repository on GitHub
    "www.td.com", "www.citizensbank.com", "www.53.com", "us.hsbc.com", "www.us.hsbc.com",
    "banking.us.barclays", "www.cit.com", "github.com",
}

class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []       # (kind, value)
        self.stack = []
        self.errors = []
        self.void = {"area","base","br","col","embed","hr","img","input","link",
                     "meta","param","source","track","wbr"}

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "href" in d and d["href"]:
            self.links.append(("href", d["href"]))
        if "src" in d and d["src"]:
            self.links.append(("src", d["src"]))
        if tag not in self.void:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.void:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            # tolerate implicit closes for <p> and <li>
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.errors.append(f"unclosed <{self.stack.pop()}> before </{tag}>")
                self.stack.pop()
            else:
                self.errors.append(f"stray closing </{tag}>")


def strip_fragment(url):
    return url.split("#", 1)[0]


def anchors_in_file(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    ids = set(re.findall(r'id="([^"]+)"', html))
    names = set(re.findall(r'name="([^"]+)"', html))
    return ids | names


def main():
    problems = []
    pages = {}
    for fn in sorted(os.listdir(ROOT)):
        if fn.endswith(".html"):
            pages[fn] = os.path.join(ROOT, fn)

    all_anchors = {fn: anchors_in_file(p) for fn, p in pages.items()}

    for fn, path in pages.items():
        with open(path, encoding="utf-8") as f:
            html = f.read()
        c = Collector()
        c.feed(html)
        c.close()
        if c.stack:
            problems.append(f"{fn}: unclosed tags at EOF: {c.stack}")
        for e in c.errors:
            problems.append(f"{fn}: {e}")

        for kind, href in c.links:
            if href.startswith(("mailto:", "tel:", "javascript:", "#")):
                if href.startswith("#") and href[1:] and href[1:] not in all_anchors[fn]:
                    problems.append(f"{fn}: broken same-page anchor {href}")
                continue
            parsed = urlparse(href)
            if parsed.scheme in ("http", "https"):
                host = parsed.hostname or ""
                if host not in ALLOWED_EXTERNAL:
                    problems.append(f"{fn}: external link to non-allowlisted host {host}: {href}")
            elif parsed.scheme == "" and not href.startswith("//"):
                target = strip_fragment(href)
                frag = href.split("#", 1)[1] if "#" in href else ""
                if target == "":
                    if frag and frag not in all_anchors[fn]:
                        problems.append(f"{fn}: broken same-page anchor #{frag}")
                else:
                    # resolve relative
                    if "/" in target:
                        tpath = os.path.normpath(os.path.join(ROOT, target))
                        if not os.path.exists(tpath):
                            problems.append(f"{fn}: missing internal file {href}")
                    else:
                        if target not in pages and not os.path.exists(os.path.join(ROOT, target)):
                            problems.append(f"{fn}: missing internal file {href}")
                        elif target in pages and frag and frag not in all_anchors[target]:
                            problems.append(f"{fn}: broken anchor {href} (#{frag} not in {target})")
            else:
                problems.append(f"{fn}: unexpected link scheme {href}")

    # nav reachability from index.html
    def reachable(start):
        seen, queue = set(), [start]
        while queue:
            cur = queue.pop()
            if cur in seen:
                continue
            seen.add(cur)
            with open(os.path.join(ROOT, cur), encoding="utf-8") as f:
                for m in re.findall(r'href="([^"]+\.html)', f.read()):
                    if "/" not in m and m in pages and m not in seen:
                        queue.append(m)
        return seen

    reach = reachable("index.html")
    for fn in pages:
        if fn not in reach:
            problems.append(f"{fn}: not reachable via nav links from index.html")

    # css referenced exists
    for fn, path in pages.items():
        with open(path, encoding="utf-8") as f:
            for m in re.findall(r'href="([^"]+\.css)"', f.read()):
                if not os.path.exists(os.path.join(ROOT, m)):
                    problems.append(f"{fn}: missing stylesheet {m}")

    print(f"Checked {len(pages)} HTML pages in docs/")
    if problems:
        print(f"\n{len(problems)} PROBLEM(S):")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("All checks passed: internal links/anchors OK, external hosts allow-listed, nav complete, stylesheets present.")


if __name__ == "__main__":
    main()
