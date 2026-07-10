"""Regenerate eval/manifest.json — the leaderboard's pointer to each env's newest run.

Drop a run snapshot into assets/exps/eval/<env>/<commit-dir>/run_<n>.json
(copied from the cua-lite repo's devs/exps/eval/<env>/logs/...), then:

    python3 assets/exps/update_manifest.py

Newest run per env wins: by the commit-dir's date prefix when it has one
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


def main() -> None:
    manifest: dict[str, str] = {}
    for env_dir in sorted(p for p in EVAL.iterdir() if p.is_dir()):
        runs = sorted((p for p in env_dir.glob("*/run_*.json") if is_run_json(p)), key=sort_key)
        if runs:
            manifest[env_dir.name] = runs[-1].relative_to(env_dir).as_posix()
    out = EVAL / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(Path.cwd()) if out.is_relative_to(Path.cwd()) else out} ({len(manifest)} envs)")
    for env, rel in manifest.items():
        print(f"  {env}: {rel}")


if __name__ == "__main__":
    main()
