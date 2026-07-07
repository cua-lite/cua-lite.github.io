"""Generate assets/apple-touch-icon.png — the iOS home-screen tile.

The terracotta paper-plane mark (logo.svg) centered on the cream brand background,
as a FULL-BLEED opaque square (180x180). Apple masks it into a rounded "squircle"
on-device, so we do NOT pre-round it — that avoids the white-corner / double-round
artifacts of a baked-in radius. PLANE_PCT sets how much of the tile the plane fills.

    uv run python scripts/make_apple_icon.py
"""
from __future__ import annotations

import io
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SIZE = 180
BG = "#faf4e8"          # brand cream (matches nav/footer)
PLANE_SVG_PX = 152      # plane render width -> ~67% ink coverage, comfortable margin

PLANE = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'style="width:{w}px;height:{w}px;display:block">'
    '<path d="M22 2 L2 9.2 L10.6 12.8 L14.4 21.5 Z" fill="#bd5a38"/>'
    '<path d="M22 2 L10.6 12.8" stroke="#faf4e8" stroke-width="1.15" stroke-linecap="round"/>'
    "</svg>"
)


def main() -> None:
    html = (
        "<!doctype html><meta charset=utf8><style>*{margin:0;padding:0}"
        f".t{{width:{SIZE}px;height:{SIZE}px;background:{BG};display:flex;"
        "align-items:center;justify-content:center}</style>"
        f'<div class="t">{PLANE.format(w=PLANE_SVG_PX)}</div>'
    )
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": SIZE, "height": SIZE}, device_scale_factor=3)
        pg.set_content(html)
        pg.wait_for_timeout(120)
        png = pg.query_selector(".t").screenshot()  # opaque (no omit_background)
        b.close()
    img = Image.open(io.BytesIO(png)).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    out = ROOT / "assets" / "apple-touch-icon.png"
    img.save(out)
    print(f"wrote {out} {img.size}")


if __name__ == "__main__":
    main()
