/* CUA-Lite — a small pixel sparkle on click (the teaser motif). That's it:
   the page is a straightforward, Minecraft-styled project landing page. */
(function () {
  "use strict";
  const layer = document.getElementById("sparkle-layer");
  if (!layer) return;
  addEventListener("pointerdown", (e) => {
    const s = document.createElement("div");
    s.className = "sparkle";
    s.style.left = e.clientX + "px";
    s.style.top = e.clientY + "px";
    layer.appendChild(s);
    s.addEventListener("animationend", () => s.remove());
  });
})();
