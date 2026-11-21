#!/usr/bin/env python3
"""Put prompts/<slug>.txt into each tool card's "Make your own" button (home and building).
Run after editing a prompt; tools/check_site.py fails if a page drifts from its prompt file."""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CARDS = {"fruit-palettes": "Cut-open palettes", "share-start-tester": "Share start tester"}
PAGES = ("index.html", "building.html")
BTN = '<button type="button" class="tl mk" data-mk="%s" data-prompt="%s">Make your own</button>'
OLD = re.compile(r'<button type="button" class="tl mk" data-mk="%s" data-prompt="[^"]*">Make your own</button>')

for page in PAGES:
    p = ROOT / page
    h = p.read_text()
    for slug, title in CARDS.items():
        btn = BTN % (slug, html.escape((ROOT / "prompts" / f"{slug}.txt").read_text().strip(), quote=True))
        if re.search(OLD.pattern % slug, h):
            h = re.sub(OLD.pattern % slug, lambda m: btn, h)
            continue
        i = h.index(f"<h4>{title}</h4>")
        j = h.index('<div class="pl">', i)
        k = h.index("</div>", j)  # the link row holds no nested div
        h = h[:k] + btn + h[k:]
    p.write_text(h)
