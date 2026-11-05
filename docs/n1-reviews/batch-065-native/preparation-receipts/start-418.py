import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
request = control / "logs" / "bdea2f71-f278-46a5-93ac-f532be61b300" / "request.txt"
raw = request.read_text(encoding="utf-8-sig")
embedded = json.loads(raw.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 417
assert progress["batch"] == "065" and progress["status"] == "continue"
assert "execution418StartingState" not in progress
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "ee672744235275d321b4bfb33a6efe0286444594"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
record = {
    "execution": 418, "batch": "065", "startingHead": head,
    "scope": "SAME065 exact-full-git-archive native fixture preparation, serial compilation and normally signed local evidence checkpoint only. No native launch, reviewer, runtime publication,066 or second runner.",
    "status": "preparing-native-fixture",
    "authorization": {
        "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "characters": len(raw), "lines": len(raw.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, final417 checkpoint and complete approved issue inspected directly. Historical middle acquired/parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
(control / "execution-418-before-progress.json").write_bytes(path.read_bytes())
progress["execution418StartingState"] = record
progress["stage"] = "batch-065-native-fixture-preparation"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(control / "execution-418-start.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution418 scope saved; full live history retained.")
