/* ============================================================
   CUA-Lite — one example, on loop.
   A computer-use agent (a real mouse cursor) does a web task:
   click the search box, type a query, run it, add to cart.
   No config, no combinatorics — just the loop, done well.
   Reduced motion: the finished frame, held still.
   ============================================================ */
(function () {
  "use strict";

  const screen = document.getElementById("screen");
  if (!screen) return;
  const cursor = document.getElementById("cursor");
  const spark = document.getElementById("ripple");
  const capAct = document.getElementById("cap-act");
  const field = screen.querySelector('[data-t="search"]');
  const query = document.getElementById("web-search");
  const grid = screen.querySelector(".bx-grid");
  const addBtn = screen.querySelector('.bx-add[data-t="add"]');

  // the one task, as a list of agent steps
  const STEPS = [
    { t: "search", cap: "click search box" },
    { t: "search", cap: 'type "wireless earbuds"', type: "wireless earbuds" },
    { t: "go", cap: "click Search", reveal: true },
    { t: "add", cap: "click Add to cart" },
    { t: "add", cap: "✓ added to cart", done: true },
  ];

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let timers = [];
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  const clearAll = () => { timers.forEach(clearTimeout); timers = []; };

  let cx = 0, cy = 0;   // tracked cursor position (px, relative to #screen)
  function place(x, y) { cx = x; cy = y; cursor.style.transform = `translate3d(${x}px, ${y}px, 0)`; }
  function centerOf(t) {
    const el = screen.querySelector(`[data-t="${t}"]`);
    if (!el) return null;
    const sr = screen.getBoundingClientRect(), r = el.getBoundingClientRect();
    return { x: r.left - sr.left + r.width / 2, y: r.top - sr.top + r.height / 2, el };
  }
  function moveTo(t) {
    const c = centerOf(t); if (!c) return;
    const dist = Math.hypot(c.x - cx, c.y - cy);
    const dur = Math.min(0.82, Math.max(0.42, dist / 540));   // longer hops take longer — natural, calm
    cursor.style.transitionDuration = dur + "s";
    place(c.x, c.y);
  }
  function click(t) {
    const c = centerOf(t); if (!c) return;
    spark.style.left = c.x + "px"; spark.style.top = c.y + "px";
    spark.classList.remove("go"); void spark.offsetWidth; spark.classList.add("go");
    c.el.classList.add("press"); at(150, () => c.el.classList.remove("press"));
  }
  function typeInto(text, done) {
    query.className = "typed caret"; field.classList.add("hot"); let i = 0;
    (function tick() {
      query.textContent = text.slice(0, i);
      if (i++ <= text.length) at(38 + Math.random() * 30, tick);
      else { query.className = "typed"; done && done(); }
    })();
  }

  function reset() {
    query.textContent = "search products…"; query.className = "mk-ph";
    field.classList.remove("hot");
    grid.classList.add("pending");   // results not there until the agent searches
    addBtn.textContent = "Add"; addBtn.classList.remove("added");
    capAct.innerHTML = "";
  }

  function run() {
    clearAll(); reset();
    // the cursor continues from wherever it last was — no teleport on loop
    let t = 650;
    STEPS.forEach((s) => {
      at(t, () => {
        moveTo(s.t);
        capAct.innerHTML = s.done ? `<b>${s.cap}</b>` : `<span class="ca-dim">agent</span> ${s.cap}`;
      });
      at(t + 520, () => {
        if (!s.done) click(s.t);
        if (s.type) typeInto(s.type);
        if (s.reveal) at(240, () => grid.classList.remove("pending")); // results pop in
        if (s.t === "add" && !s.done) at(140, () => { addBtn.textContent = "✓ Added"; addBtn.classList.add("added"); });
      });
      t += s.type ? 520 + s.type.length * 46 + 340 : (s.reveal ? 1050 : 900);
    });
    at(t + 1700, run); // hold, then loop
  }

  if (reduce) {
    query.textContent = "wireless earbuds"; query.className = "typed";
    field.classList.add("hot"); grid.classList.remove("pending");
    addBtn.textContent = "✓ Added"; addBtn.classList.add("added");
    capAct.innerHTML = "<b>✓ added to cart</b>";
    place(screen.clientWidth * 0.5, screen.clientHeight * 0.62);
  } else {
    // park the cursor with no entrance slide, then start the loop
    cursor.style.transition = "none";
    place(screen.clientWidth * 0.74, screen.clientHeight * 0.82);
    requestAnimationFrame(() => { cursor.style.transition = ""; run(); });
  }

  // the monitor tilts toward your real cursor — a physical object you can almost touch
  const heroRight = document.querySelector(".hero-right");
  const device = document.getElementById("device");
  if (!reduce && heroRight && device && matchMedia("(pointer: fine)").matches) {
    heroRight.addEventListener("pointermove", (e) => {
      const r = heroRight.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - 0.5;
      const py = (e.clientY - r.top) / r.height - 0.5;
      device.style.setProperty("--ty", (px * 6).toFixed(2) + "deg");
      device.style.setProperty("--tx", (-py * 5).toFixed(2) + "deg");
    });
    heroRight.addEventListener("pointerleave", () => {
      device.style.setProperty("--ty", "0deg");
      device.style.setProperty("--tx", "0deg");
    });
  }

  // scroll reveal — content settles up as it enters view
  const reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window && !reduce) {
    document.documentElement.classList.add("js-reveal");
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.12 });
    reveals.forEach((el) => io.observe(el));
  }
})();
