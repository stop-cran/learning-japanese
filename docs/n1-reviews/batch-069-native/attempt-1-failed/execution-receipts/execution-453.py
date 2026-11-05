import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CONTROL = Path(__file__).parent
CONTENT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
PROGRESS = CONTROL / "progress.json"
REQUEST = CONTROL / "logs" / "6a71d700-ec79-4e62-9644-4f790eff7082" / "request.txt"
TARGET = CONTENT / "docs" / "n1-reviews" / "batch-069-native"
SOURCE = CONTROL / "artifacts" / "batch-069-native-attempt-1"
HEAD = "e60c35c6536bdae22e18d3bba8aa4649b90a460d"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(directory, *args):
    return subprocess.check_output(["git", "-C", str(directory), *args], timeout=30, encoding="utf-8").strip()


def start():
    raw = REQUEST.read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(PROGRESS)
    assert p["checkpoint"] == embedded["checkpoint"] == 452 and p["batch"] == "069"
    assert "execution453StartingState" not in p
    assert git(CONTENT, "rev-parse", "HEAD") == HEAD and not git(CONTENT, "status", "--porcelain")
    assert git(ANDROID, "rev-parse", "HEAD") == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git(ANDROID, "status", "--porcelain")
    state = {
        "execution": 453, "batch": "069", "startingHead": HEAD,
        "scope": "SAME069 compiled native execution, evidence archival, direct bounded PNG inspection and normally signed local checkpoint only. No reviewer/publication/070/second runner.",
        "status": "executing-native-checkpoint", "recordedAt": datetime.now(timezone.utc).isoformat(),
        "authorization": {
            "requestSha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final452 checkpoint, approved issue and current native preparations inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "originMainFreshFetch": git(CONTENT, "rev-parse", "origin/main"),
    }
    save(CONTROL / "execution-453-start.json", state)
    p["execution453StartingState"] = state
    p["stage"] = "batch-069-native-execution-in-progress"
    save(PROGRESS, p)
    print(json.dumps(state, ensure_ascii=False, indent=2))


def archive():
    execution = load(SOURCE / "execution.json")
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    route = load(SOURCE / "n1-069-article-route.json")
    assert route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"]) == (1081, 5038, 101)
    assert route["contentVersion"] == "83ed94552dd1a9ce" and route["problems"] == 0
    assert route["fullOnyomi"] == ["ジュ"] and route["fullKunyomi"] == []
    assert route["quizOnKeys"] == ["じゅ"] and route["quizKunKeys"] == []
    assert route["acceptedReadingParserEpoch"] == 1
    if execution["passed"]:
        assert execution["terminalSuccessCases"] == 2 and route["passed"]
        for key in ["reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                    "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
                    "drawingGradeRecordedOnNext", "offline"]:
            assert route[key]
        assert route["touchInjectedReferenceStrokes"] == 16
        target = TARGET
    else:
        assert execution["terminalSuccessCases"] == 1 and not route["passed"]
        target = TARGET / "attempt-1-failed"
        target.mkdir()
    rows = load(SOURCE / "n1-069-font-raster.json")
    assert len(rows["rows"]) == 60 and rows["individualGlyphProbes"] == 56 and rows["wholeWordRasterProbes"] == 4
    indexed = []
    for original in sorted(SOURCE.iterdir()):
        if not original.is_file():
            continue
        dest = target / original.name
        if original.suffix == ".txt":
            raw = original.read_bytes()
            normalized = "\n".join(line.rstrip() for line in raw.decode("utf-8-sig").splitlines()).rstrip() + "\n"
            assert not dest.exists()
            dest.write_text(normalized, encoding="utf-8", newline="\n")
            gz = target / (original.name + ".raw.gz")
            assert not gz.exists()
            gz.write_bytes(gzip.compress(raw, mtime=0))
            entry = {"path": str(dest.relative_to(CONTENT)), "sourcePath": str(original),
                     "originalBytes": len(raw), "originalSha256": sha(original),
                     "sha256": sha(dest), "bytes": dest.stat().st_size,
                     "rawGzipPath": str(gz.relative_to(CONTENT)), "rawGzipSha256": sha(gz)}
        else:
            if dest.exists():
                assert sha(dest) == sha(original), f"Refusing overwrite: {dest}"
            else:
                shutil.copyfile(original, dest)
            entry = {"path": str(dest.relative_to(CONTENT)), "sourcePath": str(original),
                     "sha256": sha(dest), "bytes": dest.stat().st_size}
        indexed.append(entry)
    receipts = target / "execution-receipts"
    receipts.mkdir(exist_ok=True)
    for name in ["run-453-native.ps1", "execution-453.py", "execution-453-start.json"]:
        shutil.copyfile(CONTROL / name, receipts / name)
    index = target / "execution-453-artifact-index.json"
    save(index, {"execution": 453, "batch": "069", "artifacts": indexed,
                 "normalization": "Readable text copies use UTF-8 LF and trim trailing whitespace. Deterministic gzip preserves original text bytes. PNG/JSON/fixture bytes copied unchanged. Original attempt retained in control."})
    print(json.dumps({"index": str(index), "sha256": sha(index),
                      "sourceFiles": len(indexed), "pngs": len(list(SOURCE.glob("*.png")))}, indent=2))


def checks():
    results = []
    for name, tool in [("validate-453", "validate.py"), ("manifest-453", "build_manifest.py")]:
        run = subprocess.run([sys.executable, "-B", str(CONTENT / "tools" / tool)],
                             cwd=CONTENT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        path = TARGET / (name + ".txt")
        path.write_bytes(run.stdout)
        results.append({"check": name, "exitCode": run.returncode,
                        "path": str(path.relative_to(CONTENT)), "sha256": sha(path)})
        if run.returncode:
            save(CONTROL / "execution-453-checks.json", results)
            raise RuntimeError(f"{name} failed: {run.stdout.decode('utf-8', errors='replace')}")
    assert not git(CONTENT, "diff", "--name-only", "--", "manifest.json")
    save(CONTROL / "execution-453-checks.json", results)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "retry1":
        SOURCE = CONTROL / "artifacts" / "batch-069-native-attempt-2"
    {"start": start, "archive": archive, "checks": checks}[sys.argv[1]]()
