import hashlib
import json
from datetime import datetime
from pathlib import Path

control = Path(__file__).parent
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == 460
assert progress["batch"] == "070" and progress["status"] == "continue"
request = control / "logs" / "db0a651d-b074-4cca-8909-4459e6628768" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint = json.loads(text.split(marker, 1)[1])
assert checkpoint["checkpoint"] == 460
state = {
    "execution": 461,
    "batch": "070",
    "startingHead": "27a65d2fa6e711d4e23f17c2c485f044d3aef848",
    "androidHead": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "scope": "SAME070 compiled exact full-archive native execution, actual PNG inspection, evidence archival and normally signed local checkpoint only. No reviewer/publication/071/second runner.",
    "status": "executing-compiled-native-gate",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed. Operative contract, complete approved issue and complete final460 checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
    },
    "freshlyFetchedOriginMain": "caf2eebf5d8274adbd68e67349f4d12fffedbb30",
}
assert "execution461StartingState" not in progress
progress["execution461StartingState"] = state
progress["stage"] = "batch-070-native-executing"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(state, ensure_ascii=False, indent=2))
