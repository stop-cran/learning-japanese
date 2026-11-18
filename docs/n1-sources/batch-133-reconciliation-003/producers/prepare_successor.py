import importlib.util
import json
import re
import stat
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import REPO, git, sha, start_guard, write
from notes import PARENT, expected_after


def binding(path):
    return {"path": str(path), "sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        previous = OUT.parent / "teaching-reconciliation-002"
        sources = OUT.parent / "review" / "claude-confirm-002-adjudication-sources-001"
        admission_path = OUT.parent / "review" / "teaching-reconciliation-admission-003" / "admission.json"
        assert sha(admission_path.read_bytes()) == "5da5555a650a9baa32167d3377d290a51507a7eec2c528933d2b9d860b05e4bb"
        admission = json.loads(admission_path.read_bytes())
        authorities = [binding(admission_path), admission["brief"], admission["decision"], *admission["bindings"].values()]
        for item in authorities:
            guard.check()
            path = Path(item["path"])
            assert sha(path.read_bytes()) == item["sha256"]
            assert path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
        before = (OUT / "before-滝.md").read_bytes()
        assert before == git("show", PARENT + ":kanji/滝.md") == (REPO / "kanji" / "滝.md").read_bytes()
        assert before.count(b"\r\n") == 101
        for name in ("gates.py", "sign.py"):
            assert (OUT / name).read_bytes() == (previous / name).read_bytes()
        for ch in ("酒", "液"):
            assert (OUT / ("counterpart-" + ch + ".md")).read_bytes() == git("show", PARENT + ":kanji/" + ch + ".md")
        raw = (sources / "takisui-kotobank.html").read_bytes()
        assert sha(raw) == "5100a307551e7d6bf0f92665c5783cdd010fe85c6a49b9cbdc618af3d440099f"
        spec = importlib.util.spec_from_file_location("verified_takisui_extractor", sources / "extract_takisui.py")
        extractor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(extractor)
        output = []
        articles = re.findall(r"<article\b.*?</article>", raw.decode("utf-8"), flags=re.S)
        for i, article in enumerate(articles, 1):
            output.append(f"=== article {i}")
            output.extend(extractor.text_lines(article))
        rebuilt = ("\n".join(output) + "\n").encode()
        assert rebuilt == (sources / "takisui-sections.txt").read_bytes() == (OUT / "source-sections" / "takisui-sections.txt").read_bytes()
        assert sha(rebuilt) == "38244158be21a6a1aac5cfa5b5b94ad8493b0a9e45e606ec3bb269bba332d0c8"
        receipt = json.loads((sources / "takisui-sections.receipt.json").read_bytes())
        assert receipt["captureSha256"] == sha(raw) and receipt["outputSha256"] == sha(rebuilt)
        assert receipt["articles"] == len(articles) == 2
        definitions = []
        for first, last in ((4, 5), (6, 7), (8, 9)):
            headword, definition = output[first - 1:last]
            definitions.append({"sourceLines": [first, last], "headword": headword,
                                "definition": definition.split("[初出の実例]", 1)[0].strip(),
                                "selection": "Headword and definition only; explicitly exclude the following historical usage example."})
        failed = OUT.parent / "review" / "teaching3-prepare-001"
        assert json.loads((failed / "receipt.json").read_bytes())["exitCode"] == 1
        failure = {
            "originalProducer": binding(OUT / "prepare.py"), "receipt": binding(failed / "receipt.json"),
            "log": binding(failed / "output.log"), "verdict": "FAILED_UNCHANGED",
            "cause": "Original producer tested LF text literals against the 101-CRLF raw Git article. Raw matches were [1,0,0]; normalized matches [1,1,1]. Failure occurred before source-bindings.json or any runtime edit.",
            "successor": "Normalize only runtime text before the exact-transform assertion; preserve raw before/source/evidence bytes. Existing partial copies are byte-verified, not overwritten."
        }
        data = {
            "authorities": authorities, "coordinatorCapture": binding(sources / "takisui-kotobank.html"),
            "url": receipt["url"], "completeSections": binding(sources / "takisui-sections.txt"),
            "localCompleteSections": binding(OUT / "source-sections" / "takisui-sections.txt"),
            "extractor": binding(sources / "extract_takisui.py"),
            "extractorReceipt": binding(sources / "takisui-sections.receipt.json"),
            "responseHeaders": binding(sources / "takisui-kotobank.headers.txt"),
            "frozenHttpStatus": 200, "extractionReproducedByteForByte": True,
            "boundedDefinitions": definitions,
            "supportingFrozenSections": [binding(previous / "source-sections" / name) for name in
                                        ("滝-nikkoku.txt", "滝-jitsu.txt", "液-daijisen.txt")],
            "previousLocalInventory": binding(previous / "inventory.json"),
            "expectedAfterRuntimeSha256": sha(expected_after(before.replace(b"\r\n", b"\n").decode()).encode()),
            "preparationFailure": failure, "successfulProducer": binding(Path(__file__)),
            "limits": "No refetch. Complete captures/publisher sections stay local. Extracted visible text is not raw HTML; images not fetched/interpreted. Separate modern-brand publisher section is retained but not relied upon. Compound readings たきすい/たきみず/ろうすい are not independent 滝 readings."
        }
        write(OUT / "source-bindings.json", data)
        print(json.dumps({"status": "PASS", "completeExtractionReproduced": True,
                          "expectedAfterRuntimeSha256": data["expectedAfterRuntimeSha256"],
                          "originalPreparationFailurePreserved": True}))
    finally:
        write(OUT / "prepare-successor-memory.json", guard.finish())


if __name__ == "__main__":
    main()
