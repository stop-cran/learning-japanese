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
assert p["checkpoint"] == 314 and p["batch"] == "055"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip()
assert head == "9361f6129024a65699081cd1a62b589929e3fd60"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=r)
request = c / "logs" / "7d3804f6-ba10-493d-9969-b6ed6c5bbc15" / "request.txt"
raw = request.read_bytes()
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint = json.loads(raw.decode("utf-8-sig").split(marker, 1)[1])
assert checkpoint["checkpoint"] == 314
active = {
    "execution": 315, "batch": "055", "startingHead": head,
    "startedAt": datetime.now().astimezone().isoformat(),
    "scope": "SAME055 combined-current-main acceptance and bounded owner-testing publication; stop before056. No accepted Android/native/reviewer reruns absent a new concern; no second runner.",
    "status": "integrating-current-main",
    "requestRead": {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "lines": len(raw.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limit": "Complete request loaded and final checkpoint parsed. Operative contract, approved issue, final314checkpoint/current records inspected directly; no semantic re-review of every historical execution claimed.",
    },
}
assert not (c / "execution-315-starting-progress.json").exists()
(c / "execution-315-starting-progress.json").write_text(
    json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
p["execution315StartingState"] = copy.deepcopy(active)
p["activeExecution"] = active
p["stage"] = "batch-055-combined-main-acceptance-in-progress"
assert all(p[k] == v for k, v in before.items() if k not in {"activeExecution", "stage"})
path.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution315 scope persisted; complete live history preserved.")
