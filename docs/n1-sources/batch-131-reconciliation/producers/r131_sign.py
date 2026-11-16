import json
import os
import subprocess
import sys
import time
from pathlib import Path
from r131_common import *

guard = start_guard()
process = None
timed_out = False
try:
    stage = json.loads((HERE / "staging-001.json").read_text(encoding="utf8"))
    assert stage["status"] == "PASS" and stage["parent"] == PARENT
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    assert not (HERE / "signing-001.log").exists()
    for path, digest in stage["stagedRawHashes"].items():
        assert sha(git("show", ":" + path)) == digest, path
    assert not git("diff", "--name-only")
    assert not git("ls-files", "--others", "--exclude-standard")
    command = ["git", "commit", "-SD4C9A275A218AF747B787AFA9D94B9D311BD26A7",
               "-m", "Reconcile B131 direct quiz precautions",
               "-m", "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"]
    with (HERE / "signing-001.log").open("xb") as log:
        process = subprocess.Popen(command, cwd=REPO, stdout=log, stderr=subprocess.STDOUT,
                                   env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
        deadline = time.monotonic() + 30
        while True:
            try:
                code = process.wait(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                guard.check()
                if time.monotonic() >= deadline:
                    timed_out = True
                    stop_child(process)
                    code = process.returncode
                    break
    print((HERE / "signing-001.log").read_text(encoding="utf8"), end="")
    print(json.dumps({"timedOut": timed_out, "exitCode": code, "head": git("rev-parse", "HEAD").decode().strip()}))
    if timed_out or code != 0:
        raise SystemExit("Single signing attempt failed/stalled; preserve staged work and yield without retry.")
finally:
    stop_child(process)
    write(HERE / "signing-001.json", {"parent": PARENT, "timedOut": timed_out, "singleAttempt": True,
                                     "exitCode": process.returncode if process else None,
                                     "childPid": process.pid if process else None,
                                     "waitTimeoutSeconds": 0.1, "stallDeadlineSeconds": 30,
                                     "cleanupTimeoutSecondsPerStage": 10,
                                     "producerSha256": sha(Path(__file__).read_bytes()), "memory": guard.finish()})
