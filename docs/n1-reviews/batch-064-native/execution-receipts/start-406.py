import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
request = control / "logs" / "9f190156-65ab-41bb-8896-f6fcb5b92cad" / "request.txt"
raw = request.read_text(encoding="utf-8-sig")
embedded = json.loads(raw.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 405
assert progress["batch"] == "064" and progress["status"] == "continue"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "3222f60a83b844d09b47d63bb533316a34307faf"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
assert "execution406StartingState" not in progress
(control / "execution-406-progress-before.json").write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
record = {
    "execution": 406, "batch": "064", "startingHead": head,
    "scope": "SAME064 compiled native fixture execution, exact evidence archival and signed local checkpoint only. No reviewer, runtime publication,065 or second runner.",
    "status": "starting-native-execution",
    "authorization": {
        "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "characters": len(raw), "lines": len(raw.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete final405 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["execution406StartingState"] = record
progress["activeExecution"] = record
progress["stage"] = "batch-064-native-execution"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(control / "execution-406-start.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution406 scope persisted; full live history retained.")
