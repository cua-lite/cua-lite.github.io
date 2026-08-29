# CUA-Lite — LinkedIn article 01

LinkedIn 的**长文（Pulse article）**，不是 post。两者不是同一个载体：post 有折叠线、吃 hashtag、
一图一帖；article 是一篇有标题、封面和小标题的文章，靠结构读完，不靠钩子截停。

**参考的三篇**（作者给定，均为 Dawn Song 的 Pulse 文章）：*Introducing Agents' Last Exam (ALE)*、
*Can AI agents turn security vulnerabilities into real attacks?*、*Introducing OpenSage*。
从它们身上抄的是**结构**，不是句子。

三篇一致的地方（样本小，但一致性本身是信号）：

| | ALE\* | ExploitGym | How We Broke… | OpenSage\* | 本文 |
|---|---|---|---|---|---|
| 词数 | ~1800 | **295** | **732** | ~650 | **654** |
| 小标题 | 5 | 5 | 4 | 5 | 6 |
| 标题带 emoji | 无 | 🚨 | 无 | 🚀 | 有 |
| 正文内嵌图 | ? | **4** | **6** | ? | **4** |
| 平均段长 | ? | ~13 词 | **16 词** | ? | **27 词** ← 唯一在区间外的一项 |
| 致谢 | 融进感谢句 | 2 句 ~7 机构 | 一行署名收尾 | 1 句 | **无**（见下） |
| 人称 | my group / we | we | we | we | we |

**只有 ExploitGym 与 How We Broke 两列是逐词数出来的**（作者把原文贴了进来）。带 `*` 的是
WebFetch 返回的**估计值，不可靠**：它把 ExploitGym 估成 ~350（实测 295）、把 How We Broke 估成
~1200（实测 732），并且看不到正文里的 `Article content` 图片占位符 —— 这份文档一度据此断言
「三篇参考正文都无内嵌图，本文 5 张是唯一的实质偏离」，**整句是错的**：两篇实测参考各有 4 张和
6 张，本文反而是偏少的那个。**引用任何一个带 `*` 的数字之前，先把原文贴进来数。**

字数不是偏离项：删掉致谢后本文 654 词，落在两篇实测参考（295 / 732）之间。真正在区间外的是
**段落密度** —— 参考 13–16 词/段，本文 27 词/段，24 段里有 7 段是多句的（最长 68 词）。
LinkedIn 正文栏窄，长段会糊成一块。**未处理**：要贴近参考就把这 7 段拆成短段，这只加换行、不丢内容。

**本文的句子几乎全部逐字取自 `twitter/01`（少数取自 `twitter/02`）。** 这是硬规矩，不是偏好：
同一个主张在两个平台上有两种措辞，改一处就会漂移一处——这份仓库的注记、门禁和封面已经因为这个
问题被修过很多轮。`twitter/01` 的经验表里就有这一条：**「手边有已通过审核的句子却另写一个」**。
初版 LinkedIn 稿 44 句里 0 句逐字沿用、28 句全新，正是那条经验的复发；重建后 33 句里 23 句逐字。

**如果觉得某句在 LinkedIn 上不够好，改 `twitter/01`，两边一起变** —— 不要在这里另写一个更好的版本。

| | 两篇参考的做法 | 本文 |
|---|---|---|
| 小标题 | Unicode 变体字符或 emoji 前缀 | **纯文本 `## 标题`，由发布者在编辑器里套 H2** —— 见下方「关于 Unicode 粗体」 |
| 标题句式 | 多为问句 | 用 `twitter/01` 的帖标题原文，本身已是主张句 |
| 开头 | 不写「我们做了 X」，先立利害；三篇都把产品名压到第二段之后 | `twitter/01` post 1 第二段原句。**但本文比三篇参考都早**：CUA-Lite 出现在导语第一段的第二句，不是第二段 —— 这是沿用 thread 原句的代价，记在这里，不假装它符合参考 |
| 图 | 封面 + 正文内嵌图（实测两篇：4 张 / 6 张） | 封面 + 4 张，与 ExploitGym 持平 |
| 链接 | 文末带标签清单 | **提到导语末尾**（第一个 `##` 之前），文末只留一行 Site · Code —— 见下 |
| 结尾 | 致谢 + 链接清单 | 致谢已删；链接已提到开头，文末只剩一行（见下） |
| hashtag | 两篇都没有 | 没有 |
| 人称 | `we` / `our` | `we`，与 `twitter/01` 一致 |

**关于 Unicode 粗体：本文不用。** 两篇参考的小标题是 MATHEMATICAL SANS-SERIF BOLD 字符
（`𝗔𝗟𝗘 𝗶𝘀 𝗯𝘂𝗶𝗹𝘁…`），那是 LinkedIn **post** 的将就——post 完全没有格式，只能靠字符伪装。
**article 有富文本编辑器，H1/H2/H3 是真的**，没有理由把 post 的将就带进来：Unicode 数学粗体
读屏软件会逐字符念出来，搜索和复制粘贴也会坏。本文小标题写成纯文本，发布时在编辑器里套 H2 ——
和 Twitter 包里「粗体在编辑器里点，不要粘星号」是同一条规矩。

**⚠️ `posts/README.md` 的平台表写着 LinkedIn 用「3–5 个英文标签」—— 那条是给 LinkedIn *post* 定的。**
Article 不适用，两篇参考都没有 hashtag。别把 post 的规矩回灌到 article。

**内嵌图不是偏离项。** 两篇实测参考正文各有 4 张和 6 张（`Article content` 占位符），本文 3 张，
是偏少的一侧。曾经这里写着「参考只有封面、本文是唯一偏离」，那是 WebFetch 读不到图片占位符造成的
误判 —— 见上方表格下的说明。

## 资产

`red/` 是唯一图片来源（见 `posts/README.md`），本目录 `assets/` 全是**逐文件软链**，不复制、**不裁切**；
只链英文版。

| 位置 | 文件 | 来源 | 744px 列下渲染高 |
|---|---|---|---|
| 封面 | `assets/00-cover.png` | 站点社交卡 `assets/og.png` | 391px |
| 📦 沙盒 | `assets/02-sandboxes.png` | `red/01` 同名图 | 653px |
| 🗂️ 数据 | `assets/03-data.png` | 同上 | 1181px |
| 📊 评测 | `assets/04-eval.png` | 同上 | 1350px |
| 🏋️ 训练 | `assets/05-train.png` | 同上 | 1054px |

> **封面必须横版。** LinkedIn article 的封面位按 ~16:9 居中裁切，`01b-cover.png` 是 2160×2880 的
> 3:4 竖版，放上去三行 bullet 和三台设备只会活下来一条。小红书 feed 是竖的所以那张在那边完美 ——
> 同一张图换个平台就不成立。`og.png`（2400×1260，1.90）是横的，不会被切。

**不要裁这些图。** 这一节曾经写着一套「按 744px 渲染高度决定去留、再按比例裁掉下半张」的政策，
`03-data` 裁到 0.47、`04-eval` 裁到 0.55，理由是「省滚动」。**作者看了成品直接否掉**：`red/01` 的图是
**完整海报**——`03 · EVAL` 眉标、Fraunces 大标题、导语、图本体，是一个自洽的版面；按比例砍掉下半张
会从卡片网格中间切过去，剩下的既不是海报也不是图表。整张放反而好看。

那套政策的根还是那个错误前提「三篇参考正文零图，所以放图的举证责任在我们这边」——两篇实测参考
正文各有 4 张和 6 张。**滚动成本不是不存在，但它换来的是完整版面，这笔账参考文章自己也是这么算的。**

**链接放在导语末尾，不在文末。** 两篇实测参考都把链接放末尾，这里不跟，理由作者说得明确：文章不像
Twitter 有推流惩罚，而开源项目要的是**点进去**；LinkedIn 长文会折叠，滚不到底的人拿不到链接。这和
thread 01 已经做过的决定同源 —— 顾问那条 engagement optimization 的批注，做法就是把链接和 CTA 提到
铺垫内容之前。文末保留一行 `Site · Code`，只是为了不让文章停在一张图上，不是第二份清单。

**已知的两处小出入**（不影响使用，记下来免得下次当成 bug 重查）：
- `05-train.png` 显示的是 SFT 那一栏，RL 只以切换钮的形式出现；正文那句承诺了 SFT 和 RL 两者。
- 图里印的是站点原文 `GRPO and beyond`，正文写的是 `GRPO, GSPO and beyond`（沿用 `twitter/01`）。
  站点当初刻意没加 GSPO。要统一就改正文，不要为此重截图。

## Pre-flight

1. **发布前把 `SFT and RL any agent` 的限定语核一遍。** 本文写的是 `any open agent` —— 闭权重模型
   不能微调或强化，站点代码里 `AGENTS.filter(a => !a.api)` 强制着这一点。thread 与站点上仍有几处
   漏了 `open`，不要从那些地方回抄。
2. **本文不带致谢**（作者定的）。上游署名仍在 `twitter/01` 的致谢帖和 `BIBTEX.md` 里 —— 要恢复
   就从那里抄，**不要重写**，那 38 个署名逐个查过一手来源。恢复时点机构与项目名，不点 @handle：
   Twitter 版那 38 个 @ 在 LinkedIn 上是坏文本。
3. **仓库仍无 LICENSE。** 本文四处说 open，发布前必须补上，否则 `open` 是唯一可被当场证伪的词。
4. 三个链接与 leaderboard 锚点发布当天重测。

---

## The article

**Title**

```
Introducing CUA-Lite: An Open Platform for Computer-Use Agents
```

**Cover** `assets/00-cover.png`

> **封面必须是横版。** LinkedIn article 的封面位按 ~16:9 居中裁切，`01b-cover.png` 是 2160×2880 的
> 3:4 竖版，放上去三行 bullet 和三台设备只会活下来一条。小红书 feed 是竖的所以那张在那边完美 ——
> 同一张图换个平台就不成立。横版的 `og.png`（2400×1260，1.90）是站点自己的卡，标题、三支柱一行
> 摘要、四个数字都在，形状正好。竖版那张改到正文开篇内嵌，article 正文图不限比例。

**Body**

```
Training and benchmarking CUAs (computer-use agents) takes three things: sandboxes, data, and a
framework. Today all three are fragmented:

- Sandboxes are heavy and unstandardized — a full VM per task, each with its own interface and
  action space
- Every dataset has its own schema, so one agent's data can't train another
- No framework standardizes eval, SFT or RL, so every project rebuilds the same tooling — agent
  loops, sandboxes setup, eval scripts and training infra

Today we introduce CUA-Lite: the open platform for computer-use agents. It standardizes and
democratizes all three: 30k+ verifiable tasks in light-weight VM-free sandboxes, 10+ SFT datasets,
and one unified framework for rollout, eval, SFT and RL across desktop, browser and mobile.

Sandboxes, data, and framework all keep growing. We hope CUA-Lite becomes a community-driven
open-source CUA ecosystem — bring your datasets, environments, or agents.

Site: https://cua-lite.github.io
Code: https://github.com/cua-lite/cua-lite
Data: https://huggingface.co/cua-lite
Leaderboard: https://cua-lite.github.io/#benchmarks


## 📦 VM-free sandboxes, with verifiable tasks

CUA-Lite introduces lightweight, VM-free sandboxes behind one interface: they reproduce public
benchmarks and generate verifiable tasks to train any agent, on a fraction of the hardware
resources.

Lite.OSWorld is the first of them: it reproduces OSWorld — the exact same tasks and evaluators —
in a Docker container instead of a VM. It needs no /dev/kvm and no nested virtualization, which
cloud instances, CI runners, and nested containers rarely provide — so it runs anywhere Docker
does, at under a quarter of the memory and cpu. Across 13 models its scores match the original
VM's.

The VM-free container isn't just for OSWorld — it's a base for CUA-Lite's family of sandboxes,
which carry 30k+ verifiable tasks so far. The tasks range from everyday browser and desktop work
to NASA's GMAT flying spacecraft and PyMOL turning proteins. Each sandbox runs many instances in
parallel on one machine.

Four sandboxes share that base today, each re-hosting a public suite:

- Lite.OSWorld — OSWorld's 369 benchmark tasks plus 2k+ synthesized
- Lite.ScaleCUA — 20k+ tasks perturbed from OSWorld's evals
- Lite.CUAGym — browser and desktop tasks across mock sites and real apps
- Lite.CUAWorld — 40 professional apps across ~25 expert domains

[assets/02-sandboxes.png]


## 🗂️ One schema, any dataset

LiteSample is CUA-Lite's data schema, shared across every platform (desktop, browser, mobile),
environment, agent and task type — convert a dataset once, and every agent can train on it.

CUA-Lite has converted 10+ SFT datasets into LiteSample so far, plus fresh rollouts from frontier
CUAs. An adapter per model then packs a unified LiteSample into the exact training format each one
needs — so any model's rollouts can fine-tune any other.

[assets/03-data.png]


## 🔁 One framework: eval, SFT, RL

lite.gym is CUA-Lite's one agent–environment interface, so any agent can run in any environment.
You bring the agent; CUA-Lite ships the rollout loop, the sandboxes to run it in, and the eval and
training stack that consumes the rollouts.

The rollouts lite.gym produces are reused three ways:

- Eval — scored by the benchmark's own evaluators, unchanged
- SFT — rendered by each model's adapter into that model's own training format
- RL — scored by the task's own verifiable reward, and those scores drive the RL updates


## 📊 One command, any benchmark

15+ benchmarks are already integrated into CUA-Lite, and the leaderboard is live — every score on
it is a run we did ourselves.

- Desktop — OSWorld, OSWorld-2, WindowsAgentArena, Cua-Bench
- Browser — WebArena, VisualWebArena, WebVoyager, Online-Mind2Web, MiniWoB, WebGym
- Mobile — AndroidWorld, AndroidLab, MobileWorld, MobileGym
- Grounding — ScreenSpot-Pro, OSWorld-G

A unified action space per platform means one script evals any agent on any of them — set
--model-id and its config for the agent, --env-id for the benchmark.

[assets/04-eval.png]


## 🏋️ SFT and RL, any open agent

SFT on CUA-Lite's public rollout data, then reinforce in its envs — GRPO, GSPO and beyond, built
on Slime. Train any open agent on any data and any env.

[assets/05-train.png]


Site: https://cua-lite.github.io · Code: https://github.com/cua-lite/cua-lite
```

## 注记

**开头不写「我们做了 X」** —— 两篇参考都先立利害再介绍。本文第一段说三样东西各自为政、每组都要重造
同一套 tooling，第二段才出现 CUA-Lite。

**`Does a cheap copy change the answer?`** 是全文唯一的问句小标题，位置在四个支柱讲完之后 —— 参考里
问句用来做转折（`Why do ALE's results look different…`），不用来开头。

**parity 的写法** 与站点、博客、Twitter 一致：`gives the same result as the original virtual machine`，
定性不给聚合数。精确值（mean|Δ|≈2.7 / worst 5.0）内部核对，任何平台正文都不写。

**`any open agent` 的限定语** 在「One framework」节末尾明确写出。站点 hero 与 thread 有几处漏了这个词，
这里不跟随 —— 代码里 `AGENTS.filter(a => !a.api)` 强制着这个约束。

**致谢已从本文删除**，链接清单成为结尾。作者的判断是四个链接放最后更重要。**记下代价**：两篇实测
参考都带致谢（ExploitGym 2 句 7 机构，How We Broke 一行署名），而 LinkedIn 是上游作者最可能刷到的
一面，本文对 OSWorld / CUA-Gym / Slime 等 20 个上游项目 0 处致谢。要恢复，逐字抄 `twitter/01` 的
致谢帖 —— 机构名取自 `posts/twitter/01/BIBTEX.md` 里各上游 README 的 `author` 字段，不看仓库顶上的
链接；点机构与项目名，不点 @handle。
