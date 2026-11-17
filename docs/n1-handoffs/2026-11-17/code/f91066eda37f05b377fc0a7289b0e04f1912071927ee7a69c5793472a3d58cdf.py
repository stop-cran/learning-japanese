"""Snapshot the 28 correction captures and extract neutral complete HTML bodies."""
import json
from pathlib import Path
from urllib.parse import quote, urlsplit

from b129_external_sources import METHOD, extract_capture
from common import freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b129_revision_runtime import ADJUDICATION_SHA, REVIEW, allowed_pairs

HELPERS = {
    "b129_external_sources.py": "7b2e389ba246637ee70e4f848f0d91ba446eddc86f5f3221cb8919e940dfedfc",
    "b128_external_sources.py": "8d44156ccedaefbf332f0fbeade41b9e07b0a3ad701fc96cf83721acb374634e",
    "weblio_sections.py": "56a94054bc039a9cc36001a592d97d3831de383b74f9e5e9f6488dec055bd77c",
    "verify_b129_revision_runtime.py": "c4fe03b8aad8d4a377831290456ba3293289fa0c30010394bafbb875fb1be76d",
}
SOURCE = REVIEW.parent / "reconciliation-001" / "external-pages"
OUTPUT = REVIEW / "reconciliation-external-001"


def main():
    require(not OUTPUT.exists(), "Preserve existing capture snapshot")
    for name, digest in HELPERS.items():
        frozen(Path(__file__).with_name(name), digest)
    adjudication = json.loads(frozen(REVIEW / "N1-B129-GPT-001-adjudication.json", ADJUDICATION_SHA))
    pairs = allowed_pairs(adjudication)
    characters = sorted({char for group in pairs.values() for char in group})
    require(len(characters) == 28, "Comparison character inventory differs")
    guard, _ = start_guard("B129 correction external capture snapshot")
    captured, bindings = [], {}
    try:
        for index, character in enumerate(characters, 1):
            receipt_path = SOURCE / f"{character}-receipt.json"
            receipt_raw = receipt_path.read_bytes()
            receipt = json.loads(receipt_raw)
            raw_path = SOURCE / f"{character}-kotobank.html"
            raw = raw_path.read_bytes()
            require(receipt["character"] == character
                    and receipt["url"] == "https://kotobank.jp/word/" + quote(character)
                    and urlsplit(receipt["finalUrl"]).hostname == "kotobank.jp"
                    and Path(receipt["localRawCapture"]) == raw_path,
                    f"Capture identity differs: {character}")
            require(sha(raw) == receipt["rawSha256"] and len(raw) == receipt["rawBytes"],
                    f"Captured response differs from receipt: {character}")
            parsed_raw = raw_path.with_suffix(".json").read_bytes()
            selected_raw = raw_path.with_suffix(".txt").read_bytes()
            require(sha(parsed_raw) == receipt["allArticleJsonSha256"]
                    and sha(selected_raw) == receipt["selectedCompleteArticleTextSha256"],
                    f"Author extraction differs from receipt: {character}")
            parsed = json.loads(parsed_raw)
            selected = [a for a in parsed if set((a["class"] or "").split())
                        & {"daijisen", "nikkokuseisen", "jitsu"}]
            require(selected and [a["class"] for a in selected] == receipt["selectedArticleClasses"],
                    f"Selected dictionary classes differ: {character}")
            rendered = "\n".join(f"===== {character} / {a['class']} =====\n{a['text']}" for a in selected)
            require(rendered.encode("utf-8") == selected_raw, "Selected text differs from article JSON")
            text, error = extract_capture(raw, {"requestUrl": receipt["url"], "finalUrl": receipt["finalUrl"]})
            require(error is None and text, f"Neutral full-body extraction failed: {character}: {error}")
            prefix = f"{index:02d}"
            outputs = {}
            for suffix, data in (
                ("raw.html", raw), ("receipt.json", receipt_raw), ("articles.json", parsed_raw),
                ("author-selected.txt", selected_raw), ("complete-extract.txt", text.encode("utf-8")),
            ):
                name = f"{prefix}-{suffix}"
                outputs[suffix] = write_frozen(OUTPUT / name, data)
                bindings[name] = sha(data)
            require(receipt_path.read_bytes() == receipt_raw and raw_path.read_bytes() == raw
                    and raw_path.with_suffix(".json").read_bytes() == parsed_raw
                    and raw_path.with_suffix(".txt").read_bytes() == selected_raw,
                    f"Author source changed during snapshot: {character}")
            captured.append({
                "character": character, "requestUrl": receipt["url"], "finalUrl": receipt["finalUrl"],
                "capturedAt": receipt["capturedAt"], "sourceReceiptPath": str(receipt_path),
                "outputs": outputs,
            })
            guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "External snapshot RAM guard breached")
    print(json.dumps(freeze_json(OUTPUT / "manifest.json", {
        "batch": 129, "status": "PASS_CAPTURE_SNAPSHOT_ONLY", "captures": captured,
        "files": bindings, "method": METHOD, "helpers": HELPERS, "memory": memory,
        "producerSha256": sha(Path(__file__).read_bytes()),
        "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Raw responses and author receipt hashes captured without refetch; full HTML bodies "
                  "independently extracted using the pinned method. Author JSON/selected text are "
                  "internally consistent but not independently reproduced from HTML. No signed "
                  "successor, source-claim, image/rendering, linguistic or publication acceptance.",
    })))


if __name__ == "__main__":
    main()
