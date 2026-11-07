import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
SESSION = "01755ff6-fe55-417b-a9a1-0df278807936"
L = C / "logs" / SESSION
HEAD = "be6569bb5fae6c3ffa70a1c97514d27ce27ef8dc"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def start():
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["stage"], state["batch"]) == (
        671, "continue", "native-prepared-compiled-not-executed", "093")
    for root, head in [(R, HEAD), (A, APP)]:
        assert git(root, "rev-parse", "HEAD") == head
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain", "--untracked-files=all")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", SESSION)
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 671
    before = L / "progress-before-672.json"
    assert not before.exists()
    save(before, state)
    starting = {
        "execution": 672, "batch": "093", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "scope": "SAME093 compiled native fixture execution and actual PNG inspection; no publication, new batch or reviewer in this gate.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint parsed; operative contract, complete issue and final671 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry and launcher command verified; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved workspace inputs/committed source packets and control helpers only; no optional historical session helper access.",
        "actualNewPermissionDenials": [],
    }
    state["execution672StartingState"] = starting
    state["stage"] = "batch-093-native-execution-in-progress"
    state["nextAction"] = starting["scope"]
    temp = C / "progress.672.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")

    source = C / "run-663-native.ps1"
    wrapper = source.read_text(encoding="utf-8-sig")
    replacements = [
        ("ebddfa2a-d55d-4245-a060-b0008ff34f6a", SESSION),
        ("e29406823d0dab6be1bc3ff78eea0d0af711b680", HEAD),
        ("execution-662.json", "execution-671.json"),
        ("$checkpoint.checkpoint -ne 662", "$checkpoint.checkpoint -ne 671"),
        ("663", "672"),
        ("092", "093"),
    ]
    for old, new in replacements:
        assert old in wrapper, old
        wrapper = wrapper.replace(old, new)
    assert "File]::Open" not in wrapper and "runner.lock" not in wrapper
    target = C / "run-672-native.ps1"
    assert not target.exists()
    target.write_text(wrapper, encoding="utf-8")
    save(L / "native-wrapper-provenance.json", {
        "source": str(source), "sourceSha256": sha(source),
        "generated": str(target), "generatedSha256": sha(target),
        "replacements": replacements, "parentLockTouched": False,
    })
    print("Starting672 persisted with complete live history; bounded native wrapper generated.")


if __name__ == "__main__":
    start()
