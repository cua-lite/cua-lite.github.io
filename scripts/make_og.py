"""Render the Open Graph / social card to assets/og.png (1200x630, @2x).

Mirrors the homepage hero — logo, headline, subtitle, stats — so the link
preview (Telegram / X / Slack …) stays in sync with the site's brand + wording.
Edit the HTML below when the hero changes, then re-run + bump og:image ?v= in
index.html so the social caches re-fetch.

    uv run python scripts/make_og.py
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PORT = 8791

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Fraunces';src:url('/assets/fonts/Fraunces.woff2') format('woff2');font-weight:300 700;font-style:normal;}
@font-face{font-family:'Fraunces';src:url('/assets/fonts/Fraunces-Italic.woff2') format('woff2');font-weight:300 700;font-style:italic;}
@font-face{font-family:'Urbanist';src:url('/assets/fonts/Urbanist.woff2') format('woff2');font-weight:100 900;font-style:normal;}
@font-face{font-family:'Geist Mono';src:url('/assets/fonts/GeistMono.woff2') format('woff2');font-weight:400 600;font-style:normal;}
:root{--text:#453d33;--muted:#6f665a;--dim:#a89e8c;--accent:#bd5a38;--edge:#e3d6bf;}
*{margin:0;padding:0;box-sizing:border-box;}
body{width:1200px;height:630px;overflow:hidden;color:var(--text);font-family:'Urbanist',sans-serif;
  background:radial-gradient(125% 135% at 6% -5%, #fdf9f0 0%, #f8f0e0 45%, #f2e4d0 100%);
  padding:66px 70px 60px;display:flex;flex-direction:column;}
.brand{display:flex;align-items:center;gap:15px;}
.brand .plane{width:40px;height:40px;background:url('/assets/logo.svg') center/contain no-repeat;}
.brand .name{font-weight:700;font-size:32px;letter-spacing:-0.01em;}
h1{font-family:'Fraunces';font-style:italic;color:var(--accent);
  font-variation-settings:'opsz' 144,'wght' 400,'SOFT' 0,'WONK' 0;
  font-size:84px;line-height:1.0;letter-spacing:-0.025em;margin-top:46px;}
.lead{margin-top:28px;font-size:26.5px;line-height:1.5;color:var(--muted);max-width:1010px;font-weight:450;}
.lead b{color:var(--text);font-weight:680;}
.lead .lc{color:var(--accent);font-weight:680;}
.spacer{flex:1;}
.foot{display:flex;justify-content:space-between;align-items:baseline;
  font-family:'Geist Mono';font-size:19px;color:var(--dim);letter-spacing:0.01em;}
.foot .stats b{color:var(--accent);font-weight:600;}
.foot .stats i{font-style:normal;color:var(--edge);margin:0 11px;}
.foot .url{color:var(--muted);}
</style></head><body>
<div class="brand"><span class="plane"></span><span class="name">CUA-Lite</span></div>
<h1>Any agent,<br>any computer.</h1>
<p class="lead">One lightweight framework to standardize <span class="lc">computer-use</span> <b>agents</b>, <b>data</b>, <b>evaluation</b>, <b>SFT</b>, and <b>RL</b> across desktop, web, and mobile.</p>
<div class="spacer"></div>
<div class="foot">
  <div class="stats"><b>10+</b> agents <i>·</i> <b>3</b> platforms <i>·</i> <b>15+</b> benchmarks <i>·</i> <b>10+</b> datasets</div>
  <div class="url">cua-lite.github.io</div>
</div>
</body></html>"""


def main() -> None:
    tmp = ROOT / "_og_tmp.html"
    tmp.write_text(HTML)
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--directory", str(ROOT)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.0)
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=2)
            pg.goto(f"http://localhost:{PORT}/_og_tmp.html")
            pg.wait_for_timeout(700)  # let the webfonts settle
            pg.screenshot(path=str(ROOT / "assets" / "og.png"))
            b.close()
    finally:
        srv.terminate()
        tmp.unlink(missing_ok=True)
    print("wrote assets/og.png (1200x630 @2x)")


if __name__ == "__main__":
    main()
