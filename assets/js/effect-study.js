/* One short animation per request, never a background render loop. */
(() => {
  const study = document.querySelector('[data-effect-study]');
  if (!study) return;
  const play = study.querySelector('[data-effect-play]');
  const result = study.querySelector('[data-effect-result]');
  const description = document.querySelector('[data-effect-description]');
  const effects = {
    samurai: { name: 'Samurai', description: 'A sharp cut. A brief burst. Then back to the game.', duration: 1300 },
    tralalero: { name: 'Tralalero', description: 'A shadow approaches, lands one clean bite and slips back into the dark.', duration: 1720 }
  };
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let timer;
  const stop = () => { clearTimeout(timer); study.classList.remove('is-playing'); play.disabled = false; };
  document.querySelectorAll('[data-effect]').forEach(button => button.addEventListener('click', () => {
    stop(); study.dataset.effectMode = button.dataset.effect;
    const effect = effects[button.dataset.effect];
    study.querySelector('[data-effect-caption]').textContent = effect.name.toUpperCase();
    description.textContent = effect.description;
    result.textContent = '';
    document.querySelectorAll('[data-effect]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  }));
  play.addEventListener('click', () => {
    if (play.disabled) return;
    play.disabled = true; study.classList.add('is-playing');
    const effect = effects[study.dataset.effectMode];
    result.textContent = reduced.matches ? `${effect.name} selected. Motion reduced.` : `Playing ${effect.name} preview.`;
    timer = setTimeout(() => {
      stop();
      result.textContent = `${effect.name} preview ready to replay.`;
    }, reduced.matches ? 650 : effect.duration + 60);
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => { if (!entries[0].isIntersecting) stop(); }).observe(study);
})();
