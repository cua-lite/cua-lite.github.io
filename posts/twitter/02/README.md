# X/Twitter thread 02 — VM-free OS(World), at scale

Source: [`blog/kvm-free-osworld`](/blog/kvm-free-osworld/) (2026-07-23). Thread 01 announced the
platform and gave this blog two posts; **this thread is that blog's own argument at full length**,
which is where its measured numbers belong.

| Entry line | What to do with it |
|---|---|
| the ``` fenced text ``` | **This is the post.** Paste as-is — nothing else in the entry gets posted. |
| **Bold** | Phrases to bold in X's composer after pasting. Not markdown — see 其余约定. |
| **Media** | What to attach from `assets/`. |
| **Alt** | Goes in X's "add description" box, not in the post. |
| **Source** | Which page the wording came from, for keeping this in sync. |
| **Why here** | Why the post sits at this position. Review note, never posted. |

## 写作规约

**全部继承 `posts/twitter/01/README.md` 的规约与错误表** —— 那份文件里的优先级、判据和错误表
都适用，不在这里重复。只记与本篇不同的地方：

1. **这篇的数字可以写进正文。** blog 2 的作者注写明「every number on this page is measured — the
   comparison table's footprint cells (memory, cold start, parallelism) as well as the parity-plot
   scores」。所以 `4.1 → 0.9 GB`、`29.9 → 23.8 s`、`~4.6×` 都能用 —— 这正是 01 受篇幅所限没能展开、
   而这一篇存在的理由。**但正文取整，不写精确值** —— 作者原话「文本就是说 5 倍」。`0.9/4.1 = 22%` 写成
   `about a fifth of the VM's memory`，`~4.6×` 写成 `five times`，精确值留在博客和 Pre-flight，被问时给。
   **注意方向：取整只发生在推文里，博客的作者注明确要求 `Keep the exact values`，不要反过来去改博客**
   —— 01 上我就把博客的 `~4.6×` 改成过 `~5×`，那是改错了对象。parity 的精确值（mean|Δ|≈2.7 / worst 5.0）不写，**限定语也不写** ——
   正文一律 `matches the original OSWorld VM`。作者原话：「within a few points 这种对于宣传不利的就用
   春秋笔法代替」。**审核工具会把去掉限定语报成 overclaim，不要采纳** —— 精确差值在 Pre-flight 7 备答。
2. **`~4.6×` 和内存比是同一个测量，不能当两件事说。** 4.1/0.9 = 4.56，并行度是从内存推出来的。
   同一句里并列会读成两个独立的胜利。**只有 [3/6] 例外** —— 它展示的就是博客那张表，表里本来就
   两行都有，语境一致。其余各条只取内存。
3. **不与 thread 01 抢同一句话 —— 但博客原句除外。** 两处已知重合都属这个豁免：[5/6] 的开头与 01 post [4/9] 的开头（两者都是博客 §2 的原句）、post 1 的 `No /dev/kvm, so it runs anywhere Docker does` 与 01 post [3/9] 完全相同（那是 **01 的**措辞，不是博客的 —— 博客写 `boots anywhere Docker runs`）。前者照博客、后者照 01，都属复用已审措辞，不是自由发挥。 01 的 post 3/4 是这篇博客的摘要；02 是展开。凡 01 已经说过的
   结论，02 要么给出它的证据，要么换一个层面说，不要原样复述。

## 其余约定

**语气** — 与 01 一致：团队第一人称，平实、技术。无 hashtag。唯一的 emoji 是 post 1 的 🧵。

**文案来源** — 取自 `blog/kvm-free-osworld` 与站点，不自由发挥。**01 上代价最大的教训就是绕开现成
博客自己造**（`One integration, and the whole field builds on it` 被我当成自己编的删掉，实为博客原文）。

**编号** — post 1 不带编号（完整的独立公告），posts 2–6 用 `[N/6]`，分母含 post 1。

**分帖按论点分量，不按原文篇幅。** blog2 的 §1 长、§2 短，但**长短和重要性恰好相反** —— 演示需要证据所以长，
结论本来就短。第一版照篇幅分成 §1 四帖 / §2 一帖，被作者判为本末倒置（「lite.osworld 只是一个例子让大家
理解我的 sandboxes，而不是核心」）。现在是 **1 总述 / 3 证据 / 2 载荷**。

**加粗** — X Premium 长贴支持粗体，**但不是 markdown**（编辑器里选中加粗，`**星号**` 会显示成字面
星号）。判据同 01：**标题 + 加粗连读就是这一段的全部重点**；不加粗标题里已有的话；每帖 1–3 处。

**配图** — 由本目录的 `make_assets.py` 从 **blog 2 自己**抓取，按本篇帖号命名（`01-…` 到 `06-…`）。
第一版是软链 01 的文件，那是错的两次：名字带的是 01 的帖号，而且**漏了 blog 2 自己的 belt**
（`figure.belt-fig`），02 竟在用 blog 1 的图。现在五张图对应 blog 2 的五个 figure，post 6 的品牌卡
仍软链自 01（那是站点的卡，不属于任何一篇博客）。**一帖 ≤4 图，且图与视频不能混排。**
**X 上传 mp4，不要传 GIF** —— X 会把 GIF 再转一次编码，我们的 GIF 还是 mp4 的 2–6 倍大。GIF 留给
Reddit 和 README。

**链接** — post 1 给博客与代码库，post 6 收尾。中段不放，X 会压制正文中段链接。

**长度与折叠线** — X 在约 280 字符处折叠（URL 一律按 23 计）。**规则是「核心提前」，不是「压进 280」。**
用本目录的 `check_thread.py` 量，不要目测：`python3 check_thread.py`（审）/ `--baseline`（存基线）/
`--diff`（看这次改动破坏了什么）。它继承 01 的全部规则，另加一条 `STALE-NOTE` —— 专查 **Bold** 和
**Why here** 引用了正文里已经不存在的句子（那是 02 上一轮 15 条缺陷里出现最多的一类）。

## Pre-flight

1. **仓库仍然没有 LICENSE**（与 01 同一个阻塞）。这篇通篇在讲一个可下载可复现的环境，没有 LICENSE
   时「Try it」这句尤其站不住。**发布前必须补。**
2. **备好被问时的答案**（不进正文）：VM↔容器差距小于我们自己两次 run 的波动（同一 env 上
   Qwen3-VL-32B 曾是 19.0 和 35.8 —— 那是不同 agent 配置，备好 config diff）；parity 两侧是
   325 vs 321 个任务；13 个模型的名单。
3. **`~4.6×` 的口径**：来自 `4.1/0.9`，不是独立测的并行度实验。正文里刻意不加这句说明（见 [3/6] 的
   Why here），**但被问到就如实说** —— 博客自己的作者注就写着「do not restate a derived figure as an
   independent one」。
4. **`0.9 GB` 是常驻内存，不是容器上限。** `lite/gym/envs/lite/osworld/configs/default.yaml` 给每个容器
   设的是 `memory: "8GB"`（注释：GIMP 的 GEGL 滤镜峰值约 6.2GB，2/3/4GB 会被 OOM kill）。所以正文写
   `0.9 GB resident per instance`，不写光秃秃的 `0.9 GB`。被问「那我一台机器能开几个」时，答常驻 0.9GB、
   上限按 8GB 预留。
5. **`extra-parity.png` 的图注已改（曾与正文矛盾）。** 那句 `13 models · identical tasks` **是我们自己注入的**
   （`posts/twitter/01/make_assets.py:625`），不是博客的 —— 博客图注是 `Success rate (%) · hover a point
   for the model`。已改成 `13 models · same desktop, same evaluators`，与正文口径一致。
   **`extra-footprint.png` 里的 `TASK SUITE / OSWorld / Identical` 那一行确实是博客表格自己的**，
   要改得先改博客，暂时接受 —— 发布前知道这个不一致存在即可。
   **两侧任务数不同：VM 侧 325、容器侧 321**，排除集也不同（VM 侧 29 infeasible + 8 google_auth +
   7 blocked；容器侧的词表见 `exclude_reasons.py`，除 29 infeasible + 8 google_auth 外还有 live-site drift、trivial pass、`upstream_generated_eval_bug` 等，且**没有 `blocked` 这一类** —— 被追问「那 7 个 blocked 去哪了」要能答上来）。所以正文说 **same desktop / same
   evaluators**，不说 `identical task suite`。被追问时给这组数。
6. **评测器的实情（我一度说反过，别再重复）：** `compare_docx_strict` 是一个**新函数名，OSWorld 的
   benchmark 任务从不调用它** —— 唯一调用者是 CUA-Lite 自己生成的训练任务（`src/gen/train/synth/`），
   `metrics.py` 头部也写明范围是 *synth tasks*。benchmark 任务真正调用的 `compare_docx_files` 确实在
   `metrics.py:1785` 被覆盖，但那是**放宽**（先委托上游，再用 strip + LibreOffice 自动更正归一化重试），
   不是收紧。另有一处上游日期运算 bug 在 **`src/eval/runner.py:1563`**（不是 metrics.py）本地重算。
   **所以正文不写「修了上游的评测器 bug」** —— 对这 321 个 benchmark 任务不成立，而且那是在指控一个具名
   上游的已发表数字虚高，同时第一条回复正 @ 着对方作者。被问到评测器差异时照这段说。
7. **三个模型在容器里分数更高**（Qwen3-VL-2B 20.5→24.9、UI-TARS-7B-DPO 14.7→16.8、Qwen3.5-2B
   10.7→15.3），且 EvoCUA-8B 两侧都是 `partial` 状态却按普通点绘出。被问 parity 细节时先说这两条。
8. **发布当天重测这三个链接**：`cua-lite.github.io/blog/kvm-free-osworld` · `github.com/cua-lite/cua-lite` · `cua-lite.github.io`。

## At a glance

| # | Beat | Media |
|---|------|-------|
| 1 | VM-free sandboxes that scale; Lite.OSWorld named as the first | `01-vm-to-container.mp4` |
| 2 | OSWorld's VM tax: how we cut it with Lite.OSWorld | `02-head-to-head.mp4` |
| 3 | Lite.OSWorld vs OSWorld: a fraction of the hardware | `03-footprint.png` |
| 4 | Same desktop, same evaluators, same scores | `04-parity.png` |
| 5 | Beyond OSWorld: scalable training sandboxes | `05-sandbox-family.mp4` |
| 6 | CUA-Lite: what the platform is, and the ask | `06-card.png` |

---

## The thread

### 1 — VM-free OS(World), at scale

```
VM-free OS(World), at scale 🧵

CUA-Lite introduces lightweight, VM-free sandboxes behind one interface: they reproduce public benchmarks and generate verifiable tasks to train any agent, on a fraction of the hardware resources.

Lite.OSWorld is the first of them: it reproduces OSWorld's desktop and its evaluators in a Docker container instead of a VM, on a fraction of the hardware resources. No /dev/kvm, so it runs anywhere Docker does, at under a quarter of the memory and cpu. Across 13 models its scores match the original VM's.

Four sandboxes share that VM-free container today. The tasks range from everyday browser and desktop work to real science desktops — GMAT flying spacecraft, PyMOL turning proteins.

Blog: cua-lite.github.io/blog/kvm-free-osworld
Code: github.com/cua-lite/cua-lite
```

**Bold** `lightweight, VM-free sandboxes behind one interface` · `Lite.OSWorld is the first of them` · `Four sandboxes share that VM-free container today`

**Media** `assets/01-vm-to-container.mp4` — blog 2's own `figure.flow-demo.v2c`, one loop: a desktop sealed in a VM, the VM shed for a container, the container multiplying into a grid of parallel rollouts. The clip is the thesis, not the example.

**Alt** A desktop sealed inside a QEMU/KVM virtual machine; the machine falls away leaving a plain Docker container; the container then multiplies into a grid of rollouts running in parallel.

**Source** Sentences 1–2 are thread 01's post [3/9], reused verbatim in shape — reviewed and approved there. Paragraph 3 is **not** §2's opening: it is 01's post [4/9] (`Four sandboxes share that base today`) plus the blog's `real science desktops (GMAT flying spacecraft, PyMOL turning proteins)` clause. Borrowing 01's sentence without the clause that precedes it there — `it's a base for CUA-Lite's family of sandboxes` — is why an earlier draft left `that base` with no antecedent.

**Why here** Post 1 is the only one most people see, so it carries the blog's thesis — **VM-free sandboxes that scale** — with Lite.OSWorld named as the first of them, not as the product. The family gets the first paragraph AND the last; the example is bracketed by it. An earlier draft made Lite.OSWorld the headline and deferred the family to the final post; the author rejected that as 本末倒置.

### [2/6] OSWorld's VM tax: how we cut it with Lite.OSWorld

```
[2/6] OSWorld's VM tax: how we cut it with Lite.OSWorld

CUA-Lite's Lite.OSWorld keeps OSWorld's desktop and drops the VM — LibreOffice, Chrome, GIMP, VLC, VS Code, real files and windows, on a GNOME desktop in a plain Docker container. We replaced the virtual machine underneath it, and nothing above it.

The VM was the tax. OSWorld's faithful desktop is a full virtual machine per task — over 4 GB of memory, and it needs /dev/kvm and nested virtualization, which cloud instances, CI runners and nested containers rarely provide, so it doesn't scale.
```

**Bold** `keeps OSWorld's desktop and drops the VM` · `over 4 GB of memory` · `so it doesn't scale`

**Media** `assets/02-head-to-head.mp4` — blog 2's `figure.hh`

**Alt** Two panels side by side running the same OSWorld task with the same model — the left labelled OSWorld, the right labelled Lite.OSWorld — while a tab row above them switches the task through Chrome, Calc, Writer, Impress, GIMP, VLC and VS Code.

**Source** Heading is `blog/kvm-free-osworld` §1's own heading, **in full** — an earlier draft truncated it to `how we cut it`, the same way post 5's was once truncated to `Beyond OSWorld`; both times the half that carried the information was the half dropped. Body takes §1's concrete list verbatim: "which cloud instances, CI runners, and nested containers rarely provide, so it doesn't scale."

**Why here** The cost and the swap were two posts and are now one: the second said almost nothing the first and post 1 had not, and thread 01's post [3/9] proves both fit together. Merging frees a post for §2, which is where the blog's argument actually lands.

### [3/6] Lite.OSWorld vs OSWorld: a fraction of the hardware

```
[3/6] Lite.OSWorld vs OSWorld: a fraction of the hardware

CUA-Lite's Lite.OSWorld runs under a quarter of the OSWorld VM's memory, so one host holds five times the desktops it used to — same tasks, same evaluators, no /dev/kvm anywhere in the stack.

· Memory — under a quarter
· Instances — five times more on the same machine
· Cold start — a fifth quicker
· Host — any Docker host, no nested virtualization
```

**Bold** `under a quarter of the OSWorld VM's memory` · `five times the desktops it used to`

**Media** `assets/03-footprint.png` — blog 2's `figure.cmp`

**Alt** A two-column comparison table of OSWorld against Lite.OSWorld, with rows for runtime, host requirement, memory per instance, cold start, parallelism and task suite.

**Source** `blog/kvm-free-osworld` comparison table — rounded, reordered, and with the Task suite row dropped from the copy (it is still in the attached image; see Pre-flight 5).

**Why here** Every row is one shape — `label — what you get, and what it displaces` — so the five read as five wins rather than a mixed table. An earlier draft had three different shapes (`A → B`, a bare comparative, a bare adjective) and the last three rows never said what they were compared against. Comparatives throughout, no absolute figures: 01's tested phrasing is `a fraction of the hardware resources` / `under a quarter of the memory and cpu`, and the exact values stay in the blog and the attached table. Only one bold, on the memory row. Both bolds together would put a measurement and its own quotient side by side in a highlight strip, without the table structure that licenses showing them as separate rows.

### [4/6] Same desktop, same evaluators, same scores

```
[4/6] Same desktop, same evaluators, same scores

Across 13 models, CUA-Lite's Lite.OSWorld matches the original OSWorld VM. Every point is a run we did ourselves, on both sides. A cheaper desktop would be worth nothing otherwise.

The same model runs the same task the same way in the container as in the VM, judged by the same evaluators, so a score or a training signal earned in the container carries straight back to the real benchmark.
```

**Bold** `Across 13 models` · `matches the original OSWorld VM`

**Media** `assets/04-parity.png` — blog 2's `figure.par`, with the caption re-set to match this thread's copy

**Alt** A scatter plot of success rate on OSWorld against success rate on Lite.OSWorld for 13 models, with the points falling close to the diagonal.

**Source** `blog/kvm-free-osworld` §1 closing paragraph, near-verbatim — except `A cheaper desktop would be worth nothing otherwise.`, which is thread-original.

**Why here** The post that licenses everything after it: the example is faithful, so the base it runs on is worth building a family on. No hedge on `matches` — the exact deltas are in Pre-flight 7 for replies, per 写作规约 1.

### [5/6] Beyond OSWorld: scalable training sandboxes

```
[5/6] Beyond OSWorld: scalable training sandboxes

The VM-free container isn't just for OSWorld — it's a base for a family of scalable CUA-Lite sandboxes carrying 30k+ verifiable tasks, each re-hosting a public suite and generating new ones on top of it:

· Lite.OSWorld — OSWorld's 369 benchmark tasks plus 2k+ synthesized
· Lite.ScaleCUA — 20k+ tasks perturbed from OSWorld's evals
· Lite.CUAGym — browser and desktop tasks across mock sites and real apps
· Lite.CUAWorld — 40 professional apps across ~25 expert domains

Every task carries a verifiable reward, so the same sandbox that scores an agent can train one — SFT on its rollouts, or RL straight off the reward.
```

**Bold** `a family of CUA-Lite sandboxes carrying 30k+ verifiable tasks`

**Media** `assets/05-sandbox-family.mp4` — **blog 2's own `figure.belt-fig`**, not thread 01's belt. 01's clip comes from the other blog and shows different tiles; this one carries the four sandbox tabs and their per-sandbox gloss line, which is exactly what this post's copy lists.

**Alt** The sandbox family belt: tabs for Lite.OSWorld, Lite.ScaleCUA, Lite.CUAGym and Lite.CUAWorld, the selected tab's task count beneath them, and a grid of looping rollout recordings — Impress, Thunderbird, Calc, GIMP, VLC and a multi-app task.

**Source** Heading is `blog/kvm-free-osworld` §2's own heading, in full. The opening sentence is §2 with two changes — `CUA` → `CUA-Lite`, and `with verifiable tasks` → `carrying 30k+ verifiable tasks` (that figure is the homepage's, `index.html:65`). `each re-hosting a public suite:` is appended from 01's post [4/9]. The per-sandbox glosses are thread 01's post [4/9], which took them from `js/belt.js`.

**Why here** The payload, and it now names what the family contains instead of four bare proper nouns. Four unfamiliar `Lite.*` names with one shared gloss told a reader nothing; the glosses are what make the family real.

### [6/6] CUA-Lite: the open-source platform to benchmark and train computer-use agents

```
[6/6] CUA-Lite: the open-source platform to benchmark and train computer-use agents

Open sandboxes, open data, open infrastructure. The sandboxes share one interface, so one agent runs on all of them, and every task carries a verifiable reward, so each sandbox serves both benchmarking and training.

Run them on the laptop or CI runner you already have — no /dev/kvm, no VM image, room for five rollouts where one used to fit.

Try it, or bring your own sandboxes: add yours, and every agent trains and benchmarks on it, now and later.

github.com/cua-lite/cua-lite
cua-lite.github.io
```

**Bold** `Open sandboxes, open data, open infrastructure` · `every agent trains and benchmarks on it, now and later`

**Media** `assets/06-card.png`

**Alt** The CUA-Lite title card: "Any agent, on any computer", with the project's name and site.

**Source** Heading and `Try it, or bring your own sandboxes.` are `blog/kvm-free-osworld`'s own last line, verbatim. The two body sentences are `blog/why-cua-lite`'s Sandboxes section (`each sandbox serves both training and benchmarking`) and its call for contributors (`Add yours, and every agent trains and benchmarks on it — now and later`), both already approved in thread 01's post [9/9].

**Why here** The last post is the last thing a reader sees, so it names the project and says what it is, rather than repeating a slogan the attached card already displays in its own headline. The blog's closing line survives as the ask, `Try it, or bring your own sandboxes`. §2 gets two posts, not one — the blog's conclusion is short but it is the conclusion. Post 5 says what the family is; this says what it is for, and carries the ask. The blog's closing line had been used nowhere in either thread.

---

## 归属

This thread is entirely about re-hosting someone else's benchmark. OSWorld is credited by name in
post 1's copy; its authors are @-named in the first reply, the second-highest-exposure slot in a launch. **Handles are verified in `posts/twitter/01/README.md`'s handle
table — do not retype one from memory.** The ones this thread needs:

| @ | who | where it belongs |
|---|---|---|
| `@XLangNLP` | XLANG Lab — OSWorld's authors | the reply to post 1 |
| `@TianbaoX` | Tianbao Xie — OSWorld first author | the reply to post 1 |
| `@taoyds` | Tao Yu — OSWorld last author | the reply to post 1 |

**Reply to post 1** (post it yourself, immediately, so the credit is not a footnote):

```
OSWorld is @XLangNLP's — @TianbaoX, @taoyds and their co-authors built the desktop, the tasks and the evaluators. Lite.OSWorld keeps all three and only takes the virtual machine out from underneath.

github.com/xlang-ai/OSWorld
```

**第二条回复 —— 装 receipts 和上手命令**（01 判据 12：首条回复是全场第二高曝光位，要放证据图 + 一行
安装命令 + 一句第一人称）。归属占掉了第一条，所以这三样放第二条：

```
Receipts: same desktop, same evaluators, 13 models, VM vs container.

git clone github.com/cua-lite/cua-lite && uv sync --all-extras
uv run --no-sync bash lite/gym/envs/lite/osworld/scripts/install.sh

cua-lite.github.io/blog/kvm-free-osworld
```

**Media** `assets/04-parity.png` + `assets/03-footprint.png`（两张并排）。**注意宽高比不同** —— 表是 1.6 横向、散点是 0.9 纵向，X 的双图网格是裁切填充而非留白，横向的表在竖半格里会被切掉左右两侧，而那正是 `Lite.OSWorld` 那一列。发布前二选一，或先补边到同一比例。

**第一人称那句由你写** —— 我不代写。位置在这条回复的开头，一句话说你为什么做这件事。

**⚠️ 安装命令发布前必须在干净 checkout 上真跑一遍。** 01 上有过 Quick Start 被标成「verbatim from the
repo」而实际与仓库不符的先例。

**Why a reply and not a numbered post** — thread 01 carries a full acknowledgements closer for the
whole platform. Repeating it here would be filler; what this thread owes is one specific credit, and
the first reply to post 1 is the second-highest-exposure slot in the launch.
