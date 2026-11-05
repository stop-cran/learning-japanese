import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
request = control / "logs" / "147e9f3a-8b42-4837-9b15-839df356dd9c" / "request.txt"
raw = request.read_text(encoding="utf-8-sig")
embedded = json.loads(raw.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 384
assert progress["batch"] == "062" and progress["status"] == "continue"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "e157d58c5bdb9fc2d58d7043fdf0429d36f5c040"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
record = {
    "execution": 385,
    "batch": "062",
    "startingHead": head,
    "scope": "SAME062 exact-full-git-archive native fixture preparation, serial compilation and normally signed local evidence checkpoint only; no native launch, reviewer, publication,063 or second runner.",
    "status": "preparing-native-fixture",
    "authorization": {
        "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "characters": len(raw),
        "lines": len(raw.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete final384 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "historicalRootKeysAtStart": len(progress),
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
assert "execution385StartingState" not in progress
progress["execution385StartingState"] = record
progress["stage"] = "batch-062-native-fixture-preparation"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(control / "execution-385-start.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution385 starting scope persisted; complete live history retained.")
