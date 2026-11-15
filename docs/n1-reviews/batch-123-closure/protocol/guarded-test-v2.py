"""Run a command with bounded waits so RAM breaches interrupt live children."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
REPO = ROOT / "b123-worktree"
HERE = Path(__file__).resolve().parent
GUARD_PATH = ROOT / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py"
GUARD_SHA = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"
WAIT_SECONDS = 0.1


def run_command(command, output, cwd, env, guard):
    process = None
    code = None
    started = datetime.now(timezone.utc).isoformat()
    guard.start()
    try:
        with (output / "output.log").open("xb") as log:
            process = subprocess.Popen(command, cwd=cwd, env=env,
                                       stdout=log, stderr=subprocess.STDOUT)
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
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        memory = guard.finish()
        log_path = output / "output.log"
        data = log_path.read_bytes() if log_path.exists() else b""
        result = {
            "started": started, "finished": datetime.now(timezone.utc).isoformat(),
            "command": command, "cwd": str(cwd), "exitCode": code,
            "childPid": process.pid if process is not None else None,
            "childExitCodeAfterCleanup": process.returncode if process is not None else None,
            "waitTimeoutSeconds": WAIT_SECONDS,
            "logSha256": hashlib.sha256(data).hexdigest(), "memory": memory,
            "runnerSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "guardSha256": GUARD_SHA,
        }
        with (output / "receipt.json").open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(data.decode("utf-8", errors="replace"))
    print(json.dumps(result, ensure_ascii=False))
    if code != 0 or memory["breach"]:
        raise RuntimeError("Command failed or breached its RAM guard; receipt preserved.")
    return result


def main():
    if len(sys.argv) < 3:
        raise SystemExit("usage: guarded-test-v2.py NEW_OUTPUT_DIRECTORY COMMAND [ARGS...]")
    output = Path(sys.argv[1]).resolve()
    if output.parent != HERE or output.exists():
        raise ValueError("Output must be a new direct child of scratch-123\\review.")
    if hashlib.sha256(GUARD_PATH.read_bytes()).hexdigest() != GUARD_SHA:
        raise ValueError("Pinned RAM guard changed.")
    spec = importlib.util.spec_from_file_location("ramguard_v2", GUARD_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    free = module.available_ram()
    if free <= 2 * 1024**3:
        raise MemoryError(f"Requires more than 2 GiB available RAM; found {free} bytes.")
    output.mkdir()
    env = dict(os.environ, N1_REPO=str(REPO), PYTHONIOENCODING="utf-8",
               PYTHONDONTWRITEBYTECODE="1")
    run_command(sys.argv[2:], output, REPO, env, module.RamGuard())


if __name__ == "__main__":
    main()
