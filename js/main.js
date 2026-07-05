/* ============================================================
   CUA-Lite — watch the agent operate a real computer.
   The paper airplane (the agent, straight from the teaser) flies
   to real UI targets, clicks, and types — across a browser, a
   spreadsheet, and a phone. Compose an agent × an environment and
   it runs THAT task, ending in reward 1.0 · LiteSample.
   Reduced motion: the finished state, no flight.
   ============================================================ */
(function () {
  "use strict";

  const screen = document.getElementById("screen");
  if (!screen) return;
  const cursor = document.getElementById("cursor");
  const ripple = document.getElementById("ripple");
  const reward = document.getElementById("reward");
  const title = document.getElementById("screen-title");
  const capRun = document.getElementById("cap-run");
  const capAct = document.getElementById("cap-act");
  const mocks = [...document.querySelectorAll(".mock")];

  const AGENTS = [
    { id: "gpt-5.5", flag: "gpt-5.5" },
    { id: "claude", flag: "claude-opus-4-8" },
    { id: "qwen3-vl", flag: "Qwen/Qwen3-VL-8B" },
    { id: "ui-tars", flag: "ui-tars" },
  ];
  const ENVS = [
    {
      id: "web", env: "webarena",
      steps: [
        { t: "search", cap: "click search" },
        { t: "search", cap: 'type "wireless earbuds"', type: { el: "web-search", text: "wireless earbuds" } },
        { t: "go", cap: "click Search" },
        { t: "add", cap: "click Add to cart" },
      ],
    },
    {
      id: "desktop", env: "lite.osworld",
      steps: [
        { t: "cell", cap: "click cell B12" },
        { t: "fx", cap: "type =SUM(B1:B11)", type: { el: "dt-formula", text: "=SUM(B1:B11)" } },
        { t: "cell", cap: "press Enter", fill: { el: "dt-total", text: "2,402" } },
      ],
    },
    {
      id: "mobile", env: "mobilegym",
      steps: [
        { t: "fab", cap: "tap + new contact" },
        { t: "name", cap: 'type "Ada Lovelace"', type: { el: "mb-name", text: "Ada Lovelace" } },
        { t: "save", cap: "tap Save" },
      ],
    },
  ];
  const PLACEHOLDER = { "web-search": "search products…", "dt-formula": "", "mb-name": "Name", "dt-total": "" };

  const state = { ai: 0, ei: 0 };
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let timers = [];
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  const clearAll = () => { timers.forEach(clearTimeout); timers = []; };

  const activeMock = () => mocks.find((m) => m.dataset.env === ENVS[state.ei].id);
  function setCmd() {
    capRun.textContent = `$ rollout.py --model-id ${AGENTS[state.ai].flag} --env-id ${ENVS[state.ei].env}`;
    if (title) title.textContent = ENVS[state.ei].env;
  }

  function resetMock() {
    mocks.forEach((m) => m.classList.toggle("hidden", m.dataset.env !== ENVS[state.ei].id));
    reward.classList.remove("show");
    capAct.innerHTML = "";
    for (const id in PLACEHOLDER) {
      const el = document.getElementById(id);
      if (!el) continue;
      el.textContent = PLACEHOLDER[id];
      el.className = "mk-ph";
    }
    const cell = document.getElementById("dt-total");
    if (cell) cell.parentElement && cell.classList.remove("filled");
    document.querySelectorAll(".mk-field.hot").forEach((e) => e.classList.remove("hot"));
  }

  function centerOf(t) {
    const el = activeMock().querySelector(`[data-t="${t}"]`);
    if (!el) return null;
    const sr = screen.getBoundingClientRect(), r = el.getBoundingClientRect();
    return { x: r.left - sr.left + r.width / 2, y: r.top - sr.top + r.height / 2, el };
  }
  function moveTo(t) {
    const c = centerOf(t); if (!c) return;
    cursor.style.left = c.x + "px"; cursor.style.top = c.y + "px";
  }
  function fireRipple(t) {
    const c = centerOf(t); if (!c) return;
    ripple.style.left = c.x + "px"; ripple.style.top = c.y + "px";
    ripple.classList.remove("go"); void ripple.offsetWidth; ripple.classList.add("go");
  }
  function typeInto(id, text, cls, done) {
    const el = document.getElementById(id); if (!el) { done && done(); return; }
    el.className = cls || ""; let i = 0;
    (function tick() {
      el.textContent = text.slice(0, i);
      if (i++ <= text.length) at(34 + Math.random() * 26, tick); else done && done();
    })();
  }

  function playEnv() {
    clearAll(); setCmd(); resetMock();
    const ep = ENVS[state.ei];
    if (reduce) {
      // finished state
      ep.steps.forEach((s) => {
        if (s.type) { const el = document.getElementById(s.type.el); el.textContent = s.type.text; el.className = "typed"; }
        if (s.fill) { const el = document.getElementById(s.fill.el); el.textContent = s.fill.text; el.classList.add("filled"); }
      });
      reward.classList.add("show");
      return;
    }
    // park the plane center, then run steps
    cursor.style.left = "50%"; cursor.style.top = "44%";
    let t = 500;
    ep.steps.forEach((s) => {
      at(t, () => { moveTo(s.t); capAct.innerHTML = "agent · " + `<b>${s.cap}</b>`; });
      at(t + 560, () => {
        fireRipple(s.t);
        const c = centerOf(s.t); if (c && s.t === "search") c.el.classList.add("hot");
        if (s.type) typeInto(s.type.el, s.type.text, "typed");
        if (s.fill) { const el = document.getElementById(s.fill.el); el.textContent = s.fill.text; el.classList.add("filled"); }
      });
      const dur = s.type ? 560 + s.type.text.length * 42 + 320 : 900;
      t += dur;
    });
    at(t + 200, () => { capAct.innerHTML = '<b>done · reward 1.0</b>'; reward.classList.add("show"); });
  }

  function syncActive() {
    document.querySelectorAll("#env-row .chip").forEach((c, i) => c.classList.toggle("active", i === state.ei));
    document.querySelectorAll("#agent-row .chip").forEach((c, i) => c.classList.toggle("active", i === state.ai));
  }
  document.querySelectorAll("#agent-row .chip").forEach((c, i) =>
    c.addEventListener("click", () => { state.ai = i; syncActive(); playEnv(); }));
  document.querySelectorAll("#env-row .chip").forEach((c, i) =>
    c.addEventListener("click", () => { state.ei = i; syncActive(); playEnv(); }));

  addEventListener("resize", () => { if (!reduce) { /* re-park on resize */ } });
  playEnv();
})();
