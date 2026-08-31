#!/usr/bin/env python3
"""Gate every rule in README.md's 写作规约 at once, over every post in the thread.

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


def _blocks() -> list[tuple[str, str]]:
    body = README.read_text()
    thread = body[body.index("## The thread"):]
    return re.findall(r"### ([^\n]+)\n\n```\n(.*?)\n```", thread, re.S)


def posts() -> list[str]:
    return [b for _, b in _blocks()]


def titles() -> list[str]:
    """Headings, so rules can key on WHAT a post is rather than on its number.

    Every hard-coded post index in this file went stale the moment the thread was
    reordered — and one of them (`if i != 9`, the CTA's link exemption) started
    reporting the CTA's intended links as a hard failure. Match the heading instead.
    """
    return [t for t, _ in _blocks()]


def sentences(paragraph: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", paragraph) if s.strip()]


def stale_notes() -> list[str]:
    """Notes that cite a sentence the copy no longer contains.

    Ported from thread 02's checker, which had it and 01 did not — even though 01's own
    README claimed the check existed for both. That gap shipped three wrong **Bold** fields
    in this file: one dropped "verifiable"/"light-weight"/"SFT" and swapped "framework" for
    "interface"; one dropped "exact"; one invented a "one" the post never had. They survive
    because editing the copy and editing the note that cites it are two actions, and the
    second gets skipped. A machine holds both.

    Only **Bold** and **Why here** are checked — a **Source** field quotes the BLOG or another
    thread by design, so its quotations are not expected to appear in our own copy.
    """
    thread = README.read_text()
    thread = thread[thread.index("## The thread"):]
    joined = "\n".join(posts())
    out = []
    for note, line in re.findall(r"\*\*(Bold|Why here)\*\*([^\n]+)", thread):
        # a note may cite thread 02 or the blog as precedent — that copy is not ours
        if "02" in line or "thread 2" in line.lower() or "blog/" in line:
            continue
        for ph in re.findall(r"`([^`]+)`", line):
            if re.search(r"\.(md|py|html|json|js|ya?ml)(:\d+)?$", ph) or ph.startswith("assets/"):
                continue                       # a path or a file:line, not a quotation
            if len(ph) > 12 and ph not in joined:
                out.append(f"STALE-NOTE **{note}** cites text in no post: {ph!r}")
    return out


# A rule may legitimately quote copy that is NOT in the thread — when it is telling you
# what NOT to write, or naming something already deleted. These markers say so.
NEGATED = re.compile(
    r"别|不要|不许|不用|不写|不能|不在|避免|曾|旧|删|去掉|一度|反而|等于|就是为同一|"
    r"写成|改成|原句|站点|博客|README|抽取|已不|不成立|不采纳|错|假"
)


def stale_rules() -> list[str]:
    """A rule that quotes a sentence the copy no longer contains is worse than no rule.

    `stale_notes()` guards the per-post **Bold**/**Why here** fields. This guards the other
    two thirds of the file — 写作规约, 其余约定, Pre-flight, 写作决定 — which is where the rot
    actually accumulates, because those rules are written once and then outlive the copy they
    were written about. After one round of edits this check found three rules quoting sentences
    that had been deleted in the SAME session, plus four rules governing a `▪️` list that no
    post had contained for days.

    Lines that negate ("never write X", "the old wording was Y") are exempt — quoting absent
    copy is the whole point there.
    """
    md = README.read_text()
    rules = md[: md.index("## The thread")]
    joined = " ".join(posts())
    # A rule wraps across lines, so a backtick pair can straddle a newline — matching per
    # physical line both misses quotes and mis-pairs the ones it finds. Group into bullets.
    lines = rules.split("\n")
    bullets: list[tuple[int, str]] = []
    for n, line in enumerate(lines, 1):
        starts = line.startswith(("- ", "  - ", "#", "|", "**", "1.", "2.", "3.", "4.", "5.")) or not line.strip()
        if starts or not bullets:
            bullets.append((n, line))
        else:
            ln, prev = bullets[-1]
            bullets[-1] = (ln, prev + " " + line.strip())
    out = []
    for n, block in bullets:
        if NEGATED.search(block):
            continue
        for q in re.findall(r"`([^`]+)`", block):
            if len(q.split()) < 5 or "…" in q:
                continue
            if any(c in q for c in "/(){}=<>#*|"):
                continue
            if q not in joined:
                out.append(f"STALE-RULE :{n} quotes copy no post contains: {q[:70]!r}")
    return out


def ack_attribution() -> list[str]:
    """Every @ in the acknowledgements must be on a project the evidence table says it belongs to.

    Why this exists: the costliest error class in this file is not a typo, it is crediting the
    right-looking account for the WRONG work — it notifies a stranger and misattributes someone's
    paper in public. It has happened three times: Fara to `@MicrosoftAI` (Microsoft's consumer org,
    not Microsoft Research), AndroidWorld to `@GoogleResearch` (the project page says DeepMind), and
    gym-anything's first author copy-pasted onto XLANG's CUA-Gym while editing the neighbouring
    clause. All three read fine; none is catchable by eye in a 48-handle paragraph.

    The evidence table under the post is already keyed by project (`@GoogleDeepMind` has one row for
    Gemini and another for AndroidWorld). So the check is: parse `Project (@a, @b)` out of the post,
    and require that at least one table row for each handle names that project. A handle with no row
    at all is also a finding — it means it shipped without being looked up.
    """
    md = README.read_text()
    ack = [b for t, b in _blocks() if "cknowledg" in t]
    if not ack:
        return []
    rows: dict[str, list[str]] = {}
    for h, desc in re.findall(r"^\|\s*`(@[A-Za-z0-9_]+)`\s*\|([^|]*)\|", md, re.M):
        rows.setdefault(h, []).append(desc)
    if not rows:
        return []
    flat = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
    # "…@Org's Project (@a, @b)" / "and Project (@a)" / "with Project (@a)"
    pat = re.compile(
        r"(?:^|[\s,;])(?:and |with |all run through |our )?(?:@[A-Za-z0-9_]+'s )?"
        r"([A-Za-z0-9][A-Za-z0-9.\-]*)\s+\((@[A-Za-z0-9_]+(?:,\s*@[A-Za-z0-9_]+)*)\)"
    )
    out = []
    for m in pat.finditer(ack[0]):
        proj = m.group(1)
        for h in re.findall(r"@[A-Za-z0-9_]+", m.group(2)):
            if h not in rows:
                out.append(f"ACK {h} is credited on {proj} but has no row in the evidence table")
            elif not any(flat(proj) in flat(d) for d in rows[h]):
                claim = " / ".join(d.strip()[:48] for d in rows[h])
                out.append(f"ACK {h} is credited on {proj}, but the evidence table says: {claim}")
    return out


def audit() -> dict[str, list[str]]:
    ps = posts()
    ts = titles()
    fails: dict[str, list[str]] = {}
    opener_shapes: dict[str, list[int]] = {}
    sentence_index: dict[str, list[int]] = {}

    for i, post in enumerate(ps, 1):
        bad: list[str] = []
        is_cta = "call for contributors" in ts[i - 1].lower()
        cut = fold_cut(post)
        visible, hidden = post[:cut], post[cut:]
        blocks = post.split("\n\n")
        lead = blocks[1] if i > 1 and len(blocks) > 1 else blocks[0]
        first = sentences(lead)[0] if sentences(lead) else lead

        # R1 — the fold has to carry something checkable.
        # Strip the [N/10] label first: it supplies a digit and made this vacuous.
        if not re.search(r"\d", re.sub(r"^\[\d+/\d+\]", "", visible)):
            # advisory: R1 also accepts a falsifiable claim, which no script can judge.
            bad.append("R1? no NUMBER above the fold — check it carries a falsifiable claim instead")

        # R2 — a link above the fold competes with 'Show more' (the CTA post is exempt)
        if not is_cta and URL_RE.search(visible):
            bad.append(f"R2 link above the fold: {URL_RE.search(visible).group()}")
        if is_cta and URL_RE.search(hidden):
            bad.append("R2? the CTA's links fall below the fold (advisory — completeness outranks the character budget)")

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
            bad.append("R4 'Gap N' label — meaningless to a reader who skipped the gap post")

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
            # DISTRIBUTIVE `same`: "every project rebuilds the same tooling" means same
            # ACROSS instances, not same as something named earlier — a different grammar,
            # and the site's own wording. Only anaphoric `same` needs an antecedent.
            clause = post[max(0, m.start() - 90):m.start()].lower()
            if re.search(r"\b(every|each|all|both|any)\b", clause):
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
        head = set(re.findall(r"[a-z]{4,}", blocks[0].lower()))
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

    notes = stale_notes()
    if notes:
        fails.setdefault("notes", []).extend(notes)

    ack = ack_attribution()
    if ack:
        fails.setdefault("ack", []).extend(ack)

    stale = stale_rules()
    if stale:
        fails.setdefault("notes", []).extend(stale)

    return fails


def main() -> int:
    result = audit()
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
