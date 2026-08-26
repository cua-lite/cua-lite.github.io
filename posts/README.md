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
| 内存 | **under a quarter / 不足四分之一** | 实为 0.9/4.1 = 22% |
| 并行 | **~5× more instances / 并行 ~5×** | 4.1/0.9 = 4.56，四舍五入；**见下方风险** |
| 分数一致性 | **within a few points / 基本一致** | 博客 `:271` 原话 |
| 精确 parity | mean\|Δ\|≈2.7 · worst 5.0 | **内部核对，任何平台的正文都不写** —— 对外一律用「within a few points / 基本一致」 |

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
| 链接 | 页脚 | 仅首尾条 | 可前置（触达 vs 点击自选） | **后置** |
| 语气 | 站点语气，非口语 | 团队第一人称 | 宣告 | **同侪**，需作者披露 |

**通用禁令：** 不要把一个平台的痕迹带到另一个 —— `democratizing`、hashtag、`▪️`、"Built at UC Berkeley and Microsoft" 都不进 Reddit。

## 3. 资产约定

- **`red/` 是唯一的图片来源**，`linkedin/` 与 `reddit/` 的 `assets/` 全是**逐文件软链**（`mode 120000`），不复制。
- **只链英文版**（`*-zh.png` 不进 linkedin/reddit）。
- 动图链自 `twitter/01/assets/`。
- 重制：`red/0N/make_cover.py`（封面）· `capture_sections.py`（站点整段截图）· `scripts/subset_cjk.sh`（中文封面字体 → `assets/fonts/`，共享）。

### 领头图（按证据强度，不按好看）

| 帖子 | 领头 | 理由 |
|---|---|---|
| r/MachineLearning `[P]` | `red/02/04-parity.png` | 复现主张就该用复现图；y=x、13 点、caption 有 n |
| LinkedIn 02 | `red/02/02-footprint.png` | 全套最耐缩，横版不裁，一眼给全 |
| r/LocalLLaMA | `red/01/04-eval.png`（裁到只剩榜单） | 该版块的货币＝开源模型 + 分数 |
| LinkedIn 01 | `red/01/01b-cover.png` | 唯一不空的封面版式 |
| 小红书 | 各自 `01a/01b-cover` | 平台吃图文卡 |

**不要用：**
- `03-hh.png` 进技术帖 —— 标签 pill 盖在真实 Chrome 标签页上、控件被切、两图时间戳与工具栏状态不同（一张论证 identical 的图里全是不 identical）
- `01a/01b-cover` 进 Reddit —— 约 30% 空白且零数字，是该社区判定广告的标志
- `red/01/02-sandboxes` 与 `red/02/05-belt` 同时用 —— 同一条 belt 换了标题

## 4. 反复踩过的坑

1. **别自由发挥** —— 站点和博客有 battle-tested 的句子。写任何标题/bullet 前先把对应的 heading / bold lead 抄出来再压缩。本轮翻车实例：`verifiable rewards`（博客 4 处都写 **tasks**）、把沙盒级两用写成**任务级**（＝污染测试集）。
2. **别让排版删实质** —— 为挤单行/折叠线砍掉「训练」「可验证任务」「benchmark」，实测证明加回去都放得下。**先写完整，量了真放不下再删冗余**。
3. **改一处要扫全篇** —— `democratizing`、`our own`、`~5×` 都出现过只改一处的漂移。
4. **归属** —— OSWorld 等是**外部** benchmark（我们复现），`Lite.*` / CUAGym / CUAWorld 是**我们自建**，措辞里要有 `our own` /「自建」。
