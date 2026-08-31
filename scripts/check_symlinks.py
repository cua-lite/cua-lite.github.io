#!/usr/bin/env python3
"""Fail if any tracked symlink dangles. Run before pushing.

GitHub Pages refuses to build a site containing a symlink whose target is not in the
repository, and the only signal is a generic "Page build failed." in the builds API —
the site keeps serving the last good commit, so nothing looks wrong from the outside.

That happened here: `posts/twitter/01/assets/03-vm-tax.{gif,mp4}` were renamed to
`06-vm-tax.*` during the thread reorder, and two symlinks in `posts/reddit/02/assets/`
still pointed at the old names. Four commits and one push later the live site was still
two days stale, and it read as a browser-cache problem.

    uv run python scripts/check_symlinks.py
"""
import subprocess, sys
from pathlib import Path

root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
listing = subprocess.run(["git", "ls-files", "-s"], cwd=root,
                         capture_output=True, text=True, check=True).stdout
tracked = set(subprocess.run(["git", "ls-files"], cwd=root,
                             capture_output=True, text=True, check=True).stdout.split("\n"))

bad = []
for line in listing.splitlines():
    meta, _, path = line.partition("\t")
    if not meta.startswith("120000"):                      # 120000 = symlink
        continue
    target = (root / path).parent / (root / path).readlink()
    rel = target.resolve().relative_to(root.resolve()) if target.exists() else None
    if rel is None:
        bad.append(f"{path} -> {(root / path).readlink()}  (target does not exist)")
    elif str(rel) not in tracked:
        bad.append(f"{path} -> {rel}  (target exists but is not tracked by git)")

if bad:
    print("Dangling or untracked symlink targets — GitHub Pages will fail to build:")
    print("\n".join("  " + b for b in bad))
    sys.exit(1)
print(f"symlinks: all {sum(l.startswith('120000') for l in listing.splitlines())} resolve to tracked files")
