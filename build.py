#!/usr/bin/env python3
"""Genera il sito statico in dist/ a partire dai file Markdown in content/.

Uso:  pip install -r requirements.txt && python build.py
La cartella Galdus/ viene copiata IDENTICA, senza alcuna elaborazione.
"""
import re
import shutil
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
CONTENT, STATIC, TEMPLATES, OUT = (ROOT / d for d in ("content", "static", "templates", "dist"))
SITE_NAME = "Pietro Maffi"
GALDUS = {"label": "Galdus", "href": "/Galdus/", "order": 3}  # sezione intatta, voce di menu fissa


def parse(text):
    """Legge l'intestazione '---  chiave: valore  ---' e restituisce (meta, corpo)."""
    meta = {}
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = m.group(2)
    return meta, text


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    layout = (TEMPLATES / "layout.html").read_text(encoding="utf-8")
    md = markdown.Markdown(extensions=["extra", "sane_lists", "smarty"])

    pages = []
    for f in sorted(CONTENT.glob("*.md")):
        meta, body = parse(f.read_text(encoding="utf-8"))
        md.reset()
        title = meta.get("title", f.stem.capitalize())
        pages.append({
            "slug": f.stem,
            "title": title,
            "menu": meta.get("menu", title),  # "menu: -" = pagina fuori dal menu
            "order": int(meta.get("order", 50)),
            "lang": meta.get("lang", "it"),
            "html": md.convert(body),
        })

    entries = [(p["order"], p["menu"], "/" if p["slug"] == "index" else f"/{p['slug']}/", p)
               for p in pages if p["menu"] != "-"]
    entries.append((GALDUS["order"], GALDUS["label"], GALDUS["href"], None))
    entries.sort(key=lambda e: e[0])

    for p in pages:
        items = []
        for _, label, href, page in entries:
            cur = ' aria-current="page"' if page is p else ""
            items.append(f'<a href="{href}"{cur}>{label}</a>')

        page_title = SITE_NAME if p["slug"] == "index" else f'{p["title"]} · {SITE_NAME}'
        html = (layout
                .replace("{{page_title}}", page_title)
                .replace("{{lang}}", p["lang"])
                .replace("{{site_name}}", SITE_NAME)
                .replace("{{nav}}", "\n      ".join(items))
                .replace("{{content}}", p["html"])
                .replace("{{year}}", str(date.today().year))
                .replace("{{body_class}}", "home" if p["slug"] == "index" else "inner"))

        target = OUT / "index.html" if p["slug"] == "index" else OUT / p["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    if STATIC.exists():
        shutil.copytree(STATIC, OUT / "assets")

    galdus = ROOT / "Galdus"
    if galdus.exists() and any(galdus.iterdir()):
        shutil.copytree(galdus, OUT / "Galdus")  # copia fedele, nessuna modifica

    # Vecchio indirizzo del sito (/gs/) -> nuova home
    (OUT / "gs").mkdir()
    (OUT / "gs" / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>Pietro Maffi</title>'
        '<meta http-equiv="refresh" content="0; url=/"><link rel="canonical" href="/">'
        '<p>Il sito si è spostato: <a href="/">vai alla home</a>.</p>', encoding="utf-8")

    for extra in ("CNAME", "404.html"):
        if (ROOT / extra).exists():
            shutil.copy(ROOT / extra, OUT / extra)
    (OUT / ".nojekyll").write_text("")

    print(f"OK: {len(pages)} pagine generate in {OUT}")


if __name__ == "__main__":
    main()
