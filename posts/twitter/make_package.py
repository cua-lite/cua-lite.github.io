"""Build the hand-off package for whoever posts a thread: TWITTER.md + twitter.zip.

    uv run python posts/twitter/make_package.py 01
    uv run python posts/twitter/make_package.py 02
    uv run python posts/twitter/make_package.py            # both

ONE script for both threads, on purpose. A per-thread copy would drift the moment one was
edited — which is the same failure this thread's review rounds kept finding in its own notes
(a **Bold** field naming a phrase the post no longer contained). For the same reason TWITTER.md
is generated, never hand-written: every line of copy is extracted from that thread's README.md
at build time, so the two cannot disagree.

The output is ENGLISH ONLY — it goes to someone outside the project, and the Chinese design
notes in README.md are not theirs to read. The build fails loudly if any CJK survives.

The zip carries TWITTER.md plus ONLY the files the thread actually posts. The .gif twin of each
.mp4, the unused wide variants and the spare figures are left out: a package offering two
encodings of the same clip is a package where someone uploads the wrong one. Upload the MP4 —
X transcodes an uploaded GIF to silent MP4 anyway, costing an extra encode and hitting a
15 MB desktop / 5 MB mobile cap the MP4 does not.
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# README.md headings are English except these. Anything else Chinese trips the guard below.
HEADINGS = {"收尾 — Acknowledgements（不编号）": "Acknowledgements (unnumbered)"}


def posts_of(md: str) -> list[tuple[str, str]]:
    """Every ### under '## The thread', up to whatever ## heading follows it.

    The end marker differs per thread (01 ends at '## Posting notes', 02 at '## 归属'), so it is
    found rather than hard-coded — a hard-coded marker silently yields zero posts on the thread
    it does not match.
    """
    block = md[md.index("## The thread"):]
    nxt = re.search(r"\n## ", block[3:])
    if nxt:
        block = block[: nxt.start() + 3]
    parts = re.split(r"^### (.+)$", block, flags=re.M)[1:]
    return list(zip(parts[0::2], parts[1::2]))


def body(chunk: str) -> str:
    m = re.search(r"```\n(.*?)\n```", chunk, re.S)
    return m.group(1).strip() if m else ""


def media(chunk: str) -> list[str]:
    """Only files named BEFORE the rationale are attachments. The prose after the first em-dash
    or sentence break cites other files (the repo's own demo-trace.mp4, a landscape variant,
    a figure's source id) that must not reach the person posting."""
    m = re.search(r"^\*\*Media\*\* (.+?)(?=\n\s*\n|\n\*\*[A-Z]|\Z)", chunk, re.M | re.S)
    if not m:
        return []
    v = " ".join(m.group(1).split())
    if v.lower().startswith("none"):
        return []
    head = re.split(r" — |(?<=[.。]) ", v, maxsplit=1)[0]
    return re.findall(r"`(assets/[^`]+)`", head)


def build(thread: str) -> None:
    here = ROOT / thread
    entries = posts_of((here / "README.md").read_text())
    if not entries:
        raise SystemExit(f"{thread}: no posts found under '## The thread'")

    out = ["# CUA-Lite — X thread", "",
           "<!-- GENERATED from README.md by ../make_package.py. Do not edit by hand:",
           "     edit README.md, then re-run the generator. -->", "", "---", ""]
    used: list[str] = []
    shipped = 0
    for head, chunk in entries:
        text = body(chunk)
        if not text:
            # never skip in silence: a post without a fenced block means the README was edited
            # into a shape this script cannot read, and a package missing a post is worse than
            # no package at all.
            raise SystemExit(f"{thread}: post {head.strip()!r} has no ``` block — "
                             f"nothing to post. Fix README.md.")
        shipped += 1
        files = media(chunk)
        used += files
        out += [f"## {HEADINGS.get(head.strip(), head.strip())}", "", text, "",
                "**Media** " + (" + ".join(f"`{f}`" for f in files) if files
                                else "none — text only."),
                "", "---", ""]

    missing = sorted({f for f in used if not (here / f).exists()})
    if missing:
        out += ["> **Missing files** — referenced above but not in this package:",
                "> " + " · ".join(f"`{m}`" for m in missing), ""]

    doc = "\n".join(out).rstrip() + "\n"
    cjk = sorted({c for c in doc if "　" <= c <= "鿿" or "！" <= c <= "･"})
    if cjk:
        raise SystemExit(f"{thread}: TWITTER.md must be English-only; found CJK: {''.join(cjk)}\n"
                         f"  Add the heading to HEADINGS, or fix README.md.")
    (here / "TWITTER.md").write_text(doc)

    packed = 0
    with zipfile.ZipFile(here / "twitter.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(here / "TWITTER.md", "TWITTER.md")          # follows symlinks; stores content
        for f in sorted(set(used)):
            if (here / f).exists():
                z.write(here / f, f)
                packed += 1

    mb = (here / "twitter.zip").stat().st_size / 1e6
    # report what was PACKED, not what was referenced — those differed silently before.
    print(f"{thread}: TWITTER.md ({shipped} posts) + twitter.zip ({packed} assets, {mb:.1f} MB)")
    if missing:
        raise SystemExit(f"{thread}: {len(missing)} asset(s) referenced but not on disk — the zip "
                         f"is incomplete: {', '.join(missing)}")


def main() -> None:
    for t in sys.argv[1:] or ["01", "02"]:
        build(t)


if __name__ == "__main__":
    main()
