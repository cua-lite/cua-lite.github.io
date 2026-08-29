# CUA-Lite — Reddit 01（总览，改写为「训练你自己的本地 CUA 模型」）

**目标版块：** r/LocalLLaMA（810k，年增 54%，OSS 优先 —— 全站增速最快的技术版块之一）。
**次选：** r/LLMDevs（166k，技术向 LLM 应用开发，**该版块本来就在讨论 agent harness**）。同一份稿子基本能直接用，标题往「接你自己的模型」偏一点。
**不要发 r/MachineLearning 主版** —— 这篇是项目总览、没有新结果，主版把自我推广导向每周的 `[D] Self-Promotion Thread`。有数据的那篇是 `posts/reddit/02`。
**不要发 r/AI_Agents**（429k，年增 122%，看着最诱人）—— 调研显示它**重度 no-code**（n8n / Flowise / Bubble），我们这篇讲适配器和推理栈，语域完全不对，会石沉大海。

版块规模与性格的调研数据在 [`../../README.md` §2b](../../README.md)。**没有专门的 computer-use / GUI-agent 版块** —— 查过了，这类讨论散在上述几个里，所以不存在「一个最对口的版块」，只能按帖子的论证类型选。

## 立论：rollout + train，不是 benchmark，也不是平台介绍

r/LocalLLaMA 的重心是**「把模型跑在自己机器上」**，但他们确实关心开源 GUI agent 模型（UI-TARS、OpenCUA、ScaleCUA、Qwen-VL 这类）。所以主线是：

> **拿开源模型去操作电脑 —— 跑、评、训三条路都开着；数据和环境都开源。**

开头刻意写成 **run, eval or train**：那个版块想让本地模型干活、或想知道自己模型能拿几分的人，远多于要训练的人。只说 train 会把他们挡在门外；只说 benchmark 又会把评测当成主框（曾经写歪过一次）。三个动词并列，谁都能对号入座。

**两个曾经写歪的方向，别再走回去：**
- ❌ 写成**平台介绍**（Data/Environments/Training 三支柱当卖点）—— 那是 LinkedIn 的骨架。
- ❌ 写成**评测**（"running desktop-agent benchmarks locally"）—— benchmark 只是环境的一种用法，不是本篇的重点。

**不写痛点段，第一句就给东西。** 曾经写过两段痛点（沙盒是重型虚拟机、harness 得每个模型重写一遍），约 430 字符；后来压成首句分号后的半句；最后全删。理由：`If you want to run, eval, or train …` 这个开头**已经完成了筛选** —— 会往下读的人正是撞过这些墙的人，再花两段告诉他们「你的处境有多糟」是在拖延交货。**痛点没有消失，只是不再单独占位**：它们进了每块的小标题（`modular, not a black box` / `lightweight` / `unified and open`），痛点和答案贴在同一行里，比隔着四段呼应更有力。

**Sandboxes / Data / Framework 三块的正文逐字照抄 `posts/red/01` 的英文版，不要重写。** 那三段是反复打磨过的。我一度自己重写成 `VM-free — plain Docker, so they pack many per machine … 30k+ verifiable tasks across desktop, browser and mobile, each scored automatically`，结果：`across desktop, browser and mobile` 和首句的「桌面 / 网页表单 / 手机」重复，`each scored automatically` 是 `verifiable rewards` 的同义反复，整段还长了 40%。**红版有的句子就用红版的。**

唯一的追加是 Sandboxes 末尾那句 `Being plain Docker, they also run where a VM can't: WSL, many cloud instances, CI runners.` —— 这是**为这个版块专门加的一句**，不是润色：`VM-free` 本身没告诉读者「所以我在 WSL 上也能跑」，而这恰是 r/LocalLLaMA 最常撞的墙。要砍就整句砍，别动前面两句。

**三个例子只能从博客那组里挑，而且要挑主语翻转后仍然成立的。** 博客 `blog/kvm-free-osworld` 原话是「VM 需要 `/dev/kvm`、嵌套虚拟化和重资源 —— 而 `cloud instances, CI runners, and nested containers` **rarely provide**」，说的是**那些地方给不了 VM 要的东西**。我一度把第三项照搬成 `inside another container`，等于把主语翻成「**我们能在容器里跑**」—— 而容器里再跑 Docker 需要 DinD 或挂宿主 socket，常常还要 `--privileged`，**不是开箱即用**。前两项翻转后仍然成立，第三项不成立，所以换成了 `CI runners`（CI 上跑容器是常态，翻转后依然为真）。**以后从博客搬句子，注意主语有没有被翻转。**

**四块的排版照搬 `posts/red/01` 的英文版：`**名称: 定性**` 一行 + 两三句正文。** 之前是 `**Sandboxes.** 一大段` 的行内式，harness 和 sandboxes 各膨胀到 440 / 530 字符，手机上是两堵墙。分成小标题行之后，**扫读的人只看四行加粗就知道有什么**，要细节再往下看 —— 这正是 red/01 那份已经验证过的骨架。唯一的改动是 `▪️` 换成 markdown 加粗（Reddit 不吃小红书的符号），子项 `·` 换成 `-`。

**首句必须落在「你的模型」上，四个动词直接带宾语。** 曾写成 `the framework for inference, eval, SFT, and RL` —— 一串光秃秃的名词，读者不知道这些动词作用在什么上面。现在是 `the framework **to run, eval, SFT, and RL your own model**`：四个动词各自直接管住 `your own model`（`run your own model` / `RL your own model` 都成立），落点从抽象能力变成读者自己的模型，而且和 Framework 那一块的小标题 `run, eval, SFT, RL` 逐字对齐。

**句尾不补 `to drive your own computer`。** 三个理由：① 同一句开头已经写了 `to actually use a computer`，句尾重复；② 站点一贯用 `use a computer`，`drive` 是另一个词，混用会漂移；③ **事实上被操作的电脑在沙盒里，不是读者自己的电脑** —— `your own computer` 会让人以为我们要接管他的机器。

**用 `your own model` 而非 `your local model`** —— harness 那一块列了 GPT / Claude / Gemini 走 API，首句写死 local 会和它自相矛盾（和你说过的「首句不强调 open」是同一条理由）。`your own` 一样是第二人称，该版块一样买账。

**四块的顺序：harness 打头。** r/LocalLLaMA 的重心是**把模型跑在自己机器上**，所以最先该给的是「你的模型怎么接进去」，不是环境。顺序 harness → sandboxes → data → framework，正好也是 run → eval → train 的推进。

**「本地跑」写在 Framework 的引子里，不写成 `run a model locally to use your computer`。** 后者有个事实错误：agent 操作的是**沙盒里的**桌面，不是读者自己的电脑 —— 这么写读起来像我们要接管你的机器，在这个版块是反效果。现在写 `any agent plugs into any sandbox — including a local model on your own machine`：「本地」这个卖点在，归属也对（模型在你机器上，被操作的电脑在沙盒里）。

**Framework 的引子和三个子项是「产出 / 复用」的关系。** `Running it produces rollouts, reused three ways:` —— run 是**产生** rollout 的那一步，eval / SFT / RL 是**复用**。曾经想把 run 也列成第四个子项，逻辑就断了（run 不是 rollout 的一种用法）。

**每一块必须自足。** 删痛点段时 `**The harness.** That code…` 变成了悬空指代（和之前 `We open-sourced both` 同一类错误），改成 `The code that turns a model into an agent` 才自带定义。**以后任何一块的开头都不许以 `That` / `It` / `Both` 起句。**

**同一个事实只讲一次。** 「任何模型的 rollout 可微调任何模型（GPT-5.5 → Qwen3-VL）」曾同时出现在 Data 和 SFT 两处。它属于 **SFT 子项**（那里才解释了 adapter 这个机制），Data 只说「统一格式、开放下载」。red/01 的英文版本来就是这么分的，是我加回去的时候重复了。

**别自己造比喻词。** 中途把 harness 那层写成 `the glue between model and screen` —— `glue` 站点和博客一次都没用过，是自由发挥；而且比喻要读者先解码。写成 `the code that turns a model into a computer-use agent` 就够了：不打比方，直说是什么。

**通俗化不等于省掉宾语 —— 这是本篇最隐蔽的一个坑。** harness 那三样曾写成 `how screenshots go in, what actions are available, how the output gets parsed`：**三个短语全都缺宾语** —— 进到哪儿？对谁可用？解析成什么？看着像在照顾读者，实际比原词更糊，而且更长。中途改成三个 `how X does Y` 的从句，落点补齐了但更长、更难扫。最终版是三个**名词短语**：

> `context management (screenshots and action history), its action space, and turning model output back into actual clicks and keystrokes`

名词短语一眼就是一个概念，从句要边读边解析；`context management` 又正是 r/LocalLLaMA 的日常词。三项首尾接成闭环（截图进 → 点击出），一遍读懂。

**这里刻意保留了三项而不是压成两项。** `action space`（模型被告知**可以做什么**）和「把输出解析回点击」（模型**说了什么、怎么执行**）是两件事，合并会丢掉前者 —— 而它恰是博客点名的三个不标准之处之一（`different schemas, action spaces, harnesses`）。

**句尾不补 `that controls the computer`。** 同一句开头已经是 `computer-use agent`，再说一遍是冗余；而且「控制哪台电脑」这个歧义前面已经栽过两次（`use your computer` / `drive your own computer`）。**`action space` 不是术语泄漏 —— 博客 `why-cua-lite` 原话就是 `each with its own interface and action space`。** 要避开的是**参数名和函数签名**（`action_space` / `protocol` / `render_step` 这些代码标识符），不是领域概念本身。把领域概念也换成白话，只会让技术读者觉得你不懂或在敷衍。

**不要贴代码。** 曾经写过一段三行的 `gym.make/agents.make` 片段，是从 README 推断而非从示例抄的，没跑过。Reddit 上会有人直接复制。要贴就先实跑验证。

**三行链接放在开场白之后、四块正文之前**，不放页脚。r/LocalLLaMA 的发布帖惯例就是这样（`Model: hf.co/…` / `GitHub: …` 顶在开头），因为那个版块**很多人先点链接再回来读正文** —— 压到最底，等于让最想要东西的人翻到底。注意这不是 LinkedIn 那种「链接前置」：开场白仍然是第一屏第一句，链接排在它后面。

LinkedIn 版的 `democratizing`、hashtag、`▪️` —— 一个都不要带过来。

---

## 标题（选一个）

1. ⭐ `CUA-Lite: run, eval, or train your local model to use a computer`
2. `CUA-Lite: run, eval, or train an open model to use a computer`（第三人称版；发 r/LLMDevs 时把 `your local model` 换成 `your own model`）
3. `CUA-Lite: open data + lightweight sandboxes for computer-use agents (Qwen3-VL, UI-TARS, and friends)`

**标题里必须有 CUA-Lite** —— 项目帖不带项目名，读者没有可搜索、可记住的抓手。

**`your local model` 而不是 `an open model`，两个理由：**

- **第二人称 vs 第三人称。** `your local model` 直接点到读者头上，`an open model` 是在描述一类东西。
- **`local` 比 `open` 更准。** `local` 是那个版块**名字里的词**，是他们的身份标识；`open` 只是相邻概念 —— 不少开源权重的模型是走托管 API 跑的。

**标题用 `local`，正文不用 —— 这不是自相矛盾。** 我一度以「harness 块列了 GPT / Claude / Gemini 走 API」为由否掉这个标题，那是把**首句**的规则错套到标题上。**标题是筛人的，正文才是划范围的**：标题说这帖子给谁看，正文说这东西能干什么。读者点进来发现还支持 API 模型，读到的是额外好处，不是矛盾。正文首句仍写中性的 `a model`，Framework 块里的 `including a local model on your own machine` 正好和标题接上。

**`to use a computer` 而不是 `on real desktop tasks`**：后者既窄（我们是桌面 + 浏览器 + 手机三端）又抽象（"desktop task" 不是这个版块的日常词）。`use a computer` 是站点一贯的说法，也和正文第一句逐字一致 —— 标题和开头咬合，读者点进来不需要重新对焦。

**`— without a VM` 从标题里去掉了。** 它是本项目最硬的差异点，但对 r/LocalLLaMA 是**实现细节**：那个版块的钩子是「我自己的模型能干这个」，不是「用什么虚拟化」。VM 这一层留给 Sandboxes 那一块（`VM-free — plain Docker … run where a VM can't`），读者读到时已经在看解法，不必先被科普一遍问题。**VM 当标题主语的写法归 `posts/reddit/02`** —— 那篇整篇就在论证这件事，两篇不该抢同一个卖点。

---

## 正文（markdown，直接粘）

```
If you want to run, eval, or train a model to actually use a computer — clicking through desktop apps, filling in web forms, tapping through a phone app — try [CUA-Lite](https://cua-lite.github.io). It democratizes all four pieces: the harness, the sandboxes, the data, and the framework to run, eval, SFT, and RL your own model.

Code: https://github.com/cua-lite/cua-lite
Homepage: https://cua-lite.github.io
Blog: https://cua-lite.github.io/blog

**Harness: modular, not a black box**
The code that turns a model into a computer-use agent: context management (screenshots and action history), its action space, and turning model output back into actual clicks and keystrokes. 14 model families ship with one: [GPT](https://platform.openai.com/docs/guides/tools-computer-use), [Claude](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) and [Gemini](https://deepmind.google/technologies/gemini/) over their APIs, plus open weights like [Qwen3-VL](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct), [Qwen3.5](https://huggingface.co/Qwen/Qwen3.5-9B), [Qwen3.8](https://huggingface.co/Qwen/Qwen3.8-27B), [UI-TARS](https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B), [EvoCUA](https://huggingface.co/meituan/EvoCUA-8B-20260105) and [Fara](https://huggingface.co/microsoft/Fara-7B), on whatever inference stack you already run. Adding a model is one small piece, not a rewrite.

**Sandboxes: efficient, with verifiable tasks**
VM-free sandboxes carrying 30k+ CUA tasks with verifiable rewards, so the same sandbox serves both benchmarking and training. These sandboxes re-host [OSWorld](https://github.com/xlang-ai/OSWorld), [CUA-Gym](https://github.com/xlang-ai/CUA-Gym), [CUAWorld](https://github.com/cmu-l3/gym-anything) and other public task suites on one VM-free runtime — [Lite.OSWorld](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/lite/osworld/README.md), [Lite.CUAGym](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/lite/cuagym/README.md), [Lite.CUAWorld](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/lite/cuaworld/README.md). Being plain Docker, they also run where a VM can't: WSL, many cloud instances, CI runners.

**Data: unified and open**
[10+ SFT datasets](https://huggingface.co/collections/cua-lite/corpora), plus the latest [rollouts](https://huggingface.co/collections/cua-lite/rollouts) (interaction trajectories) from frontier CUAs, all in one format and free on [Hugging Face](https://huggingface.co/cua-lite).

**Framework: run, eval, SFT, RL**
One agent–environment interface, so any agent plugs into any sandbox — including a local model on your own machine. Running it produces rollouts, reused three ways:

- Eval — scored to rank agents; 15+ benchmarks integrated ([OSWorld](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/osworld/README.md), [OSWorld-2](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/osworld_2/README.md), [WindowsAgentArena](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/waa/README.md), [WebArena](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/browsergym/README.md), [WebVoyager](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/webharbor/webvoyager/README.md), [AndroidWorld](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/androidworld/README.md), [MobileWorld](https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/mobileworld/README.md), and more)
- SFT — one trajectory format, rendered by each model's adapter into its own, so any model's rollouts can fine-tune any other: GPT-5.5 → Qwen3-VL, for example
- RL — used as the learning signal, sampled continuously in the sandbox; GRPO, GSPO and more, on [Slime](https://github.com/THUDM/slime)

Disclosure: I'm one of the authors. If you've tried running, evaluating, or training a computer-use agent locally and hit a wall, I'd like to hear where — that's mostly what we've been fixing.
```

---

## 配图

`assets/` 全是软链（`mode 120000`），只链英文版；动图链自 `posts/twitter/01/assets/`。

**一帖只配一段媒体。** Reddit 的正文帖就是「一个 media slot + 一段文字」，没有轮播；多图要么被折叠，要么让帖子看起来像广告投放。所以 `assets/` 只留**三个**：领头动画的 mp4 + gif，加一张封面卡。其余（`01-hero-wide.mp4` / `02-sandboxes` / `03-data` / `04-eval` / `05-train`）全部删除。

**领头：`01-hero.mp4`（1.4 MB）** —— agent 依次操作桌面、浏览器、手机，下方跟着实时 action trace（`click([502,563]) 1.1s` … `terminate("success")`）。**首选它，因为它是「证据」——「show me it working」正是该版块的文化**，而封面卡是「主张」。

**备选 / 评论区：`01b-cover.png`。** 我原先一概反对封面卡进 Reddit，理由是「标语 + bullet + 数字条 = 广告的标志」。**重新看图之后，这张不该一概而论** —— 它下半张是三台设备的实景版式（LibreOffice Calc 里真的列着 OSWorld / WebArena / AndroidWorld / MobileWorld 的分数、浏览器、手机），加上 `30k+ · 10+ · 15+` 的数字条，**信息密度足够撑住一张图**，不是空标语卡。

**但用它之前知道一件事：下半张三台设备里的界面是版式illustration，不是真实截图** —— 那个 Google 搜索结果页和 iMessage 对话都是我们画的。作为**装饰性 hero 没问题**（读者一眼看得出是设计稿）；**但绝不能拿它当证据**，也不要在正文或评论里说「这是实际运行截图」。这和 `03-data.png` 被删掉是同一条线：**仿制界面可以当装饰，不能当证据。**（`03-data.png` 的问题是我曾把它写成「真实 HF 数据表」拿去当证据。）

**评论区补料优先给真链接，不是图。** `https://huggingface.co/cua-lite` 加一句数据长什么样 —— 能点的真链接强过一张仿制界面的图。真要配图，去 HF 页面截一张**真的**。

- **格式**：优先 `.mp4` —— Reddit 无论如何都把 GIF 转成视频播放器，直接给 mp4 画质更好、体积只有 1/4（1.4 MB vs 5.8 MB）。`01-hero.gif` 留作备用（个别版块禁视频帖，或需要贴进评论时）。
- **方向**：竖版（800×1083），Reddit 流量以移动端为主。横版已删 —— 没有它派得上用场的场景。
- **评论区补图**：`03-data.png`（真实 HF 数据表）。**留它是有明确用途的**：OP 在首条评论贴「数据长什么样」是 r/LocalLLaMA 的常见加分动作，比任何宣传图都管用。

---

## 发布前检查

- **标题里必须有 CUA-Lite** —— 项目帖不带项目名，读者没有可搜索、可记住的抓手。
- **14 个模型家族适配器**：来源为代码库 `lite/agents/models/`，发布前 `ls` 一遍确认数目。
- **不写伪代码、不写实现细节**（参数名、函数签名、API 形状）—— 帖子讲能力和取舍，不讲接口。曾贴过一段没跑过的 `gym.make/agents.make`，也写过 `processor` / `generate_fn` 这种参数级描述，都已删除。
- **别把小红书/LinkedIn 的措辞带过来**：`democratizing`、hashtag、`▪️`、"Built at UC Berkeley and Microsoft"（改成正文末尾的 Disclosure 行）。
- 结尾那句**主动问对方踩过什么坑**是刻意的：r/LocalLLaMA 吃「一起解决问题」的姿态，不吃「我们发布了」的姿态。
- 账号需有发帖历史；避免与 Reddit 02 同日发。
