import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from b126_common import BASE, GUARD_SHA, HERE, REPO, ROOT, git, sha, start_guard, write

LEAN = ROOT / "lean"
CHECKS = {
    "lint": [LEAN / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", "傘"],
    "quiz-safety": [LEAN / "quiz_safety.py", "傘"],
    "linkplan": [LEAN / "n1_linkplan.py", "verify", BASE, "傘"],
    "reading-exposure": [HERE / "check_reading_b126.py"],
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
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=0.1)
            except subprocess.TimeoutExpired:
                process.kill()
                while True:
                    try:
                        process.wait(timeout=0.1)
                        break
                    except subprocess.TimeoutExpired:
                        continue
        memory = guard.finish()
        data = log.read_bytes() if log.exists() else b""
        manifest_sha = sha((REPO / "manifest.json").read_bytes()) if name in ("manifest", "manifest-rebuild") else None
        result = {
            "gate": name, "command": command, "cwd": str(REPO),
            "startedAt": started, "completedAt": datetime.now(timezone.utc).isoformat(),
            "exitCode": code, "childPid": process.pid if process else None,
            "childExitCodeAfterCleanup": process.returncode if process else None,
            "waitTimeoutSeconds": 0.1, "runnerSha256": sha(open(__file__, "rb").read()),
            "guardSha256": GUARD_SHA, "memory": memory,
            "logSha256": sha(data), "logBytes": len(data), "manifestSha256": manifest_sha,
            "manifestReproducible": name == "manifest-rebuild" and manifest_sha == expected,
        }
        write(out / (name + ".json"), result)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    print(data.decode("utf-8", "replace"), end="", flush=True)
    if memory["breach"] or code != 0:
        raise RuntimeError(f"Gate {name} failed; preserving {out}")
    if name == "manifest-rebuild" and manifest_sha != expected:
        raise RuntimeError("Manifest byte reproduction failed")
    return manifest_sha if name == "manifest" else expected


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("author", "committed"):
        raise SystemExit("usage: run_b126_gates.py author|committed NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    if out.parent != HERE or out.exists():
        raise RuntimeError("Output must be a new direct scratch-126 subdirectory")
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
        "batch": "126", "mode": mode, "status": "PASS", "base": BASE, "startingHead": head,
        "checks": list(CHECKS), "manifestSha256": expected,
        "runnerSha256": sha(open(__file__, "rb").read()), "guardSha256": GUARD_SHA,
        "serial": True, "waitTimeoutSeconds": 0.1, "finalMemory": final_memory,
        "logs": {name: {"logSha256": sha((out / (name + ".log")).read_bytes()), "receiptSha256": sha((out / (name + ".json")).read_bytes())} for name in CHECKS},
        "limits": "Host/static checks only, not independent linguistic, arbitrary/custom-pool, multiple-borrow, Kotlin/native/device, publication or whole-set acceptance.",
    }
    write(out / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    from pathlib import Path
    main()
