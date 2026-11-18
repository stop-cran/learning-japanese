import json
import sys
from pathlib import Path
from b130_common import BASE, GUARD_SHA, HERE, REPO, git, sha, start_guard, write
from run_b130_gates import CHECKS, run_gate

PARENT = "ce1b5c895fac90852143f322a115c2de4e768e20"


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: run_b130_reconciliation_gates.py author|committed NEW_DIRECTORY")
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
    write(out / "admission.json", {"head": head, "mode": mode, "parent": PARENT, "memory": memory})
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
    summary = {
        "batch": 130, "revision": "reconciliation-001", "mode": mode, "status": "PASS",
        "parent": PARENT, "publishedBase": BASE, "startingHead": head,
        "checks": list(CHECKS), "serial": True, "manifestSha256": expected,
        "runnerSha256": sha(Path(__file__).read_bytes()),
        "gateImplementationSha256": sha((HERE / "run_b130_gates.py").read_bytes()),
        "implementationDisclosure": "Reuses the original ten gate commands and bounded run_gate implementation, including its correctly named implementation runner hash. Only outer admission/parent checks change. Lint/linkplan retain the full published-base scope, not the revision parent.",
        "commonHelperSha256": sha((HERE / "b130_common.py").read_bytes()),
        "guardSha256": GUARD_SHA, "waitTimeoutSeconds": 0.1,
        "cleanupTimeoutSecondsPerStage": 10, "finalMemory": memory,
        "logs": {n: {"logSha256": sha((out / (n + ".log")).read_bytes()),
                     "receiptSha256": sha((out / (n + ".json")).read_bytes())} for n in CHECKS},
        "limits": "Host/static bounded checks, not independent linguistic confirmation, arbitrary/custom/multiple-borrow/native/device/visual or publication acceptance.",
    }
    write(out / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
