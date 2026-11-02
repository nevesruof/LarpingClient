/* Exclusive, interruptible FAQ transitions with native summary keyboard support. */
(() => {
  const root = document.querySelector('.faq');
  if (!root) return;
  const items = [...root.querySelectorAll('details')];
  const motions = new WeakMap();
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  root.classList.add('is-enhanced');

  function transition(item, expand) {
    const summary = item.querySelector('summary');
    const start = item.getBoundingClientRect().height;
    motions.get(item)?.cancel();
    item.style.height = '';
    if (expand) item.open = true;
    const borders = parseFloat(getComputedStyle(item).borderTopWidth) + parseFloat(getComputedStyle(item).borderBottomWidth);
    const end = expand ? item.getBoundingClientRect().height : summary.getBoundingClientRect().height + borders;
    item.dataset.expanded = String(expand);
    summary.setAttribute('aria-expanded', String(expand));
    const finish = () => {
      item.open = expand;
      item.style.height = '';
      item.style.overflow = '';
      motions.delete(item);
    };
    if (reduced.matches || !item.animate) { finish(); return; }
    item.style.height = `${start}px`;
    item.style.overflow = 'hidden';
    const motion = item.animate([{ height: `${start}px` }, { height: `${end}px` }], {
      duration: 300,
      easing: 'cubic-bezier(.16, 1, .3, 1)',
    });
    motions.set(item, motion);
    motion.onfinish = () => { finish(); motion.cancel(); };
  }

  items.forEach(item => {
    const summary = item.querySelector('summary');
    item.dataset.expanded = String(item.open);
    summary.setAttribute('aria-expanded', String(item.open));
    summary.addEventListener('click', event => {
      event.preventDefault();
      const expand = item.dataset.expanded !== 'true';
      items.forEach(other => {
        if (other !== item && other.dataset.expanded === 'true') transition(other, false);
      });
      transition(item, expand);
    });
    summary.addEventListener('keydown', event => {
      if (event.key === 'Escape' && item.dataset.expanded === 'true') transition(item, false);
    });
  });
})();
