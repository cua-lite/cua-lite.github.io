"""Capture each homepage section as a full portrait block for the 小红书 carousel.

The simplest, truest approach: screenshot the whole section — its heading, lead and
every figure (belt / HF dataset viewer / leaderboard / SFT terminal) — straight off the
homepage, on the site's own cream. 小红书 is mobile-portrait, so tall blocks are ideal.
Only index.html is sourced.

    uv run python posts/red/01/capture_sections.py
Playwright's launch() cannot start Chromium on this host (SIGTRAP, no stderr — see
posts/twitter/01/make_assets.py for the bisection). Start Chrome yourself and set CUA_LITE_CDP:

    ~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome --headless --no-sandbox \
      --disable-gpu --remote-debugging-port=9411 --user-data-dir=/tmp/pw &
    CUA_LITE_CDP=http://127.0.0.1:9411 uv run python posts/red/01/capture_sections.py

"""
from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent.parent   # posts/red/01/ -> repo root
OUT = Path(__file__).resolve().parent / "assets"
PORT = 8797
MARGIN = 40   # cream breathing room kept around the actual content (not the wide container)

# NOTE: do NOT use `*{animation:none}` — entrance animations have base opacity:0, so cancelling
# them reverts rows (leaderboard, coverage board) to invisible. Instead: pause only the belt
# marquee (keeps its current frame), let entrance animations finish on their own (we wait), and
# force any below-the-fold reveal blocks visible.
FREEZE = ("header.nav{display:none !important;}"
          " .belt-track, .belt-track-rev{animation-play-state:paused !important;}"
          " .reveal{opacity:1 !important; transform:none !important; visibility:visible !important;}"
          " .belt-cap{display:none !important;}"
          # the marquee's outer tiles are cut mid-tile; fade the belt's edges so they read as
          # "still scrolling" rather than a hard clip (tabs + description sit above .belt, unaffected)
          " .belt{-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 5%,#000 95%,transparent 100%) !important;"
          " mask-image:linear-gradient(90deg,transparent 0,#000 5%,#000 95%,transparent 100%) !important;}")

# (number, name, section selector, settle wait ms, wait-for predicate, wide-content selectors)
# vertical extent = the section's .container; horizontal extent = the WIDEST real figure (the
# container is much wider than the centred figures, so clipping to it leaves huge side margins).
TARGETS = [
    ("02", "sandboxes", "#sandboxes", 1600, None, ["#sandboxes .belt-fig"]),
    ("03", "data",      "#data",      12000, None, ["#data .hf-window", "#data .src-two"]),
    ("04", "eval",      "#benchmarks", 2200, "document.querySelectorAll('#lb-body > *').length > 0",
     ["#benchmarks .lb", "#benchmarks .cov", "#benchmarks .cmdbuild"]),
    ("05", "train",     "#train",      1500, None, ["#train .cmdbuild", "#train .sft-cfg"]),
]


def _wait_for_server(port: int, timeout: float = 15.0) -> None:
    """Poll until the local server answers. A fixed sleep(1.0) is a race: it fails
    intermittently on a loaded host with ERR_CONNECTION_REFUSED at the first goto,
    which reads like a Playwright bug rather than a slow server."""
    import urllib.error
    import urllib.request
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://localhost:{port}/", timeout=0.5)
            return
        except urllib.error.HTTPError:
            return                      # answered (any status) = listening
        except Exception:
            time.sleep(0.15)
    raise RuntimeError(f"local server on :{port} never came up within {timeout:.0f}s")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--directory", str(ROOT)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        _wait_for_server(PORT)
        with sync_playwright() as p:
            cdp = os.environ.get("CUA_LITE_CDP")
            b = (p.chromium.connect_over_cdp(cdp) if cdp
                 else p.chromium.launch())
            # fresh page load per section — a single scroll-through leaves lazy blocks
            # (leaderboard, coverage board) in inconsistent render states.
            for num, name, sec, wait_ms, pred, wides in TARGETS:
                pg = b.new_page(viewport={"width": 1180, "height": 1500}, device_scale_factor=2)
                pg.goto(f"http://localhost:{PORT}/index.html")
                pg.wait_for_timeout(500)
                pg.locator(sec).scroll_into_view_if_needed()
                if pred:
                    try:
                        pg.wait_for_function(pred, timeout=9000)
                    except Exception:
                        print(f"  ! {name}: wait predicate timed out")
                pg.wait_for_timeout(wait_ms)
                pg.add_style_tag(content=FREEZE)   # freeze only after content has settled
                cont = pg.locator(f"{sec} .container").bounding_box()   # vertical extent
                left, right = cont["x"] + cont["width"], cont["x"]      # horizontal extent = widest figure
                for w in wides:
                    wb = pg.locator(w).first.bounding_box()
                    if wb:
                        left, right = min(left, wb["x"]), max(right, wb["x"] + wb["width"])
                clip = {"x": max(0, left - MARGIN), "y": max(0, cont["y"] - MARGIN),
                        "width": (right - left) + 2 * MARGIN, "height": cont["height"] + 2 * MARGIN}
                pg.screenshot(path=str(OUT / f"{num}-{name}.png"), clip=clip)
                print(f"wrote {num}-{name}.png  ({int(clip['width'])}x{int(clip['height'])})")
                pg.close()
            b.close()
    finally:
        srv.terminate()
    print("done")


if __name__ == "__main__":
    main()
