import importlib.util
import json
import unicodedata
from fontTools.ttLib import TTFont
from b127_common import GUARD_SHA, HERE, PACKET, REPO, ROOT, sha, start_guard, write

guard = start_guard()
try:
    svg = (PACKET / "05009.svg").read_bytes()
    receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))
    assert sha(svg) == receipt["kanjivg"]["sha256"]
    converter_path = REPO / "tools" / "generate_strokes.py"
    assert sha(converter_path.read_bytes()) == "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
    spec = importlib.util.spec_from_file_location("converter", converter_path)
    converter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(converter)
    generated = converter.convert("倉", svg.decode("utf-8"))
    assert generated["strokeCount"] == 10
    data = (json.dumps(generated, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    assert (REPO / "strokes" / "倉.json").read_bytes() == data
    fonts = []
    for path in sorted((ROOT / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        guard.check()
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            fonts.append({"filename": path.name, "sha256": sha(path.read_bytes()), "bytes": path.stat().st_size, "coverage": {f"U+{ord(ch):04X}": ord(ch) in cmap for ch in "倉人口宀"}})
    assert len(fonts) == 3
    assert all(all(font["coverage"][f"U+{ord(ch):04X}"] for ch in "倉人口") for font in fonts)
    assert all(not font["coverage"]["U+5B80"] for font in fonts)
    write(PACKET / "stroke-font-evidence.json", {
        "kanji": "倉", "strokeCount": 10, "strokeSha256": sha(data),
        "converterSha256": sha(converter_path.read_bytes()), "svgSha256": sha(svg),
        "kanjivgBlob": receipt["kanjivg"]["gitBlob"], "fonts": fonts,
        "codePoints": [{"character": ch, "codePoint": f"U+{ord(ch):04X}", "unicodeName": unicodedata.name(ch)} for ch in "倉人口宀"],
        "priorAttempt": {"producer": "generate_b127.py", "sha256": sha((HERE / "generate_b127.py").read_bytes()), "result": "Assertion failed after deterministic strokes were generated: all three subsets lack contrast-only 宀. Preserved original producer and memory receipt; geometry not edited or overwritten."},
        "fontLimit": "倉, radical 人 and mnemonic 口 covered in all three actual bundled cmaps. Contrast-only 宀 (explicitly NOT 倉's radical/component) lacks subset coverage and relies on system CJK fallback already used for this radical in existing cards. No native/device or rendered fallback acceptance was performed or inferred.",
        "producerSha256": sha(open(__file__, "rb").read()), "guardSha256": GUARD_SHA,
    })
    print(json.dumps({"strokes": 10, "strokeSha256": sha(data), "fonts": fonts}, ensure_ascii=False))
finally:
    write(HERE / "generation-memory-002.json", guard.finish())
