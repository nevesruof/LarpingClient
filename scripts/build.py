"""
Genera el sitio estático (index.html + docs/*.html) a partir de site.config.json,
assets/data/modules.json y el contenido de scripts/docs_content.py.

Uso:  python scripts/build.py
Vercel sirve los .html generados tal cual (no necesita paso de build).
"""
import json, html, re, pathlib, datetime, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
CFG = json.loads((ROOT / "site.config.json").read_text())
MODS = json.loads((ROOT / "assets/data/modules.json").read_text())
SPRITE = "/assets/img/icons.svg"
ALIAS = {"fps": "fpsdisplay", "ping": "pingdisplay"}
CATS = [("HUD", "HUD"), ("PVP", "PvP"), ("UTILITY", "Utility"), ("VISUALS", "Visuals"), ("COSMETICS", "Cosmetics"), ("CLIENT", "Client")]
CAT_LABEL = dict(CATS)
esc = html.escape


def icon(name, cls="ico"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="{SPRITE}#i-{ALIAS.get(name, name)}"/></svg>'


def discord_btn(cls="btn btn-glass", label="Join our Discord"):
    if not CFG.get("discordUrl"):
        return ""
    return f'<a class="{cls}" href="{esc(CFG["discordUrl"])}" target="_blank" rel="noopener">{icon("discord")}{label}</a>'


def head(title, desc, path, extra_css=""):
    url = CFG["siteUrl"].rstrip("/") + path
    full = title if title.startswith("Larp Client") else f"{title} — Larp Client"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#000000">
<link rel="canonical" href="{esc(url)}">
<link rel="icon" href="/assets/img/logo.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="{esc(CFG['siteUrl'].rstrip('/'))}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/assets/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">{extra_css}
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
"""


def nav(current=""):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    links = [a("/#product", "Product", "product"), a("/#features", "Features", "features"), a("/#cosmetics", "Cosmetics", "cosmetics"),
             a("/docs", "Docs", "docs"), a("/#faq", "FAQ", "faq")]
    dc = f'<a class="icon-link hide-m" href="{esc(CFG["discordUrl"])}" target="_blank" rel="noopener" aria-label="Discord">{icon("discord")}</a>' if CFG.get("discordUrl") else ""
    return f"""<header class="nav">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Larp Client home"><img src="/assets/img/logo.svg" alt="" width="26" height="26">Larp Client</a>
    <nav class="nav-links" aria-label="Main">{''.join(links)}</nav>
    <div class="nav-right">
      {dc}
      <a class="hide-m" href="/docs/changelog">v{CFG['version']}</a>
      <a class="btn btn-light btn-sm" href="/#access">You are my friend?</a>
      <button class="nav-toggle" type="button" aria-label="Menu" aria-expanded="false">{icon('menu')}</button>
    </div>
  </div>
</header>
<div class="mobile-menu">{''.join(links)}{('<a href="' + esc(CFG['discordUrl']) + '">Discord</a>') if CFG.get('discordUrl') else ''}<a class="btn btn-light" href="/#access">You are my friend?</a></div>
"""


def footer(scripts=""):
    dc = f'<li><a href="{esc(CFG["discordUrl"])}" target="_blank" rel="noopener">Discord</a></li>' if CFG.get("discordUrl") else ""
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="top">
      <div class="about">
        <a class="brand" href="/"><img src="/assets/img/logo.svg" alt="" width="26" height="26">Larp Client</a>
        <p>A visual client for Minecraft {CFG['minecraft']} on Fabric. Made by {esc(CFG['author'])}.</p>
      </div>
      <div><h4>Product</h4><ul>
        <li><a href="/#features">Features</a></li><li><a href="/#cosmetics">Cosmetics</a></li>
        <li><a href="/#access">Get access</a></li><li><a href="/docs/changelog">Changelog</a></li></ul></div>
      <div><h4>Docs</h4><ul>
        <li><a href="/docs/installation">Installation</a></li><li><a href="/docs/modules">All modules</a></li>
        <li><a href="/docs/performance">Performance</a></li><li><a href="/docs/troubleshooting">Troubleshooting</a></li></ul></div>
      <div><h4>More</h4><ul>
        {dc}<li><a href="/docs/credits">Credits</a></li><li><a href="/docs/faq">FAQ</a></li></ul></div>
    </div>
    <div class="bottom">
      <span>© <span data-year>{datetime.date.today().year}</span> Larp Client. Not affiliated with Mojang or Microsoft.</span>
      <span>Minecraft {CFG['minecraft']} · Fabric</span>
    </div>
  </div>
</footer>
<script src="/assets/js/site.js" defer></script>{scripts}
</body>
</html>
"""


def mini_card(mid, name, desc, on):
    return f"""<div class="mcard{' on' if on else ''}"><span class="pin">{icon('pin')}</span><div class="banner">{icon(mid)}</div><h5>{esc(name)}</h5><p>{esc(desc)}</p><span class="sw"></span></div>"""


def window_side(big=False):
    attr = lambda p: f' data-page="{p}"' if big else ""
    tag = "button type=\"button\"" if big else "div"
    end = "button" if big else "div"
    items = [("modules", "Modules", True), ("cosmetics", "Cosmetics", False), ("visuals", "Visuals", False),
             ("waypoints", "Waypoints", None), ("macros", "Macros", None), ("rpc", "RPC", None)]
    out = []
    for key, label, on in items:
        cnt = "<b></b>" if (big and on is not None) else ""
        interactive = big and on is not None
        t, e = (tag, end) if interactive else ("div", "div")
        out.append(f'<{t} class="navi{" on" if on else ""}"{attr(key) if interactive else ""}>{icon(key)}{label}{cnt}</{e}>')
    return f"""<div class="side">
  <div class="wordmark"><img src="/assets/img/logo.svg" alt="" width="32" height="32"><span>LARP<br>CLIENT</span></div>
  <div class="welcome">Welcome, {esc(CFG['author'])}</div>
  {''.join(out)}
  <div class="grow"></div>
  <div class="sbtn">{icon('settings')}Settings</div>
  <div class="sbtn">{icon('edithud')}Edit HUD</div>
  <div class="date" data-clock>{datetime.date.today().strftime('%d %b %Y')}</div>
</div>"""


def stats():
    by = {m["name"]: m for m in MODS}
    def opts(mod, setting):
        return len(next(s for s in by[mod]["settings"] if s["name"] == setting)["options"])
    items = [(len(MODS), "Modules"), (opts("Hats", "Hat"), "Hats"), (opts("Wings", "Style"), "Wing styles"),
             (opts("Target ESP", "Style"), "Target markers"), (opts("Kill Effect", "Effect"), "Kill effects")]
    return "".join(f'<div class="stat"><b>{n}</b><span>{l}</span></div>' for n, l in items)


def cosmetics_data():
    by = {m["name"]: m for m in MODS}
    def labels(mod, setting):
        return next(s for s in by[mod]["settings"] if s["name"] == setting)["options"]
    slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    groups = {
        "hats": {"label": "Hats", "items": [{"name": n, "src": f"/assets/img/cosmetics/hats/{slug(n)}.webp"} for n in labels("Hats", "Hat")]},
        "wings": {"label": "Wings", "items": [{"name": n, "src": f"/assets/img/cosmetics/wings/{slug(n)}.webp"} for n in labels("Wings", "Style")]},
        "aura": {"label": "Aura", "items": [{"name": n, "src": f"/assets/img/cosmetics/aura/{slug(n)}.webp"}
                                             for n in labels("Aura", "Orbit style") + labels("Aura", "Element") + ["Ground Runes"]]},
        "target": {"label": "Target", "items": [{"name": n, "src": f"/assets/img/cosmetics/target/{slug(n)}.webp"} for n in labels("Target ESP", "Style")]},
    }
    for g in groups.values():
        for it in g["items"]:
            assert (ROOT / it["src"].lstrip("/")).exists(), it["src"]
    return groups


FAQ = [
    ("How do I get Larp Client?",
     f"Larp Client is private and still in development, so it isn't public yet. Message {CFG['author']} and you'll get access."),
    ("Is Larp Client allowed on servers?",
     "Larp only changes what you see on your own screen. It has no combat, movement or auto-click modules, so it plays like any other visual client. "
     "Each server sets its own rules, so check theirs if you are unsure."),
    ("Can other players see my cosmetics?",
     "No. Cosmetics are drawn on your screen only. Press <kbd>F5</kbd> to see them on yourself."),
    ("How do I open the menu?",
     "Press <kbd>Right Shift</kbd> in game, or click <b>Client</b> on the title screen. You can change the key in Options › Controls › Larp Client."),
    ("Does it work with Sodium and other performance mods?",
     "Yes. Larp is made to run next to Sodium, Lithium and Entity Culling, and they are the first mods we recommend. "
     "With Iris shaderpacks, some 3D effects can look different depending on the pack."),
    ("Which Minecraft versions are supported?",
     f"Minecraft {CFG['minecraft']} with Fabric Loader {CFG['fabricLoader']} or newer, Fabric API and Java 21. Forge, NeoForge and older versions are not supported."),
    ("Where are my settings saved?",
     "In your <code>config</code> folder: <code>larpclient.json</code> for settings, <code>larpclient-profile-1.json</code> to <code>-3</code> for profiles, "
     "and <code>larpclient-waypoints.json</code> and <code>larpclient-macros.json</code>. Copy them to move your setup to another PC."),
    ("The Music Player doesn't show the album cover.",
     'The Music Player reads Windows media controls, so it only works on Windows. If the cover still doesn\'t show, see <a href="/docs/music-player">Music player</a> for the log file to check.'),
]


def index():
    cos = cosmetics_data()
    contact = CFG.get("contactUrl") or CFG.get("discordUrl") or ""
    label = CFG.get("contactLabel") or f"Message {CFG['author']}"
    dl_btn = (f'<a class="btn btn-light" href="{esc(contact)}" target="_blank" rel="noopener">{icon("discord")}{esc(label)}</a>' if contact
              else f'<span class="btn btn-light" aria-disabled="true">{icon("discord")}{esc(label)} on Discord</span>')
    faq = "".join(f'<details><summary>{q}{icon("expand")}</summary><div class="answer">{a}</div></details>' for q, a in FAQ)
    dots = "".join(f'<i style="left:{(i * 37) % 100}%;top:{(i * 53) % 100}%;opacity:{0.15 + (i % 4) * 0.08:.2f}"></i>' for i in range(18))
    perf = [("sodium", "Sodium"), ("lithium", "Lithium"), ("entityculling", "Entity Culling"), ("ferrite-core", "FerriteCore"),
            ("immediatelyfast", "ImmediatelyFast"), ("modernfix", "ModernFix")]
    perf_li = "".join(f'<li>{icon("check_circle")}<a href="https://modrinth.com/mod/{s}" target="_blank" rel="noopener">{n}</a></li>' for s, n in perf)
    features = [
        ("performance", "Smart FPS limits", "Menus, AFK and alt-tab get their own frame cap. Your FPS limit in Options is never touched."),
        ("wings", "Cached 3D cosmetics", "Wings, hats and auras rebuild their geometry up to 60 times a second and reuse it between frames, so high refresh rates stay smooth."),
        ("edithud", "A HUD that snaps", "Drag any element. It snaps to edges, the center and other elements, with a grid and 1 px arrow-key nudges."),
        ("layers", "Three profiles", "Save your whole setup in three slots and swap between a PvP layout and a clean one in a click."),
        ("rpc", "Discord presence", "Your Discord status shows Larp Client, the server you're on and the game version, with two buttons you choose."),
        ("hotbarkeybinds", "Your real hotbar keys", "Each hotbar slot shows the key it's bound to, even if your binds are 1 2 3 4 G R."),
    ]
    feat = "".join(f'<article class="feature"><div class="fi">{icon(i)}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in features)
    steps = [
        ("Install Fabric", f'Run the <a href="https://fabricmc.net/use/installer/" target="_blank" rel="noopener" style="text-decoration:underline;text-underline-offset:3px">Fabric installer</a> for Minecraft {CFG["minecraft"]}.'),
        ("Add the mods", "Put the Larp Client jar you got from Take and <a href=\"https://modrinth.com/mod/fabric-api\" target=\"_blank\" rel=\"noopener\" style=\"text-decoration:underline;text-underline-offset:3px\">Fabric API</a> in your <code>.minecraft/mods</code> folder."),
        ("Launch Fabric", f"Pick the Fabric {CFG['minecraft']} profile in the Minecraft Launcher and press Play."),
        ("Open the menu", "Press <kbd>Right Shift</kbd> or click Client on the title screen. Turn on what you like."),
    ]
    step_html = "".join(f'<div class="step"><div class="n">{i + 1}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(steps))
    nots = ["Tracers and chams", "Reach, aim assist or velocity", "Auto clicker", "X-ray or ore finders", "Entity radar"]
    nots_li = "".join(f"<li>{icon('block')}{n}</li>" for n in nots)
    cats_btn = "".join(f'<button type="button" data-cat="{k}" aria-selected="{str(i == 0).lower()}">{v["label"]}</button>' for i, (k, v) in enumerate(cos.items()))

    body = head("Larp Client — a visual client for Minecraft " + CFG["minecraft"],
                f"Larp Client is a Fabric client for Minecraft {CFG['minecraft']} with {len(MODS)} modules, 3D cosmetics, a snapping HUD editor and smart FPS limits.", "/")
    body += nav()
    body += f"""<main id="main">
<section class="hero">
  <canvas class="curtains" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="hero-copy">
      <h1>Looks illegal.<span>Isn't.</span></h1>
      <p class="lead">Larp Client is a Fabric client for Minecraft {CFG['minecraft']}. {len(MODS)} modules, 3D cosmetics, a HUD you place anywhere and smart FPS limits. Every effect stays on your screen.</p>
      <div class="actions">
        <a class="btn btn-light" href="#access">{icon('person')}You are my friend?</a>
        {discord_btn() or f'<a class="btn btn-glass" href="/docs">{icon("doc")}Read the docs</a>'}
      </div>
      <p class="fine">Private and in development. Ask {esc(CFG['author'])} for access.</p>
    </div>
    <div class="stage" aria-hidden="true">
      <div class="window">
        {window_side()}
        <div class="main">
          <div class="head"><div><h4>Modules</h4><p>Configure built-in client mods</p></div><span class="search">{icon('search')}</span></div>
          <div class="tabs"><span>All</span><span class="on">HUD</span><span>PvP</span><span>Utility</span><span>Pinned</span></div>
          <div class="cards">
            {mini_card('infobar', 'Info Bar', 'A sleek bar with your name, server, FPS and session time', True)}
            {mini_card('modulelist', 'Module List', 'Your active modules, sorted and animated', True)}
            {mini_card('fps', 'FPS', 'Frames per second, updated live', False)}
            {mini_card('ping', 'Ping', 'Your latency to the server', False)}
          </div>
        </div>
      </div>
      <div class="splash-card"><span class="x">{icon('close')}</span><div class="dots">{dots}</div><div class="logo-wrap"><img src="/assets/img/logo.svg" alt=""></div><div class="bar"><i></i></div></div>
    </div>
  </div>
</section>

<section class="strip" aria-label="Larp Client in numbers"><div class="wrap">{stats()}</div></section>

<section class="section" id="product">
  <div class="wrap">
    <div class="section-head">
      <h2>Everything lives in one menu.</h2>
      <p>Turn mods on, place your HUD and pick your cosmetics without leaving the game. Try it here: it's the same menu.</p>
    </div>
    <div class="show-tabs" role="tablist" data-tabs aria-label="Product preview">
      <button class="show-tab" role="tab" aria-selected="true" aria-controls="p-menu" id="t-menu"><b>Menu</b><span>Right Shift in game</span></button>
      <button class="show-tab" role="tab" aria-selected="false" aria-controls="p-hud" id="t-hud" tabindex="-1"><b>HUD editor</b><span>Drag, snap, done</span></button>
      <button class="show-tab" role="tab" aria-selected="false" aria-controls="p-cos" id="t-cos" tabindex="-1"><b>Cosmetics</b><span>Seen in third person</span></button>
    </div>
    <div class="show-frame">
      <div class="chrome"><i></i><i></i><i></i><span>larp client / {CFG['version']}</span></div>

      <div class="panel" id="p-menu" role="tabpanel" aria-labelledby="t-menu">
        <div class="window big" data-menu>
          {window_side(big=True)}
          <div class="main">
            <div class="head"><div><h4 data-title>Modules</h4><p data-sub>Configure built-in client mods</p></div>
              <div class="search-box"><input class="search-input" type="search" placeholder="Search mods" aria-label="Search mods"><button type="button" class="search" aria-label="Search">{icon('search')}</button></div></div>
            <div class="tabs" data-tabs-mock></div>
            <div class="cards" data-cards></div>
          </div>
        </div>
      </div>

      <div class="panel" id="p-hud" role="tabpanel" aria-labelledby="t-hud" hidden>
        <div class="hud-scene">
          <div class="grid"></div><div class="guide v"></div><div class="guide h"></div>
          <div class="hud-el hud-box infobar" style="left:14px;top:14px">
            <span><img class="logo" src="/assets/img/logo.svg" alt=""><span class="name"><svg class="crown" aria-hidden="true"><use href="{SPRITE}#i-crown"/></svg>{esc(CFG['author'])}</span></span>
            <span class="muted">eskmc.net</span><span>144 FPS</span><span class="muted">12:48</span>
          </div>
          <div class="hud-el modlist" style="right:14px;top:14px">
            <div>Target HUD</div><div>Keystrokes<small>Clean</small></div><div>Hit FX<small>White</small></div><div>Performance</div><div>Wings<small>Angel</small></div><div>Zoom</div>
          </div>
          <div class="hud-el keys" style="left:14px;top:46%">
            <span></span><span data-k="W">W</span><span></span>
            <span data-k="A">A</span><span data-k="S">S</span><span data-k="D">D</span>
            <div class="mouse"><span data-k="LMB">LMB</span><span data-k="RMB">RMB</span></div>
            <span class="wide" data-k="Space">―</span>
          </div>
          <div class="hud-el hud-box target" style="left:50%;top:58%;transform:translateX(-50%)">
            <div class="head"></div>
            <div class="info"><div class="row"><b>Steve</b><span>3.1m</span></div><div class="row"><span>12.8 ❤</span><span style="color:#3fd07a">+4.2</span></div><div class="hp"><i></i></div></div>
          </div>
          <div class="hud-el hotbar" style="left:50%;bottom:16px;transform:translateX(-50%)">
            <span class="sel"><b>1</b><i style="background:linear-gradient(135deg,#7fe3ff,#2a8bb5)"></i></span><span><b>2</b><i style="background:linear-gradient(135deg,#ffe37f,#c99a1e)"></i></span><span><b>3</b><i style="background:linear-gradient(135deg,#d8b4ff,#7c3fc4)"></i></span><span><b>4</b></span><span><b>G</b><i style="background:linear-gradient(135deg,#ff8f8f,#b52a2a)"></i></span><span><b>R</b></span><span><b>7</b></span><span><b>8</b></span><span><b>9</b></span>
          </div>
          <div class="hud-hint">Drag anything. It snaps to the center and to other elements.</div>
        </div>
      </div>

      <div class="panel" id="p-cos" role="tabpanel" aria-labelledby="t-cos" hidden>
        <div class="cos" data-cosmetics>
          <script type="application/json">{json.dumps(cos)}</script>
          <div class="cos-view"><img src="{cos['hats']['items'][0]['src']}" alt="{cos['hats']['items'][0]['name']}" width="420" height="420"><div class="cap"><b>{cos['hats']['items'][0]['name']}</b><span>Hats</span></div></div>
          <div class="cos-side"><div class="cos-cats" role="group" aria-label="Cosmetic type">{cats_btn}</div><div class="cos-grid"></div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="features" style="padding-top:40px">
  <div class="wrap">
    <div class="section-head">
      <h2>Built to stay out of your way.</h2>
      <p>The visuals are loud. The client isn't: it caps frames when you're not playing and caches what it can.</p>
    </div>
    <div class="features">{feat}</div>
  </div>
</section>

<section class="section" id="cosmetics" style="padding-top:40px">
  <div class="wrap">
    <div class="section-head">
      <h2>{len(cos['hats']['items'])} hats, {len(cos['wings']['items'])} wings, {len(cos['aura']['items'])} auras.</h2>
      <p>Every cosmetic is real 3D geometry that moves with you. Wings flap as you walk, capes flow, auras orbit. These are actual renders from the client.</p>
    </div>
    <div class="cos-strip">{''.join(f'<figure><img src="{it["src"]}" alt="" loading="lazy" width="180" height="180"><figcaption>{it["name"]}{suf}</figcaption></figure>' for it, suf in [(cos['hats']['items'][0], ''), (cos['wings']['items'][3], ' wings'), (cos['aura']['items'][5], ' aura'), (cos['hats']['items'][18], ''), (cos['wings']['items'][1], ' wings'), (cos['target']['items'][8], ' marker'), (cos['hats']['items'][21], ''), (cos['aura']['items'][10], '')])}</div>
    <p class="cos-more"><a href="/docs/cosmetics">See every cosmetic {icon('arrow')}</a></p>
  </div>
</section>

<section class="section" id="install">
  <div class="wrap">
    <div class="section-head"><h2>Installed in four steps.</h2><p>About two minutes if you already have Minecraft {CFG['minecraft']}.</p></div>
    <div class="steps">{step_html}</div>
  </div>
</section>

<section class="section" style="padding-top:20px">
  <div class="wrap">
    <div class="fair">
      <div>
        <h2>Visual only. On purpose.</h2>
        <p>Larp changes how the game looks, never how it plays. These are the things you won't find in it, and won't in future versions.</p>
        <p style="margin-top:22px"><a class="btn btn-glass btn-sm" href="/docs/modules">See every module</a></p>
      </div>
      <ul>{nots_li}</ul>
    </div>
  </div>
</section>

<section class="section" id="access">
  <div class="wrap">
    <div class="section-head center"><h2>You are my friend?</h2><p>Larp Client is private and still in development. Message me, {esc(CFG['author'])}, and I'll give you access.</p></div>
    <div class="dl">
      <article class="dl-card main">
        <span class="tag">Private · v{CFG['version']}</span>
        <h3>Larp Client</h3>
        <p class="sub">Only for friends while it's in development. Ask {esc(CFG['author'])} and you'll get the mod.</p>
        <ul>
          <li>{icon('check_circle')}Minecraft {CFG['minecraft']}</li>
          <li>{icon('check_circle')}Fabric Loader {CFG['fabricLoader']}+</li>
          <li>{icon('check_circle')}<a href="https://modrinth.com/mod/fabric-api" target="_blank" rel="noopener">Fabric API</a></li>
          <li>{icon('check_circle')}Java 21</li>
        </ul>
        {dl_btn}
      </article>
      <article class="dl-card">
        <span class="tag">In development</span>
        <h3>Larp Launcher</h3>
        <p class="sub">One click installs Fabric, Larp Client and the performance mods, then opens the game with your Minecraft account.</p>
        <ul>
          <li>{icon('check_circle')}Updates itself and your mods</li>
          <li>{icon('check_circle')}Its own profile and folder</li>
          <li>{icon('check_circle')}Pick your RAM and mods</li>
        </ul>
        <span class="btn btn-glass" aria-disabled="true">Coming soon</span>
      </article>
      <article class="dl-card">
        <span class="tag">Recommended</span>
        <h3>Performance pack</h3>
        <p class="sub">Install these next to Larp for the biggest FPS gains.</p>
        <ul>{perf_li}</ul>
        <a class="btn btn-glass" href="/docs/performance">Why these mods</a>
      </article>
    </div>
  </div>
</section>

<section class="section" id="faq" style="padding-top:40px">
  <div class="wrap">
    <div class="section-head center"><h2>Questions people ask.</h2></div>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="section cta">
  <canvas class="curtains" aria-hidden="true"></canvas>
  <div class="wrap">
    <img class="mark" src="/assets/img/logo.svg" alt="" width="64" height="64">
    <h2>Your next session can look like this.</h2>
    <p>Private for now. Message {esc(CFG['author'])} for access.</p>
    <div class="actions"><a class="btn btn-light" href="#access">{icon('person')}You are my friend?</a><a class="btn btn-glass" href="/docs">Read the docs</a></div>
  </div>
</section>
</main>
"""
    body += footer('\n<script src="/assets/js/curtains.js" defer></script>')
    (ROOT / "index.html").write_text(body)


def not_found():
    body = head("Page not found", "This page doesn't exist.", "/404")
    body += nav()
    body += f"""<main id="main"><section class="section cta" style="min-height:70vh;display:flex;align-items:center">
  <canvas class="curtains" aria-hidden="true"></canvas>
  <div class="wrap">
    <img class="mark" src="/assets/img/logo.svg" alt="" width="64" height="64">
    <h2>This page doesn't exist.</h2>
    <p>The link may be old or mistyped. Try the docs search or go back home.</p>
    <div class="actions"><a class="btn btn-light" href="/">Go home</a><a class="btn btn-glass" href="/docs">Open the docs</a></div>
  </div>
</section></main>
"""
    body += footer('\n<script src="/assets/js/curtains.js" defer></script>')
    (ROOT / "404.html").write_text(body)


if __name__ == "__main__":
    index()
    not_found()
    import docs_build
    docs_build.build(globals())
    print("ok")
