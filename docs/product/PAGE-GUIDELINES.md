# Product page guidelines

Every product page on chaseholroyd.com (Hearth, Role Radar, ccwatts, Charlie, Energy Scanner, Crew Clock) is built by `product(...)` in `tools/build.py`. Do not hand-write page markup. Chase, Nov 6: "It's the Wild West", so one template and these rules.

## Layout (fixed by the template)
1. **Hero band (dark):** eyebrow (type · status), name, one-sentence lede, one primary and at most one secondary button, one phone screenshot on sample data, then four proof facts.
2. **Numbered section bands**, in this order (skip a section only if it has no honest content):
   1. The problem (a real problem in Chase's life or a real user's, in two or three sentences)
   2. What I built (3 to 5 bullets, then screenshots via `shots(...)`)
   3. How it works (the method or the decision logic, with its limits)
   4. Product calls (3 decisions with the trade-off each)
   5. Proof (`proof_grid`: 3 to 4 checkable claims)
   6. Try it (`code_block` for commands, or the demo link)
   7. Status and what's next (what is live, what is not, the next release)
3. **Back link.** Nothing after it.

## Voice
First person, problem to what I built to result (voice B in the site-voice rule). A hook under 35 words. No superlatives, jokes, rhetorical questions or "passion project".

## Claims (site = repo truth)
- Every number and feature must be backed by the product's repo and listed in `pmo/portfolio/claims-register.md`.
- Say what is live today. Unreleased work is "next", with no date unless the repo has one.
- Counts that can't be reproduced from the repo get a rounded floor ("30+ test files"), not a precise figure.
- Privacy claims name the mechanism (for example a Content-Security-Policy with a test), not just the promise.

## Visuals
- Phone shot in the hero, sample data only, never a real person or real usage. Add a "Sample data" caption.
- Further screenshots go in `shots(...)`: WebP, real width and height set, alt text that says what the picture shows, one-line caption.
- No stock art, no collages, no decorative icons.

## Checks before a PR
`python3 tools/build.py`, view desktop (1280) and phone (390) screenshots, run the ux-reviewer in showcase mode, and add a dated line to the product repo's HANDOFF.md "Portfolio / public presence".

## Migration status
ccwatts is the reference page (all seven sections). Hearth, Role Radar, Charlie, Energy Scanner and Crew Clock already render in the new layout but keep their old sections; each is brought to this order in its own PR, by the thread that owns the repo's facts.
