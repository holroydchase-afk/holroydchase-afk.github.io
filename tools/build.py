#!/usr/bin/env python3
"""Builds the static pages for chaseholroyd.com from the PAGES content below.

Run from the repo root: python3 tools/build.py
Each page is plain HTML written to the repo root, so GitHub Pages serves it with no build step.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://chaseholroyd.com"
LINKEDIN = "https://www.linkedin.com/in/chase-holroyd"
GITHUB = "https://github.com/holroydchase-afk"

NAV = [
    ("index.html", "Work"),
    ("pm-tools.html", "How I work"),
    ("about.html", "About"),
]

FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600"
         "&family=Public+Sans:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap")

# Person markup so a search for the name can show the right profile. No email or phone, by rule.
JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfilePage","mainEntity":{"@type":"Person","name":"Chase Holroyd",
"jobTitle":"Staff Product Manager","description":"Staff product manager in pricing, payments and point-of-sale lending, building products with AI agents.",
"url":"https://chaseholroyd.com","image":"https://chaseholroyd.com/assets/share-card.png",
"address":{"@type":"PostalAddress","addressLocality":"Charlotte","addressRegion":"NC","addressCountry":"US"},
"alumniOf":{"@type":"CollegeOrUniversity","name":"West Virginia University"},
"sameAs":["https://www.linkedin.com/in/chase-holroyd","https://github.com/holroydchase-afk"]}}
</script>
"""


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
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
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
<main class="wrap" id="main">
{body}
</main>
<footer class="site"><div class="wrap">
<span>© 2026 Chase Holroyd · Product manager · Charlotte, NC</span>
<span><a href="{LINKEDIN}">LinkedIn</a> · <a href="{GITHUB}">GitHub</a></span>
</div></footer>
</body>
</html>
"""


def product(eyebrow, name, lede, facts, sections, status_note=None, links=None):
    facts_html = "".join(f'<div class="fact"><b>{v}</b><span>{k}</span></div>' for v, k in facts)
    links_html = ""
    if links:
        links_html = '<div class="cta">' + "".join(
            f'<a class="btn{" primary" if i == 0 else ""}" href="{u}">{t}</a>' for i, (t, u) in enumerate(links)
        ) + "</div>"
    secs = "".join(f"<h2>{h}</h2>{c}" for h, c in sections)
    note = f'<p class="note">{status_note}</p>' if status_note else ""
    return f"""<div class="read">
<p class="eyebrow">{eyebrow}</p>
<h1>{name}</h1>
<p class="lede">{lede}</p>
{links_html}
</div>
<div class="facts">{facts_html}</div>
<div class="read">{secs}{note}
<p style="margin-top:40px"><a href="index.html">← All work</a></p></div>"""


CARDS = [
    ("role-radar.html", "Live demo", "Role Radar",
     "A job-search radar that scans about 110 company boards each weekday and turns a good match into a tailored resume in one tap."),
    ("ccwatts.html", "Live playground", "ccwatts",
     "How much electricity does your AI coding agent use? A local tool that answers as an honest range, with every assumption sourced."),
    ("pm-tools.html", "Live demos", "How I run product work",
     "Build Slate, a multi-board roadmap, persona checks enforced in CI, a decision log, and a team of AI agents with defined lanes."),
    ("energy-scanner.html", "Live demo", "Energy Scanner",
     "A bedtime routine for kids that ends in a playful energy scan, so the machine says it's time for bed instead of the parent."),
    ("family-photos.html", "Private beta soon", "Family photo app",
     "Private photo sharing for split families and grandparents who avoid social media. Every post has a visible audience."),
]

# Every number here traces to pmo/story/resume-2026-10.md. Change them only with the resume.
PROOF = [
    ("12,000+", "credit applications a month through the offer engine I led"),
    ("3–5 pts", "dealer fees cut with lender allocation"),
    ("13+", "lender integrations shipped"),
    ("1 mo → 1 wk", "to onboard a new lender, with a rules engine"),
]

home = f"""<div class="read">
<p class="eyebrow">Open to remote senior and staff PM roles</p>
<h1>Staff PM for pricing, payments and point-of-sale lending.</h1>
<p class="lede">8+ years building credit, offer and pricing engines for lenders, dealers and about 5,000 sales reps. Staff PM at Patter AI; before that ADT and Palmetto.</p>
<div class="cta"><a class="btn primary" href="{LINKEDIN}">Connect on LinkedIn</a><a class="btn" href="about.html">My path</a></div>
</div>
<div class="facts">""" + "".join(f'<div class="fact"><b>{v}</b><span>{k}</span></div>' for v, k in PROOF) + """</div>
<div class="read">
<h2>Since Jan 2026: independent product work</h2>
<p>Between roles, I'm building AI-agent tools in public to stay sharp on how LLM products ship. Not raising, not selling; ready for a full-time role. Each one runs on sample data, right in your browser.</p>
</div>
<div class="grid">""" + "".join(
    f'<a class="card" href="{h}"><span class="tag">{s}</span><h3>{n}</h3><p>{d}</p></a>' for h, s, n, d in CARDS
) + "</div>"

family = product(
    "Mobile app · building",
    "A family photo app (name coming)",
    "Five family group texts, two divorced-and-remarried families, grandpas on Android and everyone else on iPhone. "
    "I wanted one private place where each photo goes to exactly the people it's meant for.",
    [("Per post", "audience you choose"), ("US", "where photos are stored"), ("0", "ads, trackers or AI training"),
     ("Test-first", "every fix starts as a failing test")],
    [
        ("The problem", "<p>Photos of our kids arrived late, compressed, or not at all, and every send meant worrying about who felt left out. "
         "Existing family apps didn't handle two equal households, and we don't post our kids publicly.</p>"),
        ("What I built", '<ul class="clean"><li><b>Groups and households:</b> share with Everyone, one side of the family, a single house, or an event like a birthday trip.</li>'
         "<li><b>Privacy underneath:</b> database-level access rules, a post you can't see behaves as \"not found\", and photo location data is stripped on the phone.</li>"
         "<li><b>Built for grandparents:</b> large text and tap targets, words under every icon, and invites that work from far away.</li></ul>"),
        ("How I built it", "<p>I ran it like a small team: a staff PM agent writes the spec, a QA agent writes failing tests, an engineer agent makes them pass, "
         "and privacy and UX reviewers sign off. By the second week there were 600+ backend checks and 340 app tests, and a co-parent data leak was caught in review before any real user saw it.</p>"
         "<p>Stack: Expo / React Native, Supabase (Postgres with row-level security), US-hosted storage.</p>"),
        ("What's next", "<p>A private beta with about a dozen family members, mostly grandparents in West Virginia, targeted for late November.</p>"),
    ],
    status_note="The app is being renamed before beta, so this page uses a placeholder name for now. The code is private.",
)

role_radar = product(
    "AI tool · beta",
    "Role Radar",
    "Job searching is mostly finding, filtering and re-typing. I built a radar that does the first two every weekday and turns the third into one tap.",
    [("~110", "company job boards watched"), ("4", "sources merged and de-duplicated"), ("1 tap", "from match to tailored resume"),
     ("< 20 min", "target per fast-lane application")],
    [
        ("How it works", '<ul class="clean"><li>A scheduled agent scans company boards (Greenhouse, Ashby, Lever), ZipRecruiter, Himalayas and job-alert emails.</li>'
         "<li>It filters by my rules (title, remote, comp floor, industries), rates each fit as strong, maybe or stretch with a one-line reason, and flags any role that competes with something I'm building.</li>"
         "<li>Application status updates itself from confirmation and rejection emails, read-only.</li>"
         "<li>One tracker holds everything, and an Apply button starts a resume intake that drafts a tailored version from my career master.</li></ul>"),
        ("Product decisions", '<ul class="clean"><li><b>One tracker, not three.</b> Status lived in three places and drifted, so I retired the old pipeline.</li>'
         "<li><b>Cost-aware by design.</b> Big boards run three days a week, and the scan stops paging as soon as results stop being new.</li>"
         "<li><b>Built to be shared.</b> Filters and profile live in config, so other job seekers can copy it.</li></ul>"),
        ("Stack", "<p>A Claude artifact with a saved database, a weekday scheduled agent, Gmail (read-only) and ZipRecruiter connectors, and a resume-intake skill that fills a Google Docs template.</p>"),
    ],
    status_note="The demo uses made-up jobs, companies and people, never real applications. Changes you make stay in your browser.",
    links=[("Try the demo", "demo/role-radar/")],
)

ccwatts = product(
    "Developer tool · playground live",
    "ccwatts",
    "AI use has an electricity cost, and almost nobody can see theirs. ccwatts reads your local Claude Code logs and estimates the energy your usage consumed.",
    [("Range", "low / central / high, never one number"), ("Local", "logs never leave your machine"), ("Sourced", "every assumption cited"),
     ("Open", "source on GitHub")],
    [
        ("Why it exists", "<p>In 2026 climate scientist Zeke Hausfather estimated his own Claude Code use by hand, at about 170 kWh over eight weeks. "
         "Tools already counted tokens and cost. Nobody had packaged the energy side, so I did.</p>"),
        ("Product calls", '<ul class="clean"><li><b>Dev tool first.</b> I started on an enterprise carbon feed, found an established player already publishing a method, and pivoted to the individual developer.</li>'
         "<li><b>Honest numbers.</b> Public estimates vary by an order of magnitude, so it always shows a range and a public methodology.</li>"
         "<li><b>Privacy is the trust story.</b> No network calls, no telemetry, and no mobile app, because the data lives on laptops.</li></ul>"),
        ("Stack", "<p>A TypeScript monorepo with one shared core used by both the CLI (<code>npx ccwatts</code>) and an offline HTML dashboard.</p>"),
    ],
    links=[("Try the playground", "/ccwatts/"), ("View on GitHub", f"{GITHUB}/ccwatts")],
)

energy = product(
    "Family app · prototype",
    "Energy Scanner",
    "Bedtime was a nightly negotiation. What if a neutral machine said it was time, instead of me?",
    [("Routine", "steps first, scan as the finale"), ("Colors", "each energy level has its own summary"), ("Grey", "a grown-up switch makes every scan read sleepy")],
    [
        ("The idea", "<p>Kids work through their bedtime routine, then step up for an energy scan that returns a color, like grey, yellow or rainbow, with a fun summary. "
         "A neutral \"machine says so\" authority takes the argument off the parent.</p>"),
        ("Decisions so far", '<ul class="clean"><li><b>Routine first.</b> A fake scan alone wears off, so the scan is the reward at the end of real steps.</li>'
         "<li><b>Privacy before camera.</b> Kids' faces shouldn't go to a cloud model, so the camera waits until on-device or no-storage options are settled.</li></ul>"),
        ("Status", "<p>A working prototype my kids are testing at bedtime. The vision-model version gets built only if the novelty holds.</p>"),
    ],
    links=[("Try the demo", "demo/energy-scanner/")],
)

pm_tools = """<div class="read">
<p class="eyebrow">How I work</p>
<h1>A product studio of one, run like a team.</h1>
<p class="lede">I have about an hour a night. These are the tools and rituals that let me ship several products at once without losing the thread. The two apps below are live demos with my real slate and roadmap as of October 2026; anything you change stays in your browser.</p>
<h2>Build Slate</h2>
<p>One board for every product: stage (idea, spec, building, beta, launched, paused), the very next step, and a milestone date. It caps me at five live projects so I go deep, not wide.</p>
<div class="cta"><a class="btn primary" href="/pm-tools/build-slate/">Try Build Slate</a></div>
<h2>Near-term roadmap</h2>
<p>Now, Next, Later and Done lanes with a board per product, owners, session-size estimates and a blocked flag. Any AI session can read and update it by link, so the roadmap stays current without me retyping it.</p>
<div class="cta"><a class="btn primary" href="/pm-tools/roadmap/">Try the roadmap</a></div><p>Source for both apps, plus the PM templates and routines below, is on <a href="https://github.com/holroydchase-afk/pm-tools">GitHub</a>.</p>
<h2>Decisions that leave a trail</h2>
<ul class="clean"><li><b>Decision log:</b> every call records why, and what it beat.</li>
<li><b>Persona check:</b> before a product decision is final, each persona gets a green or red with a one-line reason. CI fails if a decision file skips it.</li>
<li><b>Anchors:</b> a few principles every feature is checked against, like "anxiety-less" and "stays on US soil."</li>
<li><b>Post mortems:</b> each one adds a rule, so the same mistake doesn't happen twice.</li></ul>
<h2>An AI team with lanes</h2>
<p>Specialist agents each own one job: staff PM, QA (tests first), engineer, privacy and security, UX for low-tech users, and marketing. I keep an inventory of every agent's maturity (proven, working, dormant or broken) and decide which to use, mature or retire.</p>
<h2>One hub across projects</h2>
<p>Each project reports into a central product office: products, PM tools, agents, decisions and open loops, so nothing lives only in one chat.</p>
</div>"""

about = f"""<div class="read">
<p class="eyebrow">About</p>
<h1>From rooftops to roadmaps.</h1>
<p class="lede">I started out designing solar systems and ended up building the software that prices, sells and finances them. Pricing, payments and point-of-sale lending are my home turf, and I design my own screens and prototype with the newest AI.</p>
<h2>The path</h2>
<ol class="timeline">
<li><b>Solar engineer, Palmetto (2016).</b> Designed 2,000+ residential and commercial PV systems and replaced 75% of on-site surveys with virtual ones, saving $80K a year.</li>
<li><b>First PM, then Senior PM, then Director of Product, Palmetto (2017–2019).</b> Launched the sales enablement platform, built Alchemy (design, point of sale and project management with real-time credit decisions), and launched a machine-learning lead marketplace supporting 11,500+ consultations a month.</li>
<li><b>Founder, Bigfoot Energy (2019–2020).</b> A smart-home and clean-energy company in Charleston, WV.</li>
<li><b>Product Owner, AGDATA (2020).</b> Scoped a master data platform to replace 8+ legacy pricing and rebate systems.</li>
<li><b>PM, then Senior PM, ADT (2020–2023).</b> First PM for a 3,000-person solar division. Built the credit-check and offer engine (12,000+ applications a month), a lender allocation platform that helped cut dealer fees 3–5 points, a channel-partner pricing platform, and the Lowe's in-store program. Shipped to about 5,000 reps.</li>
<li><b>Staff PM, Patter AI (2023–2026).</b> A real-time pricing engine across loans, leases and PPAs, rep-guided checkout, AI conversation analysis that found 40% of a client's reps going off-script, and a rules engine that cut lender onboarding from about a month to a week.</li>
<li><b>Since Jan 2026: independent product work.</b> Between roles, I'm building AI-agent tools in public (job search, AI energy, PM operations) to stay sharp on how LLM products ship. Not raising, not selling; ready for a full-time role.</li>
</ol>
<h2>What I care about</h2>
<ul class="clean"><li>Checkout, pricing and payments that feel simple to the person at the kitchen table.</li>
<li>Clean energy and climate, rooted in a WVU degree in Sustainable Design.</li>
<li>Privacy that's strong underneath and obvious on the surface.</li>
<li>Calm teams that ship.</li></ul>
<h2>Get in touch</h2>
<p>I'm looking for a senior or staff product role, remote. The best way to reach me is <a href="{LINKEDIN}">LinkedIn</a>.</p>
</div>"""

notfound = """<div class="read"><p class="eyebrow">404</p><h1>That page isn't here.</h1>
<p class="lede">It may have moved. The <a href="index.html">work page</a> lists everything.</p></div>"""

PAGES = [
    ("index.html", "Work", "Chase Holroyd, staff product manager for pricing, payments and point-of-sale lending. Open to remote senior and staff PM roles.", home),
    ("family-photos.html", "Family photo app", "A private family photo app for split families and grandparents, with a chosen audience on every post.", family),
    ("role-radar.html", "Role Radar", "An AI job-search radar that scans about 110 company boards each weekday.", role_radar),
    ("ccwatts.html", "ccwatts", "Estimate the electricity your Claude Code usage consumes, as an honest range.", ccwatts),
    ("energy-scanner.html", "Energy Scanner", "A bedtime routine for kids that ends with a playful energy scan.", energy),
    ("pm-tools.html", "How I work", "The tools and rituals behind a one-person product studio.", pm_tools),
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
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"Wrote {len(PAGES)} pages to {ROOT}")
