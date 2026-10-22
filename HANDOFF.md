# Handoff: chaseholroyd.com

_Read this before starting work on this repo. Update it in the same commit whenever you make progress._

Last updated: 2026-10-22 (WEB-M5 draft #12 waits on Chase's answers; main merged in with WEB-M3.5 Role Radar move #14 and WEB-M3.6 Hearth demo #15)

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
| WEB-M3.5 | Role Radar intake (Oct 22): "Try the live demo" opens /role-radar/ (built and deployed from the role-radar repo); `demo/role-radar/`, its snapshot and its make_demos.py edits are deleted; 5 sources (adds Climatebase); "Try anything: the demo resets when you reload"; "Code on GitHub"; footer "Charlotte area"; screenshot re-shot from Role Radar's own demo | done (PR #14, Oct 22) |
| WEB-M3.6 | Hearth intake (Oct 22, `docs/portfolio/INTAKE-2026-10-22-demo.md` in the Hearth repo): no-login demo copied to `demo/hearth/` (built from Hearth main 10001df with `cd app && npm ci && bash scripts/build-demo.sh`, the contents of `app/dist-demo-site/`; a made-up family, drawn pictures, browser-only). family-photos.html gets "Try the demo", named groups, encryption (AES-256-GCM, MLS), no "Seen by" count, eight agents, 600+ app tests and 800+ database checks, and 4 screenshots in `assets/family/`. Placeholder name kept; the expo.app build and the private repo are not linked | done (this PR) |
| ES-M2.3 | Energy Scanner page: "Try it" opens the live app at /energy-scanner/ (deployed from the energy-scanner repo), copy covers the palm and on-device photo scans, adds a GitHub link. The old `demo/energy-scanner/` snapshot stays one release, unlinked, then gets removed | done (PR #8, Oct 21) |

## WEB-M4 "recruiter-ready review" (Oct 22)
ux-reviewer and qa-tdd reviewed the site and pm-tools; staff-pm ranked it: `docs/reviews/2026-10-22-recruiter-ready.md`.
- Done in this PR: WEB-M4.1 deploy only site files (`_site/` allowlist in pages.yml) and no claude.ai links in the repo (they remain in git history; no rewrite), M4.2 hero says "Most recently Staff PM at Patter AI", M4.3 "View resume" on the first screen, M4.4 How I work and family app copy, M4.5 styled 404 on nested paths, M4.6 `site-checks.yml` CI.
- Studio agents synced into `.claude/agents/` from studio-agents (includes the upgraded ux-reviewer with the visual pass and showcase review, studio-agents draft PR #6 or later); re-sync with its `scripts/sync.sh`.
- Done (overnight round 5, R4-3): How I work now says Build Slate caps "five active projects" and lists the roadmap lanes as "Later, Next, Now and Done", matching the pm-tools demo.
- Overnight Oct 22 (draft PR, branch `claude/project-thread-hsgkpq-m47`): WEB-M4.7 one 390px phone screenshot under the lede on Role Radar, ccwatts and Energy Scanner (`assets/shots/*.webp`, 26–46 KB, sample data only, Role Radar from its public view; set with `product(shot=...)`). UX-13 44px tap targets on nav, footer and back links. UX-14 "Claude artifact" jargon on Role Radar's stack line. UX-15 CTAs "Try the live demo / playground / app", plus a GitHub link on Role Radar. UX-12 the Role Radar demo's back link opens role-radar.html. To re-shoot: Playwright at 390x844 with deviceScaleFactor 2 (Energy Scanner with the clock set to 7:42 PM and three steps ticked), crop to 780x1560, then save as 600x1200 WebP q78.
- ccwatts intake (Oct 22): the Stack line no longer says `npx ccwatts` (it 404s until the npm name is final). The ccwatts playground links back to https://chaseholroyd.com/ccwatts.html, so keep that URL stable. Re-shoot `assets/shots/ccwatts-phone.webp` once ccwatts PRs #22–#29 merge.
- Round 2 (UXR2-1..3, QAR2-1) done. Nothing at P2 or above is left on the product pages; see the review doc.
- Round 1 review fixes (caption, desktop two-column hero, re-crop, 44px name/skip/demo back link, footer title) are logged in the review doc's "Overnight rounds" section.
- Not here: "Built with" and "calm by default" aren't on this site (pm-tools copy). "anxiety-less" sits in How I work, which belongs to WEB-M5 PR #12.
- Decision for Chase: WEB-M4.8, add "Independent product work, Jan 2026 – present" to the resume page? It mirrors your real resume, so it's your call.

## WEB-M5 "my AI journey" reframe (Chase, Oct 22)
Chase: the site is a case study of how he grew in using AI to solve problems in his own life, each product tied to a life story and its real users, told as a journey rather than a fixed timeline. His biggest career wins (Palmetto, ADT, Patter) belong on the front page, with links to Patter and Palmetto. He doesn't like "How I work". This overrides the staff PM's stop rule below.
| ID | Task | Status |
|---|---|---|
| WEB-M5.1 | Home: hero "A staff PM who builds with AI to fix real problems", career highlight cards (Patter, ADT, Palmetto) with outside links, "What I've built with AI" journey cards ordered by how the building grew (prototype, scheduled agent, open source, agent team, the system) with a "who uses it" line each | doing (draft PR, [check] items wait on Chase) |
| WEB-M5.2 | "How I work" leaves the nav; the page becomes "How I keep it all moving" (the system behind it), with PR #11's copy fixes plus "work-session estimates". About drops the dated "Since Jan 2026" line for "Now: building with AI" | doing (same PR) |
| WEB-M5.3 | Each product page opens with its life story and real users (needs Chase's stories) | todo |
| WEB-M5.4 | Case studies (WEB-M2.3/M2.4) linked from the ADT and Patter cards once their [check]s clear | blocked on Chase |
Open [check]s for Chase: Patter's site URL (Capterra lists salespatter.io; this container can't open patter or palmetto sites), who uses Energy Scanner, Role Radar and ccwatts today, and whether "about an hour a night" is OK to publish.

Stop rule (staff PM): after WEB-M2, stop site work. The signal is recruiter screens per 15 applications, plus asking in screens whether they saw the site.

## Keeping the demos in sync with the real apps
The real apps are Claude artifacts. The demos are snapshots of them, so they drift when an app changes.
1. Save the app's current artifact page over `tools/demo-src/<name>.html` (Claude: Artifact tool, read with `path: "index.html"`).
2. Run `python3 tools/make_demos.py`. It fails loudly if a demo-only edit no longer applies.
3. Update the version table below and commit.

| Demo | Artifact | Snapshot version |
|---|---|---|
| energy-scanner (legacy, unlinked since ES-M2.3; remove next release) | link in project memory | 1792454453-b0d3 |

## Rules
- `demo/hearth/` is a build output from the Hearth repo. Don't edit it here: rebuild it there and copy it over. Re-check /demo/hearth/photos and a full-screen photo reload after each copy.
- Only site files deploy (see pages.yml). Add a new top-level public file or folder to the `cp` line there.
- Never publish Chase's phone or email. LinkedIn is the contact route.
- Role Radar's demo lives in the role-radar repo (chaseholroyd.com/role-radar/); change it there, not here.
- The Hearth repo stays private and its name isn't final, so the site says "family photo app (name coming)".

## Next
- Who does what (Chase, Oct 21): the thread that owns a repo makes its changes. Product threads send the portfolio thread an intake for portfolio-repo changes; every portfolio change that touches a product gets a dated line in that product's HANDOFF.md, written by that product's thread.
- After ES-M2.3 merges and one release passes: delete `demo/energy-scanner/` and `tools/demo-src/energy-scanner.html`.
- Case studies (WEB-M2.3, M2.4) wait for Chase's [check] pass on Oct 22. Next without Chase: WEB-M3.1.
- Removed a stray `shots/` folder of screenshots that PR #5 committed by mistake.
- Chase: a single review pass of the pages.
- Hearth rename, then update `family-photos.html` copy.
- Optional: a "portfolio: feature / list / hidden" field in Build Slate so the site follows the slate (tracked in pm-tools PLAN.md).
