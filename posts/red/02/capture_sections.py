"""Capture blog/kvm-free-osworld figures as tight, transparent cutouts → build/fig/.

Feeds make_cover.py (grid hero) and make_slides.py (portrait designed cards). Each figure is
captured on transparency, own outer shadow stripped, tight-cropped; site-only interaction
hints in captions are rewritten to static text.

    uv run python posts/red/02/capture_sections.py
Playwright's launch() cannot start Chromium on this host (SIGTRAP, no stderr — see
posts/twitter/01/make_assets.py for the bisection). Start Chrome yourself and set CUA_LITE_CDP:

    ~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome --headless --no-sandbox \
      --disable-gpu --autoplay-policy=no-user-gesture-required --remote-debugging-port=9411 --user-data-dir=/tmp/pw &
    CUA_LITE_CDP=http://127.0.0.1:9411 uv run python posts/red/02/capture_sections.py

"""
from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent.parent   # posts/red/02/ -> repo root
FIG = Path(__file__).resolve().parent / "build" / "fig"
URL = "/blog/kvm-free-osworld/"
PORT = 8801

FREEZE = ("header.nav{display:none !important;}"
          " .belt-track, .belt-track-rev{animation-play-state:paused !important;}"
          " .reveal{opacity:1 !important; transform:none !important; visibility:visible !important;}"
          " .flow-demo, .cmp, .par, .belt-fig, .hh{box-shadow:none !important; filter:none !important;}"
          " .belt{-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 14%,#000 86%,transparent 100%) !important;"
          " mask-image:linear-gradient(90deg,transparent 0,#000 14%,#000 86%,transparent 100%) !important;}"
          # hh: stack the two panels vertically & full-width so each rollout frame is legible;
          # drop the tab row (fake-interactive on a still) and the scrub/live video chrome.
          " .hh-pair{grid-template-columns:1fr !important; gap:16px !important;}"
          " .hh-tabs{display:none !important;}"
          " .hh-panel::before{display:none !important;}"
          " .hh-scrub, .hh-live{display:none !important;}")

_FORCE_GRID = ("(()=>{for(let i=1;i<99999;i++){clearInterval(i);clearTimeout(i);}"
               "const e=document.querySelector('.v2c');if(e){e.classList.remove('s1','s2');e.classList.add('s3');}"
               "const n=document.querySelector('.v2c-note');"
               "if(n)n.textContent='Replicate the container \\u2014 rollouts run in parallel.';})()")
_FORCE_S1 = ("(()=>{for(let i=1;i<99999;i++){clearInterval(i);clearTimeout(i);}"
             "const e=document.querySelector('.v2c');if(e){e.classList.remove('s2','s3');e.classList.add('s1');}"
             "const n=document.querySelector('.v2c-note');"
             "if(n)n.textContent='A desktop sealed in a VM \\u2014 every task boots QEMU/KVM.';})()")
_FORCE_S2 = ("(()=>{for(let i=1;i<99999;i++){clearInterval(i);clearTimeout(i);}"
             "const e=document.querySelector('.v2c');if(e){e.classList.remove('s1','s3');e.classList.add('s2');}"
             "const n=document.querySelector('.v2c-note');"
             "if(n)n.textContent='Out of the VM \\u2014 the same desktop, now a container.';})()")
_FIX_PARCAP = ("(()=>{const c=document.querySelector('.par-cap');"
               "if(c)c.textContent='OSWorld vs Lite.OSWorld \\u00b7 13 models \\u00b7 identical tasks';})()")
_HH_STACK = ("(()=>{const hh=document.querySelector('.hh');if(!hh)return;"
             "const c=hh.querySelector('.hh-cap');"
             "if(c)c.textContent='Same model, same task \\u00b7 OSWorld (top) vs Lite.OSWorld (bottom)';"
             "hh.querySelectorAll('.hh-vid').forEach(v=>{try{v.pause();const d=v.duration;"
             "if(d&&isFinite(d))v.currentTime=d*0.5;}catch(e){}});})()")
_FAMILY_CAP = ("(()=>{const c=document.querySelector('.belt-cap');"
               "if(c)c.textContent='Every sandbox ships verifiable tasks';})()")

# (name, selector, settle ms, wait-for predicate, force JS)
TARGETS = [
    ("vm",        ".v2c",      1200, None, _FORCE_S1),   # VM state (left of the before/after)
    ("container", ".v2c",      1200, None, _FORCE_S2),   # container state (right of the before/after)
    ("grid",      ".v2c",      1500, None, _FORCE_GRID),
    ("footprint", ".cmp",       800, None, None),
    ("hh",        ".hh",       2200, "[...document.querySelectorAll('.hh-vid')].every(v=>v.readyState>=2)", _HH_STACK),
    ("parity",    ".par",      1600, "document.querySelectorAll('.par-svg circle,.par-svg .par-dot').length > 0", _FIX_PARCAP),
    ("belt",      ".belt-fig", 1600, None, _FAMILY_CAP),
]


def tight(path: Path, thresh: int = 110) -> None:
    im = Image.open(path).convert("RGBA")
    r, g, b, a = im.split()
    a = a.point(lambda v: v if v >= thresh else 0)
    im = Image.merge("RGBA", (r, g, b, a))
    bbox = a.getbbox()
    if bbox:
        im.crop(bbox).save(path)


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
    FIG.mkdir(parents=True, exist_ok=True)
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--directory", str(ROOT)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        _wait_for_server(PORT)
        with sync_playwright() as p:
            cdp = os.environ.get("CUA_LITE_CDP")
            b = (p.chromium.connect_over_cdp(cdp) if cdp
                 else p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]))
            for name, sel, wait_ms, pred, force in TARGETS:
                pg = b.new_page(viewport={"width": 960, "height": 1400}, device_scale_factor=2)
                pg.goto(f"http://localhost:{PORT}{URL}")
                pg.wait_for_timeout(500)
                pg.locator(sel).first.scroll_into_view_if_needed()
                if pred:
                    try:
                        pg.wait_for_function(pred, timeout=9000)
                    except Exception:
                        print(f"  ! {name}: predicate timeout")
                if force:
                    pg.evaluate(force)
                pg.wait_for_timeout(wait_ms)
                pg.add_style_tag(content=FREEZE)
                pg.locator(sel).first.screenshot(path=str(FIG / f"{name}.png"), omit_background=True)
                tight(FIG / f"{name}.png")
                pg.close()
                print(f"figure {name}")
            b.close()
    finally:
        srv.terminate()
    print("done")


if __name__ == "__main__":
    main()
