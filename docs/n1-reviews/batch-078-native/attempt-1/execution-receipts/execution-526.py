import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
CONTENT = CONTROL.parent / "learning-japanese"
LOGS = CONTROL / "logs" / "e2498e2d-1fe6-4764-a8cf-a46f0b83535d"
PROGRESS = CONTROL / "progress.json"


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    progress = json.loads(PROGRESS.read_text(encoding="utf-8-sig"))
    assert progress["checkpoint"] == 525 and progress["batch"] == "078"
    backup = LOGS / "progress-before-526.json"
    assert not backup.exists()
    backup.write_bytes(PROGRESS.read_bytes())
    request = (LOGS / "request.txt").read_bytes()
    state = {
        "execution": 526,
        "batch": "078",
        "startingHead": "02c617480a1537feef611c12d51865ace7406caf",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME078 compiled native execution and actual PNG inspection only; no reviewer, publication,079 or second runner.",
        "authorization": {
            "requestSha256": hashlib.sha256(request).hexdigest(),
            "bytes": len(request),
            "lines": len(request.decode("utf-8-sig").splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, final525, complete approved issue and durable path preflight directly inspected. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [],
        "status": "native-execution-preparing",
    }
    progress["execution526StartingState"] = state
    save(PROGRESS, progress)
    assert all(progress[key] == value for key, value in json.loads(backup.read_text(encoding="utf-8-sig")).items())
    print("Starting scope persisted; every existing historical value preserved.")
