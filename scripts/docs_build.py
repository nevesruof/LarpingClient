"""Generate searchable feature guides and the current module reference."""
import html,json,re
from content_updates import UPDATES,NEW_PAGES
esc=html.escape

def build(g):
 root,cfg,mods,icon,head,nav,footer,cats=[g[k] for k in ['ROOT','CFG','MODS','icon','head','nav','footer','CATS']]
 cosmetic=g['cosmetics_data']()
 gallery=lambda key:'<div class="gallery">'+''.join(f'<figure><img src="{i["src"]}" alt="{esc(i["name"])}" loading="lazy" width="118" height="118"><figcaption>{esc(i["name"])}</figcaption></figure>' for i in cosmetic[key]['items'])+'</div>'
 bodies=dict(UPDATES)
 bodies['cosmetics']='''<h2 id="local">Your own view of the world</h2><p>Cosmetics are rendered locally. Use third-person view to see your own character. Color, scale and behavior are adjustable in the client; available options depend on the cosmetic.</p><h2 id="wings">Wings</h2><p>Eight styles, including Dragon, Angel, Butterfly, Crystal and Phoenix.</p>'''+gallery('wings')+'''<h2 id="hats">Hats</h2><p>From antlers and ears to crowns and halos.</p>'''+gallery('hats')+'''<h2 id="aura">Auras</h2><p>Orbiting shapes, elemental effects and ground runes.</p>'''+gallery('aura')+'''<h2 id="target">Target markers</h2><p>Target ESP is part of Visuals; its styles are shown here alongside the cosmetic renders.</p>'''+gallery('target')+'''<h2 id="motion">Movement and flight</h2><p>Cosmetic attachment transforms follow the player’s body, including Elytra poses. Different effects have their own animation and refresh controls. See <a href="/docs/performance">Performance</a> to tune your setup.</p>'''
 bodies['hud-editor']='''<h2 id="place">Put your information where you want it</h2><p>Open Edit HUD in the client menu. Drag widgets into place and use snapping guides for alignment. Fine adjustments can be made with the arrow keys.</p><h2 id="style">Make it readable</h2><p>HUD modules include controls for scale, background, text color and font. Some widgets have layout, graph or compact-display options.</p><h2 id="music">A cohesive setup</h2><p>Bring together Music Player, Lyrics, coordinates, armor, potion effects and the information you actually use. Save a profile when you are happy with the arrangement.</p><h2 id="performance">Watch your frame times</h2><p>The new <a href="/docs/performance">Performance Monitor</a> helps you compare layouts and enabled effects in the same scene.</p>'''
 bodies['waypoints']='''<h2 id="create">Remember a place</h2><p>Open Waypoints in the client menu, add a name and enter the coordinates. You can organize and remove saved points from the same page.</p><h2 id="scope">World and dimension</h2><p>Waypoints are stored locally for your setup. Check the world and dimension when a marker appears in an unexpected place.</p><h2 id="files">Back up your points</h2><p>Saved data lives in <code>config/larpclient-waypoints.json</code>. Copy it with your configuration when moving to another Minecraft instance.</p>'''
 bodies['troubleshooting']='''<h2 id="startup">Minecraft does not start</h2><p>Use Minecraft 1.21.11, Java 21, Fabric Loader 0.20.1+ and matching Fabric API. Remove duplicate Larp JARs. Keep the latest log when asking for help.</p><h2 id="performance">Frame times are high</h2><p>Enable the Performance Monitor, compare the same scene and disable effects one at a time. Recording, blur, shaders and high effect counts have a cost. See <a href="/docs/performance">the performance guide</a>.</p><h2 id="clips">Replay did not save</h2><p>Wait for the 30-second buffer, leave 10 seconds between save requests, check disk space and confirm Recorder is stopped. Read the capture notification for an audio-device or encoder error.</p><h2 id="audio">No audio or media information</h2><p>Desktop media features require Windows. Check the active output device and media session. Instant Replay uses the default output device and does not capture a microphone.</p><h2 id="rpc">Discord presence is missing</h2><p>Use the Discord desktop app and review activity visibility. The application identity is built in; there is no Application ID field you need to fill.</p><h2 id="lyrics">Lyrics are unavailable</h2><p>Verify the title and artist reported by your player. LRCLIB may not have the same recording, an instrumental track or synchronized lines.</p><h2 id="keys">A key does nothing</h2><p>Check for conflicting keybinds in Minecraft Controls. The module must be enabled, and some actions require a world or an inventory to be open.</p>'''
 meta=[('', 'Introduction','Getting started','home','A visual client that feels like your own.'),('installation','Installation','Getting started','download','Get set up with Larp Client 0.14.1.'),('client-menu','The client menu','Getting started','modules','Your modules, preferences and personal setup.'),('keybinds','Keybinds','Getting started','keybinds','Useful defaults and your own shortcuts.'),('hud-editor','HUD editor','Features','edithud','Make room for the information you use.'),('cosmetics','Cosmetics','Features','wings','Actual renders of wings, hats, auras and markers.'),('waypoints','Waypoints','Features','waypoints','Keep the places you want to come back to.'),('macros','Macros','Features','macros','Commands triggered by keys and supported game events.'),('discord-rpc','Discord RPC','Features','rpc','Built-in identity, with status details you choose.'),('music-player','Music player','Features','music','Your Windows media session, inside Minecraft.'),('profiles','Profiles & settings','Features','layers','Save a setup, remove a profile or start fresh.')]
 for slug,title,ic,desc,body in NEW_PAGES:meta.append((slug,title,'Features',ic,desc));bodies[slug]=body
 meta += [('modules','All modules','Reference','modules',f'{len(mods)} registered modules, with settings from the client source.'),('performance','Performance','Help','performance','Understand the cost of your setup.'),('faq','FAQ','Help','info','A few things to know before you play.'),('troubleshooting','Troubleshooting','Help','warning2','Find a clear starting point when something goes wrong.'),('changelog','Changelog','Help','update','The 0.14 release line and recent refinements.'),('credits','Credits','Help','favorite','Projects, fonts, icons and imagery behind Larp.')]
 def settings_table(module):
  rows=[]
  for s in module['settings']:
   kind=s['type'];default=s.get('default')
   if kind=='bool':value='On' if default else 'Off'
   elif kind=='number':value=f'{default:g} ({s["min"]:g} to {s["max"]:g})' if default is not None and 'min' in s else 'Adjustable slider'
   elif kind=='mode':value=' · '.join(str(x) for x in dict.fromkeys(s.get('options',[]))) or 'In-client selector'
   elif kind=='color':value=str(default or 'Custom color picker')
   else:value=str(default or 'Editable text')
   rows.append(f'<tr><td>{esc(s["name"])}</td><td>{esc(value)}</td><td>{esc(s.get("group") or "General")}</td></tr>')
  return '<div class="table-wrap"><table><thead><tr><th>Setting</th><th>Default / options</th><th>Section</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>' if rows else '<p>Use the module options and Minecraft Controls for available actions.</p>'
 sections=[]
 for category,label in cats:
  cards=[]
  for m in mods:
   if m['category']!=category:continue
   badges='<span class="new-badge">NEW</span>' if m.get('new') else ''
   text=esc((m['name']+' '+m['description']+' '+' '.join(s['name'] for s in m['settings'])).lower())
   cards.append(f'<details class="mod" id="{m["id"]}" data-cat="{category}" data-text="{text}"><summary><span class="mi">{icon(m["id"])}</span><span class="mt"><b>{esc(m["name"])} {badges}</b><span>{esc(m["description"])}</span></span><span class="mm">{icon("expand")}</span></summary><div class="mbody">{settings_table(m)}</div></details>')
  sections.append(f'<h2 class="mcat" data-cat="{category}" id="cat-{category.lower()}">{label} <span>{len(cards)}</span></h2>'+''.join(cards))
 bodies['modules']='<div class="mod-tools"><label class="mod-search">'+icon('search')+'<input type="search" placeholder="Find a module or setting…" aria-label="Filter module reference" data-msearch></label><div class="mod-filters">'+''.join(f'<button data-f="{key}" class="'+('on' if key=='all' else '')+f'">{label}</button>' for key,label in [('all','All')]+cats)+'</div></div><p class="mod-count" data-mcount></p>'+''.join(sections)+'<p class="mod-empty" hidden>No modules found.</p>'
 groups=list(dict.fromkeys(m[2] for m in meta));search=[]
 url=lambda slug:'/docs'+('/'+slug if slug else '')
 for index,(slug,title,group,ic,desc) in enumerate(meta):
  body=bodies[slug].replace('{module_count}',str(len(mods)))
  toc=[(int(a),b,re.sub('<[^>]+>','',c)) for a,b,c in re.findall(r'<h([23])[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>',body,re.S)]
  sidebar=''.join('<div class="dgroup"><h4>'+name+'</h4>'+''.join(f'<a href="{url(s)}"'+(' aria-current="page"' if s==slug else '')+f'>{icon(i)}{t}</a>' for s,t,gr,i,d in meta if gr==name)+'</div>' for name in groups)
  anchors=lambda match:match[0]+f'<a class="anchor" href="#{match[2]}" aria-label="Link to this section">#</a>'
  body=re.sub(r'<h([23])[^>]*id="([^"]+)"[^>]*>.*?(?=</h\1>)',anchors,body,flags=re.S)
  toc_html='<h4>On this page</h4>'+''.join(f'<a href="#{anchor}">{esc(t)}</a>' for level,anchor,t in toc)
  pager=''
  for neighbor,label in [(index-1,'Previous'),(index+1,'Next')]:
   if 0<=neighbor<len(meta):
    target=meta[neighbor];pager+=f'<a class="'+('next' if label=='Next' else '')+f'" href="{url(target[0])}"><span>{label}</span><b>{target[1]}</b></a>'
  content=f'''<div class="docs"><aside class="dside" id="docs-nav" aria-label="Documentation navigation"><button class="docs-menu-close" type="button" data-close-docs>Close navigation ×</button><div class="dsearch">{icon('search')}<input type="search" placeholder="Search docs" aria-label="Search documentation" data-dsearch role="combobox" aria-expanded="false" aria-controls="docs-search-results" aria-autocomplete="list" autocomplete="off"><kbd>/</kbd><div class="dresults" id="docs-search-results" role="listbox" hidden></div></div>{sidebar}</aside><main class="dmain" id="main"><button class="dside-toggle" type="button" aria-expanded="false" aria-controls="docs-nav">{icon('menu')}Docs menu</button><div class="crumbs"><a href="/docs">Docs</a>{icon('arrow')}<span>{group}</span></div><h1>{title}</h1><p class="intro">{desc}</p><div class="prose">{body}</div><nav class="pager" aria-label="Documentation pages">{pager}</nav><p class="edited">Larp Client {cfg['version']} · Minecraft {cfg['minecraft']}</p></main><nav class="dtoc" aria-label="On this page">{toc_html}</nav></div>'''
  html_doc=head(title,desc,url(slug),'\n<link rel="stylesheet" href="'+g['asset']('/assets/css/docs.css')+'">')+nav('docs')+content+footer('<script src="'+g['asset']('/assets/js/docs.js')+'" defer></script>')
  target=root/'docs'/((slug or 'index')+'.html');target.parent.mkdir(exist_ok=True);target.write_text(html_doc)
  search.append(dict(t=title,u=url(slug),x=desc))
  for level,anchor,t in toc:search.append(dict(t=t,u=url(slug)+'#'+anchor,x=title))
 for m in mods:search.append(dict(t=m['name'],u='/docs/modules#'+m['id'],x=m['description'],k=' '.join(s['name'] for s in m['settings'])))
 (root/'assets/data/search.json').write_text(json.dumps(search,separators=(',',':')))
 print(len(meta),'documentation pages,',len(search),'search entries')
