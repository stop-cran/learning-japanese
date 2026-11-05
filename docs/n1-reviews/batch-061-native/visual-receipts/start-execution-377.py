import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
request = C / "logs" / "bc967a6b-3508-4e8b-af66-014a5130f98c" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
embedded = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
p = C / "progress.json"
original = p.read_bytes()
progress = json.loads(original)
assert progress["checkpoint"] == embedded["checkpoint"] == 376
assert progress["batch"] == "061"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip()
assert head == "f2267727d982589890b2f4ae0b17e82666337956"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=R, text=True).strip()
backup = C / "execution-377-starting-progress.json"
assert not backup.exists()
backup.write_bytes(original)
record = {
    "execution": 377, "batch": "061", "startingHead": head,
    "startedAt": datetime.now().astimezone().isoformat(),
    "scope": "SAME061 original-session two-family serial dependent visual review, reconciliation and normally signed local evidence checkpoint only. No teaching edits, accepted Android/native rerun, publication,062 or second runner.",
    "status": "preparing-bounded-dependent-visual-review",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text), "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired into memory and complete embedded checkpoint parsed. Operative contract, complete approved issue and complete final376/current061 checkpoint inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
}
progress["execution377StartingState"] = record
p.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(C / "execution-377-start.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(record, ensure_ascii=False, indent=2))
