import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
request = control / "logs" / "d1def87c-01fa-4af8-b997-5b4c5a67c656" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
embedded = json.loads(text[text.index("{", text.index("Current execution checkpoint")):])
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 355
assert progress["status"] == "continue" and progress["batch"] == "059"
assert "execution356StartingState" not in progress
progress["execution356StartingState"] = {
    "execution": 356,
    "batch": "059",
    "startingHead": "911431dad205cf031e1df9f561a47748c060439b",
    "scope": "SAME059 exact-full-archive native fixture preparation, serial compilation and signed local evidence checkpoint only. No native launch, reviewer, runtime publication,060 or second runner.",
    "status": "preparing-native-fixture",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final355 checkpoint and approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["stage"] = "batch-059-native-fixture-preparation"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Preserved full live progress; recorded execution356 preparation scope.")
