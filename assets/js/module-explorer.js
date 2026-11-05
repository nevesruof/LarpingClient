/* Source-backed catalog. Loaded once, on approach or first interaction. */
(() => {
  const section = document.getElementById('modules');
  if (!section) return;
  const grid = section.querySelector('[data-explore-grid]');
  const search = section.querySelector('[data-explore-search]');
  const count = section.querySelector('[data-explore-count]');
  const more = section.querySelector('[data-explore-more]');
  const clear = section.querySelector('[data-explore-clear]');
  const fresh = section.querySelector('[data-explore-new]');
  const labels = {HUD:'HUD', PVP:'PvP', UTILITY:'Utility', VISUALS:'Visuals', COSMETICS:'Cosmetics', CLIENT:'Client'};
  let modules, pending, category = 'all', onlyNew = false, limit = 9, timer;
  const normalize = text => text.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const node = (tag, className, text) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
  };
  const icon = name => {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    const use = document.createElementNS(svg.namespaceURI, 'use');
    svg.setAttribute('class', 'ico'); svg.setAttribute('aria-hidden', 'true');
    use.setAttribute('href', '/assets/img/icons.svg#i-' + name); svg.append(use);
    return svg;
  };
  const card = module => {
    const link = node('a', 'explore-card');
    link.href = '/docs/modules#' + module.id;
    const top = node('span', 'explore-card-top');
    top.append(icon('modules'), node('small', '', labels[module.category]));
    if (module.new) top.append(node('span', 'new-badge', 'NEW'));
    const bottom = node('span', 'explore-card-bottom', module.settings.length + ' settings');
    const action = node('span', '', 'Explore'); action.append(icon('arrow')); bottom.append(action);
    link.append(top, node('h3', '', module.name), node('p', '', module.description), bottom);
    return link;
  };
  const render = () => {
    if (!modules) return;
    const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    const filtered = modules.filter(m => {
      const translated = window.LarpLocale ? normalize([m.name, m.description, ...m.settings.map(s => s.name)].map(window.LarpLocale.t).join(' ')) : '';
      return (category === 'all' || m.category === category) && (!onlyNew || m.new) && terms.every(t => (m.searchText + ' ' + translated).includes(t));
    });
    grid.replaceChildren(...filtered.slice(0, limit).map(card));
    count.textContent = filtered.length ? `Showing ${Math.min(limit, filtered.length)} of ${filtered.length} modules` : '0 modules found';
    more.hidden = limit >= filtered.length;
    clear.hidden = !search.value && category === 'all' && !onlyNew;
    section.querySelector('[data-explore-empty]').hidden = filtered.length > 0;
  };
  const load = () => {
    if (pending) return pending;
    count.textContent = 'Loading the module catalog…';
    pending = fetch('/assets/data/modules.json').then(response => {
      if (!response.ok) throw new Error('Catalog unavailable');
      return response.json();
    }).then(data => {
      if (!Array.isArray(data) || !data.length) throw new Error('Empty catalog');
      modules = data.map(m => ({...m, searchText:normalize([m.name, m.description, ...m.settings.map(s => s.name)].join(' '))}));
      render();
    }).catch(() => {
      pending = null;
      count.textContent = 'Catalog unavailable. You can still open the complete reference below.';
    });
    return pending;
  };
  const update = () => { limit = 9; if (modules) render(); else load(); };
  section.querySelectorAll('[data-explore-category]').forEach(button => button.addEventListener('click', () => {
    category = button.dataset.exploreCategory;
    section.querySelectorAll('[data-explore-category]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    update();
  }));
  search.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(update, 90); });
  search.addEventListener('focus', load);
  fresh.addEventListener('click', () => { onlyNew = !onlyNew; fresh.setAttribute('aria-pressed', String(onlyNew)); update(); });
  const reset = () => {
    search.value = ''; category = 'all'; onlyNew = false;
    fresh.setAttribute('aria-pressed', 'false');
    section.querySelectorAll('[data-explore-category]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.exploreCategory === 'all')));
    update();
  };
  clear.addEventListener('click', reset);
  section.querySelector('[data-explore-reset]').addEventListener('click', reset);
  more.addEventListener('click', () => {
    const previous = grid.children.length;
    limit += 9; render();
    grid.children[previous]?.focus({preventScroll:true});
  });
  document.addEventListener('larp:languagechange', () => { if (modules) render(); });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) { load(); observer.disconnect(); }
    }, {rootMargin:'350px'});
    observer.observe(section);
  } else load();
})();
