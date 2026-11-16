import importlib.util
import os
import sys
from pathlib import Path

root = Path(r"C:\Users\stop-\n1-kanji-workspace")
repo = root / "b125-worktree"
scratch = root / "scratch-125"
assert os.environ["N1_REPO"] == str(repo)
spec = importlib.util.spec_from_file_location("bounded_runner", root / "scratch-124" / "run-reconciliation-002-checks.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
runner.REPO, runner.LEAN = repo, root / "lean"
out = Path(sys.argv[1]).resolve()
if out.parent != scratch or out.exists():
    raise ValueError("Output must be a new direct subdirectory of scratch-125")
out.mkdir()
runner.CHECKS = {"inventory": [Path(__file__).parent / "inventory.py", out / "card-inventory.json"]}
runner.run_gate("inventory", out, None)
