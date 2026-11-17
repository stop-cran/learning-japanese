"""Bounded captured subprocesses for B127's unchanged review lifecycle."""
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

from common import TOOLS, frozen, load_module, sha, start_guard
from verify_b127_sources import RUNNER, RUNNER_SHA


def python(*args):
    frozen(RUNNER, RUNNER_SHA)
    cleanup = load_module("b127_lifecycle_cleanup", RUNNER)
    arguments = list(map(str, args))
    if arguments and Path(arguments[0]) == TOOLS / "prepare-chain.py":
        arguments.insert(0, str(TOOLS / "run_b127_tool.py"))
    command = [sys.executable, "-B", *arguments]
    guard, _ = start_guard("B127 review lifecycle subprocess")
    process = None
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   env={**os.environ, "PYTHONIOENCODING": "utf-8",
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
        active_error = sys.exc_info()[1]
        cleanup_error = None
        try:
            cleanup.stop_child(process)
        except (OSError, subprocess.TimeoutExpired) as error:
            cleanup_error = error
        memory = guard.finish()
        print("B127 lifecycle child: " + json.dumps({
            "started": started, "finished": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "command": command, "pid": process.pid if process is not None else None,
            "exitCode": process.returncode if process is not None else None,
            "waitTimeoutSeconds": 0.1, "cleanupTimeoutSecondsPerStage": 10,
            "cleanupScope": "Immediate child PID only.",
            "cleanupError": str(cleanup_error) if cleanup_error is not None else None,
            "memory": memory, "helperSha256": sha(Path(__file__).read_bytes()),
            "cleanupHelperSha256": RUNNER_SHA,
        }), file=sys.stderr, flush=True)
        if cleanup_error is not None:
            if active_error is None:
                raise cleanup_error
            active_error.add_note(f"Child cleanup also failed: {cleanup_error}")
        if memory["breach"] and active_error is None:
            raise MemoryError(f"Lifecycle child breached RAM guard: {memory['breach']}")
