"""Return exact child output, retaining separate guarded-runner logs and immutable receipts."""
import json
import os
import subprocess
import sys
import uuid

from b131_review_v3_common import (
    RECORDS, REPO, RUNNER, TOOLS, frozen, load_module, require, sha, start_guard, write_frozen)


def python(*args):
    frozen(RUNNER["path"], RUNNER["sha256"])
    cleanup = load_module("b131_lifecycle_cleanup", RUNNER["path"])
    arguments = list(map(str, args))
    if arguments and str(TOOLS) in arguments[0]:
        arguments.insert(0, str(TOOLS / "run_b127_tool.py"))
    output = RECORDS / ("preparation-v3-lifecycle-" + uuid.uuid4().hex)
    child_command = [sys.executable, "-B", *arguments]
    command = [sys.executable, "-B", RUNNER["path"], str(output), *child_command]
    guard, _ = start_guard("B131 lifecycle immediate child")
    process = None
    try:
        process = subprocess.Popen(command, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
                                        "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(TOOLS)})
        while True:
            guard.check()
            try:
                runner_out, runner_err = process.communicate(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                continue
        guard.check()
        receipt_raw = (output / "receipt.json").read_bytes()
        receipt = json.loads(receipt_raw)
        raw = (output / "output.log").read_bytes()
        require(receipt["command"] == child_command and receipt["logSha256"] == sha(raw)
                and receipt["runnerSha256"] == RUNNER["sha256"]
                and not receipt["memory"]["breach"] and receipt["cleanupError"] is None
                and type(receipt["exitCode"]) is int
                and receipt["childExitCodeAfterCleanup"] == receipt["exitCode"]
                and process.returncode == (0 if receipt["exitCode"] == 0 else 1),
                "Guarded lifecycle child failed integrity/resource/cleanup checks")
        for name, data in (("child-output.log", raw), ("child-receipt.json", receipt_raw),
                           ("runner-stdout.log", runner_out), ("runner-stderr.log", runner_err)):
            write_frozen(output / "captured" / name, data)
        print("B131 lifecycle receipt: " + str(output / "captured" / "child-receipt.json"),
              file=sys.stderr, flush=True)
        return receipt["exitCode"], raw.decode("utf-8"), runner_err.decode("utf-8")
    finally:
        cleanup.stop_child(process)
        memory = guard.finish()
        require(not memory["breach"], "Lifecycle subprocess RAM breach")
