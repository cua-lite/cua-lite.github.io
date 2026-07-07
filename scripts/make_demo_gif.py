"""Render the hero device demo to high-res GIF + MP4 (for the cua-lite README).

Captures the REAL page (the same demo that runs on the site) as native frames via
Chromium's CDP screencast — no video-file screen recording — on a white background,
then assembles crisp loops with ffmpeg. Key trick: CDP screencast captures at CSS
resolution (it ignores device-scale), so we CSS-`zoom` the isolated demo up first
and output at the captured native size (no upscaling — that's what kept it sharp).

Produces three crops, each as .gif + .mp4, in assets/:
    demo            — the device only
    demo-trace      — device + the rollout trace below it
    demo-trace-side — device + the rollout trace to its right (landscape banner)

Requirements: `ffmpeg` on PATH, plus this repo's dev deps (playwright, pillow).

    uv run python scripts/make_demo_gif.py                # defaults
    uv run python scripts/make_demo_gif.py --zoom 2.2     # bigger / crisper (larger files)
"""
from __future__ import annotations

import argparse
import base64
import bisect
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent

# isolate the demo on white (blends into a GitHub README): drop the page's peach
# washes, hide the nav + hero copy, and flatten the layout so only the demo remains.
BASE_CSS = (
    "body,.hero{background:#fff !important}"
    ".hero::before{display:none !important}"
    "header.nav,.hero-head{display:none !important}"
    ".hero{padding:0 !important;min-height:auto !important}"
    ".container{max-width:none !important;padding:0 !important}"
    ".hero-grid{grid-template-columns:1fr !important;gap:0 !important;max-width:none !important}"
    ".stage::after{opacity:.5 !important}"
)


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def screencast(url: str, vw: int, vh: int, css: str, settle_ms: int, seconds: float, raw: Path):
    """Screencast the viewport; return (frames meta, hero-demo bbox, stage bbox) in css px."""
    meta: list[tuple[float, Path]] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=1)
        page.goto(url)
        page.add_style_tag(content=BASE_CSS + css)
        page.wait_for_timeout(settle_ms)  # skip the entrance; the tour is starting
        demo = page.query_selector(".hero-demo").bounding_box()
        stage = page.query_selector(".stage").bounding_box()
        cdp = page.context.new_cdp_session(page)
        idx = [0]

        def on_frame(e: dict) -> None:
            i = idx[0]; idx[0] += 1
            fp = raw / f"{i:05d}.jpg"; fp.write_bytes(base64.b64decode(e["data"]))
            meta.append((e["metadata"]["timestamp"], fp))
            try:
                cdp.send("Page.screencastFrameAck", {"sessionId": e["sessionId"]})
            except Exception:
                pass

        cdp.on("Page.screencastFrame", on_frame)
        cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 100, "everyNthFrame": 1})
        page.wait_for_timeout(int(seconds * 1000))
        cdp.send("Page.stopScreencast"); page.wait_for_timeout(200)
        browser.close()
    return meta, demo, stage


def build(meta, fps, rect, vw, vh, margin, max_width, gif_out, mp4_out, hold=0.0):
    """Resample to an even fps, crop (+white margin, clamped), assemble native-res gif+mp4.

    `hold` freezes the final frame for that many seconds before the loop restarts. The
    screencast emits no frames while the demo is static, so the tour's *last* dwell (on
    the finished mobile screen) isn't captured — we re-add it here as an explicit end
    freeze, sized to match the tour's mid-holds so the loop rhythm stays even.
    """
    x, y, w, h = rect
    x0, y0 = max(0.0, x - margin), max(0.0, y - margin)
    x1, y1 = min(vw, x + w + margin), min(vh, y + h + margin)
    box = (round(x0), round(y0), round(x1), round(y1))
    with tempfile.TemporaryDirectory() as td:
        fr = Path(td)
        t0 = meta[0][0]; ts = [t - t0 for t, _ in meta]
        step = 1.0 / fps; n = int((ts[-1] + hold) / step)  # + hold: freeze the last frame
        for k in range(n + 1):
            j = max(0, bisect.bisect_right(ts, k * step) - 1)
            Image.open(meta[j][1]).convert("RGB").crop(box).save(fr / f"f{k:04d}.png")
        width = min(box[2] - box[0], max_width)  # native, downscale only if huge
        pat = str(fr / "f%04d.png"); pal = str(fr / "pal.png")
        vf = f"scale={width}:-1:flags=lanczos"
        _run(["ffmpeg", "-y", "-framerate", str(fps), "-i", pat,
              "-vf", f"{vf},palettegen=max_colors=256:stats_mode=diff", pal])
        _run(["ffmpeg", "-y", "-framerate", str(fps), "-i", pat, "-i", pal,
              "-lavfi", f"{vf}[x];[x][1:v]paletteuse=dither=sierra2_4a", "-loop", "0", str(gif_out)])
        _run(["ffmpeg", "-y", "-framerate", str(fps), "-i", pat,
              "-vf", f"scale={width}:-2:flags=lanczos,format=yuv420p",
              "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", str(mp4_out)])
    print(f"  {gif_out.name} {box[2]-box[0]}x{box[3]-box[1]}px ({gif_out.stat().st_size/1e6:.1f}MB gif, {mp4_out.stat().st_size/1e6:.1f}MB mp4)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Render the hero demo to GIF + MP4 (3 versions).")
    ap.add_argument("--zoom", type=float, default=2.4, help="CSS zoom for the stacked crops; default 1.9")
    ap.add_argument("--zoom-side", type=float, default=2.0, help="CSS zoom for the side/landscape crop; default 1.5")
    ap.add_argument("--fps", type=float, default=50, help="output fps; higher = smoother transitions")
    ap.add_argument("--seconds", type=float, default=16, help="one full tour: desktop->web->mobile fully done + a dwell before the loop restarts (settle at ~17.9s from load)")
    ap.add_argument("--settle-ms", type=int, default=1200)
    ap.add_argument("--hold", type=float, default=1.4, help="freeze the final (finished-mobile) frame this long before the loop restarts; ~matches the tour's mid-holds")
    ap.add_argument("--margin", type=int, default=28, help="white margin around the demo, px")
    ap.add_argument("--max-width", type=int, default=2600, help="downscale a crop only if it exceeds this")
    ap.add_argument("--port", type=int, default=8971)
    ap.add_argument("--out", type=Path, default=ROOT / "assets")
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg not found on PATH")
    a.out.mkdir(parents=True, exist_ok=True)

    srv = subprocess.Popen(["python3", "-m", "http.server", str(a.port)], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.0)
        url = f"http://localhost:{a.port}/index.html"

        # 1 & 2 — stacked layout: device-only (crop the stage) + device+trace (crop hero-demo).
        # pin the demo to its natural design width (547px) then zoom, so proportions match the
        # site and the rollout command wraps normally instead of overflowing/clipping.
        vw, vh = 1600, 2300
        css = f".hero-demo{{width:547px !important;zoom:{a.zoom} !important;margin:20px auto !important}}"
        with tempfile.TemporaryDirectory() as td:
            raw = Path(td) / "raw"; raw.mkdir()
            print("capturing stacked layout ...")
            meta, demo, stage = screencast(url, vw, vh, css, a.settle_ms, a.seconds, raw)
            print(f"  {len(meta)} frames @ {Image.open(meta[0][1]).size}")
            build(meta, a.fps, (stage["x"], stage["y"], stage["width"], stage["height"] + 20),
                  vw, vh, a.margin, a.max_width, a.out / "demo.gif", a.out / "demo.mp4", hold=a.hold)
            build(meta, a.fps, (demo["x"], demo["y"], demo["width"], demo["height"]),
                  vw, vh, a.margin, a.max_width, a.out / "demo-trace.gif", a.out / "demo-trace.mp4", hold=a.hold)

        # 3 — side layout: device + trace to its right
        vw, vh = 2520, 1320
        # top-align device + trace: the stage normally parks the device at its bottom
        # (justify-content:flex-end) leaving empty space on top; move it to the top and
        # pin a height that fits the tallest device (the phone) so nothing clips.
        css = (f".hero-demo{{zoom:{a.zoom_side} !important;margin:24px auto !important;"
               "flex-direction:row !important;align-items:flex-start !important;gap:30px !important;width:max-content !important}"
               ".stage{flex:0 0 auto !important;width:470px !important;min-height:0 !important;height:470px !important}"
               ".stage .device{justify-content:flex-start !important}"
               ".rollout{flex:0 0 auto !important;width:430px !important;margin:0 !important}"
               # top-aligning the device (flex-start above) leaves the stage's floor shadows
               # — anchored to the 470px stage BOTTOM — orphaned far below the shorter monitor
               # and browser (the tall phone nearly reaches them, so it looked fine). The soft
               # tabletop glow also bands into faint rings under GIF quantization. So: drop both
               # stage-anchored shadows and re-ground just the monitor on its own base; the
               # browser and phone already carry their own drop-shadow.
               ".stage::after,.stage .device::after{display:none !important}"
               ".stage .crt-base{position:relative !important}"
               ".stage .crt-base::after{content:'' !important;position:absolute !important;left:50% !important;"
               "bottom:-13px !important;transform:translateX(-50%) !important;z-index:-1 !important;"
               "pointer-events:none !important;filter:blur(13px) !important;width:210px !important;height:22px !important;"
               "background:radial-gradient(50% 50% at 50% 50%,rgba(40,30,15,.42),rgba(40,30,15,.2) 46%,transparent 74%) !important}")
        with tempfile.TemporaryDirectory() as td:
            raw = Path(td) / "raw"; raw.mkdir()
            print("capturing side layout ...")
            meta, demo, stage = screencast(url, vw, vh, css, a.settle_ms, a.seconds, raw)
            print(f"  {len(meta)} frames @ {Image.open(meta[0][1]).size}")
            build(meta, a.fps, (demo["x"], demo["y"], demo["width"], demo["height"]),
                  vw, vh, a.margin, a.max_width, a.out / "demo-trace-side.gif", a.out / "demo-trace-side.mp4", hold=a.hold)
    finally:
        srv.terminate()
    print("done ->", a.out)


if __name__ == "__main__":
    main()
