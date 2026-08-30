# CUA-Lite — launch thread (X)

One standalone announcement plus nine follow-ups. Cross-platform conventions live in
[`../../README.md`](../../README.md); this file only covers X.

| Entry line | What to do with it |
|---|---|
| the ``` fenced text ``` | **This is the post.** Paste as-is — nothing else in the entry gets posted. |
| **Media** | What to attach from `assets/`. One per post. |
| **Alt** | Goes in X's "add description" box, not in the post. |
| **Source** | Which page the wording came from, for keeping this in sync with the site. |
| **Why here** | Why the post sits at this position. Review note, never posted. |

## 写作规约

**约束优先级 —— 冲突时从上往下让步，不许反过来:**

1. **事实与归属正确。** 别人的名字、别人的工作，错一个就没有第二次机会。
2. **可理解:名词齐全,指代有落点。** 不许用量词或指示词代替名词(`Each` / `many` / `Four so far` / `these` / `That base` / `of ours`)。**删名词句子仍然合语法,所以我自己读得通 —— 只有新读者会发现它不再可理解。这是这份文件上重复次数最多的缺陷。**
3. **每条经得起被单独引用。**
4. **核心提前。**
5. **字数 / 折叠线 —— 最弱的一条。** 前四条与它冲突时,**一律牺牲字数**。为挤进 280 而删掉的东西,这份文件上已经包括:`heavy` · `SFT or RL` · `across desktop, browser, and mobile` · 收尾帖的第三个 ask。**没有一次值得** —— 前三样后来都加回去了(现在分别在 gap 帖和 post 1)。

从四份审核（冷读者 / 敌意同行 / 传播 / 只读首帖）里反复验证出来的，不是通则。**改任何一条帖子之前先读 1–4。**

1. **前 ~280 字符换取那一次点击。** 里面必须有**有量级的数字**或**一句可被反驳的主张**；使命宣言换不到点击。曾把 96/280 个字符（34%）给了三行 URL，冷读测试给出「会点 Show more 吗？3/10」。
2. **链接紧贴折叠线以下，不是以上。** 链接在首屏会**和 Show more 抢点击** —— 好奇的人点了站点就再也不会展开。两个参考帖（asapzzhou、RSI-Exam）都不把链接放进首屏。例外：收尾帖（现 post 10）是 CTA，链接优先靠前 —— 但**不为它砍内容**（见「长度与折叠线」）。
3. **第一句是 `\paragraph{}`：点出这一段讲的是什么东西。** 不是「以贡献开头」也不是「以后果开头」——**这两个方向我都摇摆过，都不对，是点名主语**。三个反例，全部真实出现过：
   - `No agent loop, no VM setup, no eval scripts` —— 三个否定词，读者看完不知道你造了什么
   - `GPT-5.5's rollouts can fine-tune Qwen3-VL` 作首句 —— 那是这一段的**例子**，主语是 LiteSample
   - `That base runs a family…` / `Three more of ours…` —— 用指示代词/所有格代替名词
   **句式雷同靠换句法解决，不靠放弃点名。** 当前 posts 4/5 都用定义式（`lite.gym is CUA-Lite's one agent–environment interface…` / `LiteSample is CUA-Lite's trace format…`）—— 这是**刻意**的：站点标语本就是 `one schema, one interface, one command`，两者是并列的两个核心抽象。其余各条句法各不相同。判据：读完第一句能不能说出这段在讲哪样东西。
4. **每条必须经得起被单独引用。** X 上单条被引用、截图、算法推送远多于按顺序读，所以：不许以 `That` / `It` / `Both` / `of ours` / `the … above` 起句；**每条至少出现一次 `CUA-Lite`，且在折叠线以上**（重排前的 posts 3/4/6 曾全篇零次，而其中两条恰好装着最可能被截图的东西）。也不许用 `Gap N —` 这类只有读过 gap 帖（现 post 3）才懂的标签。
5. **痛点占一句，不占一段，而且放在贡献之后。** post 3 是唯一例外 —— 列三个 gap 就是它全部的职责。post 7 的痛点半句 `sandboxes are heavy` **已经不在正文里**（见优先级 5 的删除清单）——对照物的角色现在由 `in a Docker container instead of a VM` 自己承担；post 4 不写痛点，直接给交付物（`You bring the agent; CUA-Lite's framework ships the rollout loop, the sandboxes to run it in, and the eval and training stack…`）—— 早先那版 `A new project writes none of the usual plumbing — no agent loop, no VM setup, no eval scripts` 把贡献写成了三个「没有」，读者原话：「我们这个是 contribute 了一个空气吗」。
6. **跨帖重复无所谓，首屏内重复是致命的。** 没人读完九条，重复反而是好事 —— 而且规则 4（每条独立）**要求**每条自带价值主张，两者本就冲突，冲突时以规则 4 为准。**只有两种重复要删**：① 同一个词/主张在**同一个折叠线内**出现两次；② 一整句逐字出现在两条帖子里，且其中一条是那句话的**唯一卖点**（post 1 和当时的训练帖曾同以 `GRPO, GSPO and more, on Slime` 收尾；现在只有 post 9 这么收）。
7. **指代可以跨段，但不能跨帖，也不能指向被否定的东西。** 同一条帖子里第二段接第一段是正常散文；真正的缺陷是 ① 指向另一条帖子（`Three more beyond Lite.OSWorld` 只有读过 Lite.OSWorld 那条才成立；`that same interface` / `the same format` 同理 —— `check_thread.py` 的 ORPHAN-SAME 会报）② 指向一个刚被否定掉的名词（`no agent loop` 之后写 `The same loop`）。
8. **相邻两条不许句法雷同 —— 隔开的可以。** 排比是好事，连着两条同一个句法就成了规格表。要换就换**句法**（同位语、祈使、数字打头），不是换动词 —— 重排前的 posts 3/5/6 曾动词各不相同而句法全是「主语 + 及物动词 + 冒号 + 展开」。当前 4/5 的定义式平行是例外，理由见规约 3。
9. **一个具体画面胜过三句抽象。** `NASA's GMAT flying spacecraft, PyMOL turning proteins` 是全篇唯一能让拇指停住的东西 —— 它曾经在折叠线以下。
10. **致谢上游是加分，不是成本，但先核对是哪个上游。** 在 X 上点名会换来转发，含糊其辞会换来公开质疑。**「ScaleCUA」有两个同名项目**：环境 `Lite.ScaleCUA` 是 THUDM 的 SCALE-CUA，SFT 语料才是 OpenGVLab 的（见 `posts/README.md` §4 与代码库提交 `0598e30`）。**这条我错过两次，方向相反。**
11. **@mention 是性价比最高的未使用杠杆** —— 纯文本点名不通知任何人。发布日现查 handle，**不许猜**：错的 @ 比没有更糟。
12. **post 1 的首条回复是全场第二高曝光位** —— 放证据图 + 一行安装命令 + 一句第一人称，别空着。

## 其余约定

**加粗** — X Premium 的长贴支持粗体，而这条 thread 的多数帖超 280（posts 2/9/10 不超）、本来就要 Premium，所以粗体可用。**但它不是 markdown**：在 X 编辑器里选中文字点工具栏，`**星号**` 直接粘贴会显示成字面星号。所以 ``` 块保持纯文本，要加粗的短语写在每条的 **Bold** 字段里，发布时照着点。**判据：标题 + 加粗连起来读，就是这一段的全部重点**（作者原话）。所以 ① 不加粗标题里已有的话 —— 那等于零信息（曾把 gap 帖的 `CUA-Lite is built to close three gaps` 和榜单帖的 `one script evals any agent on any benchmark` 加粗，两句都是标题的复述）；② 每帖 1–3 处，够撑起那句话就停 —— 满屏加粗等于没有加粗。**致谢帖一处都不加**：在一串名字里给部分人加粗就是厚此薄彼。

**语气** — 团队第一人称，平实、技术。无 hashtag。唯一的 emoji 是 post 1 的 🧵（X 的 thread 信号，不是装饰）；项目符号用站点的 `▪️` 和 `·`。

**文案来源** — 取自站点和两篇博客，不自由发挥。post 1 的骨架来自 `posts/red/01` 的英文版，其余各条复用主页的主张和博客的 bold lead，只补把三个页面串成一条 thread 的连接词。

**编号** — post 1 不带编号（它是完整的独立公告，🧵 已经在说「下面还有」）。posts 2–10 用 `[N/10]`，方括号让数字读作标签而不是句子的开头。**分母是 10，含无编号的 post 1** —— 读者在无编号的公告后看到 `[3/10]`，会推断刚才那条是 1/10；改成 1–9 反而让人以为漏了一条。

**长度与折叠线** — X 在约 280 字符处折叠（URL 一律按 23 计）。**内容优先级最高，折叠线是 optional 的。** 不要为了让链接露出来而损害可读性 —— 作者原话：「不要为了这种 optional 的损坏了内容的可读性」。**post 10 整条 246 字，不折叠，两个链接都在首屏** —— 早先这里写「链接落在折叠线以下」，那是重排前的旧状态，实测已不成立。**规则是「核心提前」，不是「压进 280」**：为挤进折叠线而截断，代价大于收益，因为点开的人拿到的是残篇。实测（2026-08-30）：post 1 = 1342，posts 2–10 = 185–696，致谢帖 = 1390 —— post 1、致谢帖和 posts 3–8 需要 Premium。**posts 2（206）、9（185）、10（246）不折叠**，其余都折叠，所以那几条的核心必须在首屏内 —— 这几个数**不要手写**，跑 `check_thread.py` 重取。

**配图** — 每条一个，post 9 例外（SFT + RL 两张），全部截自文案所出的同一批页面（站点的图**就是**论证本身），不新造视觉。重制：`uv run python posts/twitter/01/make_assets.py`。

**链接** — post 2 四个全给（那是它全部的职责），post 5 重复 Hugging Face（traces 是那条的诉求），post 10 收尾两个。post 1 一个都不放 —— 链接在首屏会和 Show more 抢点击，见写作规约 §2。其余各条一个都不放：X 会压制正文中段的链接。

## Pre-flight

1. **仓库还没有 LICENSE**（`ls LICENSE*` 与 `pyproject.toml` 都没有），而 thread 里 `open` 出现多次（post 1 的标题与结尾、post 2 的 `open platform`）、post 10 还在招 PR，同时我们在再分发 Apache-2.0（OSWorld、CUA-Gym）和 MIT（gym-anything）的工作。**这条没有文案层面的解法，发布前必须补。**
2. **备好被问时的答案**（不进正文）：VM↔容器差距小于我们自己两次 run 的波动（同一 env 上 Qwen3-VL-32B 曾是 19.0 和 35.8 —— 那是不同 agent 配置，备好 config diff）；parity 两侧是 325 vs 321 个任务；Lite.ScaleCUA 与 Lite.CUAGym 目前只有 train split。
3. **发布前复核两个数**：「15+ benchmarks integrated」（覆盖板）与转换语料数 —— **按 `README.md:245` 实际列出的语料算，当前 9**，不要数 `preproc/` 的目录数（那里的 `jedi` 第一行写着 dropped in its entirety，是一份复盘，不是语料）。**不要再引入「11 个有榜单」这类对我们不利的精确数** —— 已按作者要求改为 `the leaderboard is live`。
4. `cua-lite.github.io`、`huggingface.co/cua-lite`、`github.com/cua-lite/cua-lite` 于 2026-08-22 均返回 200。发布当天重测。

---

## At a glance

The spine is the framework first, then the open resources it lets plug in. Post 1 states the
three things a CUA needs and how each is fragmented today; post 3 restates those three gaps in
the order the thread answers them. Posts 4 and 5 are the two abstractions — one interface, one
format — and post 6 is their first concrete payoff, 15+ benchmarks behind one command. Posts 7
and 8 are the sandboxes: OSWorld is the environment everyone already knows, so cutting its VM is
the cheapest way into the family. Post 9 spends the traces on SFT and RL. Post 1 ends on the ask;
post 10 opens on the same ask and then gives the mechanism — invitation first, `each plugs
into …` only once the reader has seen the nine posts that earn it.

**Sandboxes used to lead** (posts 4–5, before the framework). They were moved behind the two
abstractions because the thread's real ask is contributions, and nobody can contribute an
environment without an interface to conform to, or traces without a format. The cost is real and
recorded: the hardest evidence — 13-model parity, the footprint table — now lands at post 7
instead of post 4. Post 6 exists partly to pay that back, giving a concrete result immediately
after the two abstract posts.

### 重排后的写作决定（2026-08-30 定下，改动前先读；虽然从 post 1 起，但下面的术语与顺序规则约束全线）

叙事从「三支柱清单」改成「统一层 → 它解锁的东西」。核心论点是 **call for contributors**：
没有接口就没法贡献环境，没有格式就没法贡献 trace —— 贡献这件事字面上依赖那两层先存在，
所以它们必须在前。沙盒和 trace 是「这个框架接进来的开放资源」的例子，不是并列的第三、第四样东西。

- **主张句用冒号带出并列，不用句号断开。** `fragmented: A; B; C` / `to close all three: A, B, C`。
  三段同一个句法，读者一眼知道每段在数同样三样东西。
- **但一句话只干一件事。** 问题段一度压成 55 词单句（一个冒号、两个分号、三个 and、一个 so），
  结构对而读起来像规格书。拆成四个短句，因果留在句内，不跨句配对。
- **CTA 在三个 ▪️ 之前**，不在末尾。顾问原话：防砸位置太靠后，要在铺垫内容之前满足。
  这条被改回末尾过一次，别再犯。
- **不用 `data` / `dataset`。** verifiable tasks 和 grader 也是 data，歧义在这里是致命的
  （顾问：data often is not just SFT data）。统一用 `traces`。
- **标签宽，紧跟的定义句准。** `▪️ Traces` 后面第一句就是 `Screenshots paired with the actions
  to take — one step or a whole trajectory`（主页原话）—— 单步的 grounding 标注和整条轨迹都被它涵盖。
  准确性由定义句承担，不由标签承担。
  ⚠️ 别写 `rollout traces`：`preproc/` 里 Mind2Web、GUIOdyssey、OpenCUA(AgentNet) 是**人类**演示，
  Aguvis stage 1 是单步标注，都不是 agent 跑出来的。
- **枚举顺序必须和三个 ▪️ 一致：benchmarks → sandboxes → traces。**
  15+ benchmarks 属于框架 ▪️（它的第一条子项就是 Eval），框架排第一，所以数字也排第一。
  这条丢过两次：改对之后重写别的段落时又掉回去了。改任何一段都回来核一遍这个顺序。
- **三样东西要写出内含物**：`environments (sandbox, tasks, verifier)`。
  这个括号同时干两件事：(a) 告诉读者环境不只是一个容器；
  (b) 把 **tasks 和 verifier 明确归到环境里**，于是 traces 只剩训练数据这一种意思 ——
  正是顾问那条「data 也包括 tasks 和 grader」的歧义的解法，比换名词管用。
  但别在同一句里再套一层破折号列出管线的四件事 —— 那四件事在 (3) 和解法句里各出现一次就够，
  一句话里一个括号是清楚，加一个破折号列表就是复杂。
- **机制归定义它的那一条。** `a standardized action space per platform — desktop, browser and
  mobile` 原本在 post 6（讲榜单）的底部，是个迟到的解释；它属于 post 4，因为那是定义接口的地方。
  `one interface` 单说太抽象，读者不知道统一的是什么。
- **管线那一层叫 `framework`，不叫 `pipeline`。** 项目自己的词：post 3 是
  「No **framework** standardizes eval, SFT or RL」，旧 post 1 是「one unified **framework**」。
  写 `pipeline` 就是为同一层另造一个词。
- **三样东西之间要有因果，不是并列清单。** `a framework that drives those interactions and
  **thus** evaluates and trains the agent` —— `thus` 把链条点明：框架驱动交互 → 因而产生 traces
  → 因而能评测和训练。写成 `a framework that connects them` 等于什么都没说。
  三项之间也要互相钩住，不是三个独立名词：
  `environments **for agents to interact with**` → `traces **of those interactions**` →
  `a framework that **drives them**`。每一项都回指前一项，读者不用自己建立联系。
- **绝不点名 rollout 的教师模型。** 用 OpenAI 的输出微调竞品模型违反其条款，
  所以 rollout traces 的来源一律含糊：`fresh rollouts from frontier CUAs`（站点原句）。
  ⚠️ 事实核验会指出「rollouts 全是 GPT-5.5，复数不准」并建议点名 —— **不要采纳**，
  这里的含糊是有意的。这条已经被「优化」回点名一次。
  ⚠️ 也不要写 `frontier **open-weight** CUAs`：那是个可证伪的事实断言，而且是假的 ——
  README:246 写着「(GPT-5.5 rollouts)」，五个 rollout 数据集全出自闭权重模型。
  含糊（`frontier CUAs`）是真的；具体（`open-weight`）是假的。避 policy 靠含糊，不靠改事实。
- **「平台」是既成事实，「生态」是结尾的愿景**（`posts/red/01/README.md:14` 的裁定）。
  post 1 的钩子说 `the open platform` 是对的；不能同时断言 `CUA-Lite is an open ecosystem`，
  那会和 post 10 的 `We hope CUA-Lite becomes … ecosystem` 自相矛盾。
- **数字要按「HF 上实际有几个仓库」算，不是按 `preproc/` 目录数。**
  公开语料只有 **9 个**（README:245；`preproc/jedi` 第一行写着 dropped in its entirety）。
  加上 5 个 rollout 数据集，HF 上共 14 个 —— 所以 `10+ trace datasets on Hugging Face` 成立，
  而 `10+ public sources of traces` 不成立。
- **这两条不采纳（和仓库自己的说法一致，不是推文夸大）：**
  `one command` —— README:32 就是「One command evaluates any agent on any benchmark」；
  `any agent to run in any environment` —— README:27 就是「drop any agent into any env」。
  审核指出的 step_gui 只支持 mobile 等，是**模型能力**边界，不是接口边界。
- **术语全局一致，优先于避免重复。** 同一件事只用一套词，即使一段里出现两次。
  `expensive VM sandbox per verifiable task` ↔ `optional VM-free sandboxes carrying 30k+
  verifiable tasks` —— 问题和解法用同一组词，对照关系读者不用自己拼。
  写成 `virtual machine per task` 就是为同一件事另造一套词。
  受这条约束的词：environment / sandbox / verifiable task / trace / rollout / eval, SFT, RL /
  benchmark。**别为了句子好听换同义词。**
- **不要三个 ▪️。** 那是旧「三支柱」形状的遗留；新叙事里三个统一已经在解法句里点名了，
  ▪️ 只是把 posts 4–9 的内容提前说一遍。带 ▪️ 是 345 词，在 X 上是一堵 "show more" 墙；
  去掉后 160 词，读者会读完再往下翻。
  代价（记下来，别当成疏漏）：post 1 因此不再点名 `lite.gym` 和 `LiteSample` —— 它们分别落在 posts 4 和 5。
  （早先这里还写「`GPT-5.5 → Qwen3-VL` 那个例子落在 post 9」：该例子**任何一条里都没有**，
  而且点名教师模型本就违反上面那条规则。）
  对第 1 条的 layperson 读者来说，`one interface` 比 `lite.gym` 说明的更多。
- **代表性 benchmark 每个平台各取一个**（OSWorld / WebArena / AndroidWorld），
  正好呼应同句句尾的 `across desktop, browser and mobile`，不是随便挑三个有名的。
- **`optional` 不能删。** 它是主张本身：框架不绑定我们的沙盒，你自己的容器也能接。
  （`— yours or ours —` 那种额外解释是多余的，`any environment` 已经够。）
- **钩子只说这是什么，不列架构。** 架构下一段就讲了。旧钩子的尾巴 `with open sandboxes, data
  and infra` 是旧顺序的三个名词，重排后对不上，已去掉 —— 现在正好等于论文标题原句。
- **agent 和 environment 之间要有动词，但不是 `drive`。** 你 drive 一台电脑，不 drive 一个「环境」。
  用 `run in`（框架 ▪️ 里的原句），两处同一个动词。`agents driving computers` 留在问题段是对的，
  那里宾语是具体的电脑。

| # | Beat | Media |
|---|------|-------|
| 1 | Introducing CUA-Lite — the whole argument, standalone | `01-hero.mp4` portrait (`01-hero-wide.mp4` = landscape) |
| 2 | An open platform — site, code, traces, leaderboard | none (X cards the last URL) |
| 3 | Computer-use agent resources are fragmented | `02-fragmented.mp4` |
| 4 | One framework: eval, SFT, RL | `03-litegym.mp4` |
| 5 | One format, any dataset | `04-litesample.mp4` |
| 6 | One command, any benchmark | `05-leaderboard.mp4` |
| 7 | VM-free OS(World) at Scale | `06-vm-tax.mp4` |
| 8 | Sandboxes & verifiable tasks | `07-sandboxes.mp4` |
| 9 | SFT & RL, any open agent | `08b-rl.png` |
| 10 | Call for contributors | `09-card.png` |

Spares (replies or a quote-tweet, not part of the ten) are listed under **Posting notes**.

---

### 2026-08-30 第二轮（重排收尾）逐条定下的

- **术语规则约束全线，不只 post 1。** 第一轮只把 `data`/`dataset` 换成 `traces` 改了 posts 1 和 3，
  posts 2/5/9/10 留着旧词，post 10 甚至留着**旧三元组**（`Sandboxes, data, and framework`）。
  改一处术语就要 `check_thread.py` 全跑一遍，别只看手上那条。
- **post 4 的标题说 framework，正文必须出现 framework。** 原文整段只给 lite.gym（interface），
  读者分不清 lite.gym 就是 framework 还是 framework 另有其物。现在第二句写
  `CUA-Lite's framework ships the rollout loop…` —— 让标题的词在正文里落地。
  lite.gym 那句是作者亲手写的，一字不动。
- **post 6 的 Desktop 少了 Lite.OSWorld。** 站点 coverage board（`index.html:288-292`）是
  OSWorld / **Lite.OSWorld** / OSWorld-2 / CUABench，`manifest.json` 里 `osworld` 和 `lite.osworld`
  是两个独立条目 —— 榜上两个都有。漏掉它，紧接着 post 7 又把 Lite.OSWorld 当主角，
  读者无法判断榜上那个 OSWorld 是原版 VM 还是 Lite 版，而这正是 parity 主张的落点。
- **post 7 不许用 `introduces`。** 重排后 posts 1 和 4 都已经提过 sandboxes，
  第七条再「introduce」会让读者以为自己漏了一条。同时删掉重复的句尾
  `on a fraction of the hardware resources`（两句连着同一个结尾）。
- **post 7 也不许写成 `CUA-Lite's own sandboxes are VM-free`。** 试过，作者当场驳回：
  「搞得像我们只支持 VM-free」。CUA-Lite 跑的 15+ benchmark 里多数用的是各自原本的环境
  （含 VM 的 OSWorld），VM-free 沙盒是**额外提供的一个选项**，不是唯一形态 ——
  这正是 `optional` 那条规则（见上）说的：框架不绑定我们的沙盒。
  现在写 `CUA-Lite **also provides optional** VM-free sandboxes for hosting environments —
  efficient, highly optimized containers …`：`also` + `optional` 两个词一起挡住排他性读法。
- **不许用 `that same interface` / `the same format` 这类回指。** 试过一次，
  `check_thread.py` 的 ORPHAN-SAME 当场报出来：单看那一条的读者不知道 same 指什么。
  post 10 现在写 `CUA-Lite's one interface, one trace format and one framework`。
- **post 10 必须出现 `CUA-Lite`。** 改写 CTA 时整条把项目名删干净了，R4 硬失败。
- **post 1 与 post 10 的分工：post 1 = 愿景 + 邀请，post 10 = 邀请 + 机制。**
  两条都以 `Bring an environment (sandbox, tasks, verifier), traces, or an agent` 落地，
  但 post 1 接的是 `we hope it becomes a community-driven open-source CUA ecosystem`（愿景），
  post 10 接的是 `each plugs into … exactly like everything above`（读完九条之后才成立的机制）。
  不要让两条说同一句话。
- **`10+` 在 posts 1 和 5 必须数同一样东西。** 曾经 post 1 是「HF 上 10+，rollouts 在**之外**」，
  post 5 是「converted 10+，rollouts 在**之内**」—— 后者按 `README:245` 只有 9 个，不成立。
  现在两条都数「HF 上的 10+ 个仓库」（9 语料 + 5 rollout）。
- **post 5 的标题刻意和站点 h2 差一个词**（站点 `One schema`，这里 `One format`）：
  正文统一成 `trace format` 之后，同一个东西不能在相邻两行有两个名字。站点若改，同步回来。

- **解决句要用问题句的原词回答**（作者 2026-08-30 定）：post 1 第二段的 gap 1 是
  `every environment exposes its own **interface and action space**`，所以第三段答的是
  `one standardized **interface and action space**` —— 名词一一对上，读者不用自己建立映射。
  同理 `standardized` 是 gap 里「各家自己一套」的反义词，不是修饰性形容词。
  （作者原句写的是 `action space**s**`，`one … spaces` 数不一致，且第二段用的是单数，已统一为单数。
  「每个平台一套」这层精确度由句尾的 `— across desktop, browser and mobile` 和 post 4 承担。）

### 这一轮修掉的**文档**缺陷（比文案更容易烂）

- **beat table 的 4–8 行还是重排前的顺序** —— 它是全文唯一的索引，却和它索引的东西不一致。
  帖号写进散文一定会烂：这份文件里还有十几处「post N」是旧编号，见「犯过的错」。
- **`check_thread.py` 的硬编码帖号让门禁误报。** `if i != 9` 是给 CTA 开的链接豁免，
  重排后 CTA 是 post 10，于是脚本把 post 10 **本来就该有**的链接报成硬失败。
  已改成按标题匹配（`titles()` / `is_cta`）——**规则要 key 在「这条是什么」，不是「这条是第几」。**
- **一条已被作者否决的建议以「规则」的形式活在文件里。** 「点名 GPT-5.5 反而更有力」
  就写在「绝不点名教师模型」下面三行，同为祈使句。下一个人照着做就会重犯 policy 问题。已删。
- **三个「实测」数字全是错的**：写着 posts 2–10 在 333–741、九条全部折叠、post 10 链接在折叠线以下；
  实测 185–696，posts 2(206)/9(185)/10(246) **根本不折叠**，post 10 两个链接都在首屏。
  这类数**不要手写**，跑脚本重取。
- **致谢的注记和正文对不上**：`@ServiceNowRSRCH` / `@trycua` / `@Seed_TARS` / `@osunlp` 都已经发出去了，
  注记却还把它们列在「刻意用纯文本」和「deliberately left out」里，其中一条还叮嘱审核者
  「不要报成缺陷」—— 等于主动压掉真缺陷。@ 的条数写 27，实测 48。
- **`@GoogleResearch` 的指令会让人重犯已修的错**：一处写「AndroidWorld 走 @GoogleResearch」，
  六十行外的表格记着「**曾误用 `@GoogleResearch`**」并已改为 `@GoogleDeepMind`。已统一。

## 我在这份文案上犯过的错（同类还会再犯，先读这个）

| 失效模式 | 实例 | 代价 |
|---|---|---|
| **凭推断写规则，还写进共享 README** | 「`Lite.*` / CUAGym / CUAWorld 是我们自建」 | 用别人项目的原名声明自有，**自动复制到 4 个文件** |
| **措辞和产物拿反了** | 01 里**已通过审核的句子**我不用、自己另写（更差，还写出过事实错误：ScaleCUA 的说明、30k+ 挂在 generate 上）；01 里的**素材文件**我却直接软链过去用（名字带 01 的帖号，而且漏了 blog2 自己的 `figure.belt-fig`，02 竟在用 blog1 的图）| 判据是反的：**措辞复用**（经过审核，重写只会更差）·**产物回源重制**（生成成本低，且出处本身就是意义）。漏图的根因同「只查一个文件」——我枚举的是「01 的素材里哪些出自 blog2」，不是「blog2 有哪些图」 |
| **按原文篇幅分帖，不按论点分量** | 02 照 blog2 的两节分帖：§1 长 → 4 帖，§2 短 → 1 帖。但**两节的长短和重要性恰好相反** —— 演示需要证据所以长，结论本来就短 | 例子被放大成主角，读者以为在发布一个 OSWorld 移植版。作者原话：「lite.osworld 只是一个例子让大家理解我的 sandboxes，而不是核心」 |
| **约束一消失就丢结构** | 01 的 Lite.OSWorld 帖（现 post 7）只有一帖空间，压缩强迫我写成「总述 → `Lite.OSWorld is the first of them`」，层级是对的；02 有六帖可填，反而让例子膨胀 | **空间变大时要主动重申层级**，不能指望篇幅限制替我把结构摆正 |
| **手边有已通过审核的句子却另写一个** | 01 post 4 的 `CUA-Lite introduces lightweight, VM-free sandboxes behind one interface: they reproduce public benchmarks and generate verifiable tasks…` 正是 02 要的论点句，我却自己另写，而且写成了机制先行 | 写新 thread 前**先在既有 thread 里搜同一个论点**。这是「绕开现成资源自由发挥」在跨 thread 上的变体 |
| **成批修改后不复审，靠下一轮 agent 兜** | 02 上第一轮审出的问题我一次性改完，第二轮冷读查出 **15 条,全部是我这次改出来的**；再改 18 处后又需要一轮 | 审核轮次永远收敛不了 —— 每轮查的是我上一轮的回归，不是原始缺陷。**改完先自查，再送审** |
| **可机械化的检查靠人反复读** | 02 那 15 条里 4 条同属一类：注记引用了已被删除的句子（Why here 引 `The benchmark itself is untouched`、Bold 引已改写的短语） | 这类能发出去只因为「改文案」和「改引用它的注记」是两个动作，第二个总被跳过。**已做成 `STALE-NOTE` 检查** —— 与其多派一轮 agent，不如把这类写进脚本 |
| **改脚本前不先验证假设** | 为修循环接缝加「首尾对称裁切」，实测接缝从 13.6 恶化到 45.4（`2×head` 不是整数个动画周期）；litegym 那条也是试了五次参数才去算几何不等式 | 都是花 20 秒 ffmpeg 就能先测出来的。**先测假设，再改代码** |
| **替换锚点匹配到同名行** | 给 `check_thread.py` 加检查时，锚点 `body = README.read_text()` 匹配到了 `posts()` 里的同名行，把函数体覆盖，连带丢了 `sentences()` 和 `audit()` | 改完必须验函数完整性。这次靠 `hasattr` 全量检查发现，已从 01 的版本重建 |
| **只核了 handle，没核 handle 与项目的关系** | agent 确认「`@MicrosoftAI` 是 microsoft.ai 的账号」，我就写成 `Fara (@MicrosoftAI)` —— 但 Fara 是 **Microsoft Research** 发的，microsoft.ai 是另一个部门 | 大公司必须确认**是哪个部门发布的**，账号真实 ≠ 归属正确 |
| **给 harness 的作者记了 benchmark 的功** | `lite/gym/envs/browsergym/README.md` 顶上链接的是 ServiceNow/BrowserGym，我据此写成 `ServiceNow's WebArena` —— WebArena / VisualWebArena 的原作者是 CMU（`web-arena-x`），ServiceNow 只是我们跑它用的 harness；VisualWebArena 还整个漏了 | 致谢里张冠李戴。**归属要查 bibtex 的 author 字段，不是 README 顶上的链接** |
| **抄最近的来源，不抄权威来源** | 从仓库里一处过时链接抄了 `THUDM's ScaleCUA` | 把上海 AI Lab 的工作安给清华；**为修一个归属错误引入了另一个** |
| **只查一个来源就断言「没有」** | 只 grep 网站 → 误删 WindowsAgentArena；只 grep 网站 → 写下「链接不许现编」，漏了代码库里现成的七个 | 删掉真事实 / 该链的没链 |
| **没看图就写图注** | 当时的 `03-data.png`（该文件已不存在；`03-` 现在是 litegym）写成「真实 HF 数据表」，实为我们自绘的仿制界面 | 差点当成证据发出去 |
| **用文档标准优化社交文案** | 反复消灭跨帖重复、追求归属精确，而折叠线里一个数字都没有 | 首屏 3/10 |
| **过度纠正** | 修 `of ours` 时把细节清单提到第一句；修「链接太靠后」时把 34% 首屏给了 URL | 两次都把问题换成了另一个问题 |
| **一个测量说成两个** | `under a quarter of the memory` + `~5× more instances`（4.1/0.9 = 4.56） | 读者原话：「我发现之后回头怀疑 parity 那个数字」 |
| **改写时把主语丢掉** | 博客 `The VM-free container isn't just for OSWorld` → 我写成 `That base` | 悬空指代，第三次犯 |
| **把审核清单当待办** | 逐条「修复」评审意见，把 red 里久经检验的两个 bullet 都改坏 | 读者原话：「red 里面这个挺好的啊；你为什么一定要改」 |
| **正文逐处署名** | 为满足「每次提及都署名」在正文撒 `xlang-ai's` / `CMU's` / `THUDM's` | 注意力被从「我们做了什么」引开；正确做法是**只在致谢帖逐个 @** |
| **自己发明判据，而不是先问判据** | 加粗我定的是「只加可验证的主张」，作者的判据是「标题+加粗连读就是重点」—— 按后者，我选的两处**恰好复述了标题**，零信息 | 同一模式一轮内三次（加粗 / 内容 vs 折叠线 / 推文语法）。**判据是作者的，方案才是我的** |
| **改一处而不查引用它的散文** | 这次重排后，`写作规约`、`其余约定`、`Pre-flight`、`At a glance` 里有 **13 处**硬编码的帖号立刻失效：「post 1 三个链接全给」（post 1 现在零链接）、「分母保持 9」（标记是 /10）、「post 2 是唯一例外」（gap 帖是 3）。`check_thread.py` 只查正文和 Bold/Why here 注记，查不到散文里的 `post N` | **帖号写进散文就一定会烂。** 引用位置，不引用编号：写「gap 帖」「训练帖」「收尾帖」而不是「post 3」「post 9」「post 10」。重排后必须 `grep -n 'post [0-9]'` 全文过一遍 |
| **只 grep 一个文件就断言「源码里没有」** | `expert` 在 `js/belt.js`；`whole field builds on it` 在我从没读过的 `blog/why-cua-lite/`；语料数横跨 `README.md:244` 与 `preproc/` | 三次误判，其中两次我据此删掉了站点原文。**先枚举源文件集合再下结论**，不是「careful 一点」 |
| **把 subagent 的结论当待办执行** | agent 说「沙盒帖首段是 Lite.OSWorld 帖的主语句」（当时编号 3 与 4；现为 8 与 7），我就删了 —— 作者当场指出 post 3 讲的就是沙盒，OSWorld 只是例子 | 审核结论要先过一遍「这和作者已定的决策冲突吗」，再决定采不采纳 |
| **改一句不读依赖它的下一句** | `the same tasks and evaluators` / `the same base` 两句**本身没坏**，是我删改了给它们做先行词的上文 | 语法完好、指代落空，我自己读不出来 → 已做成 ORPHAN-SAME 机器检查 |
| **检查器假阳性反推文案** | 门禁把 `These sandboxes`（带名词）判成裸指代 | 差点把文案推回它刚被修掉的 `They re-host`；**报警先判是文案错还是规则错** |

**共同点：我最有把握的那条，恰恰是我从没回源头查过的那条。**

## The thread

### 1 — Introducing CUA-Lite

```
Introducing CUA-Lite 🧵 — the open platform for computer-use agents.

Training and benchmarking CUAs takes three things: environments (sandbox, tasks, verifier) for agents to interact with, traces of those interactions, and a framework that drives them and thus evaluates and trains the agent. Today all three are fragmented: (1) every environment exposes its own interface and action space, and most of them need an expensive VM sandbox per verifiable task; (2) there is no standard protocol for recording those traces, so every source ships its own format; and (3) with neither settled, every project builds its own framework for eval, SFT and RL.

So we are introducing CUA-Lite to close all three: one standardized interface and action space for any agent to run in any environment, one standardized format for every trace, and one framework for eval, SFT and RL — across desktop, browser and mobile.

Open resources then plug straight in: 15+ benchmarks behind one command (OSWorld, WebArena, AndroidWorld, and more), optional VM-free sandboxes carrying 30k+ verifiable tasks, and 10+ trace datasets free on Hugging Face — public corpora converted once into the standardized trace format, plus fresh rollouts from frontier CUAs.

CUA-Lite keeps growing — we hope it becomes a community-driven open-source CUA ecosystem. Bring an environment (sandbox, tasks, verifier), traces, or an agent.
```

**Bold** `one standardized interface and action space for any agent to run in any environment, one standardized format for every trace, and one framework for eval, SFT and RL`

**Source** `posts/red/01/README.md`'s English version, minus the hashtags — the most-revised copy
we have, so post 1 uses it whole rather than re-cutting it. **One deliberate divergence from red:**
the opening line. red's is `Introducing CUA-Lite — one open-source platform to train and benchmark
CUAs`, but the sentence directly under it already says `Training and benchmarking CUAs (computer-use
agents) takes three things` — the verb pair, the full term and the triple all repeat inside two
lines, at the most expensive position in the thread (X folds at ~280 chars). This opening drops the
repeated half and adopts the site's own line instead, so the first thing a reader sees matches the
`<title>`, the og card, the citation block and the paper subtitle. red/01 still carries the older
wording in both its English and Chinese versions; propagating it there is a separate decision,
because red's Chinese title is entangled with its title-options list.
**Media** `assets/01-hero.mp4` — one agent driving a desktop, a browser and a phone, with its
live action trace under it. Regenerated by `scripts/make_demo_gif.py` (the same generator
behind the repo's own `assets/demo-trace.mp4`, and identical to it: white ground, native
1368×1852, no wordmark — the one asset that is not on the cream card, because matching the
project's canonical demo beats matching the other eight). Portrait, because X is mobile-first
and a tall clip fills that screen; `01-hero-wide.mp4` is the same tour in the generator's
landscape layout (device left, trace right) rather than a crop of this one. Note X re-encodes anything over 1200px on the short side.
**Alt** An agent fills a spreadsheet, searches the web and sends a message, while a terminal
logs each click and keystroke it takes.
**Why here** On X the first post is the only one most people see, so it has to stand alone. The
earlier version was five bullet fragments under the slogan `1/9 · Any agent, on any computer`
and never said what CUA-Lite is or why anyone needs it — a table of contents, not a post. The
shape now follows [RSI-Exam's launch post](https://x.com/HuaxiuYaoML/status/2092779580004474985):
`Introducing <name> 🧵 — <what it is>` → the mechanism → a call for contributions → a **labelled**
link block. Not copied from it: its emoji bullets (🔁🔒📊), and its opening question — our first
line has to carry the project name for search.

### [2/10] An open platform — site, code, traces, leaderboard

```
[2/10] CUA-Lite is an open platform where everyone can benefit and contribute:

Site: cua-lite.github.io
Code: github.com/cua-lite/cua-lite
Traces: huggingface.co/cua-lite
Leaderboard: cua-lite.github.io/#benchmarks
```

**Bold** `where everyone can benefit and contribute`

**Media** none — X builds the card itself. **The card comes from the LAST URL in the tweet.** Here that is `cua-lite.github.io/#benchmarks`, a fragment of the homepage, so it carries the same tags and the card is the homepage's own (`summary_large_image`, `assets/og.png?v=7`, headline `An open platform for computer-use agents.`). That is what lets Site sit first in the reading order: the anchor at the end holds the card. Put a non-cua-lite.github.io URL last and the card becomes that site's instead. Verify with X's card validator before posting — this was reasoned, not tested.

**Why here** The links used to sit mid-body in post 1. They were moved out on the advisor's note
(«we should move this to the 2nd tweet thread for engagement optimization»): a lead post carrying a
URL is widely held to lose reach, since the platform would rather the reader stayed. That belief is
contested — X open-sourced the feed ranker in Jan 2026 and no explicit URL rule was found in it, and
Musk said in Jul 2026 that link posts had not been penalised for over a year — so treat it as a
practitioner heuristic, not a documented rule. It costs nothing here either way: the three lines sat
below post 1's fold, so moving them frees nothing and loses nothing, and anyone who wants to click
still finds them in the second tweet rather than the ninth.

---

### [3/10] Computer-use agent resources are fragmented

```
[3/10] Computer-use agent resources are fragmented — CUA-Lite is built to close three gaps:

· No framework standardizes eval, SFT or RL, so every project rebuilds the same tooling — agent loops, sandbox setup, eval scripts and training infra
· There is no standard protocol for recording a rollout, so every source ships its own format and one agent's traces can't train another
· Sandboxes are heavy and unstandardized — an expensive VM per task, each with its own interface and action space
```

**Bold** `No framework standardizes eval, SFT or RL` · `no standard protocol for recording a rollout` · `heavy and unstandardized`

**Source** "Why CUA-Lite" opening paragraph — bold lead as the heading, its three problems.
**Reordered from the site's version**, deliberately: the thread now closes them framework (4) →
traces (5) → sandboxes (7–8), and this post's whole job is to be the roadmap for that. The site
and both blogs still run sandboxes → data → framework; if this thread's order is adopted
sitewide, that order changes there too and this note goes away.
**Media** `assets/02-fragmented.mp4` — every dataset and benchmark reaching for every agent,
each pairing dying in the same grey tangle.
**Alt** Lines from Mind2Web, GUIOdyssey, OSWorld and WebArena to GPT, Claude, Qwen and Gemini,
accumulating into a dead tangle.
**Why here** Lists the three gaps in the order the thread closes them — framework (4),
traces (5), sandboxes (7–8). Post 1 states the same three in the order a reader *needs* them
(a place to run, a record, a machine); this post states them in the order the thread *answers*
them, which is why the framework is first. Posts 4, 5 and 7 each restate their gap in one concrete clause
and then answer it in the same breath — definitionally (`X is CUA-Lite's Y…`), not with the
earlier `Our answer is…` turn, which 写作规约 §3 replaced and which survives in no post — so a
reader who meets that post cold still gets both halves — **but as prose, not as a `Gap N` label**, which would need this post to have been read.

### [4/10] One framework: eval, SFT, RL

```
[4/10] One framework: eval, SFT, RL

lite.gym is CUA-Lite's one agent–environment interface, with a standardized action space per platform — desktop, browser and mobile — so any agent can run in any environment. You bring the agent; CUA-Lite's framework ships the rollout loop, the sandboxes to run it in, and the eval and training stack that consumes the rollouts.

The rollouts lite.gym produces are reused three ways:
· Eval — scored by the benchmark's own evaluators, unchanged
· SFT — rendered by each model's adapter into that model's own training format
· RL — scored by the task's own verifiable reward, and those scores drive the RL updates
```

**Bold** `any agent can run in any environment` · `You bring the agent`

**Source** "Why CUA-Lite" § One framework: eval & RL — heading and paragraph, verbatim.
**Media** `assets/03-litegym.mp4` — an environment and an agent trading screenshots and actions
through the lite.gym hub, then swapping for the next pair.
**Alt** OSWorld, WebArena, AndroidWorld and WebGym connect through lite.gym to GPT, Claude,
Qwen and Gemini; the board pairs them one at a time — a screenshot travels up to the agent
and an action, click or tap, comes back down.
**Why here** Closes the first gap in post 3's list, and it comes first for a reason: the interface is what lets anything else plug in. Traces and sandboxes only pay off once one framework drives them.

### [5/10] One format, any dataset

```
[5/10] One format, any dataset

LiteSample is CUA-Lite's trace format, shared across every platform (desktop, browser, mobile), environment, agent and task type — convert a corpus once, and every agent can train on it.

CUA-Lite has 10+ datasets on Hugging Face in LiteSample: public corpora converted into it, plus fresh rollouts from frontier CUAs. An adapter per model then packs a unified LiteSample into the exact training format each one needs — so any model's rollouts can fine-tune any other.

huggingface.co/cua-lite
```

**Bold** `LiteSample is CUA-Lite's trace format` · `convert a corpus once, and every agent can train on it`

**Source** Homepage `#data` heading; body = "Why CUA-Lite" § Datasets — both bold leads verbatim,
plus the homepage Data claim. **一处刻意和站点不同**：站点 h2 是 `One schema, any dataset`，这里改成
`One format`，因为正文已统一用 `trace format` —— 同一个东西在一条推文的相邻两行里不能有两个名字。
站点若始终不改，这处差异保留；改了就同步回来。
**Media** `assets/04-litesample.mp4` — datasets folding into one schema, then an adapter packing
it into each model's own training format.
**Alt** Mind2Web, GUIOdyssey, ScaleCUA and OpenCUA converge into LiteSample, which an adapter
feeds to Qwen, UI-TARS, MAI-UI and Kimi.
**Why here** Closes the second gap from post 3, and follows post 4 directly: post 4 gives the
interface that produces rollouts, this gives the one format they are recorded in. The two
together are what an outside resource plugs into.

### [6/10] One command, any benchmark

```
[6/10] One command, any benchmark

With one standardized interface, 15+ benchmarks are already integrated into CUA-Lite — and the leaderboard is live, every score on it a run we did ourselves.

Desktop: OSWorld, Lite.OSWorld, OSWorld-2, WindowsAgentArena, Cua-Bench.
Browser: WebArena, VisualWebArena, WebVoyager, Online-Mind2Web, MiniWoB, WebGym.
Mobile: AndroidWorld, AndroidLab, MobileWorld, MobileGym.
Grounding: ScreenSpot-Pro, OSWorld-G.

One script evals any agent on any of them — set --model-id and its config for the agent, --env-id for the benchmark.

cua-lite.github.io/#benchmarks
```

**Bold** `15+ benchmarks are already integrated` · `every score on it a run we did ourselves`

**Source** Homepage `#benchmarks` — heading and section lead, verbatim; the counts come from the
coverage board and `assets/exps/eval/manifest.json`.
**Media** `assets/05-leaderboard.mp4` — the eval command and its leaderboard switching benchmarks
together, across four real boards.
**Alt** An eval command's --env-id changes from OSWorld to WebVoyager to AndroidWorld to
ScreenSpot-Pro, and the leaderboard under it reloads with each benchmark's scores.
**Why here** Turns post 4's interface from a diagram into results. Opens on a prepositional bridge
(`With one standardized interface, …`) that echoes post 4's `standardized action space per platform` rather than on `That interface` — a back-reference would break 写作规约 §4,
and the count still lands in the first line, which is what a quoted screenshot shows. The
bridge used to sit at the bottom (`A unified action space per platform means one script evals…`);
it was moved up and the trailing clause trimmed so the same point is not made twice.

### [7/10] VM-free OS(World) at Scale

```
[7/10] VM-free OS(World) at Scale

CUA-Lite also provides optional VM-free sandboxes for hosting environments — efficient, highly optimized containers that reproduce public benchmarks and generate verifiable tasks to train any agent.

Lite.OSWorld is the first of them: it reproduces OSWorld — the exact same tasks and evaluators — in a Docker container instead of a VM, on a fraction of the hardware resources. No /dev/kvm, so it runs anywhere Docker does, at under a quarter of the memory and cpu.
```

**Bold** `it reproduces OSWorld — the exact same tasks and evaluators`

**Source** The VM-free post: its title as the heading, its thesis sentence and the Lite.OSWorld
bold lead verbatim, then the comparison table and the parity plot.
**Media** `assets/06-vm-tax.mp4` — the second sentence, beat for beat: the desktop sheds its
Ubuntu.qcow2 / QEMU·KVM stack and its /dev/kvm dependency, becomes a container, then replicates
into a grid of parallel rollouts (the "~4.6× more instances").
**Alt** An OSWorld desktop sealed in a VM sheds the VM to become a Docker container, which then
multiplies into a grid of parallel rollouts.
**Why here** Problem and fix in one post, because the clip already carries both. OSWorld is the
environment readers already know, so it is the cheapest way into lightweight sandboxes.

### [8/10] Sandboxes & verifiable tasks

```
[8/10] Sandboxes & verifiable tasks

The VM-free container isn't just for OSWorld — it's a base for CUA-Lite's family of sandboxes, which carry 30k+ verifiable tasks so far. The tasks range from everyday browser and desktop work to NASA's GMAT flying spacecraft and PyMOL turning proteins. Each sandbox runs many instances in parallel on one machine.

Four sandboxes share that base today, each re-hosting a public suite: Lite.OSWorld for OSWorld's 369 benchmark tasks plus 2k+ synthesized, Lite.ScaleCUA for 20k+ tasks perturbed from OSWorld's evals, Lite.CUAGym for browser and desktop tasks across mock sites and real apps, and Lite.CUAWorld for 40 professional apps across ~25 expert domains.
```

**Bold** `The VM-free container isn't just for OSWorld` · `30k+ verifiable tasks` · `Four sandboxes share that base`

**Source** The VM-free post's "Beyond OSWorld" lead and "Why CUA-Lite" § Sandboxes & verifiable
tasks, verbatim. Keep the blog's subject (`The VM-free container`) — compressing it to `That
base` left the post opening on a demonstrative with nothing to point at.
**Media** `assets/07-sandboxes.mp4` — the post's own rollout belt, walked across all four
families in 7.0s (measured; `make_assets.py:647` retimes it to exactly that). It was captured slow — `hold=3.2, settle=10` — because at `hold=1.5` the tile videos had not painted and 2.3s of the clip was black, then sped up on the way out; an earlier note here still said "2.6s each (11s total)", which was the capture pace, not the shipped file. It opens on Lite.CUAWorld, whose GMAT and PyMOL desktops
are the least familiar thing in the thread, rather than on another LibreOffice window; the
site-only caption ("click a tile for the full rollout") is hidden, since a reader can't act
on it here.
**Alt** A belt of looping agent rollouts across four sandbox families in the order shown —
Lite.CUAWorld, Lite.CUAGym, Lite.ScaleCUA, Lite.OSWorld — each tab carrying its own line of
task counts and apps.
**Why here** Generalises post 7: one reproduced benchmark becomes the family the belt shows.
It takes the blog's Beyond-OSWorld lead as its source but does not open on those words — the post
opens `The VM-free container isn't just for OSWorld`, which advances rather than restating post 7's
first sentence. (The literal heading `Beyond OSWorld` belongs to thread 02's post [5/6].)

### [9/10] SFT & RL, any open agent

```
[9/10] SFT & RL, any open agent

SFT on CUA-Lite's public rollout traces, then reinforce in its envs — GRPO, GSPO and beyond, built on Slime. Train any open agent on any traces and any env.
```

**Bold** `SFT on CUA-Lite's public rollout traces, then reinforce in its envs`

**Source** Homepage `#train` — heading, section lead and both panel notes, verbatim.
**Media** **both** `assets/08a-sft.png` and `assets/08b-rl.png`, in that order. X takes up to four
images; two is right here because the pair *is* the post — the two panels have the identical shape
(pick two things, run one script), which is the claim the copy makes.

**Measured, not assumed:** `08b-rl.png` is 1496×772 with four lines of very large type
(`MODEL_ID` / `ENV_ID` / `CONFIG_PATH` / `bash run_grpo.sh`) — it survives being halved without
trouble. `08a-sft.png` is 1438×1200; its `DATASET → MODEL` selector row is large and clear, but the
terminal beneath it **is cut off at the frame edge** — the command block runs past the bottom.

**FIXED 2026-08-29.** `08a-sft.png` was truncated at the frame edge and now is not; the terminal
closes with its own rounded border and the three-step pipeline is whole. The cause was **not**
`.term { overflow: hidden }` as an earlier note here guessed — measured, that element is
`overflow: visible` with `clientHeight == scrollHeight`. It was `still_span`'s
`page.screenshot(clip=…)` running **without `full_page=True`**: this union's box reaches y=1362 in a
1200px viewport, and a clip past the viewport bottom is silently cut. `08b-rl.png` was never
affected because its union ends at y=710. See `make_assets.py`'s note — the fix also needs the
scroll offset added to the clip, since a full-page clip is document-relative while `bounding_box()`
is viewport-relative. (An older note claimed this image was "twenty lines and turns to grey at
600px" and sent it to a reply on that basis — written without opening the file, and wrong about
both the line count and the real problem.)
**Alt** A terminal showing MODEL_ID, ENV_ID and CONFIG_PATH passed to run_grpo.sh, with the
model and env picked from dropdowns.
**Why here** Posts 1 and 4 promise SFT and RL; this is the only post that shows them — without
it the thread proves eval and merely asserts training. It opens straight on SFT: the earlier
first line ("The datasets and the sandboxes above are what you train on") was pure connective
tissue, and connective tissue in the top line wastes the only part everyone sees.

### [10/10] Call for contributors

```
[10/10] Call for contributors

Bring an environment (sandbox, tasks, verifier), traces, or an agent — each plugs into CUA-Lite's one interface, one trace format and one framework, exactly like everything above.

github.com/cua-lite/cua-lite
cua-lite.github.io
```

**Bold** `plugs into CUA-Lite's one interface, one trace format and one framework`

**Source** "Why CUA-Lite" — both calls for contributors and the closing line, verbatim.
**Media** `assets/09-card.png` — the project card.
**Alt** CUA-Lite title card: "An open platform for computer-use agents" with 30k+ tasks, 10+ datasets,
10+ agents, 15+ benchmarks.

### 收尾 — Acknowledgements（不编号）

```
Finally, CUA-Lite is the platform; it wouldn't be possible without the task suites, benchmarks and datasets other teams built.

Agents — GPT (@OpenAI), Claude (@AnthropicAI), Gemini (@GoogleDeepMind), Qwen (@Alibaba_Qwen), Fara (@MSFTResearch, @AhmedHAwadallah), GELab (@StepFun_ai), UI-TARS (@Seed_TARS), MAI-UI (Tongyi-MAI) and EvoCUA (Meituan).

Benchmarks — @XLangNLP's OSWorld (@TianbaoX, @taoyds), OSWorld-2 (@yuan_mengq43669) and OSWorld-G (@jiaqideng07, @xiaochuanlee, @junlin45300, @SFResearch); Microsoft's WindowsAgentArena (@rogerio_bonatti) and WebGym (@jackbot_cs); @LTIatCMU's WebArena (@shuyanzh36, @gneubig) and VisualWebArena (@kohjingyu, @dan_fried), with MiniWoB (@stanfordnlp), all run through @ServiceNowRSRCH's BrowserGym (@tlsdc_); @osunlp's Online-Mind2Web (@xue_tianci, @ysu_nlp); WebVoyager (@wyu_nd); ScreenSpot-Pro (@kxli_2000); @GoogleDeepMind's AndroidWorld; @thukeg's AndroidLab (@ericdongyx); Tongyi-MAI's MobileWorld; CASIA's MobileGym; and @trycua's Cua-Bench.

Sandboxes — our Lite.* family re-hosts @thukeg's SCALE-CUA (@Shawliu12, @ericdongyx), @LTIatCMU's gym-anything (@PranjalAggarw16, @gneubig, @wellecks) and @XLangNLP's CUA-Gym (@BowenWangNLP, @taoyds). Our RL builds on @thukeg's Slime.

Thanks to @LambdaAPI for part of the compute credits.

If we are hosting your work and you want it credited or shown differently, tell us and we will fix it.
```

**Every name here was checked at source. Do not edit this post without re-checking — a wrong acknowledgement is worse than any wrong number, because it is about real people.**

| Claim | Verified against |
|---|---|
| `Thanks to Lambda for part of the compute` | code repo `README.md:316-318`, verbatim — and it is the **only** acknowledgement anywhere in the repo. Lambda does not appear on the website. |
| `UC Berkeley and Microsoft` | `index.html` footer, which reads **"Presented by"** + the two logos. The Microsoft link points at `microsoft.com/research`, but the site's display name is plain **Microsoft** — do not upgrade it to "Microsoft Research". |
| `OSWorld and CUA-Gym from xlang-ai` | `lite/gym/envs/lite/cuagym/README.md:5` and `docs/envs.md:217` |
| `gym-anything from CMU` | `lite/gym/envs/lite/cuaworld/README.md:5-6` — `cmu-l3/gym-anything` (MIT). Use **gym-anything**, their public name, not "CUAWorld". |
| `SCALE-CUA from THUDM` | commit `0598e30`. **Not OpenGVLab** — that is the other, same-named project, and it owns the SFT corpus, not this environment. |
| `The RL **builds on** THUDM's Slime` | `index.html:331` links `github.com/THUDM/slime`. Deliberately **not** "runs on": `.gitmodules` points at our own fork `cua-lite/slime`, so THUDM gets the credit but the verb stays honest. |
| `the authors of the datasets we converted`（**不写数字**）| 两个来源对不上：`README.md:245` 的已发布 Corpora 是 **9** 个，`lite/data/preproc/` 有 **10** 个目录（多出 `jedi`，有转换代码未发布），而 `README.md:30` 对外写 `10+`。正文用 `10+`（同 README），致谢**不带数字** —— 这里赌一个数字换不到任何东西。 **Thanks only — makes no claim about their licences or their intentions.** An earlier draft said they "were made open by their authors first"; that was invented, and it is exactly the kind of sentence that must never appear here. |

**刻意用纯文本、不加 @ 的（查不到第一方出处，宁缺毋滥）：** Tongyi-MAI（MAI-UI / MobileWorld —— `@Ali_TongyiLab` 无任何阿里资产背书）· Meituan（EvoCUA）· MobileGym（README 只有 arXiv 号，作者不明）· AndroidLab 首作者（两个候选都无法绑定，改用 @thukeg）。
**已否决的猜测：** `@kaserty`（仅第三方转述）· `@shuyanzhxyc`（旧号）· `@BytedanceTalk` · `@_Kaixin_Li` · `@thecrawles`（Chris Rawles，本人主页与 GitHub 均无 X）· `@CaimingXiong` / `@percyliang`（均无第一方页面绑定）· `@_AndrewZhao`（另一个同名的清华博士，与 Fara 无关）。

**@ 的范围（作者原话「多多益善」）：** 一作、共同一作、末作、机构/实验室账号**都可以 @**，同一条目挂多个是好事。
**机构号只 @ 实验室/研究组，不 @ 大学。** `@CMU` / `@ZJU` / `@NUSingapore` 这类校级官方号发的是校园新闻，对一篇论文没有意义 —— 作者原话「@ 浙大、@ cmu 肯定是不 make sense 的」。有意义的粒度是**会自己转发这篇论文的那个账号**：`@XLangNLP`（XLANG Lab）· `@osunlp`（OSU NLP Group）· `@thukeg`（清华 KEG）· `@stanfordnlp` · `@GoogleResearch` · `@MSFTResearch`。企业研究部门（Tencent AI Lab、Salesforce AI Research、ServiceNow Research、Tongyi Lab、ByteDance Seed）同理算数。
**但查不到就不 @** —— 作者原话「如果实在找不到就不用 @ 就行」。纯文本条目是**刻意的结果**，不是遗漏，审核时不要报成缺陷。

**查 handle 的判据（这条是硬的）：** 第一方来源把账号绑定到**本人** —— 本人主页列出的账号、本人 GitHub profile 的 `twitter_username` 字段（自填，`gh api users/<login>` 可读）、实验室/机构页链接、论文项目页。**名字相同不算证据。** x.com 对自动抓取返回 402，所以用上述替代来源。
**大厂还要多核一步：账号真实 ≠ 发布方正确。** Fara 曾被记成 `@MicrosoftAI`（microsoft.ai 消费级 org），实际发布方是 **Microsoft Research**（`microsoft.com/en-us/research/blog/fara-7b-…`、`microsoft/fara`、MSR AI Frontiers 的 Magentic-UI）。同理 AndroidWorld 走 `@GoogleDeepMind` 而非 `@GoogleResearch` —— `google-research/` 只是代码托管 org，项目页把作者机构标为 Google DeepMind（见下表）。

**发布前注意：** 这条有 48 个 @（2026-08-30 实测），X 对高 @ 密度的贴有垃圾信息过滤风险。若被限流，优先保留作者本人的 @，把厂商账号（@OpenAI / @AnthropicAI / @GoogleDeepMind / @Alibaba_Qwen）降为纯文本。

**刻意不提，不要加回来：** `captcha`（`ASTRAL-Group/ReCAP-Agent`）—— 作者指定不进致谢。审核工具会把它报成「漏项」，不要采纳。

**Not claimed, on purpose:** no individual is named. The site lists nine authors (`index.html:386`); picking some for a tweet and not others is its own problem. If you want to thank a person, add their handle yourself — do not let this file guess one.

**No number.** Post 1 opens unnumbered and this closes unnumbered — the two bookends sit outside `[N/10]`, which stays a count of the argument itself. Adding `[10/10]` would also silently renumber every earlier post.

**Media** none, or reuse `09-card.png`. This is the one post where a bare text block is right: an acknowledgement with a graphic attached reads as a campaign.

**Why this post exists at all.** Four separate reviews named the same thing as the **cheapest unused lever in the launch: nine posts, zero @-mentions**. Plain-text credit notifies nobody; a mention does, and upstream authors reliably amplify work built on theirs. Stuffing handles into the body posts would wreck their folds — an acknowledgements post is where they all fit at no cost to any other post.

**The handles below were looked up and each was confirmed against a live profile URL. Re-check on the day
— accounts get renamed — but do NOT substitute a handle that is not on this list.**

| @ | who | confirmed at |
|---|---|---|
| `@XLangNLP` | XLANG Lab — OSWorld, CUA-Gym | x.com/XLangNLP |
| `@TianbaoX` | Tianbao Xie — OSWorld first author | x.com/TianbaoX |
| `@PranjalAggarw16` | **Pranjal Aggarwal — gym-anything's FIRST author** | listed on his own page, pranjal2041.github.io |
| `@gneubig` | Graham Neubig — gym-anything | x.com/gneubig |
| `@wellecks` | Sean Welleck — gym-anything | x.com/wellecks |
| `@thukeg` | THUDM — SCALE-CUA | the THUDM GitHub org's own listing |
| `@slime_framework` | Slime | x.com/slime_framework |
| `@opengvlab` | OpenGVLab — ScaleCUA-Data | x.com/opengvlab |
| `@jackbot_cs` | Hao Bai — WebGym's first author | listed on his own page, biechi.github.io |
| `@LambdaAPI` | Lambda | lambda.ai footer |
| `@OpenAI` | GPT | 官方账号，无歧义（openai.com 对自动抓取返回 403，未取到页面出处） |
| `@AnthropicAI` | Claude | anthropic.com 页脚 → x.com/AnthropicAI |
| `@GoogleDeepMind` | Gemini | deepmind.google/about 页脚 |
| `@Alibaba_Qwen` | Qwen | GitHub org QwenLM 的 twitter_username 字段 |
| `@MSFTResearch` | Fara | Fara-7B 由 **Microsoft Research** 发布：博客 `microsoft.com/en-us/research/blog/fara-7b-…`、仓库 `microsoft/fara`、与 MSR AI Frontiers 的 Magentic-UI 集成。**曾误用 `@MicrosoftAI`** —— 那是 microsoft.ai 消费级 org 的账号，不是发布方 |
| `@StepFun_ai` | GELab | StepFun 自己的 HF org 页 huggingface.co/stepfun-ai |
| `@rogerio_bonatti` | WindowsAgentArena | rogeriobonatti.github.io 本人主页 |
| `@shuyanzh36` | WebArena | GitHub shuyanzhou 的 twitter_username。**她主页上的 @shuyanzhxyc 是旧号，别用** |
| `@kohjingyu` | VisualWebArena | jykoh.com 本人主页 |
| `@stanfordnlp` | MiniWoB | nlp.stanford.edu 页脚 |
| `@osunlp` | Online-Mind2Web | GitHub org OSU-NLP-Group 的 twitter_username |
| `@xue_tianci` | Online-Mind2Web 首作者 | xuetianci.github.io 本人主页 |
| `@wyu_nd` | WebVoyager 共同作者 | GitHub wyu97 的 twitter_username。**首作者何洪亮无 X 账号** |
| `@kxli_2000` | ScreenSpot-Pro 首作者 | likaixin2000.github.io 本人主页。机构是 **NUS** 不是清华 |
| `@GoogleDeepMind` | AndroidWorld | 项目页 `google-research.github.io/android_world` 把作者机构标为 **Google DeepMind**；`google-research/` 只是代码托管 org。**曾误用 `@GoogleResearch`** —— 与 Fara 误用 `@MicrosoftAI` 同一类错误 |
| `@ericdongyx` | SCALE-CUA / AndroidLab 末作者 Yuxiao Dong | keg.cs.tsinghua.edu.cn/yuxiao 本人主页自列 |
| `@BowenWangNLP` | CUA-Gym 首作者 Bowen Wang | bowenbryanwang.github.io + GitHub twitter_username |
| `@ysu_nlp` | Online-Mind2Web 末作者 Yu Su | 本人主页 ysu1989.github.io 只链 `twitter.com/osunlp`；**GitHub 的 `yusuOSU` 字段是死号**（查无此人、零发帖），`@ysu_nlp` 有在题发帖史且 bio 写「professor at @osunlp」 |
| ~~`@Dong_Yu_AI`~~ **已删** | WebVoyager 末作者 Dong Yu | 本人主页确实列了此号，但**账号零活动**（无任何可检索发帖），且他现已在 Capital One 而非腾讯 AI Lab。@ 死号无收益 —— 作者判定「这个应该删的」 |
| `@dan_fried` | VisualWebArena 末作者 Daniel Fried | dpfried.github.io + GitHub 字段 |
| `@trycua` | CUABench / Cua 公司 | GitHub org trycua 的 twitter_username + cua.ai |
| `@taoyds` | OSWorld / CUA-Gym 末作者 Tao Yu | xlang.ai/blog 页面数据内嵌 twitterLink |
| `@yuan_mengq43669` | OSWorld-2 一作 Mengqi Yuan | @XLangNLP 自己的发布线程点名（仅 X 侧，经搜索快照） |
| `@tlsdc_` | BrowserGym 一作 Thibault Le Sellier de Chezelles | GitHub TLSDC 的 twitter_username |
| `@AhmedHAwadallah` | Fara 资深作者 Ahmed Awadallah | MSR 个人页 microsoft.com/…/people/hassanam/ 列出 x.com 链接 |
| `@jiaqideng07` | OSWorld-G 共同一作 Jiaqi Deng | millank0817.github.io 本人主页 social nav |
| `@xiaochuanlee` | OSWorld-G 共同一作 Xiaochuan Li | xiaochuanli.com 本人主页 + GitHub social_accounts |
| `@junlin45300` | OSWorld-G 共同一作 Junlin Yang | yangjl2003.github.io 本人主页 social-links |
| `@Shawliu12` | SCALE-CUA 共同一作 Xiao Liu | xiao9905.github.io 本人主页 |
| `@LTIatCMU` | CMU LTI（WebArena / VisualWebArena / gym-anything） | cmu.edu/social-media 官方账号目录列为 Language Technologies Institute |
| `@SFResearch` | Salesforce AI Research（OSWorld-G 末作者 Caiming Xiong） | salesforce.com 博客「Follow us on X: @SFResearch」 |
| `@ServiceNowRSRCH` | ServiceNow Research（BrowserGym） | 其自有页 servicenow.com/research 的 `twitter:site` meta（现站 403，经 Wayback 快照） |
| `@Seed_TARS` | UI-TARS（字节 TARS 团队） | seed-tars.com 的 `twitter:site` meta；该站被 UI-TARS 的 HF 卡片与 GitHub README 双双链接 |

**Two more with the same grade of evidence, deliberately left out — add only if you want a longer list:**
`@OpenBMB` (for CAGUI / GUIAct — host org, not the whole author set). (`@osunlp` was on this list too;
it is now shipped, on Online-Mind2Web.) The remaining corpora — GUI-360, UI-Genie-Agent — have no findable project
handle; leave them as plain text rather than tagging a corporate account.

**几条 check 出来的注意事项：**
- `@slime_framework` is the only one of the ten with **no first-party link** — neither `THUDM/slime`
  nor its docs site links any social account; it was confirmed by content match (its posts track the
  repo's own v0.3.x releases). If you want zero risk, drop it and let `@thukeg` carry Slime.
- `@thukeg` is correct but **quiet** — expect little amplification. The active account in that orbit is
  `@Zai_org` (Z.ai/Zhipu), which is the **wrong entity** for an academic THUDM paper. Do not substitute it.
- Unrelated, but do not cite it anywhere: **`tianbaoxie.com` has lapsed and now redirects to a squatted
  domain.** It is still the homepage link on the OSWorld page.

**Original rule, still in force:** A wrong @ is worse than none, and this file has already mis-attributed SCALE-CUA twice in opposite directions (see 写作规约 8). Handles to find: xlang-ai · `cmu-l3` (gym-anything) · THUDM (SCALE-CUA **and** Slime) · OpenGVLab (ScaleCUA-Data) · Microsoft (WebGym **and** an institution — two different roles) · Lambda · UC Berkeley. **Microsoft, not Microsoft Research** — the site's display name is plain Microsoft; an earlier version of this note said otherwise and contradicted the table above it.

**The last line is a real offer, so only ship it if you mean it.** `tell us and we will fix it` is what turns a credit list into an invitation; it is also the sentence an upstream author will hold you to.

---

## Posting notes

- **每帖一图，post 9 例外**（SFT + RL 两张，作者指定）。其余帖两图会各自减半宽度，which is what made
  the training terminal unreadable; the RL half goes in a reply instead. Every clip loops
  silently under ~60s; X autoplays them muted.
- **Clips are cut to loop and to open on motion.** Each is trimmed to a whole number of its
  figure's own animation cycle — 5.93s for the tangle, 7s for the VM figure, 5.2s for the
  pair-boards (the numbers are in the pages' own JS) — and the exact wrap point is picked by
  matching the last frames against the first. Measured seam error, 0 = perfect —
  **named by subject, not by number: the numeric prefixes shift on every reorder and this list
  was unreadable against `assets/` after the last one.** fragmented 0.3 · vm-tax 0.3 ·
  litesample 0.4 · leaderboard 0.4 · litegym 1.5 · sandboxes 17.6 (its tiles each loop a rollout
  on its own clock, so the tile contents jump at the wrap even though the layout doesn't) ·
  hero 49 (the tour ends on the phone and restarts on the desktop — inherent to a three-device
  tour, and it is the project's own canonical demo). Openings were re-cut too: the sandbox belt
  and the leaderboard used to sit frozen for the first 2-3 seconds, which is the entire window a
  scrolling reader gives them — those are the only two with a `head=` trim in `make_assets.py`
  (`:661`, `:697`).
- **Links** live in posts 2, 5 (Hugging Face), 6 (`#benchmarks`) and 10 — X buries mid-thread links.
  Post 1 carries no URL at all: it opens with a clip, so X shows the clip. That's intended (见写作规约 §2).
- **Alt text** is worth pasting in: this audience uses it, and the figures are the argument.
- **Spares**, for replies or a quote-tweet: `extra-footprint.png` and `extra-parity.png`
  (the table and parity plot behind post 7's numbers) and `extra-side-by-side.mp4` (the
  same model on the same task, VM vs container). The first reply to post 7 is the natural
  place for them.
- **Blog links**, if someone asks for detail: `/blog/kvm-free-osworld/` answers posts 7–8,
  `/blog/why-cua-lite/` answers 3 and 6–10.

## 提前写好的回复（post 1 / 7 / 9）

Each post carries one media, so the evidence that does not fit goes in a reply on the same
post — one tap away, and ready before anyone asks.

**Reply to post 1 — the highest-value slot in the launch.**

```
Receipts for the parity claim above: same task suite, same evaluators, 13 models, VM vs container.

And it takes two commands to run one yourself:

uv sync --all-extras

import asyncio, lite.gym as gym, lite.agents as agents
env = gym.make("lite.demo@create_file", max_steps=10)
agent = agents.make("gpt-5.5", env=env)
result = asyncio.run(agent.sample(env))

Write-up: cua-lite.github.io/blog/kvm-free-osworld/
```

**Media** `assets/extra-parity.png` + `assets/extra-footprint.png`.

**The code is verbatim from the repo's own Quick Start** (`README.md:45-66`) — `uv sync --all-extras`,
then the five-line `gym.make` / `agents.make` / `agent.sample` snippet, running `lite.demo`, the one env
with no upstream suite and no KVM. **Run it once on a clean checkout before posting.** A launch-day
snippet that errors is worse than no snippet, and this file has already shipped one invented
`gym.make` example in another platform's draft.

**Add one first-person sentence, in your own words, and write it yourself.** Post 1 is institutional
"we" from end to end and the account is one person; every review said the missing human is what caps
this at "star and close the tab". It should be why *you* built it — the sentence a colleague would
recognise. **I am not drafting that one**: invented motivation is the one thing a reader detects
instantly, and it is yours to say.

---

**Why this reply, in this slot.** Post 1 is the only
post most people see, so the top reply under it is the second-most-viewed text of the whole
thing; replies under 3 and 8 only reach readers who already believed you. Put three things here:
the parity receipts (`extra-parity.png` + `extra-footprint.png`), **one install/run command** —
there is no `pip install`, no `docker run` anywhere in nine posts, which is the single biggest
conversion loss in the file — and **one first-person sentence** about why you built it. The
account is one person; post 1 is written entirely in institutional "we", and `Built at UC Berkeley
and Microsoft.` sits below its fold.

**At publish time, @-mention the upstreams you build on** — xlang-ai (OSWorld, CUA-Gym),
CMU (`cmu-l3/gym-anything` — 致谢帖用他们的公开名 `gym-anything`；post 1 沿用 red 版的 `CUAWorld`，两个名字都能在代码库里找到出处，**不要为了统一而改 post 1**), THUDM (SCALE-CUA and Slime). Plain text notifies nobody; a mention does, and
upstream authors reliably amplify work built on theirs. **Look the handles up on the day —
do not guess them.** (This file has already mis-attributed ScaleCUA once by copying a stale
link instead of checking; a wrong @ is worse than none.)

**Reply to post 7 — the receipts.** Post 7 asserts the numbers; this shows them.

```
The receipts — same task suite, same evaluators, 13 models:
memory, cold start, parallelism, and every model's score in the VM vs in the container.

Full write-up: cua-lite.github.io/blog/kvm-free-osworld/
```

**Media** `assets/extra-footprint.png`, `assets/extra-parity.png`. (`extra-side-by-side.mp4`
— the same model on the same task, VM left, container right — is a good third, in a
follow-up reply rather than the same post.)

**Reply to post 9 — the SFT pipeline in full.** Post 9 shows the RL command; this is the
other half, at a size worth expanding.

```
And the SFT side, end to end: download the corpus, export a model-ready parquet for
your student, then run_sft.sh in the Slime container. Pick the dataset and the model;
the paths follow.
```

**Media** `assets/08a-sft.png`
**Alt** A terminal showing the three-step SFT pipeline for a chosen dataset and model:
download the corpus, export a model-ready parquet, run run_sft.sh.

## Facts used (and where they come from)

| Claim | Source |
|---|---|
| 4.1 → 0.9 GB · 29.9 → 23.8 s · ~4.6× instances | comparison table, `blog/kvm-free-osworld/` |
| 13 models, same tasks, matching scores | parity plot data, same post (real runs) |
| 30k+ verifiable tasks · 10+ datasets · 15+ benchmarks | homepage hero + coverage board |
| 11 benchmarks with public leaderboards | `assets/exps/eval/manifest.json`, non-`pending` entries |
| GMAT / PyMOL science desktops | blog 2, "Beyond OSWorld" (via the belt's own captions) |

Every number is on the site. If the site changes, change it here too — and re-run
`make_assets.py`, since the media is captured from those same pages. The one number still to
confirm is post 7's footprint set; see **Pre-flight 1**.
