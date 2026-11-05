import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
START = "8f9bad077f40cac9a31523a27d192accc59dcd0d"
TEACHING = "ea1dac1a6fd2c452db9cf602442e1f287ff95c67"


def save(path, value):
    assert not path.exists(), path
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    request_path = C / "logs" / "25e40f50-a72e-429a-a0a1-c528c8307f69" / "request.txt"
    request = request_path.read_text(encoding="utf-8")
    embedded = json.loads(request[request.index("{", request.index("Current execution checkpoint")):])
    progress_path = C / "progress.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8-sig"))
    assert embedded["checkpoint"] == progress["checkpoint"] == 367
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip() == START
    assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=R, text=True).strip()
    assert not subprocess.check_output(
        ["git", "diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json"],
        cwd=R, text=True,
    ).strip()
    save(C / "execution-368-starting-progress.json", progress)
    record = {
        "execution": 368, "batch": "060", "startingHead": START,
        "startedAt": datetime.now().astimezone().isoformat(),
        "scope": "SAME060 bounded dependent native visual confirmation in the two original reviewer sessions, serially, and normally signed local evidence checkpoint only. No teaching edits, accepted Android/native rerun, publication,061 or second runner.",
        "authorization": {
            "requestSha256": hashlib.sha256(request_path.read_bytes()).hexdigest(),
            "characters": len(request), "lines": len(request.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed. Operative contract, complete approved issue and complete final367/current060 checkpoint inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
        },
        "status": "preparing-bounded-original-session-native-visual-confirmation",
    }
    progress["execution368StartingState"] = record
    progress["stage"] = "batch-060-original-session-native-visual-confirmation"
    progress["nextAction"] = record["scope"]
    progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save(C / "execution-368-start.json", record)
    for label, args in [("help", ["copilot", "--help"]), ("model-catalog", ["copilot", "help", "config"])]:
        result = subprocess.run(args, text=True, encoding="utf-8", capture_output=True, check=True)
        (V / f"batch-060-copilot-{label}-execution-368.txt").write_text(result.stdout.rstrip() + "\n", encoding="utf-8")
    index = json.loads((V / "batch-060-native" / "execution-367-artifact-index.json").read_text(encoding="utf-8"))
    groups = {}
    for row in index["files"]:
        path = R / row["path"]
        assert path.stat().st_size == row["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        if path.suffix == ".png":
            groups.setdefault(row["sha256"], []).append(path.name)
    freeze = {
        "snapshot": START, "teachingSnapshot": TEACHING,
        "artifactIndexSha256": hashlib.sha256((V / "batch-060-native" / "execution-367-artifact-index.json").read_bytes()).hexdigest(),
        "sourcePngCount": sum(map(len, groups.values())),
        "distinctPngCount": len(groups),
        "groups": [{"sha256": key, "representative": names[0], "equivalentNames": names} for key, names in groups.items()],
    }
    save(C / "batch-060-visual-freeze.json", freeze)
    print(json.dumps(freeze, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
