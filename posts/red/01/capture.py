"""Capture homepage pieces for the 小红书 carousel — hero devices + each section.

Only the homepage (index.html) is sourced; nothing from the blogs. Animations are
frozen and each demo is nudged to a finished state so every still is clean. Devices
are captured on transparency and tight-cropped to their own silhouette.

    uv run python posts/red/01/capture.py
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent.parent   # posts/red/01/ -> repo root
RAW = Path(__file__).resolve().parent / "build" / "dev"   # intermediates live outside assets/ (assets = finals only)
PORT = 8795

# freeze every animation/transition and lay the hero devices out flat (kill the
# carousel's transforms/opacity) so each device can be screenshotted on its own.
FREEZE = """
*{animation:none !important; transition:none !important;}
.stage{position:static !important; height:auto !important; transform:none !important;}
.device{position:static !important; opacity:1 !important; transform:none !important;
  filter:none !important; visibility:visible !important; display:block !important; margin:0 0 40px 0 !important;}
/* drop only the OUTER frame shadows (the big soft glow that halos the whole device);
   inner cell/window styling is kept. Any faint translucency that survives is removed in
   post by the alpha threshold in tight(). */
.dev-desktop, .dev-browser, .dev-mobile, .crt, .browser, .phone, .stage, .hero-demo{box-shadow:none !important;}
"""

# nudge each demo to a finished, populated state (frozen mid-animation looks unfinished)
POPULATE = """
(() => {
  const total = document.querySelector('#total'); if (total) total.textContent = '44';
  const fbar = document.querySelector('#fbar'); if (fbar) fbar.textContent = '=AVERAGE(B2:B5)';
  const home = document.querySelector('#gg-home'); if (home) home.style.display = 'none';
  const res = document.querySelector('#gg-results');
  if (res) { res.removeAttribute('aria-hidden'); res.style.display = ''; res.style.opacity = '1'; res.style.visibility = 'visible'; }
  const host = document.querySelector('#bw-host'); if (host) host.textContent = 'google.com/search?q=cua-lite';
  const sent = document.querySelector('#msent'); if (sent) { sent.removeAttribute('aria-hidden'); sent.classList.add('show'); }
  document.querySelectorAll('.mouse-cur').forEach(c => c.style.display = 'none');  // drop the demo cursor
})();
"""


def tight(path: Path, margin: int = 2, thresh: int = 110) -> None:
    """Erase the soft translucent halo, then crop to the solid device.

    Any pixel with alpha < thresh (a leftover soft shadow / glow around the rounded frame)
    is made fully transparent; the opaque device body and its inner styling are untouched.
    Then crop to what remains, keeping a hairline margin."""
    im = Image.open(path).convert("RGBA")
    r_, g_, b_, a = im.split()
    a = a.point(lambda v: v if v >= thresh else 0)   # kill the faint halo, keep the device
    im = Image.merge("RGBA", (r_, g_, b_, a))
    bbox = a.getbbox()
    if not bbox:
        return
    l, t, rr, bb = bbox
    l, t = max(0, l - margin), max(0, t - margin)
    rr, bb = min(im.width, rr + margin), min(im.height, bb + margin)
    im.crop((l, t, rr, bb)).save(path)
    print(f"  cropped {path.name} -> {rr - l}x{bb - t}")


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--directory", str(ROOT)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.0)
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1440, "height": 1600}, device_scale_factor=2)
            pg.goto(f"http://localhost:{PORT}/index.html")
            pg.wait_for_timeout(1400)
            pg.evaluate(POPULATE)
            pg.add_style_tag(content=FREEZE)
            pg.wait_for_timeout(200)
            # capture the INNER framed element for browser/phone (avoids neighbour bleed);
            # the desktop needs the whole .dev-desktop so its neck + base (the stand) come along.
            for sel, name in [(".dev-desktop", "dev-desktop"),
                              (".dev-browser .browser", "dev-browser"),
                              (".dev-mobile .phone", "dev-mobile")]:
                el = pg.locator(sel)
                el.scroll_into_view_if_needed()
                out = RAW / f"{name}.png"
                el.screenshot(path=str(out), omit_background=True)
                tight(out)
            b.close()
    finally:
        srv.terminate()
    print("done")


if __name__ == "__main__":
    main()
