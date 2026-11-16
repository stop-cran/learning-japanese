import json
from pathlib import Path
from b130_common import BASE, HERE, PACKET, REPO, ROOT, sha, start_guard, write

guard = start_guard()
try:
    gate_dir = HERE / "author-gates-002"
    gates = json.loads((gate_dir / "summary.json").read_text(encoding="utf8"))
    reading = (gate_dir / "reading-exposure.log").read_text(encoding="utf8")
    assert gates["status"] == "PASS"
    assert "0 production hit(s)" in reading and "0 padded-session hit(s)" in reading
    warnings = [line for line in (gate_dir / "quiz-safety.log").read_text(encoding="utf8").splitlines() if line.startswith("WARN")]
    manifest = json.loads((REPO / "manifest.json").read_text(encoding="utf8"))
    write(REPO / "docs" / "n1-sources" / "batch-130-progress.json", {
        "batch": 130, "status": "local-unreviewed-author-candidate", "base": BASE,
        "members": ["塀", "拍", "耗"], "sourceRows": [191, 419, 879],
        "publishedDelivered": 261, "frozenTotal": 1228, "undelivered": 967,
        "localUnpublishedDrafts": 3, "deliveryNotIncremented": True,
        "supports": [["塀", "塀"], ["拍", "拍手"], ["耗", "消耗"]],
        "proseException": None, "practice": {"塀": "ヘイ", "拍": "ハク", "耗": "モウ"},
        "activePairTable": "batch-130/pair-dispositions-002.json",
        "activeSourceAnalysis": "batch-130/authored-source-analysis-002.json",
        "supersededLocalAuthorEvidence": ["batch-130/pair-dispositions.json", "batch-130/authored-source-analysis.json"],
        "completeJmdictFamilies": 519, "completeKanjidicRecords": 192, "comparisonCopies": 189, "pairRows": 213,
        "authorGates": {"directory": str(gate_dir), "summarySha256": sha((gate_dir / "summary.json").read_bytes()), "gates": gates["checks"]},
        "manifestSha256": sha((REPO / "manifest.json").read_bytes()), "contentVersion": manifest["contentVersion"],
        "warnings": {"quizSafetyCount": len(warnings), "quizSafetyWarnings": warnings,
                     "reading": "0 production and 0 padded hits in bounded N1/All/Starter + one target. Supplemental 耗 ボウ remains a latent collision in smaller/hypothetical or additional-borrow pools; not universal zero exposure.",
                     "font": "All three bundled cmaps lack 尸 U+5C38, 并 U+5E76, 扌 U+624C, 耒 U+8012. No rendered fallback or visual/native acceptance."},
        "boundary": "Author-only candidate. Committed ten-gate and preservation receipts bind the eventual signed SHA locally. No independent review, push, publication or next batch."})
    for path in sorted(HERE.glob("*.py")):
        write(PACKET / "producers" / path.name, path.read_bytes())
    planning = {str(p.relative_to(HERE)).replace("\\", "/"): sha(p.read_bytes())
                for p in sorted((HERE / "planning-five-001").rglob("*")) if p.is_file()}
    write(PACKET / "planning-history-bindings.json", {
        "localDirectory": str(HERE / "planning-five-001"), "files": planning,
        "scope": "Original five-member survey retained locally. Historical planning, not final three-member gates."})
    for directory in ("author-gates-001", "author-gates-002"):
        for path in sorted((HERE / directory).iterdir()):
            if path.is_file():
                write(PACKET / "author-evidence" / directory / path.name, path.read_bytes())
    for path in sorted(HERE.glob("*memory*.json")):
        write(PACKET / "author-evidence" / path.name, path.read_bytes())
    for name in ("editorial-failure-001.json", "supplement-001.log", "supplement-002.log", "survey-001.log", "survey-002.log"):
        write(PACKET / "author-evidence" / name, (HERE / name).read_bytes())
    write(PACKET / "failure-history.json", {
        "editorial001": "Failed finite coverage assertion for 拍 丸/使; original producer, exact error and memory receipt preserved. Explicit decisions added, not silently skipped.",
        "supplement001": "Failed assertion due to split text nodes in actual へる・たより capture; producer/log/memory preserved; corrected concatenation on identical raw bytes.",
        "authorGates001": "All exit codes zero, but reading exposure disclosed 百/ヒャク Starter PAD-HIT for 拍. Not treated as final safety result.",
        "authorGates002": "Replaced 拍 石 with 川 and 耗 石/未 with 川/本 after actual full card/complete-family inspection. All three are Starter choices for these targets. All ten gates pass; 0 production/0 padded hits, residual 耗 ボウ latent collision disclosed.",
        "history": "Prior pair/source analysis and original successful editorial producer remain. -002 packet files are current.",
        "localLogs": {p.name: {"sha256": sha(p.read_bytes()), "bytes": p.stat().st_size} for p in sorted(HERE.glob("*.log"))}})
    write(PACKET / "tool-bindings.json", {
        "leanTools": {name: sha((ROOT / "lean" / name).read_bytes()) for name in
                      ("n1lib.py", "n1_batch_tool.py", "quiz_safety.py", "n1_linkplan.py", "reading_exposure.py", "reading_options.py")},
        "environment": {"N1_REPO": str(REPO), "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1", "pythonFlag": "-B"},
        "guardPolicy": "Pinned guard, >2GiB admission, 0.25s sample, abort <1GiB; own-child waits <=0.1s, terminate/kill <=10s each.",
        "rawEvidence": "Original bytes retained; runtime text/n1lib.parse normalizes CRLF to LF."})
    inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
                 for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "evidence-inventory.json", {"files": inventory, "selfExcluded": True,
          "producerSha256": sha(Path(__file__).read_bytes()),
          "limits": "Raw packet binding; committed signed snapshot/runtime independently bound by local preservation receipts."})
    print(json.dumps({"filesBound": len(inventory), "planningFilesBound": len(planning), "quizWarnings": len(warnings),
                      "inventorySha256": sha((PACKET / "evidence-inventory.json").read_bytes())}))
finally:
    write(HERE / "packaging-memory-001.json", guard.finish())
