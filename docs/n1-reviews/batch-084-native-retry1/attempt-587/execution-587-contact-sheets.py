from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).parent / "artifacts" / "batch-084-native-retry1-attempt-587"
destination = root / "inspection"
destination.mkdir(exist_ok=False)
files = sorted(root.glob("*.png"))
assert len(files) == 42
for start in range(0, len(files), 6):
    sheet = Image.new("RGB", (1800, 2720), "white")
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(files[start:start + 6]):
        image = Image.open(path).convert("RGB")
        image.thumbnail((600, 1320))
        x, y = (index % 3) * 600, (index // 3) * 1360
        draw.text((x + 8, y + 8), path.name, fill="black")
        sheet.paste(image, (x, y + 32))
    sheet.save(destination / f"sheet-{start // 6 + 1}.png")
print("Seven labelled contact sheets generated from all42 original PNGs, originals preserved.")
