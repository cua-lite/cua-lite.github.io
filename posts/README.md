# posts/ — 对外文案的共享约定

各平台的稿子在 `red/`（小红书）· `twitter/` · `linkedin/` · `reddit/`。
**本文件是唯一出处**：数字、平台规范、资产约定只在这里定义一次，各篇 README 只写本篇特有的内容。
改数字时**只改这里**，然后 grep 各篇同步 —— 上一轮 `~4.6× → ~5×` 要改九处，就是因为没有这一层。

---

## 1. 事实登记表（对外文案只能用这一列的口径）

| 事实 | 对外口径 | 出处 |
|---|---|---|
| 可验证任务数 | **30k+** | `index.html:65` |
| SFT 数据集 | **10+** | `index.html:68`；HF Corpora 现为 9 个，加 Rollouts 才 10+ |
| 接入 benchmark | **15+** | 站点覆盖板 16 条；**代码库 `README.md:102` 那份更全** |
| 有公开榜单的 | 11 | `assets/exps/eval/manifest.json` 非 pending 项 |
| parity 模型数 | **13** | 博客 parity 图数据 |
| 适配器模型家族 | **14** | 代码库 `lite/agents/models/` |
| 转换语料数 | **10 个已转换 / 9 个已发布**（对外写 `10+`） | `lite/data/preproc/` 有 10 个目录（含未发布的 `jedi`）；代码库 `README.md:244` 的 Corpora 集合只列 9 个；`README.md:30` 对外写 `10+`。**两个数都有出处，所以正文用 `10+`、致谢不带数字** —— 别在致谢里赌一个精确数 |
| 内存 | **under a quarter / 不足四分之一** | 实为 0.9/4.1 = 22% |
| 并行 | **博客/正式文档写 `~4.6×`；推特正文写 `five times`** | 博客 `:264` 印的是 4.6×，由内存比推出（4.1/0.9），**不是第二次测量**。**取整只发生在推特正文里** —— 作者原话「文本就是说 5 倍」；博客的作者注要求 `Keep the exact values`，**不要反过来改博客**（01 上我犯过这个方向的错） |
| 分数一致性 | **the same result as the OSWorld VM, across 13 models / 基本一致** | 博客 `blog/kvm-free-osworld:272` 现行原话。**2026-08-28 改口径**：博客原先写 `a score that tracks it within a few points`，作者要求删掉这个对宣传不利的限定语。**但 Reddit 保留 hedge** —— `reddit/02` 的笔记记着理由：跑复现的人最多的就是那儿，写死了会被当场打脸 |
| 精确 parity | mean\|Δ\|≈2.7 · worst 5.0 | **内部核对，任何平台的正文都不写。**对外分两档：**站点 / 博客 / Twitter / 小红书**用 `the same result as the OSWorld VM, across 13 models` / 「基本一致」；**Reddit 保留 hedge** `track … within a few points` —— 那儿跑复现的人最多，写死了会被当场打脸（见 `reddit/02` 的笔记）|

**「VM-free」的适用范围 —— 会被公开质疑的一条，务必看清：**

| 这些是 VM-free | 这些**需要 KVM**，别混在一起说 |
|---|---|
| `Lite.OSWorld` · `Lite.ScaleCUA` · `Lite.CUAGym` · `Lite.CUAWorld` · `WebGym` 等 `Lite.*` / 浏览器桌面家族 | **WindowsAgentArena**（`waa/README.md`：每次 `reset()` 开一台 Windows-11 QEMU/KVM 虚拟机）· **AndroidWorld**（`androidworld/README.md`：`KVM required`）· **MobileWorld**（`mobileworld/README.md`：`KVM required`） |

`30k+ 可验证任务` 和 `VM-free` 说的都是**左列**；`15+ benchmarks integrated` 是**更大的集合**，包含右列。两句放在同一条帖子里，读者会自动连成「所有 benchmark 都不用 VM」—— 冷读测试里 60 秒就被抓到，而且抓到之后连 parity 主张一起怀疑。**任何平台把 `VM-free` 和 benchmark 清单并列时，必须让范围显而易见。**

**风险（发布前需确认）：** 博客 `blog/kvm-free-osworld/index.html:209-211` 仍有一段 authoring 注释写着
`FACTS: no measured numbers (… memory, boot times, parallel counts) — none are grounded, keep it qualitative`，
且明确 `EXCEPTION: the parity-plot scores ARE real … the comparison table's footprint cells stay skeletons until measured`。
即 **parity 分数是实测的，footprint（内存/冷启动/并行倍数）按这段注释尚未实测**。四个平台现在都在发 `~5×`。
→ 要么确认已实测并删掉那段过时注释，要么把 footprint 三项改回定性。

## 2. 平台规范

| | 小红书 | Twitter | LinkedIn | Reddit |
|---|---|---|---|---|
| 标题 | 正文首行，≤~20 字 | 正文首行 | 正文首行（**折叠线 ~140–210 字符**） | **独立字段** |
| 项目符号 | `▪️` | `·` | `▪️` | **markdown**（`**粗体**`/`-`） |
| 标签 | 9–12 个中文 | 无 | 3–5 个英文 | **禁止** |
| 链接 | 页脚 | 仅首尾条 | 可前置（触达 vs 点击自选） | **紧跟开场白，正文之前** |
| 语气 | 站点语气，非口语 | 团队第一人称 | 宣告 | **同侪**，需作者披露 |

**通用禁令：** 不要把一个平台的痕迹带到另一个 —— `democratizing`、hashtag、`▪️`、"Built at UC Berkeley and Microsoft" 都不进 Reddit。

**Reddit 的行内链接规矩（只有 Reddit 支持 markdown，小红书/LinkedIn 都不支持，别回灌）：**

0. **项目名首次出现必须带链接。** 这是自链里唯一无条件的一条 —— 别人的模型和 benchmark 都链了，唯独自己的名字是白的，读起来又古怪又敷衍。`CUA-Lite` 链主页，`Lite.OSWorld` 链它的 env README。**每篇正文里 `CUA-Lite` 至少出现一次**：`reddit/02` 从 `red/02` 搬正文时，把红版的标题行和页脚一起删了，结果整篇一次都没提到项目名。
1. **外链（别人的东西）从宽，自链（我们的）从严。** 外链是**致谢**，读起来像论文不像广告，而且不增加一分自我推广密度；顺带把归属在视觉上一次分清 —— 蓝的是别人的，`Lite.*` / CUAGym / CUAWorld 是黑的。自链另说：三个主链接已经有专门的链接块，正文里再内链只会翻倍自荐观感，**除非那一处的自链本身就是读者要的东西**（如 `reddit/02` 把 `Lite.OSWorld` 链到 env README —— `[P]` 帖的读者正要看怎么复现）。
2. **要么整组都链，要么整组都不链 —— 但「不链」必须是查完之后的结论，不是查不到就算了。** 我拿这条当过两次偷懒的借口：先说「15+ benchmark 那串没有已核 URL，所以一个都不链」，可代码库 `README.md:32` 里**七个全都有链接**（指向各自的 env README），我看见了却没用；同一句里 5 个开源模型链了、`GPT / Claude / Gemini` 空着，`OSWorld` 链了、我们自己的 `CUAGym / CUAWorld` 空着 —— **半链的观感比全不链差得多**，因为它看起来像没写完。
3. **列表里也要链，只要整组都有。** 15+ benchmark 那七个现在全部链向各自的 env README —— 对读者比链上游更有用（「怎么在这套里跑它」），而且整组齐平。
4. **URL 必须有出处，不许现编。两个已核来源：**
   - 网站：`grep -rhoE 'https?://' index.html blog/` → OSWorld · Slime · WebArena · AndroidWorld · UI-TARS · Qwen3-VL
   - **代码库 `/srv/home/zzh/projects/cua-lite/cua-lite/README.md`** —— 模型表（`:88-97`）给出全部 HF id，可拼出 `huggingface.co/<id>`：Qwen2.5-VL `Qwen/Qwen2.5-VL-7B-Instruct` · EvoCUA `meituan/EvoCUA-8B-20260105` · Fara `microsoft/Fara-7B` 等；环境文档路径（`:195-197`）可拼出 `github.com/cua-lite/cua-lite/blob/main/<path>`。
   **别只查网站就下「没有链接」的结论** —— 上一次只 grep 网站，误删过 WindowsAgentArena；这一次又据此写下「不许现编」，同样漏了代码库。
5. **同一个词在不同语境可以指向不同地方，这是对的，别「统一」掉。** `reddit/01` 里 `OSWorld` 出现两次：Sandboxes 那句写的是 `reproduce **external** benchmarks such as OSWorld` → 链**上游** `xlang-ai/OSWorld`；Eval 那条写的是 `15+ benchmarks **integrated**` → 链**我们的** env README。语义不同，落点就该不同。
6. **重复提及只链首次。** `CUA-Lite`、`Lite.OSWorld`、`Qwen3-VL` 在正文里都出现不止一次，只有第一次带链接。
7. **发布前跑一遍校验**：抽出正文块 → 列出全部 `[名](url)` → 凡是 `github.com/cua-lite/cua-lite/blob/main/<path>` 的，逐个 `os.path.isfile` 核对本地仓库确实存在。现状：`reddit/01` 23 个链接、`reddit/02` 3 个，路径失效 0 处。

**Reddit 的链接位置改过一次，理由记在这里：** 原先按「链接后置显得不像广告」写成页脚。但 r/LocalLLaMA 的发布帖惯例恰恰相反 —— `Model: hf.co/…` / `GitHub: …` 通常就顶在开场白下面，因为那个版块**一半读者是先点链接再回来读正文**的。把链接压到最后，等于让最想要东西的人翻到底。现在的位置是**开场白之后、四块正文之前**：钩子 → 拿东西 → 要细节再往下。这不等于「链接前置」（LinkedIn 那种把链接放在第一行之上）—— 开场白仍然是第一屏第一句。

## 2b. Reddit 版块选型（2026-08 调研）

数字来自 GummySearch 的第三方聚合 —— Reddit 2025-09 起不再公开订阅数，这些是估算，**看量级和增速，别引用具体值**。

| 版块 | 规模 | 年增 | 性格 | 对我们 |
|---|---|---|---|---|
| **r/LocalLLaMA** | 810k | **+54%** | OSS 优先，本地推理、显存/硬件，Qwen 是头号话题 | **01 首选** |
| r/MachineLearning | 3.1M | +2.6% | 研究向，但内容已漂向求职/求助；`[P]` 是真 flair，样本里 21 篇 | **02 首选（高上限高风险）** |
| r/AI_Agents | 429k | +122% | 涨得最快，但**重度 no-code**（n8n / Flowise / Bubble） | ❌ 不去，语域不对 |
| r/LocalLLM | 211k | +154% | 更偏新手 / Ollama | 备用，与 LocalLLaMA 重叠 |
| **r/LLMDevs** | 166k | +59% | 技术向 LLM 应用开发，**明确讨论 agent harness** | **01 次选** |
| **r/reinforcementlearning** | 88k | +32% | PPO / Stable-Baselines3 / 仿真环境 | **02 次选（低风险高信噪）** |

**没有专门的 computer-use / GUI-agent 版块** —— 查过了，这类讨论散在上面几个里。所以不存在「最对口的那个版块」，只能按帖子的**论证类型**选。

**两条从调研里得到的硬约束：**

- **r/MachineLearning 把自我推广导向每周的 `[D] Self-Promotion Thread`**，主版只留「对社区确有价值」的内容。`reddit/02` 能进主版**唯一的凭据是那份 13 模型 parity 数据** —— 它是可核验的结果，不是发布公告。**`reddit/01` 是项目总览，没有新结果，不要发主版。**
- **r/LocalLLaMA 的容忍度是 90/10** —— 自我推广不超过总活动的十分之一，且必须披露身份。账号得先有真实发帖史。

## 3. 资产约定

- **`red/` 是唯一的图片来源**，`linkedin/` 与 `reddit/` 的 `assets/` 全是**逐文件软链**（`mode 120000`），不复制。
- **只链英文版**（`*-zh.png` 不进 linkedin/reddit）。
- 动图链自 `twitter/01/assets/`。
- **Reddit 每篇只留 3 个软链**：领头动画的 `.mp4` + `.gif`，加一张留给首条评论的证据图。Reddit 正文帖是「一个 media slot + 一段文字」，没有轮播 —— 多留几张只会让下次发帖的人犹豫选哪张。LinkedIn 相反，5 张一套走 document 轮播。
- 重制：`red/0N/make_cover.py`（封面）· `capture_sections.py`（站点整段截图）· `scripts/subset_cjk.sh`（中文封面字体 → `assets/fonts/`，共享）。

### 领头图（按证据强度，不按好看）

| 帖子 | 领头 | 首条评论 | 理由 |
|---|---|---|---|
| r/LocalLLaMA | `twitter/01/01-hero.mp4` | 不配图，给 HF 真链接 | 该版块的文化是 "show me it working"；动画是证据，站点分节图是广告 |
| r/MachineLearning `[P]` | `twitter/01/03-vm-tax.mp4` | `red/02/04-parity.png` | 动画本身就是论点（VM → container）；散点留给能自行核验的读者 |
| LinkedIn 02 | `red/02/02-footprint.png` | — | 全套最耐缩，横版不裁，一眼给全 |
| LinkedIn 01 | `red/01/01b-cover.png` | — | 唯一不空的封面版式 |
| 小红书 | 各自 `01a/01b-cover` | — | 平台吃图文卡 |

**Reddit 两篇的领头都是动画，不是静态图**（早先这张表写的是 `04-eval` / `04-parity` 打头，和两篇各自的 README 冲突过）。静态证据图一律降到首条评论：OP 自己在评论里补数据，是这两个版块的加分动作。

**Reddit 只收两类图：动画论点，和读者能自行核验的图表。** `red/` 里的**站点分节图一张都不进** —— 它们全都是「眉标 + 衬线大标题 + 卡片 + `Browse ↗` CTA」的营销版式，PNG 里 CTA 还是死的。曾把 `03-data.png` 当成「真实 HF 数据表」留下来当评论区补图，**是没看图就写的说明**：那张的 HF 面板是我们自己画的仿制界面，在 r/ML 被认出来一次整帖就废了。`04-parity.png` 是唯一的例外 —— 它是**真散点**（y=x 虚线、13 个点、caption 写明 `identical tasks`），读者能自己数点验证，不是版式。**判据不是好不好看，是「读者能不能自己核验」。**

**不要用：**
- `03-hh.png` 进技术帖 —— 标签 pill 盖在真实 Chrome 标签页上、控件被切、两图时间戳与工具栏状态不同（一张论证 identical 的图里全是不 identical）
- `01a/01b-cover` 进 Reddit —— 约 30% 空白且零数字，是该社区判定广告的标志
- `red/01/02-sandboxes` 与 `red/02/05-belt` 同时用 —— 同一条 belt 换了标题

## 4. 反复踩过的坑

1. **别自由发挥** —— 站点和博客有 battle-tested 的句子。写任何标题/bullet 前先把对应的 heading / bold lead 抄出来再压缩。本轮翻车实例：`verifiable rewards`（博客 4 处都写 **tasks**）、把沙盒级两用写成**任务级**（＝污染测试集）。
2. **别让排版删实质** —— 为挤单行/折叠线砍掉「训练」「可验证任务」「benchmark」，实测证明加回去都放得下。**先写完整，量了真放不下再删冗余**。
3. **改一处要扫全篇** —— `democratizing`、`our own`、`~5×` 都出现过只改一处的漂移。
4. **归属 —— 这条我写错过一次，代价很大，照抄代码仓库，不要推断。** 核实自 env README：
   - ⚠️ **「ScaleCUA」是两个不同的项目，别再合并。** 环境 `lite.scalecua` / `Lite.ScaleCUA` = **THUDM 的 SCALE-CUA**（arXiv 2607.11185，HF 上 pin 的是 `extreme1228/ScaleCUA`）；SFT 语料 `lite/data/preproc/scalecua` = **OpenGVLab 的 ScaleCUA-Data**。依据是提交 `0598e30` 的正文：「a different project that happens to share the name … Note lite/data/preproc/scalecua is the OTHER ScaleCUA and is deliberately untouched.」**这条我错过两次**：先抄了 `docs` 里的旧链接写成 THUDM（当时是对的却以为错），又「修正」成 OpenGVLab（把对的改错了）。**动这个名字之前先读 `0598e30`。**
   - **CUA-Gym** = [xlang-ai](https://github.com/xlang-ai/CUA-Gym) 的 · **CUAWorld** = [CMU gym-anything](https://github.com/cmu-l3/gym-anything)（MIT）· **ScaleCUA** = [THUDM](https://github.com/THUDM/SCALE-CUA) 的 · **OSWorld** = xlang-ai 的
   - **沙盒镜像依赖关系（写「底座」相关句子前必读 —— twitter/01 上我写错过一次）：**
     ```
     cua-lite/sandbox.linux            共用 GNOME 桌面底座（FROM ubuntu:22.04）
     ├── cua-lite/lite.osworld         FROM sandbox.linux
     │   ├── lite.scalecua             无自有镜像，跑在 lite.osworld 上（docs/envs.md:286）
     │   └── cua-lite/lite.cuagym      FROM lite.osworld（cuagym/scripts/install.sh:48）
     └── cua-lite/lite.cuaworld.base   同一份 Dockerfile.linux 的 ga 变体（cuaworld/scripts/install.sh:316）
     ```
     **能说**「四个沙盒出自同一个 VM-free 底座」。**不能说**「都跑在 Lite.OSWorld 的容器里」（cuaworld 不是），也不能说「Lite.OSWorld 的容器就是家族底座」（真底座是它的上游）。博客原文是 **a** base for **a** family，别硬化成 the/whole。`sandbox.linux` 这个名字不必进对外文案。
   - **我们的是 VM-free 运行时、统一接口和集成**，以及 `Lite.*` 这些名字 —— **不是任务、不是评测器、不是那 40 个软件**
   - **归属放哪儿：正文用通行名，正式归属集中在结尾致谢。** 正文写 `OSWorld` / `CUA-Gym` / `CUAWorld`，**不写** `xlang-ai's OSWorld` / `CMU's gym-anything` —— 每处都挂所有者会把读者的注意力从「我们做了什么」引开，而且同一个名字要挂三遍。正式归属（真实仓库名 + 作者 @）集中在**致谢那条**，一次说清。作者原话：「你真的没必要 xlang-ai's CMU's THUDM's（只有最后致谢我觉得这个才需要）」。
   - 所以**绝不能**写 `our own training environments like CUAGym and CUAWorld` /「CUAGym、CUAWorld 等自建训练环境」：那是用别人项目的原名声明自有。正确说法是 `re-host … on one VM-free runtime` /「外部任务集的迁移，统一跑在同一套 VM-free 运行时上」。
   - 曾经的错误规则（「`Lite.*` / CUAGym / CUAWorld 是我们自建」）写在这里，于是自动复制进了 red/01 中英版、reddit/01、twitter/01 四处。**共享 README 里的规则会自我复制，写之前必须回源头核。**
