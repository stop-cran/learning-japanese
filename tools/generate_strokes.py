#!/usr/bin/env python3
"""Generate strokes/<char>.json for every kanji/<char>.md from KanjiVG.

Strokes are resampled to fixed-size polylines in KanjiVG's 109x109 coordinate space,
in stroke order, so consumers do not need an SVG path parser.

Usage: python tools/generate_strokes.py [--force]
Requires: pip install svgpathtools
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from svgpathtools import parse_path

KANJIVG_REVISION = "70a0b7ae0c18ceb5cb358274b029cce0234a43bc"
KANJIVG_URL = "https://raw.githubusercontent.com/KanjiVG/kanjivg/{rev}/kanji/{code}.svg"
POINTS_PER_STROKE = 16
ROOT = Path(__file__).resolve().parent.parent
KVG_NS = "{https://kanjivg.tagaini.net/}"


def fetch_svg(char: str) -> str:
    url = KANJIVG_URL.format(rev=KANJIVG_REVISION, code=f"{ord(char):05x}")
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def resample(path, count: int):
    fine = [path.point(i / 400) for i in range(401)]
    lengths = [0.0]
    for a, b in zip(fine, fine[1:]):
        lengths.append(lengths[-1] + abs(b - a))
    total = lengths[-1]
    points, j = [], 0
    for i in range(count):
        target = total * i / (count - 1)
        while j < len(lengths) - 2 and lengths[j + 1] < target:
            j += 1
        span = lengths[j + 1] - lengths[j]
        f = 0.0 if span == 0 else (target - lengths[j]) / span
        p = fine[j] + (fine[j + 1] - fine[j]) * f
        points.append([round(p.real, 1), round(p.imag, 1)])
    return points


def convert(char: str, svg_text: str) -> dict:
    root = ET.fromstring(svg_text.split("]>", 1)[1] if "]>" in svg_text else svg_text)
    strokes = []
    for element in root.iter("{http://www.w3.org/2000/svg}path"):
        strokes.append(
            {
                "id": len(strokes) + 1,
                "type": element.get(KVG_NS + "type", ""),
                "points": resample(parse_path(element.get("d")), POINTS_PER_STROKE),
            }
        )
    return {
        "schemaVersion": 1,
        "kanji": char,
        "source": "KanjiVG (CC BY-SA 3.0, https://kanjivg.tagaini.net)",
        "sourceRevision": KANJIVG_REVISION,
        "viewBox": [0, 0, 109, 109],
        "strokeCount": len(strokes),
        "strokes": strokes,
    }


def main() -> int:
    force = "--force" in sys.argv
    (ROOT / "strokes").mkdir(exist_ok=True)
    variants_file = ROOT / "tools" / "order_variants.json"
    variants = json.loads(variants_file.read_text(encoding="utf-8")) if variants_file.exists() else {}
    for card in sorted((ROOT / "kanji").glob("*.md")):
        char = card.stem
        target = ROOT / "strokes" / f"{char}.json"
        if target.exists() and not force:
            existing = json.loads(target.read_text(encoding="utf-8"))
            if existing.get("orderVariants", []) != variants.get(char, []):
                existing.pop("orderVariants", None)
                if char in variants:
                    existing["orderVariants"] = variants[char]
                target.write_text(json.dumps(existing, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
                print(f"{char}: order variants updated")
            continue
        data = convert(char, fetch_svg(char))
        if char in variants:
            data["orderVariants"] = variants[char]
        target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"{char}: {data['strokeCount']} strokes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
