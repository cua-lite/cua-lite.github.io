/* ============================================================
   CUA-Lite — one living element.
   The hero terminal types a real rollout (command -> agent steps ->
   reward -> LiteSample), cycling desktop / web / mobile. Everything
   else on the page is still.
   Reduced motion: static transcript, no typing.
   ============================================================ */
(function () {
  "use strict";

  const term = document.getElementById("term");
  if (!term) return;

  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  const D = (s) => `<span class="t-dim">${s}</span>`;
  const T = (s) => `<span class="t-tag">${s}</span>`;
  const G = (s) => `<span class="t-acc">${s}</span>`;
  const S = (s) => `<span class="t-str">${s}</span>`;

  const EPISODES = [
    {
      cmd: "python rollout.py --model-id gpt-5.5 --env-id lite.osworld",
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
      cmd: "python rollout.py --model-id gpt-5.5 --env-id webarena",
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
      cmd: "python rollout.py --model-id gpt-5.5 --env-id mobilegym",
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

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) {
    const ep = EPISODES[0];
    term.innerHTML = D("$ ") + esc(ep.cmd) + "\n\n" + ep.lines.join("\n");
    return;
  }

  let epi = 0, timers = [];
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  const clearTimers = () => { timers.forEach(clearTimeout); timers = []; };

  function typeCommand(cmd, done) {
    let i = 0;
    term.innerHTML = D("$ ") + '<span class="t-cur"></span>';
    (function tick() {
      if (i <= cmd.length) {
        term.innerHTML = D("$ ") + esc(cmd.slice(0, i)) + '<span class="t-cur"></span>';
        i++;
        timers.push(setTimeout(tick, 22 + Math.random() * 26));
      } else {
        term.innerHTML = D("$ ") + esc(cmd) + "\n\n";
        done();
      }
    })();
  }

  function playEpisode() {
    clearTimers();
    const ep = EPISODES[epi];
    typeCommand(ep.cmd, () => {
      const base = D("$ ") + esc(ep.cmd) + "\n\n";
      let shown = [];
      ep.lines.forEach((line, i) => {
        at(360 * (i + 1) + (i > 0 ? 90 * i : 0), () => {
          shown.push(line);
          const last = i === ep.lines.length - 1;
          term.innerHTML = base + shown.join("\n") + (last ? "" : '\n<span class="t-cur"></span>');
        });
      });
      // hold the finished transcript, then next episode
      at(360 * ep.lines.length + 90 * ep.lines.length + 3400, () => {
        epi = (epi + 1) % EPISODES.length;
        playEpisode();
      });
    });
  }

  playEpisode();
})();
