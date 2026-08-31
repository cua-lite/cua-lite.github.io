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


def provenance(md: str, body: str, slug: str) -> None:
    """Every body line must come from the thread's posts, from a blog, or be a declared deviation.

    Why this exists: the rule "sentences come verbatim from twitter/01" used to be enforced by
    eyeballing a 逐字率. That number stays high while whole sections are reordered and headings are
    rewritten, because it counts sentences. On 2026-08-30 that gap let four content-level rewrites
    through, each justified in the moment and none recorded.

    The first version of this gate had five holes of its own, all found by audit:
      · it skipped every `##` line, so a rewritten heading could never fail;
      · it skipped every list block, so reordering the resource list was invisible;
      · it skipped paragraphs starting with a digit, exempting a real prose sentence;
      · its pool was the whole thread README, so a sentence that existed only in a Chinese design
        note counted as "upstream";
      · `…`-truncated Deviations entries whitelisted by prefix, so a 7-word entry authorised a
        six-line paragraph.
    All five are closed below. Headings and list lines are checked; the pool is the fenced posts
    plus blog prose only; an entry must be substantial enough to identify what it licenses.
    """
    up = ROOT.parent.parent
    thread = (up / "posts/twitter/01/README.md").read_text()
    thread = thread[thread.index("## The thread"):]
    posts = re.findall(r"### [^\n]+\n\n```\n(.*?)\n```", thread, re.S)
    blogs = [re.sub(r"<[^>]+>", " ", f.read_text()) for f in sorted(up.glob("blog/*/index.html"))]
    flat = lambda t: re.sub(r"[\u2018\u2019]", "'",
                            re.sub(r"[\u2014\u2013]", "-", re.sub(r"\s+", " ", t))).strip()
    pool = flat(" ".join(posts + blogs))
    titles = {flat(re.sub(r"^\[\d+/\d+\] ", "", t)).rstrip(".")
              for t in re.findall(r"### ([^\n]+)", thread)}

    allowed, short, heads = set(), [], set()
    m = re.search(r"\n## Deviations\s*\n(.*?)(?=\n## |\Z)", md, re.S)
    if m:
        # only the `- \`…\`` bullets are entries; the prose around them also uses backticks.
        # A prose entry must be long enough to identify what it licenses; a HEADING entry is
        # short by nature, so it is matched exactly against the heading instead.
        for bullet in re.findall(r"^- (`[^\n]+)", m.group(1), re.M):
            for q in re.findall(r"`([^`]+)`", bullet):
                e = flat(q).rstrip(" .\u2026")
                if len(e) >= 60:
                    allowed.add(e)
                elif e:
                    heads.add(e.lstrip("# ").strip())
    if short:
        raise SystemExit(f"{slug}: Deviations entries too short to identify what they license "
                         f"(need >=60 chars): {short}")

    LINK = ("Site:", "Code:", "Data:", "Leaderboard:", "[assets/")
    MARK = re.compile(r"^(?:[\u2192\u00b7\-]|\d+ \u00b7|[\U0001F300-\U0001FAFF\u2600-\u27BF][\uFE0F]?)\s+")
    bad = []
    for block in re.split(r"\n\s*\n", body):
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        if lines[0].startswith("## "):                   # headings: must be a thread post title
            h = flat(re.sub(r"^##\s*\W*\s*", "", lines[0])).rstrip(".")
            if h not in titles and h not in heads and not any(h in a or a in h for a in allowed):
                bad.append(f"heading not a thread post title: {lines[0]}")
            continue
        if lines[0].startswith(LINK) or lines[0] == "---":
            continue
        # a list block is checked line by line (markers stripped); prose is joined first, so a
        # wrapped sentence is not split down the middle
        if MARK.match(lines[0]):
            units = [MARK.sub("", l) for l in lines]
        else:
            units = [" ".join(lines)]
        for unit in units:
            for sent in re.split(r"(?<=[.!?]) +", flat(unit)):
                if len(sent) < 26:
                    continue
                if sent in pool or any(sent.startswith(a) or a.startswith(sent) for a in allowed):
                    continue
                bad.append(sent)
    if bad:
        lines = "\n".join(f"    \u00b7 {b}" for b in bad)
        raise SystemExit(
            f"{slug}: {len(bad)} line(s) are neither verbatim upstream nor declared under\n"
            f"  **Deviations** in README.md. Either take the upstream wording, change `twitter/01`\n"
            f"  so both surfaces move together, or record the deviation and why:\n{lines}")


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

    provenance(md, body, slug)

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
