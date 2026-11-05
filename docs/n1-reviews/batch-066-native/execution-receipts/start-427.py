import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

control = Path(r"C:\Users\stop-\n1-kanji-workspace\control")
path = control / "progress.json"
raw = path.read_bytes()
state = json.loads(raw)
assert state["checkpoint"] == 426 and state["batch"] == "066"
assert state["status"] == "continue"
backup = control / "execution-427-before-progress.json"
assert not backup.exists()
backup.write_bytes(raw)
request = control / r"logs\bda066bb-9e8e-4e26-839f-5944b7c15ad4\request.txt"
text = request.read_text(encoding="utf-8")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint = json.loads(text.split(marker, 1)[1])
assert checkpoint["checkpoint"] == 426
record = {
    "execution": 427,
    "batch": "066",
    "startingHead": "428a9ecf96af91c0022f9f88892b2f8265d4cdf1",
    "scope": "SAME066 frozen compiled native execution, direct coordinator image inspection and signed local evidence checkpoint only. No reviewers, publication,067 or second runner.",
    "status": "native-execution-starting",
    "authorization": {
        "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "characters": len(text),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, final426 and approved issue inspected directly. Historical middle acquired/parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
state["execution427StartingState"] = record
state["stage"] = "batch-066-native-execution-starting"
temporary = control / "execution-427-progress.tmp"
temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temporary.replace(path)
(control / "execution-427-start.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
assert all(json.loads(raw)[key] == state[key] for key in json.loads(raw) if key != "stage")
print("Starting scope persisted; complete live history preserved.")
