# CUA-Lite — Reddit 02（VM-free OSWorld）

共享约定见 [`../../README.md`](../../README.md)（数字口径、平台规范、资产、领头图）。本文件只写本篇特有的东西。

**目标版块：** r/MachineLearning，flair **`[P]`**。
**次选：** r/reinforcementlearning（同一份稿子，标题换成侧重 verifiable-task 沙盒）。
**不发 r/LocalLLaMA** —— 见下。版块规模与性格的调研数据在 [`../../README.md` §2b](../../README.md)。

**为什么这篇不进 r/LocalLLaMA。** 那个版块的货币是「**我自己的机器能跑什么模型**」—— 显存、量化、推理栈。本篇的论点是「**换掉运行时之后基准分是否守得住**」,受众是要**复现和引用一个 benchmark** 的人，不是要在自己机器上跑模型的人。同一份 parity 散点图，在 r/ML 是可核验的证据，在 r/LocalLLaMA 是「跟我没关系的图表」。**`posts/reddit/01` 才是发那边的那篇。**

（真要在 r/LocalLLaMA 讲这件事，得整篇重写成「OSWorld 现在能在你自己的盒子上跑，不需要 KVM」，把 parity 降级成一句话的脚注。这不是换个标题的事，别硬改。）

**两个候选版块的取舍，不存在明显更优的一个：**

| | r/MachineLearning `[P]` | r/reinforcementlearning |
|---|---|---|
| 规模 | 3.1M，但年增仅 2.6%，内容已漂向求职/求助 | 88k，年增 32%，话题集中 |
| 对口 | 复现 + 数据 = `[P]` 的标准形态 | 「同一个沙盒既评测又训练」正中其关切；他们的世界就是仿真环境 |
| 风险 | **高** —— 版规把自我推广导向每周 `[D] Self-Promotion Thread`，判定权在版主 | 低 |
| 结论 | **高上限高风险**，本篇能进主版的唯一凭据是那份 13 模型 parity 数据 | **低风险高信噪**，适合先发这里试水 |

保守走法：**先发 r/reinforcementlearning**，用那边的评论把措辞和常见质疑磨一遍，隔几天再发 r/MachineLearning `[P]`。

## 立论：结构逐条照搬 `posts/red/02` 的英文版

**三块小标题直接沿用红版：`Drop the VM` / `Score parity` / `Beyond OSWorld: scalable training sandboxes`。** 我一度自己拆成 `The VM tax` / `What we changed` / `Does that change the answer?` / `Beyond OSWorld` 四块 —— 多一块、每块更长，而且 `What we changed` 和 `The VM tax` 讲的是同一件事的两面。红版那三块是打磨过的：**问题 → 我们改了什么 → 分数还作数吗 → 不止 OSWorld**，正好是读者的提问顺序。**红版有的句子就用红版的。**

**Reddit 化只动这几处，别的照抄：**

- `▪️` → markdown 加粗（Reddit 不吃小红书符号）
- 三行链接从页脚提到开场白之后（`[P]` 帖惯例本就是 `Paper: … / Code: …` 顶在开头）
- 删 hashtag、删 `UC Berkeley · Microsoft`（那是背书不是披露），换成末尾的 `Disclosure: I'm one of the authors.`
- 删 `（Project overview in the previous post…）`——那是小红书的连载语，Reddit 没有这个上下文
- `Lite.OSWorld` 首次出现补 `, our port,`（归属，见下）
- `Score parity` 末尾补一句 `The per-model plot is in the blog post above.` —— 红版靠页脚链接就够，Reddit 版链接在上方，指一下路

**删掉了 "What we'd flag" 那一段** —— 你的决定。需要知道代价：那段是 `[P]` 帖读起来像研究而非宣传的主要抓手，删掉之后本篇更接近一篇「发布」。

**但那段承担的两个 hedge 没有丢，因为红版原文自带：**

| 原来靠自曝短板兜底 | 现在靠红版原句兜底 |
|---|---|
| `The gap is small but not zero` | `scores … **track** the original OSWorld **within a few points**`（不是 identical） |
| `"~5×" is a density figure from our hardware` | `one host fits **about** 5× more instances`（"about" 就是那个 hedge） |

第三条 `OSWorld 的任务和评测器未改，上游的问题这里照样有` 是纯粹删掉了 —— 它本来也不算 hedge，是提醒，红版正文里 `keeps OSWorld's desktop, tasks, and evaluators` 已经隐含。

**别再把结论写死。** 中途写过 `Across 13 models, it barely does.`，也想过 `it doesn't` —— 后者直接和 `within a few points` 打架。**定性写法要始终留住那个非零的口子**，否则第一个跑复现的人就能当场打脸。

---

## 标题（选一个）

1. ⭐ `[P] Lite.OSWorld: we dropped the VM from OSWorld and checked whether the scores still hold (13 models)`
2. `[P] Reproducing OSWorld in a plain Docker container instead of a VM — 13-model score comparison`
3. `[P] Lite.OSWorld: VM-free OSWorld on plain Docker, and what that does to the scores`

（r/reinforcementlearning 版标题：`Verifiable-task desktop sandboxes that run without a VM — the same sandbox for eval and RL`）

**标题要带 `Lite.OSWorld` 这个可搜索的抓手**，理由同 reddit/01 的 `CUA-Lite`：不带名字的项目帖，读者事后没有能搜、能记的词。

**但带名字就必须标明归属。** `Lite.OSWorld` 单独出现会被读成「OSWorld 官方的精简版」。①号标题用 `we dropped the VM from OSWorld` 把「我们做的、从 OSWorld 派生」两件事一次说清；正文里也写成 `Lite.OSWorld, our port,`。**这一条对整个 `Lite.*` 家族都适用。**

**`~5×` 不进标题。** 它是 `../../README.md` 风险条目里标记为「按博客 authoring 注释尚未实测」的三项之一。放正文并带上 "a density figure from our hardware" 的限定可以，**当标题主张不行** —— 在 r/MachineLearning，标题里的数字就是被拿来核的那个。原②号标题的 `~5× more instances per host` 已经删掉（`per host` 的说法本身也别扭）。

---

## 正文（markdown，直接粘）

```
Training and benchmarking computer-use agents (CUAs) takes a lot of real desktop environments. [OSWorld](https://github.com/xlang-ai/OSWorld) is one such benchmark: a full Ubuntu, software included. But every task boots its own virtual machine, needs /dev/kvm, and is too heavy to run at scale.

Our answer is [CUA-Lite](https://cua-lite.github.io), a series of lightweight, VM-free CUA sandboxes. We start with the one everyone knows: OSWorld.

Blog: https://cua-lite.github.io/blog/kvm-free-osworld
Code: https://github.com/cua-lite/cua-lite
Data: https://huggingface.co/cua-lite

**Drop the VM**
[Lite.OSWorld](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/lite/osworld/README.md), our port, keeps OSWorld's desktop, tasks, and evaluators, and changes only how it runs: a plain Docker container, no /dev/kvm. Memory per instance falls to under a quarter, one host fits about 5× more instances, and it scales.

**Score parity**
A cheap copy is only worth it if it doesn't change the conclusion. Across 13 models, scores in the container track the original OSWorld within a few points; the scores and training signal you get from Lite.OSWorld carry straight back to the original benchmark. The per-model plot is in the blog post above.

**Beyond OSWorld: scalable training sandboxes**
Lite.OSWorld is only the start. On the same VM-free base we are building more sandboxes, each shipping verifiable rewards — so the same sandbox both benchmarks and trains (RL). From everyday browser and desktop work to professional software like GMAT for spacecraft trajectories and PyMOL for molecular structures.

We hope this grows into a community-driven open-source CUA sandbox ecosystem — bring your environment or agent.

Disclosure: I'm one of the authors. Happy to answer questions about the port, the evaluators, or how we ran the comparison.
```

---

## 配图

`assets/` 全是软链（`mode 120000`），只链英文版；动画链自 `posts/twitter/01/assets/`。

**一帖只配一段媒体。** Reddit 正文帖是「一个 media slot + 一段文字」，没有轮播。`assets/` 只留**三个文件**：领头动画的 mp4 + gif，加一张留给评论区的证据图。

**分工：动画负责钩住人，散点负责说服人。**

- **领头 / 钩子：`03-vm-tax.mp4`（680 KB）** —— 在两个状态间循环：`OSWorld` 顶着 `Ubuntu.qcow2` + `QEMU·KVM` + `/dev/kvm`（「A desktop sealed in a VM」），切到 `Lite.OSWorld` 的虚线 `CONTAINER` 框（「Out of the VM — the same desktop, now a container」）。**这段动画就是本篇的论点本身**，不是泛泛的产品演示。`.gif`（3.1 MB）作备用；优先 mp4，Reddit 反正会把 GIF 转视频。
- **评论区证据：`04-parity.png`（13 模型散点）** —— 散点是 r/ML 读者能一眼自行核验的东西（点是否落在对角线上），比任何文字都有说服力。

**已删除的三张，各有明确理由：**

- **`02-footprint.png`（对比表）** —— 表里全是 footprint 数字（内存 / 冷启动 / 并行倍数），而 `../../README.md` 的风险条目指出这几项按博客的 authoring 注释**尚未实测**。正文里只留了 `about 5× more instances` 这一句、带着 `about` 的限定；把同一批数字放大成一张表，等于把最没底气的部分做成主视觉，在 r/MachineLearning 是最容易被追问的地方。
- **`01b-cover.png`** —— 标语 + bullet + 数字条的图文卡，在 Reddit 技术版是广告的标志，且内容与正文重复。
- **`05-belt.png`** —— 与 `posts/reddit/01` 的沙盒总览撞题；本篇只讲「去掉虚拟机、分数是否守得住」。

同理**不要去 `red/` 里捞 `01-hero`（三端总览，不对题，属于 reddit/01）或 `03-hh.png`（并排 rollout，缩略图里看不清）**。

---

## 发布前检查

- **parity 一律定性**（"within a few points"，与博客 `:271` 原话一致）。**精确聚合值不进正文** —— 它们在站点和博客上都查不到，读者点进去会对不上；要给就先补进博客的图注。
- **`Lite.OSWorld` 每次出现都要读得出是我们的**：正文首次出现写 `Lite.OSWorld, our port,`；标题用 `we dropped the VM from OSWorld`。别让它被当成 OSWorld 官方的精简版。
- **`~5×` 只在正文出现且必须保留 `about`**。删掉 "What we'd flag" 之后，`about 5× more instances` 里那个 `about` 是**唯一**的 hedge 了 —— 它是 `../../README.md` 风险条目里标着「按博客 authoring 注释尚未实测」的三项之一。不进标题、不做主视觉（`02-footprint.png` 就是因此没进 `assets/`）。
- **不要把分数结论写死**：`track … within a few points` 不能改成 `identical` / `the same` / `it doesn't change`。删掉自曝短板之后这句同样是唯一的 hedge。

- **账号要有历史**：新号 + 首帖即自己项目，容易被自动过滤，也招读者反感。
- **别同日多版块群发**：r/MachineLearning 与 r/reinforcementlearning 至少隔开几天，标题各自改写。
- 发帖后**盯前两小时的评论**，Reddit 的算法和风评都取决于作者是否在场回应。
