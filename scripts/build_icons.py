"""Sprite SVG con los mismos íconos Material (Apache 2.0) que usa el cliente."""
import re, sys, pathlib, importlib.util
S = sys.argv[1]  # carpeta con icons/package/round y icons/custom
spec = importlib.util.spec_from_file_location("atlas_map", S + "/tools/atlas.py")
src = pathlib.Path(S + "/tools/atlas.py").read_text()
# reutiliza el diccionario M sin ejecutar el render
M = {}
exec(src.split("names=list(M.keys())")[0].split("SRC=")[0].replace("import cairosvg, io, re, sys\nfrom PIL import Image\n", ""), {}, {})
ns = {}
code = src.split("names=list(M.keys())")[0]
code = "\n".join(l for l in code.splitlines() if not l.startswith(("import", "from", "S=", "SRC=", "OUT=")))
exec(code, ns)
M = ns["M"]
M.update({
  "download": "download", "arrow": "arrow_forward", "expand": "expand_more", "menu": "menu", "copy": "content_copy",
  "external": "open_in_new", "block": "block", "check_circle": "check_circle", "folder": "folder", "info": "info",
  "warning2": "error_outline", "lightbulb": "lightbulb", "rocket": "rocket_launch", "lock": "lock", "public2": "language",
  "doc": "description", "link": "link", "chevron_right": "chevron_right", "home": "home", "update": "update",
  "mouse": "mouse", "favorite": "favorite", "keyboard2": "keyboard", "storage": "storage", "tag": "tag", "bolt": "bolt",
})
out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']
for name, f in M.items():
    p = S + "/icons/custom/" + f[1:] + ".svg" if f.startswith("@") else S + "/icons/package/round/" + f + ".svg"
    t = pathlib.Path(p).read_text()
    vb = re.search(r'viewBox="([^"]+)"', t).group(1)
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", t, flags=re.S).strip()
    inner = re.sub(r'<path fill="none" d="M0 0h24v24H0z"/>|<path d="M0 0h24v24H0z" fill="none"/>', "", inner)
    out.append(f'<symbol id="i-{name}" viewBox="{vb}">{inner}</symbol>')
# Discord (glifo de marca, solo para enlazar a Discord)
out.append('<symbol id="i-discord" viewBox="0 0 24 24"><path d="M20.32 4.37a19.8 19.8 0 0 0-4.89-1.52.07.07 0 0 0-.08.04c-.21.37-.44.86-.6 1.25a18.27 18.27 0 0 0-5.49 0 12.6 12.6 0 0 0-.62-1.25.08.08 0 0 0-.08-.04 19.74 19.74 0 0 0-4.88 1.52.07.07 0 0 0-.03.03C.53 9.05-.32 13.58.1 18.06a.08.08 0 0 0 .03.06 19.9 19.9 0 0 0 5.99 3.03.08.08 0 0 0 .08-.03c.46-.63.87-1.3 1.23-1.99a.08.08 0 0 0-.04-.1 13.1 13.1 0 0 1-1.87-.9.08.08 0 0 1 0-.13l.37-.29a.07.07 0 0 1 .08-.01c3.93 1.79 8.18 1.79 12.07 0a.07.07 0 0 1 .08 0l.37.3a.08.08 0 0 1 0 .13c-.6.35-1.22.65-1.87.89a.08.08 0 0 0-.04.11c.36.7.78 1.36 1.23 1.99a.08.08 0 0 0 .08.03 19.84 19.84 0 0 0 6-3.03.08.08 0 0 0 .03-.06c.5-5.18-.84-9.67-3.55-13.66a.06.06 0 0 0-.03-.03ZM8.02 15.33c-1.18 0-2.16-1.08-2.16-2.42 0-1.33.96-2.42 2.16-2.42 1.21 0 2.18 1.1 2.16 2.42 0 1.34-.96 2.42-2.16 2.42Zm7.97 0c-1.18 0-2.15-1.08-2.15-2.42 0-1.33.95-2.42 2.15-2.42 1.21 0 2.18 1.1 2.16 2.42 0 1.34-.95 2.42-2.16 2.42Z"/></symbol>')
out.append("</svg>")
pathlib.Path(sys.argv[2]).write_text("\n".join(out))
print(len(M) + 1, "icons")
