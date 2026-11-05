(() => {
  const faq = document.querySelector('.faq');
  if (!faq) return;

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const panels = [...faq.querySelectorAll('details')].map((item) => ({
    item,
    summary: item.querySelector('summary'),
    answer: item.querySelector('.faq-answer-wrap'),
    expanded: item.open,
    closeTimer: 0,
  }));
  const panelBySummary = new Map(panels.map((panel) => [panel.summary, panel]));

  function finishClosing(panel) {
    clearTimeout(panel.closeTimer);
    if (!panel.expanded) panel.item.open = false;
  }

  function setExpanded(panel, expanded) {
    clearTimeout(panel.closeTimer);
    panel.expanded = expanded;
    panel.summary.setAttribute('aria-expanded', String(expanded));
    panel.answer.inert = !expanded;
    panel.answer.setAttribute('aria-hidden', String(!expanded));

    if (expanded && !panel.item.open) {
      panel.item.open = true;
      if (!reducedMotion.matches) void panel.answer.offsetHeight;
    }
    panel.item.dataset.expanded = String(expanded);

    if (!expanded) {
      if (reducedMotion.matches) finishClosing(panel);
      else panel.closeTimer = setTimeout(() => finishClosing(panel), 280);
    }
  }

  panels.forEach((panel) => {
    panel.item.dataset.expanded = String(panel.expanded);
    panel.summary.setAttribute('aria-expanded', String(panel.expanded));
    panel.answer.inert = !panel.expanded;
    panel.answer.setAttribute('aria-hidden', String(!panel.expanded));
    panel.answer.addEventListener('transitionend', (event) => {
      if (event.target === panel.answer && event.propertyName === 'grid-template-rows')
        finishClosing(panel);
    });
  });
  faq.classList.add('is-enhanced');

  faq.addEventListener('click', (event) => {
    const panel = panelBySummary.get(event.target.closest('summary'));
    if (!panel) return;
    event.preventDefault();
    const expanded = !panel.expanded;
    if (expanded)
      panels.forEach((other) => {
        if (other !== panel && other.expanded) setExpanded(other, false);
      });
    setExpanded(panel, expanded);
  });

  faq.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    const panel = panelBySummary.get(event.target.closest('summary'));
    if (panel?.expanded) setExpanded(panel, false);
  });

  reducedMotion.addEventListener('change', (event) => {
    if (event.matches) panels.forEach(finishClosing);
  });
})();
