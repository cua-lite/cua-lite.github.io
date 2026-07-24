#!/usr/bin/env python3
"""
Strict environment-cost analysis for OSWorld (KVM VM) vs Lite.OSWorld (container),
computed from the REAL leaderboard eval rollouts — not a small synthetic micro-bench.

Every turn of every rollout writes `turn_*/06_timing.json`:
    { "predict": <model inference seconds>, "act": <env action+screenshot seconds>,
      "observe": <optional agent-side observe seconds> }
`predict` is the model's cost (environment-agnostic); `act` is the environment's cost
per step: dispatch the action into the desktop, wait the (shared) settle delay, then
capture + return the screenshot. `act` is therefore the honest per-step environment
latency we want to compare between the KVM VM and the KVM-free container.

Why this is stricter than the old micro-bench:
  * N is ~66k turns / env (13 agents x ~321-325 tasks), not 50 synthetic steps.
  * It is the SAME action distribution the leaderboard actually ran.
  * It is PAIRED: the same (agent, task) is compared across both envs, so the
    per-step delta isolates the environment, not the agent or the task mix.

What this script deliberately does NOT claim: idle RAM, image size on disk, cold-boot
time, and max-density/throughput-at-scale are host-level facts that require live
`docker stats` on the benchmarking host and are reported separately in RESULTS.md
(source noted there); they are not derivable from rollout timing and are not invented
here.

Usage:
    python analyze_timing.py [--osworld DIR] [--lite DIR] [--out results.json]
Defaults point at the two runs backing the leaderboard on this page.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import statistics as st
from collections import defaultdict

# Runs that back the leaderboard JSONs on the blog page.
DEFAULT_OSWORLD = "/home/haoranliu/cua-lite-all-agents/.exps/eval/osworld/2026-07-18T17-00_65ea6496ef/run_0"
DEFAULT_LITE = "/home/haoranliu/cua-lite-all-agents/.exps/eval/lite.osworld/2026-07-18T14-23_0cde57702f/run_0"


def task_hash(env: str, task_dir_name: str) -> str:
    """Reduce a per-env task directory name to the shared 8-char OSWorld hash.

    osworld:  'e0df059f-28a6-4169-...'          -> 'e0df059f'
    lite:     'osworld_libreoffice_calc_6e99a1ad' -> '6e99a1ad'
              'osworld_os_e0df059f'               -> 'e0df059f'
    """
    if env == "osworld":
        return task_dir_name.split("-", 1)[0][:8]
    return task_dir_name.rsplit("_", 1)[-1][:8]


def model_dirs(run_dir: str):
    for name in sorted(os.listdir(run_dir)):
        p = os.path.join(run_dir, name, "eval")
        if os.path.isdir(p):
            yield name, p


def collect(run_dir: str, env: str):
    """Return per-turn records and per-(model,hash) rollout records for one env."""
    turns = []          # dict(model, hash, i, act, predict, observe)
    rollouts = {}       # (model, hash) -> dict(act_total, predict_total, n_turns, ret)
    for model, eval_dir in model_dirs(run_dir):
        for task_name in sorted(os.listdir(eval_dir)):
            sdir = os.path.join(eval_dir, task_name, "sample_00")
            if not os.path.isdir(sdir):
                continue
            h = task_hash(env, task_name)
            a_tot = p_tot = 0.0
            nt = 0
            for tj in sorted(glob.glob(os.path.join(sdir, "turn_*", "06_timing.json"))):
                try:
                    t = json.load(open(tj))
                except Exception:
                    continue
                act = t.get("act")
                pred = t.get("predict")
                if act is None or act < 0:
                    continue
                turns.append({"model": model, "hash": h, "act": float(act),
                              "predict": float(pred) if pred is not None else None,
                              "observe": t.get("observe")})
                a_tot += float(act)
                if pred is not None:
                    p_tot += float(pred)
                nt += 1
            if nt:
                ret = None
                try:
                    ret = json.load(open(os.path.join(sdir, "summary.json"))).get("episode_return")
                except Exception:
                    pass
                rollouts[(model, h)] = {"act_total": a_tot, "predict_total": p_tot,
                                        "n_turns": nt, "episode_return": ret}
    return turns, rollouts


def q(xs, p):
    if not xs:
        return None
    xs = sorted(xs)
    if len(xs) == 1:
        return xs[0]
    idx = p * (len(xs) - 1)
    lo = int(idx)
    frac = idx - lo
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] * (1 - frac) + xs[hi] * frac


def describe(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None
    return {
        "n": len(xs),
        "mean": round(st.mean(xs), 4),
        "median": round(st.median(xs), 4),
        "p10": round(q(xs, 0.10), 4),
        "p90": round(q(xs, 0.90), 4),
        "std": round(st.pstdev(xs), 4) if len(xs) > 1 else 0.0,
        "total": round(sum(xs), 2),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--osworld", default=DEFAULT_OSWORLD)
    ap.add_argument("--lite", default=DEFAULT_LITE)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "results.json"))
    args = ap.parse_args()

    envs = {}
    raw = {}
    for env, run in [("osworld", args.osworld), ("lite.osworld", args.lite)]:
        turns, rollouts = collect(run, env)
        raw[env] = (turns, rollouts)
        acts = [t["act"] for t in turns]
        preds = [t["predict"] for t in turns if t["predict"] is not None]
        # env share of a turn = act / (act + predict), per turn where both known
        shares = [t["act"] / (t["act"] + t["predict"])
                  for t in turns if t["predict"] is not None and (t["act"] + t["predict"]) > 0]
        per_model = {}
        by_model = defaultdict(list)
        for t in turns:
            by_model[t["model"]].append(t["act"])
        for m, xs in by_model.items():
            per_model[m] = round(st.median(xs), 3)
        envs[env] = {
            "run_dir": run,
            "n_rollouts": len(rollouts),
            "n_turns": len(turns),
            "per_turn_act_s": describe(acts),
            "per_turn_predict_s": describe(preds),
            "env_share_of_turn": round(st.median(shares), 4) if shares else None,
            "per_task_act_total_s": describe([r["act_total"] for r in rollouts.values()]),
            "per_model_median_act_s": per_model,
        }

    # ---- PAIRED comparison: same (model, task hash) in both envs ----
    o_roll = raw["osworld"][1]
    l_roll = raw["lite.osworld"][1]
    common = sorted(set(o_roll) & set(l_roll))
    ratios, deltas = [], []
    o_pt, l_pt = [], []   # per-turn mean act within each rollout
    for key in common:
        o, l = o_roll[key], l_roll[key]
        o_mean = o["act_total"] / o["n_turns"]
        l_mean = l["act_total"] / l["n_turns"]
        o_pt.append(o_mean)
        l_pt.append(l_mean)
        if o_mean > 0:
            ratios.append(l_mean / o_mean)
        deltas.append(l_mean - o_mean)
    paired = {
        "n_pairs": len(common),
        "osworld_per_turn_act_s": describe(o_pt),
        "lite_per_turn_act_s": describe(l_pt),
        "lite_over_osworld_ratio": {
            "median": round(st.median(ratios), 3) if ratios else None,
            "mean": round(st.mean(ratios), 3) if ratios else None,
        },
        "lite_minus_osworld_s": {
            "median": round(st.median(deltas), 3) if deltas else None,
            "mean": round(st.mean(deltas), 3) if deltas else None,
        },
    }

    out = {
        "meta": {
            "what": "Per-turn environment cost (act = action dispatch + settle + screenshot) "
                    "and model cost (predict) from the real leaderboard eval rollouts.",
            "osworld_run": args.osworld,
            "lite_run": args.lite,
        },
        "envs": envs,
        "paired_same_model_same_task": paired,
    }
    json.dump(out, open(args.out, "w"), indent=2)

    # ---- console summary ----
    def line(k, v):
        print(f"  {k:34} {v}")
    for env in ("lite.osworld", "osworld"):
        e = envs[env]
        print(f"\n== {env} ==  ({e['n_rollouts']} rollouts, {e['n_turns']} turns)")
        a = e["per_turn_act_s"]
        line("per-turn ENV act (s)", f"median {a['median']}  mean {a['mean']}  p10 {a['p10']}  p90 {a['p90']}")
        p = e["per_turn_predict_s"]
        line("per-turn MODEL predict (s)", f"median {p['median']}  mean {p['mean']}")
        line("env share of a turn (median)", e["env_share_of_turn"])
        line("per-task ENV act total (s)", f"median {e['per_task_act_total_s']['median']}  mean {e['per_task_act_total_s']['mean']}")
    print(f"\n== PAIRED (same model + same task, {paired['n_pairs']} pairs) ==")
    line("OSWorld per-turn act (median)", paired["osworld_per_turn_act_s"]["median"])
    line("Lite per-turn act (median)", paired["lite_per_turn_act_s"]["median"])
    line("Lite / OSWorld ratio (median)", paired["lite_over_osworld_ratio"]["median"])
    line("Lite - OSWorld (median, s)", paired["lite_minus_osworld_s"]["median"])
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
