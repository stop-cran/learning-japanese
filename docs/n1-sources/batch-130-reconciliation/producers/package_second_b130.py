import json
from pathlib import Path
from b130_common import BASE, HERE, REPO, ROOT, sha, start_guard, write

OUT = REPO / "docs" / "n1-sources" / "batch-130-reconciliation"
PARENT = "d440617274eef6ea7611e60f147d6483f29ca710"
guard = start_guard()
try:
    directory = HERE / "reconciliation-002-author-gates-001"
    gates = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
    assert gates["status"] == "PASS" and gates["parent"] == PARENT
    manifest_raw = (REPO / "manifest.json").read_bytes()
    assert sha(manifest_raw) == gates["manifestSha256"]
    manifest = json.loads(manifest_raw)
    original = json.loads((OUT / "evidence-inventory-002.json").read_text(encoding="utf-8"))
    for name, digest in original["files"].items():
        assert sha((OUT / name).read_bytes()) == digest, name
    tools = json.loads((OUT / "tool-bindings.json").read_text(encoding="utf-8"))
    for name, binding in tools["dependencies"].items():
        assert sha(Path(binding["scratchPath"]).read_bytes()) == binding["sha256"], name
    for name, digest in tools["leanTools"].items():
        assert sha((ROOT / "lean" / name).read_bytes()) == digest, name
    for path in directory.iterdir():
        if path.is_file():
            write(OUT / "author-evidence" / "second-002" / directory.name / path.name, path.read_bytes())
    for path in (HERE / "reconciliation-002-source-read-001").iterdir():
        if path.is_file():
            write(OUT / "author-evidence" / "second-002" / "source-read" / path.name, path.read_bytes())
    producers = ("reconcile_second_b130.py", "run_b130_second_gates.py", "preserve_second_b130.py", "package_second_b130.py")
    for name in producers:
        write(OUT / "producers" / name, (HERE / name).read_bytes())
    write(OUT / "second-002-tool-bindings.json", {
        "parent": PARENT, "originalImplementationBindings": {
            "path": "tool-bindings.json", "sha256": sha((OUT / "tool-bindings.json").read_bytes())},
        "newProducers": {name: sha((HERE / name).read_bytes()) for name in producers},
        "outerChangeOnly": "Parent/closure and exact two-file runtime delta are checked separately; original ten gate commands, dependency and lean-tool hashes are unchanged.",
        "resourcePolicy": ">2GiB admission; <1GiB abort; 0.25s sampling; own-child waits <=0.1s and bounded terminate/kill <=10s each.",
        "sourcePolicy": "Existing complete records only; no new query, survey or refetch.",
    })
    inventory = {path.relative_to(OUT).as_posix(): sha(path.read_bytes())
                 for path in sorted(OUT.rglob("*")) if path.is_file()}
    write(OUT / "evidence-inventory-003.json", {
        "parent": PARENT, "files": inventory, "selfExcluded": True,
        "previousInventory": {"path": "evidence-inventory-002.json",
                              "sha256": sha((OUT / "evidence-inventory-002.json").read_bytes())},
        "scope": "Additive reconciliation-002 packet binding. All prior inventories/files stay byte-identical; signed identity and committed checks are local handoff receipts.",
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
    warnings = [line for line in (directory / "quiz-safety.log").read_text(encoding="utf-8").splitlines() if line.startswith("WARN")]
    previous_progress = json.loads((REPO / "docs" / "n1-sources" / "batch-130-progress-reconciliation-002.json").read_text(encoding="utf-8"))
    write(REPO / "docs" / "n1-sources" / "batch-130-progress-reconciliation-003.json", {
        "batch": 130, "revision": "reconciliation-002", "record": "003", "parent": PARENT,
        "publishedBase": BASE, "status": "unpublished-author-proposal-awaiting-two-independent-confirmations",
        "publishedDelivered": 261, "frozenTotal": 1228, "undelivered": 967,
        "localUnpublishedDrafts": 3, "deliveryCredit": 0,
        "previousProgressPreserved": "batch-130-progress-reconciliation-002.json",
        "runtimeDelta": ["kanji/拍.md", "manifest.json"],
        "change": "Append direct 響 precaution on 拍 and minimally qualify unresolved effect/impression allocation. Not an ordinary synonym or newly proven collision.",
        "preserved": "All other runtime, prior guards/order, metadata, practices, curation, supports/easier levels/wrappers, geometry, evidence, inventories, responses, progress and earlier notes.",
        "neutralPairs": "batch-130-reconciliation/pair-dispositions-002.json",
        "counts": {"guard": 8, "precaution": 17, "bounded-noncollision": 3},
        "boundedNoncollisions": ["耗/文", "耗/研", "耗/書"],
        "historicalOriginalQuestionsPreserved": 24, "lexicalAllocationResolved": False,
        "unprotectedAuthorQuizHolds": [], "sourceReuse": "batch-130-reconciliation/source-reuse-002.json",
        "familyIsolatedResponses": ["batch-130-reconciliation/responses/claude-response-002.md",
                                   "batch-130-reconciliation/responses/gpt-response-002.md"],
        "authorGates": {"directory": str(directory), "summarySha256": sha((directory / "summary.json").read_bytes()),
                        "checks": gates["checks"], "serial": True},
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "packetInventory": "batch-130-reconciliation/evidence-inventory-003.json",
        "packetInventorySha256": sha((OUT / "evidence-inventory-003.json").read_bytes()),
        "quizSafetyWarnings": warnings,
        "limits": [
            "Awaiting two independent confirmations; earlier acceptance applies to its earlier snapshot, not automatically this proposal.",
            "Effect/impression allocation to ordinary bare 拍 and other rare-family/image/old-dictionary allocations remain unresolved; the direct precaution is not an ordinary-synonym finding.",
            previous_progress["warnings"]["reading"], previous_progress["warnings"]["font"],
            "Host/static evidence only, not arbitrary/custom/multiple-borrow/Kotlin/native/device/old-APK coverage or linguistic proof.",
            "Initial unread index candidates remain limits, not whole-corpus safety judgments or next-batch work.",
            "Historical reports and citation errata stay unchanged; no push, reviewer contact/launch, publication or delivery credit.",
        ],
        "boundary": "One clean owner-signed direct child, no amend; actual signature and all signed-snapshot gates/preservation are in local handoff evidence.",
    })
    print(json.dumps({"boundFiles": len(inventory), "manifestSha256": sha(manifest_raw),
                      "contentVersion": manifest["contentVersion"], "warnings": len(warnings)}))
finally:
    write(HERE / "reconciliation-002-source-read-001" / "packaging-memory.json", guard.finish())
