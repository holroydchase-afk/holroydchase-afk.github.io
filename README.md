# chaseholroyd.com

The source for [chaseholroyd.com](https://chaseholroyd.com), Chase Holroyd's product management portfolio: what he built, why, and live demos you can click. It is plain static HTML on GitHub Pages, with no framework and no tracking beyond what the site itself states.

## Why it looks like this
A recruiter or hiring manager should see the work first. Pages are generated from one Python file so copy, links and demos stay consistent, and CI refuses to ship a page that breaks the basics (title, description, one `h1`, image alt text, a sitemap entry, no email address or phone number).

## Run it
Needs Python 3 and Node (the demo test and share-card script use it).

```bash
python3 tools/build.py        # regenerate the HTML at the repo root from the page content
python3 tools/make_demos.py   # rebuild the demo copies from their sources
python3 tools/check_site.py   # offline page checks
python3 -m http.server 8000   # then open http://localhost:8000
```

## Test
`site-checks.yml` runs on every pull request: it regenerates the pages and fails if the committed HTML differs (`git diff --exit-code`), runs `tools/check_site.py`, and checks for broken internal links and for claude.ai links, which do not belong in a public repo. The energy scanner demo has its own test (`node tools/test_energy_demo.mjs`).

## How it is laid out
- `tools/build.py`: all page content and the generator. Edit copy here, not in the generated `*.html`.
- `assets/`: styles (`site.css`) and self-hosted fonts. The site loads nothing from third-party hosts.
- `demo/`: static copies of the product demos (sample data only). Their sources live in each product's own repo.
- `scripts/`: shared studio checks (agent roster, logs, findings).
- `stats-proxy/`: the small proxy that serves visit stats (see its README).
- `CNAME` points the site at chaseholroyd.com. A push to `main` deploys, and `pages.yml` publishes only the public files.

## Working in this repo
Read `CLAUDE.md` and `HANDOFF.md` first. Changes go through pull requests; merging to `main` deploys the live site, so those wait for Chase's go.

## License
Site content is all rights reserved (see `LICENSE`). The demo apps stay MIT in their own repos.
