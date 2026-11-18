import importlib.util
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import BASE, REPO, git, sha, start_guard, write
from notes import PARENT

spec = importlib.util.spec_from_file_location("original_b133_gates", OUT.parent / "run_133_gates.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def main():
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert mode in ("author", "committed") and out.parent == OUT and not out.exists()
    guard = start_guard()
    try:
        head = git("rev-parse", "HEAD").decode().strip()
        if mode == "author":
            assert head == PARENT
        else:
            assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
            git("verify-commit", "HEAD")
        initial_manifest = sha((REPO / "manifest.json").read_bytes())
    finally:
        memory = guard.finish()
    out.mkdir()
    write(out / "admission.json", {"head": head, "parent": PARENT, "originalBatchBase": BASE, "mode": mode, "memory": memory})
    expected = None
    for name in runner.CHECKS:
        expected = runner.run_gate(name, out, expected)
    guard = start_guard()
    try:
        if mode == "committed":
            assert expected == initial_manifest == sha(git("show", "HEAD:manifest.json"))
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
    finally:
        memory = guard.finish()
    summary = {
        "status": "PASS", "mode": mode, "head": head, "parent": PARENT, "originalBatchBase": BASE,
        "checks": list(runner.CHECKS), "serial": True, "manifestSha256": expected,
        "scoping": "Unmodified run_133_gates.py CHECKS/run_gate, including original creation-base lint/linkplan and all three original members. Single-card preservation independently compares with 110b4ffb; no earlier plans/drafts/reconciliation records rewritten.",
        "runnerSha256": sha(Path(__file__).read_bytes()),
        "originalRunnerSha256": sha((OUT.parent / "run_133_gates.py").read_bytes()),
        "logs": {n: {"logSha256": sha((out / (n + ".log")).read_bytes()),
                     "receiptSha256": sha((out / (n + ".json")).read_bytes())} for n in runner.CHECKS},
        "memory": memory,
        "limits": "Bounded host/static checks, not linguistic review, custom/multiple-borrow pools, Kotlin/native/device, rendering, whole-set or publication acceptance."
    }
    write(out / "summary.json", summary)
    print(json.dumps({"status": "PASS", "mode": mode, "head": head, "checks": summary["checks"],
                      "summarySha256": sha((out / "summary.json").read_bytes())}))


if __name__ == "__main__":
    main()
