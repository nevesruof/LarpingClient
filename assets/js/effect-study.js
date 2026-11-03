/* One short animation per request, never a background render loop. */
(() => {
  const study = document.querySelector('[data-effect-study]');
  if (!study) return;
  const play = study.querySelector('[data-effect-play]');
  const result = study.querySelector('[data-effect-result]');
  const description = document.querySelector('[data-effect-description]');
  const labels = {samurai:['Samurai', 'A sharp cut. A brief burst. Then back to the game.'], tralalero:['Tralalero', 'An unexpected visitor. One bite. A little less serious.']};
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let timer;
  const stop = () => { clearTimeout(timer); study.classList.remove('is-playing'); play.disabled = false; };
  document.querySelectorAll('[data-effect]').forEach(button => button.addEventListener('click', () => {
    stop(); study.dataset.effectMode = button.dataset.effect;
    const [label, text] = labels[button.dataset.effect];
    study.querySelector('[data-effect-caption]').textContent = label.toUpperCase(); description.textContent = text;
    result.textContent = '';
    document.querySelectorAll('[data-effect]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  }));
  play.addEventListener('click', () => {
    if (play.disabled) return;
    play.disabled = true; study.classList.add('is-playing');
    result.textContent = labels[study.dataset.effectMode][0] + (reduced.matches ? ' selected. Motion reduced.' : ' preview played.');
    timer = setTimeout(stop, reduced.matches ? 650 : 1400);
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => { if (!entries[0].isIntersecting) stop(); }).observe(study);
})();
