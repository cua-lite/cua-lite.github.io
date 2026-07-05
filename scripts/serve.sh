#!/usr/bin/env bash
# Serve the static site locally for preview.
#   bash scripts/serve.sh [port]
set -euo pipefail
cd "$(dirname "$0")/.."
PORT="${1:-8080}"
echo "serving CUA-Lite homepage at http://localhost:${PORT}  (Ctrl-C to stop)"
python3 -m http.server "$PORT"
