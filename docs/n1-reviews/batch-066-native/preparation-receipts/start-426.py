import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
request = control / "logs" / "42873968-2117-4b32-854a-e4948b99ca47" / "request.txt"
raw = request.read_text(encoding="utf-8-sig")
embedded = json.loads(raw.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 425
assert progress["batch"] == "066" and progress["status"] == "continue"
assert "execution426StartingState" not in progress
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "175fdf3f1605f231e27a9de19a7c18c4a02cb20d"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
record = {
    "execution": 426, "batch": "066", "startingHead": head,
    "scope": "SAME066 exact-full-git-archive native fixture preparation, serial compilation and normally signed local evidence checkpoint only. No native launch, reviewer, runtime publication,067 or second runner.",
    "status": "preparing-native-fixture",
    "authorization": {
        "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "characters": len(raw), "lines": len(raw.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, final425 checkpoint and complete approved issue inspected directly. Historical middle acquired/parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
(control / "execution-426-before-progress.json").write_bytes(path.read_bytes())
progress["execution426StartingState"] = record
progress["stage"] = "batch-066-native-fixture-preparation"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(control / "execution-426-start.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution426 scope saved; full live history retained.")
