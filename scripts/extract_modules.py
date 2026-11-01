"""Build the catalog from registered Java modules and the imported Clarity definitions.
Usage: python scripts/extract_modules.py CLIENT_JAVA_ROOT OUTPUT [CLARITY_MODULES_JSON]
"""
import json,re,sys,pathlib
from collections import Counter
src=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2])
manager=(src/'module/ModuleManager.java').read_text()
order=re.findall(r'MODULES\.add\(new (\w+)\(\)\)',manager)
imported=re.search(r'for \(String n : new String\[\] \{(.*?)\}\)',manager,re.S)
extra=re.findall(r'"(\w+)"',imported[1]) if imported else []
order=order[:-3]+extra+order[-3:]
clarity=json.loads(pathlib.Path(sys.argv[3]).read_text()) if len(sys.argv)>3 else {}
old={m['cls']:m for m in json.loads(out.read_text())} if out.exists() else {}
STR=r'"((?:[^"\\]|\\.)*)"'
new={'ShulkerPreview','ItemDetails','InventoryAlert','LightMeter','Lyrics','KillEffect','Recorder','InstantReplay','PerformanceMonitor'}
mods=[]
for cls in order:
 f=next(src.rglob(cls+'.java'));t=f.read_text();base=old.get(cls,{})
 normal=re.search(r'super\(\s*'+STR+r'\s*,\s*'+STR,t)
 single=re.search(r'super\(\s*'+STR+r'\s*,\s*(?:dev\.larp\.client\.module\.)?Category\.(\w+)\s*,\s*(true|false)',t)
 if normal:
  name,desc=normal.groups();tail=t[normal.end():];cat=re.search(r'Category\.(\w+)',tail[:200]);category=cat[1] if cat else ('HUD' if re.search(r'extends (?:Stat)?HudModule',t) else 'COSMETICS' if 'extends Cosmetic' in t else 'CLIENT')
  on=bool(re.match(r'\s*,\s*(?:Category\.\w+\s*,\s*)?true',tail));settings=[]
  for match in re.finditer(r'add\(new (Bool|Number|Mode|Color|String)Setting\(([^;]*?)\)\)(?:\.in\('+STR+r'\))?',t,re.S):
   kind,args,group=match.groups();strings=re.findall(STR,args)
   if not strings:continue
   owner=re.search(r'(\w+)\s*=\s*$',t[:match.start()])
   if owner and re.search(r'\b'+re.escape(owner[1])+r'\.visible\s*=\s*\(\)\s*->\s*false',t):continue
   entry={'name':strings[0],'type':kind.lower(),'group':group}
   rest=args[args.find('"',args.find('"')+1)+1:]
   if kind=='Bool':entry['default']=bool(re.match(r'\s*,\s*true',rest))
   elif kind=='Number':
    nums=re.findall(r'(?<![\w])-?(?:\d+(?:\.\d+)?|\.\d+)',rest)
    if len(nums)>=3:entry.update(default=float(nums[0]),min=float(nums[1]),max=float(nums[2]))
   elif kind=='Mode':
    entry['options']=strings[1:]
    if not entry['options']:
     previous=next((s for s in base.get('settings',[]) if s['name']==entry['name']),{})
     entry['options']=previous.get('options',[])
   elif kind=='String':entry['default']=strings[1] if len(strings)>1 else ''
   elif kind=='Color':
    color=re.search(r'0x[0-9a-fA-F]{2}([0-9a-fA-F]{6})',rest)
    if color:entry['default']='#'+color[1].lower()
   if cls=='DiscordRpc' and entry['name'] in ['Application ID','Large image key']:continue
   if cls=='KillEffect' and entry['name'] in ['Natural colors','Color','Second color','Shockwave radius']:continue
   settings.append(entry)
  if re.search(r'extends (?:Stat)?HudModule',t):
   for s in base.get('settings',[]):
    if s.get('group')=='Style' and s['name'] not in {x['name'] for x in settings}:settings.append(s)
 elif single:
  name,category,on=single.groups();on=on=='true';desc=clarity.get('descriptions',{}).get(name,base.get('description',name)).rstrip('.');settings=[]
  for row in clarity.get('settings',{}).get(name,[]):
   label,kind,value=row[:3];entry={'name':label,'group':None}
   if kind=='check':entry.update(type='bool',default=value)
   elif kind=='range':entry.update(type='number',min=value[0],max=value[1],default=value[2])
   elif kind in ['select','skinselect','capeselect']:entry.update(type='mode',options=value if isinstance(value,list) else [value])
   elif kind in ['text','keybind']:entry.update(type='string',default=value)
   elif kind=='color':entry.update(type='color')
   else:continue
   settings.append(entry)
  if not clarity:settings=base.get('settings',[])
 else:raise ValueError('Unrecognized registered module '+cls)
 mid=re.search(r'String id\(\)\s*\{\s*return "([^"]+)"',t)
 mid=mid[1] if mid else re.sub(r'[ -]','',name.lower())
 mods.append(dict(id=mid,cls=cls,name=name,description=desc,category=category,defaultOn=on,settings=settings,new=cls in new))
assert len({m['id'] for m in mods})==len(mods)
out.write_text(json.dumps(mods,indent=1)+'\n')
print(len(mods),'registered modules',dict(Counter(m['category'] for m in mods)))
