import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from b128_common import BASE, CLEANUP_SECONDS, GUARD_SHA, HERE, REPO, ROOT, git, sha, start_guard, stop_child, write

LEAN = ROOT / "lean"
CHECKS = {
    "lint": [LEAN / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", "唇"],
    "quiz-safety": [LEAN / "quiz_safety.py", "唇"],
    "linkplan": [LEAN / "n1_linkplan.py", "verify", BASE, "唇"],
    "reading-exposure": [HERE / "check_reading_b128.py"],
    "validate": [REPO / "tools" / "validate.py"],
    "manifest": [REPO / "tools" / "build_manifest.py"],
    "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
    "budget": [REPO / "tools" / "check_content_budget.py"],
    "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
    "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
}


def run_gate(name, out, expected):
    guard = start_guard()
    process, code = None, None
    log = out / (name + ".log")
    command = [sys.executable, "-B", *map(str, CHECKS[name])]
    started = datetime.now(timezone.utc).isoformat()
    try:
        env = {**os.environ, "N1_REPO": str(REPO), "PYTHONPATH": str(LEAN), "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
        with log.open("xb") as stream:
            process = subprocess.Popen(command, cwd=REPO, stdout=stream, stderr=subprocess.STDOUT, env=env)
            while True:
                try:
                    code = process.wait(timeout=0.1)
                    break
                except subprocess.TimeoutExpired:
                    guard.check()
            guard.check()
    finally:
        active_error = sys.exc_info()[1]
        cleanup_error = None
        try:
            stop_child(process)
        except (OSError, subprocess.TimeoutExpired) as error:
            cleanup_error = error
        memory = guard.finish()
        data = log.read_bytes() if log.exists() else b""
        manifest_sha = sha((REPO / "manifest.json").read_bytes()) if name in ("manifest", "manifest-rebuild") else None
        write(out / (name + ".json"), {
            "gate": name, "command": command, "cwd": str(REPO),
            "startedAt": started, "completedAt": datetime.now(timezone.utc).isoformat(),
            "exitCode": code, "childPid": process.pid if process else None,
            "childExitCodeAfterCleanup": process.returncode if process else None,
            "waitTimeoutSeconds": 0.1, "runnerSha256": sha(Path(__file__).read_bytes()),
            "commonHelperSha256": sha((HERE / "b128_common.py").read_bytes()),
            "cleanupTimeoutSecondsPerStage": CLEANUP_SECONDS,
            "cleanupScope": "Immediate child PID only; not descendant-process acceptance.",
            "cleanupError": str(cleanup_error) if cleanup_error is not None else None,
            "activeError": str(active_error) if active_error is not None else None,
            "guardSha256": GUARD_SHA, "memory": memory,
            "logSha256": sha(data), "logBytes": len(data), "manifestSha256": manifest_sha,
            "manifestReproducible": name == "manifest-rebuild" and manifest_sha == expected,
        })
        if cleanup_error is not None:
            if active_error is None:
                raise cleanup_error
            active_error.add_note(f"Child cleanup also failed: {cleanup_error}")
    print(json.dumps({"gate": name, "exitCode": code, "log": str(log), "memoryBreach": memory["breach"]}), flush=True)
    if memory["breach"] or code != 0:
        print(data.decode("utf-8", "replace"), end="", flush=True)
        raise RuntimeError(f"Gate {name} failed; preserving {out}")
    if name == "manifest-rebuild" and manifest_sha != expected:
        raise RuntimeError("Manifest byte reproduction failed")
    return manifest_sha if name == "manifest" else expected


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: run_b128_gates.py author|committed NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert out.parent == HERE and not out.exists()
    admission_guard = start_guard()
    try:
        head = git("rev-parse", "HEAD").decode().strip()
        if mode == "author":
            assert head == BASE
        else:
            assert git("rev-parse", "HEAD^@").decode().split() == [BASE]
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
            committed_manifest = sha(git("show", "HEAD:manifest.json"))
    finally:
        admission_memory = admission_guard.finish()
    out.mkdir()
    write(out / "admission.json", {"head": head, "mode": mode, "memory": admission_memory})
    expected = None
    for name in CHECKS:
        expected = run_gate(name, out, expected)
    final_guard = start_guard()
    try:
        if mode == "committed":
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
            assert expected == committed_manifest
    finally:
        final_memory = final_guard.finish()
    summary = {
        "batch": "128", "mode": mode, "status": "PASS", "base": BASE, "startingHead": head,
        "checks": list(CHECKS), "manifestSha256": expected,
        "runnerSha256": sha(Path(__file__).read_bytes()), "guardSha256": GUARD_SHA,
        "serial": True, "waitTimeoutSeconds": 0.1, "finalMemory": final_memory,
        "commonHelperSha256": sha((HERE / "b128_common.py").read_bytes()),
        "cleanupTimeoutSecondsPerStage": CLEANUP_SECONDS,
        "logs": {name: {"logSha256": sha((out / (name + ".log")).read_bytes()), "receiptSha256": sha((out / (name + ".json")).read_bytes())} for name in CHECKS},
        "limits": "Host/static checks only, not independent linguistic, arbitrary/custom-pool, multiple-borrow, Kotlin/native/device, publication or whole-set acceptance.",
    }
    write(out / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
