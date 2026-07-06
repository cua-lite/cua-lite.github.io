/* ============================================================
   CUA-Lite — one agent, any computer.
   The same agent operates three platforms, each its own device:
   desktop (a pixel CRT running LibreOffice Calc), web (a browser),
   mobile (a phone). The lead words desktop/web/mobile are the control;
   on load it tours all three once, then rests home and lets you drive.
   Shared engine: think → move → act, GPU-composited cursor.
   Reduced motion: the desktop finished frame, held still.
   ============================================================ */
(function () {
  "use strict";
  const stage = document.getElementById("stage");
  if (!stage) return;

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const capRun = document.getElementById("cap-run");
  const rlLog = document.getElementById("rl-log");
  const plats = [...document.querySelectorAll(".plat")];   // the lead words = the control
  const demoHint = document.getElementById("demo-hint");
  let hintDone = false;   // once you've edited a score, stop inviting
  const showHint = () => { if (demoHint && !hintDone && mode === "desktop") demoHint.classList.add("show"); };
  const hideHint = () => { if (demoHint) demoHint.classList.remove("show"); };

  let timers = [];
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  const clearAll = () => { timers.forEach(clearTimeout); timers = []; };

  // the rollout streams line by line, like a live log
  const logClear = () => { rlLog.innerHTML = ""; };
  function logLine(text, cls, lat) {
    const prev = rlLog.querySelector(".rl-line.live");
    if (prev) prev.classList.remove("live");
    const el = document.createElement("div");
    el.className = "rl-line " + (cls || "live");
    const mark = /done/.test(cls || "") ? "✓" : /think/.test(cls || "") ? "⋯" : "›";
    const caret = (cls || "").includes("live") ? '<span class="caret"></span>' : "";
    const time = lat ? `<span class="rl-lat">${lat}</span>` : "";
    el.innerHTML = `<span class="rl-mark">${mark}</span><span class="rl-text">${text}${caret}</span>${time}`;
    rlLog.appendChild(el);
    return el;
  }

  /* ---------- shared engine (operates on a per-device ctx) ---------- */
  function ctxFor(deviceEl) {
    const screen = deviceEl.querySelector(".screen, .bw-view, .ph-screen");
    return { el: deviceEl, screen, cursor: screen.querySelector(".mouse-cur"), spark: screen.querySelector(".spark"), cx: 0, cy: 0 };
  }
  function place(ctx, x, y) { ctx.cx = x; ctx.cy = y; ctx.cursor.style.transform = `translate3d(${x}px, ${y}px, 0)`; }
  function centerOf(ctx, t) {
    const el = ctx.screen.querySelector(`[data-t="${t}"]`); if (!el) return null;
    const sr = ctx.screen.getBoundingClientRect(), r = el.getBoundingClientRect();
    return { x: r.left - sr.left + r.width / 2, y: r.top - sr.top + r.height / 2, el };
  }
  function moveTo(ctx, t) {
    const c = centerOf(ctx, t); if (!c) return;
    const d = Math.hypot(c.x - ctx.cx, c.y - ctx.cy);
    const dur = Math.min(0.36, Math.max(0.22, d / 700));
    ctx.cursor.style.transitionDuration = dur + "s";
    place(ctx, c.x, c.y);
  }
  function click(ctx, t) {
    const c = centerOf(ctx, t); if (!c) return;
    ctx.spark.style.left = c.x + "px"; ctx.spark.style.top = c.y + "px";
    ctx.spark.classList.remove("go"); void ctx.spark.offsetWidth; ctx.spark.classList.add("go");
    c.el.classList.add("press"); at(150, () => c.el.classList.remove("press"));
  }
  function typeInto(el, baseCls, text) {
    const base = baseCls ? baseCls + " " : "";
    el.className = base + "typed caret"; let i = 0;
    (function tick() {
      el.textContent = text.slice(0, i);
      if (i++ <= text.length) at(21 + Math.random() * 15, tick);
      else { el.className = base + "typed"; }
    })();
  }

  /* ---------- element refs ---------- */
  const $ = (s) => document.querySelector(s);
  // desktop
  const fbar = $("#fbar"), total = $("#total");
  const cells = ["b2", "b3", "b4"].map((id) => document.getElementById(id));
  const numOf = (el) => parseInt((el.textContent || "").replace(/[^0-9]/g, ""), 10) || 0;
  const fmt = (n) => n.toLocaleString("en-US");
  const sum = () => cells.reduce((a, e) => a + numOf(e), 0);
  const avg = () => sum() / cells.length;
  // web
  const wq = $("#wq"), wfield = $(".dev-web [data-t='search']");
  const ggHome = $("#gg-home"), ggResults = $("#gg-results"), ggSite = $("#gg-site"), bwHost = $("#bw-host");
  // mobile
  const mname = $("#mname"), minput = $(".dev-mobile [data-t='name']"), msave = $(".dev-mobile [data-t='save']");
  const msent = $("#msent");

  /* ---------- the three platforms ---------- */
  const MODES = {
    desktop: {
      // a spreadsheet of CUA-Lite benchmark scores; the agent averages them
      env: "osworld",
      instr: "average the scores",
      device: $(".dev-desktop"),
      reset() {
        fbar.innerHTML = '<span class="mk-ph"></span>'; fbar.className = "sh-formula";
        total.textContent = ""; total.classList.remove("filled", "sel");
      },
      steps: [
        { t: "cell", cap: "click([812, 648])", onAct: () => total.classList.add("sel") },
        { t: "fbar", cap: "click([430, 128])", onAct: () => {} },
        { t: "fbar", noClick: true, cap: 'type("=AVERAGE(B2:B4)")', typeLen: 15, onAct: () => typeInto(fbar, "sh-formula", "=AVERAGE(B2:B4)") },
        { t: "fbar", noClick: true, cap: 'key(["enter"])', onAct: () => at(120, () => { total.textContent = avg().toFixed(1); total.classList.add("filled"); }) },
        { done: true, cap: 'terminate("success")' },
      ],
      finished() { fbar.className = "sh-formula typed"; fbar.textContent = "=AVERAGE(B2:B4)"; total.textContent = avg().toFixed(1); total.classList.add("filled", "sel"); },
    },
    web: {
      // Google → search "cua-lite" → open this very homepage
      env: "webvoyager",
      instr: "look up cua-lite",
      device: $(".dev-web"),
      reset() {
        wq.textContent = "Search Google or type a URL"; wq.className = "mk-ph";
        wfield.classList.remove("hot");
        ggHome.classList.add("show"); ggResults.classList.remove("show"); ggSite.classList.remove("show");
        bwHost.textContent = "google.com";
      },
      steps: [
        { t: "search", cap: "click([500, 470])", onAct: () => wfield.classList.add("hot") },
        { t: "search", cap: 'type("cua-lite")', typeLen: 8, onAct: () => typeInto(wq, "", "cua-lite") },
        { t: "go", cap: "click([434, 566])", onAct: () => { ggHome.classList.remove("show"); ggResults.classList.add("show"); bwHost.textContent = "google.com/search?q=cua-lite"; } },
        { t: "open", cap: "click([286, 292])", onAct: () => { ggResults.classList.remove("show"); ggSite.classList.add("show"); bwHost.textContent = "cua-lite.github.io"; } },
        { done: true, cap: 'terminate("success")' },
      ],
      finished() { wq.textContent = "cua-lite"; wq.className = "typed"; ggHome.classList.remove("show"); ggResults.classList.remove("show"); ggSite.classList.add("show"); bwHost.textContent = "cua-lite.github.io"; },
    },
    mobile: {
      // texting ZHZisZZ about why CUA-Lite is good
      env: "androidworld",
      instr: "text ZHZisZZ about cua-lite",
      device: $(".dev-mobile"),
      reset() {
        mname.textContent = "iMessage"; mname.className = "mk-ph"; minput.classList.remove("hot");
        msent.classList.remove("show"); msave.classList.remove("sent");
      },
      steps: [
        { t: "name", cap: "tap([432, 900])", onAct: () => minput.classList.add("hot") },
        { t: "name", cap: 'type("yep — desktop, web & mobile")', typeLen: 26, onAct: () => typeInto(mname, "", "yep — desktop, web & mobile 🚀") },
        { t: "save", cap: "tap([928, 904])", onAct: () => at(120, () => { msent.classList.add("show"); msave.classList.add("sent"); mname.textContent = "iMessage"; mname.className = "mk-ph"; minput.classList.remove("hot"); }) },
        { done: true, cap: 'terminate("success")' },
      ],
      finished() { msent.classList.add("show"); msave.classList.add("sent"); mname.textContent = "iMessage"; mname.className = "mk-ph"; },
    },
  };
  const ORDER = ["desktop", "web", "mobile"];

  /* ---------- run one platform's task ---------- */
  const ts = (ms) => (ms / 1000).toFixed(1) + "s";
  function runSeq(ctx, steps, onFinish) {
    clearAll(); logClear();
    let t = 240;
    { const tt = t; at(tt, () => logLine("thinking", "think live", ts(tt))); }   // plan once, then act — briskly
    t += 520;
    steps.forEach((s) => {
      const tt = t;
      if (s.done) { at(tt, () => logLine(typeof s.cap === "function" ? s.cap() : s.cap, "done", ts(tt))); t += 480; return; }
      at(tt, () => { moveTo(ctx, s.t); logLine(s.cap, "live", ts(tt)); });
      at(tt + 380, () => { if (!s.noClick) click(ctx, s.t); s.onAct && s.onAct(); });
      t += 380 + (s.typeLen ? s.typeLen * 30 + 170 : 150) + 170;
    });
    at(t, onFinish);
  }

  /* ---------- mode manager: continuous auto-cycle, steered by the lead words ---------- */
  let mode = "desktop";
  let ctx = ctxFor(MODES.desktop.device);
  let running = false, paused = false, started = false, visible = false;

  function syncPlats() { plats.forEach((p) => p.classList.toggle("on", p.dataset.mode === mode)); }
  function parkCursor() {
    const s = ctx.screen;
    ctx.cursor.style.transition = "none";
    place(ctx, s.clientWidth * 0.7, s.clientHeight * 0.8);
    requestAnimationFrame(() => { ctx.cursor.style.transition = ""; });
  }
  function activate(m, skipReset) {
    const prev = mode;
    mode = m; ctx = ctxFor(MODES[m].device);
    document.querySelectorAll(".stage .device").forEach((d) => {
      const on = d.dataset.mode === m;
      d.classList.toggle("active", on);
      d.classList.toggle("exit", !on && d.dataset.mode === prev && prev !== m);   // outgoing slides out
    });
    syncPlats();
    capRun.innerHTML = `<span class="c-p">$</span> rollout.py <span class="c-flag">--env-id</span> <span class="c-env">${MODES[m].env}</span> <span class="c-flag">--instruction</span> <span class="c-val">"${MODES[m].instr}"</span>`;
    if (!skipReset) { MODES[m].reset(); logClear(); }
  }
  // the desktop task, shown already-complete (no re-run): the rest/home state
  function showDesktopDone() {
    MODES.desktop.finished();
    logClear();
    logLine("thinking", "think", "0.2s");
    [['click([812, 648])', "0.6s"], ['type("=AVERAGE(B2:B4)")', "1.1s"], ['key(["enter"])', "1.6s"]].forEach(([l, tt]) => logLine(l, "past", tt));
    logLine('terminate("success")', "done", "2.0s");
    requestAnimationFrame(() => { ctx.cursor.style.transition = "none"; const c = centerOf(ctx, "fbar"); if (c) place(ctx, c.x, c.y); });
    showHint();
  }
  // the intro tours all three machines ONCE (desktop → web → mobile), then
  // settles home on the finished desktop and invites you to drive. Calm and
  // confident, not a restless loop — the lead words steer it any time.
  let advances = 0, settled = false;
  function advance() { advances++; const i = ORDER.indexOf(mode); switchTo(ORDER[(i + 1) % ORDER.length]); }
  const held = () => paused || !visible;   // don't advance while hovered or off-screen
  function holdThenAdvance() { at(held() ? 500 : 700, () => { if (held()) holdThenAdvance(); else advance(); }); }
  // land back home without re-running the task — just show it complete + invite
  function settleHome() {
    clearAll(); running = false; settled = true; stage.classList.remove("snappy");
    activate("desktop", true);
    at(360, showDesktopDone);
  }

  function runActive() {
    running = true;
    MODES[mode].reset();
    runSeq(ctx, MODES[mode].steps, () => {
      running = false;
      if (!settled) {
        if (advances < ORDER.length - 1) holdThenAdvance();   // more machines to visit
        else at(1700, settleHome);                            // shown all three → dwell on the finished mobile, then settle home
      } else if (mode === "desktop") { showHint(); }          // driving now → rest here, invite edits
    });
  }
  // immediate = a user drove this (hover/click a lead word) → respond crisply.
  // the auto-tour leaves it off so its handoff stays calm and unhurried.
  function switchTo(m, immediate) {
    clearAll(); running = false; hideHint();
    stage.classList.toggle("snappy", !!immediate);
    activate(m); parkCursor();
    at(immediate ? 210 : 420, runActive);
  }
  // you changed a score → the agent re-runs on YOUR numbers. A short focused
  // response (~1s), not the whole select/type/enter ceremony — crisp feedback.
  function recompute() {
    clearAll(); running = true;
    logClear();
    fbar.className = "sh-formula typed"; fbar.textContent = "=AVERAGE(B2:B4)";
    total.textContent = ""; total.classList.remove("filled"); total.classList.add("sel");
    at(60, () => logLine('key(["enter"])', "live", "0.1s"));
    at(520, () => { total.textContent = avg().toFixed(1); total.classList.add("filled"); });
    at(820, () => logLine('terminate("success")', "done", "0.6s"));
    at(1000, () => { running = false; });
  }

  /* ---------- editable desktop cells: edit the numbers, the agent sums YOURS ---------- */
  const editing = () => document.activeElement && document.activeElement.classList && document.activeElement.classList.contains("editable");
  let sheetDirty = false;   // did you actually change a score? only then does the agent re-run
  cells.forEach((el) => {
    el.addEventListener("focus", () => { paused = true; hintDone = true; hideHint(); });   // engaged → stop inviting
    el.addEventListener("input", () => { sheetDirty = true; if (mode === "desktop" && !running) { total.textContent = ""; total.classList.remove("filled", "sel"); fbar.innerHTML = '<span class="mk-ph"></span>'; fbar.className = "sh-formula"; } });
    // click away after editing → the agent re-runs on YOUR number (no hidden keypress needed)
    el.addEventListener("blur", () => {
      el.textContent = fmt(numOf(el));
      at(430, () => { if (!editing()) { paused = false; if (sheetDirty) { sheetDirty = false; recompute(); } } });
    });
    el.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); el.blur(); } });
  });

  /* ---------- the lead words steer the demo ---------- */
  plats.forEach((p) => {
    const m = p.dataset.mode;
    p.addEventListener("pointerenter", () => { paused = true; if (started && m !== mode) switchTo(m, true); });
    p.addEventListener("pointerleave", () => { paused = false; });
    p.addEventListener("click", () => { paused = false; if (m !== mode) switchTo(m, true); });
    p.setAttribute("tabindex", "0");
    p.addEventListener("focus", () => { if (started && m !== mode) switchTo(m, true); });
  });

  if (reduce) {
    ORDER.forEach((m) => MODES[m].reset());
    activate("desktop", true); showDesktopDone();   // static finished frame + invite
  } else {
    activate("desktop"); parkCursor();
    if ("IntersectionObserver" in window) {
      // persistent: start on first view, and pause the cycle whenever off-screen
      const io = new IntersectionObserver((es) => { es.forEach((e) => {
        visible = e.isIntersecting;
        // first view: let the orchestrated entrance land, THEN the agent boots
        // up and types its first command — a deliberate beat, not a race.
        if (visible && !started) { started = true; at(900, runActive); }
      }); }, { threshold: 0.25 });
      io.observe(stage);
    } else { visible = true; started = true; runActive(); }
  }

  // hover the device to hold the current platform (read it, edit it); leaving resumes the cycle
  if (!reduce) {
    stage.addEventListener("pointerenter", () => { if (started) paused = true; });
    stage.addEventListener("pointerleave", () => { if (!editing()) paused = false; });
  }

  /* ---------- the live HF dataset browser: one quiet dropdown swaps the viewer ---------- */
  const hfFrame = document.getElementById("hf-frame");
  if (hfFrame) {
    // the two README sources — a hardcoded snapshot that gets replaced live from
    // the real HF collections below, so the menu always matches what's on the Hub.
    let GROUPS = {
      Rollouts: ["WebGym", "Lite.OSWorld", "CuaGymDesktopGPT55AuditV0"],
      Corpora: ["Aguvis", "ScaleCUA", "OpenCUA", "GUIAct", "GUIOdyssey", "GUI-360",
                "Multimodal-Mind2Web", "CAGUI", "UI-Genie-Agent"],
    };
    const sel = document.getElementById("hf-select");
    const trigger = document.getElementById("hf-trigger");
    const menu = document.getElementById("hf-menu");
    const nameEl = document.getElementById("hf-tg-name");
    const openEl = document.getElementById("hf-open");
    let ds = "WebGym", started = false, loadTok = 0;

    function load(name) {
      ds = name;
      const tok = ++loadTok;
      const id = "cua-lite/" + name;
      openEl.href = "https://huggingface.co/datasets/" + id;
      hfFrame.classList.remove("loaded");
      const old = hfFrame.querySelector("iframe");
      if (old) old.remove();
      const f = document.createElement("iframe");
      f.title = name + " dataset viewer on Hugging Face";
      f.loading = "lazy";
      f.src = "https://huggingface.co/datasets/" + id + "/embed/viewer/default/train";
      // the iframe 'load' fires when the HF shell loads; the data streams in a
      // beat later, so hold the dark skeleton a moment more before crossfading.
      f.addEventListener("load", () => setTimeout(() => { if (tok === loadTok) hfFrame.classList.add("loaded"); }, 2200));
      hfFrame.appendChild(f);
    }
    function pick(name) {
      nameEl.textContent = name;
      menu.querySelectorAll(".hf-opt").forEach((o) => o.classList.toggle("active", o.dataset.ds === name));
      if (started) load(name); else ds = name;
    }
    function buildMenu() {
      menu.innerHTML = "";
      for (const g of ["Rollouts", "Corpora"]) {
        const h = document.createElement("div"); h.className = "hf-grp"; h.textContent = g; menu.appendChild(h);
        GROUPS[g].forEach((name) => {
          const o = document.createElement("button");
          o.className = "hf-opt" + (name === ds ? " active" : "");
          o.dataset.ds = name; o.textContent = name; o.setAttribute("role", "option");
          o.addEventListener("click", () => { pick(name); close(); });
          menu.appendChild(o);
        });
      }
    }
    const open = () => { sel.classList.add("open"); trigger.setAttribute("aria-expanded", "true"); };
    const close = () => { sel.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); };
    trigger.addEventListener("click", (e) => { e.stopPropagation(); sel.classList.contains("open") ? close() : open(); });
    document.addEventListener("click", (e) => { if (!sel.contains(e.target)) close(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });
    buildMenu();

    // rebuild the menu from the live HF collections — never let it drift from the Hub
    (async () => {
      try {
        const parse = async (slug) => {
          const r = await fetch("https://huggingface.co/api/collections/cua-lite/" + slug);
          if (!r.ok) throw new Error(slug);
          const d = await r.json();
          return d.items.filter((i) => i.type === "dataset").map((i) => i.id.split("/").pop());
        };
        const [rol, cor] = await Promise.all([parse("rollouts"), parse("corpora")]);
        if (rol.length && cor.length) {
          GROUPS = { Rollouts: rol, Corpora: cor };
          if (!rol.includes(ds) && !cor.includes(ds)) { ds = rol[0]; nameEl.textContent = ds; if (started) load(ds); }
          buildMenu();
        }
      } catch (e) { /* offline / API change → keep the hardcoded snapshot */ }
    })();

    const start = () => { if (!started) { started = true; load(ds); } };
    if ("IntersectionObserver" in window) {
      const hio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { hio.disconnect(); start(); } }), { rootMargin: "500px" });
      hio.observe(hfFrame);
    } else { start(); }
  }

  /* ---------- command builders: the REAL rollout / run_grpo commands ----------
     Any agent × any env — the full matrix, not a curated subset. Model-ids and
     config families are all real (scripts/configs); picking an agent updates its
     --model-id AND the derived --config-path family. Eval envs = the benchmarks
     (docs/eval.md); RL envs = the training gyms. Verified vs README + docs. */
  // Mirrors lite/agents/factory.py — API families (gpt, claude) eval-only; the rest are open-weight (trainable).
  const AGENTS = [
    { model: "gpt-5.5", family: "gpt", api: true },
    { model: "gpt-5.4", family: "gpt", api: true },
    { model: "claude-opus-4-7", family: "claude", api: true },
    { model: "claude-opus-4-6", family: "claude", api: true },
    { model: "claude-sonnet-4-6", family: "claude", api: true },
    { model: "Qwen/Qwen3-VL-8B-Instruct", family: "qwen3_vl" },
    { model: "Qwen/Qwen3-VL-32B-Instruct", family: "qwen3_vl" },
    { model: "Qwen/Qwen3-VL-4B-Instruct", family: "qwen3_vl" },
    { model: "Qwen/Qwen3-VL-2B-Instruct", family: "qwen3_vl" },
    { model: "Qwen/Qwen3.5-4B", family: "qwen3_5" },
    { model: "Qwen/Qwen3.5-9B", family: "qwen3_5" },
    { model: "Qwen/Qwen3.5-27B", family: "qwen3_5" },
    { model: "Qwen/Qwen3.5-2B", family: "qwen3_5" },
    { model: "Qwen/Qwen2.5-VL-7B-Instruct", family: "qwen2_5_vl" },
    { model: "Qwen/Qwen2.5-VL-3B-Instruct", family: "qwen2_5_vl" },
    { model: "microsoft/Fara-7B", family: "fara" },
    { model: "ByteDance-Seed/UI-TARS-1.5-7B", family: "ui_tars_15_v1" },
    { model: "ByteDance-Seed/UI-TARS-7B-DPO", family: "ui_tars" },
    { model: "OpenGVLab/ScaleCUA-7B", family: "scalecua" },
    { model: "xlangai/OpenCUA-7B", family: "opencua" },
    { model: "meituan/EvoCUA-8B-20260105", family: "evocua" },
    { model: "Tongyi-MAI/MAI-UI-8B", family: "mai_ui" },
    { model: "Tongyi-MAI/MAI-UI-2B", family: "mai_ui" },
    { model: "MarsXL/UI-Voyager", family: "ui_voyager" },
    { model: "stepfun-ai/GELab-Zero-4B-preview", family: "step_gui" },
  ];
  // which platforms each family actually supports (from scripts/configs/<family>/default/*.yaml).
  // A mobile-only model can't be paired with a desktop env — the env menu filters to these.
  const ALL_PLATS = ["desktop", "web", "mobile", "grounding"];
  const FAMILY_PLATS = {
    gpt: ALL_PLATS, claude: ALL_PLATS, qwen3_vl: ALL_PLATS, qwen3_5: ALL_PLATS,
    qwen2_5_vl: ["desktop", "grounding"],
    fara: ["web", "grounding"],
    ui_tars: ["desktop", "mobile", "grounding"], ui_tars_15_v1: ["desktop", "mobile", "grounding"],
    scalecua: ["desktop", "grounding"], opencua: ["desktop", "grounding"], evocua: ["desktop", "grounding"],
    mai_ui: ["mobile", "grounding"],
    ui_voyager: ["mobile"], step_gui: ["mobile"],
  };
  // each env's platform (grounding benchmarks are cross-platform grounding tasks)
  const ENV_PLAT = {
    "osworld": "desktop", "lite.osworld": "desktop", "osworld_2": "desktop", "cua.bench": "desktop",
    "cuagym": "desktop", "cuaworld": "desktop",
    "screenspot_pro": "grounding", "osworld_g": "grounding",
    "webgym": "web", "webharbor.webvoyager": "web", "online_mind2web": "web",
    "browsergym.miniwob": "web", "browsergym.webarena": "web", "browsergym.visualwebarena": "web",
    "androidworld": "mobile", "androidlab": "mobile", "mobileworld": "mobile", "mobilegym": "mobile",
  };
  const envsFor = (agent, envs) => envs.filter((e) => FAMILY_PLATS[agent.family].includes(ENV_PLAT[e]));
  const CB_OPTS = {
    eval: {
      agents: AGENTS,
      envs: ["osworld", "lite.osworld", "osworld_2", "cua.bench", "screenspot_pro", "osworld_g",
             "webgym", "webharbor.webvoyager", "online_mind2web", "browsergym.miniwob",
             "browsergym.webarena", "browsergym.visualwebarena",
             "androidworld", "androidlab", "mobileworld", "mobilegym"],
      table: true,
    },
    rl: {
      // only open-weight agents can be fine-tuned / reinforced — API models (gpt, claude) can't
      agents: AGENTS.filter((a) => !a.api),
      envs: ["lite.osworld", "webgym", "cuagym", "cuaworld", "mobilegym"],
      table: false,
    },
  };
  // real env-id -> the proper benchmark name in the coverage table (for the highlight)
  const ENV2ROW = {
    "osworld": "OSWorld", "lite.osworld": "Lite.OSWorld", "osworld_2": "OSWorld-2", "cua.bench": "CUABench",
    "screenspot_pro": "ScreenSpot-Pro", "osworld_g": "OSWorld-G", "webgym": "WebGym",
    "webharbor.webvoyager": "WebVoyager", "online_mind2web": "Online-Mind2Web", "browsergym.miniwob": "MiniWoB",
    "browsergym.webarena": "WebArena", "browsergym.visualwebarena": "VisualWebArena",
    "androidworld": "AndroidWorld", "androidlab": "AndroidLab", "mobileworld": "MobileWorld", "mobilegym": "MobileGym",
  };
  const benchRows = document.querySelectorAll("#benchmarks .row");
  const covTabs = document.querySelectorAll("#benchmarks .cov-tab");
  const covPanels = document.querySelectorAll("#benchmarks .cov-panel");
  const showPlat = (plat) => {
    covTabs.forEach((t) => t.classList.toggle("on", t.dataset.plat === plat));
    covPanels.forEach((p) => p.classList.toggle("on", p.dataset.plat === plat));
  };
  covTabs.forEach((t) => t.addEventListener("click", () => showPlat(t.dataset.plat)));
  const capPlat = (s) => (s ? s.charAt(0).toUpperCase() + s.slice(1) : "");
  const highlightBench = (env) => {
    const nm = ENV2ROW[env] || env;
    const plat = capPlat(ENV_PLAT[env]);
    if (plat) showPlat(plat);   // jump the coverage to the env's platform tab
    benchRows.forEach((r) => { const n = r.querySelector(".r-name"); r.classList.toggle("hl", !!n && n.textContent.trim() === nm); });
  };

  document.querySelectorAll(".cmdbuild").forEach((cb) => {
    const cfg = CB_OPTS[cb.dataset.cmd];
    if (!cfg) return;
    const agentSlot = cb.querySelector('.cb-slot[data-slot="agent"]');
    const envSlot = cb.querySelector('.cb-slot[data-slot="env"]');
    if (!agentSlot || !envSlot) return;
    const drvFamily = cb.querySelectorAll('.cb-drv[data-drv="family"]');
    const drvEnv = cb.querySelectorAll('.cb-drv[data-drv="env"]');
    let agent = cfg.agents[0];
    const allowedEnvs = () => envsFor(agent, cfg.envs);
    let env = allowedEnvs()[0];
    const closeAll = (except) => cb.querySelectorAll(".cb-slot.open").forEach((s) => { if (s !== except) s.classList.remove("open"); });
    const swap = (slot) => { slot.classList.remove("swap"); void slot.offsetWidth; slot.classList.add("swap"); };
    const dimUnsupported = () => {
      const allowed = new Set(allowedEnvs());
      benchRows.forEach((r) => {
        const nm = r.querySelector(".r-name").textContent.trim();
        const envId = Object.keys(ENV2ROW).find((k) => ENV2ROW[k] === nm);
        r.classList.toggle("off", !allowed.has(envId));   // agent can't run this benchmark
      });
    };
    const sync = () => { drvFamily.forEach((e) => (e.textContent = agent.family)); drvEnv.forEach((e) => (e.textContent = env)); if (cfg.table) { highlightBench(env); dimUnsupported(); } };

    const PLAT_ORDER = { Grounding: 0, Desktop: 1, Web: 2, Mobile: 3 };
    function makeSlot(slot, getList, getLabel, curLabel, onPick, groupBy) {
      const tok = document.createElement("button");
      tok.className = "cb-tok"; tok.type = "button"; tok.setAttribute("aria-haspopup", "listbox"); tok.setAttribute("aria-expanded", "false");
      tok.innerHTML = '<span class="cb-txt"></span><span class="cb-tcaret" aria-hidden="true"></span>';
      const menu = document.createElement("span");
      menu.className = "cb-menu" + (groupBy ? " cb-menu-grp" : ""); menu.setAttribute("role", "listbox");
      function render() {
        tok.querySelector(".cb-txt").textContent = curLabel();
        menu.innerHTML = "";
        let list = getList();
        if (groupBy) list = [...list].sort((a, b) => (PLAT_ORDER[groupBy(a)] ?? 9) - (PLAT_ORDER[groupBy(b)] ?? 9));
        let lastGrp = null;
        list.forEach((v) => {
          if (groupBy) { const g = groupBy(v); if (g !== lastGrp) { const hd = document.createElement("span"); hd.className = "cb-grp"; hd.textContent = g; menu.appendChild(hd); lastGrp = g; } }
          const label = getLabel(v);
          const o = document.createElement("button");
          o.className = "cb-opt" + (label === curLabel() ? " active" : ""); o.type = "button"; o.textContent = label; o.setAttribute("role", "option");
          o.addEventListener("click", (e) => { e.stopPropagation(); slot.classList.remove("open"); tok.setAttribute("aria-expanded", "false"); if (label !== curLabel()) onPick(v); });
          menu.appendChild(o);
        });
      }
      tok.addEventListener("click", (e) => { e.stopPropagation(); const willOpen = !slot.classList.contains("open"); closeAll(slot); slot.classList.toggle("open", willOpen); tok.setAttribute("aria-expanded", String(willOpen)); });
      slot.appendChild(tok); slot.appendChild(menu);
      slot._render = render; render();
    }

    makeSlot(agentSlot, () => cfg.agents, (a) => a.model, () => agent.model, (a) => {
      agent = a;
      // the new agent may not support the current env — fall back to its first supported one
      if (!allowedEnvs().includes(env)) { env = allowedEnvs()[0]; swap(envSlot); }
      swap(agentSlot); agentSlot._render(); envSlot._render(); sync();
    });
    makeSlot(envSlot, allowedEnvs, (e) => e, () => env, (e) => {
      env = e; swap(envSlot); envSlot._render(); sync();
    }, (e) => capPlat(ENV_PLAT[e]));   // env menu grouped by platform, like the data viewer's dropdown
    sync();
    document.addEventListener("click", (e) => { if (!cb.contains(e.target)) closeAll(); });
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") document.querySelectorAll(".cb-slot.open").forEach((s) => s.classList.remove("open")); });

  /* ---------- scroll reveal ---------- */
  // give the centered sections' headers the same fade-up as their blocks, so each
  // section arrives composed (eyebrow -> headline -> lead) rather than popping in.
  // marked BEFORE js-reveal is set, so they start hidden with no flash.
  document.querySelectorAll(".section.centered").forEach((sec) => {
    const head = sec.querySelectorAll(".eyebrow, h2, .section-lead");
    head.forEach((el, i) => { el.classList.add("reveal"); el.style.setProperty("--rev-delay", (i * 0.09) + "s"); });
  });
  const reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window && !reduce) {
    document.documentElement.classList.add("js-reveal");
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px 8% 0px", threshold: 0.01 });
    reveals.forEach((el) => io.observe(el));
  }

  /* ---------- real-time clocks ---------- */
  const clocks = document.querySelectorAll("[data-clock]");
  if (clocks.length) {
    const tick = () => { const d = new Date(); const s = ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2); clocks.forEach((c) => c.textContent = s); };
    tick(); setInterval(tick, 20000);
  }

  /* ---------- copy the quickstart ---------- */
  const copyBtn = document.getElementById("term-copy");
  const codeEl = document.querySelector(".start-term .term-body");
  if (copyBtn && codeEl && navigator.clipboard) {
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(codeEl.innerText.trim()).then(() => {
        copyBtn.textContent = "copied ✓"; copyBtn.classList.add("done");
        setTimeout(() => { copyBtn.textContent = "copy"; copyBtn.classList.remove("done"); }, 1600);
      }).catch(() => {});
    });
  }
})();

/* ---------- hero stat popovers — rich, categorized, every item links out ---------- */
(function () {
  const RM = "https://github.com/cua-lite/cua-lite/blob/main/lite/gym/envs/";
  const DS = "https://huggingface.co/datasets/cua-lite/";
  const POP = {
    agents: { cap: "Proprietary &amp; open — drop in any of these", groups: [
      { label: "Proprietary", items: [
        ["GPT-5.5", "https://platform.openai.com/docs/guides/tools-computer-use"],
        ["Claude", "https://docs.anthropic.com/en/docs/agents-and-tools/computer-use"] ] },
      { label: "Open-weight", items: [
        ["Qwen3-VL", "https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct"],
        ["Qwen3.5", "https://huggingface.co/Qwen/Qwen3.5-4B"],
        ["Qwen2.5-VL", "https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct"],
        ["UI-TARS", "https://huggingface.co/ByteDance-Seed/UI-TARS-7B-DPO"],
        ["UI-TARS-1.5", "https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B"],
        ["Fara", "https://huggingface.co/microsoft/Fara-7B"],
        ["OpenCUA", "https://huggingface.co/xlangai/OpenCUA-7B"],
        ["ScaleCUA", "https://huggingface.co/OpenGVLab/ScaleCUA-7B"],
        ["EvoCUA", "https://huggingface.co/meituan/EvoCUA-8B-20260105"],
        ["MAI-UI", "https://huggingface.co/Tongyi-MAI/MAI-UI-8B"],
        ["UI-Voyager", "https://huggingface.co/MarsXL/UI-Voyager"],
        ["GELab", "https://huggingface.co/stepfun-ai/GELab-Zero-4B-preview"] ] } ] },
    platforms: { cap: "One action + observation space across all three", groups: [
      { label: "", items: [["Desktop", "#benchmarks"], ["Web", "#benchmarks"], ["Mobile", "#benchmarks"]] } ] },
    benchmarks: { cap: "One command evaluates any agent on any of these", groups: [
      { label: "Grounding", items: [["OSWorld-G", RM+"osworld_g/README.md"], ["ScreenSpot-Pro", RM+"screenspot_pro/README.md"]] },
      { label: "Desktop", items: [["OSWorld", RM+"osworld/README.md"], ["Lite.OSWorld", RM+"lite/osworld/README.md"], ["OSWorld-2", RM+"osworld_2/README.md"], ["CUABench", RM+"cua/README.md"]] },
      { label: "Web", items: [["WebGym", RM+"webgym/README.md"], ["WebVoyager", RM+"webharbor/webvoyager/README.md"], ["Online-Mind2Web", RM+"online_mind2web/README.md"], ["MiniWoB", RM+"browsergym/README.md"], ["WebArena", RM+"browsergym/README.md"], ["VisualWebArena", RM+"browsergym/README.md"]] },
      { label: "Mobile", items: [["AndroidWorld", RM+"androidworld/README.md"], ["AndroidLab", RM+"androidlab/README.md"], ["MobileWorld", RM+"mobileworld/README.md"], ["MobileGym", RM+"mobilegym/README.md"]] } ] },
    corpora: { cap: "10+ existing CUA datasets, preprocessed at scale — understanding · grounding · use", groups: [
      { label: "One schema, on the Hub", items: [
        ["Aguvis", DS+"Aguvis"], ["CAGUI", DS+"CAGUI"], ["GUI-360", DS+"GUI-360"], ["GUIAct", DS+"GUIAct"],
        ["GUIOdyssey", DS+"GUIOdyssey"], ["Multimodal-Mind2Web", DS+"Multimodal-Mind2Web"],
        ["OpenCUA", DS+"OpenCUA"], ["ScaleCUA", DS+"ScaleCUA"], ["UI-Genie-Agent", DS+"UI-Genie-Agent"] ] } ] },
  };
  document.querySelectorAll(".stat-pop[data-pop]").forEach((pop) => {
    const d = POP[pop.dataset.pop]; if (!d) return;
    let h = `<b>${d.cap}</b>`;
    d.groups.forEach((g) => {
      h += '<span class="pop-grp">';
      if (g.label) h += `<span class="pop-cat">${g.label}</span>`;
      h += '<span class="pop-list">';
      g.items.forEach(([name, href]) => {
        const ext = !href.startsWith("#");
        const attr = ext ? ' target="_blank" rel="noopener"' : "";
        h += `<a class="pop-item" href="${href}"${attr}>${name}${ext ? '<span class="pop-x">↗</span>' : ""}</a>`;
      });
      h += "</span></span>";
    });
    pop.innerHTML = h;
  });
  // hover-persist: open on enter, stay while over the stat OR the panel, close on leave (delayed to bridge the gap)
  document.querySelectorAll(".stat").forEach((stat) => {
    const pop = stat.querySelector(".stat-pop"); let t;
    const open = () => { clearTimeout(t); document.querySelectorAll(".stat.pop-open").forEach((s) => { if (s !== stat) s.classList.remove("pop-open"); }); stat.classList.add("pop-open"); };
    const close = () => { t = setTimeout(() => stat.classList.remove("pop-open"), 240); };
    stat.addEventListener("pointerenter", open);
    stat.addEventListener("pointerleave", close);
    if (pop) { pop.addEventListener("pointerenter", () => clearTimeout(t)); pop.addEventListener("pointerleave", close); }
  });
})();
