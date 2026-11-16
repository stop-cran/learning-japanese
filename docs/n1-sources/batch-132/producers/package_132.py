import json
from pathlib import Path
from common_132 import BASE, GUARD_SHA, HERE, PACKET, REPO, ROOT, sha, start_guard, write

guard = start_guard()
try:
    gate_dir = HERE / "author-gates-001"
    gates = json.loads((gate_dir / "summary.json").read_bytes())
    reading = (gate_dir / "reading-exposure.log").read_text(encoding="utf-8")
    assert gates["status"] == "PASS"
    assert "0 production hit(s)" in reading and "0 padded-session hit(s)" in reading
    assert "3 latent collision(s)" in reading and "drawable with 1 of 1 holders: 束" in reading
    warnings = [line for line in (gate_dir / "quiz-safety.log").read_text(encoding="utf-8").splitlines() if line.startswith("WARN")]
    manifest_raw = (REPO / "manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    assert sha(manifest_raw) == gates["manifestSha256"]
    write(REPO / "docs" / "n1-sources" / "batch-132-progress.json", {
        "batch": 132, "status": "local-unreviewed-author-candidate", "base": BASE, "governingIssue": 60,
        "members": ["墓"], "sourceRows": [197], "publishedDelivered": 267, "frozenTotal": 1228,
        "undelivered": 961, "localUnpublishedDrafts": 1, "deliveryNotIncremented": True,
        "supports": [["墓", "墓"]], "proseException": None, "practice": {"墓": "はか"},
        "pairTable": "batch-132/pair-dispositions.json", "sourceAnalysis": "batch-132/authored-source-analysis.json",
        "fontEvidence": "batch-132/stroke-font-evidence.json", "completeJmdictFamilies": 95,
        "completeKanjidicRecords": 7, "comparisonCopies": 6, "pairRows": 6,
        "authorGates": {"directory": str(gate_dir), "summarySha256": sha((gate_dir / "summary.json").read_bytes()), "gates": gates["checks"]},
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "warnings": {"quizSafetyCount": len(warnings), "quizSafetyWarnings": warnings,
                     "reading": "0 production and 0 Starter-plus-target hits; three latent smaller-pool collisions. つか is drawable when Starter also borrows holder 束. Multiple borrowing and arbitrary pools remain outside the bounded pass.",
                     "font": "No cmap misses in finite target/support/comparison/component scope across three checked bundled fonts; not visual/native/device acceptance.",
                     "surveyProcess": "survey-001 used two subprocess.run(timeout=10) git probes, rather than required <=0.1s child-wait loops; subsequent source/gate producers use bounded waits.",
                     "source": "字通 historical glyph images are absent from extracted text. Supplemental and old dictionary readings are over-tested, not asserted to be ordinary modern readings."},
        "boundary": "Author-only candidate. Committed ten-gate and preservation receipts bind eventual owner-signed direct child locally; no independent review, push, publication or next batch."})
    for name in ("check_reading_132.py", "run_132_gates.py", "preserve_132.py", "package_132.py"):
        write(PACKET / "producers" / name, (HERE / name).read_bytes())
    for path in sorted(gate_dir.iterdir()):
        if path.is_file():
            write(PACKET / "author-evidence" / gate_dir.name / path.name, path.read_bytes())
    write(PACKET / "author-evidence" / "preparation-memory-001.json", (HERE / "preparation-memory-001.json").read_bytes())
    for path in sorted((HERE / "source-003" / "comparison-readback").glob("*.json")):
        write(PACKET / "comparison-readback" / path.name, path.read_bytes())
    write(PACKET / "tool-bindings.json", {
        "leanTools": {name: sha((ROOT / "lean" / name).read_bytes()) for name in
                      ("n1lib.py", "n1_batch_tool.py", "quiz_safety.py", "n1_linkplan.py", "reading_exposure.py", "reading_options.py")},
        "environment": {"N1_REPO": str(REPO), "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1", "pythonFlag": "-B"},
        "guardPolicy": "Pinned >2GiB admission, 0.25s sample, abort <1GiB; own-child waits <=0.1s, terminate/kill <=10s each.",
        "rawEvidence": "Exact original bytes retained; runtime text/n1lib.parse normalizes CRLF to LF.",
        "guardSha256": GUARD_SHA})
    inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
                 for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "evidence-inventory.json", {
        "files": inventory, "selfExcluded": True, "producerSha256": sha(Path(__file__).read_bytes()),
        "limits": "Raw packet binding; final signed snapshot/runtime independently bound by local committed receipts."})
    print(json.dumps({"filesBound": len(inventory), "inventorySha256": sha((PACKET / "evidence-inventory.json").read_bytes())}))
finally:
    write(HERE / "packaging-memory-001.json", guard.finish())
