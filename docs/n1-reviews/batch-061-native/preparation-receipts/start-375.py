import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
request = control / "logs" / "b820574d-a160-41d5-96c9-462403f0aa34" / "request.txt"
raw = request.read_text(encoding="utf-8-sig")
embedded = json.loads(raw[raw.index("{", raw.index("Current execution checkpoint")):])
progress_path = control / "progress.json"
progress = json.loads(progress_path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 374
assert progress["batch"] == "061" and progress["status"] == "continue"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "f891cb1e0b43c4fefcb31da16f28f3159b49aea4"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
record = {
    "execution": 375,
    "batch": "061",
    "startingHead": head,
    "scope": "SAME061 exact-full-git-archive native fixture preparation, serial compilation and signed local evidence checkpoint only; no native launch, reviewer, publication,062 or second runner.",
    "status": "preparing-native-fixture",
    "authorization": {
        "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "characters": len(raw),
        "lines": len(raw.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative authorization, complete final374 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
assert "execution375StartingState" not in progress
progress["execution375StartingState"] = record
progress["stage"] = "batch-061-native-fixture-preparation"
progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(control / "execution-375-start.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(record, ensure_ascii=False, indent=2))
