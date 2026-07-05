/* ============================================================
   CUA-Lite — one example, on loop.
   A computer-use agent (a real mouse cursor) does a desktop task in
   LibreOffice Calc: select cell B5, type =SUM(B2:B4), press Enter —
   the total lands. Think → move → act, in a breathing pixel world.
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
  const cell = document.getElementById("total");   // the Total cell (B5)
  const fbar = document.getElementById("fbar");     // formula bar
  const fillText = "2,402";

  // the one task: compute a total in LibreOffice Calc
  const STEPS = [
    { t: "cell", cap: "select cell B5", sel: true },
    { t: "cell", cap: "type =SUM(B2:B4)", type: "=SUM(B2:B4)" },
    { t: "cell", cap: "press Enter", enter: true },
    { t: "cell", cap: "✓ Total = 2,402", done: true },
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
    fbar.className = "sh-formula typed caret"; let i = 0;
    (function tick() {
      fbar.textContent = text.slice(0, i);
      if (i++ <= text.length) at(40 + Math.random() * 32, tick);
      else { fbar.className = "sh-formula typed"; done && done(); }
    })();
  }

  function reset() {
    fbar.innerHTML = '<span class="mk-ph"></span>'; fbar.className = "sh-formula";
    cell.textContent = ""; cell.classList.remove("filled");
    document.querySelectorAll(".sh-cell.sel").forEach((e) => e.classList.remove("sel"));
    capAct.innerHTML = "";
  }

  const setCap = (html) => { capAct.innerHTML = html; };
  const THINK = '<span class="ca-dim">agent</span> <span class="think">thinking<i>.</i><i>.</i><i>.</i></span>';

  function run() {
    clearAll(); reset();
    // the cursor continues from wherever it last was — no teleport on loop
    let t = 500;
    STEPS.forEach((s) => {
      if (s.done) {                              // final: the outcome, held
        at(t, () => setCap(`<b>${s.cap}</b>`));
        t += 900;
        return;
      }
      at(t, () => setCap(THINK));                // 1) reason (fills the pause with meaning)
      at(t + 480, () => {                         // 2) move to target + name the action
        moveTo(s.t);
        setCap(`<span class="ca-dim">agent</span> ${s.cap}`);
      });
      at(t + 980, () => {                         // 3) act, once the cursor has settled
        click(s.t);
        if (s.sel) cell.classList.add("sel");            // selecting the cell
        if (s.type) typeInto(s.type);
        if (s.enter) at(120, () => { cell.textContent = fillText; cell.classList.add("filled"); }); // Enter → result lands
      });
      t += 980 + (s.type ? s.type.length * 46 + 320 : 260) + 300;   // act duration + settle
    });
    at(t + 1500, run); // hold on the result, then loop
  }

  if (reduce) {
    fbar.className = "sh-formula typed"; fbar.textContent = "=SUM(B2:B4)";
    cell.textContent = fillText; cell.classList.add("filled", "sel");
    capAct.innerHTML = "<b>✓ Total = 2,402</b>";
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

  // the desktop clock shows the real time — a small sign of life
  const clock = document.querySelector(".tb-clock");
  if (clock) {
    const tick = () => { const d = new Date(); clock.textContent = ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2); };
    tick(); setInterval(tick, 20000);
  }
})();
