import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import REPO, git, sha, start_guard, stop_child, write
from notes import PARENT, REL

KEY = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
OWNER = "Roman Konstantinovskiy"
EMAIL = "stop-cran@list.ru"


def main():
    guard = start_guard()
    process, code, error, cleanup_error = None, None, None, None
    started = datetime.now(timezone.utc).isoformat()
    log = OUT / "signing.log"
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        assert not git("diff", "--cached", "--name-only")
        for directory in ("author-gates-001", "packaged-preservation-001"):
            assert json.loads((OUT / directory / "summary.json").read_bytes())["status"] == "PASS"
        packet = REPO / REL
        inventory = json.loads((packet / "inventory.json").read_bytes())["files"]
        allowed = {"kanji/滝.md", "manifest.json"}
        expected = allowed | {REL + "/" + path for path in inventory} | {REL + "/inventory.json"}
        git("add", "--sparse", "--", *sorted(allowed), REL)
        staged = set(filter(None, git("diff", "--cached", "--name-only", "-z").decode().split("\0")))
        assert staged == expected
        hashes = {}
        for path in sorted(staged):
            guard.check()
            raw = git("show", ":" + path)
            assert raw == (REPO / path).read_bytes(), "Staging changed raw bytes: " + path
            hashes[path] = sha(raw)
        write(OUT / "staging-receipt.json", {
            "parent": PARENT, "paths": sorted(staged), "stagedRawHashes": hashes,
            "inventorySha256": sha((packet / "inventory.json").read_bytes()),
            "producerSha256": sha(Path(__file__).read_bytes())
        })
        env = {**os.environ, "GIT_AUTHOR_NAME": OWNER, "GIT_AUTHOR_EMAIL": EMAIL,
               "GIT_COMMITTER_NAME": OWNER, "GIT_COMMITTER_EMAIL": EMAIL}
        command = ["git", "commit", "-S" + KEY, "--author=" + OWNER + " <" + EMAIL + ">",
                   "-F", str(OUT / "commit-message.txt")]
        with log.open("xb") as stream:
            process = subprocess.Popen(command, cwd=REPO, env=env, stdout=stream, stderr=subprocess.STDOUT)
            deadline = time.monotonic() + 45
            while process.poll() is None:
                guard.check()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("Owner signing stalled beyond 45 seconds. Preserve staged work and yield; do not retry or bypass signing.")
                try:
                    code = process.wait(timeout=min(.1, remaining))
                except subprocess.TimeoutExpired:
                    pass
            code = process.returncode
        assert code == 0, "Owner signing failed; original log retained, no retry."
        head = git("rev-parse", "HEAD").decode().strip()
        assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
        git("verify-commit", "HEAD")
        fields = git("show", "-s", "--format=%an|%ae|%cn|%ce|%G?|%GF", "HEAD").decode().strip()
        assert fields == f"{OWNER}|{EMAIL}|{OWNER}|{EMAIL}|G|{KEY}"
        assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode()
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        result = {
            "status": "SIGNED_POST_COMMIT_GATES_PENDING", "revision": head, "parent": PARENT,
            "ownerSignature": fields, "clean": True, "changedPaths": sorted(staged),
            "manifestSha256": sha((REPO / "manifest.json").read_bytes()),
            "contentVersion": json.loads((REPO / "manifest.json").read_bytes())["contentVersion"],
            "reconciliationInventorySha256": sha((packet / "inventory.json").read_bytes()),
            "signingAttempts": 1, "push": False
        }
        write(OUT / "revision.json", result)
        print(json.dumps({k: result[k] for k in ("status", "revision", "parent", "ownerSignature", "clean")}))
    except BaseException as exc:
        error = str(exc)
        raise
    finally:
        try:
            stop_child(process)
        except (OSError, subprocess.TimeoutExpired) as exc:
            cleanup_error = str(exc)
        memory = guard.finish()
        write(OUT / "signing-receipt.json", {
            "startedAt": started, "finishedAt": datetime.now(timezone.utc).isoformat(),
            "exitCode": code, "childExitCodeAfterCleanup": process.returncode if process else None,
            "childPid": process.pid if process else None, "error": error, "cleanupError": cleanup_error,
            "attempts": 1, "signingDeadlineSeconds": 45, "waitTimeoutSeconds": .1,
            "cleanupSecondsPerStage": 10, "logSha256": sha(log.read_bytes()) if log.exists() else None,
            "memory": memory, "producerSha256": sha(Path(__file__).read_bytes())
        })
        if cleanup_error:
            raise RuntimeError(cleanup_error)


if __name__ == "__main__":
    main()
