# Handoff: chaseholroyd.com

_Read this before starting work on this repo. Update it in the same commit whenever you make progress._

Last updated: 2026-10-21 (repo renamed to holroydchase-afk.github.io)

## Current state
- **Live** at https://chaseholroyd.com. The repo is `holroydchase-afk/holroydchase-afk.github.io` (renamed from `portfolio` on Oct 21), so it is the account's user site and other repos' Pages sites appear at chaseholroyd.com/<repo>, e.g. the ccwatts playground at /ccwatts/. Deploys run on every push to `main` via `.github/workflows/pages.yml`.
- Don't add a top-level folder named after another repo with Pages on (e.g. `ccwatts/`); it would hide that repo's site.
- **Custom domain:** DNS at Porkbun and the Pages custom domain are set (Chase, Oct 21). Actions deploys ignore the `CNAME` file; the domain lives in Settings → Pages.
- **Pages:** Work (home), the family photo app (name coming), Role Radar, ccwatts, Energy Scanner, How I work, About, 404. Content lives in `tools/build.py`; run `python3 tools/build.py` to regenerate the HTML.
- **Demos** under `demo/`: Build Slate, Near-Term Roadmap, Role Radar and Energy Scanner, each running the real app on sample data saved only in the visitor's browser (`demo/fake-db.js` stands in for the artifact database).

## Keeping the demos in sync with the real apps
The real apps are Claude artifacts. The demos are snapshots of them, so they drift when an app changes.
1. Save the app's current artifact page over `tools/demo-src/<name>.html` (Claude: Artifact tool, read with `path: "index.html"`).
2. Run `python3 tools/make_demos.py`. It fails loudly if a demo-only edit no longer applies.
3. Update the version table below and commit.

| Demo | Artifact | Snapshot version |
|---|---|---|
| build-slate | https://claude.ai/artifact/261U9aQ4SAaMf5bvhCFdpM | 1792119995-cea2 |
| roadmap | https://claude.ai/artifact/1CRcZoHYYrSDTUJGMVLUpc | 1792243476-857c |
| energy-scanner | https://claude.ai/artifact/VphgM8fKNVhcDc31RVdBJr | 1792454453-b0d3 |
| role-radar | https://claude.ai/artifact/YQFGobfPX9BKkv4yibcnsr | 1792568778-859e |

## Rules
- Never publish Chase's phone or email. LinkedIn is the contact route.
- Role Radar demo data is made up (companies, people, jobs, comp floor). Never copy real applications or recruiters into `demo/role-radar/seed.js`.
- Build Slate and roadmap seeds are snapshots of the real slate with private links and notes removed.
- The Hearth repo stays private and its name isn't final, so the site says "family photo app (name coming)".

## Next
- Chase: a single review pass of the pages.
- Hearth rename, then update `family-photos.html` copy.
- Optional: a "portfolio: feature / list / hidden" field in Build Slate so the site follows the slate.
