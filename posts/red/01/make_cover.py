"""Render the 小红书 portrait covers to assets/01a-cover.png and 01b-cover.png (@2x).

Portrait siblings of assets/og.png — same brand, headline, palette and stats as
the homepage hero. Two variants:
  01a — compact (1080x1100): trimmed height, little whitespace around the text.
  01b — tall (1080x1440): text up top, the hero's own desktop / browser / mobile
        devices (captured by capture.py, with their frames) labelled along the bottom.

    uv run python posts/red/01/capture.py     # (re)make the device cutouts first
    uv run python posts/red/01/make_cover.py
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent.parent   # posts/red/01/ -> repo root
OUTDIR = Path(__file__).resolve().parent / "assets"
DEV = "/posts/red/01/build/dev"   # device cutouts (from capture.py), served from repo root
PORT = 8794

HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Fraunces';src:url('/assets/fonts/Fraunces.woff2') format('woff2');font-weight:300 700;font-style:normal;}
@font-face{font-family:'Fraunces';src:url('/assets/fonts/Fraunces-Italic.woff2') format('woff2');font-weight:300 700;font-style:italic;}
@font-face{font-family:'Urbanist';src:url('/assets/fonts/Urbanist.woff2') format('woff2');font-weight:100 900;font-style:normal;}
@font-face{font-family:'Geist Mono';src:url('/assets/fonts/GeistMono.woff2') format('woff2');font-weight:400 600;font-style:normal;}
:root{--text:#453d33;--muted:#6f665a;--dim:#a89e8c;--accent:#bd5a38;--edge:#e3d6bf;}
*{margin:0;padding:0;box-sizing:border-box;}
body{width:1080px;overflow:hidden;color:var(--text);font-family:'Urbanist',sans-serif;
  background:radial-gradient(120% 78% at 4% -4%, #fdf9f0 0%, #f8f0e0 46%, #f2e4d0 100%);
  padding:88px 84px 80px;display:flex;flex-direction:column;}
.brand{display:flex;align-items:center;gap:17px;}
.brand .plane{width:46px;height:46px;background:url('/assets/logo.svg') center/contain no-repeat;}
.brand .name{font-weight:700;font-size:38px;letter-spacing:-0.01em;}
h1{font-family:'Fraunces';font-style:italic;color:var(--accent);
  font-variation-settings:'opsz' 144,'wght' 400,'SOFT' 0,'WONK' 0;
  font-size:126px;line-height:0.98;letter-spacing:-0.025em;}
h1 .hinge{color:var(--muted);}
.claims{margin-top:58px;display:flex;flex-direction:column;gap:34px;}
.claim{position:relative;padding-left:42px;font-size:34px;line-height:1.32;color:var(--muted);font-weight:450;}
.claim::before{content:"";position:absolute;left:0;top:14px;width:15px;height:15px;border-radius:50%;background:var(--accent);}
.claim b{color:var(--text);font-weight:680;}
.claim .lc{color:var(--accent);font-weight:680;}
.plats{margin-top:34px;padding-left:42px;font-family:'Geist Mono';font-size:23px;color:var(--muted);letter-spacing:0.01em;}
.plats i{font-style:normal;color:var(--dim);margin:0 8px;}
.plats b{color:var(--text);font-weight:600;}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;}
.grow{flex:1;}
.devices{display:flex;align-items:flex-end;justify-content:center;gap:30px;}
.devcol{display:flex;flex-direction:column;align-items:center;gap:20px;}
.devcol img{display:block;filter:drop-shadow(0 10px 22px rgba(40,30,15,.20));}
.d-desktop{height:244px;} .d-browser{height:244px;} .d-mobile{height:330px;}
.dev-lab{font-family:'Geist Mono';font-size:22px;letter-spacing:0.06em;color:var(--dim);}
.foot{border-top:1px solid var(--edge);padding-top:34px;font-family:'Geist Mono';color:var(--dim);}
.foot .stats{font-size:23.5px;letter-spacing:0.01em;white-space:nowrap;}
.foot .stats b{color:var(--accent);font-weight:600;}
.foot .stats i{font-style:normal;color:var(--edge);margin:0 9px;}
.foot .url{margin-top:16px;font-size:26px;color:var(--muted);}
</style></head><body style="height:%HEIGHT%px;">
"""

BRAND = '<div class="brand"><span class="plane"></span><span class="name">CUA-Lite</span></div>'
H1 = '<h1>Any agent, <span class="hinge">on</span><br>any computer.</h1>'
H1B = '<h1 style="margin-top:56px">Any agent, <span class="hinge">on</span><br>any computer.</h1>'  # brand→headline breathing room in the tall variant
_C12 = """  <p class="claim">Scalable, efficient <b>sandboxes</b> with <b class="lc">30k+</b> verifiable tasks</p>
  <p class="claim">Unified <b>SFT data</b> — 10+ datasets plus fresh rollouts</p>"""
# 01a carries the platforms as a natural continuation of the third bullet (it has no devices);
# 01b leaves the third bullet clean because the labelled devices below already say desktop/browser/mobile.
CLAIMS_A = f'<div class="claims">\n{_C12}\n  <p class="claim">Unified <b>eval</b>, <b>SFT</b> &amp; <b>RL</b>, any <span class="lc">computer-use</span> agent, across desktop, browser &amp; mobile</p>\n</div>'
CLAIMS_B = f'<div class="claims">\n{_C12}\n  <p class="claim">Unified <b>eval</b>, <b>SFT</b> &amp; <b>RL</b>, any <span class="lc">computer-use</span> agent</p>\n</div>'
DEVICES = f"""<div class="devices">
  <div class="devcol"><img class="d-desktop" src="{DEV}/dev-desktop.png" alt=""><span class="dev-lab">desktop</span></div>
  <div class="devcol"><img class="d-browser" src="{DEV}/dev-browser.png" alt=""><span class="dev-lab">browser</span></div>
  <div class="devcol"><img class="d-mobile" src="{DEV}/dev-mobile.png" alt=""><span class="dev-lab">mobile</span></div>
</div>"""
FOOT = """<div class="foot">
  <div class="stats"><b>30k+</b> tasks <i>·</i> <b>10+</b> datasets <i>·</i> <b>10+</b> agents <i>·</i> <b>15+</b> benchmarks</div>
  <div class="url">cua-lite.github.io</div>
</div>"""

# 01a — compact: text (+ a platform line) centred in a short canvas.
BODY_A = f'{BRAND}<div class="mid">{H1}{CLAIMS_A}</div>{FOOT}'
# 01b — tall: text up top, hero devices labelled by platform along the bottom.
BODY_B = f'{BRAND}{H1B}{CLAIMS_B}<div class="grow"></div>{DEVICES}<div class="grow"></div>{FOOT}'

VARIANTS = [("01a-cover.png", 1100, BODY_A), ("01b-cover.png", 1440, BODY_B)]


def main() -> None:
    tmp = ROOT / "_red_cover_tmp.html"
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--directory", str(ROOT)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.0)
        with sync_playwright() as p:
            b = p.chromium.launch()
            for name, height, body in VARIANTS:
                tmp.write_text(HEAD.replace("%HEIGHT%", str(height)) + body + "</body></html>")
                pg = b.new_page(viewport={"width": 1080, "height": height}, device_scale_factor=2)
                pg.goto(f"http://localhost:{PORT}/_red_cover_tmp.html")
                pg.wait_for_timeout(700)  # let the webfonts + device PNGs settle
                pg.screenshot(path=str(OUTDIR / name))
                pg.close()
                print(f"wrote {OUTDIR / name} (1080x{height} @2x)")
            b.close()
    finally:
        srv.terminate()
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
