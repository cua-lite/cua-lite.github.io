"""Build every image and clip for the X/Twitter launch thread, from the live site.

═══ HOW TO REPRODUCE — read this first; the plain command does NOT work on this host ═══

1. Start Chrome yourself and point the script at it. Playwright's own launch() is broken
   here (PITFALL 1), so capture goes through CDP:

     ~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome \
       --headless --no-sandbox --disable-gpu --disable-dev-shm-usage \
       --remote-debugging-port=9401 --user-data-dir=/tmp/pw &
     until curl -sf http://127.0.0.1:9401/json/version >/dev/null; do sleep 0.5; done

2. Render mp4s (the script starts its own http server for the site):

     CUA_LITE_CDP=http://127.0.0.1:9401 uv run python posts/twitter/01/make_assets.py
     CUA_LITE_CDP=http://127.0.0.1:9401 uv run python posts/twitter/01/make_assets.py 07-sandboxes

3. SEPARATELY, build GIFs from those mp4s:

     uv run python posts/twitter/01/make_assets.py gif

   Steps 2 and 3 cannot be combined — PITFALL 2.

On a host where Playwright works, drop step 1 and CUA_LITE_CDP; nothing else changes.

═══ PITFALLS — each cost a debugging round and none is obvious from the traceback ═══

1. Playwright cannot launch Chromium here. The child dies instantly with SIGTRAP and no
   stderr, so the only symptom is "BrowserType.launch: Target page, context or browser has
   been closed". Ruled out by bisection: every revision (1208/1217/1223/1228, headless_shell
   and full chrome), with and without --no-sandbox / --single-process / --no-zygote; memory,
   disk, /dev/shm and sandboxing are all fine; the same binary run by hand works. The break
   is in Playwright's --remote-debugging-pipe path. connect_over_cdp() is unaffected — hence
   CUA_LITE_CDP.

2. `gif` SKIPS the capture. main() reads `if not only_gifs: build(...)`, so passing `gif`
   alongside clip names silently renders nothing. And gifs() takes no filter: it rebuilds
   EVERY GIF in assets/, not only the ones you named.

3. The conda ffmpeg/ffprobe on this host cannot load libiconv.so.2 and dies on every call.
   FFMPEG/FFPROBE therefore prefer /usr/bin explicitly. Do not simplify back to
   shutil.which().

4. /usr/bin ffmpeg is 4.4, which has no `-fps_mode` (added in 5.0). CFR carries the right
   flag for the detected version; the wrong one exits 1 with "Unrecognized option".

5. run() used to swallow stdout AND stderr, so every failure above surfaced as a bare
   CalledProcessError and had to be reproduced by hand to learn anything. It now raises with
   the tail of the real error plus the full command. Do not revert that.

6. A crop can run off the captured frame. bounding_box() is measured BEFORE
   Emulation.setPageScaleFactor, so at scale=2 a tall figure yields a crop past the frame
   bottom — ffmpeg rejects it, once with a negative height. cast() now clamps to the frame.
   Raising the viewport does NOT help (it pushes the element further down); if a figure still
   looks cut, lower `scale` for that clip.

7. Pacing does NOT come from HOLD/hold. cast() derives each frame's duration from CDP
   screencast timestamps, and a screencast emits nothing while the page is still — a static
   beat becomes one frame stretched to the 2.5 s cap. 05-leaderboard once shipped 5 boards in
   16 s with a 6.5 s dead stretch while its HOLD read 3.2. retime() pins the finished file to
   an exact duration and trims the opening dwell (`head=`). Tune retime(), not HOLD.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent.parent   # posts/twitter/01/ -> repo root
OUT = Path(__file__).resolve().parent / "assets"
TMP = Path("/tmp/cua-twitter")
PORT = 8146
BASE = f"http://localhost:{PORT}"
# /usr/bin first: the conda build on this host cannot load libiconv.so.2 and dies on
# every invocation, which is silent here because run() swallows stderr.
FFMPEG = next((c for c in ("/usr/bin/ffmpeg", shutil.which("ffmpeg")) if c and Path(c).exists()), "ffmpeg")
# ffmpeg 4.x uses -vsync; -fps_mode arrived in 5.0. Detect once — an unsupported flag
# makes ffmpeg exit 1 with "Unrecognized option", which run() hides entirely.
def _cfr_flag() -> list[str]:
    try:
        v = subprocess.run([FFMPEG, "-version"], capture_output=True, text=True).stdout
        return ["-fps_mode", "cfr"] if int(re.search(r"ffmpeg version (\d+)", v).group(1)) >= 5 else ["-vsync", "cfr"]
    except Exception:
        return ["-vsync", "cfr"]


FFPROBE = next((c for c in ("/usr/bin/ffprobe", shutil.which("ffprobe")) if c and Path(c).exists()), "ffprobe")

CFR = _cfr_flag()
DPR = 2                       # every capture is at 2× device pixels, never upscaled after
BG = "0xfaf4e8"               # --bg, the site's ivory canvas
BG_RGB = (250, 244, 232)
MARGIN = 30                   # cream margin around a figure, in CSS px (×DPR in output)
MAX_AR, MIN_AR = 2.45, 1.2    # X rejects past 3:1; keep every card inside a sane band
MAX_W = 1920                  # X's ceiling — downscale to it, never up


def run(cmd: list[str]) -> None:
    """Run a subprocess and, on failure, SHOW WHY.

    The original swallowed stdout and stderr, so every ffmpeg failure surfaced as a bare
    CalledProcessError and had to be reproduced by hand to learn anything. Three separate
    pitfalls in this file were invisible for exactly that reason:
      * the conda ffmpeg/ffprobe on this host cannot load libiconv.so.2 and dies instantly;
      * `-fps_mode` does not exist before ffmpeg 5.0 ("Unrecognized option");
      * a crop rectangle taller than the captured frame is rejected outright.
    Each one cost a manual re-run to diagnose. Now the message comes back with the error.
    """
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        err = (r.stderr or r.stdout or "").strip().splitlines()
        raise RuntimeError(f"{cmd[0]} failed (exit {r.returncode}):\n  "
                           + "\n  ".join(err[-6:] or ["<no output>"])
                           + f"\n  full command: {' '.join(cmd)}")


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
    # full_page is not optional: a clip that reaches past the viewport bottom is SILENTLY cut
    # without it. 08a-sft's union runs to y=1362 in a 1200px viewport — 176px of the command
    # block were missing from every capture, and the shipped PNG ends flush at the frame edge
    # with no window border. (A note in this thread's README blamed `.term { overflow: hidden }`;
    # measured, the live element is overflow:visible with clientHeight == scrollHeight.)
    # full_page is not optional: a clip reaching past the viewport bottom is SILENTLY cut without
    # it. 08a-sft's union runs to y=1362 in a 1200px viewport — 176px of the command block were
    # missing from every capture. (This thread's README blamed `.term { overflow: hidden }`;
    # measured, that element is overflow:visible with clientHeight == scrollHeight.)
    # bounding_box() is viewport-relative but a full_page clip is DOCUMENT-relative, so the
    # scroll offset has to be added back — without it the clip lands on a different section
    # entirely, which is a louder failure than the one being fixed but a failure all the same.
    sy = page.evaluate("window.scrollY")
    page.screenshot(path=str(raw), full_page=True,
                    clip={"x": max(0, b["x"] - pad), "y": max(0, b["y"] + sy - pad),
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
CAST_CSS = (# Hide every scrollbar. At scale=1 the page is tall relative to the viewport, so a
            # scrollbar renders INSIDE the captured frame and lands in the crop — a grey
            # bar down the right edge of the finished clip. Not visible at scale=2, which
            # is why it went unnoticed until 06 moved to 1x.
            "*{scrollbar-width:none !important}"
            "*::-webkit-scrollbar{display:none !important;width:0 !important;height:0 !important}"
            "header.nav{display:none !important}"
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
    # RE-MEASURE. setPageScaleFactor reflows the page, so the box measured above is stale —
    # at scale=2 a figure that sat mid-viewport can end up below the captured frame, and the
    # crop derived from the stale box then points outside it. Scroll it back into view and
    # take the box again; `scale` is not applied twice because these coordinates are already
    # in the zoomed layout.
    # Do NOT re-measure here and do NOT set scale = 1. bounding_box() returns LAYOUT
    # coordinates, which setPageScaleFactor does not change — so a "re-measure" returns the
    # same numbers, and dropping the ×scale then crops only the top-left quarter of the
    # figure. The ×scale is correct; what fails is a figure taller than viewport/scale, which
    # lands past the captured frame. Fix that by giving the clip a taller `viewport`, not by
    # touching the arithmetic here. Also do NOT call el.evaluate() after setPageScaleFactor:
    # running page script at this point wedges the CDP session, and the process then blocks
    # in do_poll forever with no error and no timeout.

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
        # Clamp the ORIGIN into the frame too, not just above zero. When cy lands past the
        # frame bottom, `fh - cy` goes negative and min() happily returns a NEGATIVE height,
        # which ffmpeg rejects with "Invalid too big or non positive size". Seen for real:
        # crop=1364:-342:0:1083 against a 1364x741 frame.
        cx, cy = max(0, min(cx, fw - 2)), max(0, min(cy, fh - 2))
        w, h = max(2, min(w, fw - cx)) // 2 * 2, max(2, min(h, fh - cy)) // 2 * 2
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
            "-r", str(fps), *CFR, "-movflags", "+faststart"]
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
                cycle: float | None = None, margin: int = 14, scale: int = 2) -> None:
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
    fdir, crop = cast(page, el, secs, out.replace(".mp4", ""), margin=margin, scale=scale)
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

    Walks four real boards (desktop → browser → mobile → grounding); the eval command's
    --env-id and the leaderboard update together, so the frame holds both. Every board is
    visited BEFORE the span is measured, and the heights pinned, so the tallest board
    can't get sliced off at the frame edge mid-tour."""
    TOUR = [("Desktop", "osworld"), ("Browser", "webharbor.webvoyager"),
            ("Mobile", "androidworld"), ("Grounding", "screenspot_pro"),
            ("Desktop", "osworld")]          # back to the first board: the clip loops
    HOLD = 1.7
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
    if want("06-vm-tax"):
        print("clip: 06-vm-tax")
        figure_clip(browser, "06-vm-tax.mp4", "/blog/kvm-free-osworld/",
                    "figure.flow-demo.v2c", secs=15.5, cycle=7.0, mark=mark)

    # spares · the receipts behind post 3's numbers, for a reply or a quote-tweet
    if want("extra-footprint"):
        print("stills:")
        still(ctx, "extra-footprint.png", "/blog/kvm-free-osworld/", "figure.cmp", mark=mark)
    if want("extra-parity"):
        still(ctx, "extra-parity.png", "/blog/kvm-free-osworld/", "figure.par", mark=mark,
              min_ar=None,      # the plot is portrait; padding it landscape wastes a third of the card
              js="""document.querySelector('.par-cap').textContent =
                      'OSWorld vs Lite.OSWorld · 13 models · same desktop, same evaluators';""")
        # NOT `identical tasks`. This caption is OURS, injected here — not the blog's,
        # whose caption is `Success rate (%) · hover a point for the model`. The two runs
        # score 325 vs 321 tasks with different exclusion vocabularies, so `identical` is
        # the one word the thread copy is forbidden to use (twitter/02 Pre-flight 5) — and
        # it was contradicting that copy from inside the attached image.

    # 04 · the Lite.* family — the site's own rollout belt, walked across all four tabs
    if want("07-sandboxes"):
        print("clip: 05-family")
        # 44s is the belt's own scroll period (css: beltscroll 44s linear infinite), so a
        # clip of exactly that length wraps with the marquee back where it started; the four
        # families + a return to the first divide it into comfortable 8.8s holds
        # The marquee is a 44s loop, so no 10s cut of it can wrap cleanly — and at 2.6s a tab
        # it is also just noise. Pause it (a state the site itself has, on hover): the tiles
        # hold still long enough to read, each family's caption gets its beat, and the clip
        # loops without the belt snapping sideways.
        tabbed_clip(browser, "07-sandboxes.mp4", "/blog/why-cua-lite/", ".belt-fig", ".belt-tab",
                    mark, secs=14.0, hold=3.2, settle=10,
                    order=[3, 2, 1, 0],      # CUAWorld (GMAT/PyMOL) first — the unfamiliar one
                    extra_css=".belt-cap{visibility:hidden !important}"
                              ".belt-track{animation-play-state:paused !important}")
        retime("07-sandboxes.mp4", 7.0, head=0.8)    # 4 families + the loop back to the first
        # Capture SLOW, ship FAST. hold must be long enough for each tab's per-tile <video>
        # elements to paint — at hold=1.5 the capture moved on before they did and the clip
        # shipped with 2.3 s of solid black tiles across the whole Lite.CUAGym panel, 34% of
        # its runtime, in the post that is the thread's payload. settle only settles the FIRST
        # tab, so it does not cover this. The fast pacing the author asked for comes from
        # retime() afterwards, not from starving the capture.

    # 05 · convert once, train anything: datasets fold into LiteSample, adapters pack it per model
    if want("04-litesample"):
        print("clip: 06-litesample")
        figure_clip(browser, "04-litesample.mp4", "/blog/why-cua-lite/",
                    "figure.flow-demo:has([data-board='data'])", secs=12, settle=9.5,
                    cycle=5.2, mark=mark)          # runBoard's own setInterval(cycle, 5200)

    # 06 · the loop itself: screenshots up, actions down, any env ⇄ any agent through lite.gym
    if want("03-litegym"):
        print("clip: 07-litegym")
        figure_clip(browser, "03-litegym.mp4", "/blog/why-cua-lite/",
                    # 2 cycles only reached one env/agent pair; 4 walks the ladder across the
                    # board, which is what the post and its alt text describe
                    # scale=1, NOT the default 2. At 2x the page is drawn twice as large in
                    # a frame that stays viewport-sized, so a crop is only valid when
                    # 2*(y+height) <= frame height, i.e. the figure must be under ~370 CSS px
                    # tall. This one is ~500, so at 2x its bottom is ALWAYS off-frame and no
                    # viewport height fixes it — a taller viewport just pushes it further
                    # down (tried 1240: captured nothing but background). 1x costs sharpness
                    # and still lands ~800px wide, which is above what X displays.
                    "figure.flow-demo:has([data-board='pair'])", secs=22, settle=10.5,
                    cycle=5.2, mark=mark, margin=18, scale=1)
        retime("03-litegym.mp4", 9.0)    # 19s of a mostly-static figure reads as a still

    # 07 · the boards those commands fill
    if want("05-leaderboard"):
        print("clip: 05-leaderboard")
        leaderboard_clip(browser, "05-leaderboard.mp4", mark)
        retime("05-leaderboard.mp4", 8.8, head=0.65) # 5 boards; anything slower reads as a still

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


def retime(out: str, target: float, *, head: float = 0.0, seam: bool = True) -> None:
    """Force a finished clip to an exact duration.

    Why this exists: `cast` derives each frame's on-screen duration from the CDP
    screencast timestamps, and a screencast emits nothing while the page is still — so a
    static beat becomes ONE frame stretched to the 2.5 s cap. Pacing therefore came out of
    capture jitter, not out of the HOLD/hold constants, and no amount of tuning them fixed
    it: 05-leaderboard shipped five boards in 16 s with a 6.5 s dead stretch in the middle
    while its HOLD said 3.2. Re-timing the encoded file is the only place the duration is
    actually knowable, so it is set here rather than hoped for upstream.
    """
    src = OUT / out
    if not src.exists():
        return
    cur = float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(src)],
                               check=True, capture_output=True, text=True).stdout.strip())
    # Early-out ONLY when there is nothing to do at all. Checking the duration alone made
    # `head` a no-op whenever the render happened to land near `target`: 07-sandboxes came
    # out at 7.367 s against a 7.5 s target, inside this tolerance, so its opening dwell was
    # never trimmed and its loop seam never re-aligned — silently, with no log line.
    if not head and abs(cur - target) < 0.15:
        return
    tmp = TMP / f"_retime_{out}"
    # `head` drops the opening dwell — the first beat is the one a scroller judges, and held
    # as long as the others the clip reads as a still and gets scrolled past.
    #
    # Cutting the head invalidates the loop. encode() already trimmed to a seam where the
    # last frame matches the first (seam_cut), and X autoplays on repeat, so a mid-cycle
    # end is a visible jump. Trimming the SAME amount off the tail does NOT fix it — that
    # was tried and made the seam three times worse (13.6 -> 45.4), because 2*head is not a
    # whole number of animation cycles. The only correct move is to re-find the seam after
    # the head cut, which is what the caller does by passing `seam=True`.
    # Trim on the INPUT side (-ss/-t BEFORE -i), then scale what is left to `target`.
    # -t placed after -i caps the OUTPUT instead, so it fights the setpts: that mistake
    # produced a 4.0 s clip against a 7.5 s target.
    kept = cur - head if head else cur
    pre = ["-ss", f"{head:.2f}"] if head else []
    run([FFMPEG, "-y", "-loglevel", "error"] + pre + ["-i", str(src),
         "-filter:v", f"setpts={target / kept:.4f}*PTS",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
         "-r", "30", "-movflags", "+faststart", str(tmp)])
    # shutil.move, NOT Path.replace: TMP is on /tmp and assets/ is on the repo disk, and
    # os.replace() across filesystems raises OSError 18 "Invalid cross-device link".
    if head and seam:
        end = seam_cut(tmp, target)
        cut = TMP / f"_seam_{out}"
        run([FFMPEG, "-y", "-loglevel", "error", "-i", str(tmp), "-t", f"{end:.3f}",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-r", "30", *CFR,
             "-movflags", "+faststart", str(cut)])
        tmp = cut
    shutil.move(str(tmp), str(src))
    print(f"    retimed {out}: {cur:.1f}s -> {target:.1f}s")


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
            # CUA_LITE_CDP: connect to a Chrome you started yourself, instead of letting
            # Playwright launch one. Needed on hosts where launch() dies with SIGTRAP (see
            # the module docstring). Start it with:
            #   chrome --headless --no-sandbox --disable-gpu --disable-dev-shm-usage \
            #          --remote-debugging-port=9401 --user-data-dir=/tmp/pw
            #   CUA_LITE_CDP=http://127.0.0.1:9401 uv run python .../make_assets.py 03-litegym
            cdp = os.environ.get("CUA_LITE_CDP")
            browser = pw.chromium.connect_over_cdp(cdp) if cdp else pw.chromium.launch()
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
