import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common_132 import BASE, HERE, REPO, git, sha, start_guard, write

OUTROOT = Path(__file__).resolve().parent
PARENT = "2e618b38ae5b420f7a1fe6783268093348367c51"
assert BASE == "2375ab9add0cc5d569c8ea35d229b82813fd8557"

spec = importlib.util.spec_from_file_location("b132_gates_original", HERE / "run_132_gates.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: gates.py author|committed NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert out.parent == OUTROOT and not out.exists()
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
    write(out / "admission.json", {"head": head, "parent": PARENT, "originalBatchBase": BASE,
                                   "mode": mode, "memory": memory})
    expected = None
    for name in runner.CHECKS:
        expected = runner.run_gate(name, out, expected)
    guard = start_guard()
    try:
        if mode == "committed":
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
            assert expected == committed_manifest
    finally:
        memory = guard.finish()
    result = {
        "status": "PASS", "mode": mode, "head": head, "parent": PARENT, "originalBatchBase": BASE,
        "checks": list(runner.CHECKS), "serial": True, "manifestSha256": expected,
        "scoping": "Lint and linkplan intentionally retain the original batch base 2375ab9a: they audit the original new member and original support wrapper against their creation base. Revised delta and all unrelated paths are independently preservation-checked against parent 2e618b38.",
        "runnerSha256": sha(Path(__file__).read_bytes()), "delegateRunnerSha256": sha((HERE / "run_132_gates.py").read_bytes()),
        "commonHelperSha256": sha((HERE / "common_132.py").read_bytes()), "finalMemory": memory,
        "logs": {n: {"logSha256": sha((out / (n + ".log")).read_bytes()),
                     "receiptSha256": sha((out / (n + ".json")).read_bytes())} for n in runner.CHECKS},
        "limits": "Host/static bounded checks; not linguistic review, arbitrary/custom/multiple-borrow pools, Kotlin/native/device, visual, whole-set or publication acceptance."}
    write(out / "summary.json", result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
