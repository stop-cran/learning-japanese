import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

c = Path(__file__).parent
p = c / "progress.json"
data = json.loads(p.read_text(encoding="utf-8-sig"))
assert data["checkpoint"] == 407 and data["batch"] == "064"
root = c.parent / "learning-japanese"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "e2c49895daee2bbf0019388c0333e3d0e245fd4a"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
request = c / "logs" / "eb6bcdec-e815-4835-920e-a90bd299cdf0" / "request.txt"
raw = request.read_bytes()
data["execution408StartingState"] = {
    "execution": 408,
    "batch": "064",
    "startingHead": head,
    "status": "preparing-original-session-visual-confirmations",
    "scope": "SAME064 two strictly serial original-session dependent native visual confirmations, audit, reconciliation and normally signed local evidence checkpoint only. No native/Android rerun, runtime publication,065 or second runner.",
    "authorization": {
        "requestSha256": hashlib.sha256(raw).hexdigest(),
        "characters": len(raw.decode("utf-8-sig")),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request acquired into memory and embedded checkpoint parsed; operative contract, final407 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    },
    "worktrees": "Dedicated content clean signedG e2c49895; dedicated Android clean. Original406 native and accepted404 Android retained, no rerun. No canonical checkout accessed.",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution408 scope persisted; all live history retained.")
