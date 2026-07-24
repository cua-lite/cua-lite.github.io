# Benchmarking — OSWorld (KVM VM) vs Lite.OSWorld (KVM-free container)

Strict re-evaluation of the **environment cost** behind the *KVM-free OS(World) at
Scale* post. Two independent, reproducible measurements, each with its own script:

| Script | Measures | Source of truth |
|---|---|---|
| `analyze_timing.py`   | **Per-step latency** — environment `act` (action + settle + screenshot) vs model `predict`, per turn | The **real leaderboard eval rollouts** (~66k turns/env), not a synthetic micro-bench |
| `measure_footprint.py`| **Resource footprint** — boot+reset, steady-state idle RAM/CPU, on-disk size | A **live** direct-mode run (`docker stats`), settled then repeatedly sampled |

Outputs: `results.json` (timing) and `footprint.json` (footprint); the human-readable
summary is `RESULTS.md`.

## Why this supersedes the earlier micro-bench

The earlier numbers were re-derived because two of them were not measured strictly:

1. **Per-step latency** was taken from 50 synthetic `mouse_move` steps with the settle
   delay forced to zero. That is not what the benchmark actually runs. `analyze_timing.py`
   instead reads the timing of **every turn of every leaderboard rollout** — the real
   action distribution, ~66k turns per env — and compares them **paired**: the same
   `(agent, task)` on both envs, so the delta isolates the environment.
2. **Idle CPU/RAM** was a *single instantaneous* `docker stats` snapshot taken the moment
   `reset()` returned — i.e. while the desktop was still settling, which made idle CPU in
   particular noisy and unreliable. `measure_footprint.py` **settles** for `--settle`
   seconds of true idle, then takes `--samples` spaced samples and reports the **median**
   (with IQR and the full series retained), which is stable and reproducible.

## What is measured vs projected

- **Measured:** per-turn `act`/`predict` latency (real rollouts); boot+reset; steady-state
  idle RAM/CPU; on-disk image + VM backing-disk size.
- **Projected (clearly labelled in `RESULTS.md`):** max instances per host and
  throughput-at-scale. These are *arithmetic* from the measured per-instance footprint ×
  host capacity × headroom — no 300–1300-instance fleet was booted. Reported as a range
  with the formula and inputs shown, never as a measured fact.

## Reproduce

### 1. Per-step latency (from the eval artifacts)
No env boot needed — reads the trajectory timing directly.

```bash
python3 analyze_timing.py \
  --osworld /path/to/.exps/eval/osworld/<run>/run_0 \
  --lite    /path/to/.exps/eval/lite.osworld/<run>/run_0 \
  --out results.json
```
Defaults point at the two runs that back the leaderboard JSONs on the blog
(`assets/exps/eval/{osworld,lite.osworld}/.../run_0.json`).

### 2. Footprint (live, direct mode)
Must run from the `cua-lite` repo so `import lite.gym` resolves; needs Docker (+ `/dev/kvm`
for the OSWorld VM).

```bash
cd /path/to/cua-lite
unset CUA_LITE_ENV_SERVER_URL CUA_LITE_ENV_SERVER_TOKEN   # force DIRECT (in-process) mode
uv run --no-sync python \
  /path/to/blog/kvm-free-osworld/benchmarking/measure_footprint.py \
  --env-id both --tasks 5 --settle 25 --samples 8 --gap 2 \
  --out /path/to/blog/kvm-free-osworld/benchmarking/footprint.json
```

Runs are **sequential**; each container is `close()`d before the next, so idle and boot
numbers are not muddied by concurrency. `act`/idle figures include the OSWorld VM's
in-container QEMU process (that is the real cost of the VM).

## Caveats

- `act` (env per-step) includes the **shared** `post_action_delay` settle on both envs, so
  the *difference* between envs — not the absolute value — is the environment overhead.
- Idle footprint is steady-state after settling; transient boot spikes are excluded by design.
- Latency N is huge and real; footprint N is small (a few matched tasks) — treat footprint
  as order-of-magnitude, with memory the stable signal (CPU%, even settled, is noisier).
- No model / GPU cost is in either environment measurement; model `predict` time is reported
  by `analyze_timing.py` only to show it is env-agnostic and dominates a real turn.
