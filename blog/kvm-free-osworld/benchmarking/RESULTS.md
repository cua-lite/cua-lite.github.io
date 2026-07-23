# Results — OSWorld (KVM VM) vs Lite.OSWorld (KVM-free container)

Strict re-evaluation. Two measurements: **per-step latency** from the real leaderboard
rollouts (`analyze_timing.py` → `results.json`), and **resource footprint** from a live
direct-mode run (`measure_footprint.py` → `footprint.json`). Host: 384 cores, ~1.5 TiB RAM,
`/dev/kvm` present. No model / GPU in either environment measurement.

## 1. Per-step latency — real rollouts (not a micro-bench)

Every turn of every leaderboard rollout is timed: `act` = environment cost (dispatch the
action + shared settle delay + capture & return the screenshot); `predict` = model
inference (environment-agnostic). N ≈ **66k turns per env** (13 agents × ~321–325 tasks).

| Per step (median) | Lite.OSWorld | OSWorld (VM) | |
|---|---|---|---|
| **Environment `act`** | **4.72 s** | **2.53 s** | OSWorld **1.9× faster/step** |
| Model `predict` | 4.88 s | 5.17 s | ≈ equal (env-agnostic) |
| Env share of a step | 52 % | 36 % | |

**Paired — same agent + same task, 4,172 matched rollouts** (isolates the environment):
Lite's per-turn `act` is a **median 1.86× (+2.4 s)** slower than the VM's.

**Reading:** the KVM VM is genuinely *faster per environment step*. Lite is
**screenshot-bound** — a software-rendered, GPU-less desktop captured and shipped over the
exec-stdio channel — not action-bound. Because model `predict` is identical across envs and
is ~half of every step, the VM's per-step edge is a small slice of a real turn. Lite's
advantage is not latency; it is footprint (§2).

## 2. Resource footprint — live, settled, sampled

Boot+reset over N matched tasks; idle mem/CPU **settled 25 s then sampled 8×**, median
reported (the earlier micro-bench's single post-reset snapshot was the source of its noisy
idle-CPU number).

| | Lite.OSWorld | OSWorld (VM) | |
|---|---|---|---|
| Boot + reset (median) | **23.8 s** (n=5) | **29.9 s** (n=3) | Lite 1.26× faster |
| **Idle memory** (steady) | **904 MiB (~0.9 GB)** | **4,165 MiB (~4.1 GB)** | **4.6× less** |
| Idle CPU (steady) | 0.8 % | 4.2 % | both single-digit |
| Image on disk | **5.4 GB** | 7.3 GB + **23 GB** `Ubuntu.qcow2` ≈ 30 GB | ~5.5× less |
| Needs KVM / nested virt | **No** | Yes | |

**Two corrections vs the earlier micro-bench:**
- **Idle CPU is NOT ~1.6 cores / 164 % for the VM.** Settled, an idle KVM guest costs
  **~4 %** — the old three-digit figure was a boot-settling snapshot artifact. Idle CPU is
  *not* a meaningful differentiator once settled.
- **Idle memory is the real, stable differentiator: ~4.6× smaller** (0.9 vs 4.1 GB). The VM
  is provisioned 4 GB and its resident footprint sits near that ceiling regardless of load;
  the container holds ~0.9 GB.

## 3. Density at scale — PROJECTION (labelled)

Not measured by booting a fleet — arithmetic from the measured idle memory. Idle CPU is
single-digit for both, so on a normal host **RAM is the binding constraint**:

```
max_instances (RAM-bound) = floor( host_RAM × 0.85 / idle_mem_per_instance )
ratio = idle_mem(osworld) / idle_mem(lite) = 4165 / 904 ≈ 4.6×
```

So one host fits **~4.6× more Lite containers** than OSWorld VMs (RAM-bound). Combined with
the VM's ~1.9× faster per-step `act`, the at-scale throughput advantage for Lite is roughly
`4.6 / 1.9 ≈ 2.4×` in the worst case (env-step-bound) and up to ~4.6× when the model term
dominates each turn (which it does — `predict` ≈ `act`). **The scaling lever is memory
footprint, not per-step speed.**

## 4. Same environment, same scores

Across 13 agents the Lite.OSWorld and OSWorld leaderboards track closely (see the post's
leaderboard; source `assets/exps/eval/{osworld,lite.osworld}/…/run_0.json`). The cheap copy
does not change the answer.

## Caveats

- `act` includes the **shared** `post_action_delay` settle on both envs; the *difference*
  (not the absolute) is the environment overhead.
- Footprint N is small (3–5 matched tasks); memory is the stable signal, CPU noisier even
  settled. Latency N is large and real.
- OSWorld boot here initially failed because the VS Code **fileWatcher exhausted
  `fs.inotify.max_user_watches`** (rootless Docker shares that pool → dnsmasq in the qemu
  container couldn't watch `/etc/resolv.conf` → QEMU fell back to usermode networking → guest
  server unreachable → `vm_ready:false`). Freeing the watches fixed it; the numbers above are
  the successful runs. On a shared box, raise the ceiling
  (`sysctl fs.inotify.max_user_watches=4194304`) and add `files.watcherExclude` for heavy
  dirs (`.venv`, `.cache`, `*.qcow2`, …).
- Density is projected, not fleet-tested.
