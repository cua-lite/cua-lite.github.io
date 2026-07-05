/* ============================================================
   CUA-Lite — the page is a rollout.
   1) FLIGHT: the paper airplane flies a planned route (dotted)
      through the section waypoints as you scroll, leaving a
      flown trajectory (solid coral) behind it.
   2) MACHINE: the in-screen demo where the agent operates
      web / desktop / mobile with measured Set-of-Marks.
   ============================================================ */
(function () {
  "use strict";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ================= FLIGHT ================= */
  const world = document.getElementById("world");
  const svg = document.getElementById("flight");
  const route = document.getElementById("route");
  const flown = document.getElementById("flown");
  const plane = document.getElementById("plane");
  const wps = [...document.querySelectorAll(".wp")];
  let pathLen = 0, y0 = 0, y1 = 1;

  function buildFlight() {
    if (innerWidth <= 900) return;
    const W = world.clientWidth, H = world.scrollHeight;
    svg.setAttribute("width", W);
    svg.setAttribute("height", H);
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    const wr = world.getBoundingClientRect();
    const pts = wps.map((el) => {
      const r = el.getBoundingClientRect();
      return { x: r.left - wr.left + r.width / 2, y: r.top - wr.top + r.height / 2 };
    });
    // launch from below the hero copy (the "scroll to fly" line), not through it
    const launch = document.querySelector(".scrollhint");
    if (launch) {
      const r = launch.getBoundingClientRect();
      pts[0] = { x: r.left - wr.left + r.width / 2, y: r.bottom - wr.top + 26 };
    }
    // land on the grass at the very bottom of the world
    pts.push({ x: W * 0.5, y: H - 40 });
    let d = `M ${pts[0].x} ${pts[0].y}`;
    for (let i = 1; i < pts.length; i++) {
      const a = pts[i - 1], b = pts[i], my = (a.y + b.y) / 2;
      d += ` C ${a.x} ${my}, ${b.x} ${my}, ${b.x} ${b.y}`;
    }
    route.setAttribute("d", d);
    flown.setAttribute("d", d);
    pathLen = flown.getTotalLength();
    flown.style.strokeDasharray = pathLen;
    flown.style.strokeDashoffset = pathLen;
    y0 = pts[0].y; y1 = pts[pts.length - 1].y;
    fly();
  }

  function fly() {
    if (innerWidth <= 900 || !pathLen) return;
    const wr = world.getBoundingClientRect();
    const anchor = -wr.top + innerHeight * 0.42; // world-space y the plane tracks
    const p = Math.min(1, Math.max(0, (anchor - y0) / (y1 - y0)));
    const len = p * pathLen;
    const pt = flown.getPointAtLength(len);
    const back = flown.getPointAtLength(Math.max(0, len - 10));
    const ang = Math.atan2(pt.y - back.y, pt.x - back.x) * 180 / Math.PI;
    plane.style.transform = `translate(${pt.x}px, ${pt.y}px) translate(-50%,-50%) rotate(${ang + 45}deg)`;
    flown.style.strokeDashoffset = pathLen - len;
  }

  if (!reduce) {
    let ticking = false;
    addEventListener("scroll", () => {
      if (!ticking) { ticking = true; requestAnimationFrame(() => { fly(); ticking = false; }); }
    }, { passive: true });
  } else {
    plane.style.display = "none";
  }

  /* ================= MACHINE ================= */
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
  const screen = document.getElementById("screen");
  const cursor = document.getElementById("cursor");
  const box = document.getElementById("target");
  const ring = document.getElementById("clickring");
  const trace = document.getElementById("trace");
  const traceTitle = document.getElementById("trace-title");
  const somLayer = document.getElementById("som-layer");
  const mocks = [...document.querySelectorAll(".mock")];

  let rects = {}, timers = [], last = null;
  const clear = () => { timers.forEach(clearTimeout); timers = []; };
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  const activeMock = () => mocks.find((m) => m.dataset.env === state.env);

  function annotate() {
    somLayer.innerHTML = "";
    rects = {};
    const sr = screen.getBoundingClientRect();
    activeMock().querySelectorAll(".somel").forEach((el) => {
      const r = el.getBoundingClientRect();
      const x = r.left - sr.left, y = r.top - sr.top;
      rects[el.dataset.tag] = { x, y, w: r.width, h: r.height, cx: x + r.width / 2, cy: y + r.height / 2 };
      const lab = document.createElement("span");
      lab.className = "som";
      lab.textContent = el.dataset.tag;
      lab.style.left = x + "px";
      lab.style.top = y + "px";
      somLayer.appendChild(lab);
    });
  }

  function spawnTrail(x0, yy0, x1, yy1) {
    for (let i = 1; i < 6; i++) {
      const t = i / 6;
      const d = document.createElement("div");
      d.className = "trail-dot";
      d.style.left = x0 + (x1 - x0) * t + "px";
      d.style.top = yy0 + (yy1 - yy0) * t + "px";
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

  /* ================= misc ================= */
  const layer = document.getElementById("sparkle-layer");
  addEventListener("pointerdown", (e) => {
    const s = document.createElement("div");
    s.className = "sparkle";
    s.style.left = e.clientX + "px";
    s.style.top = e.clientY + "px";
    layer.appendChild(s);
    s.addEventListener("animationend", () => s.remove());
  });

  let rsTimer = null;
  addEventListener("resize", () => {
    clearTimeout(rsTimer);
    rsTimer = setTimeout(() => { annotate(); buildFlight(); }, 150);
  });

  play();
  // build the flight after fonts/layout settle
  requestAnimationFrame(() => requestAnimationFrame(buildFlight));
  setTimeout(buildFlight, 600);
})();
