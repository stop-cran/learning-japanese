import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
request = c / "logs" / "383d3a78-d7df-4c09-a9da-6524cd82c792" / "request.txt"
text = request.read_text(encoding="utf-8-sig")
checkpoint = json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
assert checkpoint["checkpoint"] == 327
p = json.loads((c / "progress.json").read_text(encoding="utf-8-sig"))
assert p["checkpoint"] == 327 and p["batch"] == "056"
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip() == "6283ee5e6b90598cf92516ee6abf7cfa91d08e68"
for command, name in ((["copilot", "--help"], "copilot-help-execution-328.txt"),
                      (["copilot", "help", "config"], "copilot-config-execution-328.txt")):
    result = subprocess.run(command, cwd=r, text=True, encoding="utf-8", capture_output=True, check=True, shell=True)
    (c / name).write_text(result.stdout, encoding="utf-8")
catalog = (c / "copilot-config-execution-328.txt").read_text(encoding="utf-8")
assert all(model in catalog for model in ("claude-opus-5.5", "gpt-6.1-sol"))
p["execution328StartingState"] = {
    "execution": 328, "batch": "056", "startingHead": "6283ee5e6b90598cf92516ee6abf7cfa91d08e68",
    "scope": "SAME056 original-session serial dependent native visual confirmations and signed local evidence checkpoint only; no native/Android rerun, publication,057 or second runner.",
    "authorization": "Entire request acquired into memory and entire embedded final checkpoint parsed; operative contract, complete approved issue and final327 checkpoint read directly. Historical middle records acquired/parsed, not freshly semantically re-reviewed.",
    "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
    "status": "starting-original-serial-visual-confirmations",
    "recordedAt": datetime.now().astimezone().isoformat(),
}
temporary = c / "progress.execution328.tmp"
temporary.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temporary.replace(c / "progress.json")
print("Starting scope persisted with full live history; current help/catalog captured.")
