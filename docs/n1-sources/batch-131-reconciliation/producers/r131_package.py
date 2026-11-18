import json
from pathlib import Path
from r131_common import *

guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    gates_dir = HERE / "author-gates-001"
    gates = json.loads((gates_dir / "summary.json").read_text(encoding="utf8"))
    assert gates["status"] == "PASS" and gates["parent"] == PARENT and gates["publishedBase"] == BASE
    manifest_raw = (REPO / "manifest.json").read_bytes()
    assert sha(manifest_raw) == gates["manifestSha256"]
    manifest = json.loads(manifest_raw)
    for path in sorted(SCRIPTS.glob("r131_*.py")):
        write(PACKET / "producers" / path.name, path.read_bytes())
    for name in ("sources-memory-001.json", "decisions-memory-001.json", "responses-memory-001.json",
                 "query-audit-memory-001.json"):
        write(PACKET / "author-evidence" / name, (HERE / name).read_bytes())
    for path in sorted(gates_dir.iterdir()):
        assert path.is_file()
        write(PACKET / "author-evidence" / gates_dir.name / path.name, path.read_bytes())
    dependencies = {}
    for name in ("b131_common.py", "survey_b131.py", "survey_b131_002.py",
                 "run_b131_gates.py", "candidate_b131.py", "check_reading_b131.py"):
        assert (SCRIPTS / name).read_bytes() == (ORIGINAL / "producers" / name).read_bytes()
        dependencies[name] = sha((SCRIPTS / name).read_bytes())
    write(PACKET / "tool-bindings.json", {"originalImmutableProducerDependencies": dependencies,
                                        "originalPrefix": "docs/n1-sources/batch-131/producers/",
                                        "guardSha256": GUARD_SHA,
                                        "newProducerNames": sorted(p.name for p in SCRIPTS.glob("r131_*.py")),
                                        "resourcePolicy": "Fresh admission >2GiB, abort <1GiB, sample0.25s; own-child wait0.1s; terminate/kill cleanup10s each. No unrelated process changes."})
    write(REPO / "docs" / "n1-sources" / "batch-131-progress-reconciliation-001.json", {
        "batch": 131, "revision": "reconciliation-001",
        "status": "local-author-reconciliation-awaiting-two-original-family-confirmations",
        "parent": PARENT, "publishedBase": BASE, "members": CHARS, "sourceRows": [977, 870, 1174],
        "publishedDelivered": 264, "frozenTotal": 1228, "undelivered": 964,
        "localUnpublishedDrafts": 3, "deliveryNotIncremented": True,
        "runtimeChanges": ["kanji/衛.md", "kanji/霜.md", "manifest.json"],
        "newGuards": {"霜": list("氷凍酒涼久害枯殺卒"), "衛": list("援循番士軍送抵")},
        "unchanged": "羊; all reading inventories and practice choices; four prior support wrappers; strokes; other runtime content; original source/progress evidence.",
        "proseException": "Only concise additive qualified Notes on 衛 and 霜. No existing prose replaced; no support-word prose exception.",
        "activePairAddendum": "batch-131-reconciliation/pair-dispositions-001.json",
        "originalPairTablePreserved": "batch-131/pair-dispositions-002.json",
        "questionDispositions": {"qualifiedPrecautions": 12, "boundedNonCollision": ["Q2"], "openAuthorHolds": []},
        "completeAdditionalJmdictFamilies": 78, "completeAdditionalKanjidicRecords": 19, "comparisonCopies": 17,
        "authorGates": {"directory": str(gates_dir), "summarySha256": sha((gates_dir / "summary.json").read_bytes()),
                        "checks": gates["checks"], "serial": True},
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "warningsAndLimits": "Original six latent smaller-pool reading collisions and bounded font/image/historical source limits retained. No arbitrary/custom/multiple-borrow/Kotlin/native/device, installed APK, independent confirmation or publication acceptance.",
        "handoff": "Exact signed successor, committed ten-gate and preservation evidence bound separately after signing. No push/reviewer contact/publication/next batch."})
    files = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
             for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "evidence-inventory-001.json", {
        "parent": PARENT, "publishedBase": BASE, "files": files,
        "scope": "All new packet raw evidence bytes except this self-index. Runtime/manifest excluded; committed receipts remain local to avoid recursive commit-hash binding."})
    print(json.dumps({"packetFilesIncludingIndex": len(files) + 1,
                      "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"]}))
finally:
    write(HERE / "package-memory-001.json", guard.finish())
