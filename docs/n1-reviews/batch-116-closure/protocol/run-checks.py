"""Run the existing B116 host gates serially with fresh admission and continuous RAM guards."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT / "rollout-recovered" / "learning-japanese"
LEAN = ROOT / "lean"
GUARD = ROOT / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py"
assert hashlib.sha256(GUARD.read_bytes()).hexdigest() == "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"
spec = importlib.util.spec_from_file_location("b116_gate_guard", GUARD)
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)
selection = json.loads((HERE / "selection.json").read_bytes())
members = selection["order"]
checks = {
    "lint": [LEAN / "n1_batch_tool.py", "lint", "--base", selection["base"], "--no-jmdict", *members],
    "quiz-safety": [LEAN / "quiz_safety.py", *members],
    "linkplan": [LEAN / "n1_linkplan.py", "verify", selection["base"], *members],
    "reading-exposure-initial": [HERE / "check-reading-exposure.py"],
    "validate": [REPO / "tools" / "validate.py"],
    "manifest": [REPO / "tools" / "build_manifest.py"],
    "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
    "budget": [REPO / "tools" / "check_content_budget.py"],
    "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
    "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
    "reading-exposure-final": [HERE / "check-reading-exposure.py"],
    "tooling": ["-m", "unittest", "test-review-chain", "test-review-audit-v3",
                "test-report-structure", "test-prepare-extension"],
    "tooling-s1": ["-m", "unittest", "test-review-chain", "test-review-audit-v4",
                   "test-report-structure", "test-prepare-extension"],
    "prompts": [HERE / "build-prompts.py"],
}


def run(name):
    if name not in checks:
        raise ValueError(f"Unknown B116 gate: {name}")
    log, receipt = HERE / f"{name}.txt", HERE / f"{name}-run.json"
    if log.exists() or receipt.exists():
        raise FileExistsError(f"Preserve the existing gate run before a deliberate rerun: {name}")
    if support.available_ram() <= 2 * 1024**3:
        raise MemoryError(f"{name}: startup requires more than 2048 MiB free RAM.")
    command = [sys.executable, "-B", *map(str, checks[name])]
    cwd = HERE if name.startswith("tooling") else REPO
    guard = support.RamGuard()
    guard.start()
    process = None
    started = datetime.now(timezone.utc).isoformat()
    try:
        with log.open("xb") as output:
            process = subprocess.Popen(command, cwd=cwd, stdout=output, stderr=subprocess.STDOUT,
                                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            code = process.wait()
            guard.check()
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        memory = guard.finish()
    memory["peakScope"] = "Gate-launcher Python process and guard thread only; child peak not measured."
    memory["additionalChecks"] = "Fresh >2048 MiB admission; continuous 0.25-second free-RAM sampling and exit check."
    data = log.read_bytes()
    result = {
        "gate": name, "startedAt": started, "completedAt": datetime.now(timezone.utc).isoformat(),
        "command": command, "cwd": str(cwd), "pid": process.pid, "exitCode": code,
        "logSha256": hashlib.sha256(data).hexdigest(), "logBytes": len(data), "memory": memory,
    }
    with receipt.open("x", encoding="utf-8") as output:
        output.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False), flush=True)
    print(data.decode("utf-8"), end="", flush=True)
    if memory["breach"] or code:
        raise RuntimeError(f"B116 gate failed: {name}; see preserved log and receipt.")


if __name__ == "__main__":
    for name in sys.argv[1:] or checks:
        run(name)
