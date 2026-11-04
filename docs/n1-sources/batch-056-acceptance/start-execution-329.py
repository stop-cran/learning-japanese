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
assert p["checkpoint"] == 328 and p["batch"] == "056"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip()
assert head == "7f465a9dff08c9365ce6a32300280d8428fa979f"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=r)
request = c / "logs" / "8655a070-003b-4bac-8052-eb789fbcdd83" / "request.txt"
raw = request.read_bytes()
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint = json.loads(raw.decode("utf-8-sig").split(marker, 1)[1])
assert checkpoint["checkpoint"] == 328
active = {
    "execution": 329, "batch": "056", "startingHead": head,
    "startedAt": datetime.now().astimezone().isoformat(),
    "scope": "SAME056 fresh combined-main acceptance and bounded owner-testing publication if all gates pass; no057 or second runner. Preserve accepted Android/native/original review evidence without unnecessary reruns.",
    "status": "integrating-current-main",
    "requestRead": {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "lines": len(raw.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limit": "Entire request loaded and final checkpoint parsed. Operative contract, complete approved issue, final328checkpoint and current records inspected directly; historical middle acquired/parsed, not freshly semantically re-reviewed.",
    },
}
target = c / "execution-329-starting-progress.json"
assert not target.exists()
target.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
p["execution329StartingState"] = copy.deepcopy(active)
p["activeExecution"] = active
p["stage"] = "batch-056-combined-main-acceptance-in-progress"
assert all(p[k] == v for k, v in before.items() if k not in {"activeExecution", "stage"})
path.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution329 starting scope persisted; full live history preserved.")
