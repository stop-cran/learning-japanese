import datetime
import hashlib
import json
from pathlib import Path

control = Path(__file__).parent
session = "d0490dbe-b3a1-40f6-a8a1-7cfc0f16a6cf"
path = control / "progress.json"
original = json.loads(path.read_text(encoding="utf-8-sig"))
assert original["checkpoint"] == 713 and original["batch"] == "097"
assert original["status"] == "continue"
request = control / "logs" / session / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
state = {
    "execution": 714, "batch": "097",
    "startedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "startingHead": "1069a0463dcb497682f8336064f6cb3897b3388b",
    "androidHead": "1c1b7bf42cc91d820a93169f1088dc647ac51c0d",
    "scope": "SAME097 execute frozen native acceptance; preserve raw results and bounded visual evidence; no publication/098.",
    "request": {"sha256": hashlib.sha256(raw).hexdigest(),
                "characters": len(text), "lines": len(text.splitlines()),
                "completeFileLoadedAndCheckpointParsed": True,
                "limits": "Entire request loaded/decoded; operative contract, complete issue and terminal713 inspected. Historical middle parsed, not freshly semantically re-reviewed."},
    "runnerLockRole": json.loads((control / "logs" / session / "preflight-714.json").read_text(encoding="utf-8-sig")),
    "artifactPathPreflight": "Approved workspace/committed evidence only; no optional historical session helper accessed.",
}
original["execution714StartingState"] = state
original["stage"] = "batch-097-native-execution-in-progress"
path.write_text(json.dumps(original, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution714 starting state persisted, full history preserved.")
