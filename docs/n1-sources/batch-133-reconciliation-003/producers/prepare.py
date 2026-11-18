import importlib.util
import json
import re
import stat
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import REPO, git, sha, start_guard, write
from notes import PARENT, REL, expected_after

PREVIOUS = OUT.parent / "teaching-reconciliation-002"
SOURCES = OUT.parent / "review" / "claude-confirm-002-adjudication-sources-001"


def binding(path):
    return {"path": str(path), "sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        assert not (REPO / REL).exists()
        admission_path = OUT.parent / "review" / "teaching-reconciliation-admission-003" / "admission.json"
        assert sha(admission_path.read_bytes()) == "5da5555a650a9baa32167d3377d290a51507a7eec2c528933d2b9d860b05e4bb"
        admission = json.loads(admission_path.read_bytes())
        authorities = [binding(admission_path), admission["brief"], admission["decision"], *admission["bindings"].values()]
        for item in authorities:
            guard.check()
            path = Path(item["path"])
            assert sha(path.read_bytes()) == item["sha256"]
            assert path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
        for path in SOURCES.iterdir():
            assert path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
        headers = (SOURCES / "takisui-kotobank.headers.txt").read_text(encoding="utf-8")
        assert headers.startswith("HTTP/1.1 200 OK\n")
        inventory_path = PREVIOUS / "inventory.json"
        assert sha(inventory_path.read_bytes()) == "86241103dc690acc510378e95c0c351f9e6a803a8ac9076a9c46d677aa161c6a"
        inventory = json.loads(inventory_path.read_bytes())["files"]
        assert {str(p.relative_to(PREVIOUS)) for p in PREVIOUS.rglob("*") if p.is_file()} == set(inventory) | {"inventory.json"}
        for relative, details in inventory.items():
            guard.check()
            path = PREVIOUS / relative
            assert sha(path.read_bytes()) == details["sha256"]
            assert path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
        for name in ("gates.py", "sign.py"):
            write(OUT / name, (PREVIOUS / name).read_bytes())
            compile((OUT / name).read_bytes(), str(OUT / name), "exec")
        before = git("show", PARENT + ":kanji/滝.md")
        assert before == (REPO / "kanji" / "滝.md").read_bytes()
        write(OUT / "before-滝.md", before)
        write(OUT / "counterpart-酒.md", git("show", PARENT + ":kanji/酒.md"))
        write(OUT / "counterpart-液.md", git("show", PARENT + ":kanji/液.md"))
        assert b"title: alcohol; sake\n" in (OUT / "counterpart-酒.md").read_bytes()
        raw = (SOURCES / "takisui-kotobank.html").read_bytes()
        assert sha(raw) == "5100a307551e7d6bf0f92665c5783cdd010fe85c6a49b9cbdc618af3d440099f"
        spec = importlib.util.spec_from_file_location("frozen_takisui_extractor", SOURCES / "extract_takisui.py")
        extractor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(extractor)
        articles = re.findall(r"<article\b.*?</article>", raw.decode("utf-8"), flags=re.S)
        output = []
        for i, article in enumerate(articles, 1):
            output.append(f"=== article {i}")
            output.extend(extractor.text_lines(article))
        rebuilt = ("\n".join(output) + "\n").encode()
        assert rebuilt == (SOURCES / "takisui-sections.txt").read_bytes()
        assert sha(rebuilt) == "38244158be21a6a1aac5cfa5b5b94ad8493b0a9e45e606ec3bb269bba332d0c8"
        receipt = json.loads((SOURCES / "takisui-sections.receipt.json").read_bytes())
        assert receipt["captureSha256"] == sha(raw) and receipt["outputSha256"] == sha(rebuilt)
        assert receipt["articles"] == len(articles) == 2
        write(OUT / "source-sections" / "takisui-sections.txt", rebuilt)
        definitions = []
        for first, last in ((4, 5), (6, 7), (8, 9)):
            headword, definition = output[first - 1:last]
            definitions.append({"sourceLines": [first, last], "headword": headword,
                                "definition": definition.split("[初出の実例]", 1)[0].strip(),
                                "selection": "Headword and definition only; explicitly exclude the following historical usage example."})
        bindings = {
            "authorities": authorities,
            "coordinatorCapture": binding(SOURCES / "takisui-kotobank.html"),
            "url": receipt["url"], "completeSections": binding(SOURCES / "takisui-sections.txt"),
            "localCompleteSections": binding(OUT / "source-sections" / "takisui-sections.txt"),
            "extractor": binding(SOURCES / "extract_takisui.py"),
            "extractorReceipt": binding(SOURCES / "takisui-sections.receipt.json"),
            "responseHeaders": binding(SOURCES / "takisui-kotobank.headers.txt"),
            "frozenHttpStatus": 200,
            "extractionReproducedByteForByte": True,
            "boundedDefinitions": definitions,
            "supportingFrozenSections": [binding(PREVIOUS / "source-sections" / name) for name in
                                        ("滝-nikkoku.txt", "滝-jitsu.txt", "液-daijisen.txt")],
            "previousLocalInventory": binding(inventory_path),
            "expectedAfterRuntimeSha256": sha(expected_after(before.decode()).encode()),
            "limits": "No refetch. Complete capture and complete publisher sections stay local. Extracted visible text is not a raw HTML slice; no images fetched/interpreted. Separate modern brand publisher article is retained in complete extraction but not relied upon. Compound readings たきすい/たきみず/ろうすい are not independent character readings of 滝."
        }
        write(OUT / "source-bindings.json", bindings)
        print(json.dumps({"status": "PASS", "parent": PARENT, "completeExtractionReproduced": True,
                          "expectedAfterSha256": bindings["expectedAfterRuntimeSha256"]}))
    finally:
        write(OUT / "prepare-memory.json", guard.finish())


if __name__ == "__main__":
    main()
