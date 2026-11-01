/* Cortinas fluidas: el mismo fondo del menú principal de Larp Client.
   Se dibujan a baja resolución y el navegador las escala con blur, así cuestan casi nada. */
(function () {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const W = 220, H = 124;

  function start(canvas) {
    canvas.width = W; canvas.height = H;
    const ctx = canvas.getContext("2d", { alpha: true });
    const img = ctx.createImageData(W, H);
    const d = img.data;
    const tint = (canvas.dataset.tint || "108,123,255").split(",").map(Number);
    const strength = parseFloat(canvas.dataset.strength || "1");
    let intersecting = false, raf = 0, last = 0;
    const visible = () => intersecting && !document.hidden;

    // Pliegues: posición, ancho y fase propios; se mueven como tela colgando.
    const folds = [];
    for (let i = 0; i < 15; i++) {
      folds.push({ x: (i + 0.5) / 15 + (Math.sin(i * 12.9898) * 0.5) * 0.03, w: 0.018 + ((i * 7) % 5) * 0.004, p: i * 1.7, s: 0.35 + ((i * 3) % 4) * 0.08 });
    }

    const fxs = new Float32Array(folds.length);
    const spots = new Float32Array(W);
    for (let x = 0; x < W; x++) { const c = (x / W - 0.5) * 1.5; spots[x] = Math.exp(-(c * c) * 2.2); }

    function frame(now) {
      raf = 0;
      if (!visible()) return;
      if (now - last < 67 && !reduce) { raf = requestAnimationFrame(frame); return; } // ~30 fps
      last = now;
      const t = reduce ? 0 : now / 1000;
      let o = 0;
      const n = folds.length;
      for (let y = 0; y < H; y++) {
        const v = y / H;
        // la tela se mueve más abajo que arriba (está colgada arriba)
        const sway = v * v;
        const light = Math.exp(-v * 1.6) * 0.9 + 0.1;
        for (let k = 0; k < n; k++) {
          const f = folds[k];
          fxs[k] = f.x + Math.sin(t * f.s + f.p + v * 2.2) * 0.022 * sway + Math.sin(t * 0.21 + f.p) * 0.006;
        }
        for (let x = 0; x < W; x++) {
          const u = x / W;
          let b = 0;
          for (let k = 0; k < n; k++) {
            const dx = (u - fxs[k]) / folds[k].w;
            if (dx > -3 && dx < 3) b += Math.exp(-dx * dx);
          }
          const spot = spots[x]; // spot de luz arriba al centro, como un escenario
          let a = Math.min(1, b * 0.62) * light * spot * strength;
          a = a * 0.3 + spot * light * 0.05;
          const m = Math.min(1, a * 4);
          d[o++] = 255 - (255 - tint[0]) * 0.18 * m;
          d[o++] = 255 - (255 - tint[1]) * 0.18 * m;
          d[o++] = 255 - (255 - tint[2]) * 0.18 * m;
          d[o++] = a * 255;
        }
      }
      ctx.putImageData(img, 0, 0);
      if (!reduce) raf = requestAnimationFrame(frame);
    }

    if ("IntersectionObserver" in window) {
      new IntersectionObserver((es) => {
        intersecting = es[0].isIntersecting;
        if (!intersecting && raf) { cancelAnimationFrame(raf); raf = 0; }
        if (visible() && !raf) raf = requestAnimationFrame(frame);
      }).observe(canvas);
    }
    document.addEventListener("visibilitychange", () => {
      if (document.hidden && raf) { cancelAnimationFrame(raf); raf = 0; }
      if (visible() && !raf) raf = requestAnimationFrame(frame);
    });
    if (!("IntersectionObserver" in window)) { intersecting = true; raf = requestAnimationFrame(frame); }
  }

  document.querySelectorAll("canvas.curtains").forEach(start);
})();
