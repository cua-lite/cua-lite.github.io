# CUA-Lite — 小红书 01

小红书系列第一篇。**定位：项目总览，核心就是首页 hero 的那三条**——
「任何 agent，任何电脑 / computer-use agent 需要的一切」：① 沙盒与可验证任务、② 统一数据、③ 统一框架。
正面框架，三条平铺，不由任何一块领跑。KVM-free 只作为沙盒的一个属性一笔带过，具体数字留给 `red/02`（对应 `blog/kvm-free-osworld`）。

**语言：** follow 站点（homepage + blog）的语气——朴素、准确、平行，不用网络口语、不堆 emoji、不造夸张利益点。措辞尽量沿用站点 battle-tested 的说法，每个数字都真实，来源见文末。小红书只借它的**结构**（短段落、清单、话题标签），不借它的口语腔。

---

## 标题（选一个；小红书标题上限约 20 字，字数已标注）

1. ⭐ CUA-Lite：训练与评测 CUA 的开源生态　（22 字，略超；封面已带 brand，可接受）
2. 训练与评测 CUA 的开源生态：沙盒 · 数据 · 框架　（21 字，点出三支柱）
3. 训练与评测 CUA 的开源生态　（13 字，最稳，brand 由封面/正文承担）
4. 任何 agent，任何电脑：CUA-Lite　（＝首页 slogan，配标题卡封面才直观）

> 「生态」是 aspirational 说法（正文结尾也点明是「希望长成社区驱动的开源生态」）；沙盒/数据/框架三支柱与核心贡献放正文首段，标题塞不下全部。

---

## 正文（直接复制这段）

```
CUA-Lite：训练与评测 CUA 的开源生态

训练与评测 CUA（computer-use agent），需要沙盒、数据和一套框架：CUA-Lite 把这三样统一在一处，覆盖桌面、浏览器与移动端，开放共享、简单可跑。

▪️ 轻量沙盒与可验证任务
轻量的 KVM-free 沙盒，内置 30k+ 个可验证任务，用于大规模训练与评测 CUA。例如可高效复现 OSWorld 等 benchmark（分数对齐、可大规模并行），也容纳 CUAGym、CUAWorld 等各类 CUA 训练任务。

▪️ 统一数据
10+ 个 SFT 数据集，以及来自前沿 CUA 的新 rollout，统一为一套格式，在 Hugging Face 免费开放。转换一次，任何 agent 都能在其上训练。

▪️ 统一框架：评测、SFT、RL
一个统一接口，任何 agent 接入任何环境，几乎零改动。同一段交互记录（rollout），评测时给出排名，训练时作为学习信号。已覆盖桌面、浏览器、移动端的 15+ 个 benchmark，都带公开榜单：OSWorld、OSWorld-2、WindowsAgentArena、WebArena、WebVoyager、AndroidWorld、MobileWorld 等。

沙盒、数据、框架三者都在持续扩展。我们希望 CUA-Lite 最终长成一个社区驱动的开源 computer-use 生态: 欢迎带来你的数据集、环境或 agent。

站点 cua-lite.github.io
GitHub github.com/cua-lite/cua-lite
数据 huggingface.co/cua-lite
UC Berkeley · Microsoft

#AI #人工智能 #大模型 #agent #强化学习 #机器学习 #cua #computeruseagent #guiagent #webagent #mobileagent #科研日常
```

---

## 配图（全图片，都在 `assets/`）

轮播顺序 = 封面 + 主页四个 section（对齐主页叙事 hero→沙盒→数据→评测→训练）：

1. **封面（二选一）**
   - `assets/01a-cover.png` — 紧凑版（1080×1040），文字为主，第三条 bullet 自然带出 desktop/browser/mobile。
   - `assets/01b-cover.png` — 竖版（1080×1440），文字上移，底部放 hero 的桌面/浏览器/移动端三设备（带完整边框、标平台名）。
2. **`assets/02-sandboxes.png`** — 主页 01·Sandboxes **整段**：标题「Efficient sandboxes, any task.」+ 说明 + rollout belt（真实桌面 app：calc/files/impress/chrome/gimp/vlc…，两侧淡出）。
3. **`assets/03-data.png`** — 主页 02·Data **整段**：标题「One schema, any dataset.」+ Corpora/Rollouts 双卡 + **真实 HF 数据表**（images/messages/metadata 列、直方图、样本行）。
4. **`assets/04-eval.png`** — 主页 03·Eval **整段**：标题「One command, any benchmark.」+ evaluate.sh 命令 + 覆盖板 + **13 行真实 leaderboard**（gpt-5.5 72.3% → …）。
5. **`assets/05-train.png`** — 主页 04·Train **整段**：标题「SFT & RL, any open agent.」+ SFT/RL 切换 + 配置器 + run_sft.sh 全流程。

02–05 都是**主页 section 的整段竖版截图**（自带小标题、叙事完整），全 PNG、只取主页(不碰 blog)。封面(第 1 张)决定点击率。
**重制脚本：** `capture.py`（hero 设备切图，供封面用）· `make_cover.py`（封面 01a/01b）· `capture_sections.py`（section 02–05）。改站点后重跑即可同步。

## 话题标签

正文末已带 10 个（大词 + 精准词混合）。可按当下热度替换 1–2 个精准词（如 #LLM #RLHF）。

## 系列规划

- **01（本篇）** 总览：核心 = 首页 hero 三条（沙盒 / 数据 / 框架），正面框架。
- **02** 沙盒专篇：reflect `blog/kvm-free-osworld`——KVM-free 跑 OSWorld，4.1→0.9 GB、约多跑 4.6×、13 模型分数对齐等真实数字都放这篇。本篇结尾已埋钩子引流到它。

## 来源（和站点保持一致，改站点也要改这里）

| 说法 | 来源 |
|---|---|
| 「任何 agent，任何电脑」+「需要的一切，开放共享、简单可跑」 | 首页 hero H1 + lead（`index.html:60-61`） |
| 沙盒 — 高效环境 + 30k+ 可验证任务，大规模训练/评测 | 首页 hero 第 1 条，逐句 |
| 数据 — 10+ SFT 数据集 + 前沿 CUA rollout，统一格式，HF 免费 | 首页 hero 第 2 条，逐句 |
| eval / SFT / RL 任何 agent，桌面/浏览器/移动端 | 首页 hero 第 3 条，逐句 |
| 免虚拟机 / 并行 / 一任务两用；转换一次任何 agent 都能训 | `blog/why-cua-lite` 对应三段的 bold lead |
| 15+ benchmark 接入（正文说「都带公开榜单」= 轻度 overclaim；实际 11 个有公开榜单） | coverage board · `assets/exps/eval/manifest.json` 非 pending 项 |

## 发布前检查

- **正文已放 GitHub（`github.com/cua-lite/cua-lite`）——发布前务必确认 repo 已公开**（此前 404）；若仍未公开，就临时删掉这行。
- KVM-free 的具体数字**不在本篇**（留给 02），本篇只说「轻量、免虚拟机」到属性层面。
- 数字若与站点不一致，以站点为准，同步改这里。
- **「15+ benchmark 都带公开榜单」是经确认的轻度 overclaim**（实际 11 个有公开榜单）；若要严谨，改回「15+ 接入，11 个带公开榜单」。
