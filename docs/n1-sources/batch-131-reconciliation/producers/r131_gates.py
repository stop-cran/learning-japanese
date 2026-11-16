import json
import sys
from pathlib import Path
from r131_common import *
from run_b131_gates import CHECKS, run_gate


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: r131_gates.py author|committed NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert out.parent == HERE and not out.exists()
    guard = start_guard()
    try:
        head = git("rev-parse", "HEAD").decode().strip()
        if mode == "author":
            assert head == PARENT
        else:
            assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
            committed_manifest = sha(git("show", "HEAD:manifest.json"))
    finally:
        memory = guard.finish()
    out.mkdir()
    write(out / "admission.json", {"head": head, "parent": PARENT, "base": BASE, "mode": mode, "memory": memory})
    expected = None
    for name in CHECKS:
        expected = run_gate(name, out, expected)
    guard = start_guard()
    try:
        if mode == "committed":
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
            assert expected == committed_manifest
    finally:
        memory = guard.finish()
    summary = {"batch": 131, "revision": "reconciliation-001", "mode": mode, "status": "PASS",
               "parent": PARENT, "publishedBase": BASE, "startingHead": head,
               "checks": list(CHECKS), "serial": True, "manifestSha256": expected,
               "runnerSha256": sha(Path(__file__).read_bytes()), "guardSha256": GUARD_SHA,
               "implementation": {"path": str(SCRIPTS / "run_b131_gates.py"),
                                  "sha256": sha((SCRIPTS / "run_b131_gates.py").read_bytes()),
                                  "disclosure": "Unchanged original ten commands and bounded run_gate implementation. Its per-gate implementation/common/candidate hashes remain correctly named historical dependencies. Only outer admission binds the revision parent; lint/linkplan retain published-base scope."},
               "waitTimeoutSeconds": 0.1, "cleanupTimeoutSecondsPerStage": 10, "finalMemory": memory,
               "logs": {n: {"logSha256": sha((out / (n + ".log")).read_bytes()),
                           "receiptSha256": sha((out / (n + ".json")).read_bytes())} for n in CHECKS},
               "limits": "Host/static bounded checks, not independent linguistic confirmation, arbitrary/custom/multiple-borrow/native/device/visual or publication acceptance."}
    write(out / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
