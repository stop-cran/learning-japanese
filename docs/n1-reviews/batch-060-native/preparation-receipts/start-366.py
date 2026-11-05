import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
request = control / "logs" / "8327db1a-6be4-4e90-9f27-d86089e17e4e" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
embedded = json.loads(text[text.index("{", text.index("Current execution checkpoint")):])
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 365
assert progress["status"] == "continue" and progress["batch"] == "060"
assert "execution366StartingState" not in progress
progress["execution366StartingState"] = {
    "execution": 366, "batch": "060",
    "startingHead": "99d8ace026aaf5cf76b4adada34b14e969d10d4e",
    "scope": "SAME060 exact-full-archive native fixture preparation, serial compilation and normally signed local evidence checkpoint only. No native launch, reviewer, runtime publication,061 or second runner.",
    "status": "preparing-native-fixture",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text), "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete final365 checkpoint and approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["stage"] = "batch-060-native-fixture-preparation"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Full live history preserved; execution366 preparation scope recorded.")
