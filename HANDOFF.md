# Handoff: chaseholroyd.com

_Read this before starting work on this repo. Update it in the same commit whenever you make progress._

Last updated: 2026-10-22 (overnight: WEB-M4.7 screenshots and UX P2s, draft PR)

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
| WEB-M3.4 | Role Radar public demo shows the radar only (page reframed as "say no faster"). The resume intake/Apply, intake settings and Recruiters tab sit behind a flag: `/demo/role-radar/?full` shows them, for people Chase shares that link with. Chase's live app is unchanged. Storage keys `role-radar-v2` (public) and `role-radar-full` | done (PR #9, Oct 22). Next: Role Radar hosts its own demo (intake sent), then delete `demo/role-radar/` here |
| ES-M2.3 | Energy Scanner page: "Try it" opens the live app at /energy-scanner/ (deployed from the energy-scanner repo), copy covers the palm and on-device photo scans, adds a GitHub link. The old `demo/energy-scanner/` snapshot stays one release, unlinked, then gets removed | done (PR #8, Oct 21) |

## WEB-M4 "recruiter-ready review" (Oct 22)
ux-reviewer and qa-tdd reviewed the site and pm-tools; staff-pm ranked it: `docs/reviews/2026-10-22-recruiter-ready.md`.
- Done in this PR: WEB-M4.1 deploy only site files (`_site/` allowlist in pages.yml) and no claude.ai links in the repo (they remain in git history; no rewrite), M4.2 hero says "Most recently Staff PM at Patter AI", M4.3 "View resume" on the first screen, M4.4 How I work and family app copy, M4.5 styled 404 on nested paths, M4.6 `site-checks.yml` CI.
- Studio agents synced into `.claude/agents/` from studio-agents (includes the upgraded ux-reviewer with the visual pass and showcase review, studio-agents draft PR #6 or later); re-sync with its `scripts/sync.sh`.
- Overnight Oct 22 (draft PR, branch `claude/project-thread-hsgkpq-m47`): WEB-M4.7 one 390px phone screenshot under the lede on Role Radar, ccwatts and Energy Scanner (`assets/shots/*.webp`, 26–46 KB, sample data only, Role Radar from its public view; set with `product(shot=...)`). UX-13 44px tap targets on nav, footer and back links. UX-14 "Claude artifact" jargon on Role Radar's stack line. UX-15 CTAs "Try the live demo / playground / app", plus a GitHub link on Role Radar. UX-12 the Role Radar demo's back link opens role-radar.html. To re-shoot: Playwright at 390x844 with deviceScaleFactor 2 (Energy Scanner with the clock set to 7:42 PM and three steps ticked), crop to 780x1560, then save as 600x1200 WebP q78.
- ccwatts intake (Oct 22): the Stack line no longer says `npx ccwatts` (it 404s until the npm name is final). The ccwatts playground links back to https://chaseholroyd.com/ccwatts.html, so keep that URL stable. Re-shoot `assets/shots/ccwatts-phone.webp` once ccwatts PRs #22–#29 merge.
- Round 2 (UXR2-1..3, QAR2-1) done. Nothing at P2 or above is left on the product pages; see the review doc.
- Round 1 review fixes (caption, desktop two-column hero, re-crop, 44px name/skip/demo back link, footer title) are logged in the review doc's "Overnight rounds" section.
- Not here: "Built with" and "calm by default" aren't on this site (pm-tools copy). "anxiety-less" sits in How I work, which belongs to WEB-M5 PR #12.
- Decision for Chase: WEB-M4.8, add "Independent product work, Jan 2026 – present" to the resume page? It mirrors your real resume, so it's your call.

Stop rule (staff PM): after WEB-M2, stop site work. The signal is recruiter screens per 15 applications, plus asking in screens whether they saw the site.

## Keeping the demos in sync with the real apps
The real apps are Claude artifacts. The demos are snapshots of them, so they drift when an app changes.
1. Save the app's current artifact page over `tools/demo-src/<name>.html` (Claude: Artifact tool, read with `path: "index.html"`).
2. Run `python3 tools/make_demos.py`. It fails loudly if a demo-only edit no longer applies.
3. Update the version table below and commit.

| Demo | Artifact | Snapshot version |
|---|---|---|
| energy-scanner (legacy, unlinked since ES-M2.3; remove next release) | link in project memory | 1792454453-b0d3 |
| role-radar | link in project memory | 1792568778-859e |

## Rules
- Only site files deploy (see pages.yml). Add a new top-level public file or folder to the `cp` line there.
- Never publish Chase's phone or email. LinkedIn is the contact route.
- Role Radar demo data is made up (companies, people, jobs, comp floor). Never copy real applications or recruiters into `demo/role-radar/seed.js`.
- The Hearth repo stays private and its name isn't final, so the site says "family photo app (name coming)".

## Next
- Who does what (Chase, Oct 21): the thread that owns a repo makes its changes. Product threads send the portfolio thread an intake for portfolio-repo changes; every portfolio change that touches a product gets a dated line in that product's HANDOFF.md, written by that product's thread.
- After ES-M2.3 merges and one release passes: delete `demo/energy-scanner/` and `tools/demo-src/energy-scanner.html`.
- Case studies (WEB-M2.3, M2.4) wait for Chase's [check] pass on Oct 22. Next without Chase: WEB-M3.1.
- Removed a stray `shots/` folder of screenshots that PR #5 committed by mistake.
- Chase: a single review pass of the pages.
- Hearth rename, then update `family-photos.html` copy.
- Optional: a "portfolio: feature / list / hidden" field in Build Slate so the site follows the slate (tracked in pm-tools PLAN.md).
