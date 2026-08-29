"""Capture thread 02's media from blog 2, named by thread 02's post numbers.

Thread 02 first shipped by symlinking thread 01's files. That was wrong twice over: the
names carried 01's post numbers (`03-vm-tax.mp4` sat on 02's post 2), and one asset —
blog 2's own belt, `figure.belt-fig`, captioned "Looping rollout trajectories" — had never
been captured at all, because 01's belt clip comes from the OTHER blog. Every figure this
thread shows now comes from the blog this thread is about.

    # 1. start Chrome yourself — Playwright's launch() is broken on this host, see
    #    posts/twitter/01/make_assets.py's docstring for the full bisection
    ~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome \
      --headless --no-sandbox --disable-gpu --disable-dev-shm-usage \
      --remote-debugging-port=9401 --user-data-dir=/tmp/pw &
    until curl -sf http://127.0.0.1:9401/json/version >/dev/null; do sleep 0.5; done

    # 2. capture (accepts asset names as args; no args = all)
    CUA_LITE_CDP=http://127.0.0.1:9401 uv run python posts/twitter/02/make_assets.py

    # 3. GIFs, separately — never in the same run, see PITFALL 2 in 01's docstring
    uv run python posts/twitter/02/make_assets.py gif

Three capture settings are copied from 01 deliberately, each with its reason recorded there:
`tabbed_clip` + `order=[3,2,1,0]` + a paused `.belt-track` for the belt (without them the clip
never leaves the first tab — 02 shipped 8 s of Lite.OSWorld under a post that lists four
sandboxes), and `min_ar=None` for the portrait parity plot (padding it landscape wastes a
quarter of the card).

All the machinery lives in thread 01's script and is imported, not copied: `cast`, `retime`,
`encode`, the CFR/ffmpeg-path detection, the crop clamping, and every pitfall fix recorded
there. Only the figure list and the names are 02's.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "01"))
import make_assets as m1                                            # noqa: E402
from playwright.sync_api import sync_playwright                     # noqa: E402

OUT = Path(__file__).resolve().parent / "assets"
BLOG = "/blog/kvm-free-osworld/"

# Post number → (asset name, selector on blog 2, capture kwargs). The order is the thread's.
FIGURES = [
    # post 1 — the whole thesis in one loop: sealed VM → container → parallel grid
    ("01-vm-to-container.mp4", "figure.flow-demo.v2c",
     dict(secs=15.5, settle=6, cycle=7.45, margin=18, scale=1)),
    # post 2 — same model, same task, OSWorld's VM beside Lite.OSWorld's container
    ("02-head-to-head.mp4", "figure.hh",
     dict(tabbed=".hh-tab", secs=18.0, hold=2.2, settle=6,
          extra_css=".hh-cap{visibility:hidden !important}")),
    # post 3 — the footprint table
    ("03-footprint.png", "figure.cmp", dict(still=True, min_ar=m1.MIN_AR)),
    # post 4 — the parity plot, 13 models
    ("04-parity.png", "figure.par", dict(still=True, js=(
        "document.querySelector('figure.par figcaption').textContent = "
        "'Success rate (%) · 13 models · same desktop, same evaluators';"))),
    # post 5 — BLOG 2's OWN belt. Not blog 1's. This is the one that was missing: 01's
    # 04-sandboxes.mp4 comes from /blog/why-cua-lite/ and shows a different figure.
    ("05-sandbox-family.mp4", "figure.belt-fig",
     dict(tabbed=".belt-tab", secs=14.0, hold=3.2, settle=8, order=[3, 2, 1, 0],
          extra_css=".belt-cap{visibility:hidden !important}"
                    ".belt-track{animation-play-state:paused !important}")),
]

RETIME = {                      # finished-file durations; see PITFALL 7 in 01's docstring
    "01-vm-to-container.mp4": (9.0, 0.5),
    "02-head-to-head.mp4": (10.5, 0.6),
    "05-sandbox-family.mp4": (8.0, 0.5),
}


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "gif"]
    only_gifs = "gif" in sys.argv[1:]
    want = lambda n: not args or any(a in n for a in args)
    OUT.mkdir(parents=True, exist_ok=True)
    m1.OUT = OUT                       # every helper writes through this module-level path
    m1.TMP.mkdir(parents=True, exist_ok=True)

    # 01's main() starts the site server; importing its helpers does not, so start one here.
    import subprocess, time, urllib.request
    server = None
    try:
        urllib.request.urlopen(m1.BASE, timeout=1)
    except Exception:
        server = subprocess.Popen([sys.executable, "-m", "http.server", str(m1.PORT)],
                                  cwd=m1.ROOT, stdout=subprocess.DEVNULL,
                                  stderr=subprocess.STDOUT)
        time.sleep(1.5)
    try:
        if not only_gifs:
            with sync_playwright() as pw:
                cdp = os.environ.get("CUA_LITE_CDP")
                browser = pw.chromium.connect_over_cdp(cdp) if cdp else pw.chromium.launch()
                ctx = browser.new_context(viewport={"width": 1180, "height": 950},
                                          device_scale_factor=m1.DPR)
                mark = m1.make_mark(ctx)
                for name, sel, kw in FIGURES:
                    if not want(name):
                        continue
                    print(f"capture: {name}")
                    kw = dict(kw)
                    if kw.pop("still", False):
                        m1.still(ctx, name, BLOG, sel, mark=mark, js=kw.pop("js", None), min_ar=kw.pop("min_ar", None))
                    elif "tabbed" in kw:
                        m1.tabbed_clip(browser, name, BLOG, sel, kw.pop("tabbed"), mark, **kw)
                    else:
                        m1.figure_clip(browser, name, BLOG, sel, mark=mark, **kw)
                    if name in RETIME:
                        target, head = RETIME[name]
                        m1.retime(name, target, head=head)
                ctx.close()
                browser.close()
        if only_gifs or not args:
            m1.gifs()
    finally:
        if server:
            server.terminate()


if __name__ == "__main__":
    main()
