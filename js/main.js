/* ============================================================
   CUA-Lite — the paper-airplane agent operates a pixel computer.
   Set-of-Marks annotations are MEASURED from the real element
   geometry (no hand-tuned coordinates): every .somel gets an
   outline box + a number label flush on its top-left corner,
   and the airplane flies to the element's true center.
   ============================================================ */
(function () {
  "use strict";

  const ENV = {
    web: {
      bench: "webarena",
      steps: [
        { op: "observe", arg: "screenshot 1280×720" },
        { op: "think", arg: '"find the search box"' },
        { op: "click", tag: 2, arg: "search" },
        { op: "type", arg: '"wireless earbuds"' },
        { op: "click", tag: 3, arg: "submit" },
        { op: "click", tag: 4, arg: "add to cart" },
        { op: "done", arg: "reward 1.0", ok: true },
      ],
    },
    desktop: {
      bench: "lite.osworld",
      steps: [
        { op: "observe", arg: "screenshot 1920×1080" },
        { op: "think", arg: '"total column B"' },
        { op: "click", tag: 2, arg: "cell B12" },
        { op: "type", arg: '"=SUM(B1:B11)"' },
        { op: "key", arg: "Enter" },
        { op: "done", arg: "reward 1.0", ok: true },
      ],
    },
    mobile: {
      bench: "mobilegym",
      steps: [
        { op: "observe", arg: "screenshot 1080×2400" },
        { op: "click", tag: 1, arg: "new contact" },
        { op: "type", arg: '"Ada Lovelace"' },
        { op: "click", tag: 3, arg: "save" },
        { op: "done", arg: "reward 1.0", ok: true },
      ],
    },
  };

  const state = { agent: "gpt-5.5", env: "web" };
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const screen = document.getElementById("screen");
  const cursor = document.getElementById("cursor");
  const box = document.getElementById("target");
  const ring = document.getElementById("clickring");
  const trace = document.getElementById("trace");
  const traceTitle = document.getElementById("trace-title");
  const somLayer = document.getElementById("som-layer");
  const mocks = [...document.querySelectorAll(".mock")];

  let rects = {}; // tag -> {x,y,w,h,cx,cy} in px within screen
  let timers = [];
  const clear = () => { timers.forEach(clearTimeout); timers = []; };
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));

  function activeMock() { return mocks.find((m) => m.dataset.env === state.env); }

  /* Measure the active mock's elements; anchor labels to true corners. */
  function annotate() {
    somLayer.innerHTML = "";
    rects = {};
    const sr = screen.getBoundingClientRect();
    activeMock().querySelectorAll(".somel").forEach((el) => {
      const r = el.getBoundingClientRect();
      const x = r.left - sr.left, y = r.top - sr.top;
      const rec = { x, y, w: r.width, h: r.height, cx: x + r.width / 2, cy: y + r.height / 2 };
      rects[el.dataset.tag] = rec;
      const lab = document.createElement("span");
      lab.className = "som";
      lab.textContent = el.dataset.tag;
      lab.style.left = rec.x + "px";
      lab.style.top = rec.y + "px";
      somLayer.appendChild(lab);
    });
  }

  let last = null;
  function spawnTrail(x0, y0, x1, y1) {
    const N = 6;
    for (let i = 1; i < N; i++) {
      const t = i / N;
      const d = document.createElement("div");
      d.className = "trail-dot";
      d.style.left = x0 + (x1 - x0) * t + "px";
      d.style.top = y0 + (y1 - y0) * t + "px";
      d.style.animationDelay = t * 0.18 + "s";
      screen.appendChild(d);
      d.addEventListener("animationend", () => d.remove());
    }
  }

  function moveTo(tag) {
    const r = rects[tag];
    if (!r) return;
    if (last) spawnTrail(last[0], last[1], r.cx, r.cy);
    last = [r.cx, r.cy];
    cursor.style.left = r.cx + "px";
    cursor.style.top = r.cy + "px";
    box.style.left = r.cx + "px";
    box.style.top = r.cy + "px";
    box.style.width = r.w + 10 + "px";
    box.style.height = r.h + 10 + "px";
    box.style.opacity = "1";
  }

  function clickFx(tag) {
    const r = rects[tag];
    if (!r) return;
    ring.style.left = r.cx + "px";
    ring.style.top = r.cy + "px";
    ring.classList.remove("fire");
    void ring.offsetWidth;
    ring.classList.add("fire");
  }

  function addLine(step, i) {
    const el = document.createElement("div");
    el.className = "trace-line";
    const idx = String(i + 1).padStart(3, "0");
    const arg = step.tag ? `<span class="tag">[${step.tag}]</span> ${step.arg}` : step.arg;
    el.innerHTML = `<span class="idx">${idx}</span><span class="op"${step.ok ? ' style="color:#86e0a0"' : ""}>${step.op}</span><span class="arg">${arg}</span>`;
    trace.appendChild(el);
    requestAnimationFrame(() => el.classList.add("on"));
  }

  function play() {
    clear();
    [...trace.querySelectorAll(".trace-line")].forEach((n) => n.remove());
    box.style.opacity = "0";
    last = null;

    mocks.forEach((m) => m.classList.toggle("hidden", m.dataset.env !== state.env));
    annotate();

    const env = ENV[state.env];
    traceTitle.textContent = `rollout · ${state.agent} · ${env.bench}`;

    // park the plane mid-screen before the first move
    const sr = screen.getBoundingClientRect();
    cursor.style.left = sr.width * 0.5 + "px";
    cursor.style.top = sr.height * 0.42 + "px";

    if (reduce) { env.steps.forEach(addLine); return; }

    let t = 500;
    env.steps.forEach((step, i) => {
      at(t, () => {
        if (step.tag) moveTo(step.tag);
        at(step.tag ? 500 : 0, () => {
          if (step.tag) clickFx(step.tag);
          addLine(step, i);
        });
      });
      t += step.tag ? 1200 : 800;
    });
    at(t + 1600, play);
  }

  document.querySelectorAll("#agent-seg button").forEach((b) =>
    b.addEventListener("click", () => {
      document.querySelectorAll("#agent-seg button").forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
      state.agent = b.dataset.agent;
      play();
    })
  );
  document.querySelectorAll("#env-seg button").forEach((b) =>
    b.addEventListener("click", () => {
      document.querySelectorAll("#env-seg button").forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
      state.env = b.dataset.env;
      play();
    })
  );

  addEventListener("resize", annotate);

  // pixel click sparkle — the teaser motif, site-wide
  const layer = document.getElementById("sparkle-layer");
  addEventListener("pointerdown", (e) => {
    const s = document.createElement("div");
    s.className = "sparkle";
    s.style.left = e.clientX + "px";
    s.style.top = e.clientY + "px";
    layer.appendChild(s);
    s.addEventListener("animationend", () => s.remove());
  });

  play();
})();
