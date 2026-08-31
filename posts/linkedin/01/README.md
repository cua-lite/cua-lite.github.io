# CUA-Lite — LinkedIn article 01

LinkedIn 的**长文（Pulse article）**，不是 post。两者不是同一个载体：post 有折叠线、吃 hashtag、
一图一帖；article 是一篇有标题、封面和小标题的文章，靠结构读完，不靠钩子截停。

**参考的三篇**（作者给定，均为 Dawn Song 的 Pulse 文章）：*Introducing Agents' Last Exam (ALE)*、
*Can AI agents turn security vulnerabilities into real attacks?*、*Introducing OpenSage*。
从它们身上抄的是**结构**，不是句子。

三篇一致的地方（样本小，但一致性本身是信号）：

| | ALE\* | ExploitGym | How We Broke… | OpenSage\* | 本文 |
|---|---|---|---|---|---|
| | ALE | ExploitGym | How We Broke | **本文** | |
|---|---|---|---|---|---|
| 词数 | 858 | 281 | 710 | **744** | ✅ |
| 小标题数 | 5 | 5 | 7 | 4 | ✅ |
| 小标题带 emoji | 0/5 | **5/5** | 0/8 | 4/4 | ✅ 同 ExploitGym |
| 散文段数 | 22 | 15 | 35 | 27 | ✅ |
| 平均段长 | 35.7 词 | 17.0 | 15.9 | ~24 | ✅ |
| 最长段 | 74 词 | 24 | 63 | 61 | ✅ |
| 正文内嵌图 | 6 | 4 | 6 | 4 | ✅ **四节四图，一一对应** |
| **导语里的图** | 1 | 2 | 1 | **0** | ❌ 三篇都在开头插图 |
| **第一张图前的词数** | 236 | 63 | 117 | **299** | ❌ 超上限 27% |
| 清单段数 / 行数 | 3 / 13 | 0 / 2 | 2 / 9 | **7 / 27** | ❌ 2 倍以上 |
| emoji 总数 | 0 | 7 | 0 | **13** | ❌ 多出的 8 个是清单行首 |
| 箭头 `→` | 5 | 0 | 1 | **11** | ❌ |
| 链接块 | 1（文末） | 1（文末） | 1（文末） | **2（导语 + 文末）** | ⚠️ 作者定的，见下 |
| 致谢 段/词 | 2 / 106 | 2 / 44 | **0 / 0** | **0 / 0** | ⚠️ 同 How We Broke，作者定 |
| 产品名首次出现 | 第 2 段 | 第 2 段 | 第 41 段 | 第 6 个散文段 | ⚠️ |
| 署名行 | 无 | 无 | 有 | 无 | ✅ |
| hashtag | 0 | 0 | 0 | 0 | ✅ |
| 人称 | my group / we | we | we | we | ✅ |

> **以上为实测**（2026-08-30，三篇原文带 UA 全文抓取 + 逐块解析，词数两种方法交叉验证）。
> ⚠️ 早先这张表的数是**估的**（`~1800 / 295 / 732 / ~650`），还断言过「参考正文零图」——
> 那是 WebFetch 读不到 `Article content` 占位符造成的误判（实为 6 / 4 / 6 张）。
> **改这张表之前先重新抓，不要凭印象。**

**只有 ExploitGym 与 How We Broke 两列是逐词数出来的**（作者把原文贴了进来）。带 `*` 的是
WebFetch 返回的**估计值，不可靠**：它把 ExploitGym 估成 ~350（实测 295）、把 How We Broke 估成
~1200（实测 732），并且看不到正文里的 `Article content` 图片占位符 —— 这份文档一度据此断言
「三篇参考正文都无内嵌图，本文 5 张是唯一的实质偏离」，**整句是错的**：两篇实测参考各有 4 张和
6 张，本文反而是偏少的那个。**引用任何一个带 `*` 的数字之前，先把原文贴进来数。**

字数不是偏离项：删掉致谢后本文 654 词，落在两篇实测参考（295 / 732）之间。真正在区间外的是
**段落密度** —— 参考 13–16 词/段；本文实测（2026-08-30 重排后）见下方脚本口径。LinkedIn 正文栏窄，
长段会糊成一块。重排时 Lite.OSWorld 那段一度撑到 90 词，已拆成三段（只加换行、不丢内容）。
**这是每次改正文都要重量的数，不要手写。**

**本文的句子几乎全部逐字取自 `twitter/01`（少数取自 `twitter/02`）。** 这是硬规矩，不是偏好：
同一个主张在两个平台上有两种措辞，改一处就会漂移一处——这份仓库的注记、门禁和封面已经因为这个
问题被修过很多轮。`twitter/01` 的经验表里就有这一条：**「手边有已通过审核的句子却另写一个」**。
初版 LinkedIn 稿 44 句里 0 句逐字沿用、28 句全新，正是那条经验的复发；重建后 33 句里 23 句逐字。

**如果觉得某句在 LinkedIn 上不够好，改 `twitter/01`，两边一起变** —— 不要在这里另写一个更好的版本。

| | 两篇参考的做法 | 本文 |
|---|---|---|
| 小标题 | 两种都有：ALE 是带立场的主张句，ExploitGym 是 emoji 前缀 + 短标题 | **直接用 `twitter/01` 的帖标题**（去掉 `[N/10]`）+ 一个 emoji 前缀。⚠️ 我曾把五条全改写成「更有立场」的句子（`One schema, instead of one per dataset` 之类），**那是错的**：thread 的标题本来就是主张句，而且是 `one X, any Y` 句式 —— 那是站点自己的标语形状（`one schema, one interface, one command`），改掉等于丢掉项目的节奏换一句更普通的话，格式上也没有依据（ALE 的标题正是这个家族）。**唯一的例外是 `📦`**：那一节由 posts 7+8 合并。曾取 post 7 的 `VM-free OS(World) at Scale`，作者改成 **`VM-free sandboxes, with verifiable tasks`** —— 两条的词都在（`VM-free` 来自 post 7，`sandboxes` + `verifiable tasks` 来自 post 8），比挑一个盖不住的强；代价是丢掉 `OS(World)` 的双关 |

| 开头 | **先制造张力，产品名压后**。ALE：`Everyone says … But is that really the case?`；How We Broke：`We built an AI agent that achieved near-perfect scores on eight major AI benchmarks. It never solved a single task.` | 加了一段 article 专属的钩子（断言 + 问句），thread 里没有对应物 —— X 的 post 1 本身就是钩子，而 article 有真标题在上面，正文第一句本来空着。**钩子里不许出现 CUA-Lite，也不许剧透后面四条碎片化** —— 试过一次「No shared interface. No shared trace format. No shared training stack.」，紧接着正文又列四样，读起来是自我重复 |
| 图 | 封面 + 正文内嵌图（实测两篇：4 张 / 6 张） | 封面 + 4 张，与 ExploitGym 持平 |
| 链接 | 文末带标签清单 | **提到导语末尾**（第一个 `##` 之前），文末只留一行 Site · Code —— 见下 |
| 结尾 | **CTA + 链接**，不是裸链接。ALE：`Come test your agent on ALE → Website: …`；How We Broke：`Stop trusting scores. Start auditing evaluations. Full writeup: …` | 同形：`… and plug it into CUA-Lite →` 接一行 Site · Code。致谢已删（作者定），代价见下 |
| hashtag | 两篇都没有 | 没有 |
| 人称 | `we` / `our` | `we`，与 `twitter/01` 一致 |
| 段落 | 短到中等，2–4 句 | 实测 23 词/段、最长 55（参考 13–16），偏长一档但同量级 |

**关于 Unicode 粗体：本文不用。** 两篇参考的小标题是 MATHEMATICAL SANS-SERIF BOLD 字符
（`𝗔𝗟𝗘 𝗶𝘀 𝗯𝘂𝗶𝗹𝘁…`），那是 LinkedIn **post** 的将就——post 完全没有格式，只能靠字符伪装。
**article 有富文本编辑器，H1/H2/H3 是真的**，没有理由把 post 的将就带进来：Unicode 数学粗体
读屏软件会逐字符念出来，搜索和复制粘贴也会坏。本文小标题写成纯文本，发布时在编辑器里套 H2 ——
和 Twitter 包里「粗体在编辑器里点，不要粘星号」是同一条规矩。

**⚠️ `posts/README.md` 的平台表写着 LinkedIn 用「3–5 个英文标签」—— 那条是给 LinkedIn *post* 定的。**
Article 不适用，两篇参考都没有 hashtag。别把 post 的规矩回灌到 article。

**「article 有篇幅」不是往里加东西的理由。**（作者 2026-08-30 驳回）
我曾从 VM-free 博客搬了一句 VM 税解释进 `📦`（`OSWorld's faithful desktop is a full VM per task…`），
理由就是这个。作者的问题一针见血：**「twitter 里面没有啊」**。查下来它是那一节里 VM 对照的**第三遍**——
¶2 已有 `in a Docker container instead of a VM` 和 `No /dev/kvm, so it runs anywhere Docker does`。
**篇幅富余时的正确用法是让段落更短、让图有地方呼吸，不是把上游没有的论证补进来。**
唯一还留着的非 thread 正文句是 `Across 13 models, Lite.OSWorld's scores match the OSWorld VM's.`
（取自博客）—— 它是全文唯一的硬证据，thread 把它放在 post 7 的回复里，article 没有回复位可用。
这一条同样待作者裁定。

**X 能靠折叠藏住冗余，LinkedIn 不能 —— 这是两个平台最大的结构差异。**（作者 2026-08-30 定）
`twitter/01` 的写作规约 6 原话是「**跨帖重复无所谓**，首屏内重复是致命的……没人读完九条，
重复反而是好事」——那条成立的前提是每帖独立折叠、多数人只看到一条。同一批句子搬进一篇线性文章，
前提就没了：post 1 和 post 5 在 X 上隔八条，在这里隔十几行。
**判据：把 thread 逐句搬过来之后，必须再做一遍「同一主张说了几遍」的检查**，
只保留最靠前、语境最合适的那一遍。已删的三重之一：
`The result: one agent's rollouts can train any other agent.` —— 同节 ¶1 的
`Convert a dataset once, and any agent can train on it.` 已经说了，导语的
`Agent traces come in incompatible formats, so one agent's rollouts can't train another.`
则是它的反面。在 X 上这三句分属 post 1 与 post 5，各自成立。
⚠️ 注意别把**术语一致**误判成冗余：`environment` / `sandbox` / `verifiable task` / `trace` 这些词
按规约必须全线同名，反复出现是对的，冗余指的是**同一个主张**说了两遍。

**每个小节必须有自己的配图，否则它多半是导语已经讲完的东西。**（作者 2026-08-30 定）
`🔁 One unified framework…` 那节被删掉，就是因为它是五节里**唯一没有配图**的 ——
而它讲的「一个接口 / eval·SFT·RL 三用」，导语的 `CUA-Lite unifies the stack:` 四条已经说完。
**没有资产 = 没有独立存在的理由**，这个判据比「读起来重不重复」好用，因为它可机器检查。
代价记下来：`Lite.Gym` 这个名字和「one rollout, three uses」的展开随之消失，只在
`twitter/01` 的 post 4 里有；本文少 108 词 → 744 词，四节四图一一对应。

**`📦` 那节由 posts 7+8 合成，顺序必须是 thread 自己的：贡献 → 例子 → 推广 → 清单。**
LinkedIn 多出来的两块（VM 税细节、13 模型 parity）插在贡献之后当补充，**不动主线**。
⚠️ `optional` 必须活下来（框架不绑定我们的沙盒），它在第一句。

⚠️ **我在这一节上连错两次，都是同一个病：把「合并」当成了「可以重写」。**
第一次直接首尾相接，两条各自的总述都留着，读起来是赘述。第二次为了修它把结构改成
`问题 → 解法 → 证据 → 推广`，理由是「给这一节一条单一主线」—— 听上去像方法论，
但那**违反写作规约 5「痛点占一句，不占一段，而且放在贡献之后」**，把整节变成「OSWorld 有什么毛病」
而不是「我们提供了什么」；而且当时判定的「总述说了两次」也是错的：第一段是「我们提供 VM-free 沙盒」
（供给），第五段是「这个容器是一个家族的基座」（规模化），**两个不同的主张**。
**判据：合并只允许删掉真正重复的连接词，不允许重排两条帖子的内在顺序。**

**三篇参考的格式（2026-08-30 逐篇实测，不要再凭印象改这一节）：**

| | ALE | How We Broke | ExploitGym |
|---|---|---|---|
| 小标题 | Unicode 粗体主张句/问句 | 纯文本短句（`What we actually did`） | **emoji 前缀 + 短标题**（🚨🔬📊⚠️🛡️🙏） |
| 开头 | 常识 + 反问（`But is that really the case?`） | 断言 + 反转（`It never solved a single task.`） | 重要性 + `Today, we're excited to share X` |
| 产品名 | 第 2 段 | 第 1 段 | 第 2 段 |
| emoji | 仅 `→` | **零** | 大量 |
| 结尾 | CTA + 链接 + 致谢 | 断言对 + 链接 + 署名 | **致谢 + 📄 Paper / 📝 Blog** |
| 致谢 | 有 | 有（署名行） | **有，独立小节 `🙏 Acknowledgments`** |
| 段落 | 1–2 / 2–4 句 | 2–4 句 | 1–3 句 |

结论三条：① **emoji 小标题有先例**（ExploitGym），不必清零；② **三篇都有致谢，我们曾经零个** ——
现在补了 `🙏 Acknowledgements` 一节，名字取自 `twitter/01` 的致谢帖，按 Pre-flight 2 的规矩
**点机构与项目名、不点 @handle**；③ 开头必须先制造张力、产品名压后。

**内嵌图不是偏离项。** 两篇实测参考正文各有 4 张和 6 张（`Article content` 占位符），本文 4 张，
与 ExploitGym 持平（早先这里写「3 张」，和上面的表自相矛盾）。曾经这里写着「参考只有封面、本文是唯一偏离」，那是 WebFetch 读不到图片占位符造成的
误判 —— 见上方表格下的说明。

## 资产

`red/` 是唯一图片来源（见 `posts/README.md`），本目录 `assets/` 全是**逐文件软链**，不复制、**不裁切**；
只链英文版。

| 位置 | 文件 | 来源 | 744px 列下渲染高 |
|---|---|---|---|
| 封面 | `assets/cover.png` | 站点社交卡 `assets/og.png` | 391px |
| 🗂️ 格式 | `assets/data.png` | `red/01` 同名图 | 1181px |
| 📊 评测 | `assets/eval.png` | 同上 | 1350px |
| 📦 沙盒 | `assets/sandboxes.png` | 同上 | 653px |
| 🏋️ 训练 | `assets/train.png` | 同上 | 1054px |

> **资产按主题命名，不按位置编号。** 原来叫 `00-cover / 02-sandboxes / 03-data / 04-eval /
> 05-train` —— 那串数字编的是**主页**四支柱的位置（`red/01/capture_sections.py` 按主页锚点截的），
> 本文按 `twitter/01` 的叙事重排后就对不上了：正文里图的顺序是 03 → 04 → 02 → 05。
> **数字前缀每次重排都会烂，而且会悄悄让所有散文引用失效** —— 这条教训 `twitter/01` 已经吃过一次
> （素材重命名后，接缝表和「犯过的错」里所有按编号的引用全部指错）。软链现在叫
> `cover / data / eval / sandboxes / train`；目标文件保留 `red/01` 的原名，出处不丢。
> `🔁 框架`那一节没有图，因为主页没有对应 section —— 也正因为如此它被删了（见下）。

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


## Deviations

**每一句不逐字来自 `twitter/01` 或博客的话，都必须列在这里，带理由。** `make_package.py` 的
`provenance()` 强制这一点 —— 不是警告，是构建失败。判据：**形式**（小标题样式、列表符号、段落长度、
钩子、结尾形状、emoji）可以按 LinkedIn 参考改；**内容**（顺序、措辞、论证）只能改 `twitter/01`，两边一起变。

### 作者本人改写的导语与收尾（2026-08-30，Google Doc 往返）

这篇以 **Dawn Song 的名义**发（末句「my PhD student Zhanhui Zhou」），所以导语和收尾是作者自己的语域，
不是 thread 的搬运。以下各句 thread 里没有对应物：

- `Introducing CUA-Lite - an open platform for computer-use agents.` —— 回到 thread post 1 的钩子形状，
  但 article 有 H1 标题在上面。作者取舍：宁可重复，也要第一行就点名。
- `Agents - the models and the scaffolding that drives them` —— `scaffolding`（thread 用 `harness`）。
- `Every agent ships with its own implementation, often in a separate repo, so there is no unified way to run them all.`
- `Every environment exposes its own interface and action space, often requiring an expensive VM sandbox for each verifiable task.`
- `Traces come in incompatible formats.`
- `And without common standards across the stack, every project ends up rebuilding its own tooling for eval, SFT, and RL.`
  以上四句是碎片化段的作者版：比 thread 更短，四句仍一一对应 1️⃣–4️⃣。
- `10+ CUAs, including GPT, Claude, Gemini, Qwen, Muse-Glimmer, UI-TARS` —— **⚠️ `Muse-Glimmer` 在主干里不存在**
  作者确认它存在，只是还在另一个分支，会随后合并 —— **`factory.py` 与站点当前 0 命中是预期的，
  不要再当成事实错误报上来。**
- `Optional VM-free sandboxes with 30K+ verifiable tasks for training` —— 句尾加了 `for training`。
- 小标题 `🏋️ SFT and RL, any open agent` —— thread 是 `SFT & RL`；作者在 article 里用 `and`。
- `Led by Berkeley RDI (rdi.berkeley.edu), our goal is for CUA-Lite to become a community-driven,
  open-source ecosystem for computer-use agents.` —— 机构归属，thread 没有。
- `Huge thanks to my PhD student Zhanhui Zhou for spearheading the project!` —— 署名句，article 专属。

- 小标题 `📦 VM-free sandboxes, with verifiable tasks` —— `📦` 由 thread 的 posts 7+8 合并，
  两条的标题各自只盖一半（post 7 `VM-free OS(World) at Scale` 只讲 OSWorld，post 8
  `Sandboxes & verifiable tasks` 不含 VM-free）。这一条是两者的词合成的，是「小标题必须逐字沿用
  thread 帖标题」的**唯一例外**。

### 结构上作者定的三件（与 thread 不同，不是漂移）

- **链接移到文末**（原来在导语末尾）。三篇参考都只有文末一处链接块，这一版跟了参考。
- **`🔁 One unified framework` 那节删除** —— 它是唯一没有配图的一节，讲的东西导语的
  `CUA-Lite unifies the stack:` 四条已经说完。**没有资产 = 没有独立存在的理由。**
- **不带致谢节** —— 三篇参考里 How We Broke 也没有。代价见「注记」。


### Post = `twitter/01` 的 post 1，四处最小改动

**post 不是新写的稿子，是 post 1 原样搬过来。**（作者 2026-08-30 定：「主要还是参考 twitter 第一个
thread 就行；然后适当做一些 minimal 调整」。）我曾按 Dawn Song 那两条参考重写过一版 222 词的
—— 那是把「参考格式」又做成了「重写内容」，同一个错犯第二次。**参考决定形状，不决定文字。**

逐字比对，只有四处不同：

- 去掉 `🧵` —— 那是 X 的 thread 信号（「下面还有」），LinkedIn 上没有下文。
- `Our goal is …` → `Led by Berkeley RDI, our goal is …` —— 机构归属，**位置不动**（仍在 CTA 之前，
  和 post 1 一样；曾把它缀到 CTA 之后，愿景和邀请就倒过来了）。
- `Led by Berkeley RDI, our goal is for CUA-Lite to become a community-driven, open-source ecosystem for computer-use agents.`
- 末尾加链接：四个项目链接**和 post 2 同序同标签**（Site / Code / Data / Leaderboard），
  再单起一行 `Article: [TODO: link to the article]`。
  **占位符必须是 `[TODO: …]`，不能放一个能打开的临时 URL。** 我原来填的是
  `blog/why-cua-lite/` —— 那是个真能打开的地址，最容易就这么发出去而没人发现它本该被替换。
  另外 LinkedIn 的卡片取**最后一个 URL**：`[TODO]` 不是 URL，所以卡片来自 Leaderboard 那条
  （和 post 2 刻意选的一样）；填上 article 链接后卡片会变成 article 自己的。
- 末尾加 `Huge thanks to my PhD student Zhanhui Zhou for spearheading the project!` —— 署名句。

**长度**：310 词，Dawn Song 那两条实测是 316 / 279 —— 在区间内。两条都**没有 hashtag、没有 @、
链接一律在末尾**，本条一致。
⚠️ **`Full write-up` 现在指向 `blog/why-cua-lite/`。article 发布后要换成它自己的 LinkedIn URL。**


## Pre-flight

0. **`POST.md` 里的 `Article: [TODO: link to the article]` 必须先发 article、拿到它的 LinkedIn URL 再填。**
   顺序是：先发 article → 复制它的链接 → 填进 README 的 **Post** 块 → 重跑生成器 → 再发 post。
1. **发布前把 `SFT and RL any agent` 的限定语核一遍。** 本文写的是 `any open agent` —— 闭权重模型
   不能微调或强化，站点代码里 `AGENTS.filter(a => !a.api)` 强制着这一点。thread 与站点上仍有几处
   漏了 `open`，不要从那些地方回抄。
2. **本文不带致谢**（作者定的）。上游署名仍在 `twitter/01` 的致谢帖和 `BIBTEX.md` 里 —— 要恢复
   就从那里抄，**不要重写**，那 38 个署名逐个查过一手来源。恢复时点机构与项目名，不点 @handle：
   Twitter 版那 38 个 @ 在 LinkedIn 上是坏文本。
3. **仓库仍无 LICENSE。** 本文四处说 open，发布前必须补上，否则 `open` 是唯一可被当场证伪的词。
4. 三个链接与 leaderboard 锚点发布当天重测。

---

**Post**

```
Introducing CUA-Lite — an open platform for computer-use agents.

Training and benchmarking CUAs (Computer-Use Agents) requires four core pieces:

1 · Agents — the models and the harness that drives them
2 · Environments — runtime/sandboxes for agents to interact with, tasks & verifiers/graders
3 · Traces — records of agent trajectories
4 · Frameworks — to evaluate, SFT & RL-train agents

Today, all four are fragmented.

Every agent ships its own official implementation in its own repo, so there is no one place to run them all. Every environment exposes its own interface and action space, and often needs a full VM for every verifiable task. Agent traces come in incompatible formats, so one agent's rollouts can't train another. And because none of it is standardized, every project ends up rebuilding its own eval, SFT, and RL framework.

CUA-Lite unifies the stack:
→ One standardized interface & action space for agents and environments
→ One standardized format for agent traces
→ One framework for evaluation, SFT & RL
→ Across desktop, browser & mobile

And open resources plug straight in, creating the largest open collection of CUA agents, environments and traces, all in a unified format:
🤖 10+ CUAs, including GPT, Claude, Gemini, Qwen & UI-TARS
🌐 15+ benchmarks, including OSWorld, WebArena & AndroidWorld
⚡ Optional VM-free sandboxes with 30K+ verifiable tasks
📚 10+ trace datasets, freely available on Hugging Face, including public datasets converted into the standardized format and fresh rollouts from frontier CUAs

Led by Berkeley RDI, our goal is for CUA-Lite to become a community-driven, open-source ecosystem for computer-use agents.

Join the community and contribute today: bring an environment (runtime/sandbox + tasks + verifier), traces, or an agent, and plug it into CUA-Lite!

Site: https://cua-lite.github.io
Code: https://github.com/cua-lite/cua-lite
Data: https://huggingface.co/cua-lite
Leaderboard: https://cua-lite.github.io/#benchmarks

Article: [TODO: link to the article]

Huge thanks to my PhD student Zhanhui Zhou for spearheading the project!
```

> **写给谁、多长** —— 参考 Dawn Song 的两条实测：ExploitGym 316 词、Vero 279 词，**都没有 hashtag、
> 没有 @，链接一律在末尾**。Vero 用 `•` 列要点，ExploitGym 是纯散文。本条 ~250 词，取 Vero 的形状：
> 钩子 → 我们发布了什么 → `•` 四条具体数字 → 归属与 CTA → 链接。
> **Post 不是 article 的摘要，是它的引子** —— 每条要点都给一个数字，读者不点进去也拿到了东西。

## The article

**Title**

```
Introducing CUA-Lite: An Open Platform for Computer-Use Agents
```

**Cover** `assets/cover.png`

> **封面必须是横版。** LinkedIn article 的封面位按 ~16:9 居中裁切，`01b-cover.png` 是 2160×2880 的
> 3:4 竖版，放上去三行 bullet 和三台设备只会活下来一条。小红书 feed 是竖的所以那张在那边完美 ——
> 同一张图换个平台就不成立。横版的 `og.png`（2400×1260，1.90）是站点自己的卡，标题、三支柱一行
> 摘要、四个数字都在，形状正好。竖版那张改到正文开篇内嵌，article 正文图不限比例。

**Body**

```
Introducing CUA-Lite — an open platform for computer-use agents.

Training and benchmarking CUAs (Computer-Use Agents) requires four core pieces:

1️⃣ Agents — the models and the scaffolding that drives them
2️⃣ Environments — runtime/sandboxes for agents to interact with, tasks & verifiers/graders
3️⃣ Traces — records of agent trajectories
4️⃣ Frameworks — to evaluate, SFT & RL-train agents

Every agent ships with its own implementation, often in a separate repo, so there is no unified
way to run them all. Every environment exposes its own interface and action space, often requiring
an expensive VM sandbox for each verifiable task. Traces come in incompatible formats. And without
common standards across the stack, every project ends up rebuilding its own tooling for eval, SFT,
and RL.

CUA-Lite unifies the stack:

→ One standardized interface & action space for agents and environments
→ One standardized format for agent traces
→ One framework for evaluation, SFT & RL
→ Across desktop, browser & mobile

And open resources plug straight in, creating the largest open collection of CUA agents,
environments and traces, all in a unified format:

🤖 10+ CUAs, including GPT, Claude, Gemini, Qwen, Muse-Glimmer, UI-TARS
🌐 15+ benchmarks, including OSWorld, WebArena & AndroidWorld
⚡ Optional VM-free sandboxes with 30K+ verifiable tasks for training
📚 10+ trace datasets, freely available on Hugging Face, including public datasets converted into
   the standardized format and fresh rollouts from frontier CUAs


## 🗂️ One schema, any dataset, any agent

LiteSample is CUA-Lite's unified data schema across desktop, browser, and mobile — spanning
environments, agents, and task types. Convert a dataset once, and any agent can train on it.

CUA-Lite has 10+ datasets on Hugging Face in LiteSample — public SFT datasets it converted,
alongside fresh rollouts from frontier CUAs. A lightweight model adapter then transforms each
LiteSample into the exact training format each model expects.

The result: one agent's rollouts can train any other agent.

[assets/data.png]


## 📊 One command, any benchmark

10+ CUAs and 15+ benchmarks are already integrated into CUA-Lite's unified framework, and the
leaderboard is live, with every score on it a run we did ourselves.

🖥️ Desktop: OSWorld, Lite.OSWorld, OSWorld-2, WindowsAgentArena, CUABench
🌐 Browser: WebArena, VisualWebArena, WebVoyager, Online-Mind2Web, MiniWoB, WebGym
📱 Mobile: AndroidWorld, AndroidLab, MobileWorld, MobileGym
🎯 Grounding: ScreenSpot-Pro, OSWorld-G

One command evaluates any agent on any benchmark: set --model-id (plus its agent config) and
--env-id for the benchmark — and run.

[assets/eval.png]


## 📦 VM-free sandboxes, with verifiable tasks

CUA-Lite also provides optional VM-free sandboxes for hosting environments — lightweight, highly
optimized containers that reproduce public benchmarks and support verifiable tasks for training
any agent.

Lite.OSWorld is the first: it reproduces OSWorld with the same tasks and evaluators, but runs in a
Docker container instead of a VM. No /dev/kvm, so it runs anywhere Docker does — using less than ¼
the memory and CPU resources.

Across 13 models, Lite.OSWorld's scores match the OSWorld VM's.

The VM-free container isn't just for OSWorld — it's the foundation for CUA-Lite's family of
sandboxes, already supporting 30K+ verifiable tasks and verifiers.

Tasks range from everyday browser and desktop workflows to NASA's GMAT for spacecraft missions and
PyMOL for molecular exploration and analysis, enabling many sandbox instances running in parallel
on a single machine.

Four sandbox families share this foundation today, each re-hosting or extending public suites:

→ Lite.OSWorld: OSWorld's 369 benchmark tasks + 2K+ synthesized tasks
→ Lite.ScaleCUA: 20K+ ScaleCUA training tasks on the same desktop
→ Lite.CUAGym: browser + desktop tasks across mock sites and real apps
→ Lite.CUAWorld: 40 professional applications across ~25 expert domains

[assets/sandboxes.png]


## 🏋️ SFT and RL, any open agent

SFT on CUA-Lite's public rollout data, then RL in its environments — GRPO, GSPO, and beyond, built
on Slime. Train any open agent on any data, in any environment.

[assets/train.png]


Led by Berkeley RDI (rdi.berkeley.edu), our goal is for CUA-Lite to become a community-driven,
open-source ecosystem for computer-use agents.

Join the community and contribute today: bring an environment (runtime/sandbox + tasks + verifier),
traces, or an agent, and plug it into CUA-Lite!

Site: https://cua-lite.github.io
Code: https://github.com/cua-lite/cua-lite
Data: https://huggingface.co/cua-lite
Leaderboard: https://cua-lite.github.io/#benchmarks

Huge thanks to my PhD student Zhanhui Zhou for spearheading the project!
```

## 注记

**开头不写「我们做了 X」** —— 两篇参考都先立利害再介绍。本文第一段说三样东西各自为政、每组都要重造
同一套 tooling，第二段才出现 CUA-Lite。

**叙事顺序与 `twitter/01` 一致：框架先行，开放资源随后**（2026-08-30 对齐）。三样东西是
`environments (sandbox, tasks, verifier)` / `traces` / `framework`，三个 gap 按**回答的顺序**列
（framework → traces → sandboxes），五个小节也按这个顺序：
`🗂️ 格式 → 📊 榜单 → 📦 沙盒 → 🏋️ SFT/RL`（`🔁 框架`那节已删，见下）。
理由取自 `twitter/01`：这条文案的真实诉求是招贡献者，而**没有接口就没法贡献环境，没有格式就没法贡献轨迹** ——
所以先给让生态成立的那层，沙盒和轨迹是这层「接进开放资源」的两个例子。
代价照抄那边的记录：最硬的证据（13 模型 parity、footprint）从第一节退到第四节，
`📊 One command` 因此提前，让读者在两节抽象之后立刻拿到一个具体结果。
**旧顺序（沙盒 → 数据 → 框架）不要再回来** —— 站点和两篇博客暂时仍是旧序，那是**待办**，不是依据。

**术语跟 `twitter/01` 走**：`traces` / `trace format`，不写 `data` / `dataset` / `schema`（作者的理由：
verifiable task 和 grader 也是 data，`data` 有歧义）；管线那层叫 `framework` 不叫 `pipeline`；
沙盒一律带 `also provides` + `optional` —— 少了任何一个都会读成「我们只支持 VM-free」，作者驳回过一次。

**parity 的写法**取博客原句：`Across 13 models, Lite.OSWorld's scores match the OSWorld VM's.`
精确值（mean|Δ|≈2.7 / worst 5.0）内部核对，任何平台正文都不写。早先这里写的是
`gives the same result as the original virtual machine`，博客已不这么写了。

**`any open agent` 的限定语**在 `🏋️ SFT & RL, any open agent` 的标题和正文里各出现一次。
站点 hero 与 thread 有几处漏了这个词，这里不跟随 —— 代码里 `AGENTS.filter(a => !a.api)` 强制着这个约束。

**逐字沿用的实测（2026-08-30 二次同步后）：正文 31 句里 25 句逐字取自 `twitter/01`，1 句逐字取自
VM-free 博客，其余 5 句各只有一处偏离**，都记在这里，免得下次当成漏抄：
- **`fresh rollouts from frontier CUAs`** —— `twitter/01` 的 post 5 当前写的是 `frontier
  **open-weight** CUAs，**那是假的**（`cua-lite/README.md:246` 写着「(GPT-5.5 rollouts)」，五个
  rollout 数据集全出自闭权重模型），而同一条 thread 的 post 1 已经改回 `frontier CUAs`。
  **这里跟 post 1，不跟 post 5。** 等 post 5 修好后这条注记删掉。
- `Contribute today: …` ×2 —— thread 里是 `Join the community and contribute today: …!` 和句尾的
  🚀；LinkedIn 去掉感叹号和 emoji，article 的语域不同。
- `OSWorld's faithful desktop is a full VM per task**:** it needs …` —— 博客是句号，这里改成冒号并句。
- `No /dev/kvm, so **Lite.OSWorld** runs anywhere Docker does, using less than **a quarter** of the
  memory and CPU` —— 博客原文主语是 `it`，本文前面插了一句讲 OSWorld 的话，代词会指错，所以点名；
  thread 用的 `¼` 符号在 article 里拼成单词。

**致谢已从本文删除**，链接清单成为结尾。作者的判断是四个链接放最后更重要。**记下代价**：两篇实测
参考都带致谢（ExploitGym 2 句 7 机构，How We Broke 一行署名），而 LinkedIn 是上游作者最可能刷到的
一面，本文对 OSWorld / CUA-Gym / Slime 等 20 个上游项目 0 处致谢。要恢复，逐字抄 `twitter/01` 的
致谢帖 —— 机构名取自 `posts/twitter/01/BIBTEX.md` 里各上游 README 的 `author` 字段，不看仓库顶上的
链接；点机构与项目名，不点 @handle。
