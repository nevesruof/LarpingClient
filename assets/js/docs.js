/* Larp Client — documentación: búsqueda, filtro de módulos, índice y menú móvil */
(function () {
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /* ---------- Búsqueda ---------- */
  const input = document.querySelector("[data-dsearch]");
  const box = document.querySelector(".dresults");
  let index = null, sel = 0, results = [];
  const load = () => index || (index = fetch("/assets/data/search.json").then((r) => r.json()));

  function score(e, q) {
    const t = e.t.toLowerCase(), x = (e.x + " " + (e.k || "")).toLowerCase();
    let s = 0;
    for (const w of q.split(/\s+/).filter(Boolean)) {
      if (t === w) s += 10;
      else if (t.startsWith(w)) s += 6;
      else if (t.includes(w)) s += 4;
      else if (x.includes(w)) s += 1;
      else return 0;
    }
    return s;
  }
  function draw() {
    if (!results.length) { box.innerHTML = `<div class="none">Nothing found for "${esc(input.value)}"</div>`; return; }
    box.innerHTML = results.map((r, i) => `<a href="${r.u}" class="${i === sel ? "sel" : ""}"><b>${esc(r.t)}</b><span>${esc(r.x)}</span></a>`).join("");
  }
  async function run() {
    const q = input.value.trim().toLowerCase();
    if (!q) { box.hidden = true; return; }
    const all = await load();
    results = all.map((e) => [score(e, q), e]).filter((a) => a[0] > 0).sort((a, b) => b[0] - a[0]).slice(0, 8).map((a) => a[1]);
    sel = 0; box.hidden = false; draw();
  }
  if (input) {
    input.addEventListener("focus", load, { once: true });
    input.addEventListener("input", run);
    input.addEventListener("keydown", (e) => {
      if (box.hidden) return;
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); sel = (sel + (e.key === "ArrowDown" ? 1 : results.length - 1)) % Math.max(1, results.length); draw(); }
      else if (e.key === "Enter" && results[sel]) { location.href = results[sel].u; box.hidden = true; }
      else if (e.key === "Escape") { box.hidden = true; input.blur(); }
    });
    document.addEventListener("click", (e) => { if (!e.target.closest(".dsearch")) box.hidden = true; });
    document.addEventListener("keydown", (e) => {
      if (e.key === "/" && !/input|textarea/i.test(document.activeElement.tagName)) {
        e.preventDefault();
        const side = document.querySelector(".dside");
        if (getComputedStyle(document.querySelector(".dside-toggle")).display !== "none") side.classList.add("open");
        input.focus();
      }
    });
  }

  /* ---------- Menú lateral en móvil ---------- */
  const tog = document.querySelector(".dside-toggle"), side = document.querySelector(".dside");
  if (tog && side) {
    tog.addEventListener("click", () => { const o = side.classList.toggle("open"); tog.setAttribute("aria-expanded", o); });
    side.addEventListener("click", (e) => { if (e.target.closest(".dgroup a")) side.classList.remove("open"); });
  }

  /* ---------- Filtro de módulos ---------- */
  const mf = document.querySelector("[data-mfilter]");
  if (mf) {
    const btns = [...document.querySelectorAll(".mfilter button")];
    const mods = [...document.querySelectorAll(".mod")], heads = [...document.querySelectorAll(".mcat")];
    const none = document.querySelector("[data-mnone]");
    let cat = "";
    const apply = () => {
      const q = mf.value.trim().toLowerCase();
      let shown = 0;
      const per = {};
      mods.forEach((m) => {
        const ok = (!cat || m.dataset.cat === cat) && (!q || q.split(/\s+/).every((w) => m.dataset.text.includes(w)));
        m.hidden = !ok;
        if (ok) { shown++; per[m.dataset.cat] = (per[m.dataset.cat] || 0) + 1; }
        if (ok && q) m.open = false;
      });
      heads.forEach((h) => (h.hidden = !per[h.dataset.cat]));
      none.hidden = shown > 0;
    };
    mf.addEventListener("input", apply);
    btns.forEach((b) => b.addEventListener("click", () => { cat = b.dataset.cat; btns.forEach((x) => x.setAttribute("aria-pressed", x === b)); apply(); }));
    // Abrir el módulo enlazado con #id
    const openHash = () => {
      const t = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (t && t.classList.contains("mod")) { t.hidden = false; t.open = true; setTimeout(() => t.scrollIntoView({ block: "start" }), 0); }
    };
    addEventListener("hashchange", openHash);
    openHash();
  }

  /* ---------- Índice: resaltar la sección actual ---------- */
  const links = [...document.querySelectorAll(".dtoc a")];
  if (links.length && "IntersectionObserver" in window) {
    const targets = links.map((a) => document.getElementById(a.getAttribute("href").slice(1))).filter(Boolean);
    const vis = new Set();
    const io = new IntersectionObserver((es) => {
      es.forEach((e) => (e.isIntersecting ? vis.add(e.target) : vis.delete(e.target)));
      let cur = targets.find((t) => vis.has(t));
      if (!cur) {
        const above = targets.filter((t) => t.getBoundingClientRect().top < 120);
        cur = above[above.length - 1];
      }
      links.forEach((a) => a.classList.toggle("active", !!cur && a.getAttribute("href") === "#" + cur.id));
    }, { rootMargin: "-70px 0px -60% 0px" });
    targets.forEach((t) => io.observe(t));
  }
})();
