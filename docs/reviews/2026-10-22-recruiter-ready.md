# Recruiter-ready review: portfolio site and pm-tools (2026-10-22)

Bar (Chase, Oct 22): every product on chaseholroyd.com is ready to show a recruiter or hiring manager. Reviewers: ux-reviewer (walkthrough as a recruiter on a phone and a hiring manager on a laptop, Playwright at 390px and 1280px) and qa-tdd (builds, tests 3x, link crawl, demo flows). Triage: staff-pm.

## Test results
- Portfolio: generated pages match `tools/build.py`; 16 pages crawled, 0 internal 404s, 0 page errors, no horizontal scroll at 390px. No CI tests before this PR.
- pm-tools: `npm test` 3 runs, 8/8 + 10/10, no flakes; `check:private` clean; demos add/edit/reload/reset work.

## Ranked (P0 blocks showing it, P1 hurts the impression, P2 later)
| # | ID | Pri | Repo | Finding | Fix | Status |
|---|---|---|---|---|---|---|
| 1 | WEB-M4.1 (QA-1, QA-2, QA-9) | P0 | portfolio | Two claude.ai artifact links in `tools/make_demos.py`, and the deploy served the whole repo, so HANDOFF.md, CLAUDE.md, tools/ and the `?full` link were public | Links removed; deploy stages an allowlist into `_site/`; CI fails on claude.ai links | this PR (links stay in git history: no rewrite, per rules) |
| 2 | WEB-M4.2 (UX-1) | P0 | portfolio | Hero said "Staff PM at Patter AI" (present tense) while resume says Jan 2026 | "Most recently Staff PM at Patter AI" | this PR |
| 3 | PMT-M2.2 (UX-2, UX-3, QA-4, QA-5) | P0 | pm-tools | Build Slate and Roadmap demos are frozen at day one: ccwatts "Spec", Energy Scanner "no camera yet", "6 of 5 past it", one board at "1 of 20 done" | Re-seed both from the current scrubbed live state; 5 or fewer active projects; add a second board | overnight |
| 4 | WEB-M4.3 (UX-6) | P1 | portfolio | No resume link on the first screen | "View resume" replaces "My path" | this PR |
| 5 | WEB-M4.4 (UX-4, UX-5) | P1 | portfolio | "real slate" vs "sample data" contradiction; "studio of one"; "name coming" and "placeholder name" on the family app page | New How I work H1 and lede; "A private family photo app" | this PR |
| 6 | WEB-M4.5 (QA-3) | P1 | portfolio | 404 page unstyled on nested paths (old /portfolio/ links) | `<base href="/">` on 404.html | this PR |
| 7 | WEB-M4.6 (QA-10) | P1 | portfolio | No CI checks | `site-checks.yml`: build in sync, no claude.ai links, internal links resolve | this PR |
| 8 | PMT-M2.3 (UX-11) | P1 | pm-tools | /pm-tools/ landing has no header or way back; "Try it" twice | Top bar "← Chase Holroyd"; "Try Build Slate" / "Try the roadmap" | overnight |
| 9 | WEB-M4.7 (UX-10) | P1 | portfolio | No product page has a screenshot | One phone screenshot per product page, sample data only | overnight |
| 10 | RR intake (UX-8, UX-9, QA-6, QA-7) | P1 | Role Radar | Demo: "Sam" never introduced, 60 STRONG vs 60 MAYBE, "Open posting" goes to example.com, js-yaml from a CDN | Goes to Role Radar with its demo move | intake to Role Radar |
| 11 | WEB-M4.8 (UX-7) | P1 | portfolio | Resume ends Jan 2026 with no current entry | Chase's call: resume page mirrors his real resume | waiting on Chase |
| — | UX-12..15, QA-8, QA-11 | P2 | both | Back links go home not to the product page; 24px tap targets; jargon ("Claude artifact", "anxiety-less"); CTA wording; legacy demo/energy-scanner; pm-tools browser test | Later, after the P1s | later |

## Overnight rounds (Oct 22, draft PR #13): product pages only
Scope: role-radar, ccwatts, energy-scanner and family-photos pages, shared CSS and checks. WEB-M5 (#12) owns the home page, nav, About and How I work.

### Round 1: ux-reviewer (showcase review, 390x844 and 1280x800, light and dark) and qa-tdd
| ID | Pri | Finding | Status |
|---|---|---|---|
| WEB-M4.7 / UX-10 | P1 | No product page had a screenshot | done: phone shot under the lede on 3 pages, beside the text and facts at 900px and up so the facts stay above the fold |
| UX-12 / UXR1-3 | P2 | Demo back link went home, said "← Chase Holroyd" and was 20px tall | done: "← Back to Role Radar", opens role-radar.html, 44px |
| UX-13 / QAR1-1 / UXR1-7 | P2 | Nav, footer, back and name links under 44px | done: all 44px; focused skip link 44px (QAR1-2) |
| UX-14 | P2 | "Claude artifact" jargon on Role Radar | done ("Built with" and "calm by default" aren't on this site) |
| UX-15 | P2 | CTA wording; no GitHub link on Role Radar | done |
| UXR1-1 | P2 | Shot shows 7 boards, stat says ~110 | done: caption "The demo reads 7 sample boards. The real radar watches about 110." |
| UXR1-2 | P2 | Desktop: shot alone, facts below the fold | done (two-column hero) |
| UXR1-4 | P2 | Energy Scanner shot clipped through a line of text | done: re-cropped to 600x1092 |
| UXR1-5 | P3 | Above-the-fold shots lazy-loaded | done: eager, fetchpriority high |
| UXR1-6 | P3 | Footer links sat lower than the © line | done |
| UXR1-8 | P3 | Footer said "Product manager" | done: "Staff product manager" |
| UXR1-9 | P3 | ccwatts CTAs wrap on a phone | left as is (acceptable) |
| QAR1-0 | P0 process | QA's `git checkout -- .` wiped in-progress edits in a shared tree | redone; later QA rounds run in their own worktree |
| QAR1-3 | P3 | Role Radar demo loads js-yaml from a CDN | Role Radar intake (its demo moves to its own repo) |
| QAR1-4 | note | ?full hides in the browser only; seed data ships to everyone | fine while seed data stays made up |
Notes for WEB-M5 (home): career cards and links, the dated "Since Jan 2026" heading, and "every demo runs on sample data" not being true of the family app or Energy Scanner. #12 covers the first two; the third is a #12 copy fix.
