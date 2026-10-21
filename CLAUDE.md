# CLAUDE.md

The source for chaseholroyd.com, Chase's portfolio: a static site on GitHub Pages. Page content lives in `tools/build.py` (run `python3 tools/build.py` to regenerate the HTML); demos live under `demo/`. `HANDOFF.md` has the current state, deploy notes and how to sync demos.

## Hard rules
- Public repo: no secrets, tokens, artifact or trigger ids, and no personal data beyond what Chase publishes on the site.
- Never merge to `main` without Chase: a push to `main` deploys the live site.

## Session rules (studio-wide)

- Before starting: read this file and `HANDOFF.md` (a SessionStart hook prints it), then the doc this file points to for the task. Check open PRs and branches and resume, never redo.
- Every commit or PR that makes progress updates `HANDOFF.md` in the same commit or PR: done, in progress, exact next step, decisions to review, blockers. The `handoff-check` PR workflow enforces it; use `[skip handoff]` in the PR title only for changes that do not move the work.
- Full rules: `docs/session-rules.md` in holroydchase-afk/studio-agents.
