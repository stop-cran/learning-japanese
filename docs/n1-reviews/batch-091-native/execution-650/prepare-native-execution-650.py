import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
L = C / "logs" / "ec5e6e3f-0cb4-47c8-850d-3b276eba0562"
P = C / "progress.json"
before = json.loads(P.read_text(encoding="utf-8-sig"))
assert before["checkpoint"] == 649 and before["batch"] == "091"
assert before["status"] == "continue"
assert before["stage"] == "native-prepared-compiled-not-executed"
backup = L / "progress-before-650.json"
assert not backup.exists()
backup.write_bytes(P.read_bytes())
request = (L / "request.txt").read_bytes()
decoded = request.decode("utf-8-sig")
json.loads(decoded.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
state = json.loads(json.dumps(before))
state["execution650StartingState"] = {
    "execution": 650,
    "batch": "091",
    "startedAt": datetime.now(timezone.utc).isoformat(),
    "startingHead": "3a31f5eecbe403b81cb0c0bce9a467025feaef89",
    "androidHead": "1c1b7bf42cc91d820a93169f1088dc647ac51c0d",
    "freshOriginMain": subprocess.check_output(
        ["git", "-C", str(R), "rev-parse", "origin/main"], text=True
    ).strip(),
    "scope": "SAME091 compiled native execution and actual PNG inspection; local signed evidence only. No reviewer/publication/092.",
    "request": {
        "sha256": hashlib.sha256(request).hexdigest(),
        "bytes": len(request),
        "characters": len(decoded),
        "lines": len(decoded.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request loaded/decoded; operative contract, complete issue and final649 inspected. Historical middle parsed, not freshly semantically re-reviewed.",
    },
    "runnerLockRole": "Live parent19008 ancestry/session verified. No child lock access.",
    "artifactPathPreflight": "Approved control/committed evidence only; optional historical session recipes not accessed.",
}
state["stage"] = "batch-091-native-execution-in-progress"
state["nextAction"] = "SAME091 execute frozen compiled native cases, inspect actual PNGs, preserve results and yield at a signed local evidence checkpoint; all original gates retained."
temp = C / "progress.650.tmp"
assert not temp.exists()
temp.write_text(json.dumps(state, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
assert json.loads(temp.read_text()) == state
temp.replace(P)

source = C / "run-641-native-retry1.ps1"
wrapper = source.read_text(encoding="utf-8-sig")
replacements = {
    "6eb76a67-baeb-4c82-9712-085c7f41f102": "ec5e6e3f-0cb4-47c8-850d-3b276eba0562",
    "batch-090-native-attempt-641-retry1": "batch-091-native-attempt-650",
    "execution-640.json": "execution-649.json",
    "execution=641; batch='090'": "execution=650; batch='091'",
    "540d36f717189b2ac7b34bebeba1414ff3ff53c6": "3a31f5eecbe403b81cb0c0bce9a467025feaef89",
    "$checkpoint.checkpoint -ne 640": "$checkpoint.checkpoint -ne 649",
    "$checkpoint.batch -ne '090'": "$checkpoint.batch -ne '091'",
    "batch-090-native-execution-in-progress": "batch-091-native-execution-in-progress",
    "N1Batch090": "N1Batch091",
    "^n1-090-": "^n1-091-",
}
for old, new in replacements.items():
    assert old in wrapper, old
    wrapper = wrapper.replace(old, new)
target = C / "run-650-native.ps1"
assert not target.exists()
target.write_text(wrapper, encoding="utf-8")
assert "File.Open" not in wrapper and "runner.lock" not in wrapper
print("Starting state persisted; native wrapper generated from approved corrected control641 recipe.")
