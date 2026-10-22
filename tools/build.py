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
    ("resume.html", "Resume"),
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
{'<base href="/">' + chr(10) if slug == "404.html" else ""}<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
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
<span>© 2026 Chase Holroyd · Staff product manager · Charlotte area</span>
<span><a href="{LINKEDIN}">LinkedIn</a> · <a href="{GITHUB}">GitHub</a></span>
</div></footer>
</body>
</html>
"""


def product(eyebrow, name, lede, facts, sections, status_note=None, links=None, shot=None):
    facts_html = "".join(f'<div class="fact"><b>{v}</b><span>{k}</span></div>' for v, k in facts)
    links_html = ""
    if links:
        links_html = '<div class="cta">' + "".join(
            f'<a class="btn{" primary" if i == 0 else ""}" href="{u}">{t}</a>' for i, (t, u) in enumerate(links)
        ) + "</div>"
    secs = "".join(f"<h2>{h}</h2>{c}" for h, c in sections)
    note = f'<p class="note">{status_note}</p>' if status_note else ""
    # One phone screenshot under the lede, sample data only (WEB-M4.7). Source PNGs: 390x844 at 2x, cropped, WebP.
    # shot = (file, alt, height at 300px wide, optional caption). It sits above the fold, so it loads eagerly.
    shot_html = ""
    if shot:
        cap = f"<figcaption>{shot[3]}</figcaption>" if len(shot) > 3 else ""
        shot_html = (f'<figure class="shot"><img src="assets/shots/{shot[0]}" width="300" height="{shot[2]}" '
                     f'alt="{shot[1]}" fetchpriority="high" decoding="async">{cap}</figure>')
    return f"""<div class="hero{" has-shot" if shot else ""}"><div class="read">
<p class="eyebrow">{eyebrow}</p>
<h1>{name}</h1>
<p class="lede">{lede}</p>
{links_html}
</div>{shot_html}
<div class="facts">{facts_html}</div></div>
<div class="read">{secs}{note}
<p class="back"><a href="index.html">← All work</a></p></div>"""


# Career highlights on the home page. Facts trace to pmo/story/resume-2026-10.md; outside links are public pages.
# [check] items wait on Chase (WEB-M5); none of this merges until they're cleared.
CAREER = [
    ("Patter AI", "Staff PM · 2023–2026",
     "An AI-native sales platform for solar and home services. I led one real-time pricing engine across loans, leases and PPAs, "
     "rep-guided checkout that shows the payment impact of each add-on, and a lender rules engine that cut onboarding from about a month to a week.",
     [("See Patter", "https://salespatter.io")]),  # [check] Capterra lists salespatter.io as Patter's site; confirm the URL
    ("ADT Solar", "PM → Senior PM · 2020–2023",
     "First PM for a 3,000-person solar division. I built the credit-check and offer engine (12,000+ applications a month across 5 lenders) "
     "and lender allocation that helped cut dealer fees 3–5 points, shipped to about 5,000 reps.",
     [("Resume", "resume.html")]),
    ("Palmetto", "Engineer → Director of Product · 2016–2019",
     "I was Palmetto's first PM and built Alchemy, its design, proposal and real-time credit platform. Palmetto raised $6M to grow it. "
     "Then I launched a machine-learning lead marketplace at 11,500+ consultations a month.",
     [("Alchemy in the press", "https://techstartups.com/?p=13148"), ("Palmetto today", "https://palmetto.com")]),
]

# The AI journey: each product starts with a problem in Chase's life and its real users. Ordered by how the
# building grew (one prototype page → scheduled agent → open source → an agent team → the system behind it), not by date.
JOURNEY = [
    ("energy-scanner.html", "A one-page prototype", "Energy Scanner",
     "Bedtime with my kids was a nightly negotiation. A prototype they tested at bedtime became a routine that ends in an energy scan, so the machine says it's bedtime instead of me.",
     "[check] Who uses it today, e.g. my kids every night"),
    ("role-radar.html", "A scheduled agent", "Role Radar",
     "Job hunting meant hours of sifting. An agent now reads about 110 company boards each weekday and scores every role with a reason, so I only read the right few.",
     "[check] Who uses it besides me"),
    ("ccwatts.html", "Open source", "ccwatts",
     "I wanted to know what my own AI coding costs in electricity. Nobody had packaged it, so I built a local tool that answers as an honest range.",
     "[check] Who's using it"),
    ("family-photos.html", "A team of AI agents", "Family photo app",
     "Two blended families, five group texts, grandparents on Android. I ran AI agents like a product team (spec, tests first, privacy review) to build one private place for our photos.",
     "Family beta with about a dozen relatives, mostly grandparents, in late November"),
    ("pm-tools.html", "The system behind it", "How I keep it all moving",
     "Five products on about an hour a night only works with a system: one slate, one roadmap, and AI agents with clear lanes. The demos run on a snapshot of my real slate.",
     "[check] OK to say \"about an hour a night\"?"),
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
<h1>A staff PM who builds with AI to fix real problems.</h1>
<p class="lede">For 8+ years I built the pricing, credit and checkout software that sells and finances home solar, at Palmetto, ADT and Patter AI. Lately I've been prototyping with AI to solve problems in my own life, and I'm onboarding real people to each one.</p>
<div class="cta"><a class="btn primary" href="{LINKEDIN}">Connect on LinkedIn</a><a class="btn" href="resume.html">View resume</a></div>
</div>
<div class="facts">""" + "".join(f'<div class="fact"><b>{v}</b><span>{k}</span></div>' for v, k in PROOF) + """</div>
<div class="read"><h2>Career highlights</h2>
<p>Pricing, payments and point-of-sale lending, from the first PM seat to staff.</p></div>
<div class="grid">""" + "".join(
    f'<div class="card career"><span class="tag">{r}</span><h3>{c}</h3><p>{d}</p><p class="links">'
    + " · ".join(f'<a href="{u}">{t}</a>' for t, u in links) + "</p></div>"
    for c, r, d, links in CAREER
) + """</div>
<div class="read"><h2>What I've built with AI</h2>
<p>Each of these started as a problem in my own life. Together they show how my building with AI grew: from one prototype page to a team of agents with tests and reviews. Every demo runs on sample data, right in your browser.</p></div>
<div class="grid">""" + "".join(
    f'<a class="card" href="{h}"><span class="tag">{s}</span><h3>{n}</h3><p>{d}</p><p class="who">{w}</p></a>'
    for h, s, n, d, w in JOURNEY
) + "</div>"

family = product(
    "Mobile app · building",
    "A private family photo app",
    "Five family group texts, two divorced-and-remarried families, grandpas on Android and everyone else on iPhone. "
    "I wanted one private place where each photo goes to exactly the people it's meant for.",
    [("Per post", "audience you choose"), ("US", "where photos are stored"), ("0", "ads, trackers or AI training"),
     ("Test-first", "every fix starts as a failing test")],
    [
        ("The problem", "<p>Photos of our kids arrived late, compressed, or not at all, and every send meant worrying about who felt left out. "
         "Existing family apps didn't handle two equal households, and we don't post our kids publicly.</p>"),
        ("What I built", '<ul class="clean"><li><b>Groups you name:</b> share with Everyone, one side of the family, or an event like a birthday trip. One person can be in several groups.</li>'
         "<li><b>Privacy underneath:</b> photos are encrypted on the phone (AES-256-GCM) before upload, group chat is end-to-end encrypted with MLS (RFC 9420), "
         "database-level access rules make a post you can't see behave as \"not found\", and photo location data is stripped on the phone.</li>"
         "<li><b>No pressure to perform:</b> no \"Seen by 3 of 8\" count. A returned heart shows the photo arrived.</li>"
         "<li><b>Built for grandparents:</b> large text and tap targets, words under every icon, and invites that work from far away.</li></ul>"),
        ("What it looks like", '<figure class="gallery-wide"><img src="assets/family/laptop-01-demo.webp" width="1200" height="750" loading="lazy" alt="The demo on a laptop: the app beside a short guide"></figure>'
         '<div class="gallery">'
         '<img src="assets/family/iphone-02-share.webp" width="390" height="844" loading="lazy" alt="Share screen: a picked photo, a caption, and the group that will see it">'
         '<img src="assets/family/iphone-03-posted.webp" width="390" height="844" loading="lazy" alt="Photos as the parent: the new post says who it was shared with">'
         '<img src="assets/family/iphone-05-grandparent.webp" width="390" height="844" loading="lazy" alt="Photos as a grandparent: bigger text, only what was shared with her">'
         '</div><p class="note">A made-up family with drawn sample pictures. No real people.</p>'),
        ("How I built it", "<p>I ran it like a small team of eight AI agents (staff PM, QA, app engineer, UI/UX for grandparents, a UX reviewer for public work, privacy and security, marketing, and funding), routed by a chief-of-staff session. "
         "QA writes failing tests first and the engineer makes them pass. There are 600+ app tests and 800+ database checks, and a co-parent data leak was caught in review before any real user saw it.</p>"
         "<p>Stack: Expo / React Native, Supabase (Postgres with row-level security), US-hosted storage.</p>"),
        ("What's next", "<p>A private beta with about a dozen family members, mostly grandparents in West Virginia, targeted for late November.</p>"),
    ],
    status_note="The demo is a made-up family kept only in your browser: no sign-in, no backend. The code is private; the family beta starts late November.",
    links=[("Try the demo", "demo/hearth/")],
)

role_radar = product(
    "AI tool · beta",
    "Role Radar",
    "Most of a job search is sifting. I built a radar that reads the boards every weekday and tells me, with reasons, which roles are worth my time, so I can say no faster.",
    [("~110", "company job boards watched"), ("5", "sources merged, duplicates removed"), ("0–100", "fit score, each with a one-line reason"),
     ("By hand", "every application is still my call")],
    [
        ("How it works", '<ul class="clean"><li>A scheduled agent scans company boards (Greenhouse, Ashby, Lever), ZipRecruiter, Himalayas, Climatebase and job-alert emails, and merges duplicates across sources.</li>'
         "<li>It scores each role 0–100 against criteria I edit in one file (title, remote, comp floor, sectors, culture signals) and gives a one-line reason, so I can check its judgement instead of trusting a number.</li>"
         "<li>One tracker holds every role, and the pipeline updates itself when an application is confirmed or closed.</li></ul>"),
        ("Product decisions", '<ul class="clean"><li><b>Explainable over clever.</b> Every score shows its reasons, and the criteria are plain text, so a wrong call is a one-line fix.</li>'
         "<li><b>Precision, not volume.</b> The goal is fewer, better applications. The measure is how many top-scored roles turn into real conversations.</li>"
         "<li><b>The human stays in the loop.</b> The radar finds and ranks. Reading the posting and applying stay with me.</li>"
         "<li><b>One tracker, not three.</b> Status lived in three places and drifted, so I retired the old pipeline.</li>"
         "<li><b>Cost-aware by design.</b> Big boards run three days a week, and the scan stops paging as soon as results stop being new.</li></ul>"),
        ("Stack", "<p>A single-page app on Claude with its own saved database, a scheduled agent that runs each weekday, and connectors for ZipRecruiter and email.</p>"),
    ],
    status_note="The demo uses made-up jobs and companies, never real applications. Try anything: the demo resets when you reload.",
    links=[("Try the live demo", "/role-radar/"), ("Code on GitHub", f"{GITHUB}/role-radar")],
    shot=("role-radar-phone.webp", "Role Radar on a phone, sample data: the New tab with a Senior Product Manager role scored 90, Strong, with the reason it fits.", 600,
          "The demo reads 9 sample boards. The real radar watches about 110."),
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
        ("Stack", "<p>A TypeScript monorepo with one shared core used by both a CLI, on npm once the name is final, and an offline HTML dashboard.</p>"),
    ],
    links=[("Try the live playground", "/ccwatts/"), ("View on GitHub", f"{GITHUB}/ccwatts")],
    shot=("ccwatts-phone.webp", "The ccwatts playground on a phone, sample data: 8.5 kWh over 30 days, with a plausible range of 1.3 to 30.5 kWh.", 600),
)

energy = product(
    "Family app · live",
    "Energy Scanner",
    "Bedtime was a nightly negotiation. What if a neutral machine said it was time, instead of me?",
    [("Routine", "steps first, scan as the finale"), ("2 scans", "palm pad, or a photo with a live aura"),
     ("On-device", "photos never leave the phone"), ("Grey", "a grown-up switch makes every scan read sleepy")],
    [
        ("The idea", "<p>Kids tick off their bedtime steps (bath, PJs, teeth, potty, book), then scan. The reading is a color from Rainbow (way too much sparkle for sleeping) down to Grey (battery empty, time to recharge). "
         "A neutral \"machine says so\" authority takes the argument off the parent.</p>"),
        ("Two ways to scan", '<ul class="clean"><li><b>Palm scan:</b> press and hold the pad until the ring fills.</li>'
         "<li><b>Photo scan:</b> take or upload a photo and the child's energy glows off them as an animated aura, softer and slower when sleepy, blazing at Rainbow. Grown-ups can save or share it.</li></ul>"),
        ("Decisions", '<ul class="clean"><li><b>Routine first.</b> A scan alone wears off, so it is the reward at the end of real steps, and it never reads Rainbow once every step is done.</li>'
         "<li><b>Privacy before camera.</b> Kids' faces should never go to a cloud model, so the camera waited until the photo scan could run entirely on the phone: a person-segmentation model (MediaPipe) and a GPU shader. No server, no account, no tracking, and the page is locked so it can only talk to its own origin.</li></ul>"),
        ("Status", "<p>Live. It started as a palm-scan prototype my kids tested at bedtime; the photo scan came once it could stay on the phone.</p>"),
    ],
    links=[("Try the live app", "/energy-scanner/"), ("View on GitHub", f"{GITHUB}/energy-scanner")],
    shot=("energy-scanner-phone.webp", "Energy Scanner on a phone at 7:42 PM: three of five bedtime steps done (bath, PJs, teeth) and the palm scanner ready.", 546),
)

pm_tools = """<div class="read">
<p class="eyebrow">The system behind it</p>
<h1>How I keep it all moving.</h1>
<p class="lede">These are the tools and rituals I use to ship several products in parallel without losing the thread. The two apps below run on a scrubbed snapshot of my real slate and roadmap; anything you change stays in your browser.</p>
<h2>Build Slate</h2>
<p>One board for every product: stage (idea, spec, building, beta, launched, paused), the very next step, and a milestone date. It caps me at five active projects so I go deep, not wide.</p>
<div class="cta"><a class="btn primary" href="/pm-tools/build-slate/">Try Build Slate</a></div>
<h2>Near-term roadmap</h2>
<p>Later, Next, Now and Done lanes with a board per product, owners, work-session estimates and a blocked flag. Any AI session can read and update it by link, so the roadmap stays current without me retyping it.</p>
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
<li><b>Now: building with AI.</b> I prototype tools that fix problems in my own life (bedtime, the job search, family photos, the energy my AI use takes) and onboard real people to each one. Not raising, not selling; ready for a full-time role.</li>
</ol>
<h2>What I care about</h2>
<ul class="clean"><li>Checkout, pricing and payments that feel simple to the person at the kitchen table.</li>
<li>Clean energy and climate, rooted in a WVU degree in Sustainable Design.</li>
<li>Privacy that's strong underneath and obvious on the surface.</li>
<li>Calm teams that ship.</li></ul>
<h2>Get in touch</h2>
<p>I'm looking for a senior or staff product role, remote. The best way to reach me is <a href="{LINKEDIN}">LinkedIn</a>.</p>
</div>"""

# Resume: mirrors pmo/story/resume-2026-10.md (Oct 2026). Never add phone or email; LinkedIn is the contact route.
JOBS = [
    ("Staff Product Manager", "Patter AI", "Jan 2023 – Jan 2026 · Remote", [
        "Real-time pricing engine across loans, leases and PPAs for 4 clients.",
        "Rep-guided checkout showing the payment impact of each add-on.",
        "AI conversation analysis found 40% of a client's reps deviating from scripts; coaching went from about 4 a month to about 1 a day.",
        # The B2B contract-pricing dollar figures stay off until Chase OKs publishing them (case-study doc [check]).
        "Lender onboarding cut from about a month to about a week with a rules engine; 5 lenders integrated.",
    ]),
    ("Senior Product Manager", "ADT", "Nov 2021 – Jan 2023", [
        "Credit-check and offer engine across 5 lenders, 12,000+ applications a month, during 110% YoY sales growth.",
        "Lender allocation platform (GoodLeap, Sunlight, Mosaic, Dividend and others) used to cut dealer fees 3–5 points.",
        "Channel-partner platform with redline and tiered pricing, Power BI reporting, 4+ partners.",
        "Technical lead for the Lowe's in-store solar and security program.",
        "Post-merger integration scaling to 400,000+ consultations a year, with releases to about 5,000 reps' iPads.",
    ]),
    ("Product Manager", "ADT", "Oct 2020 – Nov 2021", [
        "Rep-guided checkout for complex solar products that cut contract review about 60%.",
        "First PM for the 3,000-person solar division.",
    ]),
    ("Product Owner", "AGDATA", "Jun – Oct 2020", [
        "Discovery for an MDM platform to consolidate 8+ legacy pricing and rebate systems (Bayer, among others).",
    ]),
    ("Founder", "Bigfoot Energy", "Oct 2019 – Jun 2020 · Charleston, WV", [
        "Smart-home and clean-energy company.",
    ]),
    ("Director of Product", "Palmetto", "Jan – Jun 2019", [
        "Machine-learning lead marketplace on about 300 data points, 11,500+ consultations a month.",
    ]),
    ("Senior Product Manager", "Palmetto", "Feb 2018 – Jan 2019", [
        "Built Alchemy (design, point of sale and project management), integrating GoodLeap and Sunlight into real-time credit.",
        "Supported a $6M venture round.",
    ]),
    ("Product Manager", "Palmetto", "Jun 2017 – Feb 2018", [
        "First PM: sales enablement platform; digitized pricing models.",
    ]),
    ("Senior Solar Engineer", "Palmetto", "Feb 2016 – Jun 2017", [
        "Designed 2,000+ PV systems; virtual surveys replaced 75% of site visits, saving $80K a year.",
    ]),
]

resume = f"""<div class="read resume">
<p class="eyebrow">Resume · Charlotte, NC · open to remote roles</p>
<h1>Chase Holroyd</h1>
<p class="lede">Staff Product Manager · Pricing, Payments &amp; Point-of-Sale Lending</p>
<p>8+ years building point-of-sale financing and pricing products: rep-guided checkout, dealer-fee and redline pricing engines, and real-time loan, lease and PPA payments. 13+ lender integrations; a credit and offer engine at 12,000+ applications a month; lender allocation that cut dealer fees 3–5 points.</p>
<p class="contact">Contact: <a href="{LINKEDIN}">linkedin.com/in/chase-holroyd</a> · Site: chaseholroyd.com</p>
<h2>Experience</h2>
""" + "".join(
    f'<section class="job"><h3>{t}, {c}</h3><p class="when">{d}</p><ul class="clean">'
    + "".join(f"<li>{b}</li>" for b in bullets) + "</ul></section>"
    for t, c, d, bullets in JOBS
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
    ("family-photos.html", "Family photo app", "A private family photo app for split families and grandparents, with a chosen audience on every post.", family),
    ("role-radar.html", "Role Radar", "An AI job-search radar that scans about 110 company boards each weekday.", role_radar),
    ("ccwatts.html", "ccwatts", "Estimate the electricity your Claude Code usage consumes, as an honest range.", ccwatts),
    ("energy-scanner.html", "Energy Scanner", "A bedtime routine for kids that ends with an energy scan: a palm pad, or a photo with an on-device aura.", energy),
    ("pm-tools.html", "How I keep it all moving", "The slate, roadmap and AI agents that keep several products moving at once.", pm_tools),
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
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"Wrote {len(PAGES)} pages to {ROOT}")
