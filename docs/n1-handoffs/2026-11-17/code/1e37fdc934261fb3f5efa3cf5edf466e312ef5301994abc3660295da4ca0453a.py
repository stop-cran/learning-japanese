"""Bounded subprocess execution with raw guarded receipts for B131 lifecycle checks."""
import os
import subprocess
import sys
import uuid

from b131_neutral_common_001 import (RECORDS, REPO, RUNNER, TOOLS, frozen,
                                     load_module, require, start_guard)


def python(*args):
    frozen(RUNNER["path"], RUNNER["sha256"])
    cleanup = load_module("b131_lifecycle_cleanup", RUNNER["path"])
    arguments = list(map(str, args))
    if arguments and str(TOOLS) in arguments[0]:
        arguments.insert(0, str(TOOLS / "run_b127_tool.py"))
    output = RECORDS / ("preparation-lifecycle-" + uuid.uuid4().hex)
    command = [sys.executable, "-B", RUNNER["path"], str(output), sys.executable, "-B", *arguments]
    guard, _ = start_guard("B131 lifecycle immediate child")
    process = None
    try:
        process = subprocess.Popen(command, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
                                        "PYTHONDONTWRITEBYTECODE": "1"})
        while True:
            guard.check()
            try:
                out, err = process.communicate(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                continue
        guard.check()
        return process.returncode, out.decode("utf-8"), err.decode("utf-8")
    finally:
        cleanup.stop_child(process)
        memory = guard.finish()
        require(not memory["breach"], "Lifecycle subprocess RAM breach")
