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

# The second donor section. `why-cua-lite`'s belt and `kvm-free-osworld`'s are the same figure
# with the same four tabs, so the merged page would show it twice; kvm-free's comes with the
# paragraph that actually names what the family runs (GMAT, PyMOL) and ends on "at scale", so
# its version replaces the bare one rather than joining it.
DONOR2_SECTION = (r'<h2>Beyond OSWorld: Scalable Training Sandboxes</h2>',
                  r'<figure class="belt-fig".*?</figure>')
BELT_START = '  <figure class="belt-fig" aria-label="Looping task trajectories across CUA-Lite sandboxes">'

# Homepage blocks. Each is a live component: the dataset browser and the leaderboard both come
# from index.html, and both are driven by js/main.js, which the bundle now carries.
HOME = "index.html"
HF_START = '    <figure class="hf-embed reveal">'
COV_START = '    <div class="cov reveal" id="leaderboard">'
LB_START = '    <div class="lb reveal" id="lb"'
DATA_CALL = '  <p class="post-call"><b class="call">Call for data contributors.</b>'
LITEGYM_START = '  <figure class="flow-demo" aria-label="Any environment paired with any agent'

# main.js gates every `.reveal` behind a `.js-reveal` class it sets on <html>, so importing it
# switches on the homepage's scroll choreography. We want its components, not its entrance:
# on someone else's site an observer that misses one element leaves that element permanently
# invisible, and a guest post should not introduce a whole class of blank-figure failure.
# main.js keeps the dataset browser and the coverage tabs inside one IIFE that opens with
# `const stage = document.getElementById("stage"); if (!stage) return;` — the homepage hero.
# On an article page that guard fires, so both blocks were shipping dead: the browser stuck on
# its loading skeleton forever, and the platform tabs inert. Splitting the guard is not an
# option — the hero half defines `clampMenu` and `reduce`, which the later half calls — and
# forking main.js for one page is worse. So the port re-binds exactly the two behaviours it
# needs, and strips the one control it cannot honestly wire (the dataset dropdown reads a list
# that only the homepage's collections fetch populates).
SHIM = """<script>
(function () {
  var f = document.getElementById("hf-frame");
  if (f && !f.querySelector("iframe")) {
    var i = document.createElement("iframe");
    i.loading = "lazy"; i.title = "CUA-Lite datasets on Hugging Face";
    i.src = "https://huggingface.co/datasets/cua-lite/WebGym/embed/viewer/default/train";
    i.addEventListener("load", function () { f.classList.add("loaded"); });
    f.appendChild(i);
  }
  var tabs = [].slice.call(document.querySelectorAll("#benchmarks .cov-tab"));
  var panels = [].slice.call(document.querySelectorAll("#benchmarks .cov-panel"));
  tabs.forEach(function (t) {
    t.addEventListener("click", function () {
      tabs.forEach(function (x) { x.classList.toggle("on", x === t); });
      panels.forEach(function (p) { p.classList.toggle("on", p.dataset.plat === t.dataset.plat); });
    });
  });
})();
</script>
"""

PORT_CSS = ("<style>/* port-only layout corrections; see make_post.py for why each exists */\n"
            # measured 0px against 18-30px after every other figure — the iframe's bottom row and
            # the pink call-out's top edge physically touch and read as one block
            ".post-wrap figure.hf-embed { margin-bottom: 22px; }\n"
            # the tab capsule is an inline-flex 412px block inside a 624px column; on the homepage
            # its section centres it, here it sat flush left with 212px of dead space beside it
            "#benchmarks .cov { text-align: center; }\n"
            "#benchmarks .cov-body, #benchmarks .cov-panel { text-align: left; }\n"
            # the composition side-panel is hidden below 1024px, but its trigger stayed visible —
            # an affordance that does nothing. And at 1280 it cleared the window by 29px.
            "@media (max-width: 1360px) { #lb-info { display: none; } }\n"
            # an h3 sat 10px above its body copy while two ordinary paragraphs sit 22px apart,
            # gluing the subsection heading to the text and flattening the h2/h3 ladder
            ".post-wrap h3 { margin: 34px 0 14px; }\n</style>\n")

OFFLINE_CSS = ("<style>/* if the cross-origin clips cannot load, show the reason, not an empty box */\n"
               ".belt-offline .belt-tabs, .belt-offline .belt { display: none; }\n"
               ".belt-offline .belt-cap { padding-top: 0; }\n</style>\n")

REVEAL_OFF = ("<style>/* main.js drives the components here, not the homepage's entrance "
              "animation */\n.js-reveal .reveal { opacity: 1; transform: none; transition: none; }"
              "\n</style>\n")

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
# The post runs four sections deep, which is one more than either source page had, so it gets
# the same numbered contents nav `kvm-free-osworld` uses — and its `.toc` CSS is already here,
# carried in with that page's stylesheet. Ids are written out rather than slugified so they are
# stable, readable anchors that a reader can link to. The highlight marks the section carrying
# the post's distinctive claim; the badge says what the heading itself does not.
TOC = [("why", "Why CUA-Lite", None),
       ("sandboxes", "Sandboxes & verifiable tasks", None),
       ("datasets", "Datasets", None),
       ("framework", "One framework: eval & RL", None)]

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
    ("js/main.js", "js/main.js"),        # drives the HF browser and the leaderboard
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
BUNDLE_DIRS = ["assets/icons", "assets/pixel"]

# assets/logos/ is copied FILE BY FILE, not wholesale: the directory also holds berkeley.svg
# and microsoft.svg, which nothing on this page references. Committing an unused UC Berkeley
# logo into UC Berkeley's own repository is not a good look, and dead bytes in a PR invite
# questions that have nothing to do with the post.
LOGO_DIR = "assets/logos"

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
    # Our favicons would put the CUA-Lite mark in the browser tab on rdi.berkeley.edu — the
    # same borrowed-identity problem as the nav, one line lower. peer-preservation declares
    # none and inherits the host's. Three <link rel=icon> lines, so this strip expects 3.
    (r'\s*<link rel="(?:apple-touch-)?icon"[^>]*>', "", 3),
    (r'<footer class="blog-foot">.*?</footer>',
     '<footer class="blog-foot">\n'
     '  <span><a href="https://cua-lite.github.io">cua-lite.github.io</a>'
     ' — open sandboxes, data and infra.</span>\n'
     '</footer>'),
]

# belt.js resolves the rollout clips off a hardcoded site-absolute base.
# Both scripts fetch from cua-lite.github.io. On our own site that is same-origin — a failure
# means the whole site is down. Here we are a third party on someone else's permanent URL, so
# the failure paths matter, and both of them lie:
#   * belt.js swallows the error and renders an empty strip under four dead tabs;
#   * main.js renders the leaderboard's "0 runs / eval pending" ghost, which sits directly under
#     the sentence "the leaderboard is live" and reads as "we have no results".
# Neither is acceptable on a host's domain. Say what actually happened instead.
JS_REWRITES = {
    "js/belt.js": [
        (r'"/blog/kvm-free-osworld/"', f'"{SITE}/blog/kvm-free-osworld/"'),
        (r'\.catch\(\(\) => \(\{ hh: \{\}, belt: \{\} \}\)\);',
         '.catch(() => { document.querySelectorAll(".belt-fig").forEach((f) => {'
         ' f.classList.add("belt-offline");'
         ' const c = f.querySelector(".belt-cap");'
         ' if (c) c.textContent = "Rollout clips are served from cua-lite.github.io and could not be loaded.";'
         ' }); return { hh: {}, belt: {} }; });'),
    ],
    # The leaderboard reads its scores from a path relative to the page, which on
    # rdi.berkeley.edu would resolve inside the post's own directory.
    "js/main.js": [
        (r'const ROOT = "assets/exps/eval/"', f'const ROOT = "{SITE}/assets/exps/eval/"'),
        (r'\.catch\(\(\) => \{ if \(fresh\(\)\) renderGhost\("empty"\); \}\);',
         '.catch(() => { if (fresh()) { renderGhost("empty"); lbOffline(); } });'),
        # The manifest is fetched first, so when the origin is unreachable THIS is the catch that
        # fires — an offline drill (routing cua-lite.github.io to abort) still showed "0 runs /
        # eval pending" until this one was covered too. Guarding only the per-run fetch tested
        # nothing, because that fetch never happens.
        (r'\.then\(\(r\) => \(r\.ok \? r\.json\(\) : \{\}\)\)\.catch\(\(\) => \(\{\}\)\)',
         '.then((r) => (r.ok ? r.json() : {})).catch(() => { lbOffline(); return {}; })'),
        # One helper, defined next to the element it writes to.
        # A flag, not a direct write: renderGhost() sets foot.innerHTML immediately afterwards,
        # so the first version of this fix was overwritten and the offline drill still showed
        # "0 runs / eval pending". Only the drill caught it — the code looked right.
        (r'(const foot = document\.getElementById\("lb-foot"\);)',
         '\\1\\n  let lbDown = false;\\n  const lbOffline = () => { lbDown = true; };'),
        (r'foot\.innerHTML = kind === "empty"',
         'foot.innerHTML = lbDown'
         ' ? `<span>scores unavailable</span><span>served from cua-lite.github.io</span>`'
         ' : kind === "empty"'),
    ],
}


def element(html: str, start: str, what: str) -> str:
    """The whole element beginning with the line `start`, closed at the same indent.

    A tag-counting scan is the obvious approach and it is wrong here: `<div` also occurs inside
    attribute values, so counting reported the benchmark-coverage block as 7 lines when it is 34.
    The homepage is consistently indented, so the matching close is the first line that is
    exactly this line's indent plus `</tag>`."""
    lines = html.split("\n")
    hits = [i for i, l in enumerate(lines) if l.startswith(start)]
    if len(hits) != 1:
        sys.exit(f"{what}: expected 1 match for {start!r}, found {len(hits)}")
    i = hits[0]
    indent = start[:len(start) - len(start.lstrip())]
    tag = re.match(r"\s*<([a-z]+)", start).group(1)
    close = f"{indent}</{tag}>"
    for j in range(i + 1, len(lines)):
        if lines[j] == close:
            return "\n".join(lines[i:j + 1])
    sys.exit(f"{what}: no closing {close!r}")


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
    # The four native headings are sentence case with no Title-Case subtitle; the two lifted ones
    # arrive as "…: How we cut it…" / "…: Scalable Training Sandboxes". Matching the local ladder
    # is the point of demoting them in the first place.
    section = section.replace(": How we cut it with", ", and how we cut it with")

    # The splice drops the donor page's lede, so the merged post's first prose mention of
    # OSWorld was "OSWorld's faithful desktop is a full VM per task" — an adjective with no
    # antecedent, in front of a whole subsection and four figures about a benchmark the reader
    # was never introduced to. These two sentences are that lede, verbatim; the "faithful"
    # echo one paragraph later is the source page's own.
    lede = re.search(r"<p><b>To eval or train a computer-use agent.*?scaling\.", donor, re.S)
    if not lede:
        sys.exit("the donor's OSWorld lede moved; the merged post would name OSWorld unintroduced")
    # Keep the source's bold. Stripping it made this the only paragraph in the article with no
    # bold lead, which breaks the project's hard rule that reading only the bold must stand alone
    # as the whole argument — and two consecutive bold leads is exactly how the source reads.
    intro = "  " + lede.group(0) + "</p>\n"
    section = section.replace("</h3>", "</h3>\n" + intro, 1)

    if base.count(DONOR_ANCHOR) != 1:
        sys.exit(f"insertion anchor is not unique in {SOURCE}: {DONOR_ANCHOR!r}")
    base = base.replace(DONOR_ANCHOR, section + "\n\n" + DONOR_ANCHOR, 1)

    m2 = re.search(DONOR2_SECTION[0] + r".*?" + DONOR2_SECTION[1], donor, re.S)
    if not m2:
        sys.exit(f"donor section 2 not found — {DONOR} was restructured.")
    beyond = (m2.group(0).replace("<h2>", "<h3>", 1).replace("</h2>", "</h3>", 1)
              .replace("Beyond OSWorld: Scalable Training Sandboxes",
                       "Beyond OSWorld: scalable training sandboxes"))
    old_belt = element(base, BELT_START, "the base page's belt figure")
    base = base.replace(old_belt, beyond, 1)

    home = (ROOT / HOME).read_text()
    hf = element(home, HF_START, "the Hugging Face dataset browser")
    drop = re.search(r'<span class="hf-ds" id="hf-select">.*?</span></span>', hf, re.S)
    if not drop:
        sys.exit("the dataset dropdown markup moved; check it is still safe to strip")
    hf = hf.replace(drop.group(0), '<span class="hf-ds">WebGym</span>', 1)
    if base.count(DATA_CALL) != 1:
        sys.exit("the data call-out moved; cannot place the dataset browser")
    base = base.replace(DATA_CALL, hf + "\n\n" + DATA_CALL, 1)

    # The benchmark grid and the leaderboard are the evidence for the framework section's own
    # claim ("15+ benchmarks are already integrated, and the leaderboard is live"), so they go
    # directly after the figure that claim sits under.
    # Both blocks go inside a #benchmarks wrapper. main.js reads the coverage cards as its
    # single source of environments via `#benchmarks .cov-panel .row[data-env]`, and switches
    # the tabs via `#benchmarks .cov-tab` — without that ancestor the leaderboard initialises,
    # renders its bar, and then sits empty forever, having never fetched a single score.
    # Satisfying the selector is better than forking the script for one page.
    gym = element(base, LITEGYM_START, "the lite.gym figure")
    cov = element(home, COV_START, "the benchmark grid")
    # The homepage marks the leaderboard's current env with `row hl`; without it no cell is
    # selected while the board below plainly shows OSWorld, so the two read as unrelated.
    if 'data-env="osworld"' not in cov:
        sys.exit("the benchmark grid has no osworld row to mark as selected")
    cov = cov.replace('<a class="row" data-env="osworld"', '<a class="row hl" data-env="osworld"', 1)

    bench = ('  <div id="benchmarks">\n'
             + cov + "\n\n"
             + element(home, LB_START, "the leaderboard") + "\n  </div>")
    base = base.replace(gym, gym + "\n\n" + bench, 1)

    # Append the donor's inline CSS/JS after the base's own, so the base still wins any tie.
    # Duplicated rules are inert (check_merge proved they are identical); the donor's script is
    # self-contained and only touches .v2c / .hh / .par, which now exist on this page.
    css = "\n".join(_blocks(donor, "style"))
    js = "\n".join(_blocks(donor, "script"))
    # An empty result reads exactly like a successful one: check_merge() would then compare {}
    # against the base, find no shared selectors, and report clean — strongest precisely when
    # the thing it guards has vanished. The .v2c/.hh/.par figures would ship unstyled and dead.
    for name, blob, probe in (("style", css, ".v2c"), ("script", js, ".par-svg")):
        if probe not in blob:
            sys.exit(f"the donor's inline {name} no longer contains {probe} — "
                     f"the merged figures would ship broken")
    base = base.replace("</head>", f"<style>\n{css}\n</style>\n</head>", 1)
    base = base.replace("</body>", f"<script>\n{js}\n</script>\n" + SHIM + "</body>", 1)
    # Anchored on the PRE-rewrite path. merge() runs before REWRITES, so the page still says
    # "/js/belt.js" here; targeting the rewritten "js/belt.js" matched nothing and shipped a
    # bundle containing main.js that no <script> tag ever loaded — silently, because a bare
    # str.replace that matches nothing is indistinguishable from one that worked.
    tag = '<script src="/js/belt.js">'
    if base.count(tag) != 1:
        sys.exit(f"cannot place the main.js tag: {tag!r} appears {base.count(tag)} times")
    base = base.replace(tag, '<script src="/js/main.js"></script>\n' + tag, 1)
    base = base.replace("</head>", REVEAL_OFF + OFFLINE_CSS + PORT_CSS + "</head>", 1)
    return base


def add_toc(html: str) -> str:
    """Give each h2 an id and insert the numbered contents nav after the resource row."""
    heads = re.findall(r"<h2>(.*?)</h2>", html, re.S)
    if len(heads) != len(TOC):
        sys.exit(f"{len(heads)} h2 sections but TOC lists {len(TOC)} — update TOC in this script:\n  "
                 + "\n  ".join(re.sub(r"\s+", " ", h).strip() for h in heads))
    for (slug, label, _), raw in zip(TOC, heads):
        plain = re.sub(r"\s+", " ", re.sub(r"<[^>]*>", "", raw)).strip().replace("&amp;", "&")
        if plain != label:
            sys.exit(f"section drifted: TOC says {label!r}, page says {plain!r}")
        html = html.replace(f"<h2>{raw}</h2>", f'<h2 id="{slug}">{raw}</h2>', 1)

    rows = []
    for i, (slug, label, badge) in enumerate(TOC, 1):
        cls = ' class="toc-hl"' if badge else ""
        tag = f'<span class="toc-badge">{badge}</span>' if badge else ""
        rows.append(f'    <a href="#{slug}"{cls}><span class="toc-n">{i:02d}</span>'
                    f'{label.replace("&", "&amp;")}{tag}</a>')
    nav = '  <nav class="toc" aria-label="Contents">\n' + "\n".join(rows) + "\n  </nav>\n"

    # Anchor on the resource row itself. "</p> … <h2" is not unique — every section ends that
    # way — and a nav dropped at the first match would land mid-article.
    html, n = re.subn(r'(<p class="post-links post-res">.*?</p>\n)',
                      lambda m: m.group(1) + "\n" + nav, html, count=1, flags=re.S)
    if n != 1:
        sys.exit("could not place the contents nav: the resource row moved")
    return html


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
    anchor = "/* headings (h1 Title"      # a source COMMENT — the most editable text there is
    if html.count(anchor) != 1:
        sys.exit(f"cannot inject the title-block CSS: {anchor!r} appears {html.count(anchor)} times")
    html = html.replace(anchor, TITLE_CSS + anchor, 1)
    for pat, rep, what in ((r"<title>[^<]*</title>", lambda m: f"<title>{TITLE}</title>", "<title>"),
                           (r'(<meta property="og:title" content=")[^"]*', None, "og:title")):
        rep = rep or (lambda m: m.group(1) + TITLE)
        html, n = re.subn(pat, rep, html, count=1)
        if n != 1:
            sys.exit(f"{what} not rewritten — the post would ship under the source page's title")
    # One description, three places. The source page's own description opens "Why CUA-Lite
    # exists" — the same cold-reader problem the title had — and leaving it would give this
    # post two different summaries: this one in the <head>, CARD_DESC on RDI's blog index.
    # og:image must be served by the host, not by us: a social preview that depends on a
    # third-party origin breaks the moment that origin does, and the bundle already ships the
    # same file as assets/card.png for the blog index.
    # The precedent post ships four twitter:* tags; without twitter:card the 2400x1260 card
    # is cropped to a small square when the post is shared.
    tw = (f'<meta name="twitter:card" content="summary_large_image" />\n'
          f'<meta name="twitter:title" content="{TITLE}" />\n'
          f'<meta name="twitter:description" content="{CARD_DESC}" />\n'
          f'<meta name="twitter:image" content="https://rdi.berkeley.edu/blog/{SLUG}/assets/card.png" />\n')
    html = html.replace('<meta property="og:type"', tw + '<meta property="og:type"', 1)

    html, n = re.subn(r'(<meta property="og:image" content=")[^"]*',
                      lambda mm: mm.group(1) + f"https://rdi.berkeley.edu/blog/{SLUG}/assets/card.png",
                      html, count=1)
    if n != 1:
        sys.exit("og:image meta not found")
    for pat in (r'(<meta name="description" content=")[^"]*',
                r'(<meta property="og:description" content=")[^"]*'):
        html, n = re.subn(pat, lambda mm: mm.group(1) + CARD_DESC, html, count=1)
        if n != 1:
            sys.exit(f"description meta not found: {pat!r}")
    return html


def port() -> Path:
    out = CLONE / "blog" / SLUG
    if not CLONE.exists():
        sys.exit(f"PR working copy missing: {CLONE}\n"
                 f"  git clone git@github.com:ZHZisZZ/rdi-berkeley.github.io.git {CLONE}")
    shutil.rmtree(out, ignore_errors=True)

    # Which logos does the finished page reference? Compute it from the merged HTML *and* the
    # stylesheet, before copying, so the bundle carries exactly those.
    html_probe = (merge((ROOT / SOURCE).read_text(), (ROOT / DONOR).read_text())
                  + (ROOT / "css/style.css").read_text())

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

    # Only the logos this page actually references (see LOGO_DIR's note above).
    (out / LOGO_DIR).mkdir(parents=True, exist_ok=True)
    wanted = set(re.findall(r"assets/logos/([\w.-]+)", html_probe))
    if not wanted:
        sys.exit("no assets/logos/* referenced — the figure chips changed; check before shipping")
    for f in sorted((ROOT / LOGO_DIR).iterdir()):
        if f.name in wanted:
            shutil.copy2(f, out / LOGO_DIR / f.name)

    html = merge((ROOT / SOURCE).read_text(), (ROOT / DONOR).read_text())
    html = add_toc(retitle(html))
    # These two point at our homepage's sections — but this page now carries the benchmark grid
    # and the live leaderboard itself. Sending a reader to another domain for content that is
    # 20 lines below them is a defect, and neither link carries target="_blank", so it navigates
    # away in place. Run BEFORE the rewrites, while the paths are still site-absolute.
    for frm, to in (('href="/#benchmarks"', 'href="#benchmarks"'),
                    ('href="/#leaderboard"', 'href="#leaderboard"')):
        if frm not in html:
            sys.exit(f"self-link rewrite found no {frm!r} — the source changed")
        html = html.replace(frm, to)

    for pat, sub in REWRITES:
        html = re.sub(pat, sub, html)
    # The source pages carry long authoring comments (the NORTH STAR block: "cut anything a
    # scanner can't use (mechanism, scope lists, hedging)", the prose-hygiene rules). Those are
    # ours to follow, not to publish on rdi.berkeley.edu, where View Source shows them next to
    # the copy they govern. Strip every HTML comment; <style>/<script> bodies are unaffected
    # because `<!--` does not occur inside them.
    html = re.sub(r"<!--.*?-->\n?", "", html, flags=re.S)

    for rule in STRIPS:
        pat, sub, want = (*rule, 1)[:3]
        html, n = re.subn(pat, sub, html, flags=re.S)
        if n != want:
            sys.exit(f"strip matched {n} times, expected {want} — source restructured: {pat!r}")
    # og:url is the only place the source page's own canonical URL survives; unrewritten, every
    # share of the guest post credits cua-lite.github.io. Derive the slug from SOURCE rather than
    # repeating it, so renaming the source file cannot leave this behind.
    src_url = f"{SITE}/blog/{Path(SOURCE).parent.name}/"
    if src_url not in html:
        sys.exit(f"og:url still points at {src_url} and no rewrite matched")
    html = html.replace(src_url, f"https://rdi.berkeley.edu/blog/{SLUG}/")
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
