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
NOT_INDEXED = {"404.html"}
# Root-absolute links that point at another repo's Pages site, not a file here.
OTHER_REPO_SITES = ("/ccwatts/", "/energy-scanner/", "/role-radar/", "/pm-tools/", "/crew-clock/", "/charlie/")

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")
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
            if not re.search(r"\.(png|webp|jpg|svg|woff2?)$", m):
                failures.append(f"{f.name}: email address on a public page: {m}")
        for m in PHONE.findall(text):
            failures.append(f"{f.name}: phone number on a public page: {m}")


def check_deploy_allowlist(failures):
    """Every top-level file a page links to must be copied by pages.yml."""
    cp = re.search(r"cp -r ([^\n]+) _site/", (ROOT / ".github/workflows/pages.yml").read_text())
    shipped = cp.group(1).split() if cp else []
    for page in pages():
        for href in re.findall(r'(?:href|src)="([^"#?]+)', page.read_text()):
            if href.startswith(("/", "..")) or re.match(r"[a-z]+:", href):
                continue
            top = href.split("/")[0]
            if top.endswith(".html") and "*.html" in shipped:
                continue
            if top and top not in shipped:
                failures.append(f"{page.name}: links {href}, but pages.yml doesn't deploy {top}")


def check_scoreboard(failures):
    """The Studio page's agent scoreboard shows every row of tools/scoreboard.json, with a source and date."""
    import json
    data = json.loads((ROOT / "tools/scoreboard.json").read_text())
    page = (ROOT / "studio.html").read_text()
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
    """Acceptance criteria for the homepage: Hearth front and center, real
    product imagery, a short h1, a resume PDF, one product name."""
    html = (ROOT / "index.html").read_text()

    # HOME-1 Hearth is featured above career and work.
    pos = {sid: html.find(f'id="{sid}"') for sid in ("hearth", "career", "work")}
    if pos["hearth"] < 0:
        failures.append('index.html: no section with id="hearth" (HOME-1)')
    else:
        for sid in ("career", "work"):
            if pos[sid] >= 0 and pos[sid] < pos["hearth"]:
                failures.append(f'index.html: id="hearth" must come before id="{sid}" (HOME-1)')

    # HOME-2 The Hearth section links to its case study and its demo.
    hearth = _section(html, "hearth") or ""
    hrefs = re.findall(r'<a\b[^>]*\bhref="([^"]+)"', hearth)
    for want in ("family-photos.html", "demo/hearth/"):
        if want not in hrefs:
            failures.append(f"index.html: Hearth section doesn't link to {want} (HOME-2)")

    # HOME-3 At least 6 product images, all on disk.
    shots = [s for s in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', html)
             if s.startswith(("assets/home/", "assets/shots/"))]
    if len(shots) < 6:
        failures.append(f"index.html: {len(shots)} product images from assets/home/ or assets/shots/, needs at least 6 (HOME-3)")
    for s in shots:
        if not (ROOT / s).exists():
            failures.append(f"index.html: image {s} doesn't exist (HOME-3)")

    # HOME-4 The single h1 is at most 14 words (REC-R13).
    h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, flags=re.S)
    if len(h1s) == 1:
        words = len(_text(h1s[0]).split())
        if words > 14:
            failures.append(f"index.html: h1 is {words} words, keep it to 14 or fewer (HOME-4, REC-R13)")
    else:
        failures.append(f"index.html: needs exactly one <h1>, found {len(h1s)} (HOME-4)")

    # HOME-5 A resume PDF link that resolves.
    pdf = "assets/chase-holroyd-resume.pdf"
    if not re.search(rf'<a\b[^>]*\bhref="{re.escape(pdf)}"', html):
        failures.append(f"index.html: no link to {pdf} (HOME-5)")
    if not (ROOT / pdf).exists():
        failures.append(f"index.html: {pdf} doesn't exist (HOME-5)")

    # HOME-6 One product name: no "name coming" once Hearth is named (REC-R2).
    text = _text(html)
    if "Hearth" in text and "name coming" in text.lower():
        failures.append('index.html: says "Hearth" and "name coming"; use one product name (HOME-6, REC-R2)')


CHECKS = [check_head, check_images, check_root_links, check_sitemap,
          check_no_contact_details, check_deploy_allowlist, check_scoreboard,
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
