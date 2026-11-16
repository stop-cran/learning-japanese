import json
import re
import unicodedata
from pathlib import Path
from fontTools.ttLib import TTFont
from b131_common import HERE, PACKET, REPO, ROOT, sha, start_guard, write

guard = start_guard()
try:
    initial = json.loads((PACKET / "stroke-font-evidence.json").read_text(encoding="utf8"))
    for row in initial["members"]:
        assert sha((REPO / "strokes" / (row["kanji"] + ".json")).read_bytes()) == row["strokeSha256"]
    text = "".join((REPO / "kanji" / (ch + ".md")).read_text(encoding="utf8") for ch in "衛羊霜")
    glyphs = "".join(sorted(set(re.findall(r"[\u3400-\u9fff]", text)) |
                           {p.stem for p in (PACKET / "comparison-cards").glob("*.md")} |
                           set("彳亍韋行羊雨相木目")))
    fonts = []
    for path in sorted((ROOT / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        guard.check()
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            fonts.append({"filename": path.name, "sha256": sha(path.read_bytes()),
                          "coverage": {f"U+{ord(ch):04X}": ord(ch) in cmap for ch in glyphs}})
    assert len(fonts) == 3
    result = {
        "initialGenerationEvidenceSha256": sha((PACKET / "stroke-font-evidence.json").read_bytes()),
        "members": initial["members"], "fonts": fonts,
        "codePoints": [{"character": ch, "codePoint": f"U+{ord(ch):04X}", "unicodeName": unicodedata.name(ch)} for ch in glyphs],
        "scope": "Han in final three cards plus all 179 baseline comparisons and explicit mnemonic components/radicals. Actual bundled font cmap membership only.",
        "limits": "Missing glyphs are reported, not assumed rendered by fallback; no native/device/visual acceptance.",
        "producerSha256": sha(Path(__file__).read_bytes())}
    write(PACKET / "stroke-font-evidence-002.json", result)
    print(json.dumps({f["filename"]: [k for k, v in f["coverage"].items() if not v] for f in fonts}))
finally:
    write(HERE / "font-final-memory-001.json", guard.finish())
