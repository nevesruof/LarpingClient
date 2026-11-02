"""Real Minecraft assets and focused feature demonstrations for the landing."""
from html import escape

ITEMS = [
    ('diamond_sword', 'Diamond sword'), ('bow', 'Bow'),
    ('golden_apple', 'Golden apple'), ('ender_pearl', 'Ender pearl'),
    ('totem_of_undying', 'Totem of Undying'), ('water_bucket', 'Water bucket'),
    ('cooked_beef', 'Steak'), ('firework_rocket', 'Firework rocket'), ('arrow', 'Arrow'),
]


def item_image(name, label, **attrs):
    extra = ' '.join(f'{k}="{escape(str(v))}"' for k, v in attrs.items())
    return f'<img src="/assets/img/minecraft/{name}.png" alt="{escape(label)}" width="16" height="16" loading="lazy" draggable="false" {extra}>'


def avatar(label='Player head supplied by iTake'):
    return f'<span class="player-avatar"><img src="/assets/img/player-head.png" alt="{label}" width="1111" height="1111" loading="lazy" draggable="false"></span>'


def hud_preview(g):
    icon, cfg = g['icon'], g['CFG']
    binds = ['1', '2', '3', '4', 'G', 'R', '7', '8', '9']
    slots = ''.join(f'<span class="{"sel" if i == 0 else ""}" title="{label}">{item_image(name, label)}<b>{bind}</b></span>'
                    for i, ((name, label), bind) in enumerate(zip(ITEMS, binds)))
    return f'''<div class="hud-scene">
      <div class="grid"></div><div class="guide v"></div><div class="guide h"></div>
      <div class="hud-el hud-box infobar" style="left:14px;top:14px">
        <span>{avatar()}<span class="name">{escape(cfg['author'])}</span></span>
        <span class="muted">mc.hypixel.net</span><span>144 FPS</span><span class="muted">12:48</span>
      </div>
      <div class="hud-el modlist" style="right:14px;top:92px"><div>Target HUD</div><div>Keystrokes<small>Clean</small></div><div>Hit FX<small>White</small></div><div>Performance</div><div>Wings<small>Angel</small></div><div>Zoom</div></div>
      <div class="hud-el keys" style="left:20px;top:43%">
        <span class="key-w" data-k="W">W</span>
        <span class="key-a" data-k="A">A</span><span class="key-s" data-k="S">S</span><span class="key-d" data-k="D">D</span>
        <div class="mouse"><span data-k="LMB">LMB</span><span data-k="RMB">RMB</span></div>
        <span class="wide" data-k="Space">―</span>
      </div>
      <div class="hud-el hud-box target" style="left:20px;top:88px">
        {avatar('FastL_ player head')}<div class="info"><div class="row"><b>FastL_</b><span>3.1m</span></div><div class="row"><span>12.8 ❤</span><span class="heal">+4.2</span></div><div class="hp"><i></i></div></div>
      </div>
      <div class="hud-el hotbar" style="left:50%;bottom:22px;transform:translateX(-50%)">{slots}</div>
      <div class="hud-hint">{icon('edithud')}Drag to make it yours</div>
      <span class="hud-scene-note">Interactive HUD preview</span>
    </div>'''


def gallery(g):
    icon = g['icon']
    return f'''<section class="section world-section" id="gallery"><div class="wrap">
      <div class="section-head"><span class="section-label">IN YOUR WORLD</span><h2>Same Minecraft. Your atmosphere.</h2><p>A quieter HUD or a little more presence. Real gameplay from Larp, with a setup you control.</p></div>
      <div class="world-gallery">
        <figure class="world-shot"><img src="/assets/img/screenshots/night-1280.webp" srcset="/assets/img/screenshots/night-800.webp 800w, /assets/img/screenshots/night-1280.webp 1280w" sizes="(max-width: 760px) 100vw, 55vw" alt="Larp cosmetics and music beats glowing in a Minecraft forest at night" width="1280" height="673" loading="lazy"><figcaption><span><small>01 / AFTER DARK</small><b>A little louder, after sunset.</b></span><a href="/docs/cosmetics" aria-label="Explore Larp cosmetics">{icon('arrow')}</a></figcaption></figure>
        <figure class="world-shot"><img src="/assets/img/screenshots/aurora-1280.webp" srcset="/assets/img/screenshots/aurora-800.webp 800w, /assets/img/screenshots/aurora-1280.webp 1280w" sizes="(max-width: 760px) 100vw, 45vw" alt="Larp HUD, cape and aurora sky in Minecraft" width="1280" height="673" loading="lazy"><figcaption><span><small>02 / ALL YOURS</small><b>Every detail, in its place.</b></span><a href="#product" data-open-preview="t-hud" aria-label="Try the HUD editor">{icon('arrow')}</a></figcaption></figure>
      </div><div class="world-foot"><span>Captured in Minecraft with Larp Client.</span><a href="/docs/visuals">Explore visual modules {icon('arrow')}</a></div>
    </div></section>'''.replace('/docs/visuals', '/docs/modules#cat-visuals')


def details(g):
    icon = g['icon']
    contents = ITEMS + [('diamond', 'Diamond'), ('emerald', 'Emerald'), ('experience_bottle', 'Bottle o’ Enchanting')]
    slots = ''.join(f'<span>{item_image(*contents[i])}<small>{[1, 1, 16, 16, 1, 1, 64, 64, 64, 32, 24, 16][i]}</small></span>' if i < len(contents) else '<span></span>' for i in range(27))
    return f'''<section class="section detail-section" id="details"><div class="wrap">
      <div class="section-head"><span class="section-label">THE SMALL THINGS</span><h2>A better session is in the details.</h2><p>Useful when you need them. Out of the way when you don't.</p></div>
      <div class="detail-grid">
        <article class="detail-card shulker-card"><div class="detail-copy"><span class="detail-kicker">{icon('inventoryhud')}SHULKER PREVIEW <span class="new-badge">NEW</span></span><h3>Know what's inside.</h3><p>A real inventory preview, a color that matches the box, and a shortcut you choose.</p></div>
          <div class="shulker-demo" data-shulker-demo><div class="shulker-title"><b data-shulker-name>White Shulker Box</b><kbd>Shift</kbd></div><div class="shulker-slots">{slots}</div><div class="shulker-caption"><span>12 / 27 slots</span><span>Preview</span></div></div>
          <div class="shulker-controls" role="group" aria-label="Shulker preview color"><button type="button" data-shulker-color="white" aria-pressed="true"><i></i>White</button><button type="button" data-shulker-color="purple" aria-pressed="false"><i></i>Purple</button><button type="button" data-shulker-color="lime" aria-pressed="false"><i></i>Lime</button></div>
          <a class="detail-link" href="/docs/shulker-preview">A peek, without opening it {icon('arrow')}</a>
        </article>
        <article class="detail-card profile-card"><div class="detail-copy"><span class="detail-kicker">{icon('layers')}YOUR PROFILES</span><h3>A setup for every mood.</h3><p>Keep the essentials for a match. Bring the visuals back when it's time to wander.</p></div>
          <div class="setup-switch" role="group" aria-label="Example profile"><button type="button" data-setup="focus" aria-pressed="true">Focus</button><button type="button" data-setup="after-dark" aria-pressed="false">After dark</button><button type="button" data-setup="creator" aria-pressed="false">Creator</button></div>
          <div class="setup-demo" data-setup-demo><div class="setup-identity">{avatar()}<div><b>iTake</b><span>mc.hypixel.net</span></div><span class="setup-status">Focus</span></div><div class="setup-mods" data-setup-mods><span>Keystrokes</span><span>Target HUD</span><span>Toggle Sprint</span></div><p data-setup-description>Just the information you need for the next fight.</p></div>
          <a class="detail-link" href="/docs/profiles">Save it. Switch it. Make it yours {icon('arrow')}</a>
        </article>
        <a class="detail-guide" href="/docs/instant-replay"><span class="detail-guide-icon">{icon('play')}</span><span><b>The last 30 seconds. With sound.</b><small>A shortcut away from a clip worth keeping.</small></span><span class="guide-key">F8</span>{icon('arrow')}</a>
        <a class="detail-guide" href="/docs/lyrics"><span class="detail-guide-icon">{icon('music')}</span><span><b>Your soundtrack belongs here.</b><small>Lyrics, colors and a place in your world.</small></span>{icon('arrow')}</a>
      </div>
    </div></section>'''
