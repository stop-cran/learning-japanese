import importlib.util
import json
import unicodedata
from pathlib import Path
from fontTools.ttLib import TTFont
from b129_common import CHARS, GUARD_SHA, HERE, PACKET, REPO, ROOT, sha, start_guard, write

guard = start_guard()
try:
    converter_path = REPO / "tools" / "generate_strokes.py"
    assert sha(converter_path.read_bytes()) == "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
    spec = importlib.util.spec_from_file_location("b129_converter", converter_path)
    converter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(converter)
    rows = json.loads((PACKET / "source-rows.json").read_text(encoding="utf8"))
    evidence = []
    for row in rows:
        ch = row["kanji"]
        svg_path = PACKET / "kanjivg" / (f"{ord(ch):05x}" + ".svg")
        svg = svg_path.read_bytes()
        assert len(svg) == row["kanjivgInventory"]["size"]
        assert __import__("hashlib").sha1(b"blob " + str(len(svg)).encode() + b"\0" + svg).hexdigest() == row["kanjivgInventory"]["sha"]
        generated = converter.convert(ch, svg.decode("utf8"))
        assert generated["strokeCount"] == row["metadata"]["strokes"]
        data = (json.dumps(generated, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
        write(REPO / "strokes" / (ch + ".json"), data)
        evidence.append({"kanji": ch, "strokeCount": generated["strokeCount"], "strokeSha256": sha(data),
                         "svgSha256": sha(svg), "kanjivgBlob": row["kanjivgInventory"]["sha"]})
    glyphs = "".join(dict.fromkeys("茉絹虹艸艹末未本古糸⺯糹口月虫工紅功石莉花木綿紙約級"))
    fonts = []
    for path in sorted((ROOT / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        guard.check()
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            fonts.append({"filename": path.name, "sha256": sha(path.read_bytes()), "bytes": path.stat().st_size,
                          "coverage": {f"U+{ord(ch):04X}": ord(ch) in cmap for ch in glyphs}})
    assert len(fonts) == 3, "Expected the three actual bundled fonts"
    write(PACKET / "stroke-font-evidence.json", {
        "members": evidence, "converterSha256": sha(converter_path.read_bytes()),
        "kanjivgRevision": "70a0b7ae0c18ceb5cb358274b029cce0234a43bc", "fonts": fonts,
        "codePoints": [{"character": ch, "codePoint": f"U+{ord(ch):04X}", "unicodeName": unicodedata.name(ch)} for ch in glyphs],
        "fontLimit": "Actual bounded font cmap membership only. Missing glyphs are reported, not assumed rendered by fallback. No visual, native/device or rendered-font acceptance.",
        "producerSha256": sha(Path(__file__).read_bytes()), "guardSha256": GUARD_SHA})
    print(json.dumps({"members": evidence, "missing": {f["filename"]: [k for k, v in f["coverage"].items() if not v] for f in fonts}}, ensure_ascii=False))
finally:
    write(HERE / "generation-memory-001.json", guard.finish())
