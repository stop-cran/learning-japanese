import json
import subprocess
import sys
import time
from b128_common import BASE, CLEANUP_SECONDS, HERE, PACKET, REPO, git, sha, start_guard, stop_child, write

if len(sys.argv) != 2 or sys.argv[1] not in ("stage", "sign"):
    raise SystemExit("usage: commit_b128.py stage|sign")
mode = sys.argv[1]
out = HERE / ("git-" + mode + "-001")
assert not out.exists()
out.mkdir()
guard = start_guard()
process = None
try:
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
    assert git("config", "user.name").decode().strip() == git("show", "-s", "--format=%an", BASE).decode("utf-8").strip()
    assert git("config", "user.signingkey").decode().strip() == "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
    assert git("config", "commit.gpgsign").decode().strip() == "true"
    inventory = json.loads((PACKET / "packet-files-002.json").read_text(encoding="utf-8"))
    for path, info in inventory["files"].items():
        guard.check()
        assert sha((PACKET / path).read_bytes()) == info["sha256"], path
    if mode == "stage":
        args = ["add", "--sparse", "--", "kanji/唇.md", "strokes/唇.json", "words/唇.md", "manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-128-progress.json", "docs/n1-sources/batch-128"]
    else:
        assert not git("diff", "--name-only")
        gate_summary = json.loads((HERE / "author-gates-002" / "summary.json").read_text(encoding="utf-8"))
        assert gate_summary["status"] == "PASS"
        assert sha((REPO / "manifest.json").read_bytes()) == gate_summary["manifestSha256"]
        args = [
            "commit", "-SD4C9A275A218AF747B787AFA9D94B9D311BD26A7",
            "-m", "Add N1 唇 authoring candidate (batch 128)",
            "-m", "Reuse the existing N2 唇 word with a reciprocal wrapper and remove its now-false no-card sentence. Preserve complete frozen readings and dictionary families, actual whole-baseline scans, direct pair dispositions and bounded author evidence. Independent review and publication remain pending.",
            "-m", "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>",
        ]
    command = ["git", *args]
    with (out / "command.log").open("xb") as stream:
        process = subprocess.Popen(command, cwd=REPO, stdout=stream, stderr=subprocess.STDOUT)
        deadline = time.monotonic() + (30 if mode == "sign" else 60)
        while True:
            try:
                code = process.wait(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                guard.check()
                if time.monotonic() >= deadline:
                    raise TimeoutError("Signing/staging deadline reached; preserve staged state and yield. Do not retry or bypass signing.")
        guard.check()
    assert code == 0, (out / "command.log").read_text(encoding="utf-8")
    head = git("rev-parse", "HEAD").decode().strip()
    if mode == "sign":
        assert git("rev-parse", "HEAD^@").decode().split() == [BASE]
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
    print((out / "command.log").read_text(encoding="utf-8"), end="")
    print(json.dumps({"mode": mode, "head": head, "output": str(out)}, ensure_ascii=False))
finally:
    active_error = sys.exc_info()[1]
    cleanup_error = None
    try:
        stop_child(process)
    except (OSError, subprocess.TimeoutExpired) as error:
        cleanup_error = error
    memory = guard.finish()
    write(out / "receipt.json", {
        "mode": mode, "head": locals().get("head"), "command": locals().get("command"),
        "exitCode": process.returncode if process else None,
        "childPid": process.pid if process else None,
        "cleanupError": str(cleanup_error) if cleanup_error is not None else None,
        "activeError": str(active_error) if active_error is not None else None,
        "memory": memory, "waitTimeoutSeconds": 0.1,
        "cleanupTimeoutSecondsPerStage": CLEANUP_SECONDS,
        "logSha256": sha((out / "command.log").read_bytes()) if (out / "command.log").exists() else None,
        "producerSha256": sha(open(__file__, "rb").read()),
    })
    if cleanup_error is not None:
        if active_error is None:
            raise cleanup_error
        active_error.add_note(f"Child cleanup also failed: {cleanup_error}")
