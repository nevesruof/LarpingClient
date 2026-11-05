/* Local translations, including content added by the interactive previews. */
(() => {
  const picker = document.querySelector('[data-language-picker]');
  if (!picker) return;
  const toggle = picker.querySelector('[data-language-toggle]');
  const menu = picker.querySelector('.language-menu');
  const options = [...menu.querySelectorAll('[data-language-option]')];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const texts = new WeakMap(), attributes = new WeakMap();
  const ignored = 'script,style,svg,code,kbd,pre,[translate="no"],[data-language-picker]';
  const translatableAttributes = ['aria-label', 'placeholder', 'title', 'alt'];
  let language = 'en', dictionary = {}, ready = false, motion, expanded = false;
  try { if (localStorage.getItem('larp-web-language') === 'es') language = 'es'; } catch {}

  const rules = [
    [/^Showing (\d+) of (\d+) modules$/, (_, a, b) => `Mostrando ${a} de ${b} módulos`],
    [/^(\d+) settings$/, (_, n) => `${n} ${n === '1' ? 'ajuste' : 'ajustes'}`],
    [/^(\d+) modules(?: · (\d+) enabled)?$/, (_, n, on) => `${n} módulos${on === undefined ? '' : ` · ${on} activos`}`],
    [/^(\d+) modules active$/, (_, n) => `${n} módulos activos`],
    [/^(\d+) active · web preview$/, (_, n) => `${n} activos · vista previa web`],
    [/^(\d+) modules? · browser preview$/, (_, n) => `${n} módulos · vista previa web`],
    [/^(\d+) of (\d+) modules$/, (_, n, total) => `${n} de ${total} módulos`],
    [/^(\d+) of (\d+) ready$/, (_, n, total) => `${n} de ${total} listos`],
    [/^(\d+) results · pages, modules and settings$/, (_, n) => `${n} resultados · páginas, módulos y ajustes`],
    [/^(\d+) clips?$/, (_, n) => `${n} ${n === '1' ? 'clip' : 'clips'}`],
    [/^Position ([-\d]+), ([-\d]+)\.$/, (_, x, y) => `Posición ${x}, ${y}.`],
    [/^(\d+) of (\d+) seconds$/, (_, n, total) => `${n} de ${total} segundos`],
    [/^Profile (\d+)$/, (_, n) => `Perfil ${n}`],
    [/^Profile (\d+) (deleted|saved|loaded) in this browser preview\.$/, (_, n, action) => `Perfil ${n} ${ {deleted:'eliminado',saved:'guardado',loaded:'cargado'}[action] } en esta vista previa.`],
    [/^(Tralalero|Samurai) is the only selected animation in this preview\.$/, (_, name) => `${name} es la única animación seleccionada en esta vista previa.`],
    [/^Toggle (.+) preview$/, (_, name) => `Activar o desactivar ${dictionary[name] || name} en la vista previa`],
    [/^(.+) settings$/, (_, name) => `Ajustes de ${dictionary[name] || name}`],
    [/^Playing (Tralalero|Samurai) preview\.$/, (_, name) => `Reproduciendo la vista previa de ${name}.`],
    [/^(Tralalero|Samurai) preview ready to replay\.$/, (_, name) => `La vista previa de ${name} está lista para repetirse.`],
    [/^(Tralalero|Samurai) selected\. Motion reduced\.$/, (_, name) => `${name} seleccionado. Movimiento reducido.`],
    [/^(Clip-\d+\.mp4) added to this demo gallery\.$/, (_, name) => `${name} añadido a esta galería de ejemplo.`],
    [/^No results for “(.+)”\.$/, (_, query) => `No hay resultados para «${query}».`],
    [/^(\d+) sample frames from (\d+) to (\d+) milliseconds\. (.+)$/, (_, n, min, max, note) => `${n} fotogramas de ejemplo entre ${min} y ${max} milisegundos. ${dictionary[note] || note}`],
    [/^(.+) — larp\.$/, (_, title) => `${dictionary[title] || title} — larp.`],
  ];
  function translate(value) {
    if (language !== 'es' || !ready || !value) return value;
    const source = value.trim();
    let result = dictionary[source];
    if (result === undefined) for (const [pattern, replace] of rules) {
      if (pattern.test(source)) { result = source.replace(pattern, replace); break; }
    }
    if (result === undefined && source.includes(' · ')) result = source.split(' · ').map(part => dictionary[part] || part).join(' · ');
    if (result === undefined) return value;
    return value.replace(source, result);
  }
  window.LarpLocale = { t: translate, get language() { return language; } };

  function translateText(node) {
    if (!node.parentElement || node.parentElement.closest(ignored) || !node.data.trim()) return;
    let record = texts.get(node);
    if (!record || node.data !== record.last) record = { source: node.data, last: node.data };
    const value = translate(record.source);
    record.last = value;
    texts.set(node, record);
    if (node.data !== value) node.data = value;
  }
  function translateAttributes(element) {
    if (element.closest(ignored)) return;
    const record = attributes.get(element) || {};
    for (const name of translatableAttributes) {
      const value = element.getAttribute(name);
      if (!value) continue;
      if (!record[name] || record[name].last !== value) record[name] = { source: value, last: value };
      const localized = translate(record[name].source);
      record[name].last = localized;
      if (value !== localized) element.setAttribute(name, localized);
    }
    attributes.set(element, record);
  }
  function translateTree(root) {
    if (root.nodeType === Node.TEXT_NODE) { translateText(root); return; }
    if (root.nodeType !== Node.ELEMENT_NODE || root.closest(ignored)) return;
    translateAttributes(root);
    root.querySelectorAll('[aria-label],[placeholder],[title],[alt]').forEach(translateAttributes);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) translateText(walker.currentNode);
  }
  const pending = new Set();
  let scheduled = false;
  new MutationObserver(records => {
    if (!ready) return;
    for (const record of records) {
      if (record.type === 'characterData') pending.add(record.target);
      else if (record.type === 'attributes') pending.add(record.target);
      else record.addedNodes.forEach(node => pending.add(node));
    }
    if (scheduled || !pending.size) return;
    scheduled = true;
    queueMicrotask(() => {
      scheduled = false;
      const batch = [...pending]; pending.clear();
      batch.filter(node => node.isConnected).forEach(translateTree);
    });
  }).observe(document.body, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: translatableAttributes });

  function setExpanded(open, restoreFocus = false) {
    expanded = open;
    motion?.cancel();
    toggle.setAttribute('aria-expanded', String(open));
    menu.inert = !open;
    if (open) menu.hidden = false;
    if (restoreFocus) toggle.focus({ preventScroll: true });
    const finish = () => { if (!expanded) menu.hidden = true; };
    if (reduced.matches || !menu.animate) { finish(); return; }
    motion = menu.animate(open ? [
      { opacity: 0, transform: 'translateY(-7px) scale(.98)' },
      { opacity: 1, transform: 'translateY(0) scale(1)' }
    ] : [
      { opacity: 1, transform: 'translateY(0) scale(1)' },
      { opacity: 0, transform: 'translateY(-5px) scale(.985)' }
    ], { duration: open ? 220 : 150, easing: 'cubic-bezier(.16,1,.3,1)' });
    motion.onfinish = finish;
  }
  function applyLanguage(next, persist = true) {
    language = next === 'es' ? 'es' : 'en';
    document.documentElement.lang = language;
    if (persist) try { localStorage.setItem('larp-web-language', language); } catch {}
    const flag = toggle.querySelector('[data-language-flag]');
    flag.src = language === 'es' ? '/assets/img/flag-es.svg' : '/assets/img/flag-us.svg';
    picker.querySelector('[data-language-current]').textContent = language === 'es' ? 'Español' : 'English';
    toggle.setAttribute('aria-label', language === 'es' ? 'Elegir idioma: español' : 'Choose language: English');
    options.forEach(option => option.setAttribute('aria-checked', String(option.dataset.languageOption === language)));
    translateTree(document.body);
    const title = document.querySelector('title');
    if (title?.firstChild) translateText(title.firstChild);
    document.dispatchEvent(new CustomEvent('larp:languagechange', { detail: { language } }));
  }
  toggle.addEventListener('click', () => setExpanded(!expanded));
  toggle.addEventListener('keydown', event => {
    if (!['ArrowDown', 'ArrowUp'].includes(event.key)) return;
    event.preventDefault(); setExpanded(true);
    options[event.key === 'ArrowDown' ? 0 : options.length - 1].focus();
  });
  options.forEach(option => option.addEventListener('click', () => {
    if (option.dataset.languageOption === 'es' && !ready) return;
    applyLanguage(option.dataset.languageOption);
    setExpanded(false, true);
  }));
  menu.addEventListener('keydown', event => {
    const index = options.indexOf(document.activeElement);
    if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
      event.preventDefault();
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? options.length - 1 : (index + (event.key === 'ArrowDown' ? 1 : options.length - 1)) % options.length;
      options[next].focus();
    }
  });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && expanded) setExpanded(false, true); });
  document.addEventListener('pointerdown', event => { if (expanded && !picker.contains(event.target)) setExpanded(false); });
  picker.addEventListener('focusout', event => { if (expanded && !picker.contains(event.relatedTarget)) setExpanded(false); });
  window.addEventListener('storage', event => { if (event.key === 'larp-web-language') applyLanguage(event.newValue, false); });
  fetch('/assets/data/es.json').then(response => { if (!response.ok) throw new Error(); return response.json(); }).then(data => {
    dictionary = data; ready = true; applyLanguage(language, false);
  }).catch(() => { language = 'en'; applyLanguage('en', false); options[1].disabled = true; });

  // Native cross-document transitions handle supported browsers. Fade only for
  // ordinary same-tab navigation in the fallback; never intercept reload/close.
  document.addEventListener('click', event => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || reduced.matches || 'onpageswap' in window) return;
    const link = event.target.closest('a[href]');
    if (!link || link.target || link.hasAttribute('download')) return;
    const target = new URL(link.href);
    if (!['http:', 'https:'].includes(target.protocol) || (target.origin === location.origin && target.pathname === location.pathname && target.search === location.search)) return;
    event.preventDefault();
    document.body.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 140 }).finished.then(() => location.assign(target.href));
  });
  window.addEventListener('pageshow', () => { document.body.style.opacity = ''; });
})();
