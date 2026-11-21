#!/usr/bin/env python3
"""Put prompts/<slug>.txt into each Tools card's "Make your own" button (home and building).
Run after editing a prompt; tools/check_site.py fails if a page drifts from its prompt file."""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CARDS = {
    "persona-twins": "Persona Twins",
    "hero-backgrounds": "Hero backgrounds",
    "build-slate-roadmap": "Build Slate and Roadmap",
    "share-start-tester": "Share start tester",
    "interview-flashcards": "Interview flashcards",
    "studio-agents-kit": "Studio agents kit",
    "screenshot-design-checker": "Screenshot and design-rule checker",
    "persona-check": "Persona check",
    "job-board-readers": "Job-board readers",
    "deploy-live-check": "Deploy live-check",
    "token-to-kwh-estimator": "Token-to-kWh estimator",
    "fruit-palettes": "Cut-open palettes",
    "live-color-tester": "Live color tester",
}
PAGES = ("index.html", "building.html")
BTN = '<button type="button" class="tl mk" data-mk="%s" data-prompt="%s">Make your own</button>'
ANY = re.compile(r'<button type="button" class="tl mk" data-mk="[a-z-]+" data-prompt="[^"]*">Make your own</button>')

if __name__ == "__main__":
    for page in PAGES:
        p = ROOT / page
        h = ANY.sub("", p.read_text())
        for slug, title in CARDS.items():
            text = (ROOT / "prompts" / f"{slug}.txt").read_text().strip()
            i = h.index(f"<h4>{title}</h4>")
            j = h.index('<div class="pl">', i)
            k = h.index("</div>", j)  # the link row holds no nested div
            h = h[:k] + BTN % (slug, html.escape(text, quote=True)) + h[k:]
        p.write_text(h)
