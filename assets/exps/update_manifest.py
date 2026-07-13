"""Regenerate eval/manifest.json — the leaderboard's pointer to each env's newest runs.

Drop a run snapshot into assets/exps/eval/<env>/<commit-dir>/run_<n>[_<config>].json
(copied from the cua-lite repo's devs/exps/eval/<env>/logs/...), then:

    python3 assets/exps/update_manifest.py

An env can ship several config settings side by side (run_0_default.json,
run_0_som.json, ...) — each becomes a manifest entry, and the leaderboard shows
them as secondary tabs. A bare run_<n>.json is the "default" config. Newest run
per config wins: by the commit-dir's date prefix when it has one
(2026-07-06T20-34_<sha>), otherwise by file mtime.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

EVAL = Path(__file__).resolve().parent / "eval"
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}")


def sort_key(path: Path) -> tuple[int, str, float]:
    m = DATED.match(path.parent.name)
    # dated dirs rank above undated ones; ties fall back to mtime
    return (1, m.group(0), path.stat().st_mtime) if m else (0, "", path.stat().st_mtime)


def is_run_json(path: Path) -> bool:
    """A publishable run: valid JSON with a non-empty results list."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        print(f"  skipping {path.relative_to(EVAL)}: not valid JSON (empty or still being written?)")
        return False
    if not isinstance(data, dict) or not data.get("results"):
        print(f"  skipping {path.relative_to(EVAL)}: no results")
        return False
    return True


RUN_RE = re.compile(r"^run_\d+(?:_(?P<cfg>.+))?\.json$")


def main() -> None:
    manifest: dict[str, dict[str, str]] = {}
    for env_dir in sorted(p for p in EVAL.iterdir() if p.is_dir()):
        by_cfg: dict[str, Path] = {}   # config -> newest run file
        for path in env_dir.glob("*/run_*.json"):
            m = RUN_RE.match(path.name)
            if not m or not is_run_json(path):
                continue
            cfg = m.group("cfg") or "default"
            if cfg not in by_cfg or sort_key(path) > sort_key(by_cfg[cfg]):
                by_cfg[cfg] = path
        if by_cfg:
            ordered = sorted(by_cfg, key=lambda c: (c != "default", c))   # default first, then a-z
            manifest[env_dir.name] = {c: by_cfg[c].relative_to(env_dir).as_posix() for c in ordered}
    out = EVAL / "manifest.json"
    # no sort_keys: envs are inserted sorted, but config order (default first) must survive
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(Path.cwd()) if out.is_relative_to(Path.cwd()) else out} ({len(manifest)} envs)")
    for env, cfgs in manifest.items():
        print(f"  {env}: " + " · ".join(f"{c} = {rel}" for c, rel in cfgs.items()))


if __name__ == "__main__":
    main()
