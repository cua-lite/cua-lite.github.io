"""Render every media asset the launch thread references into twitter/assets/.

The thread's copy lives in twitter/README.md; this script produces the files it points
at, so a re-run after a site edit keeps the thread in sync with the page.

    uv run python twitter/make_assets.py            # everything
    uv run python twitter/make_assets.py 02 04b     # only assets whose name matches
    uv run python twitter/make_assets.py gif        # only the .gif beside each .mp4

HOW THE MOTION IS CAPTURED — the site's flow figures ARE the argument (a still of a
wire mid-draw says nothing), so most assets are clips. Three approaches were tried;
only the third keeps them both sharp and true to the page:

  ✗ Playwright's record_video — low-bitrate VP8 at CSS-pixel size; anything cropped
    out of it has to be upscaled and turns to mush.
  ✗ CDP screencast — real frame timing, but it captures at CSS resolution and ignores
    deviceScaleFactor entirely (verified). scripts/make_demo_gif.py works around that
    by CSS-`zoom`ing the hero demo before capture, which is fine there because that
    demo is pure CSS. It does NOT work for the pair-boards: their wires are drawn by JS
    from getBoundingClientRect (visual px under zoom) into an SVG with no viewBox
    (layout px), so every wire overshoots by the zoom factor. Widening the column
    instead of zooming is worse — it stretches the boards away from how the site looks.
  ✓ page.screenshot(clip=…, type="jpeg") on a DPR-2 context — ~5-20 fps at true device
    pixels, natural layout, no upscaling anywhere. Frame timestamps are kept so the
    concat list replays the real tempo.

Every clip is a capture of a figure the SITE already uses to make that argument —
including its tabs, labels and caption. Nothing here composes a new visual.

The hero clip is not re-invented here: scripts/make_demo_gif.py already renders it for
the main repo's README, so this script just calls it (see hero()).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "assets"
TMP = Path("/tmp/cua-twitter")
PORT = 8146
BASE = f"http://localhost:{PORT}"
FFMPEG = shutil.which("ffmpeg") or "/home/zzh/.local/bin/ffmpeg"

DPR = 2                       # every capture is at 2× device pixels, never upscaled after
BG = "0xfaf4e8"               # --bg, the site's ivory canvas
BG_RGB = (250, 244, 232)
MARGIN = 30                   # cream margin around a figure, in CSS px (×DPR in output)
MAX_AR, MIN_AR = 2.45, 1.2    # X rejects past 3:1; keep every card inside a sane band
MAX_W = 1920                  # X's ceiling — downscale to it, never up


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def serve_html(page, html: str) -> None:
    """Open ad-hoc markup FROM the site's own origin, so its @font-face files resolve."""
    (ROOT / "_tw_tmp.html").write_text(html)
    page.goto(f"{BASE}/_tw_tmp.html")
    page.wait_for_timeout(700)


def make_mark(ctx) -> Path:
    """The wordmark stamped on every asset, rendered once in the site's own mono."""
    page = ctx.new_page()
    serve_html(page, """<!doctype html><meta charset="utf-8"><style>
        @font-face{font-family:'Geist Mono';src:url('/assets/fonts/GeistMono.woff2') format('woff2');}
        html,body{margin:0;background:transparent;}
        span{font-family:'Geist Mono',monospace;font-size:13px;letter-spacing:1.1px;color:#a89e8c;}</style>
        <span id="m">cua-lite.github.io</span>""")
    out = TMP / "_mark.png"
    page.locator("#m").screenshot(path=str(out), omit_background=True)
    page.close()
    return out


def frame_box(w: int, h: int, min_ar: float | None = MIN_AR) -> tuple[int, int]:
    """Canvas for a capture w×h (device px): cream margin, aspect in band, inside X's envelope.

    min_ar=None lets a tall capture stay portrait — X allows down to 1:3 and shows
    portrait media large on mobile, which beats shrinking it into a landscape frame."""
    m = MARGIN * DPR
    cw, ch = w + 2 * m, h + 2 * m
    ch = max(ch, int(cw / MAX_AR))                       # too wide → grow taller
    if min_ar:
        cw = max(cw, int(ch * min_ar))                   # too tall → grow wider
    lim_w, lim_h = (MAX_W, 1200) if cw >= ch else (1200, MAX_W)
    k = min(lim_w / cw, lim_h / ch, 1.0)
    return int(cw * k) // 2 * 2, int(ch * k) // 2 * 2


def fit_inside(w: int, h: int, cw: int, ch: int) -> tuple[int, int]:
    """Content size that fits the canvas minus its margins — downscale only, never up."""
    m = MARGIN * DPR
    k = min((cw - 2 * m) / w, (ch - 2 * m) / h, 1.0)
    return max(2, int(w * k) // 2 * 2), max(2, int(h * k) // 2 * 2)


# ---------------------------------------------------------------- stills

def still(ctx, out: str, url: str, selector: str, *, wait: int = 2200, mark: Path | None = None,
          viewport=(1180, 950), js: str | None = None, min_ar: float | None = MIN_AR) -> None:
    page = ctx.new_page()
    page.set_viewport_size({"width": viewport[0], "height": viewport[1]})
    page.goto(BASE + url)
    el = page.locator(selector).first
    el.scroll_into_view_if_needed()
    if js:
        page.evaluate(js)
    page.wait_for_timeout(wait)
    raw = TMP / ("raw_" + out)
    el.screenshot(path=str(raw))
    page.close()
    img = Image.open(raw)
    cw, ch = frame_box(img.width, img.height, min_ar)
    sw, sh = fit_inside(img.width, img.height, cw, ch)
    if (sw, sh) != img.size:
        img = img.resize((sw, sh), Image.LANCZOS)
    card = Image.new("RGB", (cw, ch), BG_RGB)
    card.paste(img, ((cw - img.width) // 2, (ch - img.height) // 2))
    if mark:
        m = Image.open(mark)
        card.paste(m, (cw - m.width - 26, ch - m.height - 20), m)
    card.save(OUT / out)
    print(f"  wrote {out} {card.size}")


def still_span(ctx, out: str, url: str, selectors: list[str], *, wait: int = 1800,
               mark: Path | None = None, viewport=(1400, 1200), js: str | None = None,
               min_ar: float | None = MIN_AR) -> None:
    """A still cropped to the union of several boxes — for content that is text, not motion.

    The train panels are the case in point: they are static terminals, so a clip of them is
    a 2 fps slideshow. As stills they land at full @2x sharpness, and X shows two of them
    side by side (SFT and RL) in one post."""
    page = ctx.new_page()
    page.set_viewport_size({"width": viewport[0], "height": viewport[1]})
    page.goto(BASE + url)
    page.add_style_tag(content="header.nav{display:none !important}")
    if js:                       # before the scroll: js may be what reveals the target panel
        page.evaluate(js)
        page.wait_for_timeout(500)
    page.locator(selectors[0]).first.scroll_into_view_if_needed()
    page.wait_for_timeout(wait)
    el = span_el(page, *selectors)
    b = el.bounding_box()
    pad = 14
    raw = TMP / ("raw_" + out)
    page.screenshot(path=str(raw), clip={"x": max(0, b["x"] - pad), "y": max(0, b["y"] - pad),
                                         "width": b["width"] + 2 * pad, "height": b["height"] + 2 * pad})
    page.close()
    img = Image.open(raw)
    cw, ch = frame_box(img.width, img.height, min_ar)
    sw, sh = fit_inside(img.width, img.height, cw, ch)
    if (sw, sh) != img.size:
        img = img.resize((sw, sh), Image.LANCZOS)
    card = Image.new("RGB", (cw, ch), BG_RGB)
    card.paste(img, ((cw - img.width) // 2, (ch - img.height) // 2))
    if mark:
        m = Image.open(mark)
        card.paste(m, (cw - m.width - 26, ch - m.height - 20), m)
    card.save(OUT / out)
    print(f"  wrote {out} {card.size}")


# ---------------------------------------------------------------- clips

# Each figure on a post folds and unfolds on its own clock, so the page's flow keeps
# shifting — a figure near the bottom (where the view can no longer scroll) slides out
# from under a fixed crop. Pin every figure at its tallest state first, then measure.
WATCH_HEIGHTS = """
  window.__figs = [...document.querySelectorAll('figure, .belt-fig, .cov, #train, [data-train-panel]')];
  window.__maxh = window.__figs.map(f => f.getBoundingClientRect().height);
  window.__watch = setInterval(() => window.__figs.forEach((f, i) => {
    window.__maxh[i] = Math.max(window.__maxh[i], f.getBoundingClientRect().height);
  }), 150);
"""
FREEZE_HEIGHTS = """
  clearInterval(window.__watch);
  window.__figs.forEach((f, i) => { f.style.minHeight = window.__maxh[i] + 'px'; });
"""


# Left-align the column and drop the sticky nav: with a page-scale factor the visible
# region is the TOP-LEFT quarter of the layout viewport, so a centred figure would fall
# outside it, and the fixed nav would sit on top of the frame.
CAST_CSS = ("header.nav{display:none !important}"
            ".post-wrap{margin-left:0 !important;padding-left:16px !important}"
            ".container{margin-left:0 !important;margin-right:auto !important}")


def cast(page, el, secs: float, tag: str, *, scale: int = 2, margin: int = 14,
         drive=None) -> tuple[Path, tuple[int, int, int, int]]:
    """Screencast a figure at `scale`× device pixels, at the page's own frame rate.

    Why this and not a screenshot loop: page.screenshot(clip=…) costs 50-200 ms a frame,
    which caps a capture at 5-14 fps and reads as stutter. CDP screencast delivers frames
    as the page repaints (~28 fps here) but always at CSS resolution — so the pixels come
    from Emulation.setPageScaleFactor instead, which scales the RASTER while leaving
    layout coordinates untouched. That last part matters: CSS `zoom` would double the
    pixels too, but the pair-boards compute their wire paths from getBoundingClientRect,
    and under zoom those come back in visual px while the SVG still measures in layout px,
    so every wire overshoots. Page scale has no such effect.
    """
    import base64
    # Size the viewport from the box's RIGHT EDGE, not its width: at page-scale N the
    # visible region is only viewport/N wide starting at x=0, and the page centres content
    # inside its container — sizing by width alone leaves the right half outside the frame.
    for _ in range(3):                       # each resize reflows the page; settle on a box
        page.evaluate("window.__castFit && window.__castFit()")
        b = el.bounding_box()
        vw = min(2400, int((b["x"] + b["width"] + margin) * scale))
        vh = min(2000, int((b["height"] + 2 * margin) * scale))
        if page.viewport_size == {"width": vw, "height": vh}:
            break
        page.set_viewport_size({"width": vw, "height": vh})
        page.wait_for_timeout(350)
    el.evaluate(f"el => {{ const r = el.getBoundingClientRect(); window.scrollBy(0, r.top - {margin}); }}")
    page.wait_for_timeout(300)
    page.evaluate("window.__castFit && window.__castFit()")
    b = el.bounding_box()
    cdp = page.context.new_cdp_session(page)
    cdp.send("Emulation.setPageScaleFactor", {"pageScaleFactor": scale})
    page.wait_for_timeout(300)

    fdir = TMP / f"frames_{tag}"
    shutil.rmtree(fdir, ignore_errors=True)
    fdir.mkdir(parents=True)
    frames: list[tuple[float, bytes]] = []
    cdp.on("Page.screencastFrame", lambda e: (
        frames.append((e["metadata"]["timestamp"], base64.b64decode(e["data"]))),
        cdp.send("Page.screencastFrameAck", {"sessionId": e["sessionId"]})))
    cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 95, "everyNthFrame": 1})
    t0 = time.monotonic()
    while True:
        t = time.monotonic() - t0
        if t >= secs:
            break
        if drive:
            drive(t)
        page.wait_for_timeout(120)
    cdp.send("Page.stopScreencast")
    page.wait_for_timeout(250)

    lines = []
    t_end = frames[-1][0] if frames else 0          # hold the last frame for the rest of the
    span = t_end - frames[0][0] if frames else 0    # take, so a still tail isn't cut short
    tail = max(0.3, min(2.5, secs - span))
    for i, (ts, data) in enumerate(frames):
        (fdir / f"{i:05d}.jpg").write_bytes(data)
        dur = (frames[i + 1][0] - ts) if i + 1 < len(frames) else tail
        # a screencast emits nothing while the page is still, so a long gap IS a hold —
        # keep it (capped only against a stall), or a mostly-static panel plays 3× too fast
        lines.append(f"file \'{i:05d}.jpg\'\nduration {max(0.02, min(dur, 2.5)):.3f}")
    if frames:
        lines.append(f"file '{len(frames) - 1:05d}.jpg'")
    (fdir / "list.txt").write_text("\n".join(lines) + "\n")
    print(f"    {len(frames)} frames · {len(frames) / max(secs, 0.1):.1f} fps")
    crop = (int((b["x"] - margin) * scale), int((b["y"] - margin) * scale),
            int((b["width"] + 2 * margin) * scale), int((b["height"] + 2 * margin) * scale))
    return fdir, crop



def seam_cut(path: Path, target: float, window: float | None = None, step: float = 0.04) -> float:
    """The end time nearest `target` whose frame best matches frame 0 — a clean loop wrap.

    X autoplays these on repeat, so the wrap is a visible edit. Trimming to a whole number
    of the figure's animation cycles gets close, but encoded time drifts from page time, so
    the last few frames are compared to the first and the best match wins."""
    from PIL import ImageChops, ImageStat
    window = window if window is not None else max(0.9, target * 0.09)   # long clips drift more
    ref = TMP / "_seam_ref.png"
    run([FFMPEG, "-y", "-loglevel", "error", "-ss", "0.05", "-i", str(path),
         "-frames:v", "1", str(ref)])
    a = Image.open(ref).convert("RGB")
    best, best_d = target, 1e9
    t = max(0.5, target - window)
    while t <= target + window:
        cand = TMP / "_seam_c.png"
        run([FFMPEG, "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(path),
             "-frames:v", "1", str(cand)])
        b = Image.open(cand).convert("RGB")
        if b.size == a.size:
            d = sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3
            if d < best_d:
                best, best_d = t, d
        t += step
    print(f"    seam: {best:.2f}s (diff {best_d:.2f})")
    return best


def encode(fdir: Path, out: str, *, mark: Path | None = None, fps: int = 30,
           min_ar: float | None = MIN_AR, crop: tuple[int, int, int, int] | None = None,
           dur: float | None = None) -> None:
    """Frame sequence → X-ready mp4, centred on the cream card with the wordmark."""
    fw, fh = Image.open(sorted(fdir.glob("*.jpg"))[0]).size
    if crop:
        cx, cy, w, h = crop
        cx, cy = max(0, cx), max(0, cy)
        w, h = min(w, fw - cx) // 2 * 2, min(h, fh - cy) // 2 * 2
    else:
        cx = cy = 0
        w, h = fw, fh
    cw, ch = frame_box(w, h, min_ar)
    sw, sh = fit_inside(w, h, cw, ch)
    pre = f"crop={w}:{h}:{cx}:{cy}," if crop else ""
    vf = f"{pre}scale={sw}:{sh}:flags=lanczos,setsar=1,pad={cw}:{ch}:(ow-iw)/2:(oh-ih)/2:{BG}"
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
           "-i", str(fdir / "list.txt")]
    if mark:
        cmd += ["-i", str(mark), "-filter_complex",
                f"[0:v]{vf}[v];[v][1:v]overlay=W-w-26:H-h-20,format=yuv420p[out]", "-map", "[out]"]
    else:
        cmd += ["-vf", vf + ",format=yuv420p"]
    tail = ["-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
            "-r", str(fps), "-fps_mode", "cfr", "-movflags", "+faststart"]
    if not dur:
        run(cmd + tail + [str(OUT / out)])
    else:
        tmp = TMP / ("full_" + out)          # encode in full, find the wrap point, then cut
        run(cmd + tail + [str(tmp)])
        cut = seam_cut(tmp, dur)
        run([FFMPEG, "-y", "-loglevel", "error", "-i", str(tmp), "-t", f"{cut:.3f}"]
            + tail + [str(OUT / out)])
    print(f"  wrote {out} {cw}x{ch}")


def figure_clip(browser, out: str, url: str, selector: str, *, secs: float = 13,
                settle: float = 7.0, viewport=(1400, 900), mark=None, extra_css: str = "",
                cycle: float | None = None) -> None:
    """Record one live figure at the site's own layout width, over full animation loops."""
    ctx = browser.new_context(viewport={"width": viewport[0], "height": viewport[1]})
    page = ctx.new_page()
    t0 = time.monotonic()
    page.goto(BASE + url)
    page.add_style_tag(content=CAST_CSS + extra_css)
    page.evaluate(WATCH_HEIGHTS)
    el = page.locator(selector).first
    el.evaluate("el => el.scrollIntoView({block: 'center'})")
    while time.monotonic() - t0 < settle:      # let every figure reach its tallest state…
        page.wait_for_timeout(200)
    page.evaluate(FREEZE_HEIGHTS)              # …then pin the flow so the crop can't drift
    page.wait_for_timeout(400)
    fdir, crop = cast(page, el, secs, out.replace(".mp4", ""))
    page.close()
    ctx.close()
    dur = (int(secs / cycle) * cycle) if cycle else None
    encode(fdir, out, mark=mark, crop=crop, dur=dur)


def span_el(page, *selectors: str):
    """A zero-cost stand-in element spanning several page elements, so `cast` can frame them.

    The eval command and its leaderboard (and the train tabs, their note, pickers and
    terminal) are separate boxes with other content between them; measuring a span is
    simpler than compositing crops, and keeps the page's own spacing intact. Pass every
    box that must stay inside frame — a missed one gets sliced at the edge."""
    page.evaluate("""(sels) => {
        const d = document.getElementById('__cast') || document.createElement('div');
        d.id = '__cast';
        Object.assign(d.style, {position: 'absolute', pointerEvents: 'none', zIndex: -1});
        if (!d.parentNode) document.body.appendChild(d);
        // re-fit on demand: cast() resizes the viewport, which reflows the page, and a div
        // pinned to the old geometry would crop the wrong region
        window.__castFit = () => {
            const rs = sels.map(s => document.querySelector(s)).filter(Boolean)
                           .filter(e => e.offsetParent !== null || e.getClientRects().length)
                           .map(e => e.getBoundingClientRect());
            if (!rs.length) return;
            d.style.left = (Math.min(...rs.map(r => r.left)) + scrollX) + 'px';
            d.style.top = (Math.min(...rs.map(r => r.top)) + scrollY) + 'px';
            d.style.width = (Math.max(...rs.map(r => r.right)) - Math.min(...rs.map(r => r.left))) + 'px';
            d.style.height = (Math.max(...rs.map(r => r.bottom)) - Math.min(...rs.map(r => r.top))) + 'px';
        };
        window.__castFit();
    }""", list(selectors))
    return page.locator("#__cast")


def leaderboard_clip(browser, out: str, mark: Path) -> None:
    """One command, any benchmark — as a result, not a claim.

    Walks four real boards (desktop → web → mobile → grounding); the eval command's
    --env-id and the leaderboard update together, so the frame holds both. Every board is
    visited BEFORE the span is measured, and the heights pinned, so the tallest board
    can't get sliced off at the frame edge mid-tour."""
    TOUR = [("Desktop", "osworld"), ("Web", "webharbor.webvoyager"),
            ("Mobile", "androidworld"), ("Grounding", "screenspot_pro"),
            ("Desktop", "osworld")]          # back to the first board: the clip loops
    HOLD = 3.2
    pick = """document.querySelector('.cov-tab[data-plat="%s"]').click();
        const r = [...document.querySelectorAll('.cov-panel.on .row')]
                    .find(r => r.dataset.env === '%s'); if (r) r.click();"""
    ctx = browser.new_context(viewport={"width": 1400, "height": 1100})
    page = ctx.new_page()
    page.goto(BASE + "/")
    page.add_style_tag(content=CAST_CSS + ".cov,.lb,.cmdbuild{margin-left:0 !important}")
    page.locator("#benchmarks").scroll_into_view_if_needed()
    page.wait_for_timeout(2600)                      # boards fetch their run JSON
    page.evaluate(WATCH_HEIGHTS)
    for plat, env in TOUR:
        page.evaluate(pick % (plat, env))
        page.wait_for_timeout(1500)
    page.evaluate(FREEZE_HEIGHTS)
    page.wait_for_timeout(500)
    el = span_el(page, ".cmdbuild[data-cmd='eval'] .term", "#lb .lb-card")
    state = {"i": -1, "next": 0.0}

    def drive(t: float) -> None:
        if t < state["next"]:
            return
        state["i"] += 1
        if state["i"] < len(TOUR):
            page.evaluate(pick % TOUR[state["i"]])
            state["next"] = t + HOLD

    fdir, crop = cast(page, el, len(TOUR) * HOLD + 0.8, "leaderboard", drive=drive)
    page.close()
    ctx.close()
    encode(fdir, out, mark=mark, min_ar=None, crop=crop)


def tabbed_clip(browser, out: str, url: str, selector: str, tab_sel: str, mark: Path,
                *, secs: float = 20, hold: float = 5.0, settle: float = 5.0,
                viewport=(1400, 900), min_ar=MIN_AR, extra_css: str = "",
                cycle: float | None = None, order: list[int] | None = None) -> None:
    """Capture one of the site's own tabbed figures, walking its tabs while it records.

    Used for the rollout belt and the OSWorld/Lite.OSWorld player: both already ARE the
    visual the site uses for this argument — tabs, labels and caption included."""
    ctx = browser.new_context(viewport={"width": viewport[0], "height": viewport[1]})
    page = ctx.new_page()
    page.goto(BASE + url)
    page.add_style_tag(content=CAST_CSS + extra_css)
    page.evaluate(WATCH_HEIGHTS)
    el = page.locator(selector).first
    el.evaluate("el => el.scrollIntoView({block: 'center'})")
    page.wait_for_timeout(int(settle * 1000))      # clips load and start playing
    page.evaluate(FREEZE_HEIGHTS)
    page.wait_for_timeout(400)
    n_tabs = page.locator(f"{selector} {tab_sel}").count()
    order = order or list(range(n_tabs))
    stops = order + [order[0]]                # …and back to the first, so the loop wraps clean
    state = {"i": -1}

    # Open on the chosen tab BEFORE the first frame — a tab switch takes ~0.3s to settle, and
    # frame 0 is the poster image X shows before autoplay, so a click at t=0 leaves the poster
    # on whichever tab happened to be default.
    page.evaluate(f"""document.querySelectorAll('{selector} {tab_sel}')[{stops[0]}].click();""")
    page.wait_for_timeout(900)
    state["i"] = 0

    def drive(t: float) -> None:
        nxt = int(t // hold)
        if nxt != state["i"] and nxt < len(stops):
            state["i"] = nxt
            page.evaluate(f"""document.querySelectorAll('{selector} {tab_sel}')[{stops[nxt]}].click();""")

    fdir, crop = cast(page, el, secs, out.replace(".mp4", ""), drive=drive)
    page.close()
    ctx.close()
    dur = (int(secs / cycle) * cycle) if cycle else None
    encode(fdir, out, mark=mark, min_ar=min_ar, crop=crop, dur=dur)


def hero(mark: Path) -> None:
    """01 · the hero demo — regenerated by the repo's own tuned generator, not copied.

    Output is the `demo-trace` crop (device above its rollout trace), pixel-for-pixel the
    look of assets/demo-trace.mp4: the generator's default white ground, native size, no
    wordmark. (The poster-frame artifact that clip has — the phone still on screen while the
    trace reads "--platform desktop" — was fixed in the generator itself, not worked around
    here; see the probe-restore beat in scripts/make_demo_gif.py.)

    (This is the one asset not on the site's cream card; it is the project's canonical demo
    and matching it beats matching the other eight.)
    """
    print("hero: scripts/make_demo_gif.py")
    out = TMP / "hero-white"
    run([sys.executable, str(ROOT / "scripts" / "make_demo_gif.py"), "--out", str(out),
         "--port", "8973"])
    for src, dst in (("demo-trace.mp4", "01-hero.mp4"),          # portrait — the default
                     ("demo-trace-side.mp4", "01-hero-wide.mp4")):  # landscape alternate
        shutil.copyfile(out / src, OUT / dst)
        print("  wrote", dst)


def gifs(width: int = 800, fps: int = 16) -> None:
    """A .gif beside every .mp4 — for surfaces that won't take video (GitHub, Slack, docs).

    Two-pass palette, same as scripts/make_demo_gif.py: one palette generated from the whole
    clip (stats_mode=diff weights the moving pixels) and sierra2_4a dithering, which is what
    keeps flat cream and thin terracotta strokes from banding. Downscaled and slowed to 16fps
    because a full-resolution gif of these runs to hundreds of MB; X takes the mp4 anyway."""
    print("gifs:")
    for mp4 in sorted(OUT.glob("*.mp4")):
        out = mp4.with_suffix(".gif")
        vf = f"fps={fps},scale={width}:-1:flags=lanczos"
        pal = TMP / "_pal.png"
        run([FFMPEG, "-y", "-loglevel", "error", "-i", str(mp4),
             "-vf", f"{vf},palettegen=max_colors=256:stats_mode=diff", str(pal)])
        run([FFMPEG, "-y", "-loglevel", "error", "-i", str(mp4), "-i", str(pal),
             "-lavfi", f"{vf}[x];[x][1:v]paletteuse=dither=sierra2_4a", "-loop", "0", str(out)])
        print(f"  wrote {out.name}  {out.stat().st_size / 1e6:.1f}MB")


# ---------------------------------------------------------------- the asset set

def build(browser, ctx, mark: Path, want) -> None:
    if want("01-hero"):
        hero(mark)

    # 02 · the status quo drawing itself — every dataset/benchmark reaching every agent,
    #      each pairing failing into the same grey tangle
    if want("02-fragmented"):
        print("clip: 02-fragmented")
        figure_clip(browser, "02-fragmented.mp4", "/blog/why-cua-lite/",
                    "figure.flow-demo.mess", secs=14, cycle=5.93, mark=mark)   # LEAD+3*BEAT+500+1900

    # 03 · the whole VM-tax argument in one loop: sealed VM → container → parallel rollouts
    if want("03-vm-tax"):
        print("clip: 03-vm-tax")
        figure_clip(browser, "03-vm-tax.mp4", "/blog/kvm-free-osworld/",
                    "figure.flow-demo.v2c", secs=15.5, cycle=7.0, mark=mark)

    # spares · the receipts behind post 3's numbers, for a reply or a quote-tweet
    if want("extra-footprint"):
        print("stills:")
        still(ctx, "extra-footprint.png", "/blog/kvm-free-osworld/", "figure.cmp", mark=mark)
    if want("extra-parity"):
        still(ctx, "extra-parity.png", "/blog/kvm-free-osworld/", "figure.par", mark=mark,
              min_ar=None,      # the plot is portrait; padding it landscape wastes a third of the card
              js="""document.querySelector('.par-cap').textContent =
                      'OSWorld vs Lite.OSWorld · 13 models · identical tasks';""")

    # 04 · the Lite.* family — the site's own rollout belt, walked across all four tabs
    if want("04-sandboxes"):
        print("clip: 05-family")
        # 44s is the belt's own scroll period (css: beltscroll 44s linear infinite), so a
        # clip of exactly that length wraps with the marquee back where it started; the four
        # families + a return to the first divide it into comfortable 8.8s holds
        # The marquee is a 44s loop, so no 10s cut of it can wrap cleanly — and at 2.6s a tab
        # it is also just noise. Pause it (a state the site itself has, on hover): the tiles
        # hold still long enough to read, each family's caption gets its beat, and the clip
        # loops without the belt snapping sideways.
        tabbed_clip(browser, "04-sandboxes.mp4", "/blog/why-cua-lite/", ".belt-fig", ".belt-tab",
                    mark, secs=11.0, hold=2.6, settle=8,
                    order=[3, 2, 1, 0],      # CUAWorld (GMAT/PyMOL) first — the unfamiliar one
                    extra_css=".belt-cap{visibility:hidden !important}"
                              ".belt-track{animation-play-state:paused !important}")

    # 05 · convert once, train anything: datasets fold into LiteSample, adapters pack it per model
    if want("05-litesample"):
        print("clip: 06-litesample")
        figure_clip(browser, "05-litesample.mp4", "/blog/why-cua-lite/",
                    "figure.flow-demo:has([data-board='data'])", secs=12, settle=9.5,
                    cycle=5.2, mark=mark)          # runBoard's own setInterval(cycle, 5200)

    # 06 · the loop itself: screenshots up, actions down, any env ⇄ any agent through lite.gym
    if want("06-litegym"):
        print("clip: 07-litegym")
        figure_clip(browser, "06-litegym.mp4", "/blog/why-cua-lite/",
                    # 2 cycles only reached one env/agent pair; 4 walks the ladder across the
                    # board, which is what the post and its alt text describe
                    "figure.flow-demo:has([data-board='pair'])", secs=22, settle=10.5,
                    cycle=5.2, mark=mark)

    # 07 · the boards those commands fill
    if want("07-leaderboard"):
        print("clip: 07-leaderboard")
        leaderboard_clip(browser, "07-leaderboard.mp4", mark)

    # 08 · the training half: SFT on the corpora, RL in the envs. Two stills, not a clip:
    #      these panels are static terminals, so a capture of them was a 2 fps slideshow
    #      with the code too small to read. As stills they keep full @2x sharpness, and X
    #      shows the pair side by side.
    if want("08a-sft"):
        print("stills: train")
        still_span(ctx, "08a-sft.png", "/", [".train-tabs", ".panel-note", ".sft-cfg",
                                             "[data-train-panel='sft'] .term"], mark=mark)
    if want("08b-rl"):
        still_span(ctx, "08b-rl.png", "/", [".train-tabs", ".panel-note",
                                            "[data-train-panel='rl'] .term"], mark=mark,
                   js="document.querySelector('.train-tab[data-train=\"rl\"]').click();")

    # 09 · closing brand card (the site's own social card)
    if want("09-card"):
        shutil.copyfile(ROOT / "assets" / "og.png", OUT / "09-card.png")
        print("  wrote 09-card.png (copied from assets/og.png)")

    # spare · same model, same task, VM vs container — the post's own player, kept for
    # replies / quote-tweets
    if want("extra-side-by-side"):
        print("clip: extra-side-by-side")
        tabbed_clip(browser, "extra-side-by-side.mp4", "/blog/kvm-free-osworld/",
                    "figure.hh", ".hh-tab", mark, secs=18, hold=6.0,
                    extra_css=".hh-cap{visibility:hidden !important}")


def main() -> None:
    only = [a for a in sys.argv[1:] if a != "gif"]
    only_gifs = "gif" in sys.argv[1:]
    want = lambda tag: not only or any(o in tag for o in only)
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    server = None
    try:
        import urllib.request
        urllib.request.urlopen(BASE, timeout=1)
    except Exception:
        server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)], cwd=ROOT,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.2)
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={"width": 1180, "height": 950}, device_scale_factor=DPR)
            mark = make_mark(ctx)
            if not only_gifs:
                build(browser, ctx, mark, want)
            ctx.close()
            browser.close()
        if only_gifs or not only:
            gifs()
    finally:
        (ROOT / "_tw_tmp.html").unlink(missing_ok=True)
        if server:
            server.terminate()


if __name__ == "__main__":
    main()
