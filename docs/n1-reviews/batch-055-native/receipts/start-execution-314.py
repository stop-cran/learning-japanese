import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
path = c / "progress.json"
p = json.loads(path.read_text(encoding="utf-8-sig"))
assert p["checkpoint"] == 313 and p["status"] == "continue" and p["batch"] == "055"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip()
assert head == "c4fc279c44541b3d99ddaa56ca5d1ce0452e9026"
request = c / "logs" / "a4f8768f-81ab-4791-9322-24c869896cad" / "request.txt"
text = request.read_text(encoding="utf-8-sig")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint = json.loads(text.split(marker, 1)[1])
assert checkpoint["checkpoint"] == 313
p["execution314StartingState"] = {
    "execution": 314,
    "batch": "055",
    "startingHead": head,
    "recordedAt": datetime.now().astimezone().isoformat(),
    "scope": "SAME055 bounded ORIGINAL serial native visual confirmations and signed evidence checkpoint only; no native/Android rerun, publication,056 or second runner.",
    "status": "starting-original-session-visual-confirmations",
    "requestRead": {
        "sha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limit": "Full remaining-history console export exceeded tool output limit. Operative contract, complete final checkpoint/current313record and approved issue inspected directly; no claim of semantic re-review of every historical record.",
    },
    "invariants": "Frozen teaching unchanged; clean dedicated content and Android. Preserve accepted310Android3+1,312native2case0, original initial reports and full live progress history. No review model guessed: actual current help/config catalog captured.",
}
temporary = path.with_suffix(".execution314.tmp")
temporary.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temporary.replace(path)
print("Execution314 starting scope persisted; full live history preserved.")
