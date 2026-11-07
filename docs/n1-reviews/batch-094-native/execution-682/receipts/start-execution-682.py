import datetime
import hashlib
import json
import pathlib
import subprocess

CONTROL = pathlib.Path(__file__).parent
ROOT = CONTROL.parent
SESSION = "7fa5bfa8-7e4f-4d49-9084-40fb301b94f5"
LOGS = CONTROL / "logs" / SESSION
progress_path = CONTROL / "progress.json"
original = progress_path.read_bytes()
progress = json.loads(original)
assert (progress["checkpoint"], progress["batch"], progress["status"]) == (681, "094", "continue")
assert progress["stage"] == "native-prepared-compiled-not-executed"
for folder, head in [
    ("learning-japanese", "bf3e09d6e55f64125edd3b08dd4e37df0ffdb5d4"),
    ("kanji-cards-android", "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"),
]:
    def git(*args):
        return subprocess.check_output(["git", "-C", str(ROOT / folder), *args], text=True).strip()
    assert git("rev-parse", "HEAD") == head
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
request = (LOGS / "request.txt").read_bytes()
json.loads(request.decode("utf-8-sig").split(
    "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
)[1])
backup = LOGS / "progress-before-682.json"
assert not backup.exists()
backup.write_bytes(original)
progress["execution682StartingState"] = {
    "execution": 682,
    "batch": "094",
    "startedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "startingHead": "bf3e09d6e55f64125edd3b08dd4e37df0ffdb5d4",
    "androidHead": "1c1b7bf42cc91d820a93169f1088dc647ac51c0d",
    "freshOriginMain": "48765e20846e1d6769c6ddc35146f6ce58deab57",
    "scope": "SAME094 compiled native execution and actual PNG inspection; persist signed LOCAL evidence and yield before original-session visual confirmations/publication/095.",
    "request": {
        "sha256": hashlib.sha256(request).hexdigest(),
        "bytes": len(request),
        "lines": len(request.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request loaded and embedded checkpoint decoded. Operative contract, complete issue and final681 directly inspected; historical middle parsed, not freshly semantically re-reviewed.",
    },
    "runnerLockRole": "Live parent19008 and current-session ancestry verified; no child acquire/delete/unlock.",
    "artifactPathPreflight": "Approved control and committed packets only; no optional historical-session helper access.",
    "actualNewPermissionDenials": [],
}
progress["stage"] = "batch-094-native-execution-in-progress"
progress["nextAction"] = "SAME094 execute frozen compiled native fixture with fresh parent/signed-head/clean/device ownership guards; inspect actual PNGs and persist results. No publication or095."
progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
saved = json.loads(progress_path.read_bytes())
assert all(saved[key] == value for key, value in json.loads(original).items()
           if key not in {"stage", "nextAction"})
print("Execution682 starting scope persisted; original history preserved.")
