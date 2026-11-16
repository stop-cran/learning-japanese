import importlib.util
import json
from fontTools.ttLib import TTFont
from b126_common import GUARD_SHA, HERE, PACKET, REPO, ROOT, sha, start_guard, write

guard = start_guard()
try:
    svg = (PACKET / "05098.svg").read_bytes()
    receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))
    assert sha(svg) == receipt["kanjivg"]["sha256"]
    converter_path = REPO / "tools" / "generate_strokes.py"
    assert sha(converter_path.read_bytes()) == "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
    spec = importlib.util.spec_from_file_location("converter", converter_path)
    converter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(converter)
    generated = converter.convert("傘", svg.decode("utf-8"))
    assert generated["strokeCount"] == 12
    data = (json.dumps(generated, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    write(REPO / "strokes" / "傘.json", data)
    fonts = []
    for path in sorted((ROOT / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        guard.check()
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            fonts.append({"filename": path.name, "sha256": sha(path.read_bytes()), "bytes": path.stat().st_size, "coverage": {f"U+{ord(ch):04X}": ord(ch) in cmap for ch in "傘人十"}})
    assert len(fonts) == 3
    assert all(all(font["coverage"].values()) for font in fonts)
    write(PACKET / "stroke-font-evidence.json", {
        "kanji": "傘", "strokeCount": 12, "strokeSha256": sha(data),
        "converterSha256": sha(converter_path.read_bytes()), "svgSha256": sha(svg),
        "kanjivgBlob": receipt["kanjivg"]["gitBlob"], "fonts": fonts,
        "fontLimit": "All three actual bundled cmaps cover the glyph and introduced component code points; not rendered native/device acceptance.",
        "producerSha256": sha(open(__file__, "rb").read()), "guardSha256": GUARD_SHA,
    })
    print(json.dumps({"strokes": 12, "strokeSha256": sha(data), "fonts": fonts}, ensure_ascii=False))
finally:
    write(HERE / "generation-memory-001.json", guard.finish())
