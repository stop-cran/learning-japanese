import copy
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
request = c / "logs" / "6b792418-defd-4245-8413-48711d2e38d4" / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
embedded = json.loads(text.split(
    "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
p = json.loads((c / "progress.json").read_text(encoding="utf-8-sig"))
assert embedded["checkpoint"] == p["checkpoint"] == 368 and p["batch"] == "060"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip()
assert head == "8afd309e239befc132fe476a9dde53ea21f345a1"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=r).strip()
backup = c / "execution-369-starting-progress.json"
assert not backup.exists()
backup.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
start = {
    "execution": 369, "batch": "060", "startingHead": head,
    "scope": "SAME060 latest-main integration, combined acceptance and bounded owner-testing publication; no061, accepted Android/native/review rerun or second runner absent a new concern.",
    "status": "starting-combined-main-acceptance",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(text), "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired and complete embedded checkpoint parsed; operative contract, complete final368 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
}
p["execution369StartingState"] = start
p["activeExecution"] = copy.deepcopy(start)
tmp = c / "progress.json.tmp"
assert not tmp.exists()
tmp.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
tmp.replace(c / "progress.json")
print(json.dumps(start, indent=2))
