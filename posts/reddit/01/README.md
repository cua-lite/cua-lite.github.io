# CUA-Lite — Reddit 01（总览，改写为「训练你自己的本地 CUA 模型」）

**目标版块：** r/LocalLLaMA。
**不要发 r/MachineLearning 主版** —— 这篇是项目总览、没有新结果，主版只收有实质内容的 `[P]`；要发只能进每周的 `[D] Self-Promotion Thread`。

## 立论：rollout + train，不是 benchmark，也不是平台介绍

r/LocalLLaMA 的重心是**「把模型跑在自己机器上」**，但他们确实关心开源 GUI agent 模型（UI-TARS、OpenCUA、ScaleCUA、Qwen-VL 这类）。所以主线是：

> **拿开源模型去操作电脑 —— 跑、评、训三条路都开着；数据和环境都开源。**

开头刻意写成 **run, eval or train**：那个版块想让本地模型干活、或想知道自己模型能拿几分的人，远多于要训练的人。只说 train 会把他们挡在门外；只说 benchmark 又会把评测当成主框（曾经写歪过一次）。三个动词并列，谁都能对号入座。

**两个曾经写歪的方向，别再走回去：**
- ❌ 写成**平台介绍**（Data/Environments/Training 三支柱当卖点）—— 那是 LinkedIn 的骨架。
- ❌ 写成**评测**（"running desktop-agent benchmarks locally"）—— benchmark 只是环境的一种用法，不是本篇的重点。

**开头那段承担两件事**：说清痛点（数据 schema 不一 + 环境是重型虚拟机），并就地交代 `/dev/kvm`/嵌套虚拟化这个真实门槛 —— 它属于「heavy VMs」那半句，不该另起一段。

**不要贴代码。** 曾经写过一段三行的 `gym.make/agents.make` 片段，是从 README 推断而非从示例抄的，没跑过。Reddit 上会有人直接复制。要贴就先实跑验证。

LinkedIn 版的 `democratizing`、hashtag、`▪️`、链接前置 —— 一个都不要带过来。

---

## 标题（选一个）

1. ⭐ `CUA-Lite: run, eval or train an open model on real desktop tasks — without a VM`
2. `CUA-Lite: computer-use environments that run on plain Docker — no /dev/kvm, no nested virtualization`
3. `CUA-Lite: open data + desktop environments for training computer-use agents locally (Qwen3-VL, UI-TARS, and friends)`

标题里必须有 **CUA-Lite** —— 项目帖不带项目名，读者没有可搜索、可记住的抓手。

---

## 正文（markdown，直接粘）

```
If you want to run, eval, or train a model to actually use a computer — clicking through desktop apps, filling in web forms, tapping through a phone app — two things get in the way.

Sandboxes are heavy: a full virtual machine per task, so memory limits how many you can run at once, and the hardware virtualization it needs rules out WSL, many cloud instances, and anything already inside a container.

And before you get that far, you have to write the glue between model and screen yourself — how screenshots go in, what actions are available, how the output gets parsed. It differs for every model, so everyone writes it again.

We open-sourced all four pieces: the harness, the sandboxes, the data, and the framework for inference, eval, SFT, and RL.

**The harness.** That glue, modular and readable rather than a black box, shipped for 14 model families: GPT, Claude, and Gemini through their APIs, plus open weights like Qwen3-VL, Qwen2.5-VL, UI-TARS, EvoCUA, and Fara, which run on whatever inference stack you already use. Adding a model means writing one small piece, not a rewrite.

**Sandboxes.** Lightweight and VM-free — plain Docker, so they pack many per machine and roll out in parallel. 30k+ tasks across desktop, browser, and mobile, each with an automatic pass/fail check built in: run a model against one and get a score back without training anything. The same sandboxes are what you train in afterwards, so there's one setup instead of two. They include our ports of OSWorld and other public benchmarks, alongside sandboxes we built ourselves.

**Data.** 10+ existing computer-use datasets converted into a single format, plus rollouts recorded from frontier models, free on HF. Because the format is shared and each family has an adapter, data collected from one model can fine-tune another — GPT-5.5 rollouts fine-tuning Qwen3-VL, for example.

**Framework.** One interface over the other three: run a model for inference, score it on a benchmark, fine-tune it on the data with SFT, then reinforce it in the sandboxes — GRPO, GSPO, and others, on Slime.

Code: https://github.com/cua-lite/cua-lite
Datasets: https://huggingface.co/cua-lite
Docs and benchmarks: https://cua-lite.github.io

Disclosure: I'm one of the authors. If you've tried running, evaluating, or training a computer-use agent locally and hit a wall, I'd like to hear where — that's mostly what we've been fixing.
```

---

## 配图

`assets/` 全是软链（`mode 120000`），只链英文版；hero 动图链自 `posts/twitter/01/assets/`。

**首选 `01-hero.mp4`（1.4 MB）** —— agent 依次操作桌面、浏览器、手机，下方跟着实时 action trace（`click([502,563]) 1.1s` … `terminate("success")`）。

**为什么用它，不用封面卡：** 那张 `01b-cover.png` 是标语 + bullet + 数字条的图文卡，在 Reddit 技术版是**广告的标志**，而且内容和正文重复。这段 hero 是**证据**——「show me it working」正是该版块的文化。

- **格式**：优先 `.mp4` 而非 `.gif` —— Reddit 无论如何都把 GIF 转成视频播放器，直接给 mp4 画质更好、体积只有 1/4（1.4 MB vs 5.8 MB）。`01-hero.gif` 作为备用。
- **方向**：竖版（800×1083）正确，Reddit 流量以移动端为主；`01-hero-wide.mp4` 留给桌面场景。
- **补充图**：评论区可再给 `03-data.png`（真实 HF 数据表）—— 该版块对「数据长什么样」的兴趣远高于对封面的兴趣。

---

## 发布前检查

- **标题里必须有 CUA-Lite** —— 项目帖不带项目名，读者没有可搜索、可记住的抓手。
- **14 个模型家族适配器**：来源为代码库 `lite/agents/models/`，发布前 `ls` 一遍确认数目。
- **不写伪代码、不写实现细节**（参数名、函数签名、API 形状）—— 帖子讲能力和取舍，不讲接口。曾贴过一段没跑过的 `gym.make/agents.make`，也写过 `processor` / `generate_fn` 这种参数级描述，都已删除。
- **别把小红书/LinkedIn 的措辞带过来**：`democratizing`、hashtag、`▪️`、"Built at UC Berkeley and Microsoft"（改成正文末尾的 Disclosure 行）。
- 结尾那句**主动问对方踩过什么坑**是刻意的：r/LocalLLaMA 吃「一起解决问题」的姿态，不吃「我们发布了」的姿态。
- 账号需有发帖历史；避免与 Reddit 02 同日发。
