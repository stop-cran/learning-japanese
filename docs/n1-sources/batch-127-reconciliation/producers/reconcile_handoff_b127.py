import json
from pathlib import Path
from b127_common import HERE, REPO, git, sha, start_guard, write
from reconcile_sources_b127 import OUT, PARENT

out = HERE / "reconciliation-handoff-001"
assert not out.exists()
out.mkdir()
guard = start_guard()
try:
    candidate = git("rev-parse", "HEAD").decode().strip()
    assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    verification = git("verify-commit", "--raw", "HEAD", include_stderr=True)
    write(out / "verify-commit.log", verification)
    fields = git("show", "-s", "--format=%an%n%ae%n%cn%n%ce%n%G?%n%GF%n%GP", "HEAD").decode("utf-8").splitlines()
    base_name = git("show", "-s", "--format=%an", PARENT).decode("utf-8").strip()
    assert fields[:4] == [base_name, "stop-cran@list.ru", base_name, "stop-cran@list.ru"]
    assert fields[4] == "G"
    assert fields[5:] == ["D4C9A275A218AF747B787AFA9D94B9D311BD26A7"] * 2
    assert "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in git("show", "-s", "--format=%B", "HEAD").decode("utf-8").splitlines()
    bindings = {}
    for label, directory in [
        ("authorGates", "reconciliation-author-gates-001"),
        ("authorPreservation", "reconciliation-preservation-author-001"),
        ("committedGates", "reconciliation-committed-gates-001"),
        ("committedPreservation", "reconciliation-preservation-committed-001"),
    ]:
        path = HERE / directory / "summary.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["status"] == "PASS" and data["parent"] == PARENT
        if label == "committedGates":
            assert data["startingHead"] == candidate
        if label == "committedPreservation":
            assert data["head"] == candidate
        bindings[label] = {"directory": str(path.parent), "summarySha256": sha(path.read_bytes())}
    preservation = json.loads((HERE / "reconciliation-preservation-committed-001" / "summary.json").read_text(encoding="utf-8"))
    manifest_raw = (REPO / "manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    files = []
    for rel in preservation["changedFiles"]:
        guard.check()
        path = REPO / rel
        raw = path.read_bytes()
        assert raw == git("show", f"HEAD:{rel}")
        files.append({"path": rel, "sha256": sha(raw), "bytes": len(raw)})
    write(out / "changed-files.json", {"candidate": candidate, "parent": PARENT, "files": files})
    for label, filename in [
        ("sourceReceipt", "source-receipt.json"), ("fullSelectorBindings", "source-receipt.json"),
        ("finiteDispositionTable", "pair-dispositions.json"), ("preservedHistory", "preserved-history.json"),
        ("packetInventory", "packet-files.json"), ("claudeResponse", "claude-author-response.md"),
        ("gptResponse", "gpt-author-response.md"), ("authorAudit", "author-audit.md"),
    ]:
        path = OUT / filename
        bindings[label] = {"path": str(path), "sha256": sha(path.read_bytes())}
    flat = {p: v for group in manifest.values() if isinstance(group, dict) for p, v in group.items()}
    handoff = {
        "batch": "127", "revision": "reconciliation-001", "candidate": candidate, "parent": PARENT,
        "publishedBase": "dd45f6fb7cd3ce579422e2333860aa6d245af898", "cleanDirectChild": True,
        "worktree": str(REPO), "membership": [{"kanji": "倉", "sourceRow": 57}],
        "identity": {"author": fields[0] + " <" + fields[1] + ">", "committer": fields[2] + " <" + fields[3] + ">", "signatureStatus": fields[4], "signingFingerprint": fields[5], "primaryFingerprint": fields[6], "verifyCommitExitCode": 0, "verifyLogSha256": sha(verification)},
        "changedFileInventory": {"path": str(out / "changed-files.json"), "sha256": sha((out / "changed-files.json").read_bytes()), "count": len(files)},
        "bindings": bindings,
        "runtime": {"manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"], "entries": len(flat), "kanjiCards": sum(p.startswith("kanji/") for p in flat), "wordArticles": sum(p.startswith("words/") for p in flat), "strokeFiles": sum(p.startswith("strokes/") for p in flat), "changed": ["kanji/倉.md"], "added": [], "removed": [], "unchangedEntries": 8715},
        "semanticOutcome": {"F1": "Direct 倉/止 and 倉/停 guards and qualified standalone cancellation attribution implemented.", "Q1toQ13": "Every row has both offered directions, complete relevant records, exact endpoint status and citations.", "conservativeGuardIds": ["Q1", "Q2", "Q3", "Q4", "Q5", "Q7", "Q9", "Q10", "Q11"], "sourceSupportedGuardIds": ["Q8", "Q12", "Q13"], "distinctNoGuardIds": ["Q6"], "unguardedOpenIds": [], "guardedUncertainty": "Conservative rows retain unresolved broad-choice/historical linguistic boundaries; safety guards do not assert synonymy or independent confirmation."},
        "preservation": {"originalHistoricalFiles": 189, "oldGuards": 11, "totalGuards": 23, "curatedChoices": ["金", "全", "合"], "fullReadings": {"onyomi": ["ソウ"], "kunyomi": ["くら"]}, "practice": {"quizOnyomi": ["ソウ"], "quizKunyomi": []}, "supportWordAndStrokeByteIdenticalToParent": True},
        "accounting": {"delivered": 256, "remaining": 972, "revisedUnconfirmedLocalDrafts": 1, "published": False},
        "preservedFailure": "Initial reconciliation author producer failed its CRLF-anchored regex before evidence writes; original producer and receipt retained in failed-author-producer-001. Corrected LF normalization succeeded.",
        "limits": [
            "No independent successor confirmation, push, publication, served-GitHub-ZIP, whole-set linguistic or delivery acceptance.",
            "Conservative guarded ambiguities are bounded dispositions, not fabricated clean linguistic resolution; unread candidates remain limits.",
            "Host model is not arbitrary/custom/multiple-borrow, Kotlin/native/device or older APK acceptance.",
            "Contrast-only 宀 lacks all three bundled cmap subsets; fallback rendering remains unverified. Geometry/stroke bytes unchanged.",
            "Vocabulary coverage remains existing pilot 2122/2431; no full closure.",
            "All original evidence and coordinator-owned review records preserved; no reviewer contacted.",
        ],
        "producerSha256": sha(Path(__file__).read_bytes()),
    }
    write(out / "handoff.json", handoff)
    print(json.dumps({"candidate": candidate, "parent": PARENT, "handoff": str(out / "handoff.json"), "handoffSha256": sha((out / "handoff.json").read_bytes()), "bindings": bindings, "runtime": handoff["runtime"], "identity": handoff["identity"]}, ensure_ascii=False))
finally:
    write(out / "memory.json", guard.finish())
