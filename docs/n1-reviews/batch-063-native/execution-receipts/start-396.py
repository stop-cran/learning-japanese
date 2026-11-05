import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
request = control / "logs" / "55ac28ae-0527-469f-b063-6192eacc1d2c" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 395
assert progress["status"] == "continue" and progress["batch"] == "063"
assert "execution396StartingState" not in progress
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "a652b88561ccd50577375f97af08f8004fbd641a"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
backup = control / "execution-396-progress-before.json"
assert not backup.exists()
shutil.copyfile(path, backup)
state = {
    "execution": 396, "batch": "063", "startingHead": head,
    "scope": "SAME063 compiled native fixture execution, direct evidence inspection and durable signed local checkpoint only. No reviewer, runtime publication,064 or second runner.",
    "status": "starting-native-execution",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text), "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete final395 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["execution396StartingState"] = state
progress["activeExecution"] = state
progress["stage"] = "batch-063-native-executing"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert json.loads(path.read_text(encoding="utf-8")) == progress
print(json.dumps(state, indent=2))
