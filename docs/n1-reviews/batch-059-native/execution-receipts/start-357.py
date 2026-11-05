import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
request = control / "logs" / "5544c0cc-e42f-491e-8302-24f99edbcbe1" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
embedded = json.loads(text[text.index("{", text.index("Current execution checkpoint")):])
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == embedded["checkpoint"] == 356
assert progress["status"] == "continue" and progress["batch"] == "059"
assert "execution357StartingState" not in progress
progress["execution357StartingState"] = {
    "execution": 357,
    "batch": "059",
    "startingHead": "3fdc550f492d86a7c15955990e42b297aa13adab",
    "scope": "SAME059 frozen compiled native fixture execution, direct visual inspection, owned-helper cleanup and signed durable checkpoint only. No reviewer, publication,060 or second runner.",
    "status": "executing-frozen-native-fixture",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete final356 checkpoint and approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["stage"] = "batch-059-native-execution"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Preserved full live progress; recorded execution357 native scope.")
