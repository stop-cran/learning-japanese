import json
import os
import subprocess
import sys
import time
from pathlib import Path
from common_133 import BASE, HERE, PACKET, REPO, git, sha, start_guard, stop_child, write

OUT = HERE / "sign-attempt-001"


def main():
    assert not OUT.exists()
    OUT.mkdir()
    guard = start_guard()
    process, code, timed_out = None, None, False
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert git("remote", "get-url", "origin").decode().strip() == "https://github.com/stop-cran/learning-japanese.git"
        assert git("config", "user.name").decode().strip() == "Roman Konstantinovskiy"
        assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
        assert git("config", "user.signingkey").decode().strip() == "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
        assert json.loads((HERE / "author-gates-003" / "summary.json").read_bytes())["status"] == "PASS"
        assert json.loads((HERE / "author-preservation-001" / "summary.json").read_bytes())["status"] == "PASS"
        assert not git("diff", "--cached", "--name-only", "-z")
        required = {f"kanji/{c}.md" for c in "琴鉛滝"} | {f"strokes/{c}.json" for c in "琴鉛滝"}
        required |= {f"words/{w}.md" for w in ("琴", "鉛筆", "滝")}
        required |= {"manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-133-progress.json"}
        git("add", "--sparse", "--", *sorted(required), "docs/n1-sources/batch-133")
        staged = git("diff", "--cached", "--name-only", "-z").decode().strip("\0").split("\0")
        expected = required | {"docs/n1-sources/batch-133/" + str(p.relative_to(PACKET)).replace("\\", "/")
                               for p in PACKET.rglob("*") if p.is_file()}
        assert set(staged) == expected
        git("-c", "core.whitespace=cr-at-eol", "diff", "--cached", "--check")
        write(OUT / "staged.json", {
            "base": BASE, "files": staged,
            "authorGatesSummarySha256": sha((HERE / "author-gates-003" / "summary.json").read_bytes()),
            "authorPreservationSummarySha256": sha((HERE / "author-preservation-001" / "summary.json").read_bytes())})
        command = ["git", "-c", "core.whitespace=cr-at-eol", "commit", "-S", "-m",
                   "Add N1 kanji cards for 琴, 鉛 and 滝", "-m",
                   "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"]
        log = OUT / "commit.log"
        with log.open("xb") as stream:
            process = subprocess.Popen(command, cwd=REPO, stdout=stream, stderr=subprocess.STDOUT,
                                       env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
            deadline = time.monotonic() + 75
            while True:
                try:
                    code = process.wait(timeout=0.1)
                    break
                except subprocess.TimeoutExpired:
                    guard.check()
                    if time.monotonic() >= deadline:
                        timed_out = True
                        break
        if timed_out:
            stop_child(process)
        print(json.dumps({"exitCode": code, "timedOut": timed_out, "log": str(log),
                          "logSha256": sha(log.read_bytes())}, ensure_ascii=False))
    finally:
        stop_child(process)
        write(OUT / "receipt.json", {
            "attempted": process is not None, "exitCode": code, "timedOut": timed_out,
            "childExitCodeAfterCleanup": process.returncode if process else None,
            "waitTimeoutSeconds": 0.1, "cleanupTimeoutSecondsPerStage": 10,
            "memory": guard.finish(), "producerSha256": sha(Path(__file__).read_bytes())})
    if timed_out:
        raise SystemExit("Signing stalled; staged work preserved. Do not retry.")
    if code != 0:
        raise SystemExit("Signing failed; staged work preserved. Do not retry automatically.")


if __name__ == "__main__":
    main()
