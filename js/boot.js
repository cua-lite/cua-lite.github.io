/* ============================================================
   Boot narrative — canvas replay of the README teaser:
   power-on -> paper-airplane screensaver -> cursor click -> the
   "Bliss" grass wallpaper fills in -> lift to reveal the desktop.

   Plays on FIRST visit only (localStorage), and is skipped entirely
   for repeat visitors or prefers-reduced-motion. Skip button always on.
   ============================================================ */
(function () {
  "use strict";

  const boot = document.getElementById("boot");
  const desktop = document.getElementById("desktop");
  const canvas = document.getElementById("boot-canvas");
  const skipBtn = document.getElementById("boot-skip");

  const SEEN_KEY = "cua_booted_v1";
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const seen = (() => { try { return localStorage.getItem(SEEN_KEY); } catch (e) { return null; } })();

  function reveal(instant) {
    desktop.classList.remove("hidden");
    try { localStorage.setItem(SEEN_KEY, "1"); } catch (e) {}
    if (instant) { boot.remove(); return; }
    boot.classList.add("lift");
    boot.addEventListener("animationend", () => boot.remove(), { once: true });
  }

  // Repeat visit / reduced motion -> straight to the desktop, no cinematic.
  if (seen || reduce) { reveal(true); return; }

  // ---------- assets ----------
  const A = {};
  const srcs = {
    airplane: "assets/pixel/airplane.png",
    cursor: "assets/pixel/cursor.png",
    sparkle: "assets/pixel/sparkle.png",
    wallpaper: "assets/pixel/wallpaper.png",
  };
  let pending = Object.keys(srcs).length;
  let started = false;
  Object.entries(srcs).forEach(([k, src]) => {
    const im = new Image();
    im.onload = im.onerror = () => { A[k] = im; if (--pending === 0 && !started) start(); };
    im.src = src;
  });
  // safety: never block the site on a slow asset
  setTimeout(() => { if (!started) start(); }, 1500);

  // ---------- canvas sizing (crisp pixels) ----------
  const ctx = canvas.getContext("2d");
  ctx.imageSmoothingEnabled = false;
  let W, H, dpr;
  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = W * dpr; canvas.height = H * dpr;
    canvas.style.width = W + "px"; canvas.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingEnabled = false;
  }
  window.addEventListener("resize", resize);
  resize();

  // ---------- timeline (ms) ----------
  const T = { power: 450, saver: 1500, cursor: 2150, click: 2400, wipe: 3000, done: 3250 };
  let t0 = 0;

  function drawImageContain(img, cx, cy, scale) {
    if (!img || !img.width) return;
    const w = img.width * scale, h = img.height * scale;
    ctx.drawImage(img, cx - w / 2, cy - h / 2, w, h);
  }

  // cursor path: slides in from the right edge to the click point
  const click = () => ({ x: W * 0.56, y: H * 0.52 });
  const cursorStart = () => ({ x: W + 40, y: H * 0.42 });

  function frame(now) {
    if (!t0) t0 = now;
    const t = now - t0;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = "#0d0f14";
    ctx.fillRect(0, 0, W, H);

    const cx = W / 2, cy = H / 2;

    // Phase 1: power-on — a bright band opens vertically
    if (t < T.power) {
      const p = t / T.power;
      const bandH = Math.max(2, p * H);
      ctx.fillStyle = "#0d0f14";
      ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = `rgba(244,246,248,${0.9 * (1 - p)})`;
      ctx.fillRect(0, cy - bandH / 2, W, bandH);
      requestAnimationFrame(frame);
      return;
    }

    // Wallpaper wipe (top -> down) once we reach the wipe phase
    const wiping = t >= T.click;
    if (wiping && A.wallpaper && A.wallpaper.width) {
      const wp = coverRect(A.wallpaper, W, H);
      const p = Math.min(1, (t - T.click) / (T.wipe - T.click));
      const revealH = p * H;
      ctx.save();
      ctx.beginPath();
      ctx.rect(0, 0, W, revealH);
      ctx.clip();
      ctx.drawImage(A.wallpaper, wp.x, wp.y, wp.w, wp.h);
      ctx.restore();
    }

    // Phase 2/3: airplane screensaver (fades out as wallpaper wipes in)
    if (t < T.wipe) {
      const bob = Math.sin(t / 260) * (H * 0.012);
      const scale = Math.min(W, H) / 620;
      ctx.globalAlpha = t >= T.click ? Math.max(0, 1 - (t - T.click) / (T.wipe - T.click)) : 1;
      drawImageContain(A.airplane, cx, cy + bob, scale);
      ctx.globalAlpha = 1;
    }

    // Phase 3: cursor slides in
    if (t >= T.saver) {
      const p = Math.min(1, (t - T.saver) / (T.cursor - T.saver));
      const e = 1 - Math.pow(1 - p, 3); // ease-out
      const s = cursorStart(), k = click();
      const px = s.x + (k.x - s.x) * e, py = s.y + (k.y - s.y) * e;
      const cs = Math.min(W, H) / 900; // cursor ~ modest size
      if (A.cursor) ctx.drawImage(A.cursor, px, py, A.cursor.width * cs, A.cursor.height * cs);

      // Phase 4: click sparkle
      if (t >= T.click && t < T.click + 260) {
        const sp = (t - T.click) / 260;
        const ss = (0.3 + sp) * (Math.min(W, H) / 700);
        ctx.globalAlpha = 1 - sp;
        drawImageContain(A.sparkle, px + 4, py + 4, ss);
        ctx.globalAlpha = 1;
      }
    }

    // scanlines over everything for CRT feel
    drawScanlines();

    if (t >= T.done) { reveal(false); return; }
    requestAnimationFrame(frame);
  }

  function coverRect(img, w, h) {
    const s = Math.max(w / img.width, h / img.height);
    const iw = img.width * s, ih = img.height * s;
    return { x: (w - iw) / 2, y: (h - ih) / 2, w: iw, h: ih };
  }

  function drawScanlines() {
    ctx.globalAlpha = 0.14;
    ctx.fillStyle = "#000";
    for (let y = 0; y < H; y += 3) ctx.fillRect(0, y, W, 1);
    ctx.globalAlpha = 1;
  }

  function start() {
    if (started) return;
    started = true;
    t0 = 0;
    requestAnimationFrame(frame);
  }

  skipBtn.addEventListener("click", () => reveal(false));
})();
