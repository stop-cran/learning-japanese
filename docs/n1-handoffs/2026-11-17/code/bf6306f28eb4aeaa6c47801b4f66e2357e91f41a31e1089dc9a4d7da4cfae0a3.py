"""Extract existing coordinator captures without changing the frozen B134 review."""
import importlib.util
import json
from pathlib import Path

from common import WS, freeze_json, require, sha, start_guard, write_frozen

ROOT = WS / "scratch-134" / "review"
SOURCE = ROOT / "claude-001-adjudication" / "evidence"
OUTPUT = ROOT / "reconciliation-captures-001"
EXTRACTOR = WS / "scratch-133" / "source-reconciliation-001" / "gather.py"
EXTRACTOR_SHA = "ba6dc1168c63c0495aac7c6837fb6602844b9cf107e34482236e222eb31da31a"
RETRIEVAL_SHA = "b6b1c74c2787ea04eb43921db8973942b9a0cdd0f96e6faa46e9acca16e9e5d9"
CAPTURES = {
    "kotobank-kon.html": "034cfdcee9becc92daa72857d15577059d8380016f4d0324b8d8f4c76f07b134",
    "weblio-kon.html": "44342f184df45e4729777748885df2df131e25f2487819e89506ad9097f594bd",
}


def checked_capture(path, expected):
    raw = path.read_bytes()
    require(sha(raw) == expected, "Captured input changed: " + str(path))
    return raw


def extractor_type():
    checked_capture(EXTRACTOR, EXTRACTOR_SHA)
    spec = importlib.util.spec_from_file_location("b134_reused_capture_extractor", EXTRACTOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Extractor


def extract(raw, parser_type):
    parser = parser_type()
    parser.feed(raw.decode("utf-8"))
    parser.close()
    require(parser.skip == 0, "Incomplete script/style/noscript boundary")
    text = parser.text().encode("utf-8")
    require(text.strip(), "Capture extraction is empty")
    return text, parser.images


def main():
    require(not OUTPUT.exists(), "Preserve the previous source preparation")
    guard, _ = start_guard("B134 existing reconciliation captures")
    try:
        retrieval = checked_capture(SOURCE / "retrieval.txt", RETRIEVAL_SHA)
        parser_type = extractor_type()
        prepared = []
        for name, digest in CAPTURES.items():
            path = SOURCE / name
            raw = checked_capture(path, digest)
            text, images = extract(raw, parser_type)
            prepared.append((path, raw, text, images))
            guard.check()
        records = []
        for path, raw, text, images in prepared:
            records.append({
                "source": {"path": str(path), "sha256": sha(raw), "bytes": len(raw)},
                "text": write_frozen(OUTPUT / (path.stem + ".txt"), text),
                "images": freeze_json(OUTPUT / (path.stem + ".images.json"), images),
                "lines": len(text.splitlines()), "imageCount": len(images),
            })
        result = {
            "batch": 134, "candidate": "ba80afffc20a72d31be68b355b6f90aab36a5726",
            "status": "EXTRACTED_EXISTING_CAPTURES_NOT_REVIEW_ACCEPTANCE",
            "extractor": {"path": str(EXTRACTOR), "sha256": EXTRACTOR_SHA},
            "producer": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
            "retrievalNote": write_frozen(OUTPUT / "retrieval.txt", retrieval),
            "captures": records, "networkRequests": 0,
            "scope": "Complete captured HTML text, excluding script/style/noscript only. "
                     "Whitespace is normalized by the existing extractor. All image sources "
                     "and alt-text omissions are retained separately; no selected passages.",
            "limits": [
                "Existing coordinator captures only; no new retrieval or independent HTTP verification.",
                "Original retrieval note is retained verbatim; response headers were not captured.",
                "Images, external resources, CSS visibility and browser layout are not inspected.",
                "Not part of either frozen initial review packet; not sent to the blind GPT reviewer.",
                "No semantic conclusion, teaching edit, reviewer admission or publication.",
            ],
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Capture preparation RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(OUTPUT / "index.json", result)))


if __name__ == "__main__":
    main()
