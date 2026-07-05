/* ============================================================
   CUA-Lite — interactive console
   Pick an agent + an environment; the same command runs it.
   The interaction IS the pitch: any CUA × any environment.
   ============================================================ */
(function () {
  "use strict";

  const ENV = {
    desktop: { id: "lite.osworld", task: "osworld_chrome_030eeff7", url: "lite.osworld", frame: "browser", img: "assets/showcase/lite_osworld.gif" },
    web:     { id: "webarena",     task: "webarena_shopping_147",   url: "webarena",     frame: "browser", img: "assets/showcase/webarena.gif" },
    mobile:  { id: "mobilegym",    task: "mobilegym_contacts_add",  url: "mobilegym",    frame: "phone",   img: "assets/showcase/mobilegym.gif" },
  };

  const state = { agent: "gpt-5.5", env: "desktop" };

  const frameDesktop = document.getElementById("frame-desktop");
  const framePhone = document.getElementById("frame-mobile");
  const shotLandscape = document.getElementById("shot-landscape");
  const shotPortrait = document.getElementById("shot-portrait");
  const frameUrl = document.getElementById("frame-url");
  const codeEl = document.getElementById("repro-code");

  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;"); }

  function plainCmd() {
    const e = ENV[state.env];
    return `uv run python scripts/rollout.py \\\n    --model-id ${state.agent} \\\n    --env-id ${e.id} --task-id ${e.task} \\\n    --save-gif`;
  }

  function render() {
    const e = ENV[state.env];
    // preview frame
    if (e.frame === "phone") {
      frameDesktop.classList.add("hidden");
      framePhone.classList.remove("hidden");
      shotPortrait.src = e.img;
    } else {
      framePhone.classList.add("hidden");
      frameDesktop.classList.remove("hidden");
      if (shotLandscape.getAttribute("src") !== e.img) shotLandscape.src = e.img;
      frameUrl.textContent = e.url;
    }
    // highlighted reproduce command
    codeEl.innerHTML =
      `<span class="c-dim">$</span> uv run python scripts/rollout.py \\\n` +
      `    <span class="c-flag">--model-id</span> <span class="c-str">${esc(state.agent)}</span> \\\n` +
      `    <span class="c-flag">--env-id</span> <span class="c-str">${esc(e.id)}</span> <span class="c-flag">--task-id</span> <span class="c-str">${esc(e.task)}</span> \\\n` +
      `    <span class="c-flag">--save-gif</span>`;
  }

  document.querySelectorAll("#agent-chips .chip").forEach((c) => {
    c.addEventListener("click", () => {
      document.querySelectorAll("#agent-chips .chip").forEach((x) => x.classList.remove("active"));
      c.classList.add("active");
      state.agent = c.dataset.agent;
      render();
    });
  });
  document.querySelectorAll("#env-tabs .tab").forEach((t) => {
    t.addEventListener("click", () => {
      document.querySelectorAll("#env-tabs .tab").forEach((x) => x.classList.remove("active"));
      t.classList.add("active");
      state.env = t.dataset.env;
      render();
    });
  });

  const copyBtn = document.getElementById("copy-btn");
  copyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(plainCmd()).then(() => {
      copyBtn.textContent = "copied";
      setTimeout(() => (copyBtn.textContent = "copy"), 1400);
    });
  });

  // pixel click sparkle (a small, tasteful nod to the teaser)
  const layer = document.getElementById("sparkle-layer");
  window.addEventListener("pointerdown", (e) => {
    const s = document.createElement("div");
    s.className = "sparkle";
    s.style.left = e.clientX + "px";
    s.style.top = e.clientY + "px";
    layer.appendChild(s);
    s.addEventListener("animationend", () => s.remove());
  });

  render();
})();
