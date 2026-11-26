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
NOT_INDEXED = {"404.html", "studio.html", "pm-tools.html", "about.html", "energy-scanner.html"}
# Root-absolute links that point at another repo's Pages site, not a file here.
OTHER_REPO_SITES = ("/ccwatts/", "/energy-scanner/", "/role-radar/", "/pm-tools/", "/crew-clock/", "/charlie/", "/websites/", "/Hearth/", "/hearth/")

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

    own = ("https://chaseholroyd.com", "http://localhost")
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


PRODUCT_PAGES = {"family-photos.html": "/hearth/", "crew-clock.html": "/crew-clock/",
                 "charlie.html": "/charlie/", "role-radar.html": "/role-radar/", "ccwatts.html": "/ccwatts/"}
PHONE_PRODUCTS = {"family-photos.html", "crew-clock.html", "charlie.html"}
HEADER_LINKS = ["Case studies", "Building", "Agents", "Resume", "Contact"]


def check_uniform(failures):
    """WEB-M14: one page system. Every page carries the standard header; every product page is the one template."""
    for page in pages():
        if page.name == "404.html":
            continue
        t = page.read_text()
        if 'http-equiv="refresh"' in t:
            continue  # a moved-page stub
        nav = re.search(r'<nav aria-label="Main">(.*?)</nav>', t, re.S)
        labels = re.findall(r">([^<]+)</a>", nav.group(1)) if nav else []
        if labels != HEADER_LINKS:
            failures.append(f"{page.name}: header nav must be {HEADER_LINKS}, found {labels} (UNI-1)")
        if 'id="tog"' not in t:
            failures.append(f"{page.name}: the standard header's theme button is missing (UNI-1)")
    for name, demo in PRODUCT_PAGES.items():
        t = (ROOT / name).read_text()
        if f'data-demo="{demo}"' not in t or "<iframe" not in t:
            failures.append(f"{name}: product page must embed its demo at {demo} (UNI-2)")
        for control in ("data-reload", f'href="/try/{demo.strip("/")}.html">Open full page', ">Code &#8599;</a>"):
            if control not in t:
                failures.append(f"{name}: demo control missing: {control} (UNI-2)")
        want = "is-phone" if name in PHONE_PRODUCTS else "is-browser"
        if want not in t:
            failures.append(f"{name}: demo must sit in a {'phone' if name in PHONE_PRODUCTS else 'browser'} frame (UNI-3)")
        if 'href="/building.html"' not in t:
            failures.append(f"{name}: needs the one back link to Building (UNI-4)")
    for name, demo in PRODUCT_PAGES.items():
        f = ROOT / "try" / f"{demo.strip('/')}.html"
        t = f.read_text() if f.exists() else ""
        if f'data-demo="{demo}"' not in t or 'id="tog"' not in t or "noindex" not in t:
            failures.append(f"try/{demo.strip('/')}.html: full-screen page needs the header, the demo at {demo} and noindex (UNI-7)")
    # No page sends a visitor past the product page to a raw demo address (the demo opens inside the product page).
    raw = re.compile(r'href="(?:https://chaseholroyd\.com)?/(hearth|energy-scanner|crew-clock|charlie|role-radar|ccwatts)/"')
    for page in pages():
        if page.name in PRODUCT_PAGES:
            continue
        if raw.search(page.read_text()):
            failures.append(f"{page.name}: links straight to a raw demo; link the product page instead (UNI-5)")
    # The demo header script draws the same links as the page header.
    js = (ROOT / "assets/demo-bar.js").read_text()
    for label in HEADER_LINKS:
        if f">{label}</a>" not in js:
            failures.append(f"assets/demo-bar.js: standard header link missing: {label} (UNI-6)")
    if 'window.top !== window.self' not in js:
        failures.append("assets/demo-bar.js: must stay out of the way inside the product page frame (UNI-6)")


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


def check_make_your_own(failures):
    """Make your own (Nov 21): every Tools card's copy button carries the exact prompt stored in prompts/<slug>.txt;
    prompts stay under 120 words and end with 'or something'; one button per card."""
    import html as H
    files = sorted((ROOT / "prompts").glob("*.txt"))
    for f in files:
        text = f.read_text().strip()
        if len(text.split()) > 120:
            failures.append(f"{f.name} is over 120 words")
        if not text.rstrip(".").endswith("or something"):
            failures.append(f"{f.name} should end with 'or something'")
    for page in ("index.html", "building.html"):
        h = (ROOT / page).read_text()
        found = re.findall(r'data-mk="([a-z-]+)" data-prompt="([^"]*)"', h)
        slugs = [s for s, _ in found]
        if len(set(slugs)) != len(slugs):
            failures.append(f"{page}: a Make your own button appears twice")
        for slug, prompt in found:
            f = ROOT / "prompts" / f"{slug}.txt"
            if not f.exists():
                failures.append(f"{page}: {slug} has no prompts/{slug}.txt")
            elif H.unescape(prompt) != f.read_text().strip():
                failures.append(f"{page}: {slug} differs from prompts/{slug}.txt (run tools/sync_prompts.py)")
        missing = {f.stem for f in files} - set(slugs)
        if missing:
            failures.append(f"{page}: no button for {sorted(missing)}")
        cards = len(re.findall(r'class="kc"', h.split("Small tools with code on GitHub", 1)[-1].split("</section>", 1)[0]))
        if cards != len(slugs):
            failures.append(f"{page}: {cards} Tools cards but {len(slugs)} Make your own buttons")


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
          check_home, check_make_your_own, check_uniform]


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
