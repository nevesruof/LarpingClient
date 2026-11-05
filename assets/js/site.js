/* Larp Client — interacciones de la landing */
(function () {
  const SPRITE = "/assets/img/icons.svg";
  const ALIAS = { fps: "fpsdisplay", ping: "pingdisplay" };
  const icon = (n) => `<svg class="ico" aria-hidden="true"><use href="${SPRITE}#i-${ALIAS[n] || n}"/></svg>`;
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /* ---------- Nav ---------- */
  const nav = document.querySelector(".nav");
  if (nav) {
    const onScroll = () => nav.classList.toggle("scrolled", scrollY > 8);
    addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    const btn = nav.querySelector(".nav-toggle"), menu = document.querySelector(".mobile-menu");
    if (btn && menu) {
      btn.addEventListener("click", () => {
        const open = menu.classList.toggle("open");
        btn.setAttribute("aria-expanded", open);
      });
      menu.addEventListener("click", (e) => { if (e.target.closest("a")) { menu.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); } });
    }
  }

  /* ---------- Pestañas genéricas (role=tablist) ---------- */
  document.querySelectorAll("[role=tablist][data-tabs]").forEach((list) => {
    const tabs = [...list.querySelectorAll("[role=tab]")];
    const select = (tab, focus) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute("aria-selected", on);
        t.tabIndex = on ? 0 : -1;
        const p = document.getElementById(t.getAttribute("aria-controls"));
        if (p) p.hidden = !on;
      });
      if (focus) tab.focus({ preventScroll: true });
      if (list.scrollWidth > list.clientWidth) tab.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    };
    tabs.forEach((t, i) => {
      t.addEventListener("click", () => select(t));
      t.addEventListener("keydown", (e) => {
        if (!['ArrowRight', 'ArrowLeft', 'Home', 'End'].includes(e.key)) return;
        e.preventDefault();
        const next = e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : (i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length;
        select(tabs[next], true);
      });
    });
  });

  /* ---------- HUD arrastrable con guías (como el editor de HUD) ---------- */
  const scene = document.querySelector(".hud-scene");
  if (scene) {
    // Teclas de keystrokes que se iluminan solas, como si alguien jugara
    const keys = scene.querySelectorAll(".keys [data-k]");
    if (keys.length && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
      const seq = ["W", "W", "A", "W", "D", "LMB", "W", "LMB", "S", "LMB", "W", "Space"];
      let i = 0;
      let timer = null, visible = false;
      const animateKeys = () => {
        keys.forEach((k) => k.classList.remove("on"));
        const k = scene.querySelector(`.keys [data-k="${seq[i++ % seq.length]}"]`);
        if (k) k.classList.add("on");
        if (i % 3 === 0) { const w = scene.querySelector('.keys [data-k="W"]'); if (w) w.classList.add("on"); }
      };
      const syncAnimation = () => {
        if (visible && !document.hidden && timer === null) timer = setInterval(animateKeys, 420);
        if ((!visible || document.hidden) && timer !== null) {
          clearInterval(timer); timer = null;
          keys.forEach(k => k.classList.remove('on'));
        }
      };
      new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; syncAnimation(); }).observe(scene);
      document.addEventListener('visibilitychange', syncAnimation);
    }
  }

  /* ---------- Cosméticos ---------- */
  const cos = document.querySelector("[data-cosmetics]");
  if (cos) {
    const data = JSON.parse(cos.querySelector("script[type='application/json']").textContent);
    const view = cos.querySelector(".cos-view img"), title = cos.querySelector(".cos-view .cap b"), sub = cos.querySelector(".cos-view .cap span");
    const grid = cos.querySelector(".cos-grid"), cats = [...cos.querySelectorAll(".cos-cats button")];
    let cat = cats[0].dataset.cat;
    const pick = (item) => {
      view.style.animation = "none"; void view.offsetWidth; view.style.animation = "";
      view.src = item.src; view.alt = item.name; title.textContent = item.name; sub.textContent = data[cat].label;
      grid.querySelectorAll("button").forEach((b) => b.setAttribute("aria-selected", b.dataset.src === item.src));
    };
    const show = () => {
      const g = data[cat];
      grid.innerHTML = g.items.map((it) => `<button type="button" data-src="${it.src}" aria-selected="false" title="${esc(it.name)}"><img src="${it.src}" alt="${esc(it.name)}" loading="lazy" width="90" height="90"></button>`).join("");
      pick(g.items[0]);
    };
    cats.forEach((b) => b.addEventListener("click", () => { cat = b.dataset.cat; cats.forEach((c) => c.setAttribute("aria-selected", c === b)); show(); }));
    grid.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (b) pick(data[cat].items.find((i) => i.src === b.dataset.src));
    });
    show();
  }

  /* ---------- Reloj del menú (como en el cliente) ---------- */
  const clocks = document.querySelectorAll("[data-clock]");
  const tick = () => {
    const d = new Date();
    const s = d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }) + ", " +
      d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" }).toLowerCase();
    clocks.forEach((c) => (c.textContent = s));
  };
  if (clocks.length) { tick(); setInterval(tick, 30000); }

  /* ---------- Año del footer ---------- */
  document.querySelectorAll("[data-year]").forEach((e) => (e.textContent = new Date().getFullYear()));
})();
