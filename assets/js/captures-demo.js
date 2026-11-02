/* A bounded local gallery demonstration; it never captures or exports media. */
(() => {
  const desk = document.querySelector('[data-capture-demo]');
  if (!desk) return;
  const button = desk.querySelector('[data-save-demo]');
  const files = desk.querySelector('[data-capture-files]');
  const count = desk.querySelector('[data-capture-count]');
  const status = desk.querySelector('[data-capture-status]');
  let sequence = 1, reset;

  function save() {
    if (button.disabled) return;
    clearTimeout(reset);
    button.disabled = true;
    button.setAttribute('aria-busy', 'true');
    desk.classList.add('is-saving');
    status.textContent = 'Preparing your sample clip…';
    setTimeout(() => {
      const row = files.lastElementChild.cloneNode(true);
      row.querySelector('b').textContent = `Clip-${++sequence}.mp4`;
      row.classList.add('capture-file-new');
      files.prepend(row);
      while (files.children.length > 3) files.lastElementChild.remove();
      count.textContent = `${files.children.length} clips`;
      desk.classList.remove('is-saving');
      desk.classList.add('sample-saved');
      status.textContent = `Clip-${sequence}.mp4 added to this demo gallery.`;
      button.disabled = false;
      button.removeAttribute('aria-busy');
      reset = setTimeout(() => {
        desk.classList.remove('sample-saved');
        status.textContent = 'Try saving a sample. No recording takes place.';
      }, 3200);
    }, matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 500);
  }
  button.addEventListener('click', save);
  desk.addEventListener('keydown', event => {
    if (event.key === 'F8') { event.preventDefault(); save(); }
  });
})();
