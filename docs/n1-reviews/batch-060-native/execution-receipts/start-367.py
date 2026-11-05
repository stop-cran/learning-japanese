import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
path = control / "progress.json"
request = control / "logs" / "a7d98aca-61c9-452e-a566-7c96416331d4" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
embedded = json.loads(text.split(
    "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
)[1])
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 366
assert progress["status"] == "continue" and progress["batch"] == "060"
assert "execution367StartingState" not in progress
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "3baaf2863e54a7f403723e2958330bc1d4f9674d"
backup = control / "execution-367-progress-before.json"
assert not backup.exists()
shutil.copyfile(path, backup)
state = {
    "execution": 367,
    "batch": "060",
    "startingHead": head,
    "scope": "SAME060 compiled native fixture execution, direct evidence inspection and durable signed local checkpoint only. No reviewer, runtime publication,061 or second runner.",
    "status": "starting-native-execution",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete final366 checkpoint and approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["execution367StartingState"] = state
progress["activeExecution"] = state
progress["stage"] = "batch-060-native-executing"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert json.loads(path.read_text(encoding="utf-8")) == progress
print(json.dumps(state, ensure_ascii=False, indent=2))
