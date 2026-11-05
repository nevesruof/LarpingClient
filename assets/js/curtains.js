(() => {
  const width = 220;
  const height = 124;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const scenes = new Map();

  function createScene(canvas) {
    canvas.width = width;
    canvas.height = height;
    const context = canvas.getContext('2d', { alpha: true });
    if (!context) return null;
    const image = context.createImageData(width, height);
    const pixels = image.data;
    const tint = (canvas.dataset.tint || '108,123,255').split(',').map(Number);
    const strength = parseFloat(canvas.dataset.strength || '1');
    const folds = Array.from({ length: 15 }, (_, index) => ({
      x: (index + 0.5) / 15 + Math.sin(index * 12.9898) * 0.5 * 0.03,
      width: 0.018 + ((index * 7) % 5) * 0.004,
      phase: index * 1.7,
      speed: 0.35 + ((index * 3) % 4) * 0.08,
      stride: 1 / (width * (0.018 + ((index * 7) % 5) * 0.004)),
    }));
    folds.forEach((fold) => {
      fold.ratioChange = Math.exp(-2 * fold.stride * fold.stride);
    });
    const centers = new Float32Array(folds.length);
    const offsets = new Float64Array(folds.length);
    const brightness = new Float64Array(width);
    const positions = new Float64Array(width);
    const spotlight = new Float32Array(width);
    const rowLight = new Float64Array(height);
    const rowSway = new Float64Array(height);
    let visible = false;
    let frameId = 0;
    let lastFrame = 0;

    for (let x = 0; x < width; x++) {
      positions[x] = x / width;
      const center = (x / width - 0.5) * 1.5;
      spotlight[x] = Math.exp(-(center * center) * 2.2);
    }
    for (let y = 0; y < height; y++) {
      const position = y / height;
      rowLight[y] = Math.exp(-position * 1.6) * 0.9 + 0.1;
      rowSway[y] = position * position;
    }

    function draw(time) {
      let pixel = 0;
      folds.forEach((fold, index) => {
        offsets[index] = Math.sin(time * 0.21 + fold.phase) * 0.006;
      });
      for (let y = 0; y < height; y++) {
        const position = y / height;
        const light = rowLight[y];
        brightness.fill(0);
        folds.forEach((fold, index) => {
          centers[index] =
            fold.x +
            Math.sin(time * fold.speed + fold.phase + position * 2.2) * 0.022 * rowSway[y] +
            offsets[index];
          const first = Math.max(0, Math.floor((centers[index] - fold.width * 3) * width));
          const last = Math.min(width, Math.ceil((centers[index] + fold.width * 3) * width));
          const start = (positions[first] - centers[index]) / fold.width;
          let value = Math.exp(-start * start);
          let ratio = Math.exp(-2 * start * fold.stride - fold.stride * fold.stride);
          for (let x = first; x < last; x++) {
            const distance = (positions[x] - centers[index]) / fold.width;
            if (distance > -3 && distance < 3) brightness[x] += value;
            value *= ratio;
            ratio *= fold.ratioChange;
          }
        });
        for (let x = 0; x < width; x++) {
          const spot = spotlight[x];
          let alpha = Math.min(1, brightness[x] * 0.62) * light * spot * strength;
          alpha = alpha * 0.3 + spot * light * 0.05;
          const mix = Math.min(1, alpha * 4);
          pixels[pixel++] = 255 - (255 - tint[0]) * 0.18 * mix;
          pixels[pixel++] = 255 - (255 - tint[1]) * 0.18 * mix;
          pixels[pixel++] = 255 - (255 - tint[2]) * 0.18 * mix;
          pixels[pixel++] = alpha * 255;
        }
      }
      context.putImageData(image, 0, 0);
    }

    function frame(now) {
      frameId = 0;
      if (!visible || document.hidden) return;
      if (!reducedMotion.matches && now - lastFrame < 67) {
        frameId = requestAnimationFrame(frame);
        return;
      }
      lastFrame = now;
      draw(reducedMotion.matches ? 0 : now / 1000);
      if (!reducedMotion.matches) frameId = requestAnimationFrame(frame);
    }

    function update() {
      if ((!visible || document.hidden) && frameId) {
        cancelAnimationFrame(frameId);
        frameId = 0;
      }
      if (visible && !document.hidden && !frameId) frameId = requestAnimationFrame(frame);
    }
    return {
      update,
      setVisible(next) {
        visible = next;
        update();
      },
    };
  }

  document.querySelectorAll('canvas.curtains').forEach((canvas) => {
    const scene = createScene(canvas);
    if (scene) scenes.set(canvas, scene);
  });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => scenes.get(entry.target)?.setVisible(entry.isIntersecting));
    });
    scenes.forEach((_, canvas) => observer.observe(canvas));
  } else scenes.forEach((scene) => scene.setVisible(true));
  document.addEventListener('visibilitychange', () => scenes.forEach((scene) => scene.update()));
  reducedMotion.addEventListener('change', () => scenes.forEach((scene) => scene.update()));
})();
