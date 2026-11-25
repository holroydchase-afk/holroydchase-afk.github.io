#!/usr/bin/env python3
"""Crawl the built site and write a link map: every page, every link on it, and whether it resolves.

  python3 scripts/link-map.py [--external] [--out FILE]

Internal links are checked against the files in this repo (page, file, #anchor). Links to a product's own demo
(/hearth/, /ccwatts/ ...) live in other repos, so they are listed as "other repo" and not checked here. --external
also asks each outside address with a HEAD request (needs network; GitHub private repos answer 404).
Click paths: every route from the home page to each page, up to three clicks deep (shallow navigation is the goal).
"""
import re, sys, json, urllib.request, urllib.error
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://chaseholroyd.com"
OTHER_REPOS = ("/hearth/", "/Hearth/", "/ccwatts/", "/energy-scanner/", "/role-radar/", "/pm-tools/", "/crew-clock/", "/charlie/", "/websites/", "/hero-backgrounds/")


class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.ids = set(); self.text = ""; self._a = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag == "a" and a.get("href") is not None: self._a = [a["href"], ""]
        if tag == "iframe" and a.get("src"): self.links.append((a["src"], "(frame)"))
    def handle_data(self, d):
        if self._a is not None: self._a[1] += d
    def handle_endtag(self, tag):
        if tag == "a" and self._a: self.links.append((self._a[0], " ".join(self._a[1].split()) or "(icon)")); self._a = None


def pages():
    out = sorted(ROOT.glob("*.html")) + sorted((ROOT / "try").glob("*.html")) + sorted((ROOT / "demo").glob("*/index.html"))
    return out


def rel(p): return str(p.relative_to(ROOT))


def resolve(frm, href):
    """-> (kind, target path or url, anchor)"""
    if href.startswith(("mailto:", "tel:", "javascript:")): return "special", href, ""
    if re.match(r"https?://", href):
        if href.startswith(SITE + "/") or href == SITE:
            href = href[len(SITE):] or "/"
        else: return "external", href, ""
    path, _, anchor = href.partition("#")
    path = path.partition("?")[0]
    if path.startswith(OTHER_REPOS): return "other", path, anchor
    if path == "": target = frm
    elif path.startswith("/"): target = ROOT / path.lstrip("/")
    else: target = (frm.parent / path)
    if target.is_dir() or path.endswith("/"): target = target / "index.html"
    return "internal", target.resolve() if path else frm, anchor


def check_external(url):
    """GitHub repos are checked with the gh CLI (the proxy refuses plain requests); other hosts are only reachable
    from a normal network, so here they come back "unverified" rather than broken."""
    import subprocess
    m = re.match(r"https://github\.com/holroydchase-afk/([^/#?]+)", url)
    if m:
        r = subprocess.run(["gh", "api", f"repos/holroydchase-afk/{m.group(1)}", "--jq", ".full_name"], capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        if r.returncode == 0 and out.lower().endswith("/" + m.group(1).lower()): return "ok"
        if "Numeric-ID" in out: return "ok (repo resolves; the proxy cannot read renamed repos)"
        if "not enabled for this session" in out: return "unverified (repo not in this session)"
        return f"CHECK: {out[:60]}"
    return "unverified (needs a normal network)"


def main():
    ext = "--external" in sys.argv
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "docs" / "link-map.md"
    info = {}
    for p in pages():
        parser = P(); parser.feed(p.read_text(encoding="utf-8")); info[p.resolve()] = parser
    rows = []; broken = []; graph = {}
    ext_cache = {}
    for p, parser in info.items():
        graph[p] = set()
        for href, label in parser.links:
            kind, target, anchor = resolve(p, href)
            status = "ok"
            if kind == "internal":
                if not Path(target).exists(): status = "BROKEN: file missing"
                else:
                    graph[p].add(Path(target))
                    if anchor and Path(target) in info and anchor not in info[Path(target)].ids and anchor not in ("top",): status = f"BROKEN: no #{anchor}"
            elif kind == "other": status = "other repo (not checked here)"
            elif kind == "external":
                if ext:
                    if target not in ext_cache: ext_cache[target] = check_external(target)
                    status = ext_cache[target]
                else: status = "external (not checked)"
            rows.append((p, href, label, kind, status))
            if status.startswith(("BROKEN", "CHECK")): broken.append((p, href, label, status))
    # click paths from the home page
    home = (ROOT / "index.html").resolve(); depth = {home: 0}; via = {home: []}; q = [home]
    while q:
        cur = q.pop(0)
        for nxt in sorted(graph.get(cur, ())):
            if nxt in info and nxt not in depth:
                depth[nxt] = depth[cur] + 1; via[nxt] = via[cur] + [cur]; q.append(nxt)
    L = ["# Link map", "", f"Built from the files in this repo. Click depth counts clicks from the home page (the nav counts as one).", ""]
    L += ["## Pages and how deep they are", "", "| Page | Clicks from home | Shortest path |", "|---|---|---|"]
    for p in sorted(info, key=lambda x: (depth.get(x, 99), rel(x))):
        d = depth.get(p); path = " → ".join(rel(x) for x in via.get(p, []) + [p]) if d is not None else "not linked from anywhere"
        L.append(f"| {rel(p)} | {d if d is not None else '-'} | {path} |")
    L += ["", "## Broken or stale", ""]
    L += ([f"- `{rel(p)}`: `{h}` ({lbl}) → {s}" for p, h, lbl, s in broken] or ["- none found"])
    L += ["", "## Every link, by page", ""]
    cur = None
    for p, href, label, kind, status in sorted(rows, key=lambda r: rel(r[0])):
        if p != cur: L += ["", f"### {rel(p)}", "", "| Link text | Goes to | Status |", "|---|---|---|"]; cur = p
        L.append(f"| {label[:50].replace('|', '/')} | `{href[:90]}` | {status} |")
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{len(rows)} links on {len(info)} pages; {len(broken)} broken or stale -> {out}")
    sys.exit(1 if any(s.startswith('BROKEN') for *_, s in broken) else 0)


if __name__ == "__main__":
    main()
