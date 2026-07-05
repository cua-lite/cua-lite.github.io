"""Render a page to PNG for visual debugging (this is how we iterate on the design).

    uv run python scripts/shot.py <url_or_file> <out.png> [width] [height] [wait_ms] [--full]

Examples:
    uv run python scripts/shot.py index.html /tmp/hero.png 1440 900 1500
    uv run python scripts/shot.py http://localhost:8080 /tmp/full.png 1440 900 2000 --full
"""
from __future__ import annotations

import os
import sys

from playwright.sync_api import sync_playwright


def main() -> None:
    url, out = sys.argv[1], sys.argv[2]
    w = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 1440
    h = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else 900
    wait = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5].isdigit() else 1200
    full = "--full" in sys.argv
    if "://" not in url:
        url = "file://" + os.path.abspath(url)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        page.goto(url)
        page.wait_for_timeout(wait)
        page.screenshot(path=out, full_page=full)
        browser.close()
    print("wrote", out)


if __name__ == "__main__":
    main()
