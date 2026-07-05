# cua-lite.github.io

Pixel-art, interactive landing page for **[CUA-Lite](https://github.com/cua-lite/cua-lite)** —
*Simple Computer Use Agents*. Live at **https://cua-lite.github.io/**.

The whole page is a retro pixel-art **desktop**: it replays the README teaser (CRT powers on →
paper airplane → click → the "Bliss" grass wallpaper fills in), then each interaction *is* a piece
of the framework pitch:

| README pillar | On-page interaction |
|---|---|
| **Any CUA** | task-bar of agent pills — who's flying the plane |
| **Any environment** | the CRT is a channel switch: Desktop / Web / Mobile showcase GIFs |
| **Standardized data** | a floppy "saves" the rollout → `LiteSample` |
| **Eval any benchmark** | a retro high-score board |
| **RL any environment** | an XP / level-up bar (GRPO on Slime) |

## Layout

```
index.html            # the page
css/style.css         # pixel design system (palette locked to the wallpaper)
js/boot.js            # canvas boot narrative (replays the teaser)
js/desktop.js         # cursor + sparkle, channel switch, agent×env toy, scroll reveals
assets/pixel/         # cursor / sparkle / airplane / wallpaper / bezel  (vendored)
assets/showcase/      # per-env rollout GIFs                             (vendored)
scripts/              # serve.sh · shot.py (visual debug) · sync_assets.sh
```

## Dev

The site has **no runtime dependencies** — GitHub Pages serves the static files directly, no
build step. The only tooling is for local preview and visual-debug screenshots:

```bash
bash install.sh                 # locked uv env + chromium (playwright)
bash scripts/serve.sh           # http://localhost:8080
uv run python scripts/shot.py index.html /tmp/hero.png    # render to PNG to eyeball
```

## Assets

The canonical pixel/showcase assets live in the main repo
(`cua-lite/assets/README/{teaser,showcase}`). This repo vendors a small self-contained copy (so it
clones cheap and Pages needs no submodule). Refresh them with:

```bash
bash scripts/sync_assets.sh     # copies from ../cua-lite
```

## Deploy

GitHub Pages, served from the default branch root (`/`). Pushing to `main` publishes to
`https://cua-lite.github.io/`.
