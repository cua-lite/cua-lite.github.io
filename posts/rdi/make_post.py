"""Port a CUA-Lite blog post into the rdi-berkeley.github.io PR working copy.

    uv run python posts/rdi/make_post.py

Berkeley RDI's site is Jekyll, but a blog post does NOT have to be a Jekyll page. Their own
`blog/peer-preservation/index.html` carries no front matter and no `layout:` — its own doctype,
head, 20 KB of inline CSS, inline JS and `@keyframes` — and Jekyll copies it byte for byte
(verified against the built `_site`). So our post ships as what it already is: a live page with
its real front-end figures, not screen-recorded GIFs. Skipping their layout also skips the
Tailwind v2 preflight their markdown posts have to fight (OpenSage carries a
`.blog-post ul { list-style: disc }` purely to undo it).

That makes this script a path rewriter, not a converter. The one design decision worth stating:
the bundle mirrors THIS repo's directory shape —

    blog/cua-lite/index.html
    blog/cua-lite/css/style.css        <- its url('../assets/fonts/…') then resolves correctly
    blog/cua-lite/assets/fonts/*.woff2
    blog/cua-lite/js/*.js

— so `style.css` needs zero rewriting. Flattening it (style.css beside index.html) would send
every font url to `blog/assets/fonts/` and silently drop back to system fonts.

Two things deliberately stay on cua-lite.github.io rather than entering the PR:
  * the belt figure's 46 rollout MP4s (17 MB, against RDI's 3.6 MB largest single file)
  * the leaderboard's eval JSON
Both are fetched cross-origin; that origin sends `access-control-allow-origin: *` (verified).
The cost is real and belongs in the PR description: the RDI page's figures go blank if
cua-lite.github.io ever goes away.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent          # posts/rdi/ -> repo root
CLONE = Path(__file__).resolve().parent / "rdi-berkeley.github.io"
SITE = "https://cua-lite.github.io"

SLUG = "cua-lite"
SOURCE = "blog/why-cua-lite/index.html"
DONOR = "blog/kvm-free-osworld/index.html"

# Berkeley RDI's readers arrive from a blog index that never says what CUA-Lite is, so the
# post has to carry the whole argument AND the evidence for it. `why-cua-lite` alone is 553
# words — shorter than the shortest post on their site (813). The missing half already exists,
# audited, in `kvm-free-osworld`: the VM tax, the footprint table, and the 13-model parity plot.
# Merging is safe rather than lucky: the two pages share 16 selectors and NOT ONE of them
# differs in its declarations, and the donor's inline script drives exactly .v2c, .hh and .par
# — the three figures being moved. Verified, not assumed; `check_merge()` re-verifies on
# every build so a future edit to either page cannot silently break the other.
DONOR_SECTION = (r'<h2 id="vm-tax">', r'<figure class="par".*?</figure>')

# Placed between the section's claim ("VM-free sandboxes pack many to a machine") and the belt
# that shows the resulting family — claim, then evidence, then family. Demoted to h3 because
# it is a sub-part of Sandboxes, which is what `.post-wrap h3` in style.css exists for.
DONOR_ANCHOR = '  <figure class="belt-fig"'

TITLE = "CUA-Lite: An Open Platform for Computer-Use Agents"
# The <h1> needs the two hyphenated compounds glued: at 320px and below, Chrome breaks
# "Computer-Use" at its hyphen and the title reads as two words. `.nb` is the site's existing
# guard (white-space: nowrap). Plain TITLE still feeds <title> and og:title, which take no markup.
TITLE_HTML = ('<span class="nb">CUA-Lite</span>: An Open Platform for '
              '<span class="nb">Computer-Use</span> Agents')
TAGLINE = "Why CUA-Lite \u2014 and a call for contributors"
# Verbatim from the site's own citation block (index.html) — the only authoritative list.
# No institution superscripts: RDI's markdown posts carry them, but this repo holds no verified
# affiliation for any of these names, and their own standalone post (peer-preservation) shows
# no authors at all. An invented affiliation is worse than an absent one.
AUTHORS = ("Zhanhui Zhou, Weichen Zhang, Haoran Liu, Lingjie Chen, Tianneng Shi, "
           "Kevin Lin, Zhengyuan Yang, Lijuan Wang, Dawn Song")
DATE = "August 2026"
# The listing card. `blog.md` renders /blog from site.data.blogs, so a post without this entry
# is reachable only by direct URL — the single easiest thing to forget, hence it is generated,
# not hand-edited. Description is thread 01's opening, verbatim.
CARD_DATE = "2026-08-29"
CARD_DESC = ("Training and benchmarking computer-use agents takes three things: sandboxes, data, "
             "and a framework, and today all three are fragmented. CUA-Lite standardizes and "
             "democratizes all three: 30k+ verifiable tasks in VM-free sandboxes, 10+ SFT "
             "datasets, and one framework for rollout, eval, SFT and RL.")

TITLE_CSS = """.post-wrap p.post-sub { font-family: var(--serif); font-size: var(--fs-2xl); font-style: italic;
  color: var(--accent); line-height: 1.35; margin: -6px 0 14px; }
.post-wrap p.post-authors { font-size: var(--fs-md); line-height: 1.6; color: var(--dim); margin: 0 0 18px; }
.post-wrap p.post-res { margin-bottom: 34px; }
"""

# Files copied verbatim into blog/<SLUG>/, keeping this repo's relative shape (see docstring).
BUNDLE = [
    ("css/style.css", "css/style.css"),
    ("js/belt.js", "js/belt.js"),
    ("js/lspop.js", "js/lspop.js"),
    ("assets/fonts/Fraunces.woff2", "assets/fonts/Fraunces.woff2"),
    ("assets/fonts/Fraunces-Italic.woff2", "assets/fonts/Fraunces-Italic.woff2"),
    ("assets/fonts/Urbanist.woff2", "assets/fonts/Urbanist.woff2"),
    ("assets/fonts/GeistMono.woff2", "assets/fonts/GeistMono.woff2"),
    # style.css reaches these by RELATIVE url('../assets/…'), so they must be bundled, not
    # absolutised — and the three traj frames are the only pixels the figures actually show.
    ("assets/logo.svg", "assets/logo.svg"),
    ("assets/traj/desktop.png", "assets/traj/desktop.png"),
    ("assets/traj/web.png", "assets/traj/web.png"),
    ("assets/traj/mobile.png", "assets/traj/mobile.png"),
    ("assets/og.png", "assets/card.png"),      # the listing card
]

# Whole directories copied as-is. `assets/logos/` is referenced two ways — by the inline
# <style>'s url('/assets/logos/…') and by style.css's relative url('../assets/logos/…') — so
# enumerating individual files here just invites the next missing one.
BUNDLE_DIRS = ["assets/logos", "assets/icons", "assets/pixel"]

# Ordered: the local-bundle rules must run before the catch-all that absolutises what is left.
REWRITES = [
    (r'(?<=["\'])/css/', "css/"),
    (r'(?<=["\'])/js/', "js/"),
    (r'(?<=["\'])/assets/fonts/', "assets/fonts/"),
    # CSS url() — inside the inline <style>, and quoted or bare. These carry no href=/src=, so
    # the leftover guard below had to grow a url() arm to see them at all: the first port
    # shipped with four silent 404s (logo.svg and the three traj frames) that no assertion caught.
    (r'url\((["\']?)/assets/', r"url(\1assets/"),
    # favicons and og images are not worth bundling — point them home
    (r'(?<=["\'])/assets/', f"{SITE}/assets/"),
    # every remaining site-absolute href: "/", "/#sandboxes", "/blog/", …
    (r'(?<=href=")/(?=[#"]|blog/)', f"{SITE}/"),
]

# Our own site chrome must not appear on rdi.berkeley.edu. The nav bar ("Sandboxes / Data /
# Eval / Train / Datasets / GitHub / Blog") is another organisation's navigation on their
# domain, and every link in it walks the reader off the page; the footer's "← All posts" points
# at OUR blog index. RDI's own standalone post (peer-preservation) carries neither — just a
# title/subtitle/date header and a one-line footer. Each strip asserts it matched, so a
# restructured source fails loudly instead of silently republishing the nav.
STRIPS = [
    (r'<header class="nav">.*?</header>\s*', ""),
    (r'<footer class="blog-foot">.*?</footer>',
     '<footer class="blog-foot">\n'
     '  <span><a href="https://cua-lite.github.io">cua-lite.github.io</a>'
     ' — open sandboxes, data and infra.</span>\n'
     '</footer>'),
]

# belt.js resolves the rollout clips off a hardcoded site-absolute base.
JS_REWRITES = {"js/belt.js": [(r'"/blog/kvm-free-osworld/"', f'"{SITE}/blog/kvm-free-osworld/"')]}


def _blocks(html: str, tag: str, *, external: bool = False) -> list[str]:
    pat = rf"<{tag}[^>]*>(.*?)</{tag}>" if external else rf"<{tag}(?![^>]*src)[^>]*>(.*?)</{tag}>"
    return re.findall(pat, html, re.S)


def _decls(html: str) -> dict[tuple[str, str], str]:
    """(at-rule context, selector) -> sorted declarations, for every rule in the inline CSS.

    The context belongs in the key. A first cut flattened `@media` blocks into the top level,
    so `.flow-demo` inside a 640px breakpoint was compared against the other page's base
    `.flow-demo` and reported a conflict that does not exist — selectors legitimately repeat
    across breakpoints, and only same-context pairs can actually collide."""
    css = re.sub(r"/\*.*?\*/", "", "\n".join(_blocks(html, "style")), flags=re.S)
    out: dict[tuple[str, str], str] = {}
    stack: list[str] = []
    pre = ""
    for ch in css:
        if ch == "{":
            stack.append(re.sub(r"\s+", " ", pre).strip())
            pre = ""
        elif ch == "}":
            prelude = stack.pop() if stack else ""
            if not prelude.startswith("@"):
                ctx = next((p for p in stack if p.startswith("@")), "")
                out[(ctx, prelude)] = ";".join(sorted(x.strip() for x in pre.split(";") if x.strip()))
            pre = ""
        else:
            pre += ch
    return out


def check_merge(base: str, donor: str) -> None:
    """Fail the build if the two pages have started to disagree.

    Merging their stylesheets is only safe while every shared selector declares the same thing.
    Today 16 selectors are shared and none conflict; the day someone restyles `.flow-demo` in
    one page only, the merged post would silently take whichever came last — a defect that
    survives review because the figure still renders, just wrong."""
    a, b = _decls(base), _decls(donor)
    clash = sorted(sel for sel in set(a) & set(b) if a[sel] != b[sel])
    if clash:
        sys.exit("the two source pages now style the same selectors differently — merging them "
                 "would pick one at random:\n  " + "\n  ".join(clash))


def merge(base: str, donor: str) -> str:
    """Fold the donor's VM-tax subsection, and the CSS/JS it needs, into the base page."""
    check_merge(base, donor)

    start, end = DONOR_SECTION
    m = re.search(start + r".*?" + end, donor, re.S)
    if not m:
        sys.exit(f"donor section not found ({start} … {end}) — {DONOR} was restructured.")
    section = m.group(0).replace('<h2 id="vm-tax">', "<h3>").replace("</h2>", "</h3>", 1)

    if base.count(DONOR_ANCHOR) != 1:
        sys.exit(f"insertion anchor is not unique in {SOURCE}: {DONOR_ANCHOR!r}")
    base = base.replace(DONOR_ANCHOR, section + "\n\n" + DONOR_ANCHOR, 1)

    # Append the donor's inline CSS/JS after the base's own, so the base still wins any tie.
    # Duplicated rules are inert (check_merge proved they are identical); the donor's script is
    # self-contained and only touches .v2c / .hh / .par, which now exist on this page.
    css = "\n".join(_blocks(donor, "style"))
    js = "\n".join(_blocks(donor, "script"))
    base = base.replace("</head>", f"<style>\n{css}\n</style>\n</head>", 1)
    base = base.replace("</body>", f"<script>\n{js}\n</script>\n</body>", 1)
    return base


def retitle(html: str) -> str:
    """Swap the in-repo title block for one an RDI reader can enter cold.

    "Why CUA-Lite" presumes the reader knows what CUA-Lite is; on their blog index nothing has
    said so yet. The name-first form is both the project's settled tagline and RDI's own house
    pattern (ExploitGym:, OpenSage:, CyberGym-E2E:). The old h1 keeps its job as the subtitle.
    The resource row mirrors peer-preservation's Paper/Code buttons."""
    head = (f'  <p class="post-meta">{DATE}</p>\n'
            f'  <h1>{TITLE_HTML}</h1>\n'
            f'  <p class="post-sub">{TAGLINE}</p>\n'
            f'  <p class="post-authors">{AUTHORS}</p>\n'
            f'  <p class="post-links post-res">'
            f'<a href="https://cua-lite.github.io" target="_blank" rel="noopener">Site ↗</a>'
            f' &nbsp;·&nbsp; <a href="https://github.com/cua-lite/cua-lite" target="_blank" rel="noopener">Code ↗</a>'
            f' &nbsp;·&nbsp; <a href="https://huggingface.co/cua-lite" target="_blank" rel="noopener">Data ↗</a>'
            f'</p>\n')
    # Three items, not four. With Leaderboard the row wraps at 390px and strands the "·"
    # separator alone at the end of line one — a dangling separator reads as a typo. The
    # leaderboard is linked from the framework section's own sentence, so nothing is lost.
    old = re.search(r'  <p class="post-meta">.*?</h1>\n', html, re.S)
    if not old:
        sys.exit("title block not found — the article template changed.")
    html = html.replace(old.group(0), head, 1)

    # `.post-meta` is 2.5px-tracked uppercase mono, built for a one-line date — nine names in
    # it read as a wall. The subtitle and byline get their own rules, in the template's own
    # tokens so they stay part of the ladder rather than looking bolted on.
    html = html.replace("/* headings (h1 Title", TITLE_CSS + "/* headings (h1 Title", 1)
    html = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", html, count=1)
    html = re.sub(r'(<meta property="og:title" content=")[^"]*',
                  lambda mm: mm.group(1) + TITLE, html, count=1)
    return html + ""


def port() -> Path:
    out = CLONE / "blog" / SLUG
    if not CLONE.exists():
        sys.exit(f"PR working copy missing: {CLONE}\n"
                 f"  git clone git@github.com:ZHZisZZ/rdi-berkeley.github.io.git {CLONE}")
    shutil.rmtree(out, ignore_errors=True)

    for src, rel in BUNDLE:
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / src, dst)
        for pat, sub in JS_REWRITES.get(rel, []):
            t = dst.read_text()
            if not re.search(pat, t):
                sys.exit(f"{rel}: rewrite target vanished — {pat!r}. The source moved; fix this script.")
            dst.write_text(re.sub(pat, sub, t))

    for rel in BUNDLE_DIRS:
        shutil.copytree(ROOT / rel, out / rel, dirs_exist_ok=True)

    html = merge((ROOT / SOURCE).read_text(), (ROOT / DONOR).read_text())
    html = retitle(html)
    for pat, sub in REWRITES:
        html = re.sub(pat, sub, html)
    for pat, sub in STRIPS:
        html, n = re.subn(pat, sub, html, flags=re.S)
        if n != 1:
            sys.exit(f"strip matched {n} times, expected 1 — source restructured: {pat!r}")
    html = html.replace(f"{SITE}/blog/why-cua-lite/", f"https://rdi.berkeley.edu/blog/{SLUG}/")
    (out / "index.html").write_text(html)

    # A leftover "/…" would 404 against rdi.berkeley.edu's root, and a missing font degrades
    # silently to a system face — exactly the class of failure that is invisible in review.
    leftovers = sorted(set(re.findall(r'(?:href|src)="(/[^"]*)"', html)
                           + re.findall(r'url\(["\']?(/[^)"\']*)', html)))
    if leftovers:
        sys.exit("site-absolute paths still point at rdi.berkeley.edu's root:\n  "
                 + "\n  ".join(leftovers))
    for _, rel in BUNDLE:
        if not (out / rel).exists():
            sys.exit(f"bundle missing after copy: {rel}")

    # Resolve EVERY relative reference in the ported html and css against the bundle. Three
    # rounds of this port shipped with silent 404s — /assets/traj/*.png, then assets/logo.svg,
    # then the six assets/logos/* chips — each found only by screenshotting and reading the
    # console. A missing background-image leaves an empty box, which reviews right past.
    refs = set()
    for f in [out / "index.html", out / "css" / "style.css"]:
        t = f.read_text()
        refs |= {(f.parent, r) for r in re.findall(r'url\(["\']?([^)"\':]+?)["\']?\)', t)}
        refs |= {(f.parent, r) for r in re.findall(r'(?:href|src)="([^":]+?)"', t)}
    missing = sorted({r for base, r in refs
                      if not r.startswith(("#", "data:", "//"))
                      and not (base / r).resolve().exists()})
    if missing:
        sys.exit("relative references with no file in the bundle:\n  " + "\n  ".join(missing))
    return out


def register(out: Path) -> bool:
    """Insert (or refresh) this post's entry at the top of _data/blogs.yml. Newest first."""
    yml = CLONE / "_data" / "blogs.yml"
    body = yml.read_text()
    entry = (f"- link: /blog/{SLUG}\n"
             f"  img: /blog/{SLUG}/assets/card.png\n"
             f'  title: "{TITLE}"\n'
             f'  date: "{CARD_DATE}"\n'
             f'  description: "{CARD_DESC}"\n'
             f'  category: "main"\n')
    existing = re.search(rf"- link: /blog/{SLUG}\n(?:  .*\n)*", body)
    if existing:
        if existing.group(0) == entry:
            return False
        body = body.replace(existing.group(0), entry, 1)
    else:
        body = entry + "\n" + body
    yml.write_text(body)
    return True


def main() -> None:
    out = port()
    changed = register(out)
    n = sum(1 for p in out.rglob("*") if p.is_file())
    kb = sum(p.stat().st_size for p in out.rglob("*") if p.is_file()) / 1024
    print(f"wrote {out.relative_to(CLONE)} — {n} files, {kb:.0f} KB")
    print(f"_data/blogs.yml — {'entry written' if changed else 'entry already current'}")
    print(f"preview: cd {CLONE.relative_to(ROOT)} && ./preview.sh serve   # then :4111/blog/{SLUG}/")


if __name__ == "__main__":
    main()
