import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parent
repo = root / "b125-worktree"
lean = root / "lean"
base = "419aafb53d6488f67817f325e0e63ad51651780a"
parent = "483bb066e68faf354779f7d5fc73c4594605cdd7"
assert os.environ["N1_REPO"] == str(repo)
runner_path = root / "scratch-124" / "run-reconciliation-002-checks.py"
spec = importlib.util.spec_from_file_location("bounded_runner", runner_path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
runner.REPO, runner.LEAN = repo, lean
runner.CHECKS = {
    "lint": [lean / "n1_batch_tool.py", "lint", "--base", base, "--no-jmdict", "侵"],
    "quiz-safety": [lean / "quiz_safety.py", "侵"],
    "linkplan": [lean / "n1_linkplan.py", "verify", base, "侵"],
    "reading-exposure": [here / "reading.py"],
    "validate": [repo / "tools" / "validate.py"],
    "manifest": [repo / "tools" / "build_manifest.py"],
    "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
    "budget": [repo / "tools" / "check_content_budget.py"],
    "vocabulary": [repo / "tools" / "grammar_vocabulary.py", "check"],
    "manifest-rebuild": [repo / "tools" / "build_manifest.py"],
}

def git(*args):
    return subprocess.check_output(["git", *args], cwd=repo)

if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
    raise SystemExit("usage: reconciliation-001-gates.py author|committed NEW_OUTPUT_DIRECTORY")
mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
if out.parent != here or out.exists():
    raise ValueError("Output must be a new direct subdirectory of scratch-125")
head = git("rev-parse", "HEAD").decode().strip()
if mode == "author":
    assert head == parent
else:
    assert git("rev-parse", "HEAD^@").decode().split() == [parent]
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    committed = hashlib.sha256(git("show", "HEAD:manifest.json")).hexdigest()
    assert hashlib.sha256((repo / "manifest.json").read_bytes()).hexdigest() == committed
out.mkdir()
manifest = None
for name in runner.CHECKS:
    manifest = runner.run_gate(name, out, manifest)
if mode == "committed":
    assert manifest == committed
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
summary = {"batch": 125, "reconciliation": 1, "mode": mode, "publishedBase": base, "parent": parent, "head": head, "checks": list(runner.CHECKS), "manifestSha256": manifest, "runnerSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "boundedRunnerSha256": hashlib.sha256(runner_path.read_bytes()).hexdigest(), "status": "PASS", "limits": "Bounded host model only; no arbitrary-pool, multiple-borrow, Kotlin/native/device, or publication acceptance."}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary))
