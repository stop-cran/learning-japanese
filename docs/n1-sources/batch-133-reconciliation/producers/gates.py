import importlib.util
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import BASE, REPO, git, sha, start_guard, write

PARENT = "ad047ace020579f81bde250ac948b9a4cb597887"
spec = importlib.util.spec_from_file_location("original_b133_gates", OUT.parent / "run_133_gates.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: gates.py author|committed NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert out.parent == OUT and not out.exists()
    guard = start_guard()
    try:
        head = git("rev-parse", "HEAD").decode().strip()
        if mode == "author":
            assert head == PARENT
        else:
            assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
            git("verify-commit", "HEAD")
        manifest_before = sha((REPO / "manifest.json").read_bytes())
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
            assert expected == manifest_before == sha(git("show", "HEAD:manifest.json"))
    finally:
        memory = guard.finish()
    result = {
        "status": "PASS", "mode": mode, "head": head, "parent": PARENT, "originalBatchBase": BASE,
        "checks": list(runner.CHECKS), "serial": True, "manifestSha256": expected,
        "scoping": "Unmodified original run_133_gates.py CHECKS and run_gate: lint/linkplan retain original creation base 6858fcfb to audit new cards and support wrappers. Reconciliation preservation separately compares against direct parent ad047ace. No original plan/draft/source packet is rewritten.",
        "runnerSha256": sha(Path(__file__).read_bytes()),
        "originalRunnerSha256": sha((OUT.parent / "run_133_gates.py").read_bytes()),
        "logs": {n: {"logSha256": sha((out / (n + ".log")).read_bytes()),
                     "receiptSha256": sha((out / (n + ".json")).read_bytes())} for n in runner.CHECKS},
        "finalMemory": memory,
        "limits": "Host/static bounded checks; not linguistic review, custom/multiple-borrow pools, native/device, visual, whole-set or publication acceptance."
    }
    write(out / "summary.json", result)
    print(json.dumps({"status": "PASS", "mode": mode, "head": head, "checks": list(runner.CHECKS),
                      "summarySha256": sha((out / "summary.json").read_bytes())}))


if __name__ == "__main__":
    main()
