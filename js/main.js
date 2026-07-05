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
    const dur = Math.min(0.82, Math.max(0.42, d / 540));
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
      if (i++ <= text.length) at(40 + Math.random() * 30, tick);
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
  // web
  const wq = $("#wq"), wfield = $(".dev-web [data-t='search']"), wgrid = $("#wgrid");
  const wadd = $(".dev-web [data-t='add']"), cart = $("#cart");
  // mobile
  const mname = $("#mname"), minput = $(".dev-mobile [data-t='name']"), msave = $(".dev-mobile [data-t='save']");

  /* ---------- the three platforms ---------- */
  const MODES = {
    desktop: {
      env: "osworld",
      device: $(".dev-desktop"),
      reset() {
        fbar.innerHTML = '<span class="mk-ph"></span>'; fbar.className = "sh-formula";
        total.textContent = ""; total.classList.remove("filled", "sel");
      },
      steps: [
        { t: "cell", cap: "select cell B5", onAct: () => total.classList.add("sel") },
        { t: "cell", cap: "type =SUM(B2:B4)", typeLen: 11, onAct: () => typeInto(fbar, "sh-formula", "=SUM(B2:B4)") },
        { t: "cell", cap: "press Enter", onAct: () => at(120, () => { total.textContent = fmt(sum()); total.classList.add("filled"); }) },
        { done: true, cap: () => `Total = ${fmt(sum())}` },
      ],
      finished() { fbar.className = "sh-formula typed"; fbar.textContent = "=SUM(B2:B4)"; total.textContent = fmt(sum()); total.classList.add("filled", "sel"); },
    },
    web: {
      env: "webarena",
      device: $(".dev-web"),
      reset() {
        wq.textContent = "search products…"; wq.className = "mk-ph";
        wfield.classList.remove("hot"); wgrid.classList.remove("pending");
        wadd.textContent = "Add"; wadd.classList.remove("added"); cart.textContent = "0";
      },
      steps: [
        { t: "search", cap: "click the search box", onAct: () => wfield.classList.add("hot") },
        { t: "search", cap: 'type "wireless earbuds"', typeLen: 16, onAct: () => typeInto(wq, "", "wireless earbuds") },
        { t: "go", cap: "click Search", onAct: () => { wgrid.classList.add("pending"); at(150, () => wgrid.classList.remove("pending")); } },
        { t: "add", cap: "add to cart", onAct: () => at(140, () => { wadd.textContent = "✓ Added"; wadd.classList.add("added"); cart.textContent = "1"; }) },
        { done: true, cap: "added to cart" },
      ],
      finished() { wq.textContent = "wireless earbuds"; wq.className = "typed"; wfield.classList.add("hot"); wgrid.classList.remove("pending"); wadd.textContent = "✓ Added"; wadd.classList.add("added"); cart.textContent = "1"; },
    },
    mobile: {
      env: "androidworld",
      device: $(".dev-mobile"),
      reset() { mname.textContent = "Full name"; mname.className = "mk-ph"; minput.classList.remove("hot"); msave.textContent = "Save"; msave.classList.remove("saved"); },
      steps: [
        { t: "name", cap: "tap the name field", onAct: () => minput.classList.add("hot") },
        { t: "name", cap: 'type "Ada Lovelace"', typeLen: 12, onAct: () => typeInto(mname, "", "Ada Lovelace") },
        { t: "save", cap: "tap Save", onAct: () => at(150, () => { msave.textContent = "✓ Saved"; msave.classList.add("saved"); }) },
        { done: true, cap: "contact saved" },
      ],
      finished() { mname.textContent = "Ada Lovelace"; mname.className = "typed"; minput.classList.add("hot"); msave.textContent = "✓ Saved"; msave.classList.add("saved"); },
    },
  };
  const ORDER = ["desktop", "web", "mobile"];

  /* ---------- run one platform's task ---------- */
  const ts = (ms) => (ms / 1000).toFixed(1) + "s";
  function runSeq(ctx, steps, onFinish) {
    clearAll(); logClear();
    let t = 360;
    { const tt = t; at(tt, () => logLine("thinking", "think live", ts(tt))); }   // plan once, then act
    t += 780;
    steps.forEach((s) => {
      const tt = t;
      if (s.done) { at(tt, () => logLine(typeof s.cap === "function" ? s.cap() : s.cap, "done", ts(tt))); t += 620; return; }
      at(tt, () => { moveTo(ctx, s.t); logLine(s.cap, "live", ts(tt)); });
      at(tt + 520, () => { click(ctx, s.t); s.onAct && s.onAct(); });
      t += 520 + (s.typeLen ? s.typeLen * 42 + 240 : 210) + 230;
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
  function activate(m) {
    mode = m; ctx = ctxFor(MODES[m].device);
    document.querySelectorAll(".stage .device").forEach((d) => d.classList.toggle("active", d.dataset.mode === m));
    syncPlats();
    capRun.innerHTML = `<span class="c-p">$</span> rollout.py <span class="c-flag">--model-id</span> <span class="c-val">gpt-5.5</span> <span class="c-flag">--env-id</span> <span class="c-env">${MODES[m].env}</span>`;
    MODES[m].reset(); logClear();
  }
  // the intro tours all three machines ONCE (desktop → web → mobile → home),
  // then rests on the desktop. Calm and confident, not a restless loop —
  // the lead words are there to drive it again whenever you want.
  let advances = 0;
  const touring = () => advances < ORDER.length;
  function advance() { advances++; const i = ORDER.indexOf(mode); switchTo(ORDER[(i + 1) % ORDER.length]); }
  const held = () => paused || !visible;   // don't advance while hovered or off-screen
  function holdThenAdvance() { at(held() ? 500 : 1200, () => { if (held()) holdThenAdvance(); else advance(); }); }

  function runActive() {
    running = true;
    MODES[mode].reset();
    runSeq(ctx, MODES[mode].steps, () => {
      running = false;
      if (touring()) holdThenAdvance();   // still touring → turn to the next machine; else rest
    });
  }
  function switchTo(m) {
    clearAll(); running = false;
    activate(m); parkCursor();
    at(420, runActive);
  }

  /* ---------- editable desktop cells: edit the numbers, the agent sums YOURS ---------- */
  const editing = () => document.activeElement && document.activeElement.classList && document.activeElement.classList.contains("editable");
  cells.forEach((el) => {
    el.addEventListener("focus", () => { paused = true; });   // don't cycle away mid-edit
    el.addEventListener("input", () => { if (mode === "desktop" && !running) { total.textContent = ""; total.classList.remove("filled", "sel"); fbar.innerHTML = '<span class="mk-ph"></span>'; fbar.className = "sh-formula"; } });
    el.addEventListener("blur", () => { el.textContent = fmt(numOf(el)); at(700, () => { if (!editing()) paused = false; }); });
    el.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); el.blur(); paused = false; switchTo("desktop"); } });
  });

  /* ---------- the lead words steer the demo ---------- */
  plats.forEach((p) => {
    const m = p.dataset.mode;
    p.addEventListener("pointerenter", () => { paused = true; if (started && m !== mode) switchTo(m); });
    p.addEventListener("pointerleave", () => { paused = false; });
    p.addEventListener("click", () => { paused = false; if (m !== mode) switchTo(m); });
    p.setAttribute("tabindex", "0");
    p.addEventListener("focus", () => { if (started && m !== mode) switchTo(m); });
  });

  if (reduce) {
    ORDER.forEach((m) => MODES[m].reset());
    activate("desktop"); MODES.desktop.finished();
    logClear();
    logLine("thinking", "think", "0.4s");
    [["select cell B5", "1.1s"], ["type =SUM(B2:B4)", "2.1s"], ["press Enter", "3.6s"]].forEach(([l, tt]) => logLine(l, "past", tt));
    logLine("Total = 2,402", "done", "4.2s");
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

  /* ---------- the active device tilts toward your real cursor ---------- */
  const heroRight = document.querySelector(".hero-right");
  if (!reduce && heroRight && matchMedia("(pointer: fine)").matches) {
    heroRight.addEventListener("pointermove", (e) => {
      const r = heroRight.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
      stage.style.setProperty("--ty", (px * 5).toFixed(2) + "deg");
      stage.style.setProperty("--tx", (-py * 4).toFixed(2) + "deg");
    });
    heroRight.addEventListener("pointerleave", () => { stage.style.setProperty("--ty", "0deg"); stage.style.setProperty("--tx", "0deg"); });
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
