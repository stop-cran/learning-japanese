import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

control = Path(r"C:\Users\stop-\n1-kanji-workspace\control")
path = control / "progress.json"
raw = path.read_bytes()
state = json.loads(raw)
assert state["checkpoint"] == 418 and state["batch"] == "065"
assert state["status"] == "continue"
backup = control / "execution-419-before-progress.json"
assert not backup.exists()
backup.write_bytes(raw)
request = control / r"logs\119de561-671b-4186-97f8-d7959b1239a9\request.txt"
text = request.read_text(encoding="utf-8")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint = json.loads(text.split(marker, 1)[1])
assert checkpoint["checkpoint"] == 418
record = {
    "execution": 419,
    "batch": "065",
    "startingHead": "82a2c26c9d7541f93786ab3a7722d10ca557e98c",
    "scope": "SAME065 compiled native execution, direct coordinator visual inspection and durable signed local checkpoint only. No reviewers, publication,066 or second runner.",
    "status": "native-execution-starting",
    "authorization": {
        "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "characters": len(text),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Complete request acquired and embedded checkpoint parsed; operative contract, final418 and complete approved issue inspected directly. Historical middle acquired/parsed, not freshly semantically re-reviewed.",
    },
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
state["execution419StartingState"] = record
state["stage"] = "batch-065-native-execution-starting"
temporary = control / "execution-419-progress.tmp"
temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temporary.replace(path)
(control / "execution-419-start.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
assert all(json.loads(raw)[key] == state[key] for key in json.loads(raw) if key != "stage")
print("Starting state persisted; complete prior progress preserved.")
