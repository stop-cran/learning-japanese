import json
import os
import subprocess
import sys
import time
from pathlib import Path
from recon_common import *

FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
attempt = HERE / "signing-attempt-001.json"
assert not attempt.exists(), "Never retry or bypass an existing signing attempt."
guard = start_guard()
process = None
stdout, stderr, stalled = b"", b"", False
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    assert git("rev-parse", "HEAD^@").decode().split() == [BASE]
    assert git("remote", "get-url", "origin").decode().strip() in (
        "https://github.com/stop-cran/learning-japanese.git",
        "https://github.com/stop-cran/learning-japanese")
    inventory = json.loads((PACKET / "evidence-inventory-001.json").read_text(encoding="utf8"))
    for path, digest in inventory["files"].items():
        assert sha((PACKET / path).read_bytes()) == digest
    expected = set(json.loads((PACKET / "changed-file-inventory.json").read_text(encoding="utf8"))["paths"])
    for directory in ("author-gates-001", "author-preservation-001"):
        proof = json.loads((HERE / directory / "summary.json").read_text(encoding="utf8"))
        assert proof["status"] == "PASS"
        assert proof["manifestSha256"] == sha((REPO / "manifest.json").read_bytes())
    preserve = json.loads((HERE / "author-preservation-001" / "summary.json").read_text(encoding="utf8"))
    assert preserve["finalInventorySha256"] == sha((PACKET / "evidence-inventory-001.json").read_bytes())
    assert set(git("diff", "--name-only", PARENT).decode().splitlines()) | set(git("ls-files", "--others", "--exclude-standard").decode().splitlines()) == expected
    git("add", "--sparse", "--", *sorted(expected))
    assert set(git("diff", "--cached", "--name-only", PARENT).decode().splitlines()) == expected
    assert not git("diff", "--name-only")
    assert not git("ls-files", "--others", "--exclude-standard")
    git("-c", "core.whitespace=cr-at-eol", "diff", "--cached", "--check")
    for path in expected:
        assert git("show", ":" + path) == (REPO / path).read_bytes(), path
    write(HERE / "staging-001.json", {
        "parent": PARENT, "tree": git("write-tree").decode().strip(),
        "paths": sorted(expected), "rawSha256": {p: sha((REPO / p).read_bytes()) for p in expected},
        "inventorySha256": sha((PACKET / "evidence-inventory-001.json").read_bytes()),
        "authorGatesSummarySha256": sha((HERE / "author-gates-001" / "summary.json").read_bytes()),
        "authorPreservationSummarySha256": sha((HERE / "author-preservation-001" / "summary.json").read_bytes()),
        "whitespaceDisposition": "Explicit cr-at-eol acceptance; do not rewrite old CRLF prose or frozen evidence.",
    })
    name = git("show", "-s", "--format=%an", PARENT).decode().strip()
    assert name == "Roman Konstantinovskiy"
    assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
    assert git("config", "user.signingkey").decode().strip() == FINGERPRINT
    message = ("Reconcile B129 finite meaning-guard review\n\n"
               "Bind all 28 pair dispositions, complete source queries and separate reviewer responses.\n"
               "Preserve frozen B129 evidence and all prior runtime identities and reading selections.\n\n"
               "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>")
    command = ["git", "-c", f"user.name={name}", "-c", "user.email=stop-cran@list.ru",
               "commit", "--quiet", f"--gpg-sign={FINGERPRINT}", "-m", message]
    assert "--amend" not in command
    env = {**os.environ, "GIT_AUTHOR_NAME": name, "GIT_AUTHOR_EMAIL": "stop-cran@list.ru",
           "GIT_COMMITTER_NAME": name, "GIT_COMMITTER_EMAIL": "stop-cran@list.ru"}
    process = subprocess.Popen(command, cwd=REPO, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    deadline = time.monotonic() + 30
    while True:
        try:
            stdout, stderr = process.communicate(timeout=0.1)
            break
        except subprocess.TimeoutExpired:
            guard.check()
            if time.monotonic() >= deadline:
                stalled = True
                stop_child(process)
                stdout, stderr = process.communicate(timeout=0.1)
                break
    guard.check()
finally:
    stop_child(process)
    memory = guard.finish()
    write(HERE / "signing-stdout-001.log", stdout)
    write(HERE / "signing-stderr-001.log", stderr)
    write(attempt, {"parent": PARENT, "stalled": stalled,
                    "exitCode": process.returncode if process else None,
                    "stdoutSha256": sha(stdout), "stderrSha256": sha(stderr), "memory": memory,
                    "maximumSigningWaitSeconds": 30, "fingerprint": FINGERPRINT,
                    "policy": "One direct-child signing attempt. On popup stall preserve staged work and yield; no retry or bypass."})
print(stdout.decode("utf8", "replace"), end="")
print(stderr.decode("utf8", "replace"), end="", file=sys.stderr)
if stalled:
    raise SystemExit("Signing stalled. Yield without retry.")
if process.returncode:
    raise SystemExit(process.returncode)
assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
print("Signed direct child:", git("rev-parse", "HEAD").decode().strip())
