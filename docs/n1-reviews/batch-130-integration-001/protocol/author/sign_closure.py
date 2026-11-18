import json
from pathlib import Path
from closure_common import *

guard = start_guard()
try:
    head, tree = mode_tree("author")
    gates = load(HERE / "author-gates-001" / "summary.json")
    proof = load(HERE / "author-preserve-001" / "summary.json")
    require(gates["status"] == proof["status"] == "PASS" and gates["tree"] == proof["tree"] == tree,
            "Successful author gates/preservation do not bind current tree")
    reviewed = load(HERE / "staged-review-001" / "summary.json")
    require(reviewed["status"] == "PASS" and reviewed["tree"] == tree, "Missing exact staged review")
    for role in ("AUTHOR", "COMMITTER"):
        require(git("var", "GIT_" + role + "_IDENT").decode().startswith(
            "Roman Konstantinovskiy <stop-cran@list.ru> "), "Owner identity differs")
    require(git("config", "--get", "user.signingkey").decode().strip() == FINGERPRINT, "Signing key differs")
    message = (
        "Archive B130 integrated-snapshot review closure\n\n"
        "Retain the previous closure and ledger values unchanged; append the\n"
        "accepted integration-impact lineage and bounded contributor evidence.\n"
        "Runtime payload and manifest remain byte-identical. Publication pending.\n\n"
        "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
    )
    code, stalled, stdout, stderr = command(
        ["git", "-c", "core.quotepath=false", "commit", "-S" + FINGERPRINT, "-m", message],
        HERE / "signing-001", guard, timeout=60)
    result = {
        "status": "SIGNING-STALLED-NO-RETRY" if stalled else ("SIGNED" if code == 0 else "SIGNING-FAILED-NO-RETRY"),
        "head": git("rev-parse", "HEAD").decode().strip(), "parent": PARENT, "tree": tree,
        "exitCode": code, "attempt": 1, "noRetryOrBypass": True,
        "producerSha256": sha(raw(Path(__file__))),
    }
    write(HERE / "signing-001" / "summary.json", result)
    print(json.dumps(result))
    if stalled or code:
        raise SystemExit(42)
    require(mode_tree("committed")[1] == tree, "Signed tree changed")
    signature(result["head"])
finally:
    if (HERE / "signing-001").exists():
        write(HERE / "signing-001" / "memory.json", guard.finish())
    else:
        write(HERE / "signing-admission-memory-001.json", guard.finish())
