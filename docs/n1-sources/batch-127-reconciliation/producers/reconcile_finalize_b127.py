import json
from pathlib import Path
from b127_common import HERE, REPO, git, sha, start_guard, write
from reconcile_sources_b127 import OUT, PARENT

guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    gates = HERE / "reconciliation-author-gates-001"
    summary = json.loads((gates / "summary.json").read_text(encoding="utf-8"))
    assert summary["status"] == "PASS" and summary["parent"] == PARENT
    assert len(summary["checks"]) == 10
    for path in sorted(gates.iterdir()):
        guard.check()
        if path.is_file():
            write(OUT / "author-gates-001" / path.name, path.read_bytes())
    for path in sorted((HERE / "reconciliation-author-failure-001").iterdir()):
        write(OUT / "failed-author-producer-001" / path.name, path.read_bytes())
    for path in [
        HERE / "reconciliation-sources-001" / "memory.json",
        HERE / "reconciliation-author-002-memory.json",
        HERE / "reconciliation-failure-preservation-memory-001.json",
    ]:
        name = path.parent.name + "-memory.json" if path.name == "memory.json" else path.name
        write(OUT / "author-memory" / name, path.read_bytes())
    for name in [
        "reconcile_gates_b127.py", "reconcile_finalize_b127.py",
        "reconcile_preserve_b127.py", "reconcile_commit_b127.py",
        "reconcile_handoff_b127.py", "reconcile_preserve_failure_b127.py",
    ]:
        write(OUT / "producers" / name, (HERE / name).read_bytes())
    write(OUT / "progress-seed-002.json", (REPO / "docs" / "n1-sources" / "batch-127-progress-002.json").read_bytes())
    manifest = json.loads((REPO / "manifest.json").read_bytes())
    write(OUT / "author-evidence.json", {
        "batch": "127", "revision": "reconciliation-001", "parent": PARENT,
        "authorGates": {"status": "PASS", "directory": "author-gates-001", "summarySha256": sha((gates / "summary.json").read_bytes()), "checks": summary["checks"]},
        "runtime": {"manifestSha256": sha((REPO / "manifest.json").read_bytes()), "contentVersion": manifest["contentVersion"], "entries": sum(len(v) for v in manifest.values() if isinstance(v, dict))},
        "warnings": {"lint": "0 error(s), 0 warning(s)", "quizSafety": "0 error(s), 0 warning(s)", "unittest": "431 tests pass; HTTP 429/retry output is fixture output", "vocabulary": "PASS, existing pilot coverage 2122/2431, not full closure"},
        "preservedFailures": [{"directory": "failed-author-producer-001", "cause": "Raw CRLF text was not normalized before an anchored metadata regex; corrected to LF normalization. No original evidence overwritten."}],
        "sourceReceiptSha256": sha((OUT / "source-receipt.json").read_bytes()),
        "pairDispositionsSha256": sha((OUT / "pair-dispositions.json").read_bytes()),
        "historyInventorySha256": sha((OUT / "preserved-history.json").read_bytes()),
        "familyResponses": {name: sha((OUT / name).read_bytes()) for name in ["claude-author-response.md", "gpt-author-response.md"]},
        "resourcePolicy": {"serial": True, "admitAboveBytes": 2 * 1024**3, "abortBelowBytes": 1024**3, "sampleSeconds": 0.25, "childWaitAtMostSeconds": 0.1, "cleanupDeadlineSecondsPerStage": 10, "scope": "Immediate child PID cleanup, not descendant-process acceptance."},
        "committedChecks": "Bound separately in scratch after signing, not claimed in advance.",
        "accounting": {"delivered": 256, "remaining": 972, "revisedUnconfirmedLocalDrafts": 1, "publication": False},
    })
    files = {}
    for path in sorted(OUT.rglob("*")):
        guard.check()
        if path.is_file():
            raw = path.read_bytes()
            files[path.relative_to(OUT).as_posix()] = {"sha256": sha(raw), "bytes": len(raw)}
    write(OUT / "packet-files.json", {"parent": PARENT, "files": files, "selfExcluded": True, "rawBytesNoLineEndingNormalization": True})
    print(json.dumps({"packetFilesIncludingInventory": len(files) + 1, "authorGateSummarySha256": sha((gates / "summary.json").read_bytes()), "inventorySha256": sha((OUT / "packet-files.json").read_bytes())}))
finally:
    write(HERE / "reconciliation-finalize-001-memory.json", guard.finish())
