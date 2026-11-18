import json
from b128_common import BASE, GUARD_SHA, HERE, PACKET, REPO, git, sha, start_guard, write

out = HERE / "handoff-001"
assert not out.exists()
out.mkdir()
guard = start_guard()
try:
    head = git("rev-parse", "HEAD").decode().strip()
    assert git("rev-parse", "HEAD^@").decode().split() == [BASE]
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    verification = git("verify-commit", "--raw", head, include_stderr=True)
    write(out / "verify-commit.log", verification)
    signature = git("show", "-s", "--format=%H%n%P%n%an%n%ae%n%cn%n%ce%n%G?%n%GF%n%GP%n%B", head).decode("utf-8")
    lines = signature.splitlines()
    owner_name = git("show", "-s", "--format=%an", BASE).decode("utf-8").strip()
    assert lines[:6] == [head, BASE, owner_name, "stop-cran@list.ru", owner_name, "stop-cran@list.ru"]
    assert lines[6] in ("G", "U") and "D4C9A275A218AF747B787AFA9D94B9D311BD26A7" in lines[7:9]
    assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in signature
    write(out / "identity-signature.log", signature.encode())
    inventory = json.loads((PACKET / "packet-files.json").read_text(encoding="utf-8"))
    for path, info in inventory["files"].items():
        guard.check()
        assert sha((PACKET / path).read_bytes()) == info["sha256"], path
    gates_path = HERE / "committed-gates-001" / "summary.json"
    gates = json.loads(gates_path.read_text(encoding="utf-8"))
    preservation_path = HERE / "preservation-committed-001" / "summary.json"
    preservation = json.loads(preservation_path.read_text(encoding="utf-8"))
    assert gates["status"] == preservation["status"] == "PASS"
    assert gates["startingHead"] == preservation["head"] == head
    assert gates["manifestSha256"] == preservation["manifestSha256"] == sha(git("show", "HEAD:manifest.json"))
    bindings = {}
    for relative in (
        "source-row.json", "selection.json", "source-receipt.json",
        "jmdict-selected-records.xml", "jmdict-comparison-records.xml",
        "kanjidic2-selected-records.xml", "kanjidic2-comparison-records.xml",
        "kanjidic2-expanded-comparison-records.xml", "baseline-gloss-scan.json",
        "baseline-gloss-scan-002.json", "pair-dispositions.json", "support-audit.json",
        "external-source-bindings.json", "stroke-font-evidence.json",
        "complete-source-verification-002.json", "author-evidence.json",
        "packet-files.json", "author-audit.md", "stale-remarks.json",
    ):
        raw = (PACKET / relative).read_bytes()
        bindings[relative] = {"sha256": sha(raw), "bytes": len(raw)}
    manifest = json.loads(git("show", "HEAD:manifest.json"))
    result = {
        "batch": "128", "status": "clean-owner-signed-local-authoring-candidate",
        "candidate": head, "base": BASE, "directChild": True, "clean": True,
        "worktree": str(REPO), "sourceRows": [{"sourceRow": 159, "kanji": "唇", "codePoint": "U+5507"}],
        "supportArticles": [{"path": "words/唇.md", "reading": "くちびる", "levelPreserved": 2}],
        "requiredReciprocalPairs": [["唇", "唇"]], "newWords": 0,
        "runtimeChanges": {"added": preservation["added"], "changed": preservation["changed"], "removed": [], "wordDetail": "One reciprocal wrapper plus removal of exactly the now-false no-card sentence."},
        "contributorChanges": ["docs/n1-authoring-notes.md", "docs/n1-sources/batch-128-progress.json", "docs/n1-sources/batch-128/"],
        "packet": str(PACKET), "bindings": bindings,
        "sourceInputHashes": json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))["dictionaryInputs"],
        "gates": {"directory": str(gates_path.parent), "summarySha256": sha(gates_path.read_bytes()), "checks": gates["checks"], "manifestReproducible": True},
        "baselinePreservation": {"directory": str(preservation_path.parent), "summarySha256": sha(preservation_path.read_bytes()), "baselineUnchangedEntries": preservation["baselineUnchangedRuntimeEntries"], "checkedRuntimeEntries": preservation["allCandidateRuntimeHashesChecked"]},
        "manifestSha256": gates["manifestSha256"], "contentVersion": manifest["contentVersion"],
        "identity": {"author": f"{lines[2]} <stop-cran@list.ru>", "committer": f"{lines[4]} <stop-cran@list.ru>", "displayNamePreservedFromSignedBase": True, "signatureStatus": lines[6], "signingFingerprint": lines[7], "primaryFingerprint": lines[8], "verifyCommitExitCode": 0},
        "resourcePolicy": {"guardSha256": GUARD_SHA, "admitAboveBytes": 2147483648, "abortBelowBytes": 1073741824, "sampleSeconds": 0.25, "maxChildWaitSeconds": 0.1, "cleanupTimeoutSecondsPerStage": 10},
        "warnings": ["No final scoped lint or quiz-safety warnings.", "Initial linkplan failure and one quiz-safety Notes warning preserved; no validator weakened.", "脣 U+8123 lacks all bundled cmaps; no rendered fallback/native/device acceptance.", "Two latent hypothetical reading-pool collisions; zero production/restricted-Starter hits.", "Vocabulary coverage remains pilot-stage 2122/2431; unittest HTTP429/retry output is fixture behavior."],
        "limits": ["Unreviewed and unpublished; no push, reviewer launch or next batch.", "Bounded N1/All/restricted Starter host reading model, not arbitrary/custom/multiple-borrow or Kotlin/native/device acceptance.", "Conservative broad-label direct guards, not universal synonymy or whole-set semantic certification."],
        "publishedAccountingUnchanged": {"delivered": 257, "remaining": 971, "localDrafts": 1},
    }
    write(out / "handoff.json", result)
    print(json.dumps({"candidate": head, "base": BASE, "handoff": str(out / "handoff.json"), "handoffSha256": sha((out / "handoff.json").read_bytes()), "gateSummarySha256": sha(gates_path.read_bytes()), "preservationSummarySha256": sha(preservation_path.read_bytes()), "manifestSha256": gates["manifestSha256"], "contentVersion": manifest["contentVersion"], "identity": result["identity"]}, ensure_ascii=False))
finally:
    write(out / "memory.json", guard.finish())
