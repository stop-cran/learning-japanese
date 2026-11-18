import json
import sys
from pathlib import Path
from integration_common import DELTA, FINGERPRINT, FIRST, HERE, REPO, SECOND, command, git, live_target, load, parents, sha, start_guard, write

guard = start_guard()
try:
    parents("author")
    live_target()
    preservation = load(HERE / "author-preserve-001" / "summary.json")
    gates = load(HERE / "author-gates-001" / "summary.json")
    assert preservation["status"] == gates["status"] == "PASS"
    assert preservation["tree"] == gates["tree"] == git("write-tree").decode().strip()
    assert preservation["manifestSha256"] == gates["manifestSha256"]
    assert set(git("diff", "--cached", "--name-only", FIRST).decode().splitlines()) == DELTA
    git("-c", "core.whitespace=cr-at-eol", "diff", "--cached", "--check")
    for role in ("AUTHOR", "COMMITTER"):
        assert git("var", "GIT_" + role + "_IDENT").decode().startswith(
            "Roman Konstantinovskiy <stop-cran@list.ru> ")
    assert git("config", "--get", "user.signingkey").decode().strip() == FINGERPRINT
    message = (
        "Merge B130 closure with the age-counter fix\n\n"
        "Retain both signed histories and incoming counter content unchanged.\n"
        "Resolve only the generated manifest through the existing generator.\n"
        "Local author integration evidence only; no publication credit.\n\n"
        "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
    )
    code, stalled, stdout, stderr = command(
        ["git", "-c", "core.quotepath=false", "commit", "-S" + FINGERPRINT, "-m", message],
        HERE / "signing-001", guard, timeout=60)
    result = {
        "status": "SIGNING-STALLED-NO-RETRY" if stalled else ("SIGNED" if code == 0 else "SIGNING-FAILED-NO-RETRY"),
        "parentsInOrder": [FIRST, SECOND], "head": git("rev-parse", "HEAD").decode().strip(),
        "tree": preservation["tree"], "exitCode": code, "attempt": 1, "noRetryOrBypass": True,
        "producerSha256": sha(Path(__file__).read_bytes()),
    }
    write(HERE / "signing-001" / "summary.json", result)
    print(json.dumps(result))
    if stalled or code:
        raise SystemExit(42)
    parents("committed")
finally:
    write(HERE / "signing-001" / "memory.json", guard.finish())
