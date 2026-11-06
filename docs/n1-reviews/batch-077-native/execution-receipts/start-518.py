import copy
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

control = Path(__file__).resolve().parent
content = control.parent / "learning-japanese"
request = control / "logs" / "851a0519-ca36-4275-8bf0-8653cd423e5e" / "request.txt"
text = request.read_text(encoding="utf-8-sig")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint, end = json.JSONDecoder().raw_decode(text.split(marker, 1)[1].lstrip())
assert not text.split(marker, 1)[1].lstrip()[end:].strip()
path = control / "progress.json"
original = json.loads(path.read_text(encoding="utf-8-sig"))
assert original["checkpoint"] == 517 and original["batch"] == "077"
backup = control / "logs" / "851a0519-ca36-4275-8bf0-8653cd423e5e" / "progress-before-518.json"
assert not backup.exists()
backup.write_bytes(path.read_bytes())
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=content, text=True).strip()
assert head == "594710e8e902b9450001bb0de79e44c1384419d4"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=content, text=True).strip()
progress = copy.deepcopy(original)
progress["execution518StartingState"] = {
    "execution": 518,
    "batch": "077",
    "startingHead": head,
    "scope": "SAME077 compiled native execution and coordinator PNG inspection only; no reviewer, teaching edit, publication,078 or second runner.",
    "status": "native-execution-preparing",
    "recordedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "authorization": {
        "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
        "characters": len(text),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request loaded and checkpoint parsed; operative contract, final517 and complete approved issue inspected directly. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
    },
    "optionalHistoricalHelpersAccessed": False,
    "freshOriginMain": subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=content, text=True).strip(),
}
progress["stage"] = "batch-077-native-execution-preparing"
progress["status"] = "continue"
for key, value in original.items():
    if key not in {"stage", "status"}:
        assert progress[key] == value, key
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Execution518 starting scope persisted; complete live history preserved.")
