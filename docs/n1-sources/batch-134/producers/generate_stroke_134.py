import hashlib
import importlib.util
import json

from common_134 import HERE, REPO, sha, start_guard, write

converter_path = REPO / "tools" / "generate_strokes.py"
svg_path = HERE / "source-002" / "kanjivg" / "07d2b.svg"
expected_converter = "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
expected_blob = "a360fbfd8a261a875390e839bcf92c4321b6eaf3"

guard = start_guard()
try:
    assert sha(converter_path.read_bytes()) == expected_converter
    svg = svg_path.read_bytes()
    assert hashlib.sha1(b"blob " + str(len(svg)).encode() + b"\0" + svg).hexdigest() == expected_blob
    spec = importlib.util.spec_from_file_location("stroke_converter_134", converter_path)
    converter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(converter)
    result = converter.convert("紫", svg.decode("utf-8"))
    assert result["strokeCount"] == 12
    variants = json.loads((REPO / "tools" / "order_variants.json").read_bytes())
    if "紫" in variants:
        result["orderVariants"] = variants["紫"]
    content = (json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    write(REPO / "strokes" / "紫.json", content)
    write(HERE / "stroke-001.json", {
        "character": "紫", "strokeCount": result["strokeCount"],
        "strokeSha256": sha(content), "svgSha256": sha(svg),
        "svgGitBlob": expected_blob, "converterSha256": expected_converter,
        "revision": converter.KANJIVG_REVISION,
    })
finally:
    write(HERE / "stroke-001-memory.json", guard.finish())
