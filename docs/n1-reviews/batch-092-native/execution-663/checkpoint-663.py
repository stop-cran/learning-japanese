import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

CONTROL = pathlib.Path(__file__).resolve().parent
CONTENT = CONTROL.parent / "learning-japanese"
PROGRESS = CONTROL / "progress.json"
SESSION = "ebddfa2a-d55d-4245-a060-b0008ff34f6a"


def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(CONTENT), *args], text=True, encoding="utf-8"
    ).strip()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


if sys.argv[1:] != ["start"]:
    raise SystemExit("Expected start")
progress = json.loads(PROGRESS.read_text(encoding="utf-8-sig"))
assert progress["checkpoint"] == 662 and progress["batch"] == "092"
assert progress["stage"] == "native-prepared-compiled-not-executed"
assert git("rev-parse", "HEAD") == "e29406823d0dab6be1bc3ff78eea0d0af711b680"
assert git("status", "--porcelain") == ""
request = CONTROL / "logs" / SESSION / "request.txt"
raw = request.read_bytes()
text = raw.decode("utf-8-sig")
json.loads(text.split(
    "Current execution checkpoint (complete historical state remains at checkpointHistory paths):",
    1,
)[1])
backup = CONTROL / "logs" / SESSION / "progress-before-663.json"
assert not backup.exists()
backup.write_bytes(PROGRESS.read_bytes())
progress["execution663StartingState"] = {
    "execution": 663,
    "batch": "092",
    "startedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "startingHead": git("rev-parse", "HEAD"),
    "androidHead": "1c1b7bf42cc91d820a93169f1088dc647ac51c0d",
    "scope": "SAME092 compiled native execution and actual PNG inspection; persist signed LOCAL evidence, then yield before independent visual confirmation/publication/093.",
    "request": {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "characters": len(text),
        "lines": len(text.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final662 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
    },
    "runnerLockRole": "Verified live parent19008 ancestry/session; no child lock acquisition/delete/unlock.",
    "artifactPathPreflight": "Approved workspace inputs/committed packets and durable control helpers only; no historical session recipe access.",
    "actualNewPermissionDenials": [],
}
progress["stage"] = "batch-092-native-execution-in-progress"
progress["nextAction"] = "SAME092 execute frozen compiled native fixture with fresh ownership and unchanged signed heads/heaps/guards; inspect PNGs, persist evidence and yield before serial dependent visual confirmations/publication/093."
save(PROGRESS, progress)
print("Execution663 starting state saved; full live history preserved.")
