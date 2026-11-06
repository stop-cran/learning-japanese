import json
from pathlib import Path

from PIL import Image, ImageDraw

C = Path(__file__).resolve().parent
SOURCE = C / "artifacts" / "batch-086-native-attempt-605"
TARGET = C / "artifacts" / "batch-086-native-sheets-605"
assert not TARGET.exists()
TARGET.mkdir()
files = sorted(SOURCE.glob("*.png"))
index = []
for start in range(0, len(files), 4):
    group = files[start:start + 4]
    sheet = Image.new("RGB", (1080, 2456), "white")
    draw = ImageDraw.Draw(sheet)
    for cell, path in enumerate(group):
        x, y = (cell % 2) * 540, (cell // 2) * 1228
        image = Image.open(path).convert("RGB")
        image.thumbnail((540, 1200), Image.Resampling.LANCZOS)
        draw.text((x + 4, y + 4), path.stem.removeprefix("n1-086-"), fill="black")
        sheet.paste(image, (x, y + 28))
    name = f"sheet-{start // 4 + 1:02}.png"
    sheet.save(TARGET / name)
    index.append({"sheet": name, "originals": [p.name for p in group]})
(TARGET / "index.json").write_text(json.dumps(index, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
print(f"{len(files)} original PNGs -> {len(index)} labelled visual sheets; originals retained unchanged.")
