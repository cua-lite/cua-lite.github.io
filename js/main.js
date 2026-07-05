/* ============================================================
   CUA-Lite — the terminal is interactive.
   Compose an agent × an environment; the terminal runs THAT
   real rollout: command → observe → click/type → reward 1.0 →
   LiteSample. On load it shows a completed run at a ready-prompt;
   picking a chip re-runs it with a live typing animation — a real REPL.
   Reduced motion: static transcript, no typing.
   ============================================================ */
(function () {
  "use strict";

  const term = document.getElementById("term");
  if (!term) return;
  const title = document.getElementById("term-title");

  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  const D = (s) => `<span class="t-dim">${s}</span>`;
  const T = (s) => `<span class="t-tag">${s}</span>`;
  const G = (s) => `<span class="t-acc">${s}</span>`;
  const S = (s) => `<span class="t-str">${s}</span>`;

  const AGENTS = [
    { id: "gpt-5.5", flag: "gpt-5.5" },
    { id: "claude-opus-4-8", flag: "claude-opus-4-8", label: "claude" },
    { id: "Qwen/Qwen3-VL-8B", flag: "Qwen/Qwen3-VL-8B", label: "qwen3-vl" },
    { id: "ui-tars", flag: "ui-tars" },
  ];
  const ENVS = [
    {
      id: "desktop", env: "lite.osworld",
      lines: [
        T("[env]   ") + " boot lite.osworld " + D("… ready in 2.1s"),
        T("[agent] ") + " observe   " + D("screenshot 1920×1080"),
        T("[agent] ") + " think     " + S('"total column B"'),
        T("[agent] ") + " click     cell B12",
        T("[agent] ") + " type      " + S('"=SUM(B1:B11)"') + D("  + Enter"),
        T("[eval]  ") + " reward    " + G("1.0"),
        T("[data]  ") + " LiteSample " + D("→") + " " + G("ready to train"),
      ],
    },
    {
      id: "web", env: "webarena",
      lines: [
        T("[env]   ") + " boot webarena " + D("… ready in 1.4s"),
        T("[agent] ") + " observe   " + D("screenshot 1280×720"),
        T("[agent] ") + " think     " + S('"find wireless earbuds"'),
        T("[agent] ") + " type      " + S('"wireless earbuds"') + D("  in [search]"),
        T("[agent] ") + " click     add to cart",
        T("[eval]  ") + " reward    " + G("1.0"),
        T("[data]  ") + " LiteSample " + D("→") + " " + G("ready to train"),
      ],
    },
    {
      id: "mobile", env: "mobilegym",
      lines: [
        T("[env]   ") + " boot mobilegym " + D("… ready in 1.7s"),
        T("[agent] ") + " observe   " + D("screenshot 1080×2400"),
        T("[agent] ") + " tap       + new contact",
        T("[agent] ") + " type      " + S('"Ada Lovelace"'),
        T("[agent] ") + " tap       save",
        T("[eval]  ") + " reward    " + G("1.0"),
        T("[data]  ") + " LiteSample " + D("→") + " " + G("ready to train"),
      ],
    },
  ];

  const state = { ai: 0, ei: 0, interacted: false };
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  function cmdOf() {
    return `python rollout.py --model-id ${AGENTS[state.ai].flag} --env-id ${ENVS[state.ei].env}`;
  }
  function setTitle() {
    if (title) title.textContent = `cua-lite — ${ENVS[state.ei].env}`;
  }

  if (reduce) {
    setTitle();
    term.innerHTML = D("$ ") + esc(cmdOf()) + "\n\n" + ENVS[state.ei].lines.join("\n");
    wireChips(true);
    return;
  }

  let timers = [];
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  const clearTimers = () => { timers.forEach(clearTimeout); timers = []; };

  function typeCommand(cmd, done) {
    let i = 0;
    (function tick() {
      if (i <= cmd.length) {
        term.innerHTML = D("$ ") + esc(cmd.slice(0, i)) + '<span class="t-cur"></span>';
        i++;
        timers.push(setTimeout(tick, 9 + Math.random() * 13));
      } else {
        done();
      }
    })();
  }

  function playEpisode() {
    clearTimers();
    setTitle();
    const ep = ENVS[state.ei];
    const cmd = cmdOf();
    typeCommand(cmd, () => {
      const base = D("$ ") + esc(cmd) + "\n\n";
      const shown = [];
      ep.lines.forEach((line, i) => {
        at(240 * (i + 1) + 260, () => {
          shown.push(line);
          const last = i === ep.lines.length - 1;
          // after the last line settles, drop to a fresh ready-prompt — "your turn"
          const tail = last ? '\n\n' + D("$ ") + '<span class="t-cur"></span>' : '\n<span class="t-cur"></span>';
          term.innerHTML = base + shown.join("\n") + tail;
        });
      });
    });
  }

  // on load: a completed rollout (full box, no empty void) waiting at a ready-prompt
  function renderFull() {
    clearTimers();
    setTitle();
    const ep = ENVS[state.ei];
    term.innerHTML = D("$ ") + esc(cmdOf()) + "\n\n" + ep.lines.join("\n") + "\n\n" + D("$ ") + '<span class="t-cur"></span>';
  }

  function syncActive() {
    document.querySelectorAll("#env-row .chip").forEach((c, i) => c.classList.toggle("active", i === state.ei));
    document.querySelectorAll("#agent-row .chip").forEach((c, i) => c.classList.toggle("active", i === state.ai));
  }

  function wireChips(staticMode) {
    document.querySelectorAll("#agent-row .chip").forEach((c, i) => {
      c.addEventListener("click", () => {
        state.ai = i; state.interacted = true; syncActive();
        if (staticMode) term.innerHTML = D("$ ") + esc(cmdOf()) + "\n\n" + ENVS[state.ei].lines.join("\n");
        else playEpisode();
      });
    });
    document.querySelectorAll("#env-row .chip").forEach((c, i) => {
      c.addEventListener("click", () => {
        state.ei = i; state.interacted = true; syncActive();
        if (staticMode) { setTitle(); term.innerHTML = D("$ ") + esc(cmdOf()) + "\n\n" + ENVS[state.ei].lines.join("\n"); }
        else playEpisode();
      });
    });
  }

  wireChips(false);
  renderFull();   // start filled — the deliberate typing plays when you pick a chip
})();
