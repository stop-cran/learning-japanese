import json
from pathlib import Path

from PIL import Image, ImageDraw

root = Path(__file__).parent / "artifacts" / "batch-085-native-attempt-596"
destination = root / "inspection"
destination.mkdir(exist_ok=False)
files = sorted(root.glob("*.png"))
assert len(files) == 87
index = []
for start in range(0, len(files), 6):
    sheet = Image.new("RGB", (1800, 2720), "white")
    draw = ImageDraw.Draw(sheet)
    entries = []
    for position, path in enumerate(files[start:start + 6]):
        with Image.open(path) as original:
            image = original.convert("RGB")
        image.thumbnail((600, 1320))
        x, y = (position % 3) * 600, (position // 3) * 1360
        draw.text((x + 8, y + 8), path.name, fill="black")
        sheet.paste(image, (x, y + 32))
        entries.append(path.name)
    name = f"sheet-{start // 6 + 1:02}.png"
    sheet.save(destination / name)
    index.append({"sheet": name, "originals": entries, "transform": "Full frame, aspect-preserving thumbnail <=600x1320; no crop."})
(destination / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
print("15 labelled sheets generated from all87 originals; originals preserved.")
