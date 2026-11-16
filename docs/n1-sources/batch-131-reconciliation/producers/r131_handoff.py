import json
from pathlib import Path
from r131_common import *

guard = start_guard()
try:
    candidate = git("rev-parse", "HEAD").decode().strip()
    assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    proof = {}
    for name in ("author-gates-001", "author-preservation-001", "committed-gates-001", "committed-preservation-001"):
        path = HERE / name / "summary.json"
        summary = json.loads(path.read_text(encoding="utf8"))
        assert summary["status"] == "PASS" and summary["parent"] == PARENT
        if name.startswith("committed-"):
            assert summary.get("startingHead", summary.get("head")) == candidate
        proof[name] = {"directory": str(path.parent), "summarySha256": sha(path.read_bytes())}
        if "preservation" in name:
            proof[name]["runtimeHashesSha256"] = sha((path.parent / "runtime-hashes.json").read_bytes())
    committed = json.loads((HERE / "committed-preservation-001" / "summary.json").read_text(encoding="utf8"))
    assert committed["clean"] and committed["ownerSignature"]["status"] == "G"
    manifest_raw = (REPO / "manifest.json").read_bytes()
    assert sha(manifest_raw) == committed["manifestSha256"]
    table_path = PACKET / "pair-dispositions-001.json"
    table = json.loads(table_path.read_text(encoding="utf8"))
    responses = {family: {suffix: {"path": str(PACKET / "responses" / (family + "-" + suffix)),
                                   "sha256": sha((PACKET / "responses" / (family + "-" + suffix)).read_bytes())}
                          for suffix in ("mapping-001.json", "response-001.md")}
                 for family in ("claude", "gpt")}
    changes = [p for p in git("diff", "--name-only", "-z", PARENT, "HEAD").decode().split("\0") if p]
    result = {
        "status": "signed-clean-local-author-reconciliation-awaiting-confirmations",
        "candidate": candidate, "parent": PARENT, "publishedBase": BASE,
        "members": [{"kanji": "衛", "sourceRow": 977, "supports": ["自衛", "衛星"]},
                    {"kanji": "羊", "sourceRow": 870, "supports": ["羊毛"]},
                    {"kanji": "霜", "sourceRow": 1174, "supports": ["霜"]}],
        "worktree": str(REPO), "changedFiles": changes,
        "runtimeChanges": committed["changedRuntime"], "appendedGuards": committed["appendedGuards"],
        "unchanged": "羊, all ordered readings/practice/distractors/radicals/stroke data, four existing reciprocal supports, all other runtime entries, all original packet/progress evidence. Incoming main word-only work preserved.",
        "declaredProseException": "Only concise additive qualified Notes on 衛 and 霜; no prior prose replaced and no support prose exception. One insert-only authoring-notes entry.",
        "finitePairs": {"path": str(table_path), "sha256": sha(table_path.read_bytes()),
                        "rows": 17, "questions": 13, "questionPrecautions": 12,
                        "boundedNonCollisions": ["Q2"], "openAuthorHolds": [],
                        "requiredDirectPairs": ["霜/氷", "霜/凍", "衛/援", "衛/循"]},
        "sourcePacket": {"path": str(PACKET), "sourceReceiptSha256": sha((PACKET / "source-receipt.json").read_bytes()),
                         "externalBindingsSha256": sha((PACKET / "external-source-bindings.json").read_bytes()),
                         "inventorySha256": sha((PACKET / "evidence-inventory-001.json").read_bytes()),
                         "newCompleteFamilies": 78, "newCompleteCharacterRecords": 19, "comparisonCopies": 17,
                         "originalCompleteFamilyUnion": 874,
                         "queryScope": "Exact comparison/word spellings and mechanically discovered seven-digit references; companion allocation audit identifies a collateral Kotobank identifier, not lexical support. Complete variants/restrictions/secondary senses and zero matches retained. Exact compressed/decompressed/output/canonical hashes in receipts; original source evidence unchanged."},
        "familyIsolatedResponses": responses, "proof": proof,
        "manifestSha256": sha(manifest_raw), "contentVersion": committed["contentVersion"],
        "ownerSignature": committed["ownerSignature"], "clean": True,
        "publishedDelivered": 264, "frozenTotal": 1228, "undelivered": 964, "deliveryNotIncremented": True,
        "warningsAndLimits": [
            "All 20 pre/post serial gate commands passed, including explicit supplemental-key host checks and exact manifest reproduction. Zero production/padded hits; original six latent smaller-pool reading collisions retained.",
            "No new arbitrary/custom/multiple-borrow/Kotlin/native/device, installed APK, rendered glyph/fallback, geometry or whole-set acceptance.",
            "Historical jargon, positive rare/native/name/supplemental senses, source discrepancies and image omissions remain. Precautions do not assert universal synonymy or transitivity; Q2 distinction is bounded.",
            "Raw accepted reports/limits remain historical; separate citation and Unicode errata do not rewrite them.",
            "Two original-family confirmations and publication remain coordinator-owned. No push, reviewer contact/launch, publication or next batch."],
        "producerSha256": sha(Path(__file__).read_bytes())}
    write(HERE / "author-handoff-001.json", result)
    print(json.dumps(result, ensure_ascii=False))
finally:
    write(HERE / "handoff-memory-001.json", guard.finish())
