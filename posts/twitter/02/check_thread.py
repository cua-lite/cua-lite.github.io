#!/usr/bin/env python3
"""Gate every rule in README.md's 写作规约 at once, over thread 02.

Same checks as thread 01's copy — the rules are inherited, so the code is too. What differs:
the post count, the CTA index, and the STALE-NOTE check added at the end.

Why this exists: the failure mode on this file has not been carelessness, it has been
SERIAL constraint satisfaction — fixing whatever was most recently named and silently
breaking a property established three edits ago. A human editor holds all the rules at
once; this script is the substitute for that.

    uv run python posts/twitter/01/check_thread.py            # audit
    uv run python posts/twitter/01/check_thread.py --baseline # save current state
    uv run python posts/twitter/01/check_thread.py --diff     # what did my edit break?

Run it BEFORE editing (save a baseline) and AFTER (diff). A new FAIL that was a PASS in
the baseline is the thing to look at — that is the wall you just knocked down to patch
another one.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

N = 6            # posts in this thread, incl. the unnumbered opener
README = pathlib.Path(__file__).with_name("README.md")
BASELINE = pathlib.Path(__file__).with_name(".check_baseline.json")

FOLD = 280
URL_WEIGHT = 23
URL_RE = re.compile(r"\b[\w.-]+\.(?:io|com|co|ai|org)\b\S*")
# Concrete nouns a demonstrative can legitimately point at: they identify themselves,
# so `These sandboxes re-host …` needs no antecedent. Verbs and bare numerals stay OUT —
# an earlier list held `runs?` and `three`, which let `That base RUNS a family` and
# `These are the THREE gaps` through by matching the verb and the numeral as a noun.
NOUN = (r"sandboxes?|environments?|datasets?|tasks?|agents?|models?|instances?|benchmarks?|"
        r"corpora|corpus|suites?|formats?|schemas?|containers?|rollouts?|scores?|adapters?|"
        r"rewards?|trajector(?:y|ies)|commands?|screenshots?|actions?|samples?|gaps?")
# …but a RELATIONAL noun is not self-identifying: it still needs a prior antecedent, so it
# fails when the post is quoted alone. Every historical defect on this file was one of
# these — That base · That code · That glue · The same loop · of ours.
RELATIONAL = r"base|one|ones|thing|things|code|glue|loop|same|kind|part|piece|step|way|family"
BAD_OPENERS = re.compile(
    r"^\s*(?:(?:That|This|Those|These)\s+(?:" + RELATIONAL + r")\b"        # points at a relation
    r"|(?:That|This|Those|These)(?!\s+(?:\w+\s+){0,2}(?:" + NOUN + r"))"    # points at nothing
    r"|It|They|Both|No |Nothing|Three more of ours)\b")


# twitter-text weight-1 code point ranges; everything else weighs 2.
# NOTE: U+2014 EM DASH (8212) lives in [8208,8223] and weighs 1 — an earlier
# version of this file charged it 2 and reported every fold ~2 chars early.
_W1 = ((0, 4351), (8192, 8205), (8208, 8223), (8242, 8247))


def _cw(c: str) -> int:
    o = ord(c)
    return 1 if any(a <= o <= b for a, b in _W1) else 2


def weight(s: str) -> int:
    """X charges each URL a flat 23 regardless of its real length."""
    n = sum(_cw(c) for c in s)
    for u in URL_RE.findall(s):
        n += URL_WEIGHT - sum(_cw(c) for c in u)
    return n


def fold_cut(s: str) -> int:
    """Index of the first character hidden behind 'Show more', URL-weighted."""
    spans = {m.start(): m for m in URL_RE.finditer(s)}
    n, i = 0, 0
    while i < len(s):
        if i in spans:
            n += URL_WEIGHT
            i = spans[i].end()
        else:
            n += _cw(s[i])
            i += 1
        if n > FOLD:
            return i
    return len(s)


def posts() -> list[str]:
    body = README.read_text()
    thread = body[body.index("## The thread"):]
    return [b for _, b in re.findall(r"### ([^\n]+)\n\n```\n(.*?)\n```", thread, re.S)]


def sentences(paragraph: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", paragraph) if s.strip()]


def audit() -> dict[str, list[str]]:
    ps = posts()
    fails: dict[str, list[str]] = {}
    opener_shapes: dict[str, list[int]] = {}
    sentence_index: dict[str, list[int]] = {}

    for i, post in enumerate(ps, 1):
        bad: list[str] = []
        cut = fold_cut(post)
        visible, hidden = post[:cut], post[cut:]
        blocks = post.split("\n\n")
        lead = blocks[1] if i > 1 and len(blocks) > 1 else blocks[0]
        first = sentences(lead)[0] if sentences(lead) else lead

        # R1 — the fold has to carry something checkable.
        # Strip the [N/9] label first: it supplies a digit and made this vacuous.
        if not re.search(r"\d", re.sub(r"^\[\d+/\d+\]", "", visible)):
            # advisory: R1 also accepts a falsifiable claim, which no script can judge.
            bad.append("R1? no NUMBER above the fold — check it carries a falsifiable claim instead")

        # R2 — a link above the fold competes with 'Show more' (post 9 is the CTA, exempt)
        if i != N and URL_RE.search(visible):
            bad.append(f"R2 link above the fold: {URL_RE.search(visible).group()}")
        if i == N and URL_RE.search(hidden):
            bad.append("R2? the CTA post's links fall below the fold (advisory — completeness outranks the character budget)")

        # R3 — first sentence names the subject
        if BAD_OPENERS.match(lead):
            bad.append(f"R3 opens on a bare demonstrative/negation: {lead[:44]!r}")
        # …and no SENTENCE may open on one either (post 1's `They re-host…` slipped past
        # a paragraph-only check).
        for s_ in sentences(post):
            if BAD_OPENERS.match(s_) and not BAD_OPENERS.match(lead):
                bad.append(f"R3 sentence opens on a bare pointer: {s_[:44]!r}")

        # R4 — survives being quoted alone
        at = post.find("CUA-Lite")
        if at < 0:
            bad.append("R4 'CUA-Lite' never appears")
        elif weight(post[:at]) > FOLD:
            bad.append(f"R4 'CUA-Lite' only appears below the fold (char {at})")
        if re.search(r"\bGap \d", post):
            bad.append("R4 'Gap N' label — meaningless to a reader who skipped post 2")

        # R7 — a referent must sit in the same paragraph as the word pointing at it
        for b in blocks[1:]:
            if BAD_OPENERS.match(b) and b is not lead:
                bad.append(f"R7 paragraph opens on a pronoun: {b[:44]!r}")

        # NOUN-DROP — the single most repeated defect on this file: compressing by deleting
        # the noun and leaving a quantifier or demonstrative behind. The sentence stays
        # grammatical, so it survives the author's own read; it stops being comprehensible.
        # Caught so far: That base · of ours · these · Each · many · Four so far · the same loop.
        for m in re.finditer(
            r"\b(each|many|three|four|five|several|both|these|those|all (?:three|four))\b(?!:)"
            r"(?!\s+(?:[a-z]+ ){0,2}(?:" + NOUN + r"|of the|of them))",
            post, re.I):
            # ANAPHORIC numeral: `three things: A, B, C. … all three` names its referent in
            # the preceding sentence. Only a numeral whose noun appears NOWHERE is a drop.
            if re.search(rf"\b{m.group(1)}\s+[a-z]+", post[:m.start()], re.I):
                continue
            nxt = post[m.end():m.end() + 24].strip()
            if not re.match(r"[a-z]+", nxt) or re.match(r"(so far|today|,|\.)", nxt):
                bad.append(f"NOUN-DROP {m.group()!r} with no noun after it: …{post[m.start():m.end()+22]}…")

        # ORPHAN-SAME — `the same X` / `that X` whose X was never named EARLIER in the post.
        # Three of these shipped in one session, and none was authored broken: each was a
        # sentence that STAYED correct while the paragraph giving it an antecedent was
        # deleted or rewritten. The author caught all three; the script caught none.
        for m in re.finditer(r"\b(?:the same|that same|those same|the original)\s+([a-z]+)", post, re.I):
            head, before = m.group(1).lower(), post[:m.start()].lower()
            # DISTRIBUTIVE `same`: "every project rebuilds the same plumbing" means same
            # ACROSS instances, not same as something named earlier — a different grammar,
            # and the site's own wording. Only anaphoric `same` needs an antecedent.
            clause = post[max(0, m.start() - 90):m.start()].lower()
            if re.search(r"\b(every|each|all|both|any)\b", clause):
                continue
            # EXPLICIT COMPARATOR: `the same desktop OSWorld ships`, `the same task the same
            # way in the container as in the VM` — what is being matched is named in the same
            # sentence, so `same` is comparative, not anaphoric.
            if re.search(r"\b(as in|as the|as it|ships|provides|runs|than)\b",
                         post[m.end():m.end() + 140].lower()):
                continue
            if head.rstrip("s") not in before and head not in before:
                bad.append(f"ORPHAN-SAME {m.group()!r} — {head!r} is never named earlier in this post")

        # FRAGMENT — the site writes in appositive fragments; a tweet needs full sentences.
        # `…family of sandboxes, 30k+ verifiable tasks so far.` has no verb after the comma.
        for m in re.finditer(r",\s*(\d[\dk+.,]*\+?\s+[a-z][a-z ]{3,40}?)(?:\s+so far)?\.", post, re.I):
            if not re.search(r"\b(is|are|was|were|has|have|carr\w+|hold\w+|run\w+|ship\w+|serv\w+|span\w+)\b", m.group(1)):
                bad.append(f"FRAGMENT dangling appositive, no verb: '…{m.group(0).strip()}'")

        # R6① — nothing repeated inside a single fold (the most expensive real estate).
        # The project name is exempt: rule 4 REQUIRES it above the fold. Heading words are
        # exempt too — a heading echoing its body is a separate, much cheaper problem.
        # Same pattern as the body words below. Using [a-z]{4,} here missed dotted names:
        # a heading saying `Lite.OSWorld` did not exempt `lite.osworld` in the body, so the
        # post got flagged for repeating its own subject.
        head = set(re.findall(r"[a-z][\w.+-]{4,}", blocks[0].lower()))
        exempt = head | {"cua-lite", "lite", "cua"}
        words = [w_ for w_ in re.findall(r"[a-z][\w.+-]{4,}", visible.lower()) if w_ not in exempt]
        for w_ in sorted({x for x in words if words.count(x) > 1}):
            bad.append(f"R6 {w_!r} twice inside the fold")

        # fold hygiene — a cut inside a word, URL or flag reads as a typo
        if cut < len(post) and post[cut - 1 : cut].strip() and post[cut : cut + 1].strip():
            bad.append(f"fold? cuts mid-token (advisory): …{post[max(0,cut-14):cut]}|{post[cut:cut+10]}…")

        # R8 — never trade substance for the character budget (advisory)
        if weight(post) > FOLD and len(hidden.split()) < 6:
            bad.append("R8? folds to hide only a few words (advisory — character count is the WEAKEST constraint; never cut substance for it)")

        fails[f"post {i}"] = bad
        opener_shapes.setdefault(" ".join(first.split()[:3]).lower(), []).append(i)
        for s_ in sentences(post):
            toks = re.findall(r"[a-z]{4,}", s_.lower())
            if len(toks) >= 5:
                # shingle on content words so a reordered clause still collides
                sentence_index.setdefault(" ".join(sorted(set(toks))), []).append(i)

    # R10 — the nine openings must not share a template
    for shape, where in opener_shapes.items():
        if len(where) > 1:
            fails.setdefault("thread", []).append(f"R10 posts {where} open identically: {shape!r}")
    # R6 — no sentence near-verbatim in two posts
    for s_, where in sentence_index.items():
        if len(set(where)) > 1:
            fails.setdefault("thread", []).append(
                f"R6 posts {sorted(set(where))} share a sentence (same content words): {s_[:60]!r}")

    return fails


def stale_notes() -> list[str]:
    """Notes that cite a sentence the copy no longer contains.

    Four of fifteen defects in one review round were this: a **Why here** quoting
    `The benchmark itself is untouched` after that sentence was rewritten, a **Bold** naming
    a phrase that had been reworded. They ship because editing the copy and editing the note
    that cites it are two actions, and the second gets skipped. A machine holds both.

    Only **Bold** and **Why here** are checked — a **Source** field quotes the BLOG by
    design, so its quotations are not expected to appear in our own copy.
    """
    thread = README.read_text()
    thread = thread[thread.index("## The thread"):]
    joined = "\n".join(posts())
    out = []
    for note, line in re.findall(r"\*\*(Bold|Why here)\*\*([^\n]+)", thread):
        # A Why here may cite thread 01 as precedent — those quotations belong to that
        # thread's copy, not ours, and are supposed to be absent here.
        if "01" in line or "thread 1" in line.lower():
            continue
        for ph in re.findall(r"`([^`]+)`", line):
            if re.search(r"\.(md|py|html|json|js|ya?ml)(:\d+)?$", ph) or ph.startswith("assets/"):
                continue                       # a path or a file:line, not a quotation
            if len(ph) > 12 and ph not in joined:
                out.append(f"STALE-NOTE **{note}** cites text in no post: {ph!r}")
    return out


def main() -> int:
    result = audit()
    if stale_notes():
        result.setdefault("notes", []).extend(stale_notes())
    if "--baseline" in sys.argv:
        BASELINE.write_text(json.dumps(result, indent=1, ensure_ascii=False))
        print(f"baseline saved: {sum(len(v) for v in result.values())} open findings")
        return 0

    old = json.loads(BASELINE.read_text()) if ("--diff" in sys.argv and BASELINE.exists()) else None
    total = 0
    for key in sorted(result, key=lambda k: (k == "thread", k)):
        for line in result[key]:
            total += 1
            regressed = old is not None and line not in old.get(key, [])
            print(f"{'NEW  ' if regressed else '     '}{key}: {line}")
    if old is not None:
        for key, lines in old.items():
            for line in lines:
                if line not in result.get(key, []):
                    print(f"FIXED {key}: {line}")
    print(f"\n{total} finding(s) across {len(posts())} posts.")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
