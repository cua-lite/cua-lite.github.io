/* ============================================================
   CUA-Lite — Minecraft edition
   1) CRAFTING TABLE: click the agent/env slot to swap the "items";
      the output command updates. [Agent] + [Env] -> Rollout.
   2) FLIGHT: the paper airplane glides down a gentle dashed path
      as you scroll and lands on the grass.
   ============================================================ */
(function () {
  "use strict";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- crafting table ---------------- */
  const AGENTS = [
    { id: "gpt-5.5", flag: "gpt-5.5", ico: "assets/icons/w_cpu.png" },
    { id: "claude", flag: "claude-opus-4-8", ico: "assets/icons/w_cpu.png" },
    { id: "qwen3-vl", flag: "Qwen/Qwen3-VL-8B", ico: "assets/icons/w_cpu.png" },
    { id: "ui-tars", flag: "ui-tars", ico: "assets/icons/w_cpu.png" },
  ];
  const ENVS = [
    { id: "web", env: "webarena", ico: "assets/icons/w_web.png" },
    { id: "desktop", env: "lite.osworld", ico: "assets/icons/w_desktop.png" },
    { id: "mobile", env: "mobilegym", ico: "assets/icons/w_mobile.png" },
  ];
  let ai = 0, ei = 0;
  const agentItem = document.getElementById("agent-item");
  const envItem = document.getElementById("env-item");
  const agentCap = document.getElementById("agent-cap");
  const envCap = document.getElementById("env-cap");
  const cmd = document.getElementById("craft-cmd");

  function renderCraft() {
    const a = AGENTS[ai], e = ENVS[ei];
    agentItem.style.backgroundImage = `url('${a.ico}')`;
    envItem.style.backgroundImage = `url('${e.ico}')`;
    agentCap.textContent = a.id;
    envCap.textContent = e.id;
    cmd.innerHTML =
      `<span class="dm">$</span> rollout.py ` +
      `<span class="fl">--model-id</span> <span class="st">${a.flag}</span> ` +
      `<span class="fl">--env-id</span> <span class="st">${e.env}</span>`;
  }
  function bump(el) { el.animate([{ transform: "scale(1)" }, { transform: "scale(1.18)" }, { transform: "scale(1)" }], { duration: 220 }); }
  document.getElementById("agent-slot").addEventListener("click", () => { ai = (ai + 1) % AGENTS.length; renderCraft(); bump(agentItem); });
  document.getElementById("env-slot").addEventListener("click", () => { ei = (ei + 1) % ENVS.length; renderCraft(); bump(envItem); });
  renderCraft();

  /* ---------------- flight ---------------- */
  const world = document.getElementById("world");
  const svg = document.getElementById("flight");
  const route = document.getElementById("route");
  const flown = document.getElementById("flown");
  const plane = document.getElementById("plane");
  let pathLen = 0;

  function buildFlight() {
    if (innerWidth <= 900) { plane.style.display = "none"; return; }
    plane.style.display = "";
    const W = world.clientWidth, H = world.scrollHeight;
    svg.setAttribute("width", W); svg.setAttribute("height", H); svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    // a gentle wave descending the right third, landing on the grass strip
    const cx = W * 0.82, amp = Math.min(70, W * 0.05), top = 150, bottom = H - 54;
    let d = `M ${cx} ${top}`;
    const seg = 7;
    for (let i = 1; i <= seg; i++) {
      const t = i / seg, y = top + (bottom - top) * t;
      const x = cx + Math.sin(t * Math.PI * 2.2) * amp * (1 - t * 0.4);
      const py = top + (bottom - top) * ((i - 0.5) / seg);
      const px = cx + Math.sin((t - 0.5 / seg) * Math.PI * 2.2) * amp;
      d += ` Q ${px} ${py}, ${x} ${y}`;
    }
    route.setAttribute("d", d); flown.setAttribute("d", d);
    pathLen = flown.getTotalLength();
    flown.style.strokeDasharray = `${pathLen}`;
    flown.style.strokeDashoffset = `${pathLen}`;
    fly();
  }

  function fly() {
    if (innerWidth <= 900 || !pathLen) return;
    // progress = how far down the whole page we've scrolled -> plane lands at the end
    const max = document.body.scrollHeight - innerHeight;
    const p = max > 0 ? Math.min(1, Math.max(0, scrollY / max)) : 0;
    const len = p * pathLen;
    const pt = flown.getPointAtLength(len);
    const back = flown.getPointAtLength(Math.max(0, len - 8));
    const ang = Math.atan2(pt.y - back.y, pt.x - back.x) * 180 / Math.PI;
    plane.style.transform = `translate(${pt.x}px, ${pt.y}px) translate(-50%,-50%) rotate(${ang + 45}deg)`;
    // dashed trail: reveal is subtle, so nudge dashoffset toward flown length
    flown.style.strokeDashoffset = `${pathLen - len}`;
  }

  if (!reduce) {
    let ticking = false;
    addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { fly(); ticking = false; }); } }, { passive: true });
  }

  /* ---------------- misc ---------------- */
  const layer = document.getElementById("sparkle-layer");
  addEventListener("pointerdown", (e) => {
    const s = document.createElement("div");
    s.className = "sparkle"; s.style.left = e.clientX + "px"; s.style.top = e.clientY + "px";
    layer.appendChild(s); s.addEventListener("animationend", () => s.remove());
  });
  let rs; addEventListener("resize", () => { clearTimeout(rs); rs = setTimeout(buildFlight, 150); });

  requestAnimationFrame(() => requestAnimationFrame(buildFlight));
  setTimeout(buildFlight, 500);
})();
