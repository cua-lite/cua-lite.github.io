"""Render red/02 covers: 01a (compact card) + 01b (same text + VM→container visual).

Mirrors red/01's 01a/01b relationship: both share the headline + the SAME three bullets;
01a closes with a stat footer, 01b instead carries a drawn before/after (OSWorld on a heavy
QEMU/KVM VM → the same desktop in a light Docker container). Shared brand tokens.

    uv run python posts/red/02/make_cover.py
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent.parent   # posts/red/02/ -> repo root
OUT = Path(__file__).resolve().parent / "assets"
PORT = 8802

HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Fraunces';src:url('/assets/fonts/Fraunces.woff2') format('woff2');font-weight:300 700;font-style:normal;}
@font-face{font-family:'Fraunces';src:url('/assets/fonts/Fraunces-Italic.woff2') format('woff2');font-weight:300 700;font-style:italic;}
@font-face{font-family:'Urbanist';src:url('/assets/fonts/Urbanist.woff2') format('woff2');font-weight:100 900;font-style:normal;}
@font-face{font-family:'Geist Mono';src:url('/assets/fonts/GeistMono.woff2') format('woff2');font-weight:400 600;font-style:normal;}
:root{--text:#453d33;--muted:#6f665a;--dim:#a89e8c;--accent:#bd5a38;--edge:#e3d6bf;}
*{margin:0;padding:0;box-sizing:border-box;}
html{background:#f2e4d0;}
body{width:1080px;overflow:hidden;color:var(--text);font-family:'Urbanist',sans-serif;
  background:radial-gradient(120% 72% at 4% -4%, #fdf9f0 0%, #f8f0e0 46%, #f2e4d0 100%);
  padding:88px 84px 80px;display:flex;flex-direction:column;}
.brand{display:flex;align-items:center;gap:16px;}
.brand .plane{width:44px;height:44px;background:url('/assets/logo.svg') center/contain no-repeat;}
.brand .name{font-weight:700;font-size:36px;letter-spacing:-0.01em;}
h1{font-family:'Fraunces';font-style:italic;color:var(--accent);
  font-variation-settings:'opsz' 144,'wght' 400;font-size:112px;line-height:1.0;letter-spacing:-0.03em;margin-top:42px;}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;}
.lead{margin-top:46px;font-size:34px;line-height:1.32;color:var(--muted);font-weight:500;}
.lead .lc{color:var(--accent);font-weight:600;}
.claims{margin-top:32px;display:flex;flex-direction:column;gap:32px;}
.claim{position:relative;padding-left:42px;font-size:34px;line-height:1.32;color:var(--muted);font-weight:450;}
.claim::before{content:"";position:absolute;left:0;top:13px;width:14px;height:14px;border-radius:50%;background:var(--accent);}
.claim b{color:var(--text);font-weight:680;}
.claim .lc{color:var(--accent);font-weight:680;}
.foot{border-top:1px solid var(--edge);padding-top:32px;font-family:'Geist Mono';color:var(--dim);}
.foot .stats{font-size:32px;letter-spacing:0.01em;white-space:nowrap;}
.foot .stats b{color:var(--accent);font-weight:600;}
.foot .stats i{font-style:normal;color:var(--edge);margin:0 12px;}
.foot .url{margin-top:22px;font-size:32px;color:var(--muted);}
.url1{font-family:'Geist Mono';font-size:25px;color:var(--dim);margin-top:22px;}
/* before/after (01b) */
.vwrap{margin:54px 0 22px;}   /* spacing before the before/after (01b is content-height, so no float) */
.ba{display:flex;align-items:flex-start;justify-content:center;gap:26px;}
.col{display:flex;flex-direction:column;align-items:center;gap:12px;}
.lab{font-family:'Geist Mono';font-size:23px;letter-spacing:0.5px;color:var(--muted);}
.lab.lite{color:var(--accent);font-weight:600;}
.win{width:250px;background:linear-gradient(180deg,#efe7d6,#e7dcc6);border:1px solid #d9cbb0;border-radius:11px;
  box-shadow:0 3px 8px -3px rgba(40,30,15,.2);overflow:hidden;}
.win-bar{height:30px;background:#e2d6bf;border-bottom:1px solid #d3c4a6;display:flex;align-items:center;padding:0 11px;gap:6px;}
.win-bar i{width:8px;height:8px;border-radius:50%;background:#c9b593;}
.win-body{height:124px;display:flex;align-items:center;justify-content:center;}
.win-card{width:158px;background:#fff;border:1px solid #e6dcc8;border-radius:6px;padding:12px 11px;}
.win-card .r1{height:8px;background:#e2d6bf;border-radius:3px;margin-bottom:8px;}
.win-card .r2{height:11px;width:64%;background:var(--accent);border-radius:3px;}
.slab{width:272px;margin-top:11px;background:repeating-linear-gradient(45deg,#3a3128 0 7px,#2f281f 7px 14px);
  color:#f7ecd8;border-radius:9px;padding:17px 0;text-align:center;font-family:'Geist Mono';font-size:24px;letter-spacing:1px;
  box-shadow:0 4px 10px -4px rgba(40,30,15,.35);}
.kvm{margin-top:10px;font-family:'Geist Mono';font-size:21px;color:var(--muted);background:#efe7d6;border:1px solid #d9cbb0;
  border-radius:8px;padding:7px 15px;}
.arrowcol{display:flex;flex-direction:column;align-items:center;gap:4px;margin-top:104px;}   /* aligns the arrow to the desktop-window centre */
.anno{font-family:'Geist Mono';font-size:22px;color:var(--accent);text-align:center;line-height:1.4;font-weight:600;}
.arrow{font-size:56px;color:var(--accent);font-family:'Fraunces';line-height:0.7;}
.ctr{border:2.5px dashed var(--accent);border-radius:15px;padding:20px 20px 15px;position:relative;background:rgba(189,90,56,.04);}
.ctr .tag{position:absolute;top:-15px;left:18px;background:#faf1e0;padding:0 9px;font-family:'Geist Mono';font-size:19px;
  letter-spacing:1.5px;color:var(--accent);text-transform:uppercase;}
</style></head><body style="HEIGHT">"""

BRAND = '<div class="brand"><span class="plane"></span><span class="name">CUA-Lite</span></div>'
H1 = '<h1>VM-free<br>OS(World) at scale.</h1>'
LEAD = '<p class="lead">Scalable <span class="lc">CUA</span> sandboxes with verifiable tasks:</p>'
CLAIMS = """<div class="claims">
  <p class="claim"><b class="lc">Lite.OSWorld</b>: OSWorld minus the VM, leaner &amp; parallel</p>
  <p class="claim"><b>Beyond OSWorld</b>: a growing family of training sandboxes</p>
</div>"""
_WIN = ('<div class="win"><div class="win-bar"><i></i><i></i><i></i></div>'
        '<div class="win-body"><div class="win-card"><div class="r1"></div><div class="r2"></div></div></div></div>')
BA = ('<div class="ba">'
      '<div class="col"><span class="lab">OSWorld · VM</span>' + _WIN +
      '<div class="slab">QEMU · KVM</div><div class="kvm">/dev/kvm</div></div>'
      '<div class="arrowcol"><span class="anno">~5× more instances</span><span class="arrow">→</span></div>'
      '<div class="col"><span class="lab lite">Lite.OSWorld · container</span>'
      '<div class="ctr"><span class="tag">Docker</span>' + _WIN + '</div>'
      '<div class="kvm">any Docker host</div></div>'
      '</div>')

FOOT = ('<div class="foot"><div class="stats"><b>Lite.OSWorld</b> <i>·</i> Lite.CUAGym <i>·</i> '
        'Lite.CUAWorld</div>'
        '<div class="url">cua-lite.github.io/blog/kvm-free-osworld</div></div>')
BODY_A = BRAND + '<div class="mid">' + H1 + LEAD + CLAIMS + '</div>' + FOOT
BODY_B = BRAND + H1 + LEAD + CLAIMS + '<div class="vwrap">' + BA + '</div>' + FOOT

# Chinese covers: English Fraunces headline (the brand face) + localized body, same call as red/01.
_ZH_CSS = """
@font-face{font-family:'SansSC';src:url('/assets/fonts/SansSC-Regular.woff2') format('woff2');font-weight:400;font-style:normal;}
@font-face{font-family:'SansSC';src:url('/assets/fonts/SansSC-Bold.woff2') format('woff2');font-weight:700;font-style:normal;}
.claim,.lead{font-family:'Urbanist','SansSC',sans-serif;}
.claim{line-height:1.5;}
.brand .name{font-family:'Urbanist','SansSC',sans-serif;}
.lab,.kvm,.anno,.foot .stats{font-family:'Geist Mono','SansSC',monospace;}
"""
HEAD_ZH = HEAD.replace("</style>", _ZH_CSS + "</style>")

LEAD_ZH = '<p class="lead">可扩展的 <span class="lc">CUA</span> 沙盒，自带可验证任务：</p>'
CLAIMS_ZH = """<div class="claims">
  <p class="claim"><b class="lc">Lite.OSWorld</b>：OSWorld 去掉虚拟机，更省、可并行</p>
  <p class="claim"><b>不止 OSWorld</b>：同一底座上持续扩展的训练沙盒</p>
</div>"""
BA_ZH = (BA.replace('OSWorld · VM', 'OSWorld · 虚拟机')
           .replace('Lite.OSWorld · container', 'Lite.OSWorld · 容器')
           .replace('~5× more instances', '并行 ~5×')
           .replace('any Docker host', '任意 Docker 主机'))
BODY_A_ZH = BRAND + '<div class="mid">' + H1 + LEAD_ZH + CLAIMS_ZH + '</div>' + FOOT
BODY_B_ZH = BRAND + H1 + LEAD_ZH + CLAIMS_ZH + '<div class="vwrap">' + BA_ZH + '</div>' + FOOT

# (name, height, body, head) — 01b variants are content-height
VARIANTS = [("01a-cover.png",    1080, BODY_A,    HEAD),
            ("01b-cover.png",    None, BODY_B,    HEAD),
            ("01a-cover-zh.png", 1080, BODY_A_ZH, HEAD_ZH),
            ("01b-cover-zh.png", None, BODY_B_ZH, HEAD_ZH)]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / "_red02_cover_tmp.html"
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--directory", str(ROOT)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.0)
        with sync_playwright() as p:
            b = p.chromium.launch()
            for name, h, body, head in VARIANTS:
                style = f"height:{h}px" if h else ""   # h=None → content-height, full-page shot
                tmp.write_text(head.replace("HEIGHT", style) + body + "</body></html>")
                pg = b.new_page(viewport={"width": 1080, "height": h or 900}, device_scale_factor=2)
                pg.goto(f"http://localhost:{PORT}/_red02_cover_tmp.html")
                pg.wait_for_timeout(700)
                pg.screenshot(path=str(OUT / name), full_page=(h is None))
                pg.close()
                print(f"wrote {name}")
            b.close()
    finally:
        srv.terminate()
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
