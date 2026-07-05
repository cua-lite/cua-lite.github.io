/* CUA-Lite — subtle depth only.
   Parallax on the hero horizon: distant hill layers lag, near ones lead, so the
   landscape breathes with depth as you scroll. Nothing else moves. Disabled for
   prefers-reduced-motion. No metaphors, no gimmicks — just atmosphere. */
(function () {
  "use strict";
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const layers = [
    [document.querySelector(".hill-far"), 0.14],
    [document.querySelector(".hill-mid"), 0.08],
    [document.querySelector(".hill-near"), 0.03],
  ].filter(([el]) => el);
  if (!layers.length) return;

  const hero = document.querySelector(".hero");
  let ticking = false;
  function update() {
    ticking = false;
    // only animate while the hero is on screen
    if (hero && hero.getBoundingClientRect().bottom < 0) return;
    const y = window.scrollY;
    for (const [el, f] of layers) el.style.transform = `translate3d(0, ${y * f}px, 0)`;
  }
  addEventListener("scroll", () => {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }, { passive: true });
  update();
})();
