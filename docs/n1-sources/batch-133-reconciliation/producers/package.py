import json
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import REPO, git, sha, start_guard, write

PARENT = "ad047ace020579f81bde250ac948b9a4cb597887"
PACKET = REPO / "docs" / "n1-sources" / "batch-133-reconciliation"
SOURCE = OUT.parent / "source-reconciliation-001"


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        assert not PACKET.exists()
        gates_path = OUT / "author-gates-001"
        summary = json.loads((gates_path / "summary.json").read_bytes())
        assert summary["status"] == "PASS"
        assert summary["manifestSha256"] == sha((REPO / "manifest.json").read_bytes())
        assert json.loads((OUT / "author-preservation-001" / "summary.json").read_bytes())["status"] == "PASS"
        for ch in "鉛滝琴":
            write(PACKET / ("before-" + ch + ".md"), (OUT / ("before-" + ch + ".md")).read_bytes())
            write(PACKET / ("after-" + ch + ".md"), (REPO / "kanji" / (ch + ".md")).read_bytes())
        write(PACKET / "teaching.diff", git("diff", "--no-ext-diff", PARENT, "--", "kanji/鉛.md", "kanji/滝.md", "kanji/琴.md"))
        for name in ("dictionary-receipt.json", "query-membership.json", "supplement-receipt.json",
                     "jmdict-complete-families.xml", "jmdict-supplement-complete-families.xml",
                     "kanjidic2-complete-records.xml", "kanjidic2-supplement-complete-records.xml",
                     "pair-dispositions-final.json", "verification.json", "inventory.json",
                     "reused-captures-index.json", "review-extract-binding.json"):
            write(PACKET / "source" / name, (SOURCE / name).read_bytes())
        for name in ("coordinator-adjudication-001.json", "source-reconciliation-verification-001.json"):
            write(PACKET / "source" / name, (OUT.parent / "review" / name).read_bytes())
        captures = []
        for path in sorted((SOURCE / "captures").glob("*.receipt.json")):
            item = json.loads(path.read_bytes())
            captures.append({
                "localReceipt": str(path), "receiptSha256": sha(path.read_bytes()),
                **{k: item[k] for k in ("character", "requestedUrl", "finalUrl", "canonicalUrl", "startedAt",
                                       "completedAt", "finishedAt", "status", "htmlSha256", "htmlBytes",
                                       "bytes", "textSha256", "textLines", "failedResponseSha256", "error") if k in item}
            })
        write(PACKET / "source" / "capture-bindings.json", {
            "captures": captures, "reused": json.loads((SOURCE / "reused-captures-index.json").read_bytes()),
            "scope": "29 complete new captures, two preserved HTTP404 attempts, six reused complete HTML captures. Failed URLs are not cited in teaching. Complete external HTML/text and response headers remain local, not committed. Missing image glyphs are disclosed, not reconstructed.",
            "attribution": "Constituent dictionaries named on each captured page; JMdict and KANJIDIC2: EDRDG, CC BY-SA4.0. XML selections are complete parsed/reserialized records, not raw slices."
        })
        adjudication = json.loads((OUT.parent / "review" / "coordinator-adjudication-001.json").read_bytes())
        write(PACKET / "pair-dispositions.json", {
            "parent": PARENT, "status": "Adjudicated 11 precautions implemented; original-reviewer confirmations pending.",
            "coordinatorDecisions": adjudication["decisions"], "crossPair": adjudication["crossPair"],
            "sourceAuthorProposals": "source/pair-dispositions-final.json preserves differing author proposals and unresolved source scope.",
            "implementedAppendOrder": {"鉛": ["鉱", "遅", "円"], "滝": ["速", "声", "激", "岩", "険"], "琴": ["具", "糸", "緒"]},
            "mechanism": "Direct pair exclusion on either endpoint applies symmetrically in the bounded host model; only the three admitted new cards change. No reciprocal counterpart edits or transitive guards.",
            "reviewStatus": "Original Claude CLEAN and GPT UNVERIFIED preserved. No confirmation, review closure, publication or delivery credit."
        })
        warnings = []
        for path in sorted(gates_path.iterdir()):
            if path.is_file():
                write(PACKET / "author-gates" / path.name, path.read_bytes())
                if path.suffix == ".log":
                    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                        if re.search(r"warn|latent collision|not drawable|cannot be drawn", line, re.I):
                            warnings.append({"log": path.name, "line": line_no, "text": line})
        write(PACKET / "author-gates" / "warning-bindings.json", warnings)
        for name in ("summary.json", "article-deltas.json", "all-runtime-hashes.json", "memory.json"):
            write(PACKET / "author-preservation" / name, (OUT / "author-preservation-001" / name).read_bytes())
        for name in ("admit.py", "gates.py", "preserve.py", "package.py"):
            write(PACKET / "producers" / name, (OUT / name).read_bytes())
        for name in ("run_133_gates.py", "check_reading_133.py", "bounded_launch_133.py", "common_133.py"):
            write(PACKET / "producers" / "original" / name, (OUT.parent / name).read_bytes())
        write(PACKET / "provenance.json", {
            "parent": PARENT, "coordinatorDecisionSha256": sha((OUT.parent / "review" / "coordinator-adjudication-001.json").read_bytes()),
            "coordinatorSourceVerificationSha256": sha((OUT.parent / "review" / "source-reconciliation-verification-001.json").read_bytes()),
            "sourceInventorySha256": sha((SOURCE / "inventory.json").read_bytes()),
            "authorGatesSummarySha256": sha((gates_path / "summary.json").read_bytes()),
            "manifestSha256": summary["manifestSha256"],
            "scope": "Exact 11 appended exclusions; qualified Notes and directly related successful-source citations on only 鉛/滝/琴. Original metadata except exclusions, practice, titles, distractors, common words, mnemonics, strokes, word wrappers, original B133 evidence and all other tracked paths preserved.",
            "sourceCoverage": "115 unique complete JMdict families (113+4, two equal overlaps), 43 complete KD records; 152 spelling/reading query applications, 150 distinct, 35 zero-match applications; 43 character queries.",
            "sourceDiscrepancies": "JMdict1736440 lead mine/deposits not lead ore; old 琴 ことのを scope unresolved, not taught as cord; regional タキ cliff explicitly bounded and not taught as unrestricted 滝. Coordinator retained the separately disclosed 鉛-具 pigment/white-lead distinction.",
            "gatePhase": "These serial author gates ran before signing on the exact packaged runtime snapshot. Same ten gates must run again on the signed commit; post-commit receipts stay local to avoid a self-referential commit.",
            "freezeQualification": "Source packet was verified ReadOnly before this revision; original B132 survey captures remain only hash-equal and are not claimed historically frozen. No prior writable handoff is relabeled.",
            "boundary": "Local signed reconciliation only. Original reviewer confirmations and publication remain with coordinator; no native/device, visual, custom/multiple-borrow or whole-set acceptance.",
            "delivered": 268, "remaining": 960
        })
        inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): {"sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                     for p in sorted(PACKET.rglob("*")) if p.is_file()}
        write(PACKET / "inventory.json", {"files": inventory, "selfExcluded": True,
                                         "scope": "Every other file in this additive reconciliation directory; raw evidence bytes."})
        print(json.dumps({"status": "PASS", "files": len(inventory) + 1,
                          "inventorySha256": sha((PACKET / "inventory.json").read_bytes())}))
    finally:
        write(OUT / "package-memory.json", guard.finish())


if __name__ == "__main__":
    main()
