import copy
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
path = c / "progress.json"
p = json.loads(path.read_text(encoding="utf-8-sig"))
before = copy.deepcopy(p)
assert p["checkpoint"] == 338 and p["batch"] == "057"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip()
assert head == "4aa811b55df37e07d93ec3aaf0d97a0f386881c7"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=r)
request = c / "logs" / "5f6aaf99-ed47-4d90-ab85-271326e3ff9e" / "request.txt"
raw = request.read_bytes()
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint = json.loads(raw.decode("utf-8-sig").split(marker, 1)[1])
assert checkpoint["checkpoint"] == 338
active = {
    "execution": 339, "batch": "057", "startingHead": head,
    "startedAt": datetime.now().astimezone().isoformat(),
    "scope": "SAME057 latest-main integration, combined acceptance and bounded owner-testing publication if all gates pass; no058 or second runner. Retain accepted334Android/336native/original reviews and explicit process deviations without unnecessary reruns.",
    "status": "integrating-current-main",
    "requestRead": {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "lines": len(raw.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limit": "Entire request acquired and checkpoint parsed. Operative contract, approved issue and complete final338checkpoint inspected directly; historical middle acquired/parsed, not freshly semantically re-reviewed.",
    },
}
target = c / "execution-339-starting-progress.json"
assert not target.exists()
target.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
p["execution339StartingState"] = copy.deepcopy(active)
p["activeExecution"] = active
p["stage"] = "batch-057-combined-main-acceptance-in-progress"
assert all(p[k] == v for k, v in before.items() if k not in {"activeExecution", "stage"})
path.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution339 starting scope persisted; full live history preserved.")
