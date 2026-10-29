"""Lee el código del mod y genera assets/data/modules.json para las docs."""
import json, re, sys, pathlib
src = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
order = []
mm = (src / "module/ModuleManager.java").read_text()
for m in re.finditer(r"new (\w+)\(\)", mm): order.append(m.group(1))
mods = []
STR = r'"((?:[^"\\]|\\.)*)"'
for f in list((src / "module/impl").rglob("*.java")):
    t = f.read_text()
    m = re.search(r"super\(\s*" + STR + r"\s*,\s*" + STR + r"\s*,?\s*(Category\.(\w+))?\s*,?\s*(true|false)?", t, re.S)
    if not m: continue
    name, desc = m.group(1), m.group(2)
    cat = m.group(4)
    on = m.group(5) == "true"
    if not cat:
        if "extends HudModule" in t: cat = "HUD"
        elif "extends Cosmetic" in t: cat = "COSMETICS"
    cmodes = None
    if "extends Cosmetic" in t:
        cat, on = "COSMETICS", False
        arr = re.search(r"new String\[\]\s*\{([^}]*)\}", t[m.start():m.start()+400])
        cmodes = re.findall(STR, arr.group(1)) if arr else None
    settings = []
    for s in re.finditer(r"add\(new (Bool|Number|Mode|Color|String)Setting\(([^;]*?)\)\)(?:\.in\(" + STR + r"\))?", t, re.S):
        kind, args, group = s.group(1), s.group(2), s.group(3)
        strs = re.findall(STR, args)
        if not strs: continue
        e = {"name": strs[0], "type": kind.lower(), "group": group}
        rest = args[args.find('"', args.find('"') + 1) + 1:]
        if kind == "Bool": e["default"] = "true" in rest.split(",")[1]
        elif kind == "Number":
            nums = re.findall(r"-?\d+(?:\.\d+)?", rest)
            if len(nums) >= 3: e.update(default=float(nums[0]), min=float(nums[1]), max=float(nums[2]))
        elif kind == "Mode":
            e["options"] = strs[1:]
            const = re.search(r",\s*(\w+)\s*$", args)
            if not e["options"] and const:
                arr = re.search(r"String\[\]\s+" + const.group(1) + r"\s*=\s*\{([^}]*)\}", t)
                if arr: e["options"] = re.findall(STR, arr.group(1))
            if not e["options"]:
                en = re.search(r"(\w+)\[\] all = \1\.values\(\)", t)
                if en:
                    ef = next(src.rglob(en.group(1) + ".java"), None)
                    if ef:
                        labels = [re.findall(STR, l.group(1))[-1] for l in re.finditer(r"^\s*[A-Z_]+\(((?:\s*\"[^\"]*\"\s*,)+)", ef.read_text(), re.M)]
                        if "ROYAL_CROWN" in ef.read_text() and "Royal Crown" in labels:
                            labels.remove("Royal Crown"); labels.insert(0, "Royal Crown")
                        e["options"] = labels
        elif kind == "String": e["default"] = strs[1] if len(strs) > 1 else ""
        elif kind == "Color":
            hx = re.search(r"0x([0-9A-Fa-f]{8})", rest)
            if hx: e["default"] = "#" + hx.group(1)[2:].lower()
        settings.append(e)
    if "extends Cosmetic" in t:
        settings[:0] = [{"name": "Color", "type": "mode", "group": "Color", "options": cmodes or []},
                        {"name": "Custom color", "type": "color", "group": "Color"}]
    if "extends HudModule" in t:
        settings += [{"name": n, "type": ty, "group": "Style"} for n, ty in
                     [("Scale", "number"), ("Background", "bool"), ("Background color", "color"), ("Corner radius", "number"),
                      ("Text color", "color"), ("Chroma text", "bool"), ("Font", "mode"), ("Text shadow", "bool")]]
        for s in settings:
            if s["name"] == "Font" and s["group"] == "Style": s["options"] = ["Minecraft", "Clean"]
    mods.append({"id": name.lower().replace(" ", "").replace("-", ""), "cls": f.stem, "name": name, "description": desc,
                 "category": cat or "CLIENT", "defaultOn": on, "settings": settings})
idx = {c: i for i, c in enumerate(order)}
mods.sort(key=lambda m: idx.get(m["cls"], 999))
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(mods, indent=1))
from collections import Counter
print(len(mods), Counter(m["category"] for m in mods))
