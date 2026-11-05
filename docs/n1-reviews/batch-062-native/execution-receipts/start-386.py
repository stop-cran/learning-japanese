import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
path = control / "progress.json"
request = control / "logs" / "06bdd48a-e470-4db7-ba1b-945a6ac66e41" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
embedded = json.loads(text.split(
    "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
)[1])
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 385
assert progress["status"] == "continue" and progress["batch"] == "062"
assert "execution386StartingState" not in progress
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "c81a07626f7a051879700c003b2a138808a18fed"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
backup = control / "execution-386-progress-before.json"
assert not backup.exists()
shutil.copyfile(path, backup)
state = {
    "execution": 386,
    "batch": "062",
    "startingHead": head,
    "scope": "SAME062 compiled native fixture execution, direct evidence inspection and durable signed local checkpoint only. No reviewer, runtime publication,063 or second runner.",
    "status": "starting-native-execution",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete final385 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["execution386StartingState"] = state
progress["activeExecution"] = state
progress["stage"] = "batch-062-native-executing"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert json.loads(path.read_text(encoding="utf-8")) == progress
print(json.dumps(state, ensure_ascii=False, indent=2))
