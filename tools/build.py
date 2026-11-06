#!/usr/bin/env python3
"""Builds the static pages for chaseholroyd.com from the PAGES content below.

Run from the repo root: python3 tools/build.py
Each page is plain HTML written to the repo root, so GitHub Pages serves it with no build step.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://chaseholroyd.com"
LINKEDIN = "https://www.linkedin.com/in/chase-holroyd"
GITHUB = "https://github.com/holroydchase-afk"

# Keep the site out of search engines while it's in progress (Chase, Oct 25): every page carries noindex and
# robots.txt drops the sitemap line. Anyone with the link can still open it. Set False when the site is ready.
NOINDEX = True
# robots.txt disallows these AI crawlers.
AI_BOTS = ["GPTBot", "ChatGPT-User", "ClaudeBot", "anthropic-ai", "CCBot", "Google-Extended",
           "PerplexityBot", "Bytespider", "Applebot-Extended"]

# Below the 8/10 bar: the home page leaves these out and lists them, unlinked, as in active development.
# Their pages stay up for anyone with the link. Remove a page from this set once it reaches the bar.
IN_DEVELOPMENT = {"energy-scanner.html"}

# Nov 4 shape (Chase): feature Hearth and ccwatts only. Everything else sits in a labeled "In progress" band that
# claims only what the repo backs today and says what is left. A product moves up when its row in
# pmo/portfolio/claims-register.md is "ready". FEATURED_WORK is the "Built with AI" rows (Hearth has its own band).
FEATURED_WORK = {"ccwatts.html"}
# (page, name, what it is, what's left before it moves up, link label)
IN_PROGRESS = [
    ("role-radar.html", "Role Radar", "A scheduled agent that scans company boards and scores every role 0-100 with a stated reason. The demo runs on made-up data.",
     "confirming the board count and tightening the demo's sample data.", "See the demo"),
    ("charlie.html", "Charlie", "Paper-trading ideas that start from companies you already understand, with max loss and breakeven on each. Paper trading only.",
     "publishing its test results.", "See the demo"),
    ("crew-clock.html", "Crew Clock", "A phone time clock for small crews: three taps to clock in, even with no signal.",
     "a beta with a small real crew.", "See the demo"),
    ("energy-scanner.html", "Energy Scanner", "A bedtime routine for kids that ends in an energy scan, on-device only.",
     "a copy pass before I call it done.", "See the app"),
    ("/websites/", "Open Arms Foundation", "The website I built for a children's home in Medell\u00edn, Colombia.",
     "adding the sponsorship details.", "Visit the site"),
]

# Hearth (WEB-M8, Oct 30): featured first on home. The rename is still pending, so it shows as a working name,
# matching the demo's own banner (REC-R2). After the rename, change HEARTH and HEARTH_TAG here and nowhere else.
HEARTH = "Hearth"
HEARTH_TAG = "working name · family beta late November"
# Test counts from the Hearth repo (release M1.1, Oct 28): 664 app tests, 960+ database checks.
HEARTH_FACTS = [("734", "app tests, counted Nov 4"), ("1,029", "database checks, counted Nov 4"), ("US-hosted", "photo storage"), ("0", "ads, trackers or AI training")]
HEARTH_TEAM = ("I'm the founder and product lead, with my two brothers contributing on security and on marketing and communications. "
               "I ran the build with a team of AI agents, tests first.")

NAV = [
    ("index.html", "Work"),
    ("studio.html", "Studio"),
    ("resume.html", "Resume"),
    ("about.html", "About"),
]

FONTS = ("https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;500;600"
         "&display=swap")

# Person markup so a search for the name can show the right profile. No email or phone, by rule.
JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfilePage","mainEntity":{"@type":"Person","name":"Chase Holroyd",
"jobTitle":"Staff Product Manager","description":"Staff product manager in pricing, payments and point-of-sale lending, building products with AI agents.",
"url":"https://chaseholroyd.com","image":"https://chaseholroyd.com/assets/chase-800.jpg",
"address":{"@type":"PostalAddress","addressLocality":"Charlotte","addressRegion":"NC","addressCountry":"US"},
"alumniOf":{"@type":"CollegeOrUniversity","name":"West Virginia University"},
"sameAs":["https://www.linkedin.com/in/chase-holroyd","https://github.com/holroydchase-afk"]}}
</script>
"""


# Headshot (WEB-M2.6, Chase, Oct 26): 400 and 800px WebP plus an 800px JPG for JSON-LD, metadata stripped.
# It sits above the fold on home and About, so it loads eagerly.
HEADSHOT = ('<img class="headshot" src="assets/chase-400.webp" srcset="assets/chase-400.webp 1x, assets/chase-800.webp 2x" '
            'width="200" height="200" alt="Chase Holroyd" fetchpriority="high" decoding="async">')


def page(slug, title, description, body):
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == slug else ""}>{label}</a>'
        for href, label in NAV
    )
    full_title = "Chase Holroyd" if slug == "index.html" else f"{title} · Chase Holroyd"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
{'<base href="/">' + chr(10) if slug == "404.html" else ""}{'<meta name="robots" content="noindex">' + chr(10) if NOINDEX or slug == "404.html" else ""}<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{full_title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{SITE}/{'' if slug == 'index.html' else slug}">
<meta property="og:type" content="{'profile' if slug == 'about.html' else 'website'}">
<meta property="og:image" content="{SITE}/assets/share-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Chase Holroyd, staff product manager: pricing, payments and point-of-sale lending">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITE}/{'' if slug == 'index.html' else slug}">
{JSONLD if slug in ('index.html', 'about.html') else ''}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/site.css">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<a class="mark" href="index.html"><span class="mono" aria-hidden="true">CH</span>Chase Holroyd</a>
<nav class="top" aria-label="Main">{nav}</nav>
</div></header>
<main class="{"home" if slug == "index.html" or "pp-hero" in body else "wrap"}" id="main">
{body}
</main>
<footer class="site"><div class="wrap">
<span>© 2026 Chase Holroyd · Staff product manager · Charlotte area</span>
<span><a href="{LINKEDIN}">LinkedIn</a> · <a href="{GITHUB}">GitHub</a></span>
</div></footer>
</body>
</html>
"""


def product(eyebrow, name, lede, facts, sections, status_note=None, links=None, shot=None, feature=None, accent=None):
    """The shared product-page template (docs/product/PAGE-GUIDELINES.md): dark hero band with the phone shot,
    a proof row of four facts, then one band per section (number, title, body), then a back link."""
    facts_html = "".join(f'<div class="fact"><b>{v}</b><span>{k}</span></div>' for v, k in facts)
    links_html = ""
    if links:
        links_html = '<div class="cta">' + "".join(
            f'<a class="btn{" primary" if i == 0 else ""}" href="{u}">{t}</a>' for i, (t, u) in enumerate(links)
        ) + "</div>"
    # shot = (file, alt, height at 300px wide, optional caption). Sample data only; above the fold, so eager.
    shot_html = ""
    if shot:
        cap = f'<figcaption class="shot-cap">{shot[3]}</figcaption>' if len(shot) > 3 else ""
        shot_html = f'<div class="pp-art">{phone("assets/shots/" + shot[0], shot[1], 300, shot[2], eager=True)}{cap}</div>'
    secs = "".join(
        f'<section class="psec"><div class="wrap psec-grid"><h2>{h}</h2><div class="pbody">{c}</div></div></section>'
        for h, c in sections)
    note = f'<section class="psec"><div class="wrap psec-grid"><h2>A note on the demo</h2><div class="pbody"><p>{status_note}</p></div></div></section>' if status_note else ""
    feat = f'<section class="pfeature"><div class="wrap">{feature}</div></section>' if feature else ""
    style = f' style="--pp:{accent}"' if accent else ""
    return f"""<section class="hero-band pp-hero"{style}><div class="wrap">
<div class="hero-grid{" has-art" if shot else ""}"><div>
<p class="eyebrow">{eyebrow}</p>
<h1>{name}</h1>
<p class="lede">{lede}</p>
{links_html}
</div>{shot_html}</div>
<div class="facts proof">{facts_html}</div></div></section>
{feat}{secs}{note}
<section class="psec back"><div class="wrap"><a class="btn" href="index.html">← All work</a></div></section>"""


# ---- Product-page template (docs/product/PAGE-GUIDELINES.md) -------------------------------------------------
# Every product page is product(...) with sections in the fixed order from the guidelines. These helpers build the
# shared blocks so no page hand-writes its own markup.
def code_block(*lines, label=None):
    cap = f'<p class="code-label">{label}</p>' if label else ""
    return cap + '<pre class="code"><code>' + "\n".join(lines) + "</code></pre>"


def proof_grid(items):
    """items = [(heading, text)]: short, checkable claims, each backed by the product's repo."""
    return '<ul class="proof-grid">' + "".join(f"<li><b>{h}</b><span>{t}</span></li>" for h, t in items) + "</ul>"


def shots(*figs, note=None):
    """figs = [(src, alt, w, h, caption)] rendered as captioned figures; sample data only."""
    out = "".join(
        f'<figure class="pshot"><a href="assets/shots/{s}"><img src="assets/shots/{s}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{a}"></a><figcaption>{c}</figcaption></figure>'
        for s, a, w, h, c in figs)
    return f'<div class="pshots">{out}</div>' + (f'<p class="note">{note}</p>' if note else "")


def range_viz(rows, ticks, lo, hi, caption):
    """Log-scale range bars. rows = [(label, low, high, marker, text, css_class)]. Numbers must come from the product's method doc."""
    import math
    pos = lambda v: 100 * (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
    out = ""
    for label, a, b, m, text, cls in rows:
        out += (f'<div class="rv-row {cls}"><p class="rv-label"><b>{label}</b><span>{text}</span></p>'
                f'<div class="rv-track"><i class="rv-bar" style="left:{pos(a):.1f}%;width:{pos(b) - pos(a):.1f}%"></i>'
                f'<i class="rv-dot" style="left:{pos(m):.1f}%"></i></div></div>')
    axis = "".join(f'<span style="left:{pos(t):.1f}%">{t} kWh</span>' for t in ticks)
    return f'<div class="rv" role="img" aria-label="{caption}">{out}<div class="rv-axis">{axis}</div></div><p class="rv-cap">{caption}</p>'


# Career highlights on the home page. Facts trace to pmo/story/resume-2026-10.md; outside links are public pages.
# [check] items wait on Chase (WEB-M5); none of this merges until they're cleared.
CAREER = [
    ("Patter AI", "2023–2026 · Staff PM",
     "An AI-native sales platform for solar and home services. I led a single real-time pricing engine across loans, leases and PPAs, "
     "a rep-guided checkout that shows the payment impact of each add-on, and a lender rules engine that cut lender onboarding from 4 weeks to 1 week. An agentic pipeline cut each new lender integration from 2 engineers for a 2-week sprint to 1–2 days.",
     [("See Patter", "https://salespatter.io")]),  # [check] Capterra lists salespatter.io as Patter's site; confirm the URL
    ("ADT", "2020–2023 · PM to Senior PM",
     "First PM for ADT's solar division. I built the credit-check and offer engine (35,000+ applications a month across 5 lenders) "
     "and a lender allocation platform, with releases to 5,000+ reps.",
     []),  # Links to the ADT case study once WEB-M2.3 clears
    ("Palmetto", "2016–2019 · Engineer to Director",
     "I was Palmetto's first PM and built Alchemy, its design, point-of-sale and real-time credit platform. "
     "Then I launched a machine-learning lead marketplace at 11,500+ consultations a month.",
     [("Alchemy in the press", "https://techstartups.com/?p=13148"), ("Palmetto today", "https://palmetto.com")]),
]

# The AI journey: each product starts with a problem in Chase's life and its real users. Ordered by how the
# building grew (one prototype page → scheduled agent → open source → an agent team → the system behind it), not by date.
# (page, product, the life problem, what changed in how I built it, who uses it, CTA label, line for the
# in-development list). A "[check]" who-line is not rendered until Chase answers it (WEB-M5). Pages in
# IN_DEVELOPMENT render only their last field, in the unlinked list under the steps.
JOURNEY = [
    ("energy-scanner.html", "Energy Scanner",
     "Bedtime with my kids had become a nightly negotiation. I designed a routine that ends in an energy scan, so a neutral signal, not a parent, calls lights out.",
     "Built as a single page in one evening and tested with its real users at bedtime that night.",
     "[check] Who uses it today, e.g. my kids every night", "Try the app",
     "a bedtime routine for my kids that ends in an on-device energy scan"),
    ("role-radar.html", "Role Radar",
     "A job search is mostly triage. An agent reads about 190 company boards on request and scores every role with a stated reason, so my time goes to the few worth pursuing.",
     "My first scheduled agent: it runs unattended, and I review its judgment rather than the raw feed.",
     "[check] Who uses it besides me", "Try the demo", ""),
    ("ccwatts.html", "ccwatts",
     "I wanted to know the electricity cost of my own AI-assisted coding. No tool answered it, so I built a local one that reports a sourced range instead of a false point estimate.",
     "My first open-source release, with a public methodology, full tests and a citation for every assumption.",
     "[check] Who's using it", "Try the playground", ""),
    ("charlie.html", "Charlie: Invest in What You Know",
     "Most trading apps start from the trade, so beginners act on hype instead of businesses they understand. Charlie starts from what you already know and turns it into a few paper trades with the risk spelled out.",
     "Research first, safety rules enforced in code and tests rather than copy, and one tested Python engine that runs on a server and in the browser.",
     "Built for a new investor learning options by paper trading companies inside their own circle of competence", "Try the demo", ""),
    ("family-photos.html", HEARTH,
     "Two blended families, five group texts and grandparents on Android. I'm building one private place for our photos, where every post reaches exactly the people it's meant for.",
     "I ran AI agents as a product team: a spec, tests first, a privacy review and a usability pass for grandparents.",
     "Family beta with about a dozen relatives, mostly grandparents, in late November", "Try the demo",
     "a private photo app for two blended families, with a family beta in late November"),
    ("crew-clock.html", "Crew Clock",
     "A small rural crew tracked hours on paper and memory, so pay disputes came down to whose story you believed. Crew Clock signs every punch on the phone, works with no signal, and costs nothing to run.",
     "Built with the agent team from day one: tests first, then four rounds of UX review before the demo went public.",
     "A five-person crew starts a two-week beta next", "Try the demo", ""),
    ("pm-tools.html", "Studio Console",
     "My agents were shipping across several products faster than I could read their work. I built one goal-first page that shows where my week went and every call waiting on me.",
     "It rebuilds hourly from public GitHub repos, with no database or login, and replaced my earlier slate and roadmap apps.",
     "[check] OK to say \"about an hour a night\"?", "See the console", ""),
    ("studio.html", "The studio behind it",
     "Five products and one person. Each AI chat lost what the others knew, which made me the only shared memory and the bottleneck.",
     "Specialist agents, a coordinator that only coordinates, and me as product owner, reviewing what ships.",
     "Every product on this page runs through it.", "Read the story", ""),
]

# Every number here traces to the career master impact bank (atlas-portfolio facts/career-impacts.md: PAT-01, ADTP-01, X-01). Change them only with the master.
PROOF = [
    ("8+ years", "in pricing, payments and point-of-sale lending"),
    ("14+", "lender integrations shipped"),
    ("2 wks → 48 hrs", "to onboard a new client at Patter"),
    ("60%", "faster contract review at ADT"),
]

# Home (WEB-M8, Chase, Oct 30: "Hearth front and center", quality screenshots, immersive). Full-bleed bands, each
# with its own .wrap: hero, featured Hearth, career, the AI work as image rows, closing call. Every screenshot is a
# demo on sample data (assets/home/ and assets/shots/; re-shoot with Playwright at 390x844 or 1440x900, 2x).
RESUME_PDF = "assets/chase-holroyd-resume.pdf"


def phone(src, alt, w=300, h=600, eager=False, cls=""):
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<figure class="phone{(" " + cls) if cls else ""}"><img src="{src}" width="{w}" height="{h}" alt="{alt}" {load}></figure>')


def browser(src, alt, cls="", eager=False):
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<figure class="browser{(" " + cls) if cls else ""}"><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>'
            f'<img src="{src}" width="1200" height="750" alt="{alt}" {load}></figure>')


# Career cards lead with one number each; every number traces to pmo/story/resume-2026-10.md.
CAREER_STAT = {"Patter AI": ("4 wks → 1 wk", "to onboard a new lender"),
               "ADT": ("35,000+", "credit applications a month"),
               "Palmetto": ("11,500+", "consultations a month")}

# The AI work as rows with screenshots, in the JOURNEY order. (page, images html) per row; text comes from JOURNEY.
WORK_SHOTS = {
    "role-radar.html": browser("assets/home/role-radar-wide.webp", "Role Radar on a laptop, sample data: the morning digest and the top-scored roles.")
        + phone("assets/shots/role-radar-phone.webp", "Role Radar on a phone, sample data: a Senior Product Manager role scored 90 with the reason it fits."),
    "ccwatts.html": phone("assets/shots/ccwatts-phone.webp", "The ccwatts playground on a phone, sample data: 8.5 kWh over 30 days, with a range of 1.3 to 30.5 kWh."),
    "pm-tools.html": browser("assets/home/console-wide.webp", "The Studio Console on a laptop, a snapshot from Oct 31: each product's stage, goal and next step."),
}

# Hero tiles (Chase, Oct 31: no collage, and the three-phone layout is Hearth's alone): four products in an even
# 2x2 grid, each a link to its live demo with the top of one screenshot rising from the tile's bottom edge.
# (name, one line, link, image, alt, "wide" for a laptop shot or "phone")
HERO_TILES = [
    ("ccwatts", "Electricity use of AI coding, as a sourced range", "/ccwatts/", "assets/home/ccwatts-wide.webp",
     "ccwatts, sample data: estimated electricity for 30 days of AI coding.", "wide"),
    (HEARTH, "Private family photos, with an audience on every post", "#hearth", "assets/home/hearth-feed.webp",
     f"{HEARTH}, sample family: a photo that says which side of the family it went to.", "phone"),
]
SIZES = {"assets/home/ccwatts-wide.webp": (1200, 750), "assets/home/charlie-wide.webp": (1200, 750),
         "assets/home/hearth-feed.webp": (600, 1097), "assets/home/crew-clock-phone.webp": (600, 1191)}
# Hero tiles (Chase, Nov 6): no products before Career, so the hero shows the three career wins instead. Each links to
# the Career band. Numbers come from CAREER_STAT below (every one traces to the resume and the career facts).
HERO_GRID = '<ul class="tiles career-tiles">' + "".join(
    f'<li><a class="tile t-stat" href="#career"><span class="tile-text"><b>{c}</b><span class="when">{r}</span>'
    f'<span class="big">{CAREER_STAT[c][0]}</span><span>{CAREER_STAT[c][1]}</span></span></a></li>'
    for c, r, *_ in CAREER) + "</ul>"

home = f"""<section class="band hero-band"><div class="wrap hero-grid">
<div class="hero-copy">
<div class="who-line">{HEADSHOT}<p class="eyebrow">Open to remote senior and staff PM roles</p></div>
<h1>Staff PM for pricing, payments and <span class="nowrap">point-of-sale</span> lending.</h1>
<p class="lede">8+ years building the pricing, credit and checkout systems that sell and finance home solar, at Palmetto, ADT and Patter AI. I now use AI to take real problems to working products, with the same discipline: clear rules, tests first and privacy by design.</p>
<div class="cta"><a class="btn primary" href="#hearth">See the work</a><a class="btn" href="{RESUME_PDF}" download>Download resume (PDF)</a><a class="btn ghost" href="{LINKEDIN}">LinkedIn</a></div>
</div>
<div class="hero-art tiles-wrap">{HERO_GRID}</div>
</div>
<div class="wrap"><div class="facts proof">""" + "".join(f'<div class="fact"><b>{v}</b><span>{k}</span></div>' for v, k in PROOF) + f"""</div></div></section>

<section class="band" id="career" aria-labelledby="career-h"><div class="wrap">
<div class="read reveal"><p class="eyebrow">Part one · Career</p><h2 id="career-h">Where I've led</h2>
<p>From first PM to staff, in pricing, payments and point-of-sale lending.</p></div>
<div class="grid career-grid">""" + "".join(
    f'<article class="card career reveal"><span class="tag">{r}</span><h3>{c}</h3>'
    + (f'<p class="stat"><b>{CAREER_STAT[c][0]}</b> {CAREER_STAT[c][1]}</p>' if c in CAREER_STAT else "")
    + f'<p>{d}</p>'
    + (('<p class="links">' + " · ".join(f'<a href="{u}">{t}</a>' for t, u in links) + "</p>") if links else "")
    + "</article>"
    for c, r, d, links in CAREER
) + """</div>
<div class="bridge reveal"><h3>The through-line</h3>
<p>Across all three companies the work was the same: decisions that touch money need written rules and a stated reason for every outcome. That is how an offer engine scores a credit application, and it is the discipline I carry into the AI work below.</p>
<p class="links"><a href="resume.html">Read the full resume</a></p></div>
</div></section>

<section class="band divider" id="built" aria-labelledby="built-h"><div class="wrap">
<p class="eyebrow">Part two</p><h2 id="built-h">What I've built with AI</h2>
<p class="lede">Since January 2026 I've taken real problems from my own life to working, tested products. Two of them, then the rest.</p>
</div></section>

<section class="band feature" id="hearth" aria-labelledby="hearth-h"><div class="wrap feature-grid">
<div class="feature-copy reveal">
<p class="eyebrow">Featured · {HEARTH_TAG}</p>
<h2 id="hearth-h">{HEARTH}: one private place for a blended family's photos</h2>
<p class="lede">Two blended families, five group texts and grandparents on Android. {HEARTH} lets a parent choose exactly who sees each post, and keeps it simple enough for a grandparent who stays off social media.</p>
<ul class="ticks">
<li><b>Audience on every post.</b> Share with everyone, one side of the family, or a group you name.</li>
<li><b>Built for grandparents.</b> Large text, words under every icon, no passwords.</li>
<li><b>Private underneath.</b> Photos encrypted before upload, group chat end-to-end encrypted, access enforced in the database, no ads or AI training.</li>
</ul>
<div class="facts">{"".join(f'<div class="fact"><b>{v}</b><span>{k}</span></div>' for v, k in HEARTH_FACTS)}</div>
<div class="cta"><a class="btn" href="/Hearth/">Try the demo</a><a class="btn" href="family-photos.html">Read the case study</a></div>
<p class="credit">{HEARTH_TEAM}</p>
</div>
<div class="feature-art reveal">""" + phone("assets/home/hearth-grandma.webp", f"{HEARTH} as a grandparent, sample family: bigger text and only the photos shared with her.", h=533, cls="f-back") \
    + phone("assets/home/hearth-share.webp", f"{HEARTH}'s share screen, sample family: who can see the post, by group and by name.", h=563, cls="f-front") \
    + phone("assets/home/hearth-groups.webp", f"{HEARTH}'s groups, sample family: Everyone and each side of the family, by name.", h=563, cls="f-side") + """</div>
</div></section>

<section class="band alt" id="work" aria-labelledby="work-h"><div class="wrap">
<div class="read reveal"><p class="eyebrow">Featured · open source</p><h2 id="work-h">ccwatts</h2>
<p>My open-source release: a sourced range for the electricity AI coding uses. The demo runs on sample data in your browser. How I direct the agents behind it: <a href="studio.html">the studio</a> and the <a href="pm-tools.html">Studio Console</a>.</p></div>
""" + "".join(
    f'<article class="work-row reveal{" has-art" if h in WORK_SHOTS else ""}"><div class="work-copy">'
    f'<p class="num">{i:02d}</p><h3><a href="{h}">{n}</a></h3><p>{d}</p><p class="how">{how}</p>'
    + (f'<p class="who">{w}</p>' if not w.startswith("[check]") else "")
    + f'<p class="go"><a class="btn" href="{h}">{cta} →</a></p></div>'
    + (f'<div class="work-art{" combo" if WORK_SHOTS[h].startswith("<figure class=\"browser") and "phone" in WORK_SHOTS[h] else ""}">{WORK_SHOTS[h]}</div>' if h in WORK_SHOTS else "")
    + "</article>"
    for i, (h, n, d, how, w, cta, _) in enumerate([j for j in JOURNEY if j[0] in FEATURED_WORK], 1)
) + "</div></section>" + f"""
<section class="band" id="in-progress" aria-labelledby="ip-h"><div class="wrap">
<div class="read reveal"><p class="eyebrow">In progress</p><h2 id="ip-h">Also in progress</h2>
<p>These are working builds, shown with what is still open. Each moves up when it is finished.</p></div>
<div class="grid career-grid">""" + "".join(
    f'<article class="card career reveal"><h3>{n}</h3><p>{d}</p>'
    f'<p class="how"><b>Next:</b> {left}</p><p class="links"><a href="{h}">{cta} \u2192</a></p></article>'
    for h, n, d, left, cta in IN_PROGRESS) + f"""</div></div></section>

<section class="band closing"><div class="wrap closing-inner reveal">
<h2>Senior and staff PM roles in pricing, payments and lending</h2>
<p class="lede">I'm open to remote roles. LinkedIn is the fastest way to reach me.</p>
<div class="cta"><a class="btn primary" href="{LINKEDIN}">Connect on LinkedIn</a><a class="btn" href="{RESUME_PDF}" download>Download resume (PDF)</a></div>
</div></section>
<script>
// Fade sections in as they scroll into view. Without JS, or with reduced motion, everything is simply visible.
if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {{
  document.documentElement.classList.add('js-reveal');
  const io = new IntersectionObserver(es => es.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }}), {{ rootMargin: '0px 0px -8% 0px' }});
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
}}
</script>"""

family = product(
    f"Mobile app · {HEARTH_TAG}",
    f"{HEARTH}: a private family photo app",
    "Two blended families, five family group texts, and grandparents on Android while everyone else is on iPhone. "
    "I set out to build one private place where each photo reaches exactly the people it's meant for.",
    [("Per post", "audience you choose"), ("US", "where photos are stored"), ("0", "ads, trackers or AI training"),
     ("Test-first", "every fix starts as a failing test")],
    [
        ("The problem", "<p>Families with divorces, remarriages and step-relatives don't fit one group chat. Photos of our kids arrived late, compressed, or not at all, and every send carried the worry of who might feel left out. "
         "Existing family apps assume one household, and we don't post our kids publicly.</p>"),
        ("What I built", '<ul class="clean"><li><b>Groups you name:</b> share with Everyone, one side of the family, or an event. One person can be in several groups.</li>'
         "<li><b>No social pressure:</b> no \"Seen by 3 of 8\" count. A returned heart shows the photo arrived.</li>"
         "<li><b>Built for grandparents:</b> large text and tap targets, words under every icon, and a 6-digit email code instead of a password.</li></ul>"
         '<figure class="gallery-wide wide-only"><img src="assets/family/laptop-01-demo.webp" width="1200" height="750" loading="lazy" alt="The demo on a laptop: the app beside a short guide"></figure>'
         '<div class="gallery">'
         '<img src="assets/family/iphone-02-share.webp" width="390" height="844" loading="lazy" alt="Share screen: a picked photo, a caption, and the group that will see it">'
         '<img src="assets/family/iphone-03-posted.webp" width="390" height="844" loading="lazy" alt="Photos as the parent: the new post says who it was shared with">'
         '<img src="assets/family/iphone-05-grandparent.webp" width="390" height="844" loading="lazy" alt="Photos as a grandparent: bigger text, only what was shared with her">'
         '</div><p class="note">A made-up family with drawn sample pictures. No real people.</p>'),
        ("How it works", "<p>Photos are encrypted on the phone (AES-256-GCM) before upload, location and camera data are stripped and checked on the phone, group chat is end-to-end encrypted with MLS (RFC 9420), "
         "and access rules live in the database with Postgres row-level security, so a post you can't see behaves as if it doesn't exist.</p>"
         "<p><b>The limit:</b> today Hearth's server still holds the photo keys. A family vault, where only family phones hold the keys, is planned and not built.</p>"),
        ("Product calls", '<ul class="clean"><li><b>Delete the model built yesterday.</b> A fixed family tree was specced, built and deployed. One real relative belonged in two households, so it was replaced by plain named groups anyone can be in more than once.</li>'
         "<li><b>Measure feelings, not just engagement.</b> \"Seen by 3 of 8\" is a guilt meter in a family, so it was cut.</li>"
         "<li><b>Claim only what's true today.</b> The app says \"stored in the US\", not \"never leaves the US\", because push notifications and vendor support cross borders.</li></ul>"),
        ("Proof", proof_grid([
            ("Tested", "734 app tests and 1,029 database checks, counted Nov 4 with a script in the repo (scripts/test-totals.sh)."),
            ("Test-first", "Every change starts with a failing test, and every product decision gets a persona check that CI enforces."),
            ("Open", "The code is public on GitHub, with architecture and threat-model docs."),
            ("Self-reviewed", "No outside security audit yet."),
        ])),
        ("Try it", "<p>Open the demo, a made-up family kept only in your browser. Switch to Grandma Jo's view from the demo bar's Details and see only what was shared with her.</p>"),
        ("Status and what's next", f"<p>The core flow works end to end on a phone. A private beta with about a dozen family members, mostly grandparents, is a soft target for late November. {HEARTH_TEAM} "
         "I built it with a team of nine AI agents, routed by a chief-of-staff session.</p>"),
    ],
    status_note="The demo is a made-up family kept only in your browser: no sign-in, no backend.",
    links=[("Try the demo", "/Hearth/")],
)

role_radar = product(
    "AI tool · beta",
    "Role Radar",
    "Most of a job search is triage. Role Radar reads the boards when I run a scan and explains which roles merit my time, so I can say no faster and focus on the few that fit.",
    [("~190", "company job boards watched"), ("5", "sources merged, duplicates removed"), ("0–100", "fit score, each with a one-line reason"),
     ("By hand", "every application is still my call")],
    [
        ("The problem", "<p>Most of a job search is triage: dozens of boards, repeat postings, and a pull to apply to everything. The scarce thing is my attention, so the tool's job is to say no faster.</p>"),
        ("What I built", '<ul class="clean"><li><b>A scan on request</b> across company boards (Greenhouse, Ashby, Lever), ZipRecruiter, Himalayas, Climatebase and job-alert emails, with duplicates merged.</li>'
         "<li><b>A 0-100 fit score</b> for every role with a one-line reason.</li>"
         "<li><b>One tracker</b> that updates itself when an application is confirmed or closed.</li></ul>"),
        ("How it works", "<p>Each role is scored against criteria I edit in one plain file: title, remote, pay, sectors and culture signals. The score always shows its reasons, so a wrong call is a one-line fix to the criteria, not a mystery. The agent finds and ranks; reading the posting and applying stay with me.</p>"),
        ("Product calls", '<ul class="clean"><li><b>Explainable over clever.</b> Every score shows its reasons, and the criteria are plain text.</li>'
         "<li><b>Precision, not volume.</b> The goal is fewer, better applications, measured by how many top-scored roles become real conversations.</li>"
         "<li><b>One tracker, not three.</b> Status lived in three places and drifted, so I retired the old pipeline.</li>"
         "<li><b>Cost-aware.</b> Big boards run three days a week, and a scan stops paging when results stop being new.</li></ul>"),
        ("Proof", proof_grid([
            ("Tested", "30+ test files in the public repo."),
            ("Demo on sample data", "Made-up jobs and companies; screenshots are labeled demo data."),
            ("Open", "Code on GitHub, with a README case study."),
        ])),
        ("Try it", "<p>The demo runs the real app in your browser on made-up jobs. Try anything: it resets when you reload.</p>"),
        ("Status and what's next", "<p>The radar runs for me every weekday. The public demo shows the radar only; I am confirming the board count against the repo and tightening the demo's sample data before calling it done. A single-page app on Claude with its own saved database, plus connectors for ZipRecruiter and email.</p>"),
    ],
    links=[("Try the live demo", "/role-radar/"), ("Code on GitHub", f"{GITHUB}/role-radar")],
    shot=("role-radar-phone.webp", "Role Radar on a phone, sample data: the New tab with a Senior Product Manager role scored 90, Strong, with the reason it fits.", 600,
          "The demo reads 9 sample boards. The real radar watches about 190."),
)

ccwatts = product(
    "Developer tool · on npm · live playground",
    "ccwatts",
    "ccwatts estimates the electricity your Claude Code use consumes, as a sourced range and never a single number. It reads the logs Claude Code already keeps on your machine. I did the research, the product calls, the method and the build.",
    [("1.3–30.5 kWh", "range on the sample data, never one number"), ("0", "network requests, enforced by a test"), ("30+", "test files, CI on every change"),
     ("MIT", "code open, methodology public")],
    [
        ("The problem", "<p>Developers run AI agents all day and almost nobody can see the electricity behind it. Providers don't publish energy per token, and public estimates disagree by about 10x. "
         "In 2026 the climate scientist Zeke Hausfather worked out his own Claude Code use by hand, at about 170 kWh over eight weeks. Existing log tools counted tokens and cost, not energy.</p>"),
        ("What I built", '<ul class="clean"><li><b>One command:</b> electricity for the last 30 days, an everyday comparison, and the split by model, token type and project.</li>'
         "<li><b>A playground in the browser:</b> opens on labeled sample data, needs no install, and parses your own logs on the page without uploading them.</li>"
         "<li><b>A history that lasts:</b> Claude Code deletes old logs, so ccwatts keeps its own daily counts, and can export them or make a shareable card.</li>"
         "<li><b>Inside Claude Code:</b> the same CLI ships as a plugin, so you can check usage without leaving a session.</li></ul>"
         + shots(("ccwatts-laptop.webp", "The ccwatts playground on a laptop, sample data: 8.5 kWh for the last 30 days with a plausible range of 1.3 to 30.5 kWh and a daily chart.", 1280, 1060, "The playground, 30 days of sample data. Open the image to read it at full size."),
                 note="Synthetic sample data, not anyone's real usage.")),
        ("How the estimate works", "<p>Energy is tokens times an energy cost per token, by model family and token type. Every parameter has a low and a high bound, a source and a date, and the bounds combine into the range you see. "
         "The least certain assumption is what a cache read costs, which matters because cache reads are usually 90%+ of an agent's tokens. The method uses 10% of fresh input and tests 1% to 25%, and the playground has a \"What if?\" slider for it.</p>"
         "<p>Published figures from Google and Microsoft, and Hausfather's 170 kWh, run as unit tests.</p>"),
        ("Product calls", '<ul class="clean"><li><b>Dev tool first.</b> I started on an enterprise carbon feed, found an established player already publishing a method, and pivoted to the individual developer.</li>'
         "<li><b>Honest numbers.</b> Public estimates vary by an order of magnitude, so it always shows a range and a public methodology.</li>"
         "<li><b>Privacy is the trust story.</b> No network calls, no telemetry, counts only, no prompt or code content, and no mobile app because the data lives on laptops.</li></ul>"),
        ("Proof", proof_grid([
            ("Privacy, enforced", "The web page's Content-Security-Policy is default-src 'none', and a test confirms zero requests in a real browser."),
            ("Tested", "30+ test files and CI on every change."),
            ("Open", "MIT license for the code, CC BY 4.0 for the methodology and parameters."),
            ("On npm", "Published as ccwatts and runnable with npx."),
        ])),
        ("Try it", code_block("npx ccwatts --demo", label="Sample data, no logs needed (Node 22+):")
         + code_block("npx ccwatts", label="Your own Claude Code logs:")
         + code_block("/plugin marketplace add holroydchase-afk/ccwatts", label="As a Claude Code plugin:")),
        ("Status and what's next", "<p>The CLI and the playground are live. 0.2.0 is finished and waiting on my npm publishing setup. It adds an opt-in view of your own work rhythm and an opt-in bedtime nudge, both counts only and local.</p>"),
    ],
    links=[("Try the live playground", "/ccwatts/"), ("View on GitHub", f"{GITHUB}/ccwatts")],
    accent="#F0AE4E",
    feature='<p class="eyebrow">The check</p><h2>Same question as a climate scientist, and the ranges overlap.</h2>'
            + range_viz([("Hausfather, by hand", 70, 330, 170, "70–330 kWh, about 170", "a"),
                         ("ccwatts, same case", 32, 678, 194, "32–678 kWh, central 194", "b")], [10, 100, 1000], 10, 1000,
                        "Eight weeks of heavy Claude Code use, log scale. ccwatts' range is wider on purpose. The token mix is illustrative because Hausfather's exact counts aren't published (METHODOLOGY.md).")
            + '<p class="go"><a class="btn" href="https://github.com/holroydchase-afk/ccwatts/blob/main/METHODOLOGY.md">Read the methodology</a></p>',
    shot=("ccwatts-phone.webp", "The ccwatts playground on a phone, sample data: 8.5 kWh over 30 days, with a plausible range of 1.3 to 30.5 kWh.", 600,
          "Sample data: 8.5 kWh over 30 days, range 1.3 to 30.5."),
)

energy = product(
    "Family app · in active development",
    "Energy Scanner",
    "Bedtime had become a nightly negotiation. I built a routine that ends with a neutral machine, not a parent, deciding it's time to sleep.",
    [("Routine", "steps first, scan as the finale"), ("2 scans", "palm pad, or a photo with a live aura"),
     ("On-device", "photos never leave the phone"), ("Grey", "a grown-up switch makes every scan read sleepy")],
    [
        ("The problem", "<p>Bedtime with my kids had become a nightly negotiation. A parent saying \"it's time\" starts the argument; a neutral machine saying it takes the argument off the parent.</p>"),
        ("What I built", '<ul class="clean"><li><b>A routine first:</b> kids tick off their steps (bath, PJs, teeth, potty, book), then scan.</li>'
         "<li><b>Palm scan:</b> press and hold the pad until the ring fills.</li>"
         "<li><b>Photo scan:</b> take or upload a photo and the child's energy glows off them as an animated aura, softer and slower when sleepy. Grown-ups can save or share it.</li></ul>"),
        ("How it works", "<p>The reading is a color from Rainbow (far too energetic for sleep) down to Grey (time to recharge). It never reads Rainbow once every step is done, and a grown-up switch makes every scan read sleepy. The photo scan runs entirely on the phone with a person-segmentation model (MediaPipe) and a GPU shader.</p>"),
        ("Product calls", '<ul class="clean"><li><b>Routine first.</b> A scan alone wears off, so it is the reward at the end of real steps.</li>'
         "<li><b>Privacy before camera.</b> Kids' faces should never go to a cloud model, so the camera waited until the photo scan could run on the phone. No server, no account, no tracking.</li>"
         "<li><b>An illustrated sample person.</b> Anyone can see the aura without a photo, and no real person's photo is ever published.</li></ul>"),
        ("Proof", proof_grid([
            ("On-device", "Photos never leave the phone; the page is locked so it can only talk to its own origin."),
            ("Tested", "10+ test files, including end-to-end."),
            ("Documented", "A case study in the repo covers the constraints and decisions."),
        ])),
        ("Try it", "<p>Open the app and use the sample person to see the aura, or run the palm scan.</p>"),
        ("Status and what's next", "<p>Live. It started as a palm-scan prototype my kids tested at bedtime; the photo scan came once it could stay on the phone. Next is a copy pass before I call it done.</p>"),
    ],
    links=[("Try the live app", "/energy-scanner/"), ("View on GitHub", f"{GITHUB}/energy-scanner")],
    shot=("energy-scanner-phone.webp", "Energy Scanner on a phone at 7:42 PM: three of five bedtime steps done (bath, PJs, teeth) and the palm scanner ready.", 546),
)

crew_clock = product(
    "Field app · live demo",
    "Crew Clock",
    "A small rural crew tracked hours on paper and memory, on cheap phones with weak signal, so pay disputes came down to whose story you believed. Crew Clock makes every punch a record both sides can trust.",
    [("3 taps", "to clock in, even with no signal"), ("Signed", "every punch is signed on the phone"),
     ("Fair", "the geofence flags a punch, never blocks it"), ("Free tiers", "cover the beta, per the setup doc")],
    [
        ("The problem", "<p>My dad runs a small construction crew on rural job sites, often with one bar of signal or none. Hours lived on paper and memory, so a pay dispute came down to whose story you believed. He needed to know who showed up, where and when, without tracking anyone all day.</p>"),
        ("What I built", '<ul class="clean"><li><b>Three-tap clock-in</b> on the phones the crew already owns, saved on the phone with no signal and sent later.</li>'
         "<li><b>A boss view:</b> a map and a Today list of who is on the clock, plus a weekly timesheet as a CSV with names, dates, times and hours, no GPS.</li>"
         "<li><b>Encrypted crew chat</b> (MLS).</li></ul>"),
        ("How it works", "<p>The phone saves the time and location at the tap. Each phone signs every punch with a key that can't be copied off the phone and chains it to the one before, so a changed time can be caught. "
         "In the demo the boss's Today list checks every punch in the browser, and a Try tampering button shows a changed one in red.</p>"
         "<p><b>The limit:</b> that Verified line is demo only today. In the crew app the server checks the signatures, and showing the check on the boss's screen needs the phones' public keys there.</p>"),
        ("Product calls", '<ul class="clean"><li><b>Never block a clock-in.</b> Bad GPS or no signal means a photo or a flag for the boss, never "you can\'t clock in."</li>'
         "<li><b>A fair geofence.</b> Phone GPS can be off by a lot in the hills, so the app counts that error in the worker's favor.</li>"
         "<li><b>Location only at the tap, and only with consent.</b> No background tracking, each worker agrees once, and tests check that no other screen reads location.</li></ul>"),
        ("Proof", proof_grid([
            ("Tested", "40+ test files, run in CI."),
            ("Privacy contract", "A written privacy contract in the repo, with consent records that are never edited."),
            ("Open", "MIT-licensed code on GitHub."),
            ("Built to be cheap", "The setup doc says every service used has a free tier that covers a beta."),
        ])),
        ("Try it", "<p>Open the demo and tap Travis K. to clock in as a worker. Turn on No signal to see the offline queue, then tap Not you? and choose Sam W. to see the boss's view.</p>"),
        ("Status and what's next", "<p>The demo runs the real app on a made-up crew. The crew's own app is getting ready for a two-week beta with five workers; it has not started.</p>"),
    ],
    status_note="The demo uses a made-up crew and job sites, and it never asks for your real location unless you turn that on. Everything stays in your browser.",
    links=[("Try the live demo", "/crew-clock/"), ("View on GitHub", f"{GITHUB}/crew-clock")],
    shot=("crew-clock-phone.webp", "Crew Clock on a phone, made-up crew: the boss's Today list with all punches verified, one worker not in yet, and who is on site.", 600),
)

# Charlie intake (Oct 29): copy from Charlie's positioning pass; facts trace to the charlie repo README and HANDOFF.md.
charlie = product(
    "Investing tool · paper trading · demo live",
    "Charlie: Invest in What You Know",
    "Most trading apps start from the trade, so beginners act on hype instead of businesses they understand. "
    "Charlie starts from the person: it maps what you already know to companies, then offers the most conservative way to act on one.",
    [("1–3", "trade ideas a day, one per sector"), ("Paper", "never places a real order"),
     ("Every trade", "max loss, breakeven and an exit plan"), ("360+", "tests behind the engine")],
    [
        ("The problem", "<p>Most trading apps start from the trade, so beginners act on hype instead of businesses they understand. A new investor learning options needs ideas from companies their own job and life already taught them.</p>"),
        ("What I built", '<ul class="clean"><li><b>Profile:</b> a resume, interests and brands become ranked sectors, each with the evidence behind it.</li>'
         "<li><b>Today:</b> 1-3 ideas, each with the exact trade, chance of profit, max loss in dollars, breakeven, a payoff chart and an exit plan.</li>"
         "<li><b>Paper portfolio:</b> one click opens a paper position, marked to current prices, and it is flagged when its exit plan says to act.</li></ul>"),
        ("How it works", "<p>Companies in your circle of competence are scored against a Charlie Munger-style checklist. The risk slider starts conservative (covered calls and cash-secured puts) and widens only when you choose. Uncovered calls and same-day options are never offered.</p>"
         "<p><b>The limit:</b> the demo uses a fictional person and simulated prices. The local app can use free live data and falls back to demo data, and its badge says Demo data whenever numbers are simulated.</p>"),
        ("Product calls", '<ul class="clean"><li><b>Person before trade.</b> Ideas come only from sectors the profile supports, and each card says why it is in your circle.</li>'
         "<li><b>Safety in code, not copy.</b> Position sizing and banned strategies are enforced and tested in the engine, not left to a disclaimer.</li>"
         "<li><b>Paper only.</b> Charlie never places real orders and is not financial advice.</li></ul>"),
        ("Proof", proof_grid([
            ("Tested", "360+ unit and end-to-end tests, with CI on every change."),
            ("Demo checked", "A repo check fails the demo build if it needs keys or hosts beyond the Pyodide CDN, or loses its strict content security policy."),
            ("Local first", "The local app answers only to localhost and refuses writes from other sites."),
            ("Documented", "Decision records and a research log in the repo."),
        ])),
        ("Try it", "<p>Open the demo. It turns a fictional resume into paper trades in your browser, with no sign-up. Reset demo clears it.</p>"),
        ("Status and what's next", "<p>The demo is live and the engine runs in the browser with Pyodide. The next feature (an earnings check or paper trading through a broker) has not been chosen.</p>"),
    ],
    status_note="The demo turns a fictional resume into paper trades on simulated prices, kept only in your browser: no sign-up, and Reset demo clears it. Not financial advice.",
    links=[("Try the live demo", "/charlie/"), ("Code on GitHub", f"{GITHUB}/charlie")],
    shot=("charlie-phone.webp", "Charlie's Today screen on a phone: the top paper-trade idea with its score, chance of profit, max loss and payoff chart, above the line &quot;Not financial advice. Paper trading only.&quot;", 649),
)

# The studio story (WEB-M6.1). Facts trace to studio-agents, pm-tools STUDIO-STATUS.md and the Atlas Story logs.
# No schedule ids, project names from private chats, or anyone but Chase.
STUDIO_AGENTS = [
    ("Staff PM", "starts from the bet, writes testable criteria, cuts scope, and runs go/no-go gates."),
    ("QA (tests first)", "turns each criterion or bug into a failing test before anyone writes a fix."),
    ("Engineer", "makes that test pass in one small, reversible PR, and never merges or deploys on its own."),
    ("UX reviewer", "reviews every screen and word as the least tech-savvy person who will use it, on a real phone width."),
    ("Privacy and security", "holds each product to its own promise, like \"logs never leave the laptop\" or \"photos never leave the phone\"."),
    ("Positioning", "keeps a register of what's true today, so no page or post claims more than the product does."),
]

# Agent scoreboard (agent upgrade 3 of 3). Scores come from studio-agents plugins/studio/evals (claude plugin eval);
# update tools/scoreboard.json from that README, never by hand-tuning. tools/check_site.py checks the page matches it.
SCOREBOARD = json.loads((ROOT / "tools/scoreboard.json").read_text())


def scoreboard_html(sb):
    rows = "".join(
        f'<tr><th scope="row">{r["agent"]}</th><td>{r["task"]}</td>'
        f'<td class="num">{r["with"]}/{r["runs"]}</td><td class="num">{r["without"]}/{r["runs"]}</td></tr>'
        for r in sb["evals"])
    return ('<div class="table-scroll"><table class="scoreboard"><caption>Agent evals, ' + sb["as_of"] + '. Tasks passed with the agent and with a plain session.</caption>'
            '<thead><tr><th scope="col">Agent</th><th scope="col">Fixed task</th><th scope="col" class="num">With agent</th><th scope="col" class="num">Without</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            f'<p class="small">One run per arm, judged by fixed checks plus a model grader. <a href="{sb["source"]}">The tasks and graders are on GitHub</a>. '
            "Rows with more than one task count tasks passed. On the QA recall row, a plain session spotted most gaps but never proved one with a failing test. "
            "Two single tasks don't yet separate the agent from a plain session, so harder versions are next.</p>")


studio = product(
    "The studio behind the work",
    "How I run a small AI product studio.",
    "Every product here began as a single AI conversation. By the fifth, I was the only thing connecting them. "
    "This is how I turned that into a studio: specialist agents with defined lanes, a coordinator above them, and me as product owner.",
    [("6", "shared agents, one file each"), ("5", "products, each with its own project"), ("2:15am", "unattended nightly builds"),
     ("1 file", "per repo says where the work stands")],
    [
        ("One chat per product", "<p>It started simply: describe a problem from my own life in a chat and have a working page that evening. "
         "That worked well enough to scale, and scaling is where it broke. Each chat lost what the others knew. I was restating rules, "
         "carrying decisions between windows, and finding two chats solving the same problem two different ways. "
         "The constraint wasn't the AI. It was me, as the only shared memory.</p>"),
        ("Specialists with lanes", "<p>The first fix came from how strong product teams work: give each role one clear job. "
         "I codified the agents I kept recreating by hand, made them product-agnostic, and moved them into one shared library that every repo syncs from.</p>"
         '<ul class="clean">' + "".join(f"<li><b>{n}:</b> {d}</li>" for n, d in STUDIO_AGENTS) + "</ul>"
         "<p>None is tied to a product. Each reads the repo it's working in first: its hard rules, its story and its current state. "
         "The same staff PM agent works on a kids' bedtime app and an energy CLI, and an improvement to one agent lands everywhere. "
         "On the family photo app, this review loop caught a co-parent data leak before any real user saw it.</p>"),
        ("A coordinator, not another builder", "<p>The more important decision was that one project should build nothing. "
         "Each product has its own project that owns its code. Above them, a coordinator, the product studio, holds the view across all of them: "
         "what moved, what stalled, what needs my decision, and where the portfolio stands.</p>"
         "<p>It mirrors what happens when a team outgrows one person: "
         "the job shifts from doing the work to designing the system that keeps it on track.</p>"),
        ("The operating system around it", '<ul class="clean">'
         "<li><b>One handoff file per repo.</b> Every repo keeps a HANDOFF.md: what's done, what's in progress, the exact next step, and what's blocked. "
         "Every session reads it first, and a check fails any pull request that makes progress without updating it.</li>"
         "<li><b>One status list across the studio.</b> A single page lists what's done and what's waiting on me. Anything done is never raised again, and anything waiting is never asked twice.</li>"
         "<li><b>The repo decides who owns the work.</b> A change to a product's repo belongs to that product's project. Anything else goes to the studio. "
         "A project that needs a change it doesn't own writes a short intake, and the owner does the work. Routing never needs my judgment.</li>"
         "<li><b>Overnight shifts.</b> Each product runs an unattended build at 2:15am, timed just after my usage limit resets. One night took ccwatts from a log parser to a working dashboard and playground in seven small PRs.</li>"
         "<li><b>A morning digest.</b> At 6:30 I read one short summary: what shipped overnight, what's blocked, and the one thing that needs me today.</li>"
         "<li><b>A story log.</b> Every notable call goes into a running log as it happens, which is the source for this page.</li></ul>"),
        ("My job became the product owner", "<p>I don't review the code line by line. I review the pull request descriptions: what changed and why, how it was tested, "
         "and which decision is mine. The agents write for that reader, so a clear description is part of the deliverable.</p>"
         "<p>Nothing reaches a live site or a user without me. Agents open draft pull requests and stop. "
         "My evenings shifted from writing prompts to making decisions: approve, cut, or return it with one sentence of direction. "
         "In one recruiter-ready sprint, three review rounds found 21 issues in ccwatts, and every one was fixed test-first across eight small draft PRs overnight.</p>"),
        ("How I know the agents work", "<p>An agent saying it ran the tests isn't evidence. Two checks turn that claim into something I can verify.</p>"
         '<ul class="clean">'
         "<li><b>Every credit is checked against a log.</b> A hook records each time a session hands work to an agent. "
         "A pull request that credits an agent with no logged run fails CI, and when QA ran, CI reruns the test suites three times on its own. "
         "On its first day it failed one of my own pull requests.</li>"
         "<li><b>Every agent is scored.</b> Each one has fixed tasks with known answers, run with the agent and without it, "
         "so a change to an agent's instructions gets a score before it reaches any product.</li></ul>"
         + scoreboard_html(SCOREBOARD)),
        ("What I took from it", '<ul class="clean">'
         "<li><b>Write the rule down once.</b> A hard rule in the repo is followed by every session. One stated only in chat is gone by the next.</li>"
         "<li><b>One source of truth per thing.</b> When status lived in three places, it drifted in three directions.</li>"
         "<li><b>Make every ask one step.</b> My time is the scarcest resource in the studio, so every request is a link, a paste box or a one-word choice.</li>"
         "<li><b>Credibility comes from candor.</b> Agents say \"untested\" when they couldn't check something, and sample data says so everywhere.</li></ul>"),
    ],
    links=[("See the agents on GitHub", f"{GITHUB}/studio-agents"), ("See the Studio Console", "pm-tools.html")],
)

pm_tools = """<div class="read">
<p class="eyebrow">The system behind it</p>
<h1>The console I use to direct my agent team.</h1>
<p class="lede">When agents ship faster than I can read, my attention becomes the scarce resource. I built the console to spend it on my goals first.</p>
<p>I run a team of AI agents across several products: a staff PM, QA, an engineer, a UX reviewer, privacy and security, and positioning. By October their pull requests and handoff notes arrived faster than I could read them, and I was losing hours to work that felt urgent but served no goal.</p>
<div class="cta"><a class="btn primary" href="/pm-tools/console/">Open the Studio Console</a></div>
<p>The live page shows real numbers. In its first week, most of my agents' work matched no goal, which is the problem it exists to catch. Job-search progress is kept private.</p>
<h2>What it shows</h2>
<ul class="clean"><li><b>Focus:</b> my three or four goals, where this week's effort went, and any work that served no goal, flagged as a possible rabbit hole.</li>
<li><b>Call Sheet:</b> everything waiting on my decision, each reduced to one step.</li>
<li><b>Build Slate:</b> each product's stage and health.</li>
<li><b>Horizon Board:</b> milestones in Now, Next, Later and Done.</li>
<li><b>Agent Roster:</b> which agents ran on each pull request and whether it passed its gates.</li></ul>
<h2>How it works</h2>
<p>The page rebuilds every hour from the studio's public GitHub repos: each product's HANDOFF.md, its open pull requests, intake issues and agent run logs. It has no database and no login. I built it for one job, a product owner directing an agent team, so it has no team accounts or permissions.</p>
<p>It went live on October 31 with a success test set in advance: five weekdays in a row run from the Call Sheet without opening a handoff file. If that hasn't happened by November 14, I'll change it or retire it.</p>
<h2>What it replaced</h2>
<p>Before the console I ran two small apps, Build Slate and a near-term roadmap. Both were organized by product. Neither showed whether the week's work served a goal or which calls were waiting on me. Their sample-data demos are still up: <a href="/pm-tools/build-slate/">Build Slate</a> and <a href="/pm-tools/roadmap/">the roadmap</a>.</p>
<p>Source for the console, both earlier apps and the PM templates below is on <a href="https://github.com/holroydchase-afk/pm-tools">GitHub</a>.</p>
<h2>Decisions that leave a trail</h2>
<ul class="clean"><li><b>Decision log:</b> every call records why, and what it beat.</li>
<li><b>Persona check:</b> before a product decision is final, each persona gets a green or red with a one-line reason. CI fails if a decision file skips it.</li>
<li><b>Anchors:</b> a few principles every feature is checked against, like "anxiety-less" and "stays on US soil."</li>
<li><b>Post mortems:</b> each one adds a rule, so the same mistake doesn't happen twice.</li></ul>
<h2>The team it directs</h2>
<p>Each agent owns one lane, every repo keeps a handoff file, and nothing ships without my review. <a href="studio.html">The story of how the studio came together</a>.</p>
</div>"""

about = f"""<div class="intro">{HEADSHOT}<div class="read">
<p class="eyebrow">About</p>
<h1>From solar engineering to product leadership.</h1>
<p class="lede">I started out designing solar systems and ended up building the software that prices, sells and finances them. Pricing, payments and point-of-sale lending are my core expertise. I design my own screens and prototype with current AI tools, so ideas reach users as working software, not slides.</p>
</div></div>
<div class="read">
<h2>The path</h2>
<ol class="timeline">
<li><b>Solar engineer, Palmetto (2016).</b> Designed 2,000+ residential and commercial PV systems and replaced 75% of on-site surveys with virtual ones, saving $80K a year.</li>
<li><b>First PM, then Senior PM, then Director of Product, Palmetto (2017–2019).</b> Launched the sales enablement platform, built Alchemy (design, point of sale and project management with real-time credit decisions), and launched a machine-learning lead marketplace supporting 11,500+ consultations a month.</li>
<li><b>Founder, Bigfoot Energy (2019–2020).</b> A smart-home and clean-energy company in Charleston, WV.</li>
<li><b>Product Owner, AGDATA (2020).</b> Scoped a master data platform to replace 8+ legacy pricing and rebate systems.</li>
<li><b>PM, then Senior PM, ADT (2020–2023).</b> First PM for ADT's solar division. Built the credit-check and offer engine (35,000+ applications a month), a lender allocation platform, a channel-partner pricing platform, and the Lowe's in-store program. Shipped to 5,000+ reps.</li>
<li><b>Staff PM, Patter AI (2023–2026).</b> A real-time pricing engine across loans, leases and PPAs, rep-guided checkout, AI conversation analysis that found 40% of a client's reps going off-script, a rules engine that cut lender onboarding from 4 weeks to 1 week, and an agentic pipeline that cut new lender integrations from a 2-week sprint to 1–2 days.</li>
<li><b>Jan 2026 to now: career break for family caregiving, building with AI.</b> I prototype tools that fix problems in my own life (bedtime, the job search, family photos, the energy my AI use takes) and onboard real people to each one. I'm not raising or selling; I'm looking for my next full-time role.</li>
</ol>
<h2>What I care about</h2>
<ul class="clean"><li>Checkout, pricing and payments that feel simple to the person at the kitchen table.</li>
<li>Clean energy and climate, rooted in a WVU degree in Sustainable Design.</li>
<li>Privacy that's strong underneath and obvious on the surface.</li>
<li>Steady, focused teams that ship.</li></ul>
<h2>Get in touch</h2>
<p>I'm looking for a senior or staff product role, remote. The best way to reach me is <a href="{LINKEDIN}">LinkedIn</a>.</p>
</div>"""

# Resume: mirrors pmo/story/resume-2026-10.md (Oct 2026). Never add phone or email; LinkedIn is the contact route.
# One short story per company, no bullets (Chase, Oct 23): the problem, what I did, the outcome. Every number traces to the resume.
# (company, [(title, dates)], [paragraphs]); a company with several roles gets one paragraph per stage.
JOBS = [
    ("Career break", [("Family caregiving", "Jan 2026 – present")], [
        "Stepped back from employment for family caregiving. Shipped ccwatts (open source) and am building Hearth, a private family photo app, with a team of AI agents, tests first. Both are on this site with the code public."]),
    ("Patter AI", [("Staff Product Manager", "Jan 2023 – Jan 2026 · Remote")], [
        "Patter's clients sell solar and home services, and their reps had to price loans, leases and PPAs on the spot. "
        "I led one real-time pricing engine across all three for 4 clients, and a rep-guided checkout that shows the payment impact of each add-on. "
        "Its AI conversation analysis found 40% of one client's reps going off script, and coaching rose from <strong>about 4 sessions a month to about 1 a day</strong>.",
        # The B2B contract-pricing dollar figures stay off until Chase OKs publishing them (case-study doc [check]).
        "A lender rules engine cut onboarding a new lender <strong>from 4 weeks to 1 week</strong>, and I integrated 6+ lenders. "
        "An agentic pipeline read each lender's API documents and, with an engineer in the loop, built, tested and fixed the integration, cutting a new one from <strong>2 engineers for a 2-week sprint to 1–2 days</strong>. "
        "Patter's agents ran on a LangGraph platform, and I defined a trust ladder for 6 of them, from human-run to AI with human observation, with audit logs, undo and approvals. "
        "Every model call went through one shared gateway with rate limits, failover and spend tracking that routed each use case by accuracy and cost."]),
    ("ADT Solar", [("Senior Product Manager", "Nov 2021 – Jan 2023"), ("Product Manager", "Oct 2020 – Nov 2021")], [
        "I joined as the first PM for ADT's solar division, where complex solar contracts were slow to review. "
        "A rep-guided checkout cut contract review <strong>about 60%</strong>. "
        "A training app for new reps cut training from <strong>6 weeks to 2</strong> and tripled the training team's onboarding capacity without adding trainers.",
        "As senior PM I built the credit-check and offer engine: 5 lenders, <strong>35,000+ applications a month</strong>, and 110% year-over-year sales growth. "
        "I built the lender allocation platform (GoodLeap, Sunlight, Mosaic, Dividend and others). "
        "I also led a channel-partner platform with redline and tiered pricing for 4+ partners, was technical lead for the Lowe's in-store solar and security program, "
        "and scaled the post-merger platform to 400,000+ consultations a year, with releases to 5,000+ reps' iPads."]),
    ("AGDATA", [("Product Owner", "Jun – Oct 2020")], [
        "Pricing and rebate data for clients such as Bayer was spread across 8+ legacy systems. "
        "I led discovery for a master data management platform to consolidate them."]),
    ("Bigfoot Energy", [("Founder", "Oct 2019 – Jun 2020 · Charleston, WV")], [
        "I founded a smart-home and clean-energy company in Charleston, West Virginia."]),
    ("Palmetto", [("Director of Product", "Jan – Jun 2019"), ("Senior Product Manager", "Feb 2018 – Jan 2019"),
                  ("Product Manager", "Jun 2017 – Feb 2018"), ("Senior Solar Engineer", "Feb 2016 – Jun 2017")], [
        "I started as a solar engineer and designed 2,000+ PV systems. "
        "Virtual surveys replaced 75% of site visits, <strong>saving $80K a year</strong>.",
        "As Palmetto's first PM I digitized its pricing models, then built Alchemy, a design, point-of-sale and project management platform with real-time GoodLeap and Sunlight credit. "
        "As Director of Product I launched a machine-learning lead marketplace on about 300 data points, running <strong>11,500+ consultations a month</strong>."]),
]

resume = f"""<div class="read resume">
<p class="eyebrow">Resume · Charlotte, NC · open to remote roles</p>
<h1>Chase Holroyd</h1>
<p class="lede">Staff Product Manager · Pricing, Payments &amp; Point-of-Sale Lending</p>
<p>8+ years building point-of-sale financing and pricing products: rep-guided checkout, dealer-fee and redline pricing engines, and real-time loan, lease and PPA payments. 14+ lender integrations; a credit and offer engine at 35,000+ applications a month; lender allocation across GoodLeap, Sunlight, Mosaic and Dividend.</p>
<p class="contact">Contact: <a href="{LINKEDIN}">linkedin.com/in/chase-holroyd</a> · Site: <a href="index.html">chaseholroyd.com</a></p>
<h2>Experience</h2>
""" + "".join(
    f'<section class="job"><h3>{c}</h3>'
    + "".join(f'<p class="when"><span class="role">{t}</span><span class="sep"> · </span><span class="dates">{d}</span></p>' for t, d in roles)
    + "".join(f"<p>{para}</p>" for para in paras) + "</section>"
    for c, roles, paras in JOBS
) + """
<h2>Education</h2>
<p>B.A., Sustainable Design, West Virginia University, 2014.</p>
<h2>Skills</h2>
<p>Pricing and payments, lending, product strategy, AI/ML (LLMs, RAG, multi-agent orchestration, conversation intelligence), APIs, rules engines, SQL, Figma.</p>
</div>"""

notfound = """<div class="read"><p class="eyebrow">404</p><h1>That page isn't here.</h1>
<p class="lede">It may have moved. The <a href="index.html">work page</a> lists everything.</p></div>"""

PAGES = [
    ("index.html", "Work", "Chase Holroyd, staff product manager for pricing, payments and point-of-sale lending. Open to remote senior and staff PM roles.", home),
    ("family-photos.html", HEARTH, f"{HEARTH} (working name): a private family photo app for split families and grandparents, with a chosen audience on every post.", family),
    ("role-radar.html", "Role Radar", "An AI job-search radar that scans about 190 company boards on request.", role_radar),
    ("ccwatts.html", "ccwatts", "Estimate the electricity your Claude Code usage consumes, as an honest range.", ccwatts),
    ("charlie.html", "Charlie", "Learn options by paper trading the companies you already understand, with max loss, breakeven and an exit plan on every idea.", charlie),
    ("energy-scanner.html", "Energy Scanner", "A bedtime routine for kids that ends with an energy scan: a palm pad, or a photo with an on-device aura.", energy),
    ("crew-clock.html", "Crew Clock", "A phone time clock for small rural crews: three taps to clock in, even with no signal, and every punch signed.", crew_clock),
    ("studio.html", "The studio", "How Chase runs a small AI product studio: shared agents with lanes, a coordinator, overnight shifts, and a product owner who reviews the PRs.", studio),
    ("pm-tools.html", "Studio Console", "The goal-first console Chase uses to direct a team of AI agents across several products, rebuilt hourly from public GitHub repos.", pm_tools),
    ("resume.html", "Resume", "Chase Holroyd's resume: staff product manager for pricing, payments and point-of-sale lending.", resume),
    ("about.html", "About", "Chase Holroyd's path from solar design to product management and AI.", about),
    ("404.html", "Not found", "Page not found.", notfound),
]

if __name__ == "__main__":
    for slug, title, desc, body in PAGES:
        (ROOT / slug).write_text(page(slug, title, desc, body), encoding="utf-8")
    urls = "".join(f"<url><loc>{SITE}/{'' if s == 'index.html' else s}</loc></url>\n"
                   for s, *_ in PAGES if s != "404.html")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      f"{urls}</urlset>\n", encoding="utf-8")
    # Crawlers must be allowed in to see each page's noindex, so robots.txt only drops the sitemap line.
    sitemap_line = "" if NOINDEX else f"Sitemap: {SITE}/sitemap.xml\n"
    # AI training and answer bots are shut out (Chase, Oct 26). Well-behaved bots obey; it isn't a lock.
    ai_block = "".join(f"User-agent: {bot}\n" for bot in AI_BOTS) + "Disallow: /\n\n"
    (ROOT / "robots.txt").write_text(f"{ai_block}User-agent: *\nAllow: /\n{sitemap_line}", encoding="utf-8")
    print(f"Wrote {len(PAGES)} pages to {ROOT}")
