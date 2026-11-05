(() => {
  document.querySelectorAll('.hud-scene').forEach((scene) => {
    const widgets = [...scene.querySelectorAll('.hud-el')];
    const vertical = scene.querySelector('.guide.v');
    const horizontal = scene.querySelector('.guide.h');
    const hint = scene.querySelector('.hud-hint');
    const controls = scene.nextElementSibling;
    const status = controls?.querySelector('[data-hud-status]');
    const moved = new Set();
    let active = null;

    function bounds(widget) {
      const box = widget.getBoundingClientRect();
      const area = scene.getBoundingClientRect();
      return { x: box.left - area.left, y: box.top - area.top, w: box.width, h: box.height };
    }
    function place(widget, x, y, snap = false) {
      const { w, h } = bounds(widget);
      let vx = null,
        hy = null;
      if (snap) {
        const xs = [scene.clientWidth / 2];
        const ys = [scene.clientHeight / 2];
        for (const other of widgets)
          if (other !== widget) {
            const b = bounds(other);
            xs.push(b.x, b.x + b.w);
            ys.push(b.y, b.y + b.h);
          }
        for (const line of xs) {
          const anchor = [x, x + w / 2, x + w].find((value) => Math.abs(value - line) < 5);
          if (anchor !== undefined) {
            x += line - anchor;
            vx = line;
            break;
          }
        }
        for (const line of ys) {
          const anchor = [y, y + h / 2, y + h].find((value) => Math.abs(value - line) < 5);
          if (anchor !== undefined) {
            y += line - anchor;
            hy = line;
            break;
          }
        }
      }
      x = Math.max(4, Math.min(Math.max(4, scene.clientWidth - w - 4), x));
      y = Math.max(4, Math.min(Math.max(4, scene.clientHeight - h - 4), y));
      Object.assign(widget.style, {
        left: `${x}px`,
        top: `${y}px`,
        right: 'auto',
        bottom: 'auto',
        transform: 'none',
      });
      vertical.classList.toggle('show', vx !== null);
      horizontal.classList.toggle('show', hy !== null);
      if (vx !== null) vertical.style.left = `${vx}px`;
      if (hy !== null) horizontal.style.top = `${hy}px`;
      moved.add(widget);
      if (hint) hint.hidden = true;
    }
    function finish(event) {
      if (!active || (event && event.pointerId !== active.id)) return;
      const { widget, id, frame } = active;
      if (frame) cancelAnimationFrame(frame);
      if (frame && event?.type === 'pointerup') {
        const area = scene.getBoundingClientRect();
        place(
          widget,
          event.clientX - area.left - active.dx,
          event.clientY - area.top - active.dy,
          true,
        );
      }
      widget.classList.remove('drag');
      scene.classList.remove('dragging');
      vertical.classList.remove('show');
      horizontal.classList.remove('show');
      active = null;
      if (widget.hasPointerCapture(id)) widget.releasePointerCapture(id);
      if (status) status.textContent = 'Widget placed. Use Reset layout to start again.';
    }
    widgets.forEach((widget) => {
      widget.addEventListener('dragstart', (event) => event.preventDefault());
      widget.addEventListener('pointerdown', (event) => {
        if (!event.isPrimary || event.button !== 0 || active) return;
        event.preventDefault();
        widget.focus({ preventScroll: true });
        const box = widget.getBoundingClientRect();
        active = {
          widget,
          id: event.pointerId,
          dx: event.clientX - box.left,
          dy: event.clientY - box.top,
          frame: 0,
        };
        widget.setPointerCapture(event.pointerId);
        widget.classList.add('drag');
        scene.classList.add('dragging');
      });
      widget.addEventListener('pointermove', (event) => {
        if (!active || active.widget !== widget || event.pointerId !== active.id) return;
        active.x = event.clientX;
        active.y = event.clientY;
        if (active.frame) return;
        active.frame = requestAnimationFrame(() => {
          if (!active) return;
          active.frame = 0;
          const area = scene.getBoundingClientRect();
          place(widget, active.x - area.left - active.dx, active.y - area.top - active.dy, true);
        });
      });
      ['pointerup', 'pointercancel', 'lostpointercapture'].forEach((type) =>
        widget.addEventListener(type, finish),
      );
      widget.addEventListener('keydown', (event) => {
        const delta = {
          ArrowLeft: [-1, 0],
          ArrowRight: [1, 0],
          ArrowUp: [0, -1],
          ArrowDown: [0, 1],
        }[event.key];
        if (!delta) return;
        event.preventDefault();
        const b = bounds(widget),
          step = event.shiftKey ? 10 : 1;
        place(widget, b.x + delta[0] * step, b.y + delta[1] * step);
        if (status)
          status.textContent = `Position ${Math.round(parseFloat(widget.style.left))}, ${Math.round(parseFloat(widget.style.top))}.`;
      });
    });
    controls?.querySelector('[data-hud-reset]')?.addEventListener('click', () => {
      finish();
      widgets.forEach((widget) => widget.removeAttribute('style'));
      moved.clear();
      if (hint) hint.hidden = false;
      if (status) status.textContent = 'Default HUD layout restored.';
    });
    new ResizeObserver(() => {
      if (!scene.clientWidth || active) return;
      moved.forEach((widget) => {
        const b = bounds(widget);
        place(widget, b.x, b.y);
      });
    }).observe(scene);
  });
})();
