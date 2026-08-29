"""Build the hand-off package for whoever posts the LinkedIn article: LINKEDIN.md + linkedin.zip.

    uv run python posts/linkedin/make_package.py        # all articles
    uv run python posts/linkedin/make_package.py 01

A sibling of posts/twitter/make_package.py, deliberately NOT the same script: a thread is a
numbered sequence of posts with per-post media and a fold budget, an article is one title, one
cover and a body with inline figures. Sharing one code path would mean a pile of `if platform ==`.
What IS shared is the discipline, and every rule below was learnt the hard way over there:

  · LINKEDIN.md is generated, never hand-written. A second hand-kept copy of the copy drifts from
    README.md the moment either is edited — that is the defect the twitter thread's own review
    rounds kept finding in its own annotations.
  · English only. The package goes to someone outside the project; the Chinese design notes in
    README.md are not theirs to read. The build fails if any CJK survives.
  · Every referenced image must exist, and the summary reports what was PACKED, not what was
    referenced. Those two numbers differed silently in the first version of the twitter script.
  · Missing body, missing asset, stray CJK: all fail loudly with a non-zero exit. A package that
    is quietly wrong is worse than no package.
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def field(md: str, name: str) -> str:
    """A `**Name**` line's value — the title, the cover, and so on."""
    m = re.search(rf"^\*\*{name}\*\*\s*\n?\s*(.+?)$", md, re.M)
    return m.group(1).strip() if m else ""


def fenced_after(md: str, label: str) -> str:
    m = re.search(rf"\*\*{label}\*\*\s*\n\n```\n(.*?)\n```", md, re.S)
    return m.group(1).strip() if m else ""


def build(slug: str) -> None:
    here = ROOT / slug
    md = (here / "README.md").read_text()

    title = fenced_after(md, "Title")
    body = fenced_after(md, "Body")
    if not title:
        raise SystemExit(f"{slug}: no ``` block under **Title** — nothing to post.")
    if not body:
        raise SystemExit(f"{slug}: no ``` block under **Body** — nothing to post.")

    cover = re.search(r"`(assets/[^`]+)`", field(md, "Cover") or "")
    cover = cover.group(1) if cover else None
    if not cover:
        raise SystemExit(f"{slug}: **Cover** names no assets/… file.")

    inline = re.findall(r"^\[(assets/[^\]]+)\]$", body, re.M)
    used = [cover] + inline

    out = [
        "# " + title,
        "",
        "<!-- GENERATED from README.md by ../make_package.py. Do not edit by hand:",
        "     edit README.md, then re-run the generator. -->",
        "",
        f"**Cover** `{cover}`",
        "",
        "---",
        "",
        body,
        "",
    ]
    doc = "\n".join(out).rstrip() + "\n"

    cjk = sorted({c for c in doc if "　" <= c <= "鿿" or "！" <= c <= "･"})
    if cjk:
        raise SystemExit(f"{slug}: LINKEDIN.md must be English-only; found CJK: {''.join(cjk)}")

    missing = sorted({f for f in used if not (here / f).exists()})
    (here / "LINKEDIN.md").write_text(doc)

    packed = 0
    with zipfile.ZipFile(here / "linkedin.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(here / "LINKEDIN.md", "LINKEDIN.md")
        for f in dict.fromkeys(used):                  # keep article order, drop repeats
            if (here / f).exists():
                z.write(here / f, f)                   # follows the symlink, stores the bytes
                packed += 1

    mb = (here / "linkedin.zip").stat().st_size / 1e6
    print(f"{slug}: LINKEDIN.md ({len(body.split())} words, {len(inline)} inline figures) "
          f"+ linkedin.zip ({packed} images, {mb:.1f} MB)")
    if missing:
        raise SystemExit(f"{slug}: {len(missing)} image(s) referenced but not on disk — the zip is "
                         f"incomplete: {', '.join(missing)}")


def main() -> None:
    slugs = sys.argv[1:] or sorted(d.name for d in ROOT.iterdir() if d.is_dir() and d.name.isdigit())
    if not slugs:
        raise SystemExit("no article directories found under posts/linkedin/")
    for s in slugs:
        build(s)


if __name__ == "__main__":
    main()
