"""Páginas de la documentación. Lo llama build.py."""
import json, re, html

esc = html.escape


def build(g):
    ROOT, CFG, MODS, icon, head, nav, footer, CATS, CAT_LABEL, cosmetics_data, FAQ = (
        g["ROOT"], g["CFG"], g["MODS"], g["icon"], g["head"], g["nav"], g["footer"], g["CATS"], g["CAT_LABEL"], g["cosmetics_data"], g["FAQ"])
    V, MC = CFG["version"], CFG["minecraft"]
    by = {m["name"]: m for m in MODS}

    def callout(kind, text):
        ic = {"tip": "lightbulb", "warn": "warning2", "note": "info"}[kind]
        return f'<div class="callout {kind}">{icon(ic)}<p>{text}</p></div>'

    def mlink(name):
        m = by[name]
        return f'<a href="/docs/modules#{m["id"]}">{esc(name)}</a>'

    def settings_table(m):
        if not m["settings"]:
            return '<p class="none">No settings. Turn it on and it works.</p>'
        rows = []
        for s in m["settings"]:
            t = s["type"]
            if t == "bool":
                val = ("On" if s.get("default") else "Off") if "default" in s else "On / Off"
            elif t == "number":
                d = s.get("default")
                fmt = lambda x: ("%g" % x)
                val = f'{fmt(d)} <span style="color:var(--dim)">({fmt(s["min"])} to {fmt(s["max"])})</span>' if d is not None else "Slider"
            elif t == "mode":
                opts = s.get("options") or []
                val = '<div class="chips">' + "".join(f"<span>{esc(o)}</span>" for o in opts) + "</div>"
            elif t == "color":
                c = s.get("default")
                val = f'<span class="swatch" style="background:{c}"></span> {c}' if c else "Color picker"
            else:
                val = f'<code>{esc(s.get("default") or "")}</code>' if s.get("default") else "Text"
            grp = f'<span style="color:var(--dim)">{esc(s["group"])}</span>' if s.get("group") else ""
            rows.append(f"<tr><td>{esc(s['name'])}</td><td>{val}</td><td>{grp}</td></tr>")
        return '<div class="table-wrap"><table><thead><tr><th>Setting</th><th>Default / options</th><th>Section</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>"

    # ---------------- Contenido ----------------
    cos = cosmetics_data()

    def gallery(items):
        return '<div class="gallery">' + "".join(
            f'<figure><img src="{it["src"]}" alt="{esc(it["name"])}" loading="lazy" width="118" height="118"><figcaption>{esc(it["name"])}</figcaption></figure>' for it in items) + "</div>"

    counts = {c: sum(1 for m in MODS if m["category"] == c) for c, _ in CATS}

    pages = []

    def page(slug, title, group, ic, desc, body):
        pages.append(dict(slug=slug, title=title, group=group, icon=ic, desc=desc, body=body))

    page("", "Introduction", "Getting started", "home",
         f"Larp Client is a visual client for Minecraft {MC} built on Fabric.",
         f"""
<p>Larp Client is a Fabric mod for Minecraft {MC}. It adds {len(MODS)} modules (HUD elements, PvP info, visuals and 3D cosmetics), its own menus and a HUD editor. Everything it draws stays on your screen: it never changes how the game plays.</p>
<div class="cards-doc">
  <a href="/docs/installation">{icon('download')}<b>Installation</b><span>Get Larp running in about two minutes.</span></a>
  <a href="/docs/client-menu">{icon('modules')}<b>The client menu</b><span>Turn mods on, change settings and bind keys.</span></a>
  <a href="/docs/modules">{icon('layers')}<b>All modules</b><span>Every module and every setting, searchable.</span></a>
  <a href="/docs/cosmetics">{icon('cosmetics')}<b>Cosmetics</b><span>Wings, hats, auras, capes and trails.</span></a>
</div>
<h2 id="whats-inside">What's inside</h2>
<div class="table-wrap"><table><thead><tr><th>Section</th><th>Modules</th><th>Examples</th></tr></thead><tbody>
<tr><td>HUD</td><td>{counts['HUD']}</td><td>{mlink('Info Bar')}, {mlink('Module List')}, {mlink('Armor Status')}, {mlink('Hotbar Keybinds')}</td></tr>
<tr><td>PvP</td><td>{counts['PVP']}</td><td>{mlink('Keystrokes')}, {mlink('Target HUD')}, {mlink('Session Stats')}, {mlink('Cooldowns')}</td></tr>
<tr><td>Utility</td><td>{counts['UTILITY']}</td><td>{mlink('Zoom')}, {mlink('Performance')}, {mlink('Waypoints')}, {mlink('Macros')}</td></tr>
<tr><td>Visuals</td><td>{counts['VISUALS']}</td><td>{mlink('Hit FX')}, {mlink('Kill Effect')}, {mlink('Hitboxes')}, {mlink('Custom Sky')}</td></tr>
<tr><td>Cosmetics</td><td>{counts['COSMETICS']}</td><td>{mlink('Wings')}, {mlink('Hats')}, {mlink('Aura')}, {mlink('Cape')}</td></tr>
<tr><td>Client</td><td>{counts['CLIENT']}</td><td>{mlink('Interface')}, {mlink('Discord RPC')}</td></tr>
</tbody></table></div>
<h2 id="requirements">Requirements</h2>
<ul>
<li>Minecraft <b>{MC}</b> (Java Edition)</li>
<li>Fabric Loader <b>{CFG['fabricLoader']}</b> or newer</li>
<li><a href="https://modrinth.com/mod/fabric-api" target="_blank" rel="noopener">Fabric API</a> for {MC}</li>
<li>Java 21 (the official Minecraft Launcher already includes it)</li>
</ul>
{callout('warn', f'Larp Client is private and in development. To get it, message {CFG["author"]} for access.')}
{callout('note', 'Larp is a Fabric mod, not a separate launcher like Lunar or Badlion. It runs inside the normal Minecraft Launcher, Prism, Modrinth App or any launcher that supports Fabric.')}
""")

    page("installation", "Installation", "Getting started", "download",
         "Install Fabric, add Larp Client and Fabric API, and launch.",
         f"""
{callout('warn', f'Larp Client is private for now. Message {CFG["author"]} to get access and the jar.')}
<h2 id="steps">Install in four steps</h2>
<ol class="steps-doc">
<li><b>Install Fabric</b>Download the <a href="https://fabricmc.net/use/installer/" target="_blank" rel="noopener">Fabric installer</a>, open it, pick Minecraft <b>{MC}</b> and click Install. Keep "Create profile" checked.</li>
<li><b>Open your mods folder</b>Press <kbd>Win</kbd> + <kbd>R</kbd>, type <code>%appdata%\\.minecraft</code> and press Enter. Create a folder called <code>mods</code> if it isn't there.</li>
<li><b>Add the two mods</b>Put the Larp Client jar ({CFG["author"]} sends it to you when you get access) and <a href="https://modrinth.com/mod/fabric-api/versions?g={MC}" target="_blank" rel="noopener">Fabric API for {MC}</a> in <code>mods</code>.</li>
<li><b>Launch</b>In the Minecraft Launcher, choose the <b>fabric-loader-{MC}</b> profile and press Play. The Larp title screen means it worked.</li>
</ol>
{callout('tip', 'Add <a href="/docs/performance">Sodium, Lithium and Entity Culling</a> to the same folder for a big FPS boost. Larp is made to run with them.')}
<h2 id="other-launchers">Prism, Modrinth App and others</h2>
<p>Create a new instance for Minecraft {MC} with the Fabric loader, then add Fabric API and drop <code>larp-client-{V}.jar</code> into the instance's <code>mods</code> folder (usually under "Open folder").</p>
<h2 id="updating">Updating</h2>
<p>Delete the old <code>larp-client-*.jar</code> from <code>mods</code> and put the new one in. Your settings are kept, they live in the <code>config</code> folder.</p>
<h2 id="mac-linux">macOS and Linux</h2>
<p>The mods folder is <code>~/Library/Application Support/minecraft/mods</code> on macOS and <code>~/.minecraft/mods</code> on Linux. Everything works except the <a href="/docs/music-player">Music Player</a>, which reads Windows media controls.</p>
<h2 id="not-working">It doesn't start</h2>
<ul>
<li>Make sure Fabric API is the <b>{MC}</b> build, not an older one.</li>
<li>Remove other clients or mods that replace the title screen and menus, then try again.</li>
<li>Still stuck? See <a href="/docs/troubleshooting">Troubleshooting</a>.</li>
</ul>
""")

    page("client-menu", "The client menu", "Getting started", "modules",
         "Open the menu, find mods, change their settings and bind keys.",
         f"""
<p>Press <kbd>Right Shift</kbd> in game, or click <b>Client</b> on the title screen. The menu has a sidebar with six pages:</p>
<div class="table-wrap"><table><thead><tr><th>Page</th><th>What's there</th></tr></thead><tbody>
<tr><td>Modules</td><td>HUD, PvP and Utility mods, with tabs for each plus <b>Enabled</b> and <b>Pinned</b>.</td></tr>
<tr><td>Cosmetics</td><td>Cape, Wings, Hats, Aura and Trail, with a live preview.</td></tr>
<tr><td>Visuals</td><td>World, combat and camera effects, with <b>World</b>, <b>Combat</b>, <b>Camera</b> and <b>Enabled</b> tabs.</td></tr>
<tr><td>Waypoints</td><td>Your saved places. See <a href="/docs/waypoints">Waypoints</a>.</td></tr>
<tr><td>Macros</td><td>Keys that send a command or message. See <a href="/docs/macros">Macros</a>.</td></tr>
<tr><td>RPC</td><td>Your Discord status and a preview of it. See <a href="/docs/discord-rpc">Discord RPC</a>.</td></tr>
</tbody></table></div>
<p>At the bottom are <b>Settings</b> (theme, menus, profiles) and <b>Edit HUD</b>. The number next to each page is how many mods are on there.</p>
<h2 id="cards">Mod cards</h2>
<ul>
<li><b>Click the switch</b> or <b>right-click the card</b> to turn a mod on or off.</li>
<li><b>Click the card</b> to open its settings.</li>
<li><b>Click the pin</b> to keep a mod at the top, and in the Pinned tab.</li>
<li>Use the <b>search</b> button to find a mod by name or description.</li>
</ul>
<h2 id="settings-page">Settings page</h2>
<p>Each mod's settings are grouped into sections, with checkboxes in two columns, sliders and option pickers. The back arrow returns to the list. <b>Reset settings</b> puts the mod back to how it came, including its HUD position.</p>
<h2 id="keybinds">Binding a key to a mod</h2>
<p>On a mod's settings page, click the key button and press any key. Right-click it to clear the bind. The key shows on the mod's card, and pressing it in game toggles the mod with a small notification.</p>
<h2 id="theme">Theme</h2>
<p>In <b>Settings → Theme</b> choose an accent color: {', '.join(next(s for s in by['Interface']['settings'] if s['name']=='Accent')['options'])}. It colors switches, glows and the HUD. <b>Menu background</b> switches the title screen between fluid curtains and the blurred panorama.</p>
""")

    page("keybinds", "Keybinds", "Getting started", "keybinds",
         "Default keys and where to change them.",
         f"""
<p>All Larp keys are in <b>Options → Controls → Key Binds → Larp Client</b>. Mod toggles can also be set from each mod's settings page.</p>
<div class="table-wrap"><table><thead><tr><th>Action</th><th>Default</th></tr></thead><tbody>
<tr><td>Open the client menu</td><td><kbd>Right Shift</kbd></td></tr>
<tr><td>Zoom (hold)</td><td><kbd>C</kbd></td></tr>
<tr><td>Open the HUD editor</td><td>Not bound</td></tr>
<tr><td>Music: play / pause</td><td>Not bound</td></tr>
<tr><td>Music: next / previous</td><td>Not bound</td></tr>
<tr><td>Toggle any mod</td><td>Not bound, set it on the mod's page</td></tr>
</tbody></table></div>
{callout('tip', f'Turn on {mlink("Hotbar Keybinds")} to see the key bound to each hotbar slot, even if they are 1 2 3 4 G R, in the corner of every slot.')}
""")

    page("hud-editor", "HUD editor", "Features", "edithud",
         "Place every HUD element exactly where you want it.",
         f"""
<p>Open it from <b>Edit HUD</b> at the bottom of the client menu, or bind a key for it in Controls. Every HUD module that's on shows up and can be dragged.</p>
<h2 id="moving">Moving elements</h2>
<ul>
<li><b>Drag</b> an element to move it. It snaps to the screen edges, the center and the edges of other elements, with guide lines.</li>
<li>Use the <b>arrow keys</b> to move the selected element by 1 pixel, or 10 with <kbd>Shift</kbd>.</li>
<li>Positions are saved relative to the screen, so they stay put when you resize the window or change the GUI scale.</li>
</ul>
<h2 id="toolbar">Toolbar</h2>
<div class="table-wrap"><table><tbody>
<tr><td>Done</td><td>Save and close.</td></tr>
<tr><td>Mods</td><td>Go to the client menu to turn elements on or off.</td></tr>
<tr><td>Grid</td><td>Show a grid while you place things.</td></tr>
<tr><td>Snap</td><td>Turn snapping on or off.</td></tr>
<tr><td>Reset all</td><td>Put every element back in its default spot.</td></tr>
</tbody></table></div>
<h2 id="style">Styling elements</h2>
<p>Every HUD module shares the same style settings: <b>Scale</b>, <b>Background</b>, <b>Background color</b>, <b>Corner radius</b>, <b>Text color</b>, <b>Chroma text</b>, <b>Font</b> (Minecraft or Clean) and <b>Text shadow</b>.</p>
""")

    hats, wings, aura, target = cos["hats"]["items"], cos["wings"]["items"], cos["aura"]["items"], cos["target"]["items"]
    page("cosmetics", "Cosmetics", "Features", "cosmetics",
         "3D wings, hats, auras, capes and trails that move with you.",
         f"""
<p>Cosmetics are real 3D models drawn around your player. Only you see them, on your own screen. Press <kbd>F5</kbd> to look at yourself. Every cosmetic can use the theme accent, a fixed color, your own color or rainbow.</p>
{callout('note', 'The images on this page are rendered with the same code the client uses.')}
<h2 id="hats">Hats</h2>
<p>{len(hats)} hats: crowns, halos, ears, horns, antlers and the China Hat. In {mlink('Hats')} you can change the scale, height and opacity, and make it bob, spin or follow your head.</p>
{gallery(hats)}
<h2 id="wings">Wings</h2>
<p>{len(wings)} styles. They flap faster as you move, and you can set the scale, height, opacity and flap speed in {mlink('Wings')}.</p>
{gallery(wings)}
<h2 id="aura">Aura</h2>
<p>{mlink('Aura')} has five modes: <b>Orbiting</b> (shards, swords, orbs, runes or rings circling you), <b>Elemental</b> (flame, frost, void, sakura or storm), <b>Ground Runes</b>, <b>Energy Sphere</b> and <b>Lightning Arcs</b>.</p>
{gallery(aura)}
<h2 id="target-esp">Target ESP</h2>
<p>A marker on the player you're fighting, from {mlink('Target ESP')}. {len(target)} styles. It's part of Visuals, not Cosmetics, but uses the same 3D engine.</p>
{gallery(target)}
<h2 id="cape-trail">Cape and Trail</h2>
<p>{mlink('Cape')} is a flowing cape with your colors and the Larp logo, in Gradient, Solid or Split styles with physics you can tune. {mlink('Trail')} leaves a ribbon of light behind you, with optional sparkles.</p>
<h2 id="performance">Performance</h2>
<p>Cosmetic shapes are rebuilt up to 60 times a second and reused between frames, so at 144 FPS or more most of the work is skipped. Change it in <b>Settings → Performance → Cosmetic FPS</b> (30, 60, 120 or Max).</p>
""")

    page("waypoints", "Waypoints", "Features", "waypoints",
         "Save places and see them in the world with beams and labels.",
         f"""
<p>Open the <b>Waypoints</b> page in the client menu and click <b>Add here</b> to save where you're standing. Each waypoint has a name and a color and belongs to the world or server you made it in.</p>
<ul>
<li>Every waypoint can be renamed, recolored, hidden or deleted from the list.</li>
<li>In the world you'll see a <b>beam of light</b> and a <b>label</b> with the distance.</li>
<li>When you die, a <b>Death</b> waypoint is added where it happened (turn off in settings).</li>
</ul>
<h2 id="settings">Settings</h2>
{settings_table(by['Waypoints'])}
{callout('tip', f'{mlink("Breadcrumbs")} draws a glowing path of where you walked, handy for finding your way back.')}
""")

    page("macros", "Macros", "Features", "macros",
         "Keys that send a command or a chat message.",
         """
<p>Open the <b>Macros</b> page in the client menu and add a macro. Pick a key and type what it sends: a command like <code>/home</code> or <code>/spawn</code>, or a normal chat message.</p>
<ul>
<li>Press the key in game and Larp sends it, exactly as if you typed it.</li>
<li>Macros are saved in <code>config/larpclient-macros.json</code>.</li>
</ul>
<div class="callout warn"><svg class="ico" aria-hidden="true"><use href="/assets/img/icons.svg#i-warning2"/></svg><p>Some servers limit how fast you can send messages. Don't spam macros or you might get kicked.</p></div>
""")

    page("discord-rpc", "Discord RPC", "Features", "rpc",
         "Show Larp Client, your server and the game version on Discord.",
         f"""
<p>{mlink('Discord RPC')} sets your Discord status while you play: the Larp logo, <b>Larp Client</b>, the server you're on (for example <i>In eskmc.net</i>), <i>Multiplayer [{MC}]</i>, how long you've been playing and two buttons.</p>
<h2 id="setup">Set it up</h2>
<ol class="steps-doc">
<li><b>Create a Discord app</b>Go to the <a href="https://discord.com/developers/applications" target="_blank" rel="noopener">Discord Developer Portal</a>, click New Application and name it <b>Larp Client</b>. That name is what people see.</li>
<li><b>Copy the Application ID</b>In game, open the menu → RPC → Application ID and paste it.</li>
<li><b>Upload the logo</b>In your app, go to Rich Presence → Art Assets and upload a transparent PNG named <code>logo</code>.</li>
<li><b>Set the buttons</b>Change the two button texts and links. Links must start with <code>https://</code>.</li>
</ol>
{callout('note', 'Discord doesn\'t let you click your own buttons. Other people see them and can use them.')}
{callout('tip', 'If your launcher also shows a Discord status (for example the Modrinth App), turn it off there so only Larp\'s shows.')}
<h2 id="settings">Settings</h2>
{settings_table(by['Discord RPC'])}
""")

    page("music-player", "Music player", "Features", "musicplayer",
         "See what's playing on Spotify, with cover art and controls.",
         f"""
<p>{mlink('Music Player')} shows what's playing on your PC (Spotify, YouTube in a browser, Apple Music and others) with the album cover, title, artist and progress. It reads Windows media controls, so it only works on <b>Windows</b>.</p>
<h2 id="controls">Controls</h2>
<ul>
<li>With the chat open, click the widget's previous, play/pause and next buttons.</li>
<li>Or bind keys in Options → Controls → Larp Client → Music.</li>
</ul>
<h2 id="no-cover">The cover doesn't show</h2>
<p>Larp writes what happened to <code>%TEMP%\\larp_media_log.txt</code>. Open it to see why the cover couldn't be read, and include it if you ask for help.</p>
""")

    page("profiles", "Profiles", "Features", "layers",
         "Save your whole setup and switch in one click.",
         """
<p>Go to <b>Settings → Profiles</b> in the client menu. There are three slots. <b>Save</b> stores every mod, setting, keybind and HUD position in a slot; <b>Load</b> brings it back.</p>
<h2 id="files">Where it's stored</h2>
<div class="table-wrap"><table><tbody>
<tr><td><code>config/larpclient.json</code></td><td>Your current settings</td></tr>
<tr><td><code>config/larpclient-profile-1.json</code> to <code>-3</code></td><td>Profiles</td></tr>
<tr><td><code>config/larpclient-waypoints.json</code></td><td>Waypoints</td></tr>
<tr><td><code>config/larpclient-macros.json</code></td><td>Macros</td></tr>
</tbody></table></div>
<p>Copy these files to move your setup to another PC or instance.</p>
""")

    # Referencia de módulos
    sections = []
    for c, label in CATS:
        items = [m for m in MODS if m["category"] == c]
        cards = []
        for m in items:
            on = '<span class="on">On by default</span>' if m["defaultOn"] else '<span>Off by default</span>'
            cards.append(f"""<details class="mod" id="{m['id']}" data-cat="{c}" data-text="{esc((m['name'] + ' ' + m['description'] + ' ' + ' '.join(s['name'] for s in m['settings'])).lower())}">
<summary><span class="mi">{icon(m['id'])}</span><span class="mt"><b>{esc(m['name'])}</b><span>{esc(m['description'])}</span></span><span class="mm"><span class="state">{on}</span>{icon('expand')}</span></summary>
<div class="mbody">{settings_table(m)}</div></details>""")
        sections.append(f'<h2 class="mcat" id="cat-{c.lower()}" data-cat="{c}">{label} <span style="color:var(--dim);font-weight:400">{len(items)}</span></h2>' + "".join(cards))
    filt = '<div class="mfilter"><input type="search" placeholder="Filter modules and settings" aria-label="Filter modules" data-mfilter>' + \
        '<button type="button" aria-pressed="true" data-cat="">All</button>' + "".join(f'<button type="button" aria-pressed="false" data-cat="{c}">{l}</button>' for c, l in CATS) + "</div>"
    page("modules", "All modules", "Modules", "layers",
         f"Every module in Larp Client {V} and all of its settings.",
         filt + "".join(sections) + '<p class="none" data-mnone hidden style="color:var(--muted)">No modules match that filter.</p>')

    perf = [("sodium", "Sodium", "Rewrites chunk rendering. The biggest FPS boost you can get."),
            ("lithium", "Lithium", "Speeds up physics, mob AI and ticking. Great in singleplayer and big farms."),
            ("entityculling", "Entity Culling", "Skips entities and block entities hidden behind walls."),
            ("ferrite-core", "FerriteCore", "Cuts memory use a lot, so fewer stutters from garbage collection."),
            ("immediatelyfast", "ImmediatelyFast", "Faster HUD, text and entity rendering. Pairs well with Larp's HUD."),
            ("modernfix", "ModernFix", "Faster startup and lower memory use."),
            ("moreculling", "More Culling", "Skips block faces you can't see, like leaves."),
            ("iris", "Iris Shaders", "Runs shaderpacks on top of Sodium, if you want shaders.")]
    perf_rows = "".join(f'<tr><td><a href="https://modrinth.com/mod/{s}" target="_blank" rel="noopener">{n}</a></td><td>{d}</td></tr>' for s, n, d in perf)
    page("performance", "Performance", "Help", "performance",
         "Get the most FPS out of Larp Client.",
         f"""
<h2 id="built-in">What Larp does for you</h2>
<ul>
<li>{mlink('Performance')} caps your FPS in menus, while AFK and when the game isn't focused. It never touches the FPS limit in Options.</li>
<li>{mlink('FPS Boost')} turns heavy video settings down (entity shadows, clouds, biome blend, entity distance, view bobbing) and restores your exact values when you turn it off.</li>
<li>Cosmetics are cached and rebuilt at a set rate (see <a href="/docs/cosmetics#performance">Cosmetics</a>).</li>
<li>Text widths, icons and module lookups are cached, and the menus draw in a few batches.</li>
</ul>
<h2 id="performance-settings">Performance settings</h2>
{settings_table(by['Performance'])}
<h2 id="recommended-mods">Recommended mods</h2>
<p>Put these in the same <code>mods</code> folder. All are on Modrinth; download the {MC} Fabric version of each.</p>
<div class="table-wrap"><table><tbody>{perf_rows}</tbody></table></div>
{callout('tip', 'Start with Sodium, Lithium and Entity Culling. They give most of the gain and rarely conflict with anything.')}
<h2 id="settings-tips">Video settings that matter</h2>
<ul>
<li><b>Render distance</b> costs the most. 10–12 chunks is plenty for PvP.</li>
<li><b>Simulation distance</b> 5–8 for multiplayer.</li>
<li>Give Minecraft 4 GB of RAM. More doesn't make it faster and can cause longer pauses.</li>
</ul>
""")

    faq_extra = "".join(f'<h3 id="{re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")}">{q}</h3><p>{a}</p>' for q, a in FAQ)
    page("faq", "FAQ", "Help", "info", "Answers to common questions.", faq_extra)

    page("troubleshooting", "Troubleshooting", "Help", "warning2",
         "Fixes for the most common problems.",
         f"""
<h2 id="crash-on-start">The game crashes on start</h2>
<ul>
<li>Check that Fabric API is the <b>{MC}</b> version and that there's only one copy of it.</li>
<li>Check you're launching the Fabric {MC} profile, not vanilla or another version.</li>
<li>Remove other mods to find a conflict, especially ones that change the title screen, menus or HUD.</li>
<li>The crash report is in <code>.minecraft/crash-reports</code>; the latest log is <code>.minecraft/logs/latest.log</code>.</li>
</ul>
<h2 id="menu-wont-open">The menu doesn't open</h2>
<p>Another mod may use <kbd>Right Shift</kbd>. Change the key in Options → Controls → Larp Client, or use the <b>Client</b> button on the title screen.</p>
<h2 id="low-fps">Low FPS</h2>
<p>Install the <a href="/docs/performance#recommended-mods">recommended mods</a>, turn on {mlink('FPS Boost')}, lower <b>Cosmetic FPS</b> to 30 and turn on <b>Reduced menu effects</b> in Settings.</p>
<h2 id="cosmetics-missing">I can't see my cosmetics</h2>
<p>Press <kbd>F5</kbd>: cosmetics are hidden in first person unless you turn on <b>Show in first person</b> in their settings. Other players don't see them.</p>
<h2 id="rpc-not-showing">Discord status doesn't show</h2>
<ul>
<li>Use the Discord desktop app, not the browser.</li>
<li>In Discord, turn on User Settings → Activity Privacy → <b>Share my activity</b>.</li>
<li>Check the Application ID and that the asset is named exactly <code>logo</code>.</li>
</ul>
<h2 id="settings-reset">My settings reset</h2>
<p>If the game closes by crashing, the last changes may not be saved. Save a <a href="/docs/profiles">profile</a> as a backup.</p>
""")

    log = [
        ("0.9.5", "Performance and fixes", [
            "3D cosmetics, kill effects and target markers cache their geometry. New <b>Cosmetic FPS</b> setting (30, 60, 120, Max).",
            "Faster module lookups and cached text and icon sizes in every menu.",
            "Performance and FPS Boost no longer save their temporary values into your options while the Options screen is open.",
            "Kill Effect only plays for your own kills.",
        ]),
        ("0.9.4", "Visual refresh", ["Polished visuals across the menu, module pages and sections."]),
        ("0.9.3", "Hotbar Keybinds", ["New <b>Hotbar Keybinds</b>: the key bound to each slot, shown on the hotbar and in inventories.", "More HUD and PvP modules."]),
        ("0.9.1 – 0.9.2", "Hitboxes and Discord", ["New <b>Hitboxes</b>: clean custom hitboxes instead of F3+B.", "Discord RPC shows Larp Client, the server and the game version, with a logo and no background.", "The crown on the Info Bar sits on the R and is smaller."]),
        ("0.9.0", "3D cosmetics", ["New cosmetics engine: 8 wing styles, 22 hats, auras, kill effects and target markers.", "Your name and an underline above the title-screen character.", "A crown on your name in the Info Bar."]),
        ("0.8.0", "New menu", ["New client menu with a sidebar, centered tabs, mod cards and full settings pages.", "Separate Visuals and RPC pages, plus Settings and Edit HUD buttons.", "Fluid curtains on the title screen and a clean loading screen."]),
        ("0.7.x", "Title screen", ["New title screen with a small player on the left and a Client button.", "Album covers in the Music Player load reliably."]),
    ]
    log_html = "".join(f'<h2 id="v{re.sub(r"[^0-9a-z]+", "-", v)}">{v} <span style="color:var(--dim);font-weight:400">· {t}</span></h2><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul>" for v, t, items in log)
    page("changelog", "Changelog", "Help", "update", "What changed in each version of Larp Client.", log_html)

    page("credits", "Credits", "Help", "favorite",
         "Open source projects Larp Client is built with.",
         """
<div class="table-wrap"><table><thead><tr><th>Project</th><th>Used for</th><th>License</th></tr></thead><tbody>
<tr><td><a href="https://fabricmc.net" target="_blank" rel="noopener">Fabric</a></td><td>Mod loader and API</td><td>Apache 2.0</td></tr>
<tr><td>Clarity</td><td>The 3D engine behind wings, hats, auras, kill effects and target markers</td><td>CC0 1.0</td></tr>
<tr><td><a href="https://fonts.google.com/icons" target="_blank" rel="noopener">Material Icons</a></td><td>Icons in the client and this site</td><td>Apache 2.0</td></tr>
<tr><td><a href="https://rsms.me/inter/" target="_blank" rel="noopener">Inter</a></td><td>Font in the client and this site</td><td>SIL OFL 1.1</td></tr>
</tbody></table></div>
<p>Minecraft is a trademark of Mojang AB. Larp Client is not affiliated with Mojang or Microsoft.</p>
""")

    # ---------------- Render ----------------
    groups = []
    for p in pages:
        if p["group"] not in groups:
            groups.append(p["group"])
    search = []

    def toc_of(body):
        out = []
        for m in re.finditer(r'<h([23])[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>', body, re.S):
            text = re.sub(r"<[^>]+>", "", m.group(3)).strip()
            out.append((int(m.group(1)), m.group(2), text))
        return out

    def add_anchors(body):
        return re.sub(r'(<h([23])([^>]*)id="([^"]+)"([^>]*)>)(.*?)(</h\2>)',
                      lambda m: f'{m.group(1)}{m.group(6)}<a class="anchor" href="#{m.group(4)}" aria-label="Link to this section">#</a>{m.group(7)}', body, flags=re.S)

    for i, p in enumerate(pages):
        url = "/docs" + ("/" + p["slug"] if p["slug"] else "")
        side = []
        for gname in groups:
            links = "".join(f'<a href="/docs{("/" + q["slug"]) if q["slug"] else ""}"{" aria-current=\"page\"" if q is p else ""}>{icon(q["icon"])}{q["title"]}</a>' for q in pages if q["group"] == gname)
            side.append(f'<div class="dgroup"><h4>{gname}</h4>{links}</div>')
        toc = toc_of(p["body"])
        toc_html = ""
        if toc and p["slug"] != "modules":
            toc_html = "<h4>On this page</h4>" + "".join(f'<a class="{"sub" if lv == 3 else ""}" href="#{hid}">{esc(t)}</a>' for lv, hid, t in toc)
        elif p["slug"] == "modules":
            toc_html = "<h4>Sections</h4>" + "".join(f'<a href="#cat-{c.lower()}">{l}</a>' for c, l in CATS)
        prev_p, next_p = (pages[i - 1] if i > 0 else None), (pages[i + 1] if i + 1 < len(pages) else None)
        purl = lambda q: "/docs" + ("/" + q["slug"] if q["slug"] else "")
        pager = '<nav class="pager" aria-label="Pages">' + \
            (f'<a href="{purl(prev_p)}"><span>Previous</span><b>{prev_p["title"]}</b></a>' if prev_p else "") + \
            (f'<a class="next" href="{purl(next_p)}"><span>Next</span><b>{next_p["title"]}</b></a>' if next_p else "") + "</nav>"
        body = add_anchors(p["body"])
        doc = head(p["title"] if p["slug"] else "Docs", p["desc"], url, '\n<link rel="stylesheet" href="/assets/css/docs.css">')
        doc += nav("docs")
        doc += f"""<div class="docs">
<aside class="dside" aria-label="Docs navigation">
  <div class="dsearch">{icon('search')}<input type="search" placeholder="Search docs" aria-label="Search docs" data-dsearch autocomplete="off"><kbd>/</kbd><div class="dresults" hidden></div></div>
  {''.join(side)}
</aside>
<main class="dmain" id="main">
  <button type="button" class="dside-toggle" aria-expanded="false">{icon('menu')}Docs menu</button>
  <div class="crumbs"><a href="/docs">Docs</a>{icon('chevron_right')}<span>{p['group']}</span></div>
  <h1>{p['title']}</h1>
  <p class="intro">{p['desc']}</p>
  <div class="prose">{body}</div>
  {pager}
  <p class="edited">Larp Client {V} · Minecraft {MC}</p>
</main>
<nav class="dtoc" aria-label="On this page">{toc_html}</nav>
</div>
"""
        doc += footer('\n<script src="/assets/js/docs.js" defer></script>')
        out = ROOT / ("docs/index.html" if not p["slug"] else f"docs/{p['slug']}.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc)

        plain = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()
        search.append({"t": p["title"], "u": url, "x": p["desc"]})
        if p["slug"] != "modules":
            for lv, hid, t in toc:
                search.append({"t": t, "u": f"{url}#{hid}", "x": p["title"]})
    for m in MODS:
        search.append({"t": m["name"], "u": f"/docs/modules#{m['id']}", "x": m["description"], "k": " ".join(s["name"] for s in m["settings"])})
    (ROOT / "assets/data/search.json").write_text(json.dumps(search, separators=(",", ":")))
    print(len(pages), "docs pages,", len(search), "search entries")
