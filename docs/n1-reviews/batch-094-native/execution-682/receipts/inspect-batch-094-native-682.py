import hashlib
import json
import pathlib

from PIL import Image, ImageDraw

CONTROL = pathlib.Path(__file__).parent
source = CONTROL / "artifacts" / "batch-094-native-attempt-682"
target = CONTROL / "batch-094-native-inspection-682"
target.mkdir(exist_ok=False)
files = sorted(p for p in source.glob("*.png") if "font-panel" not in p.name)
pages = []
for offset in range(0, len(files), 4):
    canvas = Image.new("RGB", (1000, 2260), "white")
    draw = ImageDraw.Draw(canvas)
    entries = []
    for index, path in enumerate(files[offset:offset + 4]):
        x, y = (index % 2) * 500, (index // 2) * 1130
        image = Image.open(path).convert("RGB")
        image.thumbnail((500, 1100))
        canvas.paste(image, (x, y + 30))
        draw.text((x + 4, y + 6), path.stem, fill="black")
        entries.append({"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    output = target / f"sheet-{offset // 4 + 1:02d}.png"
    canvas.save(output)
    pages.append({"sheet": output.name, "sources": entries})
(target / "index.json").write_text(json.dumps(pages, indent=2) + "\n", encoding="utf-8")
route = json.loads((source / "n1-094-article-route.json").read_bytes())
summary = {k: ({"entries": len(v)} if isinstance(v, list) and len(v) > 20 else v)
           for k, v in route.items()}
for key, value in route.items():
    if isinstance(value, list) and value and isinstance(value[0], dict) and "options" in value[0]:
        summary[key + "UniqueOptions"] = sorted({
            json.dumps(option, ensure_ascii=False, sort_keys=True)
            for item in value for option in item["options"]
        })
(target / "route-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"screenshots": len(files), "sheets": len(pages), "routeKeys": list(route)}, indent=2))
