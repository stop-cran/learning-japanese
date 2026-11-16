import json
import subprocess
import sys
from pathlib import Path
from b127_common import CLEANUP_SECONDS, HERE, REPO, git, sha, start_guard, stop_child, write
from reconcile_sources_b127 import OUT, PARENT

mode = sys.argv[1]
assert mode in ("stage", "sign")
out = HERE / ("reconciliation-git-" + mode + "-001")
assert not out.exists()
out.mkdir()
guard, process = start_guard(), None
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
    assert git("config", "user.name").decode("utf-8").strip() == git("show", "-s", "--format=%an", PARENT).decode("utf-8").strip()
    assert git("config", "user.signingkey").decode().strip() == "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
    assert git("config", "commit.gpgsign").decode().strip() == "true"
    preserved = json.loads((HERE / "reconciliation-preservation-author-001" / "summary.json").read_text(encoding="utf-8"))
    assert preserved["status"] == "PASS" and preserved["parent"] == PARENT
    inventory = json.loads((OUT / "packet-files.json").read_text(encoding="utf-8"))
    for path, info in inventory["files"].items():
        guard.check()
        assert sha((OUT / path).read_bytes()) == info["sha256"]
    if mode == "stage":
        args = ["add", "--sparse", "--", "kanji/倉.md", "manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-127-progress-002.json", "docs/n1-sources/batch-127-reconciliation"]
    else:
        assert not git("diff", "--name-only")
        staged = git("-c", "core.quotepath=false", "diff", "--cached", "--name-only").decode("utf-8").splitlines()
        assert set(staged) == set(preserved["changedFiles"])
        args = [
            "commit", "-SD4C9A275A218AF747B787AFA9D94B9D311BD26A7",
            "-m", "Reconcile B127 倉 cancellation and finite meaning guards",
            "-m", "Preserve complete finite comparison families, both displayed directions, explicit conservative uncertainty and isolated author responses. Keep original B127 evidence, vocabulary and stroke bytes unchanged. Independent confirmations and publication remain pending.",
            "-m", "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>",
        ]
    command = ["git", *args]
    with (out / "command.log").open("xb") as stream:
        process = subprocess.Popen(command, cwd=REPO, stdout=stream, stderr=subprocess.STDOUT)
        while True:
            try:
                code = process.wait(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                guard.check()
        guard.check()
    assert code == 0, (out / "command.log").read_text(encoding="utf-8")
    head = git("rev-parse", "HEAD").decode().strip()
    if mode == "sign":
        assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
    print((out / "command.log").read_text(encoding="utf-8"), end="")
    print(json.dumps({"mode": mode, "head": head, "output": str(out)}))
finally:
    active_error, cleanup_error = sys.exc_info()[1], None
    try:
        stop_child(process)
    except (OSError, subprocess.TimeoutExpired) as error:
        cleanup_error = error
    memory = guard.finish()
    write(out / "receipt.json", {
        "mode": mode, "parent": PARENT, "head": locals().get("head"), "command": locals().get("command"),
        "exitCode": process.returncode if process else None, "childPid": process.pid if process else None,
        "cleanupError": str(cleanup_error) if cleanup_error is not None else None,
        "activeError": str(active_error) if active_error is not None else None,
        "memory": memory, "waitTimeoutSeconds": 0.1, "cleanupTimeoutSecondsPerStage": CLEANUP_SECONDS,
        "logSha256": sha((out / "command.log").read_bytes()) if (out / "command.log").exists() else None,
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
    if cleanup_error is not None:
        if active_error is None:
            raise cleanup_error
        active_error.add_note(f"Child cleanup also failed: {cleanup_error}")
