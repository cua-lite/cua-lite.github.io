#!/usr/bin/env bash
# Reproducible dev setup for the CUA-Lite homepage.
#
#   bash install.sh
#
# The SITE itself needs nothing installed (static HTML/CSS/JS — GitHub Pages serves
# it directly). This only sets up the DEV tooling: a locked Python env (uv) with
# playwright for visual-debug screenshots, plus the Chromium it drives.
set -euo pipefail
cd "$(dirname "$0")"

# 1. locked python env from pyproject.toml (creates .venv + uv.lock -> reproducible)
uv sync

# 2. the headless browser playwright drives (reuses the shared ms-playwright cache)
uv run playwright install chromium

echo
echo "done. next:"
echo "  bash scripts/serve.sh                 # preview at http://localhost:8080"
echo "  uv run python scripts/shot.py <url> out.png   # visual-debug screenshot"
echo "  bash scripts/sync_assets.sh           # refresh pixel/showcase assets from ../cua-lite"
