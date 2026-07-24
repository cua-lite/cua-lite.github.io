#!/usr/bin/env python3
"""
Strict RESOURCE-FOOTPRINT measurement: OSWorld (QEMU/KVM VM-in-Docker) vs
Lite.OSWorld (KVM-free container). Measures what the rollout timing cannot —
boot time and steady-state idle memory / CPU per instance — and captures the
static on-disk footprint (image + VM backing disk).

What makes this STRICTER than the earlier micro-bench:
  * Idle CPU/mem is NOT a single instantaneous `docker stats` snapshot taken the
    instant reset() returns (that samples a still-settling desktop and was the
    source of the earlier noisy CPU number). Here we SETTLE for `--settle` seconds
    of true idle, then take `--samples` spaced `docker stats` samples and report the
    MEDIAN (+ IQR + full series), which is stable and reproducible.
  * Boot is measured over N matched tasks (N>1) so we get a real spread, and each
    container is torn down before the next so numbers are not muddied by concurrency.
  * On-disk footprint records the container image sizes AND the OSWorld VM's
    Ubuntu.qcow2 backing disk (the real disk cost of running the VM), not just the
    image layer.

Runs in-process (direct mode): NO env-server, NO model, NO GPU — pure environment
cost. Must run from the cua-lite repo (imports `lite.gym`):

    cd /home/haoranliu/cua-lite
    unset CUA_LITE_ENV_SERVER_URL CUA_LITE_ENV_SERVER_TOKEN   # force direct mode
    uv run --no-sync python \
      /home/haoranliu/cua-lite.github.io/blog/kvm-free-osworld/benchmarking/measure_footprint.py \
      --env-id both --tasks 5 --settle 25 --samples 8 --gap 2 \
      --out /home/haoranliu/cua-lite.github.io/blog/kvm-free-osworld/benchmarking/footprint.json

    # quick smoke: 1 task, short settle
    uv run --no-sync python measure_footprint.py --env-id lite.osworld --smoke
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import statistics as st
import subprocess
import time
from typing import Any

import lite.gym as gym

# Matched OSWorld tasks (same task in both envs, matched by 8-char hash), spanning
# several apps so the idle desktop content is representative, not one outlier app.
MATCHED_TASKS: list[dict[str, str]] = [
    {"label": "libreoffice_calc", "hash": "7a4e4bc8",
     "osworld": "7a4e4bc8-922c-4c84-865c-25ba34136be1",
     "lite.osworld": "osworld_libreoffice_calc_7a4e4bc8"},
    {"label": "libreoffice_impress", "hash": "841b50aa",
     "osworld": "841b50aa-df53-47bd-a73a-22d3a9f73160",
     "lite.osworld": "osworld_libreoffice_impress_841b50aa"},
    {"label": "vs_code", "hash": "ea98c5d7",
     "osworld": "ea98c5d7-3cf9-4f9b-8ad3-366b58e0fcae",
     "lite.osworld": "osworld_vs_code_ea98c5d7"},
    {"label": "multi_apps", "hash": "bc2b57f3",
     "osworld": "bc2b57f3-686d-4ec9-87ce-edf850b7e442",
     "lite.osworld": "osworld_multi_apps_bc2b57f3"},
    {"label": "os", "hash": "13584542",
     "osworld": "13584542-872b-42d8-b299-866967b5c3ef",
     "lite.osworld": "osworld_os_13584542"},
]

QCOW2 = "/home/haoranliu/cua-lite/lite/gym/envs/osworld/.cache/Ubuntu.qcow2"


# ---------------- docker helpers ----------------
def _ps() -> dict[str, str]:
    out = subprocess.run(["docker", "ps", "--format", "{{.ID}}\t{{.Names}}"],
                         capture_output=True, text=True, timeout=30).stdout
    return {l.split("\t", 1)[0]: l.split("\t", 1)[1] for l in out.splitlines() if "\t" in l}


def _pick(baseline: dict[str, str], now: dict[str, str], env_id: str):
    new = {c: n for c, n in now.items() if c not in baseline}
    if not new:
        return None
    if len(new) == 1:
        return next(iter(new.items()))
    for c, n in new.items():
        if env_id == "osworld" and "lite.osworld" in n:
            continue
        if env_id in n:
            return c, n
    return next(iter(new.items()))


def _mem_to_mib(s: str) -> float | None:
    s = s.strip()
    for u, mul in (("GiB", 1024.0), ("MiB", 1.0), ("KiB", 1 / 1024.0), ("B", 1 / (1024 * 1024.0))):
        if s.endswith(u):
            try:
                return round(float(s[:-len(u)]) * mul, 1)
            except ValueError:
                return None
    return None


def _stat(cid: str) -> dict[str, Any]:
    out = subprocess.run(
        ["docker", "stats", "--no-stream", "--format",
         "{{.MemUsage}}\t{{.CPUPerc}}\t{{.PIDs}}", cid],
        capture_output=True, text=True, timeout=60).stdout.strip()
    if not out:
        return {}
    mem, cpu, pids = (out.split("\t") + ["", "", ""])[:3]
    try:
        cpu_v = float(cpu.replace("%", "").strip())
    except ValueError:
        cpu_v = None
    return {"mem_mib": _mem_to_mib(mem.split("/")[0]), "cpu_perc": cpu_v, "pids": pids.strip()}


def _cleanup(env_id: str) -> int:
    n = 0
    for cid, name in _ps().items():
        if "lite-env-" not in name:
            continue
        if env_id == "osworld" and "lite.osworld" in name:
            continue
        if env_id in name:
            subprocess.run(["docker", "rm", "-f", cid], capture_output=True, timeout=60)
            n += 1
    return n


def _desc(xs: list[float]) -> dict[str, Any]:
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"n": 0}
    xs_s = sorted(xs)
    return {
        "n": len(xs),
        "median": round(st.median(xs), 2),
        "mean": round(st.mean(xs), 2),
        "min": round(min(xs), 2),
        "max": round(max(xs), 2),
        "std": round(st.pstdev(xs), 2) if len(xs) > 1 else 0.0,
    }


# ---------------- per-env measurement ----------------
async def measure_env(env_id: str, tasks, settle: float, samples: int, gap: float):
    per_task = []
    boot, idle_mem, idle_cpu = [], [], []
    for t in tasks:
        task_id = t[env_id]
        rec = {"label": t["label"], "hash": t["hash"], "task_id": task_id}
        print(f"\n[{env_id}] {t['label']} ({task_id})", flush=True)
        baseline = _ps()
        env = None
        try:
            t0 = time.perf_counter()
            env = gym.make(f"{env_id}@{task_id}", max_steps=30,
                           post_action_delay=0.0, cursor_overlay=False)
            res = await env.reset()
            b = time.perf_counter() - t0
            ready = bool(getattr(res.observation, "screenshot_b64", None))
            rec["boot_reset_s"] = round(b, 2)
            rec["ready"] = ready
            print(f"  boot+reset: {b:.1f}s ready={ready}", flush=True)
            if ready:
                boot.append(b)

            picked = _pick(baseline, _ps(), env_id)
            if not picked:
                rec["container"] = None
                print("  WARN: no container identified", flush=True)
            else:
                cid, cname = picked
                rec["container"] = cname
                # settle to true idle, THEN sample repeatedly
                print(f"  settling {settle:.0f}s then {samples} samples @ {gap:.0f}s ...", flush=True)
                await asyncio.sleep(settle)
                series = []
                for _ in range(samples):
                    s = _stat(cid)
                    if s:
                        series.append(s)
                    await asyncio.sleep(gap)
                mems = [s["mem_mib"] for s in series if s.get("mem_mib") is not None]
                cpus = [s["cpu_perc"] for s in series if s.get("cpu_perc") is not None]
                rec["idle_series"] = series
                rec["idle_mem_mib"] = _desc(mems)
                rec["idle_cpu_perc"] = _desc(cpus)
                if mems:
                    idle_mem.append(st.median(mems))
                if cpus:
                    idle_cpu.append(st.median(cpus))
                print(f"  idle mem median={rec['idle_mem_mib'].get('median')} MiB  "
                      f"cpu median={rec['idle_cpu_perc'].get('median')}%  pids={series[-1].get('pids') if series else '?'}",
                      flush=True)
        except Exception as e:
            rec["error"] = f"{type(e).__name__}: {e}"
            print(f"  ERROR: {rec['error']}", flush=True)
        finally:
            if env is not None:
                try:
                    await env.close()
                except Exception as e:
                    rec["close_error"] = f"{type(e).__name__}: {e}"
        per_task.append(rec)
    reaped = _cleanup(env_id)
    return {
        "env_id": env_id,
        "per_task": per_task,
        "aggregate": {
            "boot_reset_s": _desc(boot),
            "idle_mem_mib": _desc(idle_mem),      # per-task medians -> across-task stats
            "idle_cpu_perc": _desc(idle_cpu),
        },
        "leftover_reaped": reaped,
    }


def _host() -> dict[str, Any]:
    def sh(c):
        try:
            return subprocess.run(c, capture_output=True, text=True, timeout=30).stdout.strip()
        except Exception:
            return ""
    ctx = {
        "date": time.strftime("%Y-%m-%d"),
        "nproc": sh(["nproc"]),
        "mem_total": sh(["bash", "-c", "free -h | awk 'NR==2{print $2}'"]),
        "kvm_present": bool(sh(["bash", "-c", "test -e /dev/kvm && echo 1"])),
        "images": {},
    }
    for tag in ("cua-lite/osworld:latest", "cua-lite/lite.osworld:latest",
                "cua-lite/sandbox.linux:latest"):
        s = sh(["docker", "images", "--format", "{{.Size}}", tag])
        if s:
            ctx["images"][tag] = s
    if os.path.exists(QCOW2):
        try:
            ctx["osworld_qcow2_bytes"] = os.path.getsize(QCOW2)
            ctx["osworld_qcow2_gib"] = round(os.path.getsize(QCOW2) / 1024**3, 1)
        except OSError:
            pass
    return ctx


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--env-id", default="both", choices=["osworld", "lite.osworld", "both"])
    ap.add_argument("--tasks", type=int, default=5)
    ap.add_argument("--settle", type=float, default=25.0, help="idle seconds before sampling")
    ap.add_argument("--samples", type=int, default=8, help="docker stats samples per container")
    ap.add_argument("--gap", type=float, default=2.0, help="seconds between samples")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "footprint.json"))
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    if args.smoke:
        args.tasks, args.settle, args.samples, args.gap = 1, 8, 4, 1.5

    tasks = MATCHED_TASKS[:args.tasks]
    envs = ["lite.osworld", "osworld"] if args.env_id == "both" else [args.env_id]
    results = {
        "meta": {"harness": "measure_footprint.py", "n_tasks": len(tasks),
                 "settle_s": args.settle, "samples": args.samples, "sample_gap_s": args.gap,
                 "mode": "direct (no env-server, no model, no GPU)", "host": _host()},
        "envs": {},
    }
    for env_id in envs:
        print(f"\n{'='*66}\nFOOTPRINT: {env_id}\n{'='*66}", flush=True)
        results["envs"][env_id] = asyncio.run(
            measure_env(env_id, tasks, args.settle, args.samples, args.gap))
        json.dump(results, open(args.out, "w"), indent=2)   # incremental save

    print(f"\nwrote {args.out}\n")
    for env_id, r in results["envs"].items():
        a = r["aggregate"]
        print(f"{env_id}:")
        print(f"  boot+reset : {a['boot_reset_s'].get('median')} s (median, n={a['boot_reset_s'].get('n')})")
        print(f"  idle mem   : {a['idle_mem_mib'].get('median')} MiB (median across tasks)")
        print(f"  idle cpu   : {a['idle_cpu_perc'].get('median')} % (median across tasks)")


if __name__ == "__main__":
    main()
