import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from common_133 import BASE, GUARD_SHA, HERE, PACKET, REPO, ROOT, sha, start_guard, write


def main():
    guard = start_guard()
    try:
        gate_dir = HERE / "author-gates-002"
        gates = json.loads((gate_dir / "summary.json").read_bytes())
        reading = (gate_dir / "reading-exposure.log").read_text(encoding="utf-8")
        assert gates["status"] == "PASS"
        assert "0 production hit(s)" in reading and "0 padded-session hit(s)" in reading
        assert "1 latent collision(s)" in reading and "うるおす" in reading
        warnings = [line for line in (gate_dir / "quiz-safety.log").read_text(encoding="utf-8").splitlines() if line.startswith("WARN")]
        raw_manifest = (REPO / "manifest.json").read_bytes()
        manifest = json.loads(raw_manifest)
        assert sha(raw_manifest) == gates["manifestSha256"]
        kd = set()
        for name in ("kanjidic2-targets.xml", "kanjidic2-comparisons.xml", "kanjidic2-variants-components.xml", "additional/kanjidic2-additional-comparisons.xml"):
            kd.update(n.findtext("literal") for n in ET.parse(PACKET / name).getroot())
        fonts = json.loads((PACKET / "stroke-font-evidence.json").read_bytes())
        misses = {f["filename"]: [k for k, v in f["coverage"].items() if not v] for f in fonts["fonts"]}
        write(REPO / "docs" / "n1-sources" / "batch-133-progress.json", {
            "batch": 133, "status": "local-unreviewed-author-candidate", "base": BASE, "governingIssue": 60,
            "members": ["琴", "鉛", "滝"], "sourceRows": [707, 1120, 643],
            "publishedDelivered": 268, "frozenTotal": 1228, "undelivered": 960, "localUnpublishedDrafts": 3,
            "deliveryNotIncremented": True, "supports": [["琴", "琴"], ["鉛", "鉛筆"], ["滝", "滝"]],
            "proseException": None, "practice": {"琴": {"on": [], "kun": ["こと"]}, "鉛": {"on": ["エン"], "kun": []}, "滝": {"on": [], "kun": ["たき"]}},
            "pairTable": "batch-133/pair-dispositions.json", "sourceAnalysis": "batch-133/authored-source-analysis.json",
            "fontEvidence": "batch-133/stroke-font-evidence.json", "completeJmdictFamilies": 515,
            "completeKanjidicRecords": len(kd), "comparisonCopies": 68, "baselineScanRowsPerMember": 1258,
            "baselinePairRows": 74, "newMemberPairRows": 3,
            "authorGates": {"directory": str(gate_dir), "summarySha256": sha((gate_dir / "summary.json").read_bytes()), "gates": gates["checks"]},
            "manifestSha256": sha(raw_manifest), "contentVersion": manifest["contentVersion"],
            "warnings": {
                "quizSafetyCount": len(warnings), "quizSafetyWarnings": warnings,
                "existingFallbackCards": ["人", "休", "何", "入", "出", "口", "女", "日", "月", "男", "買"],
                "reading": "0 production / 0 Starter-plus-target hits. One latent smaller-pool 滝/湿 collision for うるおす; not drawable even with one extra holder in tested Starter model. Arbitrary/custom and multiple-borrow pools unaccepted.",
                "fontCmapMisses": misses,
                "font": "Actual misses include component/variant/supplemental glyphs. All three target glyphs present; not rendered fallback, visual or native/device acceptance.",
                "source": "Reused B132 captures, not fresh fetches. Supplemental/name/historical and uncertain readings deliberately over-tested; missing historical glyph images not reconstructed.",
                "originalFailure": "author-gates-001 lint failed three H1 ASCII delimiters; fixed to repository-required em dash. Original log/receipt preserved, not relabeled.",
            },
            "boundary": "Author-only candidate. Final signed-snapshot ten-gate and preservation receipts remain local outside commit. No independent review, push, publication or next batch."})
        for name in ("bounded_launch_133.py", "check_reading_133.py", "run_133_gates.py", "preserve_133.py", "package_133.py", "sign_133_once.py"):
            write(PACKET / "producers" / name, (HERE / name).read_bytes())
        for directory in ("author-gates-001", "author-gates-002"):
            for path in sorted((HERE / directory).iterdir()):
                if path.is_file():
                    write(PACKET / "author-evidence" / directory / path.name, path.read_bytes())
        write(PACKET / "author-evidence" / "preparation-memory-001.json", (HERE / "preparation-memory-001.json").read_bytes())
        write(PACKET / "tool-bindings.json", {
            "leanTools": {name: sha((ROOT / "lean" / name).read_bytes()) for name in
                          ("n1lib.py", "n1_batch_tool.py", "quiz_safety.py", "n1_linkplan.py", "reading_exposure.py", "reading_options.py")},
            "environment": {"N1_REPO": str(REPO), "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1", "pythonFlag": "-B"},
            "guardPolicy": "Pinned >2GiB admission, 0.25s sample, abort <1GiB; own-child waits <=0.1s, terminate/kill <=10s each. Bounded launcher applies communicate polling also to subprocess.run/check_output used inside original tools.",
            "rawEvidence": "Original bytes retained; runtime text/n1lib.parse normalize CRLF to LF.",
            "guardSha256": GUARD_SHA})
        inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes()) for p in sorted(PACKET.rglob("*")) if p.is_file()}
        write(PACKET / "evidence-inventory.json", {
            "files": inventory, "selfExcluded": True, "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "Packet binding; final signed snapshot and all runtime hashes bound by external committed receipts."})
        print(json.dumps({"filesBound": len(inventory), "completeKanjidicUnion": len(kd), "inventorySha256": sha((PACKET / "evidence-inventory.json").read_bytes())}))
    finally:
        write(HERE / "packaging-memory-001.json", guard.finish())


if __name__ == "__main__":
    main()
