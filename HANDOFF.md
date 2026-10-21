# Handoff: chaseholroyd.com

_Read this before starting work on this repo. Update it in the same commit whenever you make progress._

Last updated: 2026-10-21 (studio status file; Energy Scanner app is live)

Studio-wide status (what's done across every project and what's waiting on Chase): https://github.com/holroydchase-afk/pm-tools/blob/main/STUDIO-STATUS.md. Product repos record portfolio facts in their own HANDOFF.md "Portfolio / public presence" section.

## Current state
- 2026-10-21: studio session rules installed: `.claude/settings.json` SessionStart hook prints this file into every Claude Code session, `.github/workflows/handoff-check.yml` fails a PR that changes files without updating this file, and CLAUDE.md has a "Session rules" section.
- **Live** at https://chaseholroyd.com. The repo is `holroydchase-afk/holroydchase-afk.github.io` (renamed from `portfolio` on Oct 21), so it is the account's user site and other repos' Pages sites appear at chaseholroyd.com/<repo>, e.g. the ccwatts playground at /ccwatts/. Deploys run on every push to `main` via `.github/workflows/pages.yml`.
- Don't add a top-level folder named after another repo with Pages on (e.g. `ccwatts/`, `pm-tools/`); it would hide that repo's site.
- **Custom domain:** DNS at Porkbun and the Pages custom domain are set (Chase, Oct 21). Actions deploys ignore the `CNAME` file; the domain lives in Settings → Pages.
- **Pages:** Work (home), the family photo app (name coming), Role Radar, ccwatts, Energy Scanner, How I work, About, 404. Content lives in `tools/build.py`; run `python3 tools/build.py` to regenerate the HTML.
- **Demos** under `demo/`: Role Radar and Energy Scanner, each running the real app on sample data saved only in the visitor's browser (`demo/fake-db.js` stands in for the artifact database).
- **Build Slate and the Near-Term Roadmap** demos live in the `pm-tools` repo, served at chaseholroyd.com/pm-tools/build-slate/ and /pm-tools/roadmap/. "How I work" links there. Sync those apps in pm-tools (its HANDOFF.md), not here.

- License audit (2026-10-21): added `LICENSE` (site content all rights reserved; demo apps MIT from their source repos; Google Fonts are OFL and linked, not stored) and a © line in the footer. No takedown needed.

## Plan: WEB-M2 "recruiter-ready"
The research, audit and ranked plan from the "Portfolio research and upgrade plan" thread (Oct 21) are summarized here; WEB-M1 was the launch (done Oct 21).
| ID | Task | Status |
|---|---|---|
| WEB-M2.1 | Link preview card (`assets/share-card.png`, source `tools/share-card.html`, render with `node tools/make_share_card.mjs`), canonical URLs, sitemap.xml and robots.txt (written by build.py), Person JSON-LD (no email or phone), skip link, eyebrow contrast to WCAG AA | done (PR #5, Oct 21) |
| WEB-M2.2 | Hero: "Staff PM for pricing, payments and point-of-sale lending", proof bar of 4 resume numbers, "Since Jan 2026: independent product work" replaces "studio of one" on home and About, cards reordered with live demos first | done (PR #5, Oct 21; leads with Staff, Chase can still switch to Senior) |
| WEB-M2.3 | Case study: ADT credit and offer engine plus lender allocation (context / my role / decisions / outcome / what I'd change; every claim I or we) | blocked (Chase reviews the [check] questions Oct 22) |
| WEB-M2.4 | Case study: Patter real-time pricing engine plus lender rules engine | blocked (Chase reviews the [check] questions Oct 22) |
| WEB-M2.5 | Resume page (`resume.html`, in the nav) mirroring pmo/story/resume-2026-10.md, print CSS (2 Letter pages), no phone or email. Patter's B2B dollar figures left off until Chase OKs them | done (PR #6, Oct 21) |
| WEB-M2.6 | Chase: headshot, LinkedIn Featured link and headline, LinkedIn Post Inspector | todo |
| WEB-M3.1 | Outcomes and "what I'd do differently" on Role Radar and ccwatts pages | todo |
| WEB-M3.2 | Hearth page after the rename | dropped (off the job-hunt critical path) |
| WEB-M3.3 | Visit counter | dropped (no-analytics rule) |

Stop rule (staff PM): after WEB-M2, stop site work. The signal is recruiter screens per 15 applications, plus asking in screens whether they saw the site.

## Keeping the demos in sync with the real apps
The real apps are Claude artifacts. The demos are snapshots of them, so they drift when an app changes.
1. Save the app's current artifact page over `tools/demo-src/<name>.html` (Claude: Artifact tool, read with `path: "index.html"`).
2. Run `python3 tools/make_demos.py`. It fails loudly if a demo-only edit no longer applies.
3. Update the version table below and commit.

| Demo | Artifact | Snapshot version |
|---|---|---|
| energy-scanner | https://claude.ai/artifact/VphgM8fKNVhcDc31RVdBJr | 1792454453-b0d3 |
| role-radar | https://claude.ai/artifact/YQFGobfPX9BKkv4yibcnsr | 1792568778-859e |

## Rules
- Never publish Chase's phone or email. LinkedIn is the contact route.
- Role Radar demo data is made up (companies, people, jobs, comp floor). Never copy real applications or recruiters into `demo/role-radar/seed.js`.
- The Hearth repo stays private and its name isn't final, so the site says "family photo app (name coming)".

## Next
- ES-M2.3: the Energy Scanner app is live at chaseholroyd.com/energy-scanner/ (deployed Oct 21 23:32 UTC); point `energy-scanner.html` there instead of /demo/energy-scanner/.
- Case studies (WEB-M2.3, M2.4) wait for Chase's [check] pass on Oct 22. Next without Chase: WEB-M3.1.
- Removed a stray `shots/` folder of screenshots that PR #5 committed by mistake.
- Chase: a single review pass of the pages.
- Hearth rename, then update `family-photos.html` copy.
- Optional: a "portfolio: feature / list / hidden" field in Build Slate so the site follows the slate (tracked in pm-tools PLAN.md).
