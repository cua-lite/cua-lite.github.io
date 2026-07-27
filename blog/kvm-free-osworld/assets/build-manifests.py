#!/usr/bin/env python3
"""Regenerate assets/rollouts.json from the raw rollout folders.

Run from this directory (blog/kvm-free-osworld/assets) after adding or replacing clips:

    python3 build-manifests.py

It walks the two asset trees and emits one manifest the page fetches at load:

  osworld/<task>/{os,liteos}/     -> "hh"   (the side-by-side parity section)
  beyond_os/<family>/<task>/      -> "belt" (the scrolling training-env belt)

Each entry carries the task instruction, the trajectory clip, and one row per turn
(a short action label + the time in the clip where that turn is on screen, so the page
can seek to it). Media paths are relative to index.html so the page uses them verbatim.

Needs ffmpeg/ffprobe, numpy and Pillow for the turn->timestamp alignment.
"""

import json
import glob
import os
import re
import subprocess
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.dirname(HERE)          # media paths are written relative to index.html
OUT = os.path.join(HERE, "rollouts.json")

# ---------------------------------------------------------------- instructions

def _instruction_from_json(raw):
    """beyond_os: 01_prompt.txt is a JSON message list."""
    for msg in json.loads(raw):
        if msg.get("role") != "user":
            continue
        content = msg.get("content")
        if isinstance(content, str):
            return content.strip()
        for c in content or []:
            if c.get("type") == "input_text":
                return (c.get("text") or "").strip()
    return None


def _instruction_from_chat(raw):
    """osworld: 01_prompt.txt is a rendered chat template with an `Instruction:` line."""
    m = re.search(r"^Instruction:\s*(.+?)(?:\n\s*Previous actions:|\n\s*\n|\Z)", raw, re.S | re.M)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else None


def get_instruction(sample_dir):
    p = os.path.join(sample_dir, "turn_00", "01_prompt.txt")
    if not os.path.isfile(p):
        return None
    raw = open(p, encoding="utf-8", errors="replace").read()
    try:
        return _instruction_from_json(raw)
    except (ValueError, TypeError):
        return _instruction_from_chat(raw)

# ---------------------------------------------------------------- action labels

TEXT_LIMIT = 52   # keep typed strings readable in the narrow action column


def _lit(v):
    """A Python-looking literal (JSON's string escaping matches Python's closely enough)."""
    return json.dumps(v, ensure_ascii=False)


def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return _lit(v)
    return str(int(f)) if f == int(f) else str(f)


def _xy(coord):
    return [str(int(round(float(c)))) for c in (coord or [])[:2]]


def _text(s):
    s = " ".join(str(s or "").split())
    return _lit(s if len(s) <= TEXT_LIMIT else s[:TEXT_LIMIT - 1] + "…")


def format_call(tc):
    """Render one lite (litedesktop) tool call as its Python call, e.g. click(47, 951)."""
    fn = tc.get("function") or {}
    name, a = fn.get("name"), fn.get("arguments") or {}
    pos, kw = [], []
    if name in ("click", "mouse_move"):
        pos = _xy(a.get("coordinate"))
        if a.get("button") and a["button"] != "left":
            kw.append(f'button={_lit(a["button"])}')
        if a.get("clicks") and a["clicks"] != 1:
            kw.append(f'clicks={int(a["clicks"])}')
    elif name == "drag":
        pos = _xy(a.get("start_coordinate")) + _xy(a.get("coordinate"))
    elif name == "scroll":
        pos = _xy(a.get("coordinate"))
        if a.get("direction"):
            kw.append(f'direction={_lit(a["direction"])}')
        if a.get("amount") is not None:
            kw.append(f"amount={_num(a['amount'])}")
    elif name == "key":
        pos = [_lit(k) for k in (a.get("keys") or [])]
    elif name in ("type", "response"):
        pos = [_text(a.get("text"))]
    elif name == "wait":
        pos = [_num(a.get("duration"))]
    elif name == "screenshot":
        pass
    else:                                        # terminate(status=...) and anything new
        kw = [f"{k}={_lit(v)}" for k, v in sorted(a.items())]
    return f"{name}({', '.join(pos + kw)})"


def action_label(actions):
    """The turn's calls in the lite action space, one per line."""
    msg = actions.get("lite_message") or actions.get("agent_message") or {}
    calls = msg.get("tool_calls") or []
    return "\n".join(format_call(c) for c in calls) or None


# ------------------------------------------------------- turn -> clip timestamp

STAY_PENALTY = 1e-3   # on a tie, advance a frame rather than sit on the same one
WEAK_MATCH = 0.9      # below this, the turn's screen isn't really in the clip
STATS = {"weak": 0, "clips": 0, "turns": 0}


def _frame_times(video):
    """Real presentation timestamps — don't assume a constant frame rate."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "frame=best_effort_timestamp_time", "-of", "csv=p=0", video],
        capture_output=True, text=True).stdout.split()
    return [float(x) for x in out if x and x[0].isdigit()]


def _descriptors(paths):
    """Mean-centred, L2-normalised 32x32 greyscale thumbnails — cosine sim compares them."""
    rows = []
    for p in paths:
        a = np.asarray(Image.open(p).convert("L").resize((32, 32), Image.BILINEAR),
                       dtype=np.float32).ravel()
        a -= a.mean()
        norm = np.linalg.norm(a)
        rows.append(a / norm if norm else a)
    return np.array(rows)


def align_times(video, shots):
    """Map each turn screenshot to the clip time showing it.

    The clips are slideshows of these very screenshots, but the frame count doesn't
    match the turn count reliably (identical consecutive states sometimes collapse into
    one frame). So align by image similarity under a monotonic constraint: turn i's frame
    is never earlier than turn i-1's. Falls back to spreading turns evenly if the video
    can't be decoded.
    """
    n = len(shots)
    try:
        times = _frame_times(video)
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", "scale=64:64",
                            os.path.join(tmp, "f_%04d.png")], check=True)
            frames = _descriptors(sorted(glob.glob(os.path.join(tmp, "f_*.png"))))
        if not len(frames) or not times:
            raise RuntimeError("no frames decoded")
        times = times[:len(frames)]

        sim = _descriptors(shots) @ frames.T
        m = sim.shape[1]
        best = np.full((n, m), -np.inf)
        back = np.zeros((n, m), dtype=int)
        best[0] = sim[0]
        for i in range(1, n):
            run_max, run_arg = -np.inf, 0          # best over frames strictly left of j
            for j in range(m):
                stay = best[i - 1, j] - STAY_PENALTY
                if run_max > stay:
                    best[i, j], back[i, j] = sim[i, j] + run_max, run_arg
                else:
                    best[i, j], back[i, j] = sim[i, j] + stay, j
                if best[i - 1, j] > run_max:
                    run_max, run_arg = best[i - 1, j], j
        path = [int(np.argmax(best[n - 1]))]
        for i in range(n - 1, 0, -1):
            path.append(int(back[i, path[-1]]))
        path = list(reversed(path))
        return [times[j] for j in path], [float(sim[i, j]) for i, j in enumerate(path)]
    except Exception as exc:                        # noqa: BLE001 - degrade, don't fail the build
        print(f"  ! {video}: alignment failed ({exc}); spacing turns evenly")
        span = _frame_times(video)
        end = span[-1] if span else max(n - 1, 1)
        return [end * i / max(n - 1, 1) for i in range(n)], [0.0] * n


def get_turns(sample_dir, video):
    """Every turn's action label, paired with the time in the clip where that turn is on screen."""
    dirs = sorted(glob.glob(os.path.join(sample_dir, "turn_*")),
                  key=lambda p: int(re.search(r"turn_(\d+)", p).group(1)))
    rows = []
    for td in dirs:
        shot, act = os.path.join(td, "00_screenshot.png"), os.path.join(td, "03_actions.json")
        if not os.path.isfile(shot):
            continue
        try:
            label = action_label(json.load(open(act))) if os.path.isfile(act) else None
        except ValueError:
            label = None
        rows.append((shot, label))
    if not rows:
        return []

    times, sims = align_times(video, [shot for shot, _ in rows])
    # a turn whose screen never appears in the clip (some clips start a turn late) can only be
    # pinned to the closest frame — count those so the build reports them rather than hiding them
    weak = sum(1 for (_, label), s in zip(rows, sims) if label and s < WEAK_MATCH)
    if weak:
        STATS["weak"] += weak
        STATS["clips"] += 1
    # only ship turns that actually did something; their timestamps come from the full alignment
    return [{"action": label, "t": round(t, 2)}
            for (_, label), t in zip(rows, times) if label]


def build_clip(sample_dir, domain, rel_to):
    video = os.path.join(sample_dir, "trajectory.mp4")
    if not os.path.isfile(video):
        return None
    instruction, turns = get_instruction(sample_dir), get_turns(sample_dir, video)
    if not instruction or not turns:
        return None
    return {"domain": domain, "instruction": instruction,
            "video": os.path.relpath(video, rel_to), "turns": turns}

# ---------------------------------------------------------------- domain naming

DOMAIN_KEYWORDS = [
    ("vscode", [r"vscode", r"vs code", r"pylance", r"pyright", r"\bmypy\b", r"\btypescript\b", r"\beslint\b"]),
    ("calc", [r"spreadsheet", r"\bsheet\b", r"\bexcel\b", r"\bcell\b", r"\bcsv\b", r"\btable\b", r"\bcolumn\b", r"\brow\b"]),
    ("impress", [r"presentation", r"\bslide\b", r"powerpoint", r"speaker note"]),
    ("gimp", [r"\bgimp\b", r"image editor", r"\bphoto\b", r"\bpng\b", r"\bjpe?g\b"]),
    ("vlc", [r"\bvlc\b", r"video player", r"media player", r"\bplaylist\b"]),
    ("chrome", [r"\bbrowser\b", r"\bchrome\b", r"\bwebsite\b", r"\bwebpage\b", r"web page", r"\burl\b", r"\bfirefox\b"]),
    ("writer", [r"\bdocument\b", r"\bdocx\b", r"\bparagraph\b", r"\bcontract\b", r"\breport\b", r"\bresume\b"]),
    ("files", [r"file manager", r"\bterminal\b", r"\bfolder\b", r"\bdirectory\b", r"\bnautilus\b"]),
]


def domain_from_text(instruction):
    text = (instruction or "").lower()
    for domain, patterns in DOMAIN_KEYWORDS:
        if any(re.search(p, text) for p in patterns):
            return domain
    return "desktop"


DOMAIN_ALIASES = {"vs_code": "vscode", "libreoffice_calc": "calc", "libreoffice_impress": "impress",
                  "libreoffice_writer": "writer", "multi_apps": "multi-app", "os": "files"}


def domain_from_name(name):
    """Task folders embed their app category before the task id, e.g.

        osworld_libreoffice_calc_0326d92d                      -> calc
        scalecua_osworld_rl_thunderbird_030eeff7_b492_..._0    -> thunderbird
    """
    base = re.sub(r"^(scalecua_)?osworld(_rl)?_", "", name)     # drop the harness prefix
    m = re.match(r"(.+?)_[0-9a-f]{8}(?![0-9a-f])", base)        # category runs up to the task id
    base = m.group(1) if m else base
    return DOMAIN_ALIASES.get(base, base)


def domain_from_env(task_dir):
    try:
        env = json.load(open(os.path.join(task_dir, "summary.json"))).get("env_id", "")
    except (OSError, ValueError):
        return "desktop"
    return env.split(".")[-1] if env else "desktop"

# ---------------------------------------------------------------- section: hh

SIDES = [("os", "OSWorld"), ("liteos", "Lite.OSWorld")]


def build_hh():
    root = os.path.join(HERE, "osworld")
    out = {}
    for task_dir in sorted(glob.glob(os.path.join(root, "*"))):
        if not os.path.isdir(task_dir):
            continue
        task = os.path.basename(task_dir)
        sides = {}
        for key, label in SIDES:
            clip = build_clip(os.path.join(task_dir, key), f"{task} · {label}", PAGE)
            if clip:
                sides[key] = clip
        if len(sides) == len(SIDES):          # only ship a task when both sides are present
            out[task] = sides
        else:
            print(f"  ! {task}: skipped (sides found: {sorted(sides) or 'none'})")
    return out

# -------------------------------------------------------------- section: belt

FAMILIES = [("Lite.OSWorld", "osworld"), ("Lite.ScaleCUA", "scalecua"),
            ("Lite.CUAGym", "cuagym"), ("Lite.CUAWorld", "cuaworld")]
PER_FAMILY = 8


def _round_robin(by_domain):
    doms = sorted(by_domain)
    idx = {d: 0 for d in doms}
    while any(idx[d] < len(by_domain[d]) for d in doms):
        for d in doms:
            if idx[d] < len(by_domain[d]):
                yield by_domain[d][idx[d]], d
                idx[d] += 1


def _spread(items, n):
    if len(items) <= n:
        return items
    step = len(items) / n
    return [items[int(i * step)] for i in range(n)]


def build_belt():
    root = os.path.join(HERE, "beyond_os")
    out = {}
    for family, folder in FAMILIES:
        dirs = sorted(d for d in glob.glob(os.path.join(root, folder, "*"))
                      if os.path.isfile(os.path.join(d, "sample_00", "trajectory.mp4")))
        by_domain = {}
        for d in dirs:
            if folder in ("osworld", "scalecua"):
                dom = domain_from_name(os.path.basename(d))
            elif folder == "cuaworld":
                dom = domain_from_env(d)
            else:
                dom = domain_from_text(get_instruction(os.path.join(d, "sample_00")))
            by_domain.setdefault(dom, []).append(d)

        # interleave domains when there are several; with only one, spread across the whole set
        order = list(_round_robin(by_domain)) if len(by_domain) > 1 else \
            [(d, dom) for dom, ds in by_domain.items() for d in _spread(ds, PER_FAMILY)]

        clips = []
        for task_dir, dom in order:
            if len(clips) >= PER_FAMILY:
                break
            clip = build_clip(os.path.join(task_dir, "sample_00"), dom, PAGE)
            if clip:
                clips.append(clip)
        out[family] = clips
        print(f"  {family}: {len(clips)} clips {sorted({c['domain'] for c in clips})}")
    return out


if __name__ == "__main__":
    print("hh (parity section):")
    hh = build_hh()
    print(f"  {len(hh)} tasks: {', '.join(sorted(hh))}")
    print("belt (training envs):")
    belt = build_belt()

    manifest = {"hh": hh, "belt": belt}
    with open(OUT, "w") as f:
        json.dump(manifest, f, indent=1)

    media = sum(1 for sec in (hh.values()) for c in sec.values() for _ in [c]) + \
        sum(len(v) for v in belt.values())
    turns = sum(len(c["turns"]) for sec in hh.values() for c in sec.values()) + \
        sum(len(c["turns"]) for v in belt.values() for c in v)
    print(f"\nwrote {os.path.relpath(OUT, HERE)} ({os.path.getsize(OUT) / 1024:.0f} KB, "
          f"{media} clips, {turns} turns)")
    if STATS["weak"]:
        print(f"  note: {STATS['weak']}/{turns} turns across {STATS['clips']} clips have no exact "
              f"frame in their clip (those clips skip a turn); each is pinned to the nearest frame.")
