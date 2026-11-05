/* Shared, on-demand navigation. The existing docs / shortcut stays intact. */
(() => {
  const dialog = document.querySelector('[data-quick-search]');
  if (!dialog || !dialog.showModal) return;
  const input = dialog.querySelector('[data-quick-input]');
  const results = dialog.querySelector('[data-quick-results]');
  const count = dialog.querySelector('[data-quick-count]');
  const initial = [...results.children].map(el => el.cloneNode(true));
  const extra = [
    {t:'Module explorer', u:'/#modules', x:'Search the client catalog'},
    {t:'Style lab', u:'/#style-lab', x:'Try accents, scale and layout'},
    {t:'Lyric studio', u:'/#studio', x:'Preview lyrics, typography and a sample timeline'},
    {t:'Performance room', u:'/#performance-room', x:'Compare frame times and slow frames'},
    {t:'Kill Efects preview', u:'/#kill-effects', x:'Samurai and Tralalero'},
    {t:'First session checklist', u:'/#first-session', x:'A short list for your setup'},
    {t:'Gallery', u:'/#gallery', x:'From menu to world'},
    {t:'Get access', u:'/#access', x:'Private client access from iTake'},
  ];
  let index, pending, timer;
  const normalize = text => text.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const render = () => {
    const query = normalize(input.value.trim());
    if (!query) { results.replaceChildren(...initial.map(el => el.cloneNode(true))); count.textContent = 'Quick links'; return; }
    if (!index) { results.replaceChildren(); count.textContent = 'Loading the search index…'; return; }
    const terms = query.split(/\s+/);
    const matches = index.filter(item => {
      const translated = window.LarpLocale ? normalize(window.LarpLocale.t(item.t) + ' ' + window.LarpLocale.t(item.x)) : '';
      return terms.every(t => (item.searchText + ' ' + translated).includes(t));
    }).sort((a, b) => Number(normalize(b.t).startsWith(query)) - Number(normalize(a.t).startsWith(query))).slice(0, 8);
    count.textContent = matches.length ? `${matches.length} results · pages, modules and settings` : 'No results. Try a module name or a shorter search.';
    results.replaceChildren(...matches.map(item => {
      const a = document.createElement('a'); a.href = item.u;
      const label = document.createElement('span'); label.textContent = item.t;
      const sub = document.createElement('small'); sub.textContent = item.x; label.append(sub); a.append(label);
      return a;
    }));
  };
  const load = () => {
    if (pending) return;
    pending = fetch('/assets/data/search.json').then(r => { if (!r.ok) throw new Error(); return r.json(); }).then(data => {
      index = [...extra, ...data].map(item => ({...item, searchText:normalize([item.t, item.x, item.k || ''].join(' '))}));
      render();
    }).catch(() => { pending = null; index = extra.map(item => ({...item, searchText:normalize(item.t + ' ' + item.x)})); render(); });
  };
  const open = () => {
    if (dialog.open) return;
    document.querySelector('.mobile-menu')?.classList.remove('open');
    document.querySelector('.nav-toggle')?.setAttribute('aria-expanded', 'false');
    dialog.showModal(); input.focus(); load();
  };
  document.querySelectorAll('[data-search-open]').forEach(button => button.addEventListener('click', open));
  dialog.querySelector('[data-search-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', e => {
    if (e.target.closest('a')) dialog.close();
    else if (e.target === dialog) {
      const r = dialog.getBoundingClientRect();
      if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close();
    }
  });
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); if (dialog.open) dialog.close(); else open(); }
  });
  input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(render, 70); });
  document.addEventListener('larp:languagechange', () => { if (dialog.open) render(); });
  dialog.addEventListener('keydown', e => {
    // Flush pending input before keyboard navigation can activate an older result.
    if (e.target === input && ['ArrowDown', 'ArrowUp', 'Enter'].includes(e.key)) {
      clearTimeout(timer);
      render();
    }
    const links = [...results.querySelectorAll('a')];
    const current = links.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); (links[current + 1] || links[0] || input).focus(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); (current <= 0 ? input : links[current - 1]).focus(); }
    if (e.key === 'Enter' && e.target === input && links[0]) { e.preventDefault(); links[0].click(); }
  });
})();
