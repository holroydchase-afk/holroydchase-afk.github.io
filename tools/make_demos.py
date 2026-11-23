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

SOURCES = {  # demo name -> artifact the snapshot came from (links live in project memory; this repo is public)
    "energy-scanner": "energy-scanner bedtime artifact",
}
# Demo-only changes to the app itself, as (old, new) pairs.
EDITS = {
    # Start with a real reading; in the app a parent switch keeps every scan grey.
    "energy-scanner": [
        ('store.get("alwaysGrey",true)', 'store.get("alwaysGrey",false)'),
        # UX agent run UX-R2/R3/R10/R11 and the Grown-ups row (UX-R6); styles and the tap button live in tools/demo-fixes/.
        ('Press and hold to scan your energy', 'Scan my energy'),
        ('Put your hand on the scanner and hold', 'Tap Scan my energy, or hold your hand on the circle'),
        ('Too fast! Hold until the circle fills', 'Keep your hand on the circle'),
        ('<summary>Grown-ups</summary>', '<summary>Grown-ups: bedtime and settings</summary>'),
        ('<div class="hint" id="hint">', '<button class="scanbtn" id="scanBtn" type="button">Scan my energy</button>\n    <div class="hint" id="hint">'),
        ('$("reading").hidden=false;', '$("reading").hidden=false;$("reading").scrollIntoView({block:"nearest"});'),
    ],
}
FIXES = SRC.parent / "demo-fixes"


def build(name):
    t = (SRC / f"{name}.html").read_text(encoding="utf-8")
    t = re.sub(r'<meta name="claude:[^"]*"[^>]*>\s*', "", t)
    for old, new in EDITS.get(name, []):
        assert old in t, f"{name}: app changed, update EDITS ({old})"
        t = t.replace(old, new)
    css, js = FIXES / f"{name}.css", FIXES / f"{name}.js"
    if css.exists():
        assert '<canvas id="stars"' in t, f"{name}: app changed, update the style marker"
        t = t.replace('<canvas id="stars"', "<style>" + css.read_text(encoding="utf-8") + '</style>\n<canvas id="stars"', 1)
    if js.exists():
        marker = "renderSteps();tick();setInterval(tick,15000);"
        assert marker in t, f"{name}: app changed, update the fix marker"
        t = t.replace(marker, js.read_text(encoding="utf-8") + marker, 1)
    t = t.replace("<html>", '<html lang="en">', 1)
    t = t.replace("</head>", '<meta name="robots" content="noindex"><link rel="icon" href="../../assets/favicon.svg"></head>', 1)
    t = t.replace("<body>", '<body>\n<script src="seed.js"></script><script src="../fake-db.js"></script>\n', 1)
    out = ROOT / "demo" / name
    assert (out / "seed.js").exists(), f"{name}: write demo/{name}/seed.js first"
    (out / "index.html").write_text(t, encoding="utf-8")


if __name__ == "__main__":
    for name in SOURCES:
        build(name)
    print("Rebuilt", ", ".join(SOURCES))
