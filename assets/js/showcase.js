/* Small, local demonstrations. No network requests or animation loops. */
(() => {
  const shulker = document.querySelector('[data-shulker-demo]');
  const colors = {
    white: ['#d1d3de', '#a2a6b3', '#30313e', 'White Shulker Box'],
    purple: ['#8672aa', '#665484', '#211b30', 'Purple Shulker Box'],
    lime: ['#acbf82', '#82965c', '#26351a', 'Lime Shulker Box'],
  };
  document.querySelectorAll('[data-shulker-color]').forEach(button => {
    button.addEventListener('click', () => {
      if (!shulker) return;
      const [box, slot, ink, name] = colors[button.dataset.shulkerColor];
      shulker.style.setProperty('--box', box);
      shulker.style.setProperty('--slot', slot);
      shulker.style.setProperty('--ink', ink);
      shulker.querySelector('[data-shulker-name]').textContent = name;
      document.querySelectorAll('[data-shulker-color]').forEach(b => b.setAttribute('aria-pressed', b === button));
    });
  });

  const setup = document.querySelector('[data-setup-demo]');
  const profiles = {
    focus: ['Focus', '#9aa8ff', ['Keystrokes', 'Target HUD', 'Toggle Sprint'], 'Just the information you need for the next fight.'],
    'after-dark': ['After dark', '#c4a2f6', ['Aurora sky', 'Music Beats', 'Wings'], 'Bring back the atmosphere when the match is over.'],
    creator: ['Creator', '#8acbb7', ['Instant Replay', 'Recorder', 'Lyrics'], 'Your soundtrack, your point of view, your next clip.'],
  };
  document.querySelectorAll('[data-setup]').forEach(button => {
    button.addEventListener('click', () => {
      if (!setup) return;
      const [name, accent, modules, description] = profiles[button.dataset.setup];
      setup.style.setProperty('--setup-accent', accent);
      setup.querySelector('.setup-status').textContent = name;
      setup.querySelector('[data-setup-description]').textContent = description;
      setup.querySelector('[data-setup-mods]').replaceChildren(...modules.map(label => {
        const span = document.createElement('span');
        span.textContent = label;
        return span;
      }));
      document.querySelectorAll('[data-setup]').forEach(b => b.setAttribute('aria-pressed', b === button));
    });
  });

  document.querySelectorAll('[data-open-preview]').forEach(link => {
    link.addEventListener('click', () => document.getElementById(link.dataset.openPreview)?.click());
  });
})();
