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
.lead{margin-top:48px;font-size:34px;line-height:1.32;color:var(--muted);font-weight:500;white-space:nowrap;}  /* same size as the bullets; must stay one line */
.lead .lc{color:var(--accent);font-weight:600;}
.claims{margin-top:34px;display:flex;flex-direction:column;gap:34px;}
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

# Chinese covers: keep the brand's English Fraunces headline (the signature slogan) as the hero,
# localize only the body — bullets/labels/footer in Noto Sans SC (echoes Urbanist). This keeps the
# brand face intact and sidesteps 电脑/设备; English-hero + Chinese-body is the premium bilingual look.
_ZH_CSS = """
@font-face{font-family:'SansSC';src:url('/posts/red/01/build/fonts/SansSC-Regular.woff2') format('woff2');font-weight:400;font-style:normal;}
@font-face{font-family:'SansSC';src:url('/posts/red/01/build/fonts/SansSC-Bold.woff2') format('woff2');font-weight:700;font-style:normal;}
.claim,.lead{font-family:'Urbanist','SansSC',sans-serif;}
.claim{line-height:1.5;}
.brand .name{font-family:'Urbanist','SansSC',sans-serif;}
.plats,.foot .stats{font-family:'Geist Mono','SansSC',monospace;}
.dev-lab{font-family:'SansSC',sans-serif;letter-spacing:0.05em;}
"""
HEAD_ZH = HEAD.replace("</style>", _ZH_CSS + "</style>")

# Optional fully-Chinese headline (Noto Serif SC echoes Fraunces; CJK has no italic, so it's upright
# with only the Latin "agent" kept in Fraunces italic). To use: set HEAD_ZH = HEAD.replace("</style>",
# _ZH_CSS + _ZH_SERIF_CSS + "</style>") and swap H1→H1_ZH / H1B→H1B_ZH in the ZH bodies below.
_ZH_SERIF_CSS = """
@font-face{font-family:'SerifSC';src:url('/posts/red/01/build/fonts/SerifSC.woff2') format('woff2');font-weight:600;font-style:normal;}
h1{font-family:'SerifSC','Fraunces',serif;font-style:normal;font-weight:600;font-size:120px;line-height:1.1;letter-spacing:0.005em;}
h1 .en{font-family:'Fraunces';font-style:italic;font-weight:400;letter-spacing:-0.02em;}
"""

BRAND = '<div class="brand"><span class="plane"></span><span class="name">CUA-Lite</span></div>'
H1 = '<h1>Any agent, <span class="hinge">on</span><br>any computer.</h1>'
H1B = '<h1 style="margin-top:56px">Any agent, <span class="hinge">on</span><br>any computer.</h1>'  # brand→headline breathing room in the tall variant
# Lead that introduces the bullets (homepage hero pattern) — names the computer-use agent once so
# all three bullets inherit the CUA context; bullet 3 then drops "computer-use" and just says "agent".
LEAD = '<p class="lead">One open-source platform for <span class="lc">computer-use</span> agents:</p>'
LEAD_ZH = '<p class="lead">一个开源平台，提供 <span class="lc">computer-use</span> agent 所需的一切：</p>'
# Each bullet leads with its pillar noun (homepage pattern: Sandboxes / Data / Framework) so the
# three read as parallel pillars and no two start with the same word.
_C12 = """  <p class="claim"><b>Sandboxes</b> — efficient, <b class="lc">30k+</b> verifiable CUA tasks</p>
  <p class="claim"><b>Data</b> — 10+ SFT datasets, plus frontier-CUA rollouts</p>"""
# Both variants carry the platforms: 01b's labelled devices show them, but the bullet should still
# say them in words so the claim stands on its own. "any agent" is dropped — the headline already
# says it — which is what lets the whole bullet sit on ONE line (measured 846px of 870 available;
# keeping "across" instead of "on" overflows, and the colon form fits by only 1px, too fragile).
CLAIMS = f'<div class="claims">\n{_C12}\n  <p class="claim"><b>Framework</b> — eval, SFT, RL on <b class="lc">desktop, browser, mobile</b></p>\n</div>'
CLAIMS_A = CLAIMS_B = CLAIMS
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
BODY_A = f'{BRAND}<div class="mid">{H1}{LEAD}{CLAIMS_A}</div>{FOOT}'
# 01b — tall: text up top, hero devices labelled by platform along the bottom.
BODY_B = f'{BRAND}{H1B}{LEAD}{CLAIMS_B}<div class="grow"></div>{DEVICES}<div class="grow"></div>{FOOT}'

# --- Chinese siblings (English Fraunces headline + localized body) ---
# Full-Chinese headline alternative (used only with _ZH_SERIF_CSS above): slogan「任何 agent，任何电脑。」
H1_ZH = '<h1>任何 <span class="en">agent</span>，<br>任何电脑。</h1>'
H1B_ZH = '<h1 style="margin-top:56px">任何 <span class="en">agent</span>，<br>任何电脑。</h1>'
_C12_ZH = """  <p class="claim"><b>沙盒</b>：高效、可扩展，内置 <b class="lc">30k+</b> 个可验证 CUA 任务</p>
  <p class="claim"><b>数据</b>：10+ 个 SFT 数据集、前沿 CUA rollout</p>"""
CLAIMS_ZH = f'<div class="claims">\n{_C12_ZH}\n  <p class="claim"><b>框架</b>：评测、SFT、RL，覆盖 <b class="lc">桌面、浏览器与移动端</b></p>\n</div>'
CLAIMS_A_ZH = CLAIMS_B_ZH = CLAIMS_ZH
DEVICES_ZH = f"""<div class="devices">
  <div class="devcol"><img class="d-desktop" src="{DEV}/dev-desktop.png" alt=""><span class="dev-lab">桌面</span></div>
  <div class="devcol"><img class="d-browser" src="{DEV}/dev-browser.png" alt=""><span class="dev-lab">浏览器</span></div>
  <div class="devcol"><img class="d-mobile" src="{DEV}/dev-mobile.png" alt=""><span class="dev-lab">移动端</span></div>
</div>"""
FOOT_ZH = """<div class="foot">
  <div class="stats"><b>30k+</b> 任务 <i>·</i> <b>10+</b> 数据集 <i>·</i> <b>10+</b> agent <i>·</i> <b>15+</b> benchmark</div>
  <div class="url">cua-lite.github.io</div>
</div>"""
BODY_A_ZH = f'{BRAND}<div class="mid">{H1}{LEAD_ZH}{CLAIMS_A_ZH}</div>{FOOT_ZH}'
BODY_B_ZH = f'{BRAND}{H1B}{LEAD_ZH}{CLAIMS_B_ZH}<div class="grow"></div>{DEVICES_ZH}<div class="grow"></div>{FOOT_ZH}'

# (name, height, body, head)
VARIANTS = [
    ("01a-cover.png",    1240, BODY_A,    HEAD),
    ("01b-cover.png",    1440, BODY_B,    HEAD),
    ("01a-cover-zh.png", 1240, BODY_A_ZH, HEAD_ZH),
    ("01b-cover-zh.png", 1440, BODY_B_ZH, HEAD_ZH),
]


def main() -> None:
    tmp = ROOT / "_red_cover_tmp.html"
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--directory", str(ROOT)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.0)
        with sync_playwright() as p:
            b = p.chromium.launch()
            for name, height, body, head in VARIANTS:
                tmp.write_text(head.replace("%HEIGHT%", str(height)) + body + "</body></html>")
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
