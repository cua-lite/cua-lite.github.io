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

  // the one task, as a list of agent steps
  const STEPS = [
    { t: "search", cap: "click search box" },
    { t: "search", cap: 'type "wireless earbuds"', type: "wireless earbuds" },
    { t: "go", cap: "click Search" },
    { t: "add", cap: "click Add to cart" },
    { t: "add", cap: "✓ added to cart", done: true },
  ];

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let timers = [];
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  const clearAll = () => { timers.forEach(clearTimeout); timers = []; };

  function centerOf(t) {
    const el = screen.querySelector(`[data-t="${t}"]`);
    if (!el) return null;
    const sr = screen.getBoundingClientRect(), r = el.getBoundingClientRect();
    return { x: r.left - sr.left + r.width / 2, y: r.top - sr.top + r.height / 2, el };
  }
  function moveTo(t) {
    const c = centerOf(t); if (!c) return;
    cursor.style.left = c.x + "px"; cursor.style.top = c.y + "px";
  }
  function click(t) {
    const c = centerOf(t); if (!c) return;
    spark.style.left = c.x + "px"; spark.style.top = c.y + "px";
    spark.classList.remove("go"); void spark.offsetWidth; spark.classList.add("go");
    c.el.classList.add("press"); at(150, () => c.el.classList.remove("press"));
  }
  function typeInto(text, done) {
    query.className = "typed"; field.classList.add("hot"); let i = 0;
    (function tick() {
      query.textContent = text.slice(0, i);
      if (i++ <= text.length) at(38 + Math.random() * 30, tick); else done && done();
    })();
  }

  function reset() {
    query.textContent = "search products…"; query.className = "mk-ph";
    field.classList.remove("hot");
    capAct.innerHTML = "";
  }

  function run() {
    clearAll(); reset();
    // park the cursor bottom-right, then work
    cursor.style.left = "76%"; cursor.style.top = "82%";
    let t = 650;
    STEPS.forEach((s) => {
      at(t, () => {
        moveTo(s.t);
        capAct.innerHTML = s.done ? `<b>${s.cap}</b>` : `<span class="ca-dim">agent</span> ${s.cap}`;
      });
      at(t + 520, () => { if (!s.done) click(s.t); if (s.type) typeInto(s.type); });
      t += s.type ? 520 + s.type.length * 46 + 340 : 900;
    });
    at(t + 1700, run); // hold, then loop
  }

  if (reduce) {
    query.textContent = "wireless earbuds"; query.className = "typed";
    field.classList.add("hot");
    capAct.innerHTML = "<b>✓ added to cart</b>";
  } else {
    run();
  }
})();
