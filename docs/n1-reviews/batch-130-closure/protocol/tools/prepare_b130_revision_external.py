"""Capture B130's three observed external sources and neutral full-body extracts."""
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, urlsplit

from b129_external_sources import METHOD, extract_capture
from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

ROOT = WS / "scratch-130" / "review"
SOURCE = WS / "scratch-130" / "reconciliation-001" / "external"
EVIDENCE = WS / "b130-worktree" / "docs" / "n1-sources" / "batch-130-reconciliation"
OUTPUT = ROOT / "revision-external-observation-001"
CHARACTERS = "\u97f3\u4fe1\u57ce"
HELPERS = {
    "b129_external_sources.py": "7b2e389ba246637ee70e4f848f0d91ba446eddc86f5f3221cb8919e940dfedfc",
    "b128_external_sources.py": "8d44156ccedaefbf332f0fbeade41b9e07b0a3ad701fc96cf83721acb374634e",
    "weblio_sections.py": "56a94054bc039a9cc36001a592d97d3831de383b74f9e5e9f6488dec055bd77c",
}


def compact(value):
    return re.sub(r"\s+", "", value)


def verify_capture(item, raw, text, analysis):
    character = item["character"]
    require(character in CHARACTERS and len(character) == 1
            and item["url"] == "https://kotobank.jp/word/" + quote(character)
            and urlsplit(item["finalUrl"]).scheme == "https"
            and urlsplit(item["finalUrl"]).hostname == "kotobank.jp"
            and Path(item["localRawCapture"]) == SOURCE / f"{character}-kotobank.html"
            and datetime.fromisoformat(item["capturedAt"]).tzinfo is not None,
            "External capture identity/path/time differs")
    require(sha(raw) == item["rawSha256"] and len(raw) == item["rawBytes"]
            and sha(text) == item["textSha256"], "External capture bytes differ")
    require(all(analysis[field] == item[field] for field in
                ("url", "finalUrl", "capturedAt", "rawSha256", "textSha256")),
            "Author analysis cites another capture")
    neutral, error = extract_capture(raw, {"requestUrl": item["url"], "finalUrl": item["finalUrl"]})
    require(error is None and neutral, "Neutral complete-body extraction failed: " + str(error))
    excerpt = compact(analysis["shortExcerpt"])
    require(excerpt and excerpt in compact(text.decode("utf-8"))
            and excerpt in compact(neutral), "Author excerpt is missing from captured source")
    return neutral.encode("utf-8")


def main():
    require(not OUTPUT.exists(), "Preserve the previous external observation")
    for name, digest in HELPERS.items():
        frozen(Path(__file__).with_name(name), digest)
    paths = {name: EVIDENCE / name for name in
             ("external-capture-bindings.json", "authored-source-analysis-001.json")}
    evidence = {name: path.read_bytes() for name, path in paths.items()}
    declarations = json.loads(evidence["external-capture-bindings.json"])
    analysis = json.loads(evidence["authored-source-analysis-001.json"])
    require([item["character"] for item in declarations["captures"]] == list(CHARACTERS)
            and set(analysis["externalEntries"]) == set(CHARACTERS)
            and declarations["completeCapturesCommitted"] is False,
            "External observation inventory or retention differs")
    producer = WS / "scratch-130" / "reconcile_external_b130.py"
    producer_raw = producer.read_bytes()
    require(sha(producer_raw) == declarations["producerSha256"], "External capture producer changed")
    guard, _ = start_guard("B130 reconciliation neutral external snapshot")
    captures = []
    try:
        for index, item in enumerate(declarations["captures"], 1):
            raw_path = SOURCE / f"{item['character']}-kotobank.html"
            text_path = raw_path.with_suffix(".txt")
            raw, text = raw_path.read_bytes(), text_path.read_bytes()
            neutral = verify_capture(item, raw, text, analysis["externalEntries"][item["character"]])
            outputs = {suffix: write_frozen(OUTPUT / f"{index:02d}-{suffix}", value)
                       for suffix, value in (("raw.html", raw), ("author-extract.txt", text),
                                             ("complete-extract.txt", neutral))}
            require(raw_path.read_bytes() == raw and text_path.read_bytes() == text,
                    "Author external capture changed during observation")
            captures.append({"character": item["character"], "receipt": item, "outputs": outputs})
            guard.check()
        for name, raw in evidence.items():
            require(paths[name].read_bytes() == raw, "Author analysis changed during observation")
            write_frozen(OUTPUT / name, raw)
        require(producer.read_bytes() == producer_raw, "Capture producer changed during observation")
        write_frozen(OUTPUT / "reconcile_external_b130.py", producer_raw)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "External observation RAM guard breached")
    print(json.dumps(freeze_json(OUTPUT / "manifest.json", {
        "batch": 130, "status": "PASS_CAPTURE_SNAPSHOT_ONLY", "candidate": None,
        "captures": captures, "sourceBindings": {name: sha(raw) for name, raw in evidence.items()},
        "method": METHOD, "helpers": HELPERS, "memory": memory,
        "producerSha256": sha(frozen(Path(__file__))),
        "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Raw responses and author extraction hashes captured without refetch. Complete "
                  "HTML bodies independently extracted; short excerpts occur in both representations. "
                  "Author PageText output is hash-bound, not independently reproduced. Heading/source "
                  "allocation, substantive interpretation, image glyphs and prose independence still "
                  "require human/model review. These complete captures remain local.",
    })))


if __name__ == "__main__":
    main()
