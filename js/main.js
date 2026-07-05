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
  let hintDone = false;   // once you've edited a cost, stop inviting
  const showHint = () => { if (!hintDone && mode === "desktop") demoHint.classList.add("show"); };
  const hideHint = () => demoHint.classList.remove("show");

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
      device: $(".dev-desktop"),
      reset() {
        fbar.innerHTML = '<span class="mk-ph"></span>'; fbar.className = "sh-formula";
        total.textContent = ""; total.classList.remove("filled", "sel");
      },
      steps: [
        { t: "cell", cap: "select cell B5", onAct: () => total.classList.add("sel") },
        { t: "cell", cap: "type =AVERAGE(B2:B4)", typeLen: 15, onAct: () => typeInto(fbar, "sh-formula", "=AVERAGE(B2:B4)") },
        { t: "cell", cap: "press Enter", onAct: () => at(120, () => { total.textContent = avg().toFixed(1); total.classList.add("filled"); }) },
        { done: true, cap: () => `Average = ${avg().toFixed(1)}` },
      ],
      finished() { fbar.className = "sh-formula typed"; fbar.textContent = "=AVERAGE(B2:B4)"; total.textContent = avg().toFixed(1); total.classList.add("filled", "sel"); },
    },
    web: {
      // Google → search "cua-lite" → open this very homepage
      env: "webvoyager",
      device: $(".dev-web"),
      reset() {
        wq.textContent = "Search Google or type a URL"; wq.className = "mk-ph";
        wfield.classList.remove("hot");
        ggHome.style.display = ""; ggResults.classList.remove("show"); ggSite.classList.remove("show");
        bwHost.textContent = "google.com";
      },
      steps: [
        { t: "search", cap: "click the search bar", onAct: () => wfield.classList.add("hot") },
        { t: "search", cap: 'type "cua-lite"', typeLen: 8, onAct: () => typeInto(wq, "", "cua-lite") },
        { t: "go", cap: "press Search", onAct: () => { ggHome.style.display = "none"; ggResults.classList.add("show"); bwHost.textContent = "google.com/search?q=cua-lite"; } },
        { t: "open", cap: "open cua-lite.github.io", onAct: () => { ggResults.classList.remove("show"); ggSite.classList.add("show"); bwHost.textContent = "cua-lite.github.io"; } },
        { done: true, cap: "cua-lite.github.io" },
      ],
      finished() { wq.textContent = "cua-lite"; wq.className = "typed"; ggHome.style.display = "none"; ggResults.classList.remove("show"); ggSite.classList.add("show"); bwHost.textContent = "cua-lite.github.io"; },
    },
    mobile: {
      // texting ZHZisZZ about why CUA-Lite is good
      env: "androidworld",
      device: $(".dev-mobile"),
      reset() {
        mname.textContent = "iMessage"; mname.className = "mk-ph"; minput.classList.remove("hot");
        msent.classList.remove("show"); msave.classList.remove("sent");
      },
      steps: [
        { t: "name", cap: "tap the message field", onAct: () => minput.classList.add("hot") },
        { t: "name", cap: 'type "any agent, any computer"', typeLen: 24, onAct: () => typeInto(mname, "", "any agent, any computer 🚀") },
        { t: "save", cap: "tap Send", onAct: () => at(120, () => { msent.classList.add("show"); msave.classList.add("sent"); mname.textContent = "iMessage"; mname.className = "mk-ph"; minput.classList.remove("hot"); }) },
        { done: true, cap: "message sent" },
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
      at(tt + 380, () => { click(ctx, s.t); s.onAct && s.onAct(); });
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
    capRun.innerHTML = `<span class="c-p">$</span> rollout.py <span class="c-flag">--model-id</span> <span class="c-val">gpt-5.5</span> <span class="c-flag">--env-id</span> <span class="c-env">${MODES[m].env}</span>`;
    if (!skipReset) { MODES[m].reset(); logClear(); }
  }
  // the desktop task, shown already-complete (no re-run): the rest/home state
  function showDesktopDone() {
    MODES.desktop.finished();
    logClear();
    logLine("thinking", "think", "0.2s");
    [["select cell B5", "0.6s"], ["type =AVERAGE(B2:B4)", "1.1s"], ["press Enter", "1.6s"]].forEach(([l, tt]) => logLine(l, "past", tt));
    logLine(`Average = ${avg().toFixed(1)}`, "done", "2.0s");
    requestAnimationFrame(() => { ctx.cursor.style.transition = "none"; const c = centerOf(ctx, "cell"); if (c) place(ctx, c.x, c.y); });
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
        else settleHome();                                    // shown all three → settle home
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
  // you changed a cost → the agent re-runs on YOUR number. A short focused
  // response (~1s), not the whole select/type/enter ceremony — crisp feedback.
  function recompute() {
    clearAll(); running = true;
    logClear();
    fbar.className = "sh-formula typed"; fbar.textContent = "=AVERAGE(B2:B4)";
    total.textContent = ""; total.classList.remove("filled"); total.classList.add("sel");
    at(60, () => logLine("read cells B2:B4", "live", "0.1s"));
    at(360, () => { moveTo(ctx, "cell"); logLine("recompute =AVERAGE(B2:B4)", "live", "0.4s"); });
    at(820, () => { click(ctx, "cell"); total.textContent = avg().toFixed(1); total.classList.add("filled"); });
    at(1080, () => logLine(`Average = ${avg().toFixed(1)}`, "done", "0.9s"));
    at(1240, () => { running = false; });
  }

  /* ---------- editable desktop cells: edit the numbers, the agent sums YOURS ---------- */
  const editing = () => document.activeElement && document.activeElement.classList && document.activeElement.classList.contains("editable");
  let sheetDirty = false;   // did you actually change a cost? only then does the agent re-run
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
        if (visible && !started) { started = true; runActive(); }
      }); }, { threshold: 0.25 });
      io.observe(stage);
    } else { visible = true; started = true; runActive(); }
  }

  // hover the device to hold the current platform (read it, edit it); leaving resumes the cycle
  if (!reduce) {
    stage.addEventListener("pointerenter", () => { if (started) paused = true; });
    stage.addEventListener("pointerleave", () => { if (!editing()) paused = false; });
  }

  /* ---------- scroll reveal ---------- */
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
      navigator.clipboard.writeText(codeEl.textContent.trim()).then(() => {
        copyBtn.textContent = "copied ✓"; copyBtn.classList.add("done");
        setTimeout(() => { copyBtn.textContent = "copy"; copyBtn.classList.remove("done"); }, 1600);
      }).catch(() => {});
    });
  }
})();
