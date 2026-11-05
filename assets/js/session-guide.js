(() => {
  const guide = document.getElementById('first-session');
  if (!guide) return;
  const tasks = [...guide.querySelectorAll('[data-session-task]')];
  const key = 'larp-web-first-session-v1';
  const note = guide.querySelector('[data-session-note]');
  let storage = true;
  try {
    const saved = JSON.parse(localStorage.getItem(key) || '[]');
    if (Array.isArray(saved))
      tasks.forEach((t) => {
        t.checked = saved.includes(t.dataset.sessionTask);
      });
  } catch {
    storage = false;
  }
  const render = () => {
    const ready = tasks.filter((t) => t.checked).length;
    guide.querySelector('[data-session-progress]').textContent =
      ready === tasks.length
        ? 'All set. Make the session yours.'
        : `${ready} of ${tasks.length} ready`;
    guide.querySelector('[data-session-progress-bar]').style.width =
      (ready / tasks.length) * 100 + '%';
    note.textContent = storage
      ? ''
      : 'Checklist kept for this visit; browser storage is unavailable.';
  };
  const save = () => {
    if (storage)
      try {
        localStorage.setItem(
          key,
          JSON.stringify(tasks.filter((t) => t.checked).map((t) => t.dataset.sessionTask)),
        );
      } catch {
        storage = false;
      }
    render();
  };
  tasks.forEach((t) => t.addEventListener('change', save));
  guide.querySelector('[data-session-reset]').addEventListener('click', () => {
    tasks.forEach((t) => {
      t.checked = false;
    });
    save();
  });
  render();
})();
