"""Preserve and independently extract the additional exact-noun source capture."""
import html
import json
import re
from pathlib import Path

from b128_external_sources import METHOD, extract
from common import freeze_json, frozen, require, sha, start_guard, write_frozen
from prepare_b129_revision_external import HELPERS, REVIEW, SOURCE

CHARACTER = "\u7f82\u7d22"
OUTPUT = REVIEW / "reconciliation-noose-external-001"
RAW_SHA = "1abe621e063e2ac4ea8ba229715c0a3ff6bc6f0fa8b1b42475f56ec50fc07683"
JSON_SHA = "91baed1ac5f398ee572dbac6ff91ac4163a425be1f41c503666402d4a2d6c695"
SELECTED_SHA = "46c471bd9885a350ac1364ed87bd18361acec4461f7c2d311c812ba77021d748"
URL = "https://kotobank.jp/word/%E7%BE%82%E7%B4%A2"


def extract_noose(raw, capture):
    require(capture["requestUrl"] == URL and capture["finalUrl"] == URL + "-491940",
            "Exact compound URL changed")
    titles = re.findall(r"<title\b[^>]*>(.*?)</title\s*>", raw.decode("utf-8"), re.I | re.S)
    require(len(titles) == 1
            and html.unescape(titles[0]).strip().startswith(CHARACTER + "("),
            "Exact compound title differs")
    return extract(raw, capture["finalUrl"], list(CHARACTER))


def main():
    require(not OUTPUT.exists(), "Preserve existing follow-up capture")
    for name, digest in HELPERS.items():
        frozen(Path(__file__).with_name(name), digest)
    guard, _ = start_guard("B129 additional exact-noun capture")
    try:
        paths = {
            "raw.html": SOURCE / f"{CHARACTER}-kotobank.html",
            "receipt.json": SOURCE / f"{CHARACTER}-receipt.json",
            "articles.json": SOURCE / f"{CHARACTER}-kotobank.json",
            "author-selected.txt": SOURCE / f"{CHARACTER}-kotobank.txt",
        }
        data = {name: path.read_bytes() for name, path in paths.items()}
        receipt = json.loads(data["receipt.json"])
        require(receipt["character"] == CHARACTER and receipt["url"] == URL
                and receipt["finalUrl"] == URL + "-491940"
                and Path(receipt["localRawCapture"]) == paths["raw.html"],
                "Follow-up capture identity changed")
        require(sha(data["raw.html"]) == receipt["rawSha256"] == RAW_SHA
                and len(data["raw.html"]) == receipt["rawBytes"]
                and sha(data["articles.json"]) == receipt["allArticleJsonSha256"] == JSON_SHA
                and sha(data["author-selected.txt"]) ==
                receipt["selectedCompleteArticleTextSha256"] == SELECTED_SHA,
                "Follow-up capture bytes changed")
        articles = [a for a in json.loads(data["articles.json"])
                    if set((a["class"] or "").split()) & {"daijisen", "nikkokuseisen", "jitsu"}]
        rendered = "\n".join(f"===== {CHARACTER} / {a['class']} =====\n{a['text']}" for a in articles)
        require([a["class"] for a in articles] == receipt["selectedArticleClasses"]
                and rendered.encode("utf-8") == data["author-selected.txt"],
                "Follow-up selection differs")
        text, error = extract_noose(data["raw.html"], {"requestUrl": URL, "finalUrl": receipt["finalUrl"]})
        require(error is None and text, f"Independent extraction failed: {error}")
        require(all(path.read_bytes() == data[name] for name, path in paths.items()),
                "Author capture changed during snapshot")
        data["complete-extract.txt"] = text.encode("utf-8")
        outputs = {name: write_frozen(OUTPUT / name, raw) for name, raw in data.items()}
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Follow-up capture RAM guard breached")
    print(json.dumps(freeze_json(OUTPUT / "manifest.json", {
        "batch": 129, "status": "PASS_CAPTURE_SNAPSHOT_ONLY", "character": CHARACTER,
        "requestUrl": URL, "finalUrl": receipt["finalUrl"], "capturedAt": receipt["capturedAt"],
        "sourceReceiptPath": str(paths["receipt.json"]), "outputs": outputs,
        "method": "Require this exact compound URL, redirect and complete title headword; " + METHOD,
        "helpers": HELPERS, "memory": memory,
        "producerSha256": sha(Path(__file__).read_bytes()),
        "preservedFailure": {
            "execution": str(REVIEW / "revision-noose-external-execution-001"),
            "producerSha256": "c7ce964d0aa00346ed2e65a51b19ff3083c3806de9e5f22bcb9e0b5a55466906",
            "reason": "The original single-character adapter correctly rejected the two-character "
                      "headword before writing outputs. This producer uses the underlying full-body "
                      "extractor only after an exact compound identity check; no fabricated URL.",
        },
        "limits": "Additional exact-noun capture only. Complete HTML independently extracted; author "
                  "article JSON/selection checked for internal agreement, not independently reproduced. "
                  "Bind these bytes to the signed successor before acceptance. The JMdict zero-match "
                  "does not negate positive monolingual evidence or resolve the swing/noose discrepancy.",
    })))


if __name__ == "__main__":
    main()
