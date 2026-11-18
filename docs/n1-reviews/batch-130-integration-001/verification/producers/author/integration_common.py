import json
import subprocess
import sys
import time
from pathlib import Path

SCRATCH = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-130")
sys.path.insert(0, str(SCRATCH))
import b130_common as original
from b130_common import REPO, git, sha, start_guard, stop_child, write

HERE = Path(__file__).resolve().parent
FIRST = "9151a6f6ad5bdba9b58178167fba4cabab876504"
SECOND = "153c6b833f68d99f59cbbce34b0bdc6d09a59bc7"
BASE = "f237a8d590a4cb91029bc0b8485163933f44b403"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
CONTENT = {"articles/numbers-and-counters.md", "counters/age.json"}
DELTA = CONTENT | {"manifest.json"}
assert sha((SCRATCH / "b130_common.py").read_bytes()) == "7809e589e7ac8691e9e3081f40f33eed329bce10c10c6696f03fd03486dde530"
assert sha((SCRATCH / "run_b130_gates.py").read_bytes()) == "9d9d302e713c4ac14563caaf83f71f0036e51b97fdd4817f7c2c5e81aeb6465c"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def live_target():
    remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
    assert remote == [SECOND, "refs/heads/main"], ("Incoming main advanced or unavailable", remote)
    assert git("rev-parse", "origin/main").decode().strip() == SECOND


def parents(mode):
    head = git("rev-parse", "HEAD").decode().strip()
    if mode == "author":
        assert head == FIRST
        assert git("rev-parse", "MERGE_HEAD").decode().strip() == SECOND
        assert not git("ls-files", "-u")
    else:
        assert git("rev-parse", "HEAD^@").decode().split() == [FIRST, SECOND]
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
    return head


def command(args, directory, guard, timeout=120):
    directory.mkdir()
    process = subprocess.Popen(args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    deadline, timed_out = time.monotonic() + timeout, False
    try:
        while True:
            guard.check()
            try:
                stdout, stderr = process.communicate(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                if time.monotonic() >= deadline:
                    timed_out = True
                    stop_child(process)
                    stdout, stderr = process.communicate(timeout=0.1)
                    break
    finally:
        stop_child(process)
    write(directory / "stdout.log", stdout)
    write(directory / "stderr.log", stderr)
    write(directory / "command.json", {
        "command": args, "exitCode": process.returncode, "timedOut": timed_out,
        "timeoutSeconds": timeout, "childWaitSeconds": 0.1, "cleanupTimeoutSecondsPerStage": 10,
        "stdoutSha256": sha(stdout), "stderrSha256": sha(stderr),
    })
    return process.returncode, timed_out, stdout, stderr


def tree_entries(ref):
    entries = {}
    for row in git("ls-tree", "-r", "-z", "--full-tree", ref).split(b"\0"):
        if row:
            info, path = row.split(b"\t", 1)
            mode, kind, oid = info.decode().split()
            entries[path.decode("utf-8")] = {"mode": mode, "kind": kind, "blob": oid}
    return entries
