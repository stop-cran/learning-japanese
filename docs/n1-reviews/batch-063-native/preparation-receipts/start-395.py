import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
request = control / "logs" / "26d26d7d-31ea-4398-bdba-f322f0c10428" / "request.txt"
raw = request.read_text(encoding="utf-8-sig")
embedded = json.loads(raw.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 394
assert progress["batch"] == "063" and progress["status"] == "continue"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "53ecd11711804be900ca95f9f1018942910aecec"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
assert "execution395StartingState" not in progress
record = {
    "execution": 395, "batch": "063", "startingHead": head,
    "scope": "SAME063 exact-full-git-archive native fixture preparation, serial compilation and normally signed local evidence checkpoint only; no native launch, reviewer, publication,064 or second runner.",
    "status": "preparing-native-fixture",
    "authorization": {
        "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "characters": len(raw), "lines": len(raw.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete final394 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "historicalRootKeysAtStart": len(progress),
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["execution395StartingState"] = record
progress["stage"] = "batch-063-native-fixture-preparation"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(control / "execution-395-start.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution395 scope persisted; complete request parsed and live history retained.")
