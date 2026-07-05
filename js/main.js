/* ============================================================
   CUA-Lite — the agent's-eye view
   The cursor walks the Set-of-Marks tags while the action trace
   types the observe -> think -> act loop. Pick an agent or an env
   and the same loop replays — the interaction IS the thesis.
   ============================================================ */
(function () {
  "use strict";

  // SoM tag anchor points (% of the screen), matching the tags in the HTML
  // [x, y, w, h] in % of the screen — box frames the element, cursor lands on it
  const P = { 1: [90, 16, 7, 11], 2: [38, 37, 66, 12], 3: [85, 37, 13, 12], 4: [12, 84, 13, 11], 5: [55, 84, 13, 11] };

  // per-environment scenario: url + a rollout as a list of steps
  const ENV = {
    web: {
      url: "shop.example.com",
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
      url: "LibreOffice Calc — report.ods",
      steps: [
        { op: "observe", arg: "screenshot 1920×1080" },
        { op: "click", tag: 1, arg: "File menu" },
        { op: "click", tag: 2, arg: "cell B12" },
        { op: "type", arg: '"=SUM(B1:B11)"' },
        { op: "key", arg: "Enter" },
        { op: "done", arg: "reward 1.0", ok: true },
      ],
    },
    mobile: {
      url: "Contacts",
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
  const mockUrl = document.getElementById("mock-url");

  let timers = [];
  const clear = () => { timers.forEach(clearTimeout); timers = []; };
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));

  function moveTo(tag) {
    const [x, y, w, h] = P[tag];
    cursor.style.left = x + "%";
    cursor.style.top = y + "%";
    box.style.left = x + "%";
    box.style.top = y + "%";
    box.style.width = w + "%";
    box.style.height = h + "%";
    box.style.opacity = "1";
  }
  function clickFx(tag) {
    const [x, y] = P[tag];
    ring.style.left = x + "%";
    ring.style.top = y + "%";
    ring.classList.remove("fire");
    void ring.offsetWidth;
    ring.classList.add("fire");
  }

  function addLine(step, i) {
    const el = document.createElement("div");
    el.className = "trace-line";
    const idx = String(i + 1).padStart(3, "0");
    const arg = step.tag
      ? `<span class="tag">[${step.tag}]</span> ${step.arg}`
      : step.arg;
    const opColor = step.ok ? "arg" : "op";
    el.innerHTML = `<span class="idx">${idx}</span><span class="op" style="${step.ok ? "color:#7ddc9a" : ""}">${step.op}</span><span class="arg">${arg}</span>`;
    trace.appendChild(el);
    requestAnimationFrame(() => el.classList.add("on"));
    return el;
  }

  function resetTrace() {
    [...trace.querySelectorAll(".trace-line")].forEach((n) => n.remove());
  }

  function play() {
    clear();
    resetTrace();
    box.style.opacity = "0";
    const env = ENV[state.env];
    traceTitle.textContent = `rollout · ${state.agent} · ${state.env === "web" ? "webarena" : state.env === "desktop" ? "lite.osworld" : "mobilegym"}`;
    mockUrl.textContent = env.url;

    if (reduce) { env.steps.forEach(addLine); return; }

    let t = 400;
    env.steps.forEach((step, i) => {
      at(t, () => {
        if (step.tag) moveTo(step.tag);
        at(step.tag ? 480 : 0, () => {
          if (step.tag) clickFx(step.tag);
          addLine(step, i);
        });
      });
      t += step.tag ? 1150 : 780;
    });
    // loop
    at(t + 1400, play);
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

  // click sparkle — a small nod to the teaser, site-wide
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
