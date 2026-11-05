import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
request = control / "logs" / "90f1816e-9dd2-4f59-ba6b-106bfdc45098" / "request.txt"
raw = request.read_text(encoding="utf-8-sig")
embedded = json.loads(raw.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 404
assert progress["batch"] == "064" and progress["status"] == "continue"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "bf6204e5b4e4c64f340dcd8db65b2924b869cc45"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
assert "execution405StartingState" not in progress
record = {
    "execution": 405, "batch": "064", "startingHead": head,
    "scope": "SAME064 exact-full-git-archive native fixture preparation, serial compilation and normally signed local evidence checkpoint only; no native launch, reviewer, runtime publication,065 or second runner.",
    "status": "preparing-native-fixture",
    "authorization": {
        "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "characters": len(raw), "lines": len(raw.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete final404 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "historicalRootKeysAtStart": len(progress),
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["execution405StartingState"] = record
progress["stage"] = "batch-064-native-fixture-preparation"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(control / "execution-405-start.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution405 scope persisted; complete request parsed and live history retained.")
