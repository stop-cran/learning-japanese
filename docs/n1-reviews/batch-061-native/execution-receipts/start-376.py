import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
path = control / "progress.json"
request = control / "logs" / "96c14184-06ca-4c58-a3ea-ed3acf70d5df" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
embedded = json.loads(text.split(
    "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
)[1])
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 375
assert progress["status"] == "continue" and progress["batch"] == "061"
assert "execution376StartingState" not in progress
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "46904016c058ad1609a4004079d9cc16b0988bfa"
backup = control / "execution-376-progress-before.json"
assert not backup.exists()
shutil.copyfile(path, backup)
state = {
    "execution": 376,
    "batch": "061",
    "startingHead": head,
    "scope": "SAME061 compiled native fixture execution, direct evidence inspection and durable signed local checkpoint only. No reviewer, runtime publication,062 or second runner.",
    "status": "starting-native-execution",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete final375 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["execution376StartingState"] = state
progress["activeExecution"] = state
progress["stage"] = "batch-061-native-executing"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert json.loads(path.read_text(encoding="utf-8")) == progress
print(json.dumps(state, ensure_ascii=False, indent=2))
