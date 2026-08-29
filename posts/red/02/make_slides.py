"""Render red/02 inner slides (02-05) as designed cards — English, standalone.

Each card: eyebrow (section label) + a headline that states the OSWorld↔Lite.OSWorld context
on its own · the figure (which carries its own caption) · watermark. Card height follows its
content (no forced portrait → wide figures never float in dead space). One cream ground, brand
accents. Figures from build/fig/ (capture_sections.py).

    uv run python posts/red/02/make_slides.py
Playwright's launch() cannot start Chromium on this host (SIGTRAP, no stderr — see
posts/twitter/01/make_assets.py for the bisection). Start Chrome yourself and set CUA_LITE_CDP:

    ~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome --headless --no-sandbox \
      --disable-gpu --remote-debugging-port=9411 --user-data-dir=/tmp/pw &
    CUA_LITE_CDP=http://127.0.0.1:9411 uv run python posts/red/02/make_slides.py

"""
from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent.parent   # posts/red/02/ -> repo root
OUT = Path(__file__).resolve().parent / "assets"
FIGURL = "/posts/red/02/build/fig"
PORT = 8804

CARD = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Fraunces';src:url('/assets/fonts/Fraunces.woff2') format('woff2');font-weight:300 700;font-style:normal;}}
@font-face{{font-family:'Fraunces';src:url('/assets/fonts/Fraunces-Italic.woff2') format('woff2');font-weight:300 700;font-style:italic;}}
@font-face{{font-family:'Urbanist';src:url('/assets/fonts/Urbanist.woff2') format('woff2');font-weight:100 900;font-style:normal;}}
@font-face{{font-family:'Geist Mono';src:url('/assets/fonts/GeistMono.woff2') format('woff2');font-weight:400 600;font-style:normal;}}
:root{{--text:#453d33;--muted:#6f665a;--dim:#a89e8c;--accent:#bd5a38;--edge:#e3d6bf;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html{{background:#f2e6d2;}}
body{{width:1080px;color:var(--text);font-family:'Urbanist',sans-serif;
  background:radial-gradient(125% 68% at 50% -4%, #fdf9f0 0%, #f7efe0 55%, #f2e6d2 100%);
  padding:58px 96px 48px;}}   /* side padding = the figure's margin: headline, figure & mark share one edge */
.eyebrow{{font-family:'Geist Mono',monospace;font-size:25px;letter-spacing:3px;color:var(--accent);font-weight:600;}}
.title{{font-family:'Fraunces';font-size:60px;line-height:1.08;color:var(--text);margin-top:12px;
  letter-spacing:-0.015em;font-variation-settings:'opsz' 144,'wght' 420;}}
.title i{{font-style:italic;color:var(--accent);}}
.fig{{margin:32px 0 26px;text-align:center;}}
.fig img{{max-width:100%;filter:drop-shadow(0 16px 34px rgba(40,30,15,.16));}}   /* fills the padded content box → aligns with the headline's left/right edge */
.mark{{font-family:'Geist Mono',monospace;font-size:22px;letter-spacing:1px;color:var(--dim);text-align:right;}}
</style></head><body>
<div class="eyebrow">{eyebrow}</div>
<div class="title">{title}</div>
<div class="fig"><img src="{src}"></div>
<div class="mark">cua-lite.github.io</div>
</body></html>"""

# (number, fig, eyebrow, title HTML with <i> accent) — each headline is standalone context
SLIDES = [
    ("02", "footprint", "01 · VM TAX",          "Keeps the desktop, <i>drops the VM</i>"),
    ("03", "hh",        "02 · SAME TASK",        "The same task, <i>same behavior</i>"),
    ("04", "parity",    "03 · SAME SCORES",      "Container scores <i>match the VM</i>"),
    ("05", "belt",      "04 · BEYOND OSWORLD",   "One base, <i>a family of sandboxes</i>"),
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
            for num, fig, eyebrow, title in SLIDES:
                tmp = ROOT / f"_red02_slide_{fig}.html"
                tmp.write_text(CARD.format(eyebrow=eyebrow, title=title, src=f"{FIGURL}/{fig}.png"))
                # small viewport so full_page grows to the real content height (it floors at
                # the viewport, so a 900px viewport left a big dead band under short slides)
                pg = b.new_page(viewport={"width": 1080, "height": 200}, device_scale_factor=2)
                pg.goto(f"http://localhost:{PORT}/{tmp.name}")
                pg.wait_for_load_state("networkidle")
                pg.wait_for_timeout(400)
                pg.screenshot(path=str(OUT / f"{num}-{fig}.png"), full_page=True)
                pg.close()
                tmp.unlink(missing_ok=True)
                print(f"slide {num}-{fig}")
            b.close()
    finally:
        srv.terminate()
    print("done")


if __name__ == "__main__":
    main()
