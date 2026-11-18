import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
REPO = ROOT / "b128-worktree"
HERE = Path(__file__).resolve().parent
PACKET = REPO / "docs" / "n1-sources" / "batch-128"
BASE = "bd0f4b842c588e581ccb31ad946eecedb63d32b8"
GUARD = ROOT / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py"
GUARD_SHA = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"
ACTIVE_GUARD = None
CLEANUP_SECONDS = 10


def sha(data):
    return hashlib.sha256(data).hexdigest()


def wait_for_exit(process, seconds):
    deadline = time.monotonic() + seconds
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            code = process.poll()
            if code is not None:
                return code
            raise subprocess.TimeoutExpired(process.args, seconds)
        try:
            return process.wait(timeout=min(0.1, remaining))
        except subprocess.TimeoutExpired:
            continue


def stop_child(process):
    if process is not None and process.poll() is None:
        process.terminate()
        try:
            wait_for_exit(process, CLEANUP_SECONDS)
        except subprocess.TimeoutExpired:
            process.kill()
            wait_for_exit(process, CLEANUP_SECONDS)


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(data, bytes):
        data = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(data)


def git(*args, include_stderr=False):
    process = subprocess.Popen(["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        while True:
            try:
                out, err = process.communicate(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                if ACTIVE_GUARD:
                    ACTIVE_GUARD.check()
        if process.returncode:
            raise RuntimeError(f"git {args}: {err.decode('utf-8', 'replace')}")
        return out + err if include_stderr else out
    finally:
        active_error = sys.exc_info()[1]
        cleanup_error = None
        try:
            stop_child(process)
        except (OSError, subprocess.TimeoutExpired) as error:
            cleanup_error = error
        if active_error is not None or cleanup_error is not None:
            write(HERE / "git-failures" / (str(uuid.uuid4()) + ".json"), {
                "command": ["git", *args], "cwd": str(REPO), "childPid": process.pid,
                "exitCode": process.returncode, "activeError": str(active_error),
                "cleanupError": str(cleanup_error), "waitTimeoutSeconds": 0.1,
                "cleanupTimeoutSecondsPerStage": CLEANUP_SECONDS,
            })
        if cleanup_error is not None:
            if active_error is None:
                raise cleanup_error
            active_error.add_note(f"Child cleanup also failed: {cleanup_error}")


def start_guard():
    global ACTIVE_GUARD
    assert os.environ["N1_REPO"] == str(REPO)
    assert sha(GUARD.read_bytes()) == GUARD_SHA
    spec = importlib.util.spec_from_file_location("ramguard", GUARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    free = module.available_ram()
    if free <= 2 * 1024**3:
        raise MemoryError(f"Requires >2 GiB free; got {free}")
    guard = module.RamGuard()
    guard.start()
    ACTIVE_GUARD = guard
    return guard
