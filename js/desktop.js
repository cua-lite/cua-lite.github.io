/* ============================================================
   Desktop interactions — every one of these is a piece of the pitch:
   - agent × env knobs -> "any CUA, any environment" (the thesis)
   - CRT channel switch -> unified action space across Desktop/Web/Mobile
   - click sparkle       -> the teaser motif, site-wide
   - scroll reveals      -> feature windows "open" as you go
   ============================================================ */
(function () {
  "use strict";

  // ---- state: which agent × which env is currently "running" ----
  const state = { agent: "gpt-5.5", env: "desktop", title: "lite.osworld" };

  const runCmd = document.getElementById("run-cmd");
  const crtTitle = document.getElementById("crt-title");
  const channels = document.querySelectorAll(".channel");

  // env_id shown in the run line per channel
  const ENV_ID = { desktop: "lite.osworld", web: "webarena", mobile: "mobilegym" };
  const TASK = {
    desktop: "osworld_chrome_030eeff7",
    web: "webarena_shopping_147",
    mobile: "mobilegym_contacts_add",
  };

  function renderRunLine() {
    // the run line literally shows how any agent composes with any env
    runCmd.textContent =
      `rollout.py --model-id ${state.agent} --env-id ${ENV_ID[state.env]} --task-id ${TASK[state.env]}`;
  }

  function setChannel(env) {
    state.env = env;
    channels.forEach((c) => c.classList.toggle("active", c.dataset.env === env));
    crtTitle.textContent = ENV_ID[env];
    renderRunLine();
  }

  // ---- pills: agent picker ----
  document.querySelectorAll("#agent-pills .pill").forEach((p) => {
    p.addEventListener("click", () => {
      document.querySelectorAll("#agent-pills .pill").forEach((x) => x.classList.remove("active"));
      p.classList.add("active");
      state.agent = p.dataset.agent;
      renderRunLine();
    });
  });

  // ---- pills: env picker (also flips the CRT channel) ----
  document.querySelectorAll("#env-pills .pill").forEach((p) => {
    p.addEventListener("click", () => {
      document.querySelectorAll("#env-pills .pill").forEach((x) => x.classList.remove("active"));
      p.classList.add("active");
      setChannel(p.dataset.env);
    });
  });

  renderRunLine();

  // ---- click sparkle (teaser motif) site-wide ----
  const layer = document.getElementById("sparkle-layer");
  window.addEventListener("pointerdown", (e) => {
    const s = document.createElement("div");
    s.className = "sparkle";
    s.style.left = e.clientX + "px";
    s.style.top = e.clientY + "px";
    layer.appendChild(s);
    s.addEventListener("animationend", () => s.remove());
  });

  // ---- reveal feature windows on scroll; fill the XP bar when it appears ----
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        const fill = en.target.querySelector(".xp-fill");
        if (fill) fill.style.width = (fill.dataset.fill || 80) + "%";
        io.unobserve(en.target);
      });
    },
    { threshold: 0.25 }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  // expose for boot.js to call once the desktop is revealed
  window.__cuaDesktop = { setChannel, renderRunLine };
})();
