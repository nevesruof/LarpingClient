/* Small landing-page demos. Each interaction updates only its own section. */
(() => {
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    const running = new Set();
    const appearances = new IntersectionObserver(entries => {
      for (const [index, entry] of entries.entries()) {
        if (!entry.isIntersecting) continue;
        appearances.unobserve(entry.target);
        if (reducedMotion.matches || entry.target.contains(document.activeElement)) continue;
        const animation = entry.target.animate?.([
          { opacity: 0, transform: 'translateY(22px)' },
          { opacity: 1, transform: 'translateY(0)' }
        ], {
          duration: 620,
          delay: Math.min(index * 45, 135),
          fill: 'backwards',
          easing: 'cubic-bezier(.16,1,.3,1)'
        });
        if (animation) {
          running.add(animation);
          animation.onfinish = animation.oncancel = () => running.delete(animation);
        }
      }
    }, { threshold: .03, rootMargin: '0px 0px -20px 0px' });
    const blocks = [
      '.chapter-heading', '.section-head', '.show-frame', '.shortcut-strip',
      '.world-shot', '.style-lab', '.feature', '.explore-toolbar',
      '.explore-filters', '.explore-grid', '.detail-card', '.detail-guide',
      '.effect-layout', '.cos-strip', '.studio-layout', '.studio-tools',
      '.room-layout', '.session-layout', '.fair', '.field-note',
      '.release-intro', '.release-list', '.dl', '.faq',
      '.install-heading', '.install-requirements', '.install-step', '.install-footer'
    ];
    document.querySelectorAll(blocks.join(',')).forEach(block => appearances.observe(block));
    reducedMotion.addEventListener('change', event => {
      if (event.matches) for (const animation of running) animation.cancel();
    });
  }

  const studio = document.querySelector('[data-lyric-studio]');
  if (studio) {
    const scene = studio.querySelector('.studio-scene');
    const seek = studio.querySelector('#studio-seek');
    const time = studio.querySelector('[data-studio-time]');
    const lines = [...studio.querySelectorAll('.studio-lines li')];
    const layout = studio.querySelector('[data-studio-layout-select]');
    const font = studio.querySelector('[data-studio-font-select]');
    const color = studio.querySelector('[data-studio-accent]');
    const updateTime = () => {
      const seconds = Number(seek.value);
      const duration = Number(seek.max);
      const current = Math.min(lines.length - 1, Math.floor(seconds / duration * lines.length));
      time.textContent = `00:${String(seconds).padStart(2, '0')} / 00:${duration}`;
      seek.setAttribute('aria-valuetext', `${seconds} of ${duration} seconds`);
      lines.forEach((line, index) => {
        line.classList.toggle('is-current', index === current);
        if (index === current) line.setAttribute('aria-current', 'true');
        else line.removeAttribute('aria-current');
      });
    };
    const updateStyle = () => {
      scene.dataset.studioLayout = layout.value;
      scene.dataset.studioFont = font.value;
      scene.style.setProperty('--studio-ink', color.value);
    };
    seek.addEventListener('input', updateTime);
    [layout, font, color].forEach(control => control.addEventListener('input', updateStyle));
    updateTime();
    updateStyle();
  }

  const room = document.querySelector('[data-frame-room]');
  if (!room) return;
  const samples = {
    steady: {
      frames: [8, 8, 7, 9, 8, 8, 7, 8, 9, 8, 8, 9, 8, 10, 8, 7, 8, 9, 8, 8, 9, 7, 8, 8],
      note: 'Steady frames stay close together in this sample.'
    },
    busy: {
      frames: [9, 10, 8, 10, 11, 26, 13, 10, 9, 9, 13, 12, 20, 11, 9, 10, 28, 13, 10, 9, 10, 16, 10, 9],
      note: 'The median changes a little. The slowest frames take nearly three times as long.'
    }
  };
  const buttons = [...room.querySelectorAll('[data-frame-sample]')];
  const line = room.querySelector('[data-frame-line]');
  const area = room.querySelector('[data-frame-area]');
  const chart = room.querySelector('.room-chart');
  let animation;
  const render = (sample, animate = false) => {
    const { frames, note } = samples[sample];
    const sorted = [...frames].sort((a, b) => a - b);
    const middle = sorted.length / 2;
    const median = (sorted[middle - 1] + sorted[middle]) / 2;
    const p95 = sorted[Math.ceil(sorted.length * .95) - 1];
    const slowest = sorted.at(-1);
    const points = frames.map((ms, index) => `${(34 + index * 390 / (frames.length - 1)).toFixed(2)},${(143 - ms * 129 / 30).toFixed(2)}`);
    line.setAttribute('points', points.join(' '));
    area.setAttribute('d', `M34,143 L${points.join(' L')} L424,143 Z`);
    room.querySelector('[data-frame-median]').textContent = `${median.toFixed(1)} ms`;
    room.querySelector('[data-frame-p95]').textContent = `${p95.toFixed(1)} ms`;
    room.querySelector('[data-frame-max]').textContent = `${slowest.toFixed(1)} ms`;
    room.querySelector('[data-frame-note]').textContent = note;
    room.querySelector('[data-frame-description]').textContent = `${frames.length} sample frames from ${sorted[0]} to ${slowest} milliseconds. ${note}`;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.frameSample === sample)));
    animation?.cancel();
    if (animate && !reducedMotion.matches) animation = chart.animate?.([{ opacity: .55 }, { opacity: 1 }], { duration: 250 });
  };
  buttons.forEach(button => button.addEventListener('click', () => render(button.dataset.frameSample, true)));
  render('steady');
})();
