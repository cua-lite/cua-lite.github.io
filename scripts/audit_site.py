#!/usr/bin/env python3
"""Mechanical site audit — the checks that keep regressing, frozen as code.

Run after ANY content edit:  python3 scripts/audit_site.py
Exit 1 on any finding. Extend the lists when a review finds a new class of drift.
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [ROOT / "blog/why-cua-lite/index.html", ROOT / "index.html", ROOT / "blog/index.html"]

# hub entities must carry their hover class everywhere (entity grammar: same entity, same affordance)
HUB = {"LiteSample": "ls", "lite.gym": "lg", "adapter": "ad"}
# one word, one meaning — these spellings were unified and must not come back
BANNED = [
    (r"\bfolded\b", "use 'collapsed' (the repo's user-visible verb)"),
    (r"unified rows|the same rows", "name the entity: LiteSample rows"),
    (r"benchmark ships its own harness", "benchmark side says 'runner'; 'harness' belongs to agents"),
    (r"dies with the model", "unearned metaphor — say it plainly"),
]

# type scale: every font-size is a role (var(--fs-*)), never a raw number — the
# only literal px allowed are the body root and "scenography" (the depicted demo
# screens / animated figures, drawn at reduced device scale). See the type-scale
# comment block in css/style.css. This freezes the refactor so no one re-introduces
# a by-eye size.
SCENERY = re.compile(r'\.(win|sh|bw|gg|gs|ph|taskbar|tb|pair|chip-tag|node-sub|node-glyph|'
                     r'flow-lab|wire-stage|tape|tp|pack|mess)\b')
CSS_SOURCES = [ROOT / "css/style.css", ROOT / "blog/why-cua-lite/index.html",
               ROOT / "blog/index.html"]
fail = 0
for src in CSS_SOURCES:
    css = src.read_text()
    rel = src.relative_to(ROOT)
    for sel, decl in re.findall(r'([^{}]+)\{([^{}]*)\}', css, re.S):
        m = re.search(r'font-size:\s*[0-9.]+px', decl)
        if not m:
            continue
        last = sel.strip().split("\n")[-1].strip()
        if last == "body" or SCENERY.search(sel):
            continue
        print(f"{rel}: {last[:40]!r} sets a raw {m.group(0)} — use a var(--fs-*) role"); fail = 1

for page in PAGES:
    s = page.read_text()
    body = s[s.index("<main"):s.index("</main>")] if "<main" in s else s
    rel = page.relative_to(ROOT)
    if "why-cua-lite" in str(page):
        for name in HUB:
            for m in re.finditer(r"<code>(%s)</code>" % re.escape(name), body):
                print(f"{rel}: bare hub chip <code>{name}</code> — add class + tabindex"); fail = 1
        for m in re.finditer(r'<code class="(ls|lg|ad)"(?![^>]*tabindex)', body):
            print(f"{rel}: hover chip missing tabindex ({m.group(0)})"); fail = 1
    for pat, why in BANNED:
        for m in re.finditer(pat, body):
            print(f"{rel}: banned wording {m.group(0)!r} — {why}"); fail = 1

# the skim chain, for the human half of the audit
post = PAGES[0].read_text()
main = post[post.index("<main"):post.index("</main>")]
leads = re.findall(r"<p[^>]*><b[^>]*>(.*?)</b>", main, re.S)
clean = lambda t: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()
print("\nskim chain (read this aloud — it must be the whole argument):")
for i, l in enumerate(leads, 1):
    print(f"  {i}. {clean(l)}")
sys.exit(fail)
