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
REPO = ROOT / "b124-worktree"
LEAN = ROOT / "lean"
PUBLISHED_BASE = "2655539b587c1ab57e64ab74a97cddaf81bb81c6"
RECONCILIATION_PARENT = "fa394d237e28df96319495a003718cc9c880a069"
WAIT_SECONDS = 0.1
GUARD = ROOT / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py"
GUARD_SHA256 = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"

if hashlib.sha256(GUARD.read_bytes()).hexdigest() != GUARD_SHA256:
    raise RuntimeError("Pinned RAM guard hash mismatch")
spec = importlib.util.spec_from_file_location("ramguard", GUARD)
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)

CHECKS = {
    "lint": [LEAN / "n1_batch_tool.py", "lint", "--base", PUBLISHED_BASE, "--no-jmdict", "裕"],
    "quiz-safety": [LEAN / "quiz_safety.py", "裕"],
    "linkplan": [LEAN / "n1_linkplan.py", "verify", PUBLISHED_BASE, "裕"],
    "reading-exposure": [HERE / "check-reading-exposure.py"],
    "validate": [REPO / "tools" / "validate.py"],
    "manifest": [REPO / "tools" / "build_manifest.py"],
    "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
    "budget": [REPO / "tools" / "check_content_budget.py"],
    "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
    "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def run_gate(name, output_dir, expected_manifest):
    free = support.available_ram()
    if free <= 2 * 1024**3:
        (output_dir / f"{name}-admission.json").write_text(
            json.dumps({
                "gate": name,
                "freeBytes": free,
                "requiredExclusiveBytes": 2 * 1024**3,
                "admitted": False,
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        raise MemoryError(f"{name}: requires >2 GiB free RAM; got {free} bytes.")
    log_path = output_dir / f"{name}.log"
    guard = support.RamGuard()
    guard.start()
    process = None
    code = None
    started = datetime.now(timezone.utc).isoformat()
    env = {
        **os.environ,
        "N1_REPO": str(REPO),
        "PYTHONPATH": os.pathsep.join(
            value for value in (str(LEAN), os.environ.get("PYTHONPATH", "")) if value
        ),
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    command = [sys.executable, "-B", *map(str, CHECKS[name])]
    try:
        with log_path.open("xb") as stream:
            process = subprocess.Popen(
                command,
                cwd=REPO,
                stdout=stream,
                stderr=subprocess.STDOUT,
                env=env,
            )
            while True:
                try:
                    code = process.wait(timeout=WAIT_SECONDS)
                    break
                except subprocess.TimeoutExpired:
                    guard.check()
            guard.check()
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=WAIT_SECONDS)
            except subprocess.TimeoutExpired:
                process.kill()
                while True:
                    try:
                        process.wait(timeout=WAIT_SECONDS)
                        break
                    except subprocess.TimeoutExpired:
                        continue
        memory = guard.finish()
        data = log_path.read_bytes()
        manifest_sha = (
            hashlib.sha256((REPO / "manifest.json").read_bytes()).hexdigest()
            if name in ("manifest", "manifest-rebuild")
            else None
        )
        result = {
            "gate": name,
            "startedAt": started,
            "completedAt": datetime.now(timezone.utc).isoformat(),
            "command": command,
            "cwd": str(REPO),
            "exitCode": code,
            "childPid": process.pid if process else None,
            "childExitCodeAfterCleanup": process.returncode if process else None,
            "waitTimeoutSeconds": WAIT_SECONDS,
            "runnerSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "guardSha256": hashlib.sha256(GUARD.read_bytes()).hexdigest(),
            "logSha256": hashlib.sha256(data).hexdigest(),
            "logBytes": len(data),
            "memory": memory,
            "manifestSha256": manifest_sha,
            "manifestReproducible": (
                name == "manifest-rebuild" and manifest_sha == expected_manifest
            ),
        }
        (output_dir / f"{name}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, ensure_ascii=False), flush=True)
    print(data.decode("utf-8", errors="replace"), end="", flush=True)
    if memory["breach"] or code:
        raise RuntimeError(f"Reconciliation gate failed: {name}; see preserved log and receipt.")
    if name == "manifest-rebuild" and manifest_sha != expected_manifest:
        raise ValueError(f"Manifest rebuild changed bytes: {expected_manifest} != {manifest_sha}")
    return manifest_sha if name == "manifest" else expected_manifest


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit(
            "usage: python run-reconciliation-002-checks.py author|committed NEW_OUTPUT_DIRECTORY"
        )
    mode, output_dir = sys.argv[1], Path(sys.argv[2]).resolve()
    if output_dir.parent != HERE or output_dir.exists():
        raise ValueError("Output must be a new direct subdirectory of scratch-124.")
    head = git("rev-parse", "HEAD").decode().strip()
    if mode == "author":
        if head != RECONCILIATION_PARENT:
            raise RuntimeError("Authoring checks must start at the pinned reconciliation parent")
    else:
        if git("rev-parse", "HEAD^@").decode().split() != [RECONCILIATION_PARENT]:
            raise RuntimeError("Committed candidate is not a direct child of the reconciliation parent")
        if git("status", "--porcelain=v1", "--untracked-files=all"):
            raise RuntimeError("Committed candidate worktree is not clean")
        expected_commit_manifest = hashlib.sha256(
            git("show", "HEAD:manifest.json")
        ).hexdigest()
        if hashlib.sha256((REPO / "manifest.json").read_bytes()).hexdigest() != expected_commit_manifest:
            raise RuntimeError("Working manifest differs from the committed manifest")
    output_dir.mkdir()
    names = list(CHECKS)
    manifest_sha = None
    for name in names:
        manifest_sha = run_gate(name, output_dir, manifest_sha)
    if mode == "committed":
        if git("status", "--porcelain=v1", "--untracked-files=all"):
            raise RuntimeError("Committed candidate worktree changed during verification")
        if manifest_sha != expected_commit_manifest:
            raise RuntimeError("Committed manifest was not reproducible")
    summary = {
        "batch": "124",
        "reconciliation": 2,
        "status": "PASS",
        "mode": mode,
        "publishedBase": PUBLISHED_BASE,
        "reconciliationParent": RECONCILIATION_PARENT,
        "startingHead": head,
        "checks": names,
        "manifestSha256": manifest_sha,
        "runnerSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "limits": (
            "Bounded host model only; no arbitrary-pool, multiple-borrow, Kotlin/native/device, "
            "linguistic, exact served-ZIP, or publication acceptance."
        ),
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
