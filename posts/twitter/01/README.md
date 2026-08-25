# CUA-Lite — launch thread (X)

Nine posts, in order.

**How to read each entry below**

| Line | What to do with it |
|---|---|
| the ``` fenced text ``` | **This is the post.** Paste it as-is — nothing else in the entry gets posted. |
| **Media** | The file to attach from `assets/`, in the order listed. |
| **Alt** | Paste into X's "add description" box on that media (not into the post). |
| **Source** | Which page the wording came from — for keeping this in sync with the site. |
| **Why here** | Why the post sits at this position. Review note, never posted. |

**Voice:** the team ("we"), plain and technical. No hashtags, no emoji.
**Copy:** lifted from the site — the homepage's claims and both posts' bold leads are the
battle-tested wording, so each post reuses those sentences and only adds the connective
tissue that makes one thread out of three pages. Every heading is a heading or bold lead
off the site, so reading the nine headings alone gives the whole argument.
**Length:** posts run 264–529 characters (long posts, i.e. a Premium account). X collapses
each one at ~280 with "Show more" — a URL counts as 23 there, whatever its real length — so
every post is written to land its core claim ABOVE that fold, checked with a script, not
eyeballed. Posts 1, 2, 8 and 9 sit entirely above it (9 in particular: its whole job is the
links, so they must never be behind "Show more"). Where a post does fold, what stays visible
is: 3 the fix and its numbers · 4 the sandbox claim and the task count · 5 the schema claim ·
6 the interface · 7 the benchmark counts.
**Media:** every post carries exactly one, captured from those same pages, because the site's figures *are* the argument. Nothing here composes a new visual —
each clip is a figure the site already uses to make that argument, tabs and captions included.
**Links:** the repo in 1 and 9, the site in 9, Hugging Face in 5 — and nowhere else, since
X buries mid-thread links. Post 5's is the one exception worth the reach: the data is the
ask of that post, and "free on Hugging Face" with no address was the loudest gap a reader
review found.
**Regenerating the media:** `uv run python posts/twitter/01/make_assets.py` (see `make_assets.py`).

### Pre-flight, before the first post goes out

1. **`github.com/cua-lite/cua-lite` 404s today** — the repo is not public yet. It is linked
   from posts 1 and 9 (and from every page of the site). Either make it public first, or
   swap both to `cua-lite.github.io`. Checked 2026-08-22: site 200 · `huggingface.co/cua-lite` 200 · GitHub **200 (now public)**.
2. **Confirm the footprint numbers in post 3 are measured.** The VM-free post's own authoring
   note still says the comparison table's cells "stay skeletons until measured"; the values
   landed later (commit `40a0451`). Post 3 rests on them. If any is an estimate, label it or
   cut it — one unmeasured number discredits the other three. Note 4.1 / 0.9 = 4.56, so
   "~4.6× more instances" may be derived from the memory ratio rather than measured; if it
   is, post 3 is presenting one measurement as two and the × should go.
3. Re-check the two counts against the site: "15+ benchmarks integrated" (coverage board)
   and "11 with public leaderboards" (non-`pending` entries in `assets/exps/eval/manifest.json`).

---

## At a glance

The spine is the homepage's story. Post 2 names three gaps — heavy sandboxes, a per-dataset
schema, no standard framework — and posts 3, 5 and 6 close them in that order, each opening
by restating its gap in full and then turning on "Our answer is…". Posts 4, 7 and 8 extend
the answer that precedes them rather than opening a new gap. The VM-free post is cut in at 3 as the evidence for the
first: OSWorld is the environment everyone already knows, so it is the cheapest way into
lightweight sandboxes and verifiable tasks. Post 9 closes on the line post 1 opened with.

| # | Beat | Media |
|---|------|-------|
| 1 | Any agent, on any computer | `01-hero.mp4` portrait (`01-hero-wide.mp4` = landscape) |
| 2 | Computer-use agent resources are fragmented | `02-fragmented.mp4` |
| 3 | VM-free OS(World) at Scale | `03-vm-tax.mp4` |
| 4 | Sandboxes & verifiable tasks | `04-sandboxes.mp4` |
| 5 | One schema, any dataset | `05-litesample.mp4` |
| 6 | One framework: eval & RL | `06-litegym.mp4` |
| 7 | One command, any benchmark | `07-leaderboard.mp4` |
| 8 | SFT & RL, any open agent | `08b-rl.png` |
| 9 | Bring a dataset, an env, or an agent | `09-card.png` |

Spares, for replies or a quote-tweet — not part of the nine:
`extra-footprint.png` (the OSWorld vs Lite.OSWorld table), `extra-parity.png` (13 models,
scores matching within a few points), `extra-side-by-side.mp4` (the same model on the same task,
VM vs container — it visits 3 of the player's 7 task tabs). See the reply plan below.

---

## The thread

### 1 / 9 — Any agent, on any computer

```
1/9 · Any agent, on any computer

· Sandboxes — efficient environments with 30k+ verifiable CUA tasks
· Data — 10+ SFT datasets plus fresh rollouts from frontier CUAs
· Eval, SFT, and RL any agent: desktop, browser, mobile

CUA-Lite — UC Berkeley · Microsoft
github.com/cua-lite/cua-lite
```

**Source** Homepage hero (`index.html:62-75`) — the lead and all three claims, verbatim.
**Media** `assets/01-hero.mp4` — one agent driving a desktop, a browser and a phone, with its
live action trace under it. Regenerated by `scripts/make_demo_gif.py` (the same generator
behind the repo's own `assets/demo-trace.mp4`, and identical to it: white ground, native
1368×1852, no wordmark — the one asset that is not on the cream card, because matching the
project's canonical demo beats matching the other eight). Portrait, because X is mobile-first
and a tall clip fills that screen; `01-hero-wide.mp4` is the same tour in the generator's
landscape layout (device left, trace right) rather than a crop of this one. Note X re-encodes anything over 1200px on the short side.
**Alt** An agent fills a spreadsheet, searches the web and sends a message, while a terminal
logs each click and keystroke it takes.

### 2 / 9 — Computer-use agent resources are fragmented

```
2/9 · Computer-use agent resources are fragmented

· Sandboxes are heavy — a full virtual machine per task
· Every dataset picks its own schema, so data collected for one agent can't train another
· No framework standardizes eval, SFT or RL

CUA-Lite closes all three.
```

**Source** "Why CUA-Lite" opening paragraph, verbatim — bold lead as the heading, its three problems
in the site's own order, then the pivot.
**Media** `assets/02-fragmented.mp4` — every dataset and benchmark reaching for every agent,
each pairing dying in the same grey tangle.
**Alt** Lines from Mind2Web, GUIOdyssey, OSWorld and WebArena to GPT, Claude, Qwen and Gemini,
accumulating into a dead tangle.
**Why here** Lists the three gaps in the order the thread closes them — sandboxes (3–4),
schema (5), framework (6–8). Posts 3, 5 and 6 each open by restating their gap in full and
then turning on "Our answer is…", so a reader who meets that post cold still gets both halves.

### 3 / 9 — VM-free OS(World) at Scale

```
3/9 · VM-free OS(World) at Scale

Gap 1 — sandboxes are heavy: a full VM per task, needing /dev/kvm. Our answer is a series of lightweight, VM-free sandboxes. Lite.OSWorld (ours) keeps OSWorld's desktop and drops the VM: a fraction of the memory, several times more instances per host.

Same task, same score: across 13 models the container's scores track the VM's within a few points.

The same recipe reproduces other benchmarks and generates verifiable tasks to train on.
```

**Source** The VM-free post: its title as the heading, its thesis sentence and the Lite.OSWorld
bold lead verbatim, then the comparison table and the parity plot.
**Media** `assets/03-vm-tax.mp4` — the second sentence, beat for beat: the desktop sheds its
Ubuntu.qcow2 / QEMU·KVM stack and its /dev/kvm dependency, becomes a container, then replicates
into a grid of parallel rollouts (the "several times more instances per host").
**Alt** An OSWorld desktop sealed in a VM sheds the VM to become a Docker container, which then
multiplies into a grid of parallel rollouts.
**Why here** Problem and fix in one post, because the clip already carries both. OSWorld is the
environment readers already know, so it is the cheapest way into lightweight sandboxes.

### 4 / 9 — Sandboxes & verifiable tasks

```
4/9 · Sandboxes & verifiable tasks

That base runs a family of sandboxes, not one: each packs many to a machine, runs in parallel, and every task is verifiable — so the same task serves both training and benchmarking. 30k+ verifiable tasks so far.

Three more of ours beyond Lite.OSWorld: Lite.ScaleCUA (20k+ tasks perturbed from OSWorld's evals), Lite.CUAGym (browser and desktop tasks across mock sites and real apps), Lite.CUAWorld (40 professional apps across ~25 expert domains — GMAT flying spacecraft, PyMOL turning proteins).
```

**Source** "Why CUA-Lite" § Sandboxes & verifiable tasks (heading + bold lead) and the VM-free
post's "Beyond OSWorld" lead, verbatim.
**Media** `assets/04-sandboxes.mp4` — the post's own rollout belt, walked across all four
families at 2.6s each (11s total). It opens on Lite.CUAWorld, whose GMAT and PyMOL desktops
are the least familiar thing in the thread, rather than on another LibreOffice window; the
site-only caption ("click a tile for the full rollout") is hidden, since a reader can't act
on it here.
**Alt** A belt of looping agent rollouts across four sandbox families in the order shown —
Lite.CUAWorld, Lite.CUAGym, Lite.ScaleCUA, Lite.OSWorld — each tab carrying its own line of
task counts and apps.
**Why here** Generalises post 3: one reproduced benchmark becomes the family the belt shows.
It opens on "Beyond OSWorld" so it advances rather than restating post 3's first sentence.

### 5 / 9 — One schema, any dataset

```
5/9 · One schema, any dataset

Gap 2 — every dataset arrives in its own schema, so data collected for one agent can't train another. Our answer is one schema for all of them: convert a dataset once, and every agent can train on it.

That schema is LiteSample, shared across every env, agent, and task type: 10+ existing CUA datasets converted, plus fresh rollouts from frontier CUAs. CUA-Lite then ships an adapter per model, packing a unified LiteSample into the exact training format each one needs.

huggingface.co/cua-lite
```

**Source** Homepage `#data` heading; body = "Why CUA-Lite" § Datasets — both bold leads verbatim,
plus the homepage Data claim.
**Media** `assets/05-litesample.mp4` — datasets folding into one schema, then an adapter packing
it into each model's own training format.
**Alt** Mind2Web, GUIOdyssey, ScaleCUA and OpenCUA converge into LiteSample, which an adapter
feeds to Qwen, UI-TARS, MAI-UI and Kimi.
**Why here** Closes the second gap from post 2. Sandboxes are where an agent practises;
this is what it learns from first.

### 6 / 9 — One framework: eval & RL

```
6/9 · One framework: eval & RL

Gap 3 — nothing standardizes how computer-use agents are evaluated and trained, so every project rebuilds the same loop. Our answer is one interface that any agent plugs into, for any environment.

They meet in lite.gym — screenshots up, actions down, one action space per platform plus each env's extra tools. The same loop serves both eval and RL: a rollout is scored to rank an agent, or trained on to improve it.
```

**Source** "Why CUA-Lite" § One framework: eval & RL — heading and paragraph, verbatim.
**Media** `assets/06-litegym.mp4` — an environment and an agent trading screenshots and actions
through the lite.gym hub, then swapping for the next pair.
**Alt** OSWorld, WebArena, AndroidWorld and WebGym connect through lite.gym to GPT, Claude,
Qwen and Gemini; the board pairs them one at a time — a screenshot travels up to the agent
and an action, click or tap, comes back down.
**Why here** Closes the third gap. Data and sandboxes only pay off if one framework drives them.

### 7 / 9 — One command, any benchmark

```
7/9 · One command, any benchmark

That interface is already running: 15+ benchmarks integrated, 11 with a leaderboard on the site today — every score on them is a run of ours.

A unified action space per platform means one script evals any agent on any benchmark — swap --model-id and --env-id (and its config): desktop, browser, mobile, grounding.
```

**Source** Homepage `#benchmarks` — heading and section lead, verbatim; the counts come from the
coverage board and `assets/exps/eval/manifest.json`.
**Media** `assets/07-leaderboard.mp4` — the eval command and its leaderboard switching benchmarks
together, across four real boards.
**Alt** An eval command's --env-id changes from OSWorld to WebVoyager to AndroidWorld to
ScreenSpot-Pro, and the leaderboard under it reloads with each benchmark's scores.
**Why here** Turns post 6's interface from a diagram into results.

### 8 / 9 — SFT & RL, any open agent

```
8/9 · SFT & RL, any open agent

The datasets and the sandboxes above are what you train on, in that order.

First SFT: pick a dataset and the model you want to train, and CUA-Lite exports that data in the format that model expects.

Then RL: pick a model and a sandbox, let it roll out, and each task's verifiable reward scores the rollout — that score is the training signal. GRPO and beyond, on THUDM's Slime.
```

**Source** Homepage `#train` — heading, section lead and both panel notes, verbatim.
**Media** `assets/08b-rl.png` — the RL panel: MODEL_ID + ENV_ID → run_grpo.sh. Four lines,
and the only one of the two training panels that survives X's display width; the SFT
pipeline is twenty lines and turns to grey at 600px, so it goes in the reply below. The SFT
half is not unillustrated either way — post 5's clip ends on its `export_sft` command.
(A still, not a clip: these panels are static terminals, so a capture played as a slideshow.)
**Alt** A terminal showing MODEL_ID, ENV_ID and CONFIG_PATH passed to run_grpo.sh, with the
model and env picked from dropdowns.
**Why here** Posts 1 and 6 promise SFT and RL; this is the only post that shows them. Without it the
thread proves eval and merely asserts training.

### 9 / 9 — Bring a dataset, an env, or an agent

```
9/9 · Bring a dataset, an env, or an agent

Add an environment, and every agent can be trained and measured in it. Convert a dataset, and every agent can train on it — including models that don't exist yet. Integrate an agent once, and it runs on all of the above.

That is what one schema and one interface buy: whatever you add works with everything already there.

github.com/cua-lite/cua-lite
cua-lite.github.io
```

**Source** "Why CUA-Lite" — both calls for contributors and the closing line, verbatim.
**Media** `assets/09-card.png` — the project card.
**Alt** CUA-Lite title card: "Any agent, on any computer" with 30k+ tasks, 10+ datasets,
10+ agents, 15+ benchmarks.

---

## Posting notes

- **One media per post.** Two images in one post halve each one's width, which is what made
  the training terminal unreadable; the RL half goes in a reply instead. Every clip loops
  silently under ~60s; X autoplays them muted.
- **Clips are cut to loop and to open on motion.** Each is trimmed to a whole number of its
  figure's own animation cycle — 5.93s for the tangle, 7s for the VM figure, 5.2s for the
  pair-boards (the numbers are in the pages' own JS) — and the exact wrap point is picked by
  matching the last frames against the first. Measured seam error, 0 = perfect: 02 0.3 ·
  03 0.3 · 05 0.4 · 07 0.4 · 06 1.5 · 04 17.6 (its tiles each loop a rollout on its own clock,
  so the tile contents jump at the wrap even though the layout doesn't) · 01 49 (the hero tour
  ends on the phone and restarts on the desktop — inherent to a three-device tour, and it is
  the project's own canonical demo). Openings were re-cut too: 02 and 05 used to sit frozen
  for the first 2-3 seconds, which is the entire window a scrolling reader gives them.
- **Links** live in post 1 and post 9 only — X buries mid-thread links. Post 1 carries a
  clip, so X shows the clip instead of a link card. That's intended.
- **Alt text** is worth pasting in: this audience uses it, and the figures are the argument.
- **Spares**, for replies or a quote-tweet: `extra-footprint.png` and `extra-parity.png`
  (the table and parity plot behind post 3's numbers) and `extra-side-by-side.mp4` (the
  same model on the same task, VM vs container). The first reply to post 3 is the natural
  place for them.
- **Blog links**, if someone asks for detail: `/blog/kvm-free-osworld/` answers posts 3–4,
  `/blog/why-cua-lite/` answers 2 and 5–9.

## Two replies to write in advance

Each post carries one media, so the evidence that does not fit goes in a reply on the same
post — one tap away, and ready before anyone asks.

**Reply to post 3 — the receipts.** Post 3 asserts the numbers; this shows them.

```
The receipts — same task suite, same evaluators, 13 models:
memory, cold start, parallelism, and every model's score in the VM vs in the container.

Full write-up: cua-lite.github.io/blog/kvm-free-osworld/
```

**Media** `assets/extra-footprint.png`, `assets/extra-parity.png`. (`extra-side-by-side.mp4`
— the same model on the same task, VM left, container right — is a good third, in a
follow-up reply rather than the same post.)

**Reply to post 8 — the SFT pipeline in full.** Post 8 shows the RL command; this is the
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
`make_assets.py`, since the media is captured from those same pages.

**Open check before posting:** the footprint numbers in post 3 come from the comparison
table, but that post's authoring note still says the table's cells "stay skeletons until
measured". They were added later (commit `40a0451`), so they look measured — confirm that
before posting, and drop the stale note from the post if so.
