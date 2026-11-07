import datetime
import hashlib
import json
import pathlib
import subprocess

CONTROL = pathlib.Path(__file__).parent
ROOT = CONTROL.parent
SESSION = "6538b1ef-d7d4-465b-bd47-d66aa8a6ea9f"
LOGS = CONTROL / "logs" / SESSION
progress_path = CONTROL / "progress.json"
original = progress_path.read_bytes()
progress = json.loads(original)
assert (progress["checkpoint"], progress["batch"], progress["status"]) == (693, "095", "continue")
assert progress["stage"] == "native-prepared-compiled-not-executed"
for folder, head in [
    ("learning-japanese", "95be0577bea120a757bccd190625499b01e94a63"),
    ("kanji-cards-android", "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"),
]:
    def git(*args):
        return subprocess.check_output(["git", "--no-pager", "-C", str(ROOT / folder), *args], text=True).strip()
    assert git("rev-parse", "HEAD") == head
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
request = (LOGS / "request.txt").read_bytes()
checkpoint = json.loads(request.decode("utf-8-sig").split(
    "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
)[1])
assert checkpoint["checkpoint"] == 693
assert checkpoint["execution693CoordinatorCheckpoint"]["savedCommit"] == "95be0577bea120a757bccd190625499b01e94a63"
role = json.loads((LOGS / "preflight-694.json").read_bytes())
assert role["liveParentPid"] == 19008 and role["decodedLauncherMatches"] and not role["lockTouched"]
backup = LOGS / "progress-before-694.json"
assert not backup.exists()
backup.write_bytes(original)
progress["execution694StartingState"] = {
    "execution": 694, "batch": "095",
    "startedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "startingHead": "95be0577bea120a757bccd190625499b01e94a63",
    "androidHead": "1c1b7bf42cc91d820a93169f1088dc647ac51c0d",
    "freshOriginMain": subprocess.check_output(
        ["git", "-C", str(ROOT / "learning-japanese"), "rev-parse", "origin/main"], text=True).strip(),
    "scope": "SAME095 compiled native execution and actual PNG inspection; persist signed LOCAL evidence and yield before original-session rendered confirmations/publication/096.",
    "request": {
        "sha256": hashlib.sha256(request).hexdigest(), "bytes": len(request),
        "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request loaded and embedded checkpoint decoded. Operative contract, complete issue and final693 directly inspected; historical middle parsed, not freshly semantically re-reviewed.",
    },
    "runnerLockRole": role,
    "artifactPathPreflight": "Approved control and committed packets only; no optional historical-session helper access.",
    "actualNewPermissionDenials": [],
}
progress["stage"] = "batch-095-native-execution-in-progress"
progress["nextAction"] = progress["execution694StartingState"]["scope"]
temporary = CONTROL / "progress.694.tmp"
assert not temporary.exists()
temporary.write_text(json.dumps(progress, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
assert json.loads(temporary.read_bytes()) == progress
temporary.replace(progress_path)
saved = json.loads(progress_path.read_bytes())
assert all(saved[key] == value for key, value in json.loads(original).items()
           if key not in {"stage", "nextAction"})
print("Execution694 starting scope persisted; original history preserved.")
