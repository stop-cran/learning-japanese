import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common_132 import HERE, REPO, git, normalized, sha, start_guard, write

OUT = Path(__file__).resolve().parent
PACKET = REPO / "docs" / "n1-sources" / "batch-132-reconciliation"
SOURCE = HERE / "source-reconciliation-001"
REVIEW = HERE / "review"
PARENT = "2e618b38ae5b420f7a1fe6783268093348367c51"


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        summary = json.loads((OUT / "author-gates-001" / "summary.json").read_bytes())
        assert summary["status"] == "PASS"
        assert summary["manifestSha256"] == sha((REPO / "manifest.json").read_bytes())
        write(PACKET / "before-墓.md", (OUT / "before-墓.md").read_bytes())
        write(PACKET / "after-墓.md", (REPO / "kanji" / "墓.md").read_bytes())
        write(PACKET / "teaching.diff", git("-c", "core.quotepath=false", "diff", "--no-ext-diff", PARENT, "--", "kanji/墓.md"))
        for name in ("dictionary-receipt.json", "membership.json", "referenced-receipt.json",
                     "referenced-membership.json", "jmdict-exact-families.xml", "jmdict-referenced-families.xml",
                     "kanjidic2-exact-characters.xml", "dispositions.json", "inventory.json", "verification.json"):
            write(PACKET / "source" / name, (SOURCE / name).read_bytes())
        for name in ("source-reconciliation-adjudication-001.json", "source-reconciliation-verification-001.json",
                     "source-reconciliation-freeze-001.json"):
            write(PACKET / "source" / name, (REVIEW / name).read_bytes())
        captures = []
        for name in ("external-captures.json", "referenced-external-captures.json"):
            for item in json.loads((SOURCE / name).read_bytes())["captures"]:
                captures.append({k: item[k] for k in ("term", "provider", "url", "finalUrl", "status", "capturedAt",
                                                        "raw", "rawBytes", "rawSha256", "extraction", "extractionBytes",
                                                        "extractionSha256", "extractionMethod", "error") if k in item})
        write(PACKET / "source" / "capture-bindings.json", {
            "captures": captures, "sourceLedgerSha256": {
                name: sha((SOURCE / name).read_bytes()) for name in ("external-captures.json", "referenced-external-captures.json")},
            "originalTargetCaptures": json.loads((HERE / "source-003" / "external-capture-bindings.json").read_bytes()),
            "limits": "Raw HTML and complete text remain at the cited local paths, not committed. One 墓塔 Kotobank request failed with HTTP 404; the failure response body was not retained."})
        source = json.loads((SOURCE / "dispositions.json").read_bytes())
        write(PACKET / "pair-dispositions.json", {
            "parent": PARENT, "claimIds": ["Q1", "Q2"],
            "status": "Precautions implemented; original-reviewer confirmations pending.",
            "pairs": [{"claim": claim["id"], "pair": claim["pair"], "decision": "direct symmetric precaution",
                       "labelDirections": claim["displayedLabelDirections"], "evidence": claim["positiveEvidence"],
                       "qualifications": claim["counterEvidenceAndLimits"]} for claim in source["claims"]],
            "directExclusionsBefore": ["埋", "石"], "directExclusionsAfter": ["埋", "石", "標", "塔"],
            "mechanism": "Content-side tools/audit_n1_batch.py:575-584 rejects a curated pair when either endpoint directly names the other; no transitive inference, reciprocal edit or Kotlin/device execution claimed.",
            "reviewStatus": "Claude CLEAN and GPT UNVERIFIED initial outcomes remain unchanged; Q1/Q2 open pending independent confirmations; O1/O2 optional/no-required-change."})
        write(PACKET / "provenance.json", {
            "parent": PARENT, "sourceInventorySha256": sha((SOURCE / "inventory.json").read_bytes()),
            "coordinatorDecisionSha256": sha((REVIEW / "source-reconciliation-adjudication-001.json").read_bytes()),
            "independentSourceVerificationSha256": sha((REVIEW / "source-reconciliation-verification-001.json").read_bytes()),
            "laterSourceFreezeSha256": sha((REVIEW / "source-reconciliation-freeze-001.json").read_bytes()),
            "freezeQualification": "The original source handoff and four reused captures were writable on receipt. Coordinator subsequently verified bytes and set ReadOnly; this is not retrospective immutability.",
            "sourceSummary": "27 unique complete parsed/reserialized JMdict families (23+5 with one canonical-equal overlap), three complete KANJIDIC2 records; exact spelling predicates and absence disclosures in receipts.",
            "authorGatesSummarySha256": sha((OUT / "author-gates-001" / "summary.json").read_bytes()),
            "manifestSha256": summary["manifestSha256"],
            "scope": "Two conservative direct exclusions, two qualified notes and directly related citations only. All other teaching/runtime except regenerated manifest is unchanged.",
            "boundary": "Unreviewed local reconciliation. Q1/Q2 stay open pending both original-reviewer confirmations; no publication, native/device, visual or whole-set acceptance."})
        for path in sorted((OUT / "author-gates-001").iterdir()):
            if path.is_file():
                write(PACKET / "author-gates" / path.name, path.read_bytes())
        for name in ("admit.py", "gates.py", "package.py", "preserve.py"):
            write(PACKET / "producers" / name, (OUT / name).read_bytes())
        inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
                     for p in sorted(PACKET.rglob("*")) if p.is_file()}
        write(PACKET / "inventory.json", {"files": inventory, "selfExcluded": True,
                                           "limits": "Local raw-byte evidence binding; committed parent and runtime hashes bind separately."})
        print(json.dumps({"files": len(inventory), "inventorySha256": sha((PACKET / "inventory.json").read_bytes())}))
    finally:
        write(OUT / "package-memory.json", guard.finish())


if __name__ == "__main__":
    main()
