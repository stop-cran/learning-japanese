import json
from pathlib import Path
from b130_common import BASE, GUARD_SHA, HERE, PACKET, REPO, ROOT, sha, start_guard, write

OUT = REPO / "docs" / "n1-sources" / "batch-130-reconciliation"
PARENT = "ce1b5c895fac90852143f322a115c2de4e768e20"
PRODUCERS = (
    "reconcile_sources_b130.py", "reconcile_external_b130.py", "reconcile_decisions_b130.py",
    "reconcile_responses_b130.py", "run_b130_reconciliation_gates.py",
    "preserve_b130_reconciliation.py", "package_b130_reconciliation.py",
)

guard = start_guard()
try:
    directory = HERE / "reconciliation-author-gates-001"
    gates = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
    assert gates["status"] == "PASS"
    manifest_raw = (REPO / "manifest.json").read_bytes()
    assert sha(manifest_raw) == gates["manifestSha256"]
    manifest = json.loads(manifest_raw)
    reading = (directory / "reading-exposure.log").read_text(encoding="utf-8")
    assert "0 production hit(s)" in reading and "0 padded-session hit(s)" in reading
    warnings = [line for line in (directory / "quiz-safety.log").read_text(encoding="utf-8").splitlines() if line.startswith("WARN")]
    pairs = json.loads((OUT / "pair-dispositions-001.json").read_text(encoding="utf-8"))
    for path in directory.iterdir():
        if path.is_file():
            write(OUT / "author-evidence" / directory.name / path.name, path.read_bytes())
    for name in PRODUCERS:
        write(OUT / "producers" / name, (HERE / name).read_bytes())
    for path in (HERE / "reconciliation-001").rglob("*memory*.json"):
        write(OUT / "author-evidence" / path.name, path.read_bytes())
    dependencies = ("b130_common.py", "survey_b130.py", "run_b130_gates.py", "check_reading_b130.py")
    write(OUT / "tool-bindings.json", {
        "dependencies": {name: {"scratchPath": str(HERE / name), "sha256": sha((HERE / name).read_bytes()),
                                 "immutableOriginalProducer": "batch-130/producers/" + name}
                         for name in dependencies},
        "leanTools": {name: sha((ROOT / "lean" / name).read_bytes()) for name in
                      ("n1lib.py", "n1_batch_tool.py", "quiz_safety.py", "n1_linkplan.py", "reading_exposure.py", "reading_options.py")},
        "environment": {"N1_REPO": str(REPO), "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1", "pythonFlag": "-B"},
        "guardSha256": GUARD_SHA, "policy": ">2GiB admission; 0.25s sampling; abort <1GiB; own-child waits <=0.1s, terminate/kill <=10s each.",
        "toolingChange": "A new outer gate runner and preservation verifier admit the actual signed parent and retain all 24 historical initial open IDs with explicit source-backed mappings. The old empty-initial-open-IDs assumption is not used. Original gate commands keep published-base lint/link/payload scope.",
        "executionContext": "Producer copies preserve exact scratch implementations/bindings; they depend on the bound scratch layout and are not advertised as standalone relocatable scripts.",
    })
    inventory = {p.relative_to(OUT).as_posix(): sha(p.read_bytes()) for p in sorted(OUT.rglob("*")) if p.is_file()}
    write(OUT / "evidence-inventory.json", {
        "files": inventory, "selfExcluded": True, "producerSha256": sha(Path(__file__).read_bytes()),
        "scope": "New reconciliation packet only. Original batch-130 packet is unchanged; final signed candidate and committed gates are bound in local handoff/preservation receipts to avoid a self-referential commit.",
    })
    write(REPO / "docs" / "n1-sources" / "batch-130-progress-reconciliation-001.json", {
        "batch": 130, "revision": "reconciliation-001", "status": "local-author-successor-awaiting-independent-confirmation",
        "parent": PARENT, "publishedBase": BASE, "members": ["塀", "拍", "耗"], "sourceRows": [191, 419, 879],
        "publishedDelivered": 261, "frozenTotal": 1228, "undelivered": 967,
        "localUnpublishedDrafts": 3, "deliveryNotIncremented": True,
        "supports": [["塀", "塀", 3], ["拍", "拍手", 3], ["耗", "消耗", 2]],
        "supportWordChangesFromParent": [], "metadataPracticeCurationGeometryChanges": [],
        "newGuards": {ch: [row["pair"][1] for row in pairs["rows"] if row["pair"][0] == ch
                           and row["decision"] != "bounded-noncollision"] for ch in ("塀", "拍", "耗")},
        "neutralPairs": "batch-130-reconciliation/pair-dispositions-001.json",
        "completeSourceCounts": {"jmdict": 99, "kanjidic2": 31, "comparisonCards": 28},
        "familyIsolatedResponses": ["batch-130-reconciliation/responses/claude-response-001.md",
                                   "batch-130-reconciliation/responses/gpt-response-001.md"],
        "historicalOpenQuestionsPreserved": 24, "authorOpenQuizHolds": [],
        "historicalAndRareSpellingAllocationResolved": False,
        "authorGates": {"directory": str(directory), "summarySha256": sha((directory / "summary.json").read_bytes()),
                        "checks": gates["checks"], "serial": True},
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "newEvidenceInventorySha256": sha((OUT / "evidence-inventory.json").read_bytes()),
        "originalEvidenceInventorySha256": sha((PACKET / "evidence-inventory.json").read_bytes()),
        "warnings": {"quizSafetyCount": len(warnings), "quizSafetyWarnings": warnings,
                     "reading": "0 production/0 padded hits in bounded pools; latent 拍ひゃく and 耗ぼう remain outside drawable tested pools, not universal zero exposure.",
                     "font": "Original cmap absence of 尸/并/扌/耒 retained; no rendered fallback or visual/native acceptance."},
        "boundary": "One local owner-signed direct child of the initial candidate is required; exact signed identity and all committed gates/preservation are in local handoff evidence. No reviewer contact, independent confirmation, push, publication, delivery credit or next batch.",
    })
    print(json.dumps({"newPacketBoundFiles": len(inventory), "warningCount": len(warnings),
                      "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"]}, ensure_ascii=False))
finally:
    write(HERE / "reconciliation-001" / "packaging-memory-001.json", guard.finish())
