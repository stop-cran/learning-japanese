import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
path = control / "progress.json"
progress = json.loads(path.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == 345 and progress["batch"] == "058"
assert progress["status"] == "continue"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert head == "00491dddddaa65467b0f7ad474689e054a00f5f4"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root)
progress["execution346StartingState"] = {
    "execution": 346, "batch": "058", "startingHead": head,
    "scope": "SAME058 exact-full-archive native fixture preparation, serial compilation and signed local evidence checkpoint only. No native launch, reviewer, publication,059 or second runner.",
    "authorization": "Entire1191181-character14891-line request acquired into memory and complete embedded checkpoint parsed; operative authorization, complete final345 checkpoint and complete approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
    "status": "preparing-current-batch-native-fixture",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
progress["stage"] = "batch-058-native-preparation-in-progress"
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution346 starting scope persisted; all live historical keys preserved.")
