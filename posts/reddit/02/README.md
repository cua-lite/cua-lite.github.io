# CUA-Lite — Reddit 02（VM-free OSWorld）

共享约定见 [`../../README.md`](../../README.md)（数字口径、平台规范、资产、领头图）。本文件只写本篇特有的东西。

**目标版块：** r/MachineLearning，flair **`[P]`**（主版只收有实质内容的项目帖；纯宣告只能进每周的 `[D] Self-Promotion Thread`）。
**次选：** r/reinforcementlearning（同一份稿子，标题换成侧重 verifiable-reward 环境）。

## 与 LinkedIn 版的差异

平台规范对照表已收进 [`../../README.md`](../../README.md)。本篇特有的一点：**这里有一段 "What we'd flag" 的自曝短板**，那是 `[P]` 帖读起来像研究而非宣传的关键；但**数字仍一律定性**，与其余平台同口径。

---

## 标题（选一个）

1. ⭐ `[P] Reproducing OSWorld without a VM: plain Docker containers, scores within a few points across 13 models`
2. `[P] OSWorld in a container instead of a VM — 13-model score parity, ~5× more instances per host`
3. `[P] We dropped the VM from OSWorld and checked whether the scores still hold (13 models)`

（r/reinforcementlearning 版标题：`Verifiable-reward desktop environments that run without a VM — same sandbox for eval and RL`）

---

## 正文（markdown，直接粘）

```
We maintain CUA-Lite, an open-source stack for training and benchmarking computer-use agents. This post is about one piece of it: running OSWorld without a virtual machine, and whether that changes the numbers.

**The problem.** OSWorld hands an agent a real Ubuntu desktop per task, which is what you want for computer-use work. But every task boots its own VM and needs `/dev/kvm`, so nested virtualization rules out a lot of cloud instances, and memory per instance makes large rollout sweeps expensive.

**What we changed.** Lite.OSWorld keeps OSWorld's desktop, task suite and evaluators as they are, and swaps only the runtime: a plain Docker container, no `/dev/kvm`. Memory per instance drops to under a quarter, and a host fits roughly 5× more instances.

**Does it change the answer?** That's the only question that matters — a cheaper copy is worthless if it moves the scores. We ran the same 13 models on the original VM build and on ours, and the container tracks the VM within a few points, so scores and training signal collected in the container carry back to the original benchmark. The per-model parity plot is in the write-up.

**Why it matters beyond OSWorld.** The same container base carries our other sandboxes, so one environment serves both benchmarking and RL training instead of two separate stacks.

**What we'd flag if you're evaluating this:**

- The gap is small but not zero. If your work turns on small score differences, check the per-model plot and measure it yourself before trusting the port.
- "~5× more instances" is a density figure from our hardware; yours will differ.
- OSWorld's task suite and evaluators are unchanged, so anything wrong with them upstream is still wrong here.

Write-up with the comparison table and parity plot: https://cua-lite.github.io/blog/kvm-free-osworld
Code: https://github.com/cua-lite/cua-lite
Datasets and rollouts: https://huggingface.co/cua-lite

Disclosure: I'm one of the authors. Happy to answer questions about the port, the evaluators, or how we ran the comparison.
```

---

## 配图

`assets/` 全是软链（`mode 120000`），只链英文版；动画链自 `posts/twitter/01/assets/`。

**分工：动画负责钩住人，散点负责说服人。**

- **封面 / 钩子：`03-vm-tax.mp4`（680 KB）** —— 在两个状态间循环：`OSWorld` 顶着 `Ubuntu.qcow2` + `QEMU·KVM` + `/dev/kvm`（「A desktop sealed in a VM」），切到 `Lite.OSWorld` 的虚线 `CONTAINER` 框（「Out of the VM — the same desktop, now a container」）。**这段动画就是本篇的论点本身**，不是泛泛的产品演示。`.gif`（3.1 MB）作备用；优先 mp4，Reddit 反正会把 GIF 转视频。
- **证据：`04-parity.png`（13 模型散点）+ `02-footprint.png`（对比表）** —— 放正文链接或首条评论。散点是 r/ML 读者能一眼自行核验的东西（点是否落在对角线上），比任何文字都有说服力。

**不要用 `01-hero.gif`。** 它演示的是三端平台总览，而本篇只讲「去掉虚拟机、分数是否守得住」—— 不对题，会显得在硬塞宣传素材。那段属于 `posts/reddit/01`。

**也不要用 `01a/01b-cover.png`。** 标语 + bullet + 数字条的图文卡在 Reddit 技术版是广告的标志，且内容与正文重复。

`03-hh.png`（并排 rollout）不建议用：缩略图里看不清。

---

## 发布前检查

- **parity 一律定性**（"within a few points"，与博客 `:271` 原话一致）。**精确聚合值不进正文** —— 它们在站点和博客上都查不到，读者点进去会对不上；要给就先补进博客的图注。

- **账号要有历史**：新号 + 首帖即自己项目，容易被自动过滤，也招读者反感。
- **别同日多版块群发**：r/MachineLearning 与 r/reinforcementlearning 至少隔开几天，标题各自改写。
- 发帖后**盯前两小时的评论**，Reddit 的算法和风评都取决于作者是否在场回应。
