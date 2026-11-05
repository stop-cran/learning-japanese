import hashlib
import json
import shutil
import subprocess
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
folder = root / "docs" / "n1-reviews" / "batch-063-native"
receipts = folder / "execution-receipts"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(path) == value


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


index_path = folder / "execution-396-artifact-index.json"
index = load(index_path)
assert len(index["files"]) == 58
for source in [Path(__file__)] + [
    control / "logs" / f"execution-396-{name}.txt"
    for name in ("validate", "manifest", "budget")
]:
    destination = receipts / source.name
    assert not destination.exists()
    shutil.copyfile(source, destination)
    assert sha(source) == sha(destination)
    index["files"].append({
        "path": str(destination.relative_to(root)),
        "bytes": destination.stat().st_size,
        "sha256": sha(destination),
    })
duplicate_groups = {}
for name in index["directCoordinatorImageRequests"]:
    duplicate_groups.setdefault(sha(folder / "attempt-1" / name), []).append(name)
index["duplicateDirectImageGroups"] = [names for names in duplicate_groups.values() if len(names) > 1]
assert index["duplicateDirectImageGroups"] == [[
    "n1-063-kanji-on-reading.png", "n1-063-kanji-kun-reading.png", "n1-063-imitation-backlink.png"
]]
index["limits"] = (
    "Fourteen direct coordinator image requests / twelve distinct hashes. "
    "On-reading, kun-reading and imitation-backlink captures have identical bytes. "
    "Not every captured image or independent visual acceptance. Hashes establish bytes, not readability."
)
save(index_path, index)
for entry in index["files"]:
    assert sha(root / entry["path"]) == entry["sha256"]
record_path = root / "docs" / "n1-sources" / "execution-396.json"
record = load(record_path)
record["artifactIndexSha256"] = sha(index_path)
record["validation"] = [
    {
        "check": name, "exitCode": 0,
        "log": str((receipts / f"execution-396-{name}.txt").relative_to(root)),
        "sha256": sha(receipts / f"execution-396-{name}.txt"),
    }
    for name in ("validate", "manifest", "budget")
]
record["glyphEvidence"]["duplicateDirectImageGroups"] = index["duplicateDirectImageGroups"]
record["glyphEvidence"]["limits"] += " On-reading/kun-reading/imitation-backlink form one byte-identical group."
record["runtimeUnchangedAfterValidation"] = not subprocess.check_output(
    ["git", "diff", "--name-only", record["startingHead"], "--",
     "kanji", "words", "strokes", "articles", "manifest.json", "grammar", "listening"],
    cwd=root,
)
assert record["runtimeUnchangedAfterValidation"]
record["originalPublishingBudgets"] = {
    "entries": 8339, "entryLimit": 18000,
    "retainedBytes": 44021291, "retainedLimit": 56 * 1024 * 1024,
    "inflatedBytes": 44289629, "inflatedLimit": 80 * 1024 * 1024,
    "localZipBytes": 30102781, "compressedLimit": 42 * 1024 * 1024,
}
save(record_path, record)
path = control / "progress.json"
progress = load(path)
assert progress["checkpoint"] == 396 and progress["status"] == "continue"
for key in ("execution396CoordinatorCheckpoint", "batch063NativeExecutionCheckpoint"):
    progress[key]["artifactIndexSha256"] = sha(index_path)
    progress[key]["validation"] = record["validation"]
    progress[key]["runtimeUnchanged"] = True
    progress[key]["fullHistoryCompared"] = True
progress["execution396StartingState"]["status"] = "native-assertions-archived-pending-signing"
before = load(control / "execution-396-progress-before.json")
mutable = {"checkpoint", "status", "stage", "nextAction", "blocker", "activeExecution"}
for key, value in before.items():
    if key not in mutable:
        assert progress[key] == value, key
save(path, progress)
print(json.dumps({
    "checkpoint": 396, "indexedArtifacts": len(index["files"]),
    "pngs": index["sourcePngCount"], "distinctDirectImages": index["distinctDirectImageHashes"],
    "preservedHistoricalKeys": len(before) - len(mutable),
    "runtimeUnchanged": record["runtimeUnchangedAfterValidation"],
}, indent=2))
