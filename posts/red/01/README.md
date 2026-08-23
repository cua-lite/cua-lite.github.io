# CUA-Lite — 小红书 01

小红书系列第一篇。**定位：项目总览，核心就是首页 hero 的那三条**——
「任何 agent，任何电脑 / computer-use agent 需要的一切」：① 沙盒与可验证任务、② 统一数据、③ 统一框架。
正面框架，三条平铺，不由任何一块领跑。KVM-free 只作为沙盒的一个属性一笔带过，具体数字留给 `red/02`（对应 `blog/kvm-free-osworld`）。

**语言：** follow 站点（homepage + blog）的语气——朴素、准确、平行，不用网络口语、不堆 emoji、不造夸张利益点。措辞尽量沿用站点 battle-tested 的说法，每个数字都真实，来源见文末。小红书只借它的**结构**（短段落、清单、话题标签），不借它的口语腔。

---

## 标题（选一个；小红书标题上限约 20 字，字数已标注）

1. ⭐ CUA-Lite：训练与评测 CUA 的开源平台　（22 字，略超；封面 lead 不带品牌名，故标题必须带 CUA-Lite）
   　**用「平台」不用「生态」**：平台是现在**已经**成立的事实（沙盒+数据+框架），生态是结尾那句「希望长成社区驱动的开源 CUA 生态」的**愿景**；标题若已写「生态」，结尾的愿景就自相矛盾。与封面 lead「一个开源平台」也一致。
2. 训练与评测 CUA 的开源生态：沙盒 · 数据 · 框架　（21 字，点出三支柱）
3. 训练与评测 CUA 的开源生态　（13 字，最稳，brand 由封面/正文承担）
4. 任何 agent，任何电脑：CUA-Lite　（＝首页 slogan，配标题卡封面才直观）

> 「生态」是 aspirational 说法（正文结尾也点明是「希望长成社区驱动的开源生态」）；沙盒/数据/框架三支柱与核心贡献放正文首段，标题塞不下全部。

---

## 正文（直接复制这段）

```
CUA-Lite：训练与评测 CUA 的开源平台

训练与评测 CUA（computer-use agent）需要沙盒、数据与框架三个要素。CUA-Lite 是集成这三者的开源平台，覆盖桌面、浏览器与移动端。

▪️ 沙盒：高效、任务可验证
免虚拟机（KVM-free）的沙盒，内置 30k+ 个可验证 CUA 任务，可并行支撑大规模训练与评测。既能复现 OSWorld 等外部 benchmark（我们的 Lite.OSWorld 与原版分数相当），也自建了 Lite.CUAGym、Lite.CUAWorld 等训练环境。

▪️ 数据：统一、开放
10+ 个 SFT 数据集，以及前沿 CUA 产生的最新 rollout（交互轨迹），统一为一套格式，在 Hugging Face 免费开放。

▪️ 框架：评测、SFT、RL
统一的 agent 与环境交互接口，任何 agent 均可接入任何环境。同一份 rollout，评测时用于打分排名，训练时用作学习信号。已接入 15+ 个 benchmark：OSWorld、OSWorld-2、WebArena、WebVoyager、AndroidWorld、MobileWorld 等。

三者都在持续扩展。我们希望 CUA-Lite 最终成长为社区驱动的开源 CUA 生态，欢迎贡献你的数据集、环境或 agent。

站点 cua-lite.github.io
GitHub github.com/cua-lite/cua-lite
数据 huggingface.co/cua-lite
UC Berkeley · Microsoft

#AI #人工智能 #大模型 #agent #强化学习 #机器学习 #cua #computeruseagent #guiagent #webagent #mobileagent #科研日常
```

---

## 配图（全图片，都在 `assets/`）

轮播顺序 = 封面 + 主页四个 section（对齐主页叙事 hero→沙盒→数据→评测→训练）：

1. **封面（4 张：英文 + 中文各两版，同版式）**
   - `assets/01a-cover.png` / `assets/01a-cover-zh.png` — 紧凑版（1080×1240），纯文字。
   - `assets/01b-cover.png` / `assets/01b-cover-zh.png` — 竖版（1080×1440），文字上移，底部放 hero 的桌面/浏览器/移动端三设备（带完整边框、标平台名）。
   - **定位 lead 引出三条 bullet**（与首页 hero 同步：`One open-source platform with everything a computer-use agent needs:` / 中文「一个开源平台，提供 computer-use agent 所需的一切：」）——先点名 CUA、给出「开源平台」定位，三条 bullet 才都落在 CUA 语境里；因此第三条 bullet 跟首页一样只说「any agent / 任何 agent」，不再重复 computer-use。封面 lead **不重复品牌名**（logo 已自证），首页/正文才带 CUA-Lite。
   - **三条 bullet 以支柱名打头**（`Sandboxes / Data / Framework`＝`沙盒 / 数据 / 框架`，同首页），三条平行、无一重复起首词；`30k+ verifiable CUA tasks / 可验证 CUA 任务` 点明任务是给 CUA 的。排版硬约束：lead 与 bullet **同字号（34px）**、lead **必须单行**、平台清单（`across desktop, browser, and mobile`）用 `.keep` 整体换行，不从中间断开。
   - **中文版 = 英文 Fraunces 标题（品牌招牌脸）+ 中文正文**：保留品牌 slogan、避开「电脑/设备」取舍；正文/标签/页脚用**思源黑体（Noto Sans SC，对应 Urbanist）**。全中文标题（思源宋体 + Fraunces 斜体 `agent`）为可选项，见 `make_cover.py` 里 `_ZH_SERIF_CSS` / `H1_ZH` 注释。
2. **`assets/02-sandboxes.png`** — 主页 01·Sandboxes **整段**：标题「Efficient sandboxes, any task.」+ 说明 + rollout belt（真实桌面 app：calc/files/impress/chrome/gimp/vlc…，两侧淡出）。
3. **`assets/03-data.png`** — 主页 02·Data **整段**：标题「One schema, any dataset.」+ Corpora/Rollouts 双卡 + **真实 HF 数据表**（images/messages/metadata 列、直方图、样本行）。
4. **`assets/04-eval.png`** — 主页 03·Eval **整段**：标题「One command, any benchmark.」+ evaluate.sh 命令 + 覆盖板 + **13 行真实 leaderboard**（gpt-5.5 72.3% → …）。
5. **`assets/05-train.png`** — 主页 04·Train **整段**：标题「SFT & RL, any open agent.」+ SFT/RL 切换 + 配置器 + run_sft.sh 全流程。

02–05 都是**主页 section 的整段竖版截图**（自带小标题、叙事完整），全 PNG、只取主页(不碰 blog)。封面(第 1 张)决定点击率。
**重制脚本：** `capture.py`（hero 设备切图，供封面用）· `subset_cjk.sh`（下载并子集化中文封面字体 → `build/fonts/*.woff2`，约 10KB/个；仅新增中文字时才需重跑）· `make_cover.py`（封面 01a/01b + 中文版 -zh，共 4 张）· `capture_sections.py`（section 02–05）。改站点后重跑即可同步。

## 话题标签

正文末已带 10 个（大词 + 精准词混合）。可按当下热度替换 1–2 个精准词（如 #LLM #RLHF）。

## 系列规划

- **01（本篇）** 总览：核心 = 首页 hero 三条（沙盒 / 数据 / 框架），正面框架。
- **02** 沙盒专篇：reflect `blog/kvm-free-osworld`——KVM-free 跑 OSWorld，4.1→0.9 GB、约多跑 4.6×、13 模型分数对齐等真实数字都放这篇。本篇结尾已埋钩子引流到它。

## 来源（和站点保持一致，改站点也要改这里）

| 说法 | 来源 |
|---|---|
| 「任何 agent，任何电脑」slogan + 定位 lead「One open-source platform …」 | 首页 hero H1 + lead（`index.html`；封面、首页、`blog/why-cua-lite` 均已同步此 lead） |
| **「开源」贯穿全篇**：标题「开源平台」→ 首段「是一个把三者集成在一起的开源平台」→ 结尾「希望长成社区驱动的开源 CUA 生态」 | 平台＝现状，生态＝愿景，前后不矛盾。首段必须用**判断句**（CUA-Lite **是**平台），写成「把三者统一在一个平台**上**」会读成 CUA-Lite 和平台是两个东西 |
| 沙盒 — 高效环境 + 30k+ 可验证任务，大规模训练/评测 | 首页 hero 第 1 条，逐句 |
| 数据 — 10+ SFT 数据集 + 前沿 CUA rollout，统一格式，HF 免费 | 首页 hero 第 2 条，逐句 |
| eval / SFT / RL 任何 agent，桌面/浏览器/移动端 | 首页 hero 第 3 条，逐句 |
| 免虚拟机 / 并行 / 一任务两用；转换一次任何 agent 都能训 | `blog/why-cua-lite` 对应三段的 bold lead |
| 15+ benchmark 接入（正文只说「已接入 15+ 个 benchmark」，不再提榜单；实际 11 个有公开榜单） | coverage board · `assets/exps/eval/manifest.json` 非 pending 项 |
| CUAGym / CUAWorld = **我们的** Lite.CUAGym / Lite.CUAWorld（外部 OSWorld 我们复现，Lite.* 是自建） | 首页 + blog belt-tab（`index.html:214-215`），与 red/02 封面命名一致 |

## 发布前检查

- ✅ **GitHub 已公开**（2026-08-22 实测 `HTTP 200`、`gh api private=false`），正文那行 `github.com/cua-lite/cua-lite` 可以保留。此前的 404 阻塞已解除。
- ❌ **`WindowsAgentArena` 已从 benchmark 清单删除**：全仓库 grep（`index.html`、两篇 blog、`assets/exps/eval/manifest.json`）零命中，站点覆盖板 16 条里也没有它 —— 属于已证伪的 overclaim。清单现只留覆盖板上真实存在的 6 个。
- **术语用 `KVM-free`，不要写 `VM-free`**：全站 11 处一律 KVM-free，`VM-free` 是我们自造且主张更大（读者会问「Docker 算不算 VM」）。
- 「分数相当」只绑定在 **Lite.OSWorld** 上（13 模型实测，平均差 ~2.7、最差 5.0，博客原文为 "within a few points"）；不要写成「复现的所有 benchmark 都分数对齐」。
- KVM-free 的具体数字**不在本篇**（留给 02），本篇只说「免虚拟机（KVM-free）」到属性层面。
- 数字若与站点不一致，以站点为准，同步改这里。
- ✅ 原「15+ benchmark 都带公开榜单」的轻度 overclaim **已删除**：正文现在只说「已接入 15+ 个 benchmark」，不再声称都带榜单（实际 11 个有公开榜单，严谨且安全）。
