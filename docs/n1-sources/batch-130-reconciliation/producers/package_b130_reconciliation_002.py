import json
from pathlib import Path
from b130_common import HERE, REPO, sha, start_guard, write

OUT = REPO / "docs" / "n1-sources" / "batch-130-reconciliation"
guard = start_guard()
try:
    directory = HERE / "reconciliation-author-gates-002"
    gates = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
    assert gates["status"] == "PASS"
    manifest_raw = (REPO / "manifest.json").read_bytes()
    assert sha(manifest_raw) == gates["manifestSha256"]
    manifest = json.loads(manifest_raw)
    original = json.loads((OUT / "evidence-inventory.json").read_text(encoding="utf-8"))
    for name, digest in original["files"].items():
        assert sha((OUT / name).read_bytes()) == digest, name
    for path in directory.iterdir():
        if path.is_file():
            write(OUT / "author-evidence" / directory.name / path.name, path.read_bytes())
    for path in (HERE / "reconciliation-author-preserve-001").iterdir():
        if path.is_file():
            write(OUT / "author-evidence" / "reconciliation-author-preserve-001" / path.name, path.read_bytes())
    write(OUT / "author-evidence" / "packaging-memory-001.json",
          (HERE / "reconciliation-001" / "packaging-memory-001.json").read_bytes())
    write(OUT / "producers" / "preserve_b130_reconciliation_002.py",
          (HERE / "preserve_b130_reconciliation.py").read_bytes())
    write(OUT / "producers" / Path(__file__).name, Path(__file__).read_bytes())
    write(OUT / "history-002.json", {
        "reason": "Final self-inspection corrected sentence capitalization and made a curated-card pronoun explicit in 耗. Full ten-gate run repeated on the changed runtime; the earlier successful run and full evidence remain immutable, not relabelled as the final snapshot.",
        "activeAuthorGates": directory.name, "historicalAuthorGates": "reconciliation-author-gates-001",
        "historicalPreservation": "reconciliation-author-preserve-001",
        "activePreservationProducer": "producers/preserve_b130_reconciliation_002.py",
        "originalPreservationProducer": "producers/preserve_b130_reconciliation.py",
        "scratchProducerVersioning": "The original exact preservation producer remains in the first immutable packet inventory; the revised scratch implementation is copied under an explicit -002 identity.",
        "activeProgress": "batch-130-progress-reconciliation-002.json",
        "historicalProgress": "batch-130-progress-reconciliation-001.json",
        "neutralSourceAndPairEvidence": "Unchanged; no source/semantic disposition or isolated response was rewritten.",
    })
    inventory = {p.relative_to(OUT).as_posix(): sha(p.read_bytes()) for p in sorted(OUT.rglob("*")) if p.is_file()}
    write(OUT / "evidence-inventory-002.json", {
        "files": inventory, "selfExcluded": True, "producerSha256": sha(Path(__file__).read_bytes()),
        "supersedesInventoryAsActiveBindingOnly": "evidence-inventory.json",
        "scope": "Additive final packet binding; the first inventory and all files it bound remain byte-identical. Signed identity and committed checks stay in local handoff receipts.",
    })
    progress = json.loads((REPO / "docs" / "n1-sources" / "batch-130-progress-reconciliation-001.json").read_text(encoding="utf-8"))
    progress["record"] = "002"
    progress["supersededRecordPreserved"] = "batch-130-progress-reconciliation-001.json"
    progress["authorGates"] = {
        "directory": str(directory), "summarySha256": sha((directory / "summary.json").read_bytes()),
        "checks": gates["checks"], "serial": True,
    }
    progress["manifestSha256"] = sha(manifest_raw)
    progress["contentVersion"] = manifest["contentVersion"]
    progress["newEvidenceInventorySha256"] = sha((OUT / "evidence-inventory-002.json").read_bytes())
    progress["activeNewEvidenceInventory"] = "batch-130-reconciliation/evidence-inventory-002.json"
    warnings = [line for line in (directory / "quiz-safety.log").read_text(encoding="utf-8").splitlines() if line.startswith("WARN")]
    progress["warnings"]["quizSafetyCount"] = len(warnings)
    progress["warnings"]["quizSafetyWarnings"] = warnings
    write(REPO / "docs" / "n1-sources" / "batch-130-progress-reconciliation-002.json", progress)
    print(json.dumps({"boundFiles": len(inventory), "manifestSha256": sha(manifest_raw),
                      "contentVersion": manifest["contentVersion"], "warningCount": len(warnings)}))
finally:
    write(HERE / "reconciliation-001" / "packaging-memory-002.json", guard.finish())
