import json
import os
import subprocess
import sys
import time
from pathlib import Path
from recon_common import *
from recover_preflight import check_patch_whitespace

FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
attempt = HERE / "actual-signing-attempt-001.json"
assert not attempt.exists(), "Never retry or bypass an actual signing attempt."
guard = start_guard()
process = None
stdout, stderr, stalled = b"", b"", False
try:
    first = json.loads((HERE / "signing-attempt-001.json").read_text(encoding="utf8"))
    assert first["exitCode"] is None and first["stalled"] is False
    assert not (HERE / "staging-001.json").exists(), "The initial preflight must have stopped before staging receipt and GPG launch."
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    assert git("rev-parse", "HEAD^@").decode().split() == [BASE]
    for directory in ("author-gates-002", "author-preservation-002"):
        proof = json.loads((HERE / directory / "summary.json").read_text(encoding="utf8"))
        assert proof["status"] == "PASS"
        assert proof["manifestSha256"] == sha((REPO / "manifest.json").read_bytes())
    final_inventory = PACKET / "evidence-inventory-002.json"
    inventory = json.loads(final_inventory.read_text(encoding="utf8"))
    for path, digest in inventory["files"].items():
        assert sha((PACKET / path).read_bytes()) == digest
    preserve = json.loads((HERE / "author-preservation-002" / "summary.json").read_text(encoding="utf8"))
    assert preserve["finalInventorySha256"] == sha(final_inventory.read_bytes())
    expected = set(json.loads((PACKET / "changed-file-inventory-002.json").read_text(encoding="utf8"))["paths"])
    git("add", "--sparse", "--", *sorted(expected))
    assert set(git("diff", "--cached", "--name-only", PARENT).decode().splitlines()) == expected
    assert not git("diff", "--name-only") and not git("ls-files", "--others", "--exclude-standard")
    whitespace = check_patch_whitespace(guard)
    for path in expected:
        assert git("show", ":" + path) == (REPO / path).read_bytes(), path
    write(HERE / "staging-002.json", {
        "parent": PARENT, "tree": git("write-tree").decode().strip(),
        "paths": sorted(expected), "rawSha256": {p: sha((REPO / p).read_bytes()) for p in expected},
        "inventorySha256": sha(final_inventory.read_bytes()), "whitespace": whitespace,
        "authorGatesSummarySha256": sha((HERE / "author-gates-002" / "summary.json").read_bytes()),
        "authorPreservationSummarySha256": sha((HERE / "author-preservation-002" / "summary.json").read_bytes()),
        "predecessorPreflight": "No GPG/commit process was launched; the preserved failure was a unified-diff context-space check.",
    })
    name = git("show", "-s", "--format=%an", PARENT).decode().strip()
    assert name == "Roman Konstantinovskiy"
    assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
    assert git("config", "user.signingkey").decode().strip() == FINGERPRINT
    assert git("remote", "get-url", "origin").decode().strip().removesuffix(".git") == "https://github.com/stop-cran/learning-japanese"
    message = ("Reconcile B129 finite meaning-guard review\n\n"
               "Bind all 28 pair dispositions, complete sources and separate reviewer responses.\n"
               "Preserve frozen B129 evidence, including the pre-sign patch-syntax whitespace failure.\n\n"
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
    write(HERE / "actual-signing-stdout-001.log", stdout)
    write(HERE / "actual-signing-stderr-001.log", stderr)
    write(attempt, {"parent": PARENT, "stalled": stalled,
                    "exitCode": process.returncode if process else None,
                    "stdoutSha256": sha(stdout), "stderrSha256": sha(stderr), "memory": memory,
                    "maximumSigningWaitSeconds": 30, "fingerprint": FINGERPRINT,
                    "policy": "One actual GPG signing attempt; the initial preserved preflight never launched GPG. On popup stall preserve staged work and yield without retry or bypass."})
print(stdout.decode("utf8", "replace"), end="")
print(stderr.decode("utf8", "replace"), end="", file=sys.stderr)
if stalled:
    raise SystemExit("Signing stalled. Yield without retry.")
if process.returncode:
    raise SystemExit(process.returncode)
assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
print("Signed direct child:", git("rev-parse", "HEAD").decode().strip())
