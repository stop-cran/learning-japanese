import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
REPO = ROOT / "b129-worktree"
HERE = Path(__file__).resolve().parent
PACKET = REPO / "docs" / "n1-sources" / "batch-129"
BASE = "20fda42f7b456889ae4ef82650dde227a139917c"
CHARS = list("茉絹虹")
GUARD = ROOT / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py"
GUARD_SHA = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"
ACTIVE = None


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(data, bytes):
        data = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(data)


def start_guard():
    global ACTIVE
    assert os.environ["N1_REPO"] == str(REPO)
    assert sha(GUARD.read_bytes()) == GUARD_SHA
    spec = importlib.util.spec_from_file_location("b129_ramguard", GUARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.available_ram() > 2 * 1024**3, "Admission requires >2 GiB free"
    ACTIVE = module.RamGuard()
    ACTIVE.start()
    return ACTIVE


def bounded_wait(process, seconds):
    deadline = time.monotonic() + seconds
    while process.poll() is None:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise subprocess.TimeoutExpired(process.args, seconds)
        try:
            process.wait(timeout=min(0.1, remaining))
        except subprocess.TimeoutExpired:
            pass
    return process.returncode


def stop_child(process):
    if process is not None and process.poll() is None:
        process.terminate()
        try:
            bounded_wait(process, 10)
        except subprocess.TimeoutExpired:
            process.kill()
            bounded_wait(process, 10)


def git(*args):
    process = subprocess.Popen(["git", "-c", "core.quotepath=false", *args], cwd=REPO,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        while True:
            try:
                out, err = process.communicate(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                if ACTIVE:
                    ACTIVE.check()
        if process.returncode:
            raise RuntimeError(err.decode("utf-8", "replace"))
        return out
    finally:
        stop_child(process)


def normalized(path):
    return path.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
