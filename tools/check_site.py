"""Offline checks for the built site. Run: python3 tools/check_site.py

Runs in site-checks.yml after build.py. Each check prints what it found and the
script exits 1 if any check fails, so a page can't ship without a title,
description, canonical URL, one h1, image alt text, a sitemap entry, or with an
email address or phone number in it.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://chaseholroyd.com/"
# 404 is served for missing paths and is not a page to index.
# studio.html and pm-tools.html are hidden "moved" stubs (Chase, Nov 18); they stay out of the sitemap.
NOT_INDEXED = {"404.html", "studio.html", "pm-tools.html"}
# Root-absolute links that point at another repo's Pages site, not a file here.
OTHER_REPO_SITES = ("/ccwatts/", "/energy-scanner/", "/role-radar/", "/pm-tools/", "/crew-clock/", "/charlie/", "/websites/", "/Hearth/")

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")
# The one public address (Chase, Nov 4 and Nov 13): it may appear on pages; no others.
ALLOWED_EMAILS = {"hello@chaseholroyd.com"}
PHONE = re.compile(r"(?<![\d.])\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)")


def pages():
    return sorted(p for p in ROOT.glob("*.html"))


def check_head(failures):
    for page in pages():
        html = page.read_text()
        name = page.name
        if not re.search(r"<title>[^<]+</title>", html):
            failures.append(f"{name}: no <title>")
        if not re.search(r'<meta name="description" content="[^"]+"', html):
            failures.append(f"{name}: no meta description")
        if len(re.findall(r"<h1[\s>]", html)) != 1:
            failures.append(f"{name}: needs exactly one <h1>")
        if name in NOT_INDEXED:
            if '<meta name="robots" content="noindex">' not in html:
                failures.append(f"{name}: should carry noindex so search engines skip it")
            continue
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        want = SITE if name == "index.html" else SITE + name
        if not canon or canon.group(1) != want:
            failures.append(f"{name}: canonical should be {want}")


def check_images(failures):
    for page in pages():
        for tag in re.findall(r"<img\b[^>]*>", page.read_text()):
            if "alt=" not in tag:
                failures.append(f"{page.name}: <img> without alt: {tag[:80]}")
            if "width=" not in tag or "height=" not in tag:
                failures.append(f"{page.name}: <img> without width and height (layout shift): {tag[:80]}")


def check_root_links(failures):
    for page in pages():
        for href in re.findall(r'(?:href|src)="(/[^"#?]*)', page.read_text()):
            if href == "/" or href.startswith(OTHER_REPO_SITES):
                continue
            target = ROOT / href.lstrip("/")
            if href.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                failures.append(f"{page.name}: root link to missing file {href}")


def check_sitemap(failures):
    sitemap = (ROOT / "sitemap.xml").read_text()
    for page in pages():
        if page.name in NOT_INDEXED:
            continue
        want = SITE if page.name == "index.html" else SITE + page.name
        if f"<loc>{want}</loc>" not in sitemap:
            failures.append(f"sitemap.xml: missing {want}")


def check_no_contact_details(failures):
    files = pages() + [ROOT / "sitemap.xml", ROOT / "robots.txt"]
    for f in files:
        text = f.read_text()
        for m in EMAIL.findall(text):
            # Image and font filenames like name@2x.png aren't addresses.
            if m not in ALLOWED_EMAILS and not re.search(r"\.(png|webp|jpg|svg|woff2?)$", m):
                failures.append(f"{f.name}: email address on a public page: {m}")
        for m in PHONE.findall(text):
            failures.append(f"{f.name}: phone number on a public page: {m}")


def check_deploy_allowlist(failures):
    """Every top-level file a page links to must be copied by pages.yml."""
    cp = re.search(r"cp -r ([^\n]+) _site/", (ROOT / ".github/workflows/pages.yml").read_text())
    shipped = cp.group(1).split() if cp else []
    for page in pages():
        for href in re.findall(r'(?:href|src)="([^"#?]+)', page.read_text()):
            if href.startswith(("/", "..", "'")) or re.match(r"[a-z]+:", href):
                continue  # a leading ' is a link built in page script, not a file
            top = href.split("/")[0]
            if top.endswith(".html") and "*.html" in shipped:
                continue
            if top and top not in shipped:
                failures.append(f"{page.name}: links {href}, but pages.yml doesn't deploy {top}")


def check_no_third_party_loads(failures):
    """Nothing loads from another host (Chase, Nov 19: Safari showed "Reduce Protections"). Fonts are self-hosted in
    assets/fonts; links to LinkedIn and GitHub are ordinary <a> links and fine."""
    from html.parser import HTMLParser

    own = ("https://chaseholroyd.com", "https://stats.chaseholroyd.com", "http://localhost")  # stats. is the first-party analytics proxy (Umami)
    loaders = {"link", "script", "img", "iframe", "source", "video", "audio", "embed", "object", "track"}

    class Loads(HTMLParser):
        def __init__(self):
            super().__init__()
            self.urls = []

        def handle_starttag(self, tag, attrs):
            for name, value in attrs:
                value = (value or "").strip()
                if tag in loaders and name in ("href", "src", "srcset", "data") and value.startswith(("http://", "https://", "//")):
                    self.urls.append(value)
                if tag == "link" and name == "rel" and value.lower() in ("preconnect", "dns-prefetch"):
                    self.urls.append("preconnect")

    for path in list(pages()) + sorted((ROOT / "assets").glob("*.css")):
        text = re.sub(r"base64,[A-Za-z0-9+/=]+", "", path.read_text())
        if path.suffix == ".html":
            parser = Loads()
            parser.feed(text)
            for url in parser.urls:
                if url == "preconnect":
                    failures.append(f"{path.name}: preconnect to another host")
                elif not url.startswith(own):
                    failures.append(f"{path.name}: loads {url[:60]} from another host (self-host it or remove it)")
        for url in re.findall(r"url\(\s*[\"']?((?:https?:)?//[^)\"']+)", text, flags=re.I):
            if not url.startswith(own):
                failures.append(f"{path.name}: CSS loads {url[:60]} from another host")


def check_scoreboard(failures):
    """The Studio page's agent scoreboard shows every row of tools/scoreboard.json, with a source and date."""
    import json
    data = json.loads((ROOT / "tools/scoreboard.json").read_text())
    page = (ROOT / "studio.html").read_text()
    if "http-equiv=\"refresh\"" in page:
        return  # the Studio page is hidden for now; the scoreboard data stays in tools/scoreboard.json
    if 'class="scoreboard"' not in page:
        failures.append("studio.html: no agent scoreboard table")
    for row in data["evals"]:
        cells = re.search(rf"<tr><th scope=\"row\">{re.escape(row['agent'])}</th><td>{re.escape(row['task'])}</td>(.*?)</tr>", page)
        if not cells:
            failures.append(f"studio.html: scoreboard is missing {row['agent']}: {row['task']}")
        elif f"{row['with']}/{row['runs']}" not in cells.group(1) or f"{row['without']}/{row['runs']}" not in cells.group(1):
            failures.append(f"studio.html: {row['agent']} scores don't match tools/scoreboard.json")
    if data["as_of"] not in page or not data.get("source"):
        failures.append("studio.html: scoreboard needs its date and a source")


def _section(html, sid):
    """The HTML of the element carrying id=sid, up to its matching close tag."""
    m = re.search(rf'<(\w+)\b[^>]*\bid="{re.escape(sid)}"[^>]*>', html)
    if not m:
        return None
    tag, depth, pos = m.group(1), 1, m.end()
    for t in re.finditer(rf"<(/?){tag}\b[^>]*>", html[pos:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return html[m.start():pos + t.end()]
    return html[m.start():]


def _text(html):
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def check_home(failures):
    """Home page v60 (Chase, Nov 16): photo, greeting, one headline, two journey lines, case studies, building, career."""
    html = (ROOT / "index.html").read_text()
    # HOME-1 Sections in order: hero, impact (journey lines), cases, ai (building), career, about, contact.
    order = [html.find(f'id="{sid}"') for sid in ("hero", "impact", "cases", "ai", "career", "about", "contact")]
    if -1 in order or order != sorted(order):
        failures.append("index.html: sections must run hero, impact, cases, ai, career, about, contact (HOME-1)")
    # HOME-2 The journey lines link to the case studies and to the building section or page.
    impact = _section(html, "impact") or ""
    if 'href="#cases"' not in impact:
        failures.append('index.html: the journey lines must link to href="#cases" (HOME-2)')
    if 'href="#ai"' not in impact and 'href="building.html"' not in impact:
        failures.append('index.html: the journey lines must link to href="#ai" or href="building.html" (HOME-2)')
    # HOME-3 At most one primary button in the hero (v60 has none: green marks links and results only).
    hero = _section(html, "hero") or ""
    if len(re.findall(r'class="btn p"', hero)) > 1:
        failures.append("index.html: the hero has more than one primary button (HOME-3)")
    # HOME-4 The single h1 is at most 25 words (Chase wants the staff PM title and the AI/ML claim in it).
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if len(h1s) == 1:
        words = len(_text(h1s[0]).split())
        if words > 25:
            failures.append(f"index.html: h1 is {words} words, keep it to 25 or fewer (HOME-4)")
    else:
        failures.append("index.html: expected exactly one h1 (HOME-4)")
    # HOME-5 No banned claims (Chase, Nov 6).
    for bad in ("$6M", "3–5 points", "3-5 points"):
        if bad in html:
            failures.append(f"index.html: remove {bad!r} (HOME-5)")
    # HOME-6 Every image on disk, and no inlined photos.
    for src in re.findall(r'<img[^>]*src="([^"]+)"', html):
        if src.startswith("data:"):
            failures.append("index.html: photos must be files in assets/, not inlined (HOME-6)")
        elif not src.startswith("http") and not (ROOT / src).exists():
            failures.append(f"index.html: image {src} doesn't exist (HOME-6)")
    # HOME-7 The greeting and headline never loop an animation (Chase, Nov 19: "Hey there" kept bobbing, a recurring
    # bug). They may fade in once; no rule that targets them may use an infinite animation.
    from html.parser import HTMLParser

    class Styles(HTMLParser):
        def __init__(self):
            super().__init__()
            self.css, self.inside = [], False

        def handle_starttag(self, tag, attrs):
            self.inside = tag == "style"

        def handle_endtag(self, tag):
            self.inside = False

        def handle_data(self, data):
            if self.inside:
                self.css.append(data)

    styles = Styles()
    styles.feed(html)
    for selector, block in re.findall(r"([^{}]+)\{([^{}]*)\}", "\n".join(styles.css)):
        if re.search(r"\.pw\b|\.hey\b|\.hero\s+h1|\.l1\b|\.l2\b", selector) and re.search(r"animation[^;}]*\binfinite\b", block, flags=re.I):
            failures.append(f"index.html: {' '.join(selector.split())[-60:]} loops an animation; the greeting must stay still (HOME-7)")


CHECKS = [check_head, check_images, check_root_links, check_sitemap,
          check_no_contact_details, check_deploy_allowlist, check_no_third_party_loads, check_scoreboard,
          check_home]


def main():
    failures = []
    for check in CHECKS:
        before = len(failures)
        check(failures)
        print(f"{check.__name__}: {'ok' if len(failures) == before else 'FAIL'}")
    if failures:
        print("\n".join(failures))
        sys.exit(1)


if __name__ == "__main__":
    main()
