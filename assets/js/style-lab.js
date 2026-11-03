/* Design values affect only this preview. Copying never imports a game profile. */
(() => {
  const lab = document.querySelector('[data-style-lab]');
  if (!lab) return;
  const color = lab.querySelector('[data-lab-color]');
  const scale = lab.querySelector('[data-lab-scale]');
  const compact = lab.querySelector('[data-lab-compact]');
  const coords = lab.querySelector('[data-lab-coords]');
  const status = lab.querySelector('[data-lab-status]');
  const fallback = lab.querySelector('[data-lab-fallback]');
  const copy = lab.querySelector('[data-lab-copy]');
  let accent = color.value, busy = false;
  const update = () => {
    lab.style.setProperty('--lab-accent', accent);
    lab.style.setProperty('--lab-scale', Number(scale.value) / 100);
    lab.classList.toggle('is-compact', compact.checked);
    lab.querySelector('[data-lab-coordinates]').hidden = !coords.checked;
    lab.querySelector('[data-lab-hex]').textContent = accent.toUpperCase();
    lab.querySelector('[data-lab-scale-label]').textContent = scale.value + '%';
    lab.querySelectorAll('[data-lab-accent]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.labAccent === accent)));
    fallback.hidden = true;
    status.textContent = 'Preview only. Apply your choices in the client.';
  };
  lab.querySelectorAll('[data-lab-accent]').forEach(button => button.addEventListener('click', () => { accent = button.dataset.labAccent; color.value = accent; update(); }));
  color.addEventListener('input', () => { accent = color.value; update(); });
  [scale, compact, coords].forEach(el => el.addEventListener('input', update));
  lab.querySelector('[data-lab-reset]').addEventListener('click', () => { accent = '#b5a3e8'; color.value = accent; scale.value = '100'; compact.checked = false; coords.checked = true; update(); });
  copy.addEventListener('click', async () => {
    if (busy) return;
    busy = true; copy.disabled = true;
    const text = `larp. style notes\nAccent: ${accent.toUpperCase()}\nScale: ${scale.value}%\nCompact: ${compact.checked ? 'On' : 'Off'}\nCoordinates: ${coords.checked ? 'On' : 'Off'}\nWebsite preview values; apply manually in the client.`;
    try { await navigator.clipboard.writeText(text); status.textContent = 'Style notes copied. Make them yours in the client.'; }
    catch { fallback.value = text; fallback.hidden = false; fallback.focus(); fallback.select(); status.textContent = 'Select and copy the style notes below.'; }
    finally { busy = false; copy.disabled = false; }
  });
})();
