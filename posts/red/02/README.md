# CUA-Lite — 小红书 02（沙盒专篇 · VM-free OSWorld）

系列第二篇。**定位：沙盒深挖，核心 = `blog/kvm-free-osworld`**——OSWorld 太重跑不了规模，
Lite.OSWorld（我们的）把它搬成 VM-free、分数还对得上。这里放真实数字（红书 01 只做总览）。

**语言：** 沿用站点语气（朴素、准确、平行）；OSWorld = 已有的第三方 benchmark（重型虚拟机），
Lite.OSWorld = **我们**把它迁移成 VM-free 的产物（保留同样的任务与评测器）——务必保持这个 ownership 区分。

---

## 标题（选一个；小红书上限约 20 字，已标字数）

> **重心（已修正）：** 核心 = 一系列**轻量、免虚拟机的沙盒 + 可验证任务**（训练/评测任何 agent、可扩展）；OSWorld 复现只是**抛砖引玉的第一个例子**。标题别让「OSWorld 同分」抢了核心。

1. ⭐ VM-free OS(World)：可扩展的 CUA 沙盒环境　（对齐 red/01「…的开源生态」句式：双关做钩子，冒号后是干净的名词短语，不用清单式副标题）
2. VM-free OS(World)：一套可扩展的 CUA 沙盒
3. 不止 OSWorld：轻量、可验证的 CUA 沙盒　（纯中文核心版）
4. VM-free OS(World)，at scale　（＝博客原标题，最省）

---

## 正文（中文 / English，各自直接复制）

**中文版**

```
VM-free OS(World)：可扩展的 CUA 沙盒环境

训练、评测 computer-use agent（CUA）都需要大量真实桌面环境。常用的 OSWorld 就是这样一个评测环境：完整的 Ubuntu、软件齐全；但每个任务都要开一台虚拟机，依赖 /dev/kvm、开销大，难以规模化。

为此，我们要做的是一系列轻量、免虚拟机的 CUA 沙盒。先从最熟悉的 OSWorld 入手。

▪️ 去掉虚拟机
把它迁移成 Lite.OSWorld：桌面、任务、评测器全部保留，只把运行方式换成普通 Docker 容器，不再需要虚拟机。单实例内存降到原来的不足四分之一，同一台机器能并行的实例数大约是原来的 4.6 倍，自然就能规模化。

▪️ 分数一致性
便宜的复制品，只有不改变结论才有意义。13 个模型实测下来，容器里的分数和原版 OSWorld 基本一致；在 Lite.OSWorld 上得到的分数与训练信号，可以直接迁回原来的 benchmark。

▪️ 不止 OSWorld：可扩展的训练沙盒
Lite.OSWorld 只是起点。在同一套 VM-free 底座上，我们正扩展出更多沙盒，每个都自带可验证的奖励，因此既能用来评测，也能用来训练（RL）。场景从浏览器、桌面的日常任务，到用 GMAT 算航天轨道、PyMOL 看分子结构这类专业软件。

我们希望它长成一个社区驱动的开源 CUA 沙盒生态，欢迎带来你的环境或 agent。

博客 cua-lite.github.io/blog/kvm-free-osworld
GitHub github.com/cua-lite/cua-lite
数据 huggingface.co/cua-lite
UC Berkeley · Microsoft

（项目总览看上一篇，这篇专讲沙盒。）

#人工智能 #ai #agent #强化学习 #cua #webagent #guiagent #mobileagent #擦边
```

**English**

```
VM-free OS(World): scalable CUA sandboxes

Training and benchmarking computer-use agents (CUAs) takes a lot of real desktop environments. OSWorld is one such benchmark: a full Ubuntu, software included. But every task boots its own virtual machine, needs /dev/kvm, and is too heavy to run at scale.

Our answer is a series of lightweight, VM-free CUA sandboxes. We start with the one everyone knows: OSWorld.

▪️ Drop the VM
Lite.OSWorld keeps OSWorld's desktop, tasks, and evaluators, and changes only how it runs: a plain Docker container, no /dev/kvm. Memory per instance falls to under a quarter, one host fits about 4.6× more instances, and it scales.

▪️ Score parity
A cheap copy is only worth it if it doesn't change the conclusion. Across 13 models, scores in the container track the original OSWorld within a few points; the scores and training signal you get from Lite.OSWorld carry straight back to the original benchmark.

▪️ Beyond OSWorld: scalable training sandboxes
Lite.OSWorld is only the start. On the same VM-free base we are building more sandboxes, each shipping verifiable rewards — so the same sandbox both benchmarks and trains (RL). From everyday browser and desktop work to professional software like GMAT for spacecraft trajectories and PyMOL for molecular structures.

We hope this grows into a community-driven open-source CUA sandbox ecosystem — bring your environment or agent.

Blog cua-lite.github.io/blog/kvm-free-osworld
GitHub github.com/cua-lite/cua-lite
Data huggingface.co/cua-lite
UC Berkeley · Microsoft

(Project overview in the previous post; this one is all about the sandboxes.)

#人工智能 #ai #agent #强化学习 #cua #webagent #guiagent #mobileagent #擦边
```

---

## 配图（全图片，都在 `assets/`；抓自 `blog/kvm-free-osworld`）

全英文;每张 standalone(标题自带 OSWorld↔Lite.OSWorld 语境);统一设计语言(小标题 + Fraunces 标题 + 图 + 图注/水印);卡片按内容高、无死空。

1. **封面(4 张:英文 + 中文各两版,同版式;与 red/01 同一套排版系统)** — 标题 = blog H1「VM-free OS(World) at scale.」;lead 讲清「可验证」的因果(`Verifiable rewards, so one sandbox benchmarks and trains:` / 「每个任务自带可验证奖励,一套沙盒既评测也训练(RL):」),两条 bullet 分别是第一个例子与家族。lead 与 bullet 同字号 34px,**全部单行**。
   - `assets/01a-cover.png` / `assets/01a-cover-zh.png`(1:1) — 页脚是沙盒家族(Lite.OSWorld · Lite.CUAGym · Lite.CUAWorld)。
   - `assets/01b-cover.png` / `assets/01b-cover-zh.png`(内容高) — 底部加 **VM → 容器** before/after;两栏结构对称(标签/窗口/运行时/宿主要求),右栏 `any Docker host` 与左栏 `/dev/kvm` 对位;箭头标 `~4.6× per host`。
2. **`assets/02-footprint.png`** — 「Keeps the desktop, drops the VM」+ 对比表(`.cmp`)。
3. **`assets/03-hh.png`** — 「The same task, same behavior」+ VM/容器同任务**上下堆叠**(`.hh` 竖排,单栏全宽 → 每帧可读;OSWorld 在上、Lite.OSWorld 在下)。
4. **`assets/04-parity.png`** — 「Container scores match the VM」+ 13 模型 parity 散点(`.par`)。
5. **`assets/05-belt.png`** — 「One base, a family of sandboxes」+ 沙盒 belt(`.belt-fig`);图注「Every sandbox ships verifiable tasks」。

**重制脚本：** `capture_sections.py`(抓 5 张博客图 + vm/container 两态,透明紧裁)· `make_slides.py`(内页 02–05 设计卡)· `make_cover.py`(01a/01b)。中间产物在 `build/`。

---

## 来源（真实性核对）

| 说法 | 来源 / 状态 |
|---|---|
| OSWorld = 重型 VM，需 /dev/kvm、嵌套虚拟化 | 博客 §01 段一，逐句 |
| Lite.OSWorld（ours）= 迁移 OSWorld、VM-free、同任务同评测器 | 博客 §01 段二 + 对比表「Task suite: Identical」 |
| 内存 4.1 → 0.9 GB · 并行 ~4.6× · 冷启动 29.9→23.8 s | 博客对比表 `.cmp`（**见发布前检查**） |
| 13 模型分数「基本一致」（正文用词） | parity plot 真实数据（`assets/exps/eval/{osworld,lite.osworld}`）。内部核对：mean\|Δ\|≈2.7 / worst 5.0（真实，但**按你要求不进正文**，只用定性「基本一致」；封面/图沿用「same scores · 13 models」） |
| 不止 OSWorld：一系列带可验证任务的 CUA 沙盒 | 博客 §02「Beyond OSWorld」 |

## 发布前检查

- **对比表数字（4.1→0.9 GB、~4.6×、29.9→23.8 s）**：博客里**仍有一段旧的 authoring 注释**把这些标成 placeholder（"stay skeletons until measured"），但作者（你）此前确认它们已是真实值（commit `40a0451`）。→ 正文按真实使用；**建议顺手删掉博客里那段过时注释**以免误导。若仍有存疑，就把这三项在正文里改成定性（「更省内存、一机多开」）。
- parity：正文只说「基本一致」（与博客「within a few points」同为定性口径）；真实 mean 2.7 / worst 5.0 仅内部核对，不进正文。
- ✅ **GitHub 已公开**（2026-08-22 实测 `HTTP 200`、`gh api private=false`），正文那行 `github.com/cua-lite/cua-lite` 可以保留。此前的 404 阻塞已解除。
- **术语统一用 `VM-free`**（2026-08-25 全站从 `KVM-free` 改定）：容器不是虚拟机，VM-free 属实且读者更熟悉；博客正文本就写「VM tax」「drops the VM」。**URL slug `/blog/kvm-free-osworld/` 保持不变**（已发布，改了会断链），故会出现「标题 VM-free / 网址 kvm-free」的不对称，属预期。
- 「GMAT、PyMOL」只点名软件、不描述夸张动作（博客原文的「flying spacecraft / turning proteins」偏文学，红书从简以免 overclaim）。
- **「UC Berkeley · Microsoft」不在本篇博客里**——来源是首页 citation（作者含 Berkeley/Microsoft）+ 已发布的 red/01（你此前认可）。发布前确认无误即可。
- 「same scores / 基本一致」是 headline 压缩，正文与博客都用定性口径，真实数据支持（mean 2.7 / worst 5.0），可站得住。

## 系列

- **01** 总览（首页 hero 三条）· **02（本篇）** 沙盒专篇（VM-free OSWorld）· 后续可做 数据 / 框架 专篇。
