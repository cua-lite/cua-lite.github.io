# CUA-Lite — LinkedIn 01（项目总览）

共享约定见 [`../../README.md`](../../README.md)（数字口径、平台规范、资产、领头图）。本篇是**项目宣告**：三支柱 + 机构背书。

改编自 `posts/red/01/README.md` 的 **English** 版。**内容相同，形态按 LinkedIn 重排**。

## 与小红书版的四点差异

1. **链接前置** —— LinkedIn 的链接可点击，所以主链接放在开头钩子之后，而不是压在页脚。
   （代价：站内普遍认为带站外链接的帖子触达会打折。若你更在意触达，就把链接挪到**第一条评论**，正文只留 “links in the comments”。两种都写在下面。）
2. **首两行定生死** —— 正文约 140–210 字符处会被折叠成 “…see more”，所以第一句必须自带信息量，不能是铺垫。
3. **标签 3–5 个足矣** —— 不是小红书那种 9–12 个；且必须是英文专业标签。
4. **@ 提及机构** —— 发布时把 `UC Berkeley` / `Microsoft` 换成真实的 @ 提及，触达和可信度都会涨。

---

## 正文（直接复制）

```
Training and benchmarking computer-use agents takes three things: sandboxes, data, and a framework. We're democratizing all three.

CUA-Lite → https://cua-lite.github.io
Code → https://github.com/cua-lite/cua-lite

Everything below works across desktop, browser, and mobile.

▪️ Sandboxes — efficient, with verifiable tasks
VM-free sandboxes carrying 30k+ CUA tasks with verifiable rewards, so the same sandbox serves both benchmarking and training. They reproduce external benchmarks such as OSWorld, and include our own training environments like CUAGym and CUAWorld.

▪️ Data — unified and open
10+ SFT datasets plus the latest rollouts from frontier CUAs, all in one format, free on Hugging Face: https://huggingface.co/cua-lite

▪️ Framework — eval, SFT, RL
One agent–environment interface, so any agent plugs into any environment. The rollouts it produces get reused three ways:

· Eval — scored to rank agents, across 15+ integrated benchmarks (OSWorld, OSWorld-2, WindowsAgentArena, WebArena, WebVoyager, AndroidWorld, MobileWorld, and more)
· SFT — one trajectory format, rendered by each model's adapter into its own, so any model's rollouts can fine-tune any other: GPT-5.5 → Qwen3-VL, for example
· RL — used as the learning signal, sampled continuously in the environment; GRPO, GSPO and more, on Slime

Sandboxes, data, and framework all keep growing. We'd like CUA-Lite to become a community-driven open-source CUA ecosystem — bring your datasets, environments, or agents.

Built at UC Berkeley and Microsoft.

#MachineLearning #AIAgents #ReinforcementLearning #OpenSource
```

### 变体：链接放评论区（若优先考虑触达）

正文删掉开头两行链接与 Hugging Face 那行，结尾改成 `Links in the comments. 👇`，然后首条评论发：

```
Site → https://cua-lite.github.io
Code → https://github.com/cua-lite/cua-lite
Data → https://huggingface.co/cua-lite
```

---

## 配图

`assets/` 下每张图都是指向 `posts/red/01/assets/` 的**软链**（`mode 120000`），不复制文件。
**只链英文版** —— LinkedIn 以英文为主，`*-zh.png` 未纳入。

- **单图**：`assets/01b-cover.png`（竖版，含桌面/浏览器/移动端三设备，信息量最足）
- **轮播**：`01b-cover.png` → `02-sandboxes.png` → `03-data.png` → `04-eval.png` → `05-train.png`
  （顺序＝主页叙事 hero→沙盒→数据→评测→训练）
> **建议试试 LinkedIn 的 document（PDF 轮播）**：把上面 5 张合成一个 PDF 发布，站内对 document 帖的触达通常好于普通多图帖，且读者可左右翻页。

---

## 发布前检查

- 事实与来源同 `posts/red/01/README.md` 的「来源」表，未改动任何数字。
- `#擦边` 等小红书标签**不要带过来**（LinkedIn 语境完全不适用）。
- 发布时把 “UC Berkeley and Microsoft” 换成真实 @ 提及。
- 首条评论主动认领作者身份，LinkedIn 上这是加分项。
