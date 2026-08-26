# CUA-Lite — LinkedIn 02（沙盒专篇 · VM-free OSWorld）

共享约定见 [`../../README.md`](../../README.md)（数字口径、平台规范、资产、领头图）。本篇是**一个结果**：结果前置，钩子必须落在折叠线以内。

改编自 `posts/red/02/README.md` 的 **English** 版。**内容相同，形态按 LinkedIn 重排**。
LinkedIn 版式说明见 `../01/README.md`（链接前置、首两行折叠、3–5 个标签、@ 提及机构）。

**本篇与 01 的分工：** 01 讲平台总览，02 拿一个**可核查的结果**说话 —— 这也是 LinkedIn 上更容易被工程师转发的类型：结果先行，方法随后。

---

## 正文（直接复制）

```
We reproduced OSWorld without a virtual machine: under a quarter of the memory, ~5× more instances, and scores that track the original within a few points across 13 models.

Write-up → https://cua-lite.github.io/blog/kvm-free-osworld
Code → https://github.com/cua-lite/cua-lite

Why bother: training and benchmarking computer-use agents takes a lot of real desktop environments. OSWorld is one such benchmark — a full Ubuntu, software included — but every task boots its own VM, needs /dev/kvm, and is too heavy to run at scale.

▪️ Drop the VM
Lite.OSWorld keeps OSWorld's desktop, tasks, and evaluators, and changes only how it runs: a plain Docker container, no /dev/kvm.

▪️ Score parity
A cheap copy is only worth it if it doesn't change the conclusion. Across 13 models, container scores track the original within a few points, so scores and training signal from Lite.OSWorld carry straight back to the original benchmark.

▪️ Beyond OSWorld
Lite.OSWorld is only the start. On the same VM-free base we're building more sandboxes, each shipping verifiable rewards — so the same sandbox both benchmarks and trains (RL). From everyday browser and desktop work to professional software like GMAT for spacecraft trajectories and PyMOL for molecular structures.

We'd like this to grow into a community-driven open-source CUA sandbox ecosystem — bring your environment or agent.

Built at UC Berkeley and Microsoft.

#MachineLearning #AIAgents #ReinforcementLearning #OpenSource
```

---

## 配图

`assets/` 下每张图都是指向 `posts/red/02/assets/` 的**软链**（`mode 120000`），不复制文件。
**只链英文版** —— LinkedIn 以英文为主，`*-zh.png` 未纳入。

- **单图（领头）**：`assets/02-footprint.png` —— 全套最耐缩的一张，横版不会被裁，一眼给全：同一套任务、`/dev/kvm` 没了、4.1→0.9 GB。`01b-cover.png`（VM → 容器示意）作第二张。
- **轮播**：`02-footprint.png` → `04-parity.png`（13 模型散点）→ `01b-cover.png` → `05-belt.png`（沙盒家族）
  **不用 `03-hh.png`** —— 理由见 `../../README.md`「不要用」一节。
- 同样建议用 **document（PDF 轮播）** 形态。

---

## 发布前检查（比 01 严格，因为本篇是拿数字说话）

- **`~4.6×` 必须能说清是怎么来的。** `posts/twitter/01/README.md` 里留有一条自查：这个数**可能是由内存比 4.1/0.9 = 4.56 推导，而非实测**。LinkedIn 上工程师会直接问“什么硬件、并发多少、怎么测的”。发之前确认它是实测；若是推导，就改成定性说法（“fits several times more instances per host”）。
- **parity 的具体数字要准备好**：mean |Δ| ≈ 2.7、worst 5.0（13 个模型）。正文用定性的 “within a few points”（与博客口径一致），但评论区被追问时要能立刻给出精确值 —— 主动披露比被人扒出来好。
- 其余事实与来源同 `posts/red/02/README.md` 的「来源」表。
- 小红书标签（含 `#擦边`）不要带过来。
