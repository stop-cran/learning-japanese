"""Run every B-batch gate in the current worktree. Usage: python n1_gates.py BATCH BASE 'K1 K2 ...' 'CHANGED ...' 'WORD1 WORD2 ...'"""
import os, subprocess as sp, sys
from pathlib import Path

batch, base, new, changed, words = sys.argv[1], sys.argv[2], sys.argv[3].split(), sys.argv[4].split(), sys.argv[5].split()
r = Path.cwd()
lean = r.parent / "lean"
env = dict(os.environ, N1_REPO=str(r), N1_LEAN=str(lean), PYTHONIOENCODING="utf-8")
py = [sys.executable, "-X", "utf8", "-B"]
ev = r / "docs" / "n1-reviews"
steps = [
    ("unittest", py + ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
    ("validate", py + ["tools/validate.py"]),
    ("budget", py + ["tools/check_content_budget.py"]),
    ("grammar", py + ["tools/grammar_vocabulary.py", "check"]),
    ("audit", py + ["tools/audit_n1_batch.py", "--batch", batch]),
    ("quiz_safety", py + [str(lean / "quiz_safety.py"), *new]),
    ("reading_exposure", py + [str(lean / "reading_exposure.py"), *new]),
    ("reading_options", py + [str(lean / "reading_options.py"), *new]),
    ("lint", py + [str(lean / "n1_batch_tool.py"), "lint", "--base", base, *new]),
    ("meta_scan", py + [str(ev / "batch-137-closure/confirm-packet/gpt/evidence/meta_scan.py"), str(r), *new, *changed]),
    ("word_quiz", py + [str(ev / "batch-156-closure/packet/evidence/audits/word_quiz_audit.py"), str(r), *words]),
]
only = set(os.environ.get("ONLY", "").split()) or None
for name, cmd in steps:
    if only and name not in only:
        continue
    p = sp.run(cmd, cwd=r, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (p.stdout + p.stderr).strip().splitlines()
    tail = out[-6:] if name != "word_quiz" else [l for l in out if "problem" in l.lower()][-3:]
    print(f"== {name} exit={p.returncode}")
    print("\n".join(tail))
# Manifest freshness: rebuilding must not change the committed/staged manifest.
before = (r / "manifest.json").read_bytes()
sp.run(py + ["tools/build_manifest.py"], cwd=r, env=env, capture_output=True)
print("== manifest fresh:", before == (r / "manifest.json").read_bytes())
