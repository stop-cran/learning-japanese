"""Derive B118 finalization for its second correction without changing earlier evidence."""
from pathlib import Path

from common import freeze_json, frozen, sha
from derive_selected_followups import derive_file

HERE = Path(__file__).resolve().parent
HELPER = '''
def second_reconciliation(config, candidate, proof):
    records = WS / "scratch-118" / "review"
    prior_raw = frozen(WS / "scratch-118" / "revision-verification-001" / "revision-verification.json",
                       proof["priorProofSha256"])
    prior = json.loads(prior_raw)
    require(prior["status"] == "PASS" and prior["candidate"] == proof["prior"]
            and git(config, "rev-parse", f"{candidate}^").decode().strip() == prior["candidate"]
            and prior["base"] == proof["base"] and prior["initial"] == proof["initial"],
            "Earlier proof or lineage differs")
    require(proof["dictionaryProof"] == prior["sourceProof"], "Dictionary proof changed")
    freeze_raw = frozen(records / "reconciliation-002-freeze.json")
    handoff = json.loads(freeze_raw)
    require(handoff["candidate"] == candidate, "Handoff belongs to another candidate")
    for path, digest in handoff["files"].items():
        frozen(WS / path, digest)
    newer = records / "reconciliation-002"
    artifacts = {
        "revision-verification-001.json": prior_raw,
        "reconciliation-002/freeze.json": freeze_raw,
    }
    for name in ("author-response-gpt-001-confirm-002.md", "pair-dispositions.json",
                 "source-receipt.json", "target-source-receipt.json",
                 "kanjidic2-extraction.json", "changed-file-inventory.json"):
        artifacts[f"reconciliation-002/{name}"] = frozen(newer / name)
    for name in ("pair-dispositions.json", "source-receipt.json"):
        require(artifacts[f"reconciliation-002/{name}"] == git(
            config, "show", f"{candidate}:docs/n1-sources/batch-118/reconciliation-002/{name}"),
            f"Second correction evidence differs: {name}")
    require(sha(artifacts["reconciliation-002/source-receipt.json"])
            == proof["captureProof"]["receiptSha256"]
            and sha(artifacts["reconciliation-002/target-source-receipt.json"])
            == proof["captureProof"]["targetReceiptSha256"], "Capture proof differs")
    return artifacts


'''


def derive():
    result = derive_file("finalize_b118.py", "finalize_b118_v2.py", [
        ('"""Persist B118\'s accepted textual closure without counting it as delivered."""',
         '"""Persist both B118 reconciliations and final confirmations without claiming delivery."""'),
        ('def finalize(candidate, gates, proof_path):',
         HELPER + 'def finalize(candidate, gates, proof_path):'),
        ('            and proof["baselineRuntimePreservedExceptRequiredWrappers"]\n'
         '            and proof["originalMetadataStrokesGuardsAndSourceReceiptsPreserved"]',
         '            and proof["priorRuntimeChangedOnlyTargetCard"]\n'
         '            and proof["earlierMetadataStrokesGuardsBodyAndReceiptsPreserved"]\n'
         '            and proof["sourceMembersPublishedBeforeBatch"] == 246\n'
         '            and proof["sourceMembersInCandidate"] == 247\n'
         '            and proof["linguisticAcceptance"] is False\n'
         '            and proof["publicationAccepted"] is False'),
        ('        artifacts = {"revision-verification.json": proof_raw}',
         '        artifacts = {"revision-verification.json": proof_raw,\n'
         '                     **second_reconciliation(config, candidate, proof)}'),
        ('== proof["sourceProof"]["receiptSha256"],',
         '== proof["dictionaryProof"]["receiptSha256"],'),
        ('                     "record_publication.py", "test_record_publication.py"):',
         '                     "record_publication.py", "test_record_publication.py",\n'
         '                     "verify_b118_revision_v2.py", "test_verify_b118_revision_v2.py",\n'
         '                     "finalize_b118_v2.py", "derive_finalize_b118_v2.py",\n'
         '                     "finalize-b118-v2-derivation.json"):'),
        ('                               "reconciliationReceiptSha256": proof["sourceProof"]["receiptSha256"]},',
         '                               "reconciliationReceiptSha256": proof["dictionaryProof"]["receiptSha256"],\n'
         '                               "secondReconciliation": "batch-118/reconciliation-002/source-receipt.json",\n'
         '                               "secondReconciliationReceiptSha256": proof["captureProof"]["receiptSha256"],\n'
         '                               "priorRevision": proof["prior"],\n'
         '                               "priorProofSha256": proof["priorProofSha256"]},'),
    ])
    print(freeze_json(HERE / "finalize-b118-v2-derivation.json", {
        "derivation": result,
        "tool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "scope": "Use the second-correction proof, preserve both reconciliation rounds and their "
                 "lineage, and retain the original two-family final-acceptance and publication gates.",
    }))


if __name__ == "__main__":
    derive()
