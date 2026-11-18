import json
import sys
from pathlib import Path
import run_b127_gates as original
from b127_common import CLEANUP_SECONDS, GUARD_SHA, HERE, REPO, git, sha, start_guard, write
from reconcile_sources_b127 import PARENT

original.CHECKS = {
    **original.CHECKS,
    "lint": [original.LEAN / "n1_batch_tool.py", "lint", "--base", PARENT, "--no-jmdict", "倉"],
    "linkplan": [original.LEAN / "n1_linkplan.py", "verify", PARENT, "倉"],
}


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: reconcile_gates_b127.py author|committed NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert out.parent == HERE and not out.exists()
    out.mkdir()
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
        write(out / "admission.json", {"head": locals().get("head"), "mode": mode, "parent": PARENT, "memory": guard.finish()})
    expected = None
    for name in original.CHECKS:
        expected = original.run_gate(name, out, expected)
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == head
        if mode == "committed":
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
            assert expected == committed_manifest
    finally:
        final_memory = guard.finish()
    summary = {
        "status": "PASS", "batch": "127", "revision": "reconciliation-001", "mode": mode,
        "parent": PARENT, "startingHead": head,
        "publishedBase": "dd45f6fb7cd3ce579422e2333860aa6d245af898",
        "checks": list(original.CHECKS), "commands": {name: list(map(str, args)) for name, args in original.CHECKS.items()},
        "manifestSha256": expected, "contentVersion": json.loads((REPO / "manifest.json").read_bytes())["contentVersion"],
        "runnerSha256": sha(Path(__file__).read_bytes()),
        "reusedSerialRunGateSha256": sha(Path(original.__file__).read_bytes()),
        "commonHelperSha256": sha((HERE / "b127_common.py").read_bytes()),
        "guardSha256": GUARD_SHA, "serial": True, "waitTimeoutSeconds": 0.1,
        "cleanupTimeoutSecondsPerStage": CLEANUP_SECONDS, "finalMemory": final_memory,
        "logs": {name: {"logSha256": sha((out / (name + ".log")).read_bytes()), "receiptSha256": sha((out / (name + ".json")).read_bytes())} for name in original.CHECKS},
        "limits": "Host/static checks, not independent linguistic, custom/multiple-borrow, Kotlin/native/device, publication or whole-set acceptance.",
    }
    write(out / "summary.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k not in ("commands", "logs", "finalMemory")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
