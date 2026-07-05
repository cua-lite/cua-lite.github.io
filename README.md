# cua-lite.github.io

Landing page for **[CUA-Lite](https://github.com/cua-lite/cua-lite)** — *Simple Computer Use Agents*.
Live at **https://cua-lite.github.io/**.

Design language: **refined retro computing** — warm paper canvas, ink, monospace type, hard
pixel-edged surfaces (2px borders, offset shadows, no blur), pixel cursor + pixel icons as accents.
The centerpiece is an interactive console: pick an **agent** × an **environment** and the same
`rollout.py` command + a live rollout preview update — the interaction *is* the pitch.

## Layout

```
index.html            # the page (nav · hero · try console · features · benchmarks · quick start)
css/style.css         # design system (palette, pixel surfaces, responsive)
js/main.js            # console controller (agent×env → preview + reproduce code) + click sparkle
assets/icons/         # pixel UI icons (blue PNGs used as background-image; + cursor)
assets/pixel/         # cursor / sparkle
assets/showcase/      # per-env rollout GIFs (Desktop/Web/Mobile), vendored from the main repo
scripts/              # serve.sh · shot.py (visual-debug screenshots) · sync_assets.sh
```

## Dev

The site is pure static HTML/CSS/JS — GitHub Pages serves it directly, no build step. Tooling is
only for local preview and visual-debug screenshots:

```bash
bash install.sh                 # locked uv env + chromium (playwright)
bash scripts/serve.sh           # http://localhost:8080
uv run python scripts/shot.py index.html /tmp/page.png 1440 900   # render to PNG to eyeball
```

Icons are drawn as low-res pixel bitmaps and upscaled nearest-neighbour (see the generator snippets
in git history); they're shipped as plain PNGs (not CSS masks) so they render identically in every
engine.

## Assets

Canonical rollout GIFs live in the main repo (`cua-lite/assets/README/showcase`). This repo vendors
a small copy so it clones cheap and Pages needs no submodule. Refresh with:

```bash
bash scripts/sync_assets.sh     # copies from ../cua-lite
```

## Deploy

GitHub Pages, served from the default branch root (`/`). Pushing to `main` publishes to
`https://cua-lite.github.io/`.
