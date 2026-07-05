/* ============================================================
   CUA-Lite — one agent, any computer.
   The same agent operates three platforms, each its own device:
   desktop (a pixel CRT running LibreOffice Calc), web (a browser),
   mobile (a phone). A segmented toggle switches the focal device;
   on load it auto-tours all three, then rests and lets you drive.
   Shared engine: think → move → act, GPU-composited cursor.
   Reduced motion: the desktop finished frame, held still.
   ============================================================ */
(function () {
  "use strict";
  const stage = document.getElementById("stage");
  if (!stage) return;

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const capAct = document.getElementById("cap-act");
  const capRun = document.getElementById("cap-run");
  const agentLine = document.querySelector(".agent-line");
  const runBtn = document.getElementById("run-btn");
  const toggle = document.getElementById("mode-toggle");
  const ind = document.getElementById("mode-ind");

  let timers = [];
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  const clearAll = () => { timers.forEach(clearTimeout); timers = []; };
  const setCap = (html) => { capAct.innerHTML = html; };
  const THINK = '<span class="ca-dim">agent</span> <span class="think">thinking<i>.</i><i>.</i><i>.</i></span>';
  const setBtn = (label, dis) => { if (runBtn) { runBtn.innerHTML = label; runBtn.disabled = dis; } };

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
  const mname = $("#mname"), minput = $(".dev-mobile [data-t='name']");

  /* ---------- the three platforms ---------- */
  const MODES = {
    desktop: {
      env: "lite.osworld",
      device: $(".dev-desktop"),
      reset() {
        fbar.innerHTML = '<span class="mk-ph"></span>'; fbar.className = "sh-formula";
        total.textContent = ""; total.classList.remove("filled", "sel");
      },
      steps: [
        { t: "cell", cap: "select cell B5", onAct: () => total.classList.add("sel") },
        { t: "cell", cap: "type =SUM(B2:B4)", typeLen: 11, onAct: () => typeInto(fbar, "sh-formula", "=SUM(B2:B4)") },
        { t: "cell", cap: "press Enter", onAct: () => at(120, () => { total.textContent = fmt(sum()); total.classList.add("filled"); }) },
        { done: true, cap: () => `✓ Total = ${fmt(sum())}` },
      ],
      finished() { fbar.className = "sh-formula typed"; fbar.textContent = "=SUM(B2:B4)"; total.textContent = fmt(sum()); total.classList.add("filled", "sel"); },
    },
    web: {
      env: "webarena",
      device: $(".dev-web"),
      reset() {
        wq.textContent = "search products…"; wq.className = "mk-ph";
        wfield.classList.remove("hot"); wgrid.classList.add("pending");
        wadd.textContent = "Add"; wadd.classList.remove("added"); cart.textContent = "0";
      },
      steps: [
        { t: "search", cap: "click the search box", onAct: () => wfield.classList.add("hot") },
        { t: "search", cap: 'type "wireless earbuds"', typeLen: 16, onAct: () => typeInto(wq, "", "wireless earbuds") },
        { t: "go", cap: "click Search", onAct: () => at(220, () => wgrid.classList.remove("pending")) },
        { t: "add", cap: "add to cart", onAct: () => at(140, () => { wadd.textContent = "✓ Added"; wadd.classList.add("added"); cart.textContent = "1"; }) },
        { done: true, cap: "✓ added to cart" },
      ],
      finished() { wq.textContent = "wireless earbuds"; wq.className = "typed"; wfield.classList.add("hot"); wgrid.classList.remove("pending"); wadd.textContent = "✓ Added"; wadd.classList.add("added"); cart.textContent = "1"; },
    },
    mobile: {
      env: "mobilegym",
      device: $(".dev-mobile"),
      reset() { mname.textContent = "Full name"; mname.className = "mk-ph"; minput.classList.remove("hot"); },
      steps: [
        { t: "name", cap: "tap the name field", onAct: () => minput.classList.add("hot") },
        { t: "name", cap: 'type "Ada Lovelace"', typeLen: 12, onAct: () => typeInto(mname, "", "Ada Lovelace") },
        { t: "save", cap: "tap Save" },
        { done: true, cap: "✓ contact saved" },
      ],
      finished() { mname.textContent = "Ada Lovelace"; mname.className = "typed"; minput.classList.add("hot"); },
    },
  };
  const ORDER = ["desktop", "web", "mobile"];

  /* ---------- run one platform's task ---------- */
  function runSeq(ctx, steps, onFinish) {
    clearAll();
    let t = 500;
    steps.forEach((s) => {
      if (s.done) { at(t, () => setCap(`<b>${typeof s.cap === "function" ? s.cap() : s.cap}</b>`)); t += 700; return; }
      at(t, () => setCap(THINK));
      at(t + 480, () => { moveTo(ctx, s.t); setCap(`<span class="ca-dim">agent</span> ${s.cap}`); });
      at(t + 980, () => { click(ctx, s.t); s.onAct && s.onAct(); });
      t += 980 + (s.typeLen ? s.typeLen * 46 + 320 : 260) + 300;
    });
    at(t, onFinish);
  }

  /* ---------- mode manager ---------- */
  let mode = "desktop";
  let ctx = ctxFor(MODES.desktop.device);
  let running = false, touring = false;

  function moveIndicator() {
    const btn = toggle && toggle.querySelector(".mode-btn.active");
    if (!btn || !ind) return;
    ind.style.width = btn.offsetWidth + "px";
    ind.style.transform = `translateX(${btn.offsetLeft}px)`;
  }
  function parkCursor() {
    const s = ctx.screen;
    ctx.cursor.style.transition = "none";
    place(ctx, s.clientWidth * 0.7, s.clientHeight * 0.8);
    requestAnimationFrame(() => { ctx.cursor.style.transition = ""; });
  }
  function activate(m) {
    mode = m; ctx = ctxFor(MODES[m].device);
    document.querySelectorAll(".stage .device").forEach((d) => d.classList.toggle("active", d.dataset.mode === m));
    document.querySelectorAll(".mode-btn").forEach((b) => b.classList.toggle("active", b.dataset.mode === m));
    moveIndicator();
    capRun.textContent = `$ rollout.py --model-id gpt-5.5 --env-id ${MODES[m].env}`;
    MODES[m].reset();
    setCap("");
  }

  function runActive() {
    running = true; setBtn("● Running", true); agentLine.classList.add("busy");
    MODES[mode].reset();
    runSeq(ctx, MODES[mode].steps, () => {
      running = false; agentLine.classList.remove("busy");
      if (touring) {
        const i = ORDER.indexOf(mode);
        if (i < ORDER.length - 1) {
          at(1000, () => { activate(ORDER[i + 1]); parkCursor(); at(520, runActive); });
        } else { touring = false; setBtn("↻&nbsp;Run&nbsp;again", false); }
      } else { setBtn("↻&nbsp;Run&nbsp;again", false); }
    });
  }

  function pickMode(m) {
    if (m === mode && running) return;
    touring = false; clearAll(); running = false;
    activate(m); parkCursor();
    at(360, runActive);
  }

  /* ---------- editable desktop cells ---------- */
  cells.forEach((el) => {
    el.addEventListener("input", () => { if (mode === "desktop" && !running) { total.textContent = ""; total.classList.remove("filled", "sel"); fbar.innerHTML = '<span class="mk-ph"></span>'; fbar.className = "sh-formula"; } });
    el.addEventListener("blur", () => { el.textContent = fmt(numOf(el)); });
    el.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); el.blur(); pickMode("desktop"); } });
  });

  /* ---------- wire it up ---------- */
  if (toggle) toggle.querySelectorAll(".mode-btn").forEach((b) => b.addEventListener("click", () => pickMode(b.dataset.mode)));
  if (runBtn) runBtn.addEventListener("click", () => { if (!running) { touring = false; runActive(); } });

  if (reduce) {
    ORDER.forEach((m) => { MODES[m].reset(); });
    MODES.desktop.finished(); setBtn("↻&nbsp;Run&nbsp;again", false);
    moveIndicator();
  } else {
    activate("desktop"); parkCursor(); moveIndicator();
    // auto-tour once when the stage is first seen
    const start = () => { touring = true; runActive(); };
    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver((es) => { es.forEach((e) => { if (e.isIntersecting) { io.disconnect(); start(); } }); }, { threshold: 0.35 });
      io.observe(stage);
    } else { start(); }
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
  addEventListener("resize", moveIndicator);

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
})();
