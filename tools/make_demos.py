"""Rebuild demo/<name>/index.html from the app snapshots in tools/demo-src/.

Each snapshot is the real app's page, saved from its Claude artifact (see SOURCES).
This script strips the artifact-only tags and loads the demo's seed.js and
../fake-db.js first, so the app runs on sample data in the visitor's browser.
Seeds (demo/<name>/seed.js) are edited by hand and never overwritten here.

To sync after an app changes: save its artifact page over tools/demo-src/<name>.html,
run `python3 tools/make_demos.py`, record the new version in HANDOFF.md, and commit.
"""
import re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "demo-src"

SOURCES = {  # demo name -> artifact the snapshot came from
    "energy-scanner": "https://claude.ai/artifact/VphgM8fKNVhcDc31RVdBJr",
    "role-radar": "https://claude.ai/artifact/YQFGobfPX9BKkv4yibcnsr",
}
# Demo-only changes to the app itself, as (old, new) pairs.
EDITS = {
    # Start with a real reading; in the app a parent switch keeps every scan grey.
    "energy-scanner": [('store.get("alwaysGrey",true)', 'store.get("alwaysGrey",false)')],
    # Portfolio shows the radar (scan, score, track), not resume drafting or the recruiter tracker (WEB-M3.4).
    "role-radar": [
        ('{id:"people",label:"Recruiters"},', ''),
        ('<button class="apply" data-apply="${id}">${resumeUrl?"Re-run intake":"Apply"}</button>', ''),
        ('${resumeUrl?`<a class="resume" href="${esc(resumeUrl)}" target="_blank" rel="noopener">${esc(j.resumeName||"Tailored resume")} ↗</a>`:(j.resumeName?`<span class="hint">Resume: ${esc(j.resumeName)}</span>`:`<span class="hint">Copies an intake prompt for a new chat</span>`)}', '<span class="hint">Every application is my own call, made by hand.</span>'),
        ('<label for="cCmd">Intake command<input id="cCmd" class="mono" value="${esc(config.intakeCommand)}"></label>', ''),
        ('<label for="cInstr">Intake instructions (added to every Apply prompt)<textarea id="cInstr">${esc(config.intakeInstructions)}</textarea></label>', ''),
        ('return "Resume ready, not submitted"', 'return "Ready, not submitted"'),
        ('intakeCommand:$("#cCmd").value.trim()||"/job-intake",intakeInstructions:$("#cInstr").value.trim()', ''),
        ('"Follow-ups due, stale applications and unsent resumes show up here."', '"Follow-ups due and stale applications show up here."'),
    ],
}


def build(name):
    t = (SRC / f"{name}.html").read_text(encoding="utf-8")
    t = re.sub(r'<meta name="claude:[^"]*"[^>]*>\s*', "", t)
    for old, new in EDITS.get(name, []):
        assert old in t, f"{name}: app changed, update EDITS ({old})"
        t = t.replace(old, new)
    t = t.replace("<html>", '<html lang="en">', 1)
    t = t.replace("</head>", '<meta name="robots" content="noindex"><link rel="icon" href="../../assets/favicon.svg"></head>', 1)
    t = t.replace("<body>", '<body>\n<script src="seed.js"></script><script src="../fake-db.js"></script>\n', 1)
    out = ROOT / "demo" / name
    assert (out / "seed.js").exists(), f"{name}: write demo/{name}/seed.js first"
    (out / "index.html").write_text(t, encoding="utf-8")


if __name__ == "__main__":
    for name in SOURCES:
        build(name)
    shutil.copy(SRC / "role-radar-scoring.js", ROOT / "demo" / "role-radar" / "scoring.js")
    print("Rebuilt", ", ".join(SOURCES))
