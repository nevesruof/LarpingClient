"""Check generated pages, internal routes, fragments, image text and catalog integrity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys
root=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.refs=[];self.issues=[];self.h1=0;self.lang=False;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.lang=bool(a.get('lang'))
  if tag=='h1':self.h1+=1
  if a.get('id'):self.ids.append(a['id'])
  if tag=='img' and 'alt' not in a:self.issues.append('Image without alt text')
  if tag=='button' and a.get('type','button') not in ['button','submit','reset']:self.issues.append('Invalid button type')
  for key in ['href','src']:
   value=a.get(key)
   if value and not value.startswith(('http:','https:','data:','mailto:','tel:','javascript:')):self.refs.append(value)
  if str(a.get('href','')).startswith('javascript:'):self.issues.append('Unsafe link')
  if a.get('target')=='_blank' and 'noopener' not in a.get('rel',''):self.issues.append('External window missing noopener')
files=[root/'index.html',root/'404.html',*sorted((root/'docs').glob('*.html'))]
parsed={p:Page(p.read_text()) for p in files};errors=[];links=0
for path,page in parsed.items():
 rel=path.relative_to(root)
 if len(set(page.ids))!=len(page.ids):errors.append(f'{rel}: duplicate IDs')
 if page.h1!=1 and path.name!='404.html':errors.append(f'{rel}: expected one h1, got {page.h1}')
 if not page.lang:errors.append(f'{rel}: missing page language')
 errors += [f'{rel}: '+issue for issue in page.issues]
 for ref in page.refs:
  links+=1;url=urlsplit(ref);name=unquote(url.path)
  if name.startswith('/'):target=root/name.lstrip('/')
  elif name:target=path.parent/name
  else:target=path
  if target.is_dir():target=target/'index.html'
  elif not target.exists() and not target.suffix:target=target.with_suffix('.html')
  if not target.exists():errors.append(f'{rel}: missing {ref}');continue
  if url.fragment:
   if target.suffix=='.svg':valid=bool(re.search(r'id="'+re.escape(url.fragment)+r'"',target.read_text()))
   elif target in parsed:valid=unquote(url.fragment) in parsed[target].ids
   else:valid=True
   if not valid:errors.append(f'{rel}: missing fragment {ref}')
mods=json.loads((root/'assets/data/modules.json').read_text());ids={m['id'] for m in mods}
if len(ids)!=116 or len(ids)!=len(mods):errors.append('Catalog differs from 116 unique registered modules')
for name in ['instantreplay','performancemonitor','shulkerpreview','killeffect','lyrics','recorder']:
 if name not in ids:errors.append('Missing current module '+name)
if any(s['name']=='Application ID' for m in mods if m['id']=='discordrpc' for s in m['settings']):errors.append('Built-in Discord identity incorrectly exposed as configurable')
source=(root/'docs/discord-rpc.html').read_text()
if 'Create a Discord app' in source:errors.append('Outdated Discord instructions')
for p in files:
 if re.search(r'0\.9\.5',p.read_text()):errors.append(str(p.relative_to(root))+': old release remains')
if errors:print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(files)} HTML pages; {links} local references; {len(mods)} unique modules; all referenced fragments and assets present.')
