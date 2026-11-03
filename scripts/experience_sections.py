"""Focused, source-backed ways to explore the existing client."""
from html import escape
from website_details import avatar, item_image


def module_explorer(g):
    icon, mods, cats = (g[k] for k in ['icon', 'MODS', 'CATS'])
    filters = ''.join(f'<button type="button" data-explore-category="{key}" aria-pressed="false">{label}<small>{sum(m["category"] == key for m in mods)}</small></button>' for key, label in cats)
    cards = ''
    # Useful even when scripting is unavailable; the complete reference is always linked.
    for mid in ['instantreplay', 'lyrics', 'shulkerpreview', 'killeffect', 'performancemonitor', 'musicbeats']:
        m = next(m for m in mods if m['id'] == mid)
        badge = '<span class="new-badge">NEW</span>' if m.get('new') else ''
        cards += f'<a class="explore-card" href="/docs/modules#{m["id"]}"><span class="explore-card-top">{icon(m["id"])}<small>{escape(dict(cats)[m["category"]])}</small>{badge}</span><h3>{escape(m["name"])}</h3><p>{escape(m["description"])}</p><span class="explore-card-bottom">{len(m["settings"])} settings<span>Explore {icon("arrow")}</span></span></a>'
    return f'''<section class="section explore-section" id="modules"><div class="wrap">
      <div class="experience-head"><div><span class="section-label">FIND YOUR ESSENTIALS <span class="new-badge">NEW ON THE WEB</span></span><h2>Less scrolling.<br>More finding your thing.</h2></div><p>{len(mods)} modules. Six categories. Search by a name, an idea or a setting, and go straight to the details.</p></div>
      <div class="explore-toolbar"><label class="explore-search">{icon('search')}<input type="search" data-explore-search aria-label="Search module explorer" placeholder="Try wings, audio, crosshair…" autocomplete="off"></label><button class="explore-new" type="button" data-explore-new aria-pressed="false">{icon('update')}New additions</button></div>
      <div class="explore-filters" role="group" aria-label="Module categories"><button type="button" data-explore-category="all" aria-pressed="true">All<small>{len(mods)}</small></button>{filters}</div>
      <div class="explore-meta"><p data-explore-count role="status" aria-live="polite">A few favorites to start with.</p><button type="button" data-explore-clear hidden>Clear filters ×</button></div>
      <div class="explore-grid" data-explore-grid>{cards}</div>
      <div class="explore-empty" data-explore-empty hidden><span>{icon('search')}</span><h3>Nothing here yet.</h3><p>Try a shorter search or another category.</p><button class="btn btn-glass btn-sm" type="button" data-explore-reset>Show all modules</button></div>
      <div class="explore-foot"><button class="btn btn-glass btn-sm" type="button" data-explore-more hidden>Show more modules {icon('expand')}</button><a href="/docs/modules">The complete reference {icon('arrow')}</a></div>
    </div></section>'''


def style_lab(g):
    icon = g['icon']
    slots = ''.join(item_image(n, label) for n, label in [('diamond_sword', 'Diamond sword'), ('ender_pearl', 'Ender pearl'), ('golden_apple', 'Golden apple'), ('bow', 'Bow')])
    return f'''<section class="section lab-section" id="style-lab"><div class="wrap">
      <div class="section-head"><span class="section-label">A LITTLE MORE YOU <span class="new-badge">NEW ON THE WEB</span></span><h2>Find your shade of larp.</h2><p>Different accent. Different scale. Same world. Put together a look before you open the client.</p></div>
      <div class="style-lab" data-style-lab>
        <div class="lab-scene" data-lab-scene><span class="lab-scene-tag">STYLE PREVIEW / NOT GAMEPLAY</span><div class="lab-scene-center"><img src="/assets/img/logo.svg" width="52" height="52" alt=""><span>Your world. Your point of view.</span></div>
          <div class="lab-widget"><div class="lab-player">{avatar('FastL_ player head')}<span><b>FastL_</b><small>mc.hypixel.net</small></span><span class="lab-health">20 / 20</span></div><div class="lab-health-bar"><i></i></div><div class="lab-coordinates" data-lab-coordinates>{icon('coordinates')}<span>X 128</span><span>Y 64</span><span>Z −32</span></div></div>
          <div class="lab-hotbar">{slots}<span>1 &nbsp; 2 &nbsp; 3 &nbsp; 4</span></div><span class="lab-scene-bottom">Vanilla Minecraft panorama · local preview</span>
        </div>
        <div class="lab-controls"><span class="detail-kicker">THE STYLE LAB</span><h3>Small changes.<br> Your kind of clean.</h3><label class="lab-field-title">Accent <output data-lab-hex>#B5A3E8</output></label><div class="lab-swatches" role="group" aria-label="HUD accent"><button type="button" data-lab-accent="#b5a3e8" style="--swatch:#b5a3e8" aria-label="Lavender accent" aria-pressed="true"></button><button type="button" data-lab-accent="#9acbdb" style="--swatch:#9acbdb" aria-label="Ice accent" aria-pressed="false"></button><button type="button" data-lab-accent="#e9ad91" style="--swatch:#e9ad91" aria-label="Ember accent" aria-pressed="false"></button><button type="button" data-lab-accent="#aac7a3" style="--swatch:#aac7a3" aria-label="Sage accent" aria-pressed="false"></button><label class="lab-custom" title="Choose your own accent">+<input type="color" value="#b5a3e8" data-lab-color aria-label="Custom HUD accent"></label></div>
          <label class="lab-field-title" for="lab-scale">Widget scale <output data-lab-scale-label>100%</output></label><input type="range" id="lab-scale" min="80" max="115" value="100" data-lab-scale>
          <label class="lab-check"><span>Compact layout</span><input type="checkbox" data-lab-compact></label><label class="lab-check"><span>Coordinates</span><input type="checkbox" data-lab-coords checked></label>
          <div class="lab-buttons"><button type="button" class="btn btn-light btn-sm" data-lab-copy>Copy style {icon('copy')}</button><button type="button" class="lab-reset" data-lab-reset>Reset</button></div><p class="lab-status" data-lab-status role="status" aria-live="polite">Preview only. Apply your choices in the client.</p><textarea class="lab-copy-fallback" data-lab-fallback aria-label="Style values to copy manually" readonly hidden></textarea>
        </div>
      </div>
    </div></section>'''


def effect_spotlight(g):
    icon = g['icon']
    # Code-native graphic for a lightweight, symbolic preview, not a game capture.
    shark = '<svg viewBox="0 0 300 160" class="effect-shark" aria-hidden="true"><path d="M25 91C65 54 125 58 153 55L181 12L189 59C217 65 231 77 245 84L286 58L274 95L292 123L245 107C217 128 188 132 155 125L123 149L128 122C87 119 55 113 25 91Z" fill="currentColor"/><path d="M57 95Q96 119 142 98" fill="none" stroke="#080a10" stroke-width="6"/><circle cx="70" cy="80" r="4" fill="#080a10"/><path d="M159 76l-7 27m18-23-7 26m18-21-7 23" stroke="#080a10" stroke-width="3" opacity=".4"/><path d="M125 146h30l6-12h-30zm53-2h29l8-12h-30z" fill="#85aecf"/></svg>'
    pieces = ''.join(f'<i style="--piece:{i};--dx:{(-1 if i % 2 else 1) * (45 + i * 8)}px;--dy:{(-1 if i < 3 else 1) * (24 + i * 9)}px;--turn:{(-1 if i % 2 else 1) * (12 + i * 6)}deg"></i>' for i in range(6))
    return f'''<section class="section effect-section" id="kill-effects"><div class="wrap"><div class="effect-layout">
      <div class="effect-copy"><span class="section-label">THE FINISHING TOUCH <span class="new-badge">NEW ON THE WEB</span></span><h2>Two endings.<br>Your call.</h2><p>Samurai or Tralalero. Choose one effect for a player kill and keep the rest of your setup your own.</p><div class="effect-choice" role="group" aria-label="Kill effect demonstration"><button type="button" data-effect="samurai" aria-pressed="true">01 <b>Samurai</b></button><button type="button" data-effect="tralalero" aria-pressed="false">02 <b>Tralalero</b></button></div><p class="effect-description" data-effect-description>A sharp cut. A brief burst. Then back to the game.</p><a class="detail-link" href="/docs/kill-effects">Explore Kill Efects options {icon('arrow')}</a></div>
      <div class="effect-study" data-effect-study data-effect-mode="samurai"><div class="effect-study-head"><span>AN INTERACTION STUDY</span><span data-effect-caption>SAMURAI</span></div><div class="effect-arena"><div class="effect-grid"></div><div class="effect-mark">{pieces}</div><div class="effect-slash"></div>{shark}<span class="effect-spark">✦</span></div><div class="effect-study-foot"><span>Stylized web preview<br><small>Actual effects render in Minecraft.</small></span><button type="button" class="btn btn-glass btn-sm" data-effect-play>{icon('play')}Play effect</button></div><p class="effect-result sr-only" data-effect-result role="status" aria-live="polite"></p></div>
    </div></div></section>'''


def session_guide(g):
    icon = g['icon']
    tasks = [
        ('access', 'Get your invite.', 'Larp is private. Request the client from iTake.', '/#access', 'Access details'),
        ('install', 'Build a clean start.', 'Minecraft 1.21.11, Java 21, Fabric and the matching Fabric API.', '/docs/installation', 'Installation guide'),
        ('layout', 'Keep what you use.', 'Place your HUD, choose your modules and save a profile.', '/docs/hud-editor', 'Arrange your HUD'),
        ('capture', 'Make the first moment count.', 'Choose your clip key and check your Windows audio output.', '/docs/instant-replay', 'Set up your clips'),
    ]
    rows = ''.join(f'<article class="session-task"><label><input type="checkbox" data-session-task="{key}"><span class="session-check">{icon("check")}</span><span><small>0{i+1}</small><b>{title}</b><span>{description}</span></span></label><a href="{href}" aria-label="{link}">{icon("arrow")}</a></article>' for i, (key, title, description, href, link) in enumerate(tasks))
    return f'''<section class="section session-section" id="first-session"><div class="wrap"><div class="session-layout"><div class="session-intro"><span class="section-label">YOUR FIRST SESSION <span class="new-badge">NEW ON THE WEB</span></span><h2>From hello<br>to your own setup.</h2><p>A short list for a good start. Tick things off as you go; your checklist stays in this browser.</p><div class="session-progress"><span data-session-progress role="status" aria-live="polite">0 of 4 ready</span><span class="session-progress-track"><i data-session-progress-bar></i></span></div><button type="button" data-session-reset>Reset checklist</button><p class="session-storage-note" data-session-note></p></div><div class="session-tasks">{rows}</div></div></div></section>'''


def field_notes(g):
    icon = g['icon']
    notes = [
        ('performance', '01 / FRAME TIMES', 'A smoother session starts with a comparison.', 'Keep the scene the same. Change one effect. Compare frame times with Performance Monitor.', '/docs/performance', 'Tune your setup'),
        ('music', '02 / YOUR SOUNDTRACK', 'Let the song find its place.', 'Your media session, LRCLIB lyrics and a layout that leaves room for the world.', '/docs/lyrics', 'Style your lyrics'),
        ('layers', '03 / THE LITTLE BACKUP', 'A good layout deserves a second copy.', 'Save a profile before experimenting. Keep your configuration when moving between instances.', '/docs/profiles', 'Keep your setup'),
    ]
    cards = ''.join(f'<a class="field-note" href="{href}"><span class="field-note-icon">{icon(ic)}</span><small>{number}</small><h3>{title}</h3><p>{text}</p><span class="field-note-link">{label}{icon("arrow")}</span></a>' for ic, number, title, text, href, label in notes)
    return f'<section class="section notes-section" id="field-notes"><div class="wrap"><div class="section-head"><span class="section-label">A FEW FIELD NOTES <span class="new-badge">NEW ON THE WEB</span></span><h2>Good looks. Better habits.</h2><p>Three small things worth getting right.</p></div><div class="field-notes">{cards}</div></div></section>'


def search_dialog(g):
    icon = g['icon']
    return f'''<dialog class="quick-search" data-quick-search aria-labelledby="quick-search-title"><div class="quick-search-head"><h2 id="quick-search-title">Find your way.</h2><button type="button" data-search-close aria-label="Close quick search">{icon('close')}</button></div><label class="quick-search-input">{icon('search')}<input type="search" data-quick-input aria-label="Search pages and modules" placeholder="Pages, modules, settings…" autocomplete="off" maxlength="120"></label><p class="quick-search-count" data-quick-count role="status" aria-live="polite">Quick links</p><div class="quick-search-results" data-quick-results><a href="/#modules"><span>Module explorer<small>Find your essentials</small></span>{icon('arrow')}</a><a href="/#style-lab"><span>Style lab<small>Try a different accent</small></span>{icon('arrow')}</a><a href="/docs/installation"><span>Installation<small>Your first session</small></span>{icon('arrow')}</a><a href="/docs/instant-replay"><span>Instant Replay<small>Your last 30 seconds, with sound</small></span>{icon('arrow')}</a></div><div class="quick-search-foot"><span><kbd>↑</kbd><kbd>↓</kbd> to move <kbd>↵</kbd> to open</span><span><kbd>Esc</kbd> to close</span></div></dialog>'''
