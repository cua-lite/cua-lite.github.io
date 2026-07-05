#!/usr/bin/env bash
# Refresh the homepage's vendored pixel + showcase assets from the canonical source:
# the main cua-lite repo (sibling checkout). Source of truth lives there; the homepage
# keeps a small self-contained copy so it clones cheap and Pages builds with no submodule.
#
#   bash scripts/sync_assets.sh [path-to-cua-lite-repo]   # default: ../cua-lite
set -euo pipefail
cd "$(dirname "$0")/.."
SRC="${1:-../cua-lite}/assets/README"

if [ ! -d "$SRC" ]; then
  echo "error: canonical assets not found at $SRC" >&2
  echo "pass the cua-lite repo path: bash scripts/sync_assets.sh /path/to/cua-lite" >&2
  exit 1
fi

mkdir -p assets/pixel assets/showcase
cp "$SRC"/teaser/assets/{wallpaper,cursor,sparkle,airplane,bezel_overlay}.png assets/pixel/
cp "$SRC"/showcase/{lite_osworld,webarena,mobilegym,androidworld,lite_demo}.gif assets/showcase/

echo "synced pixel + showcase assets from $SRC"
ls -1 assets/pixel assets/showcase
