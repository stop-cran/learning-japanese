import json
from pathlib import Path
from b131_common import HERE, PACKET, REPO, ROOT, sha, start_guard, write
from candidate_b131 import BASE

guard = start_guard()
try:
    gate_dir = HERE / "author-gates-003"
    gates = json.loads((gate_dir / "summary.json").read_text(encoding="utf8"))
    reading = (gate_dir / "reading-exposure.log").read_text(encoding="utf8")
    assert gates["status"] == "PASS"
    assert "0 production hit(s)" in reading and "0 padded-session hit(s)" in reading
    assert "6 latent collision(s)" in reading
    warnings = [line for line in (gate_dir / "quiz-safety.log").read_text(encoding="utf8").splitlines() if line.startswith("WARN")]
    manifest_raw = (REPO / "manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    assert sha(manifest_raw) == gates["manifestSha256"]
    write(REPO / "docs" / "n1-sources" / "batch-131-progress.json", {
        "batch": 131, "status": "local-unreviewed-author-candidate", "base": BASE,
        "originalSourceBase": "6da1184b82b60553f9b65c57f53289c779f96f7c",
        "members": ["衛", "羊", "霜"], "sourceRows": [977, 870, 1174],
        "publishedDelivered": 264, "frozenTotal": 1228, "undelivered": 964,
        "localUnpublishedDrafts": 3, "deliveryNotIncremented": True,
        "supports": [["衛", "自衛"], ["衛", "衛星"], ["羊", "羊毛"], ["霜", "霜"]],
        "proseException": None, "practice": {"衛": "エイ", "羊": "ヨウ", "霜": "しも"},
        "activePairTable": "batch-131/pair-dispositions-002.json",
        "activeSourceAnalysis": "batch-131/authored-source-analysis.json",
        "activeSourceAudit": "batch-131/final-source-audit-002.json",
        "activeFontEvidence": "batch-131/stroke-font-evidence-002.json",
        "historicalAuthorEvidence": ["batch-131/pair-dispositions.json", "batch-131/final-source-audit.json", "batch-131/stroke-font-evidence.json"],
        "completeJmdictFamilies": 874, "completeKanjidicRecords": 182, "comparisonCopies": 179, "pairRows": 195,
        "authorGates": {"directory": str(gate_dir), "summarySha256": sha((gate_dir / "summary.json").read_bytes()), "gates": gates["checks"]},
        "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
        "warnings": {
            "quizSafetyCount": len(warnings), "quizSafetyWarnings": warnings,
            "reading": "0 production/0 padded hits in bounded N1/All/Starter + target; six latent collisions remain in hypothetical smaller or arbitrary pools. Single additional holder checks also found no drawable hits; no arbitrary/custom or multiple-borrow claim.",
            "font": "All three bundled cmaps lack 亍 U+4E8D, 凜 U+51DC, 彳 U+5F73, 衞 U+885E and 韋 U+97CB in the finite taught/comparison scope. Fallback/rendering/native/device unverified.",
            "historicalFailures": "Two 羊 Starter padded reading hits in author-gates-002 were real despite zero exit codes; replaced non-Starter 石 with checked Starter 川. Earlier logs and producers preserved.",
            "source": "衛 state founder/date discrepancies and missing historical glyph images are unresolved; positive historical/native/name evidence is qualified."},
        "boundary": "Author-only candidate. Final committed ten-gate and preservation receipts bind the eventual owner-signed direct child locally. No independent review, push, publication or next batch."})
    for path in sorted(HERE.glob("*.py")):
        write(PACKET / "producers" / path.name, path.read_bytes())
    for directory in ("author-gates-001", "author-gates-002", "author-gates-003"):
        for path in sorted((HERE / directory).iterdir()):
            if path.is_file():
                write(PACKET / "author-evidence" / directory / path.name, path.read_bytes())
    for path in sorted(HERE.glob("*memory*.json")):
        write(PACKET / "author-evidence" / path.name, path.read_bytes())
    write(PACKET / "author-evidence" / "editorial-failure-001.json", (HERE / "editorial-failure-001.json").read_bytes())
    for directory in ("survey-001", "survey-002"):
        write(PACKET / "author-evidence" / directory / "memory.json", (HERE / directory / "memory.json").read_bytes())
    write(PACKET / "author-evidence" / "failed-external-bindings.json", (HERE / "survey-002" / "external-bindings.json").read_bytes())
    history = {}
    for directory in ("survey-001", "survey-002", "external-003"):
        for path in sorted((HERE / directory).rglob("*")):
            if path.is_file():
                history[str(path.relative_to(HERE)).replace("\\", "/")] = {"sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}
    for pattern in ("semantic-*.jsonl", "complete-target-*.jsonl", "target-compact-*.txt",
                    "comparison-readback-*.jsonl", "cards-compact-*.txt", "supplement-cards-*.txt"):
        for path in sorted(HERE.glob(pattern)):
            history[path.name] = {"sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}
    write(PACKET / "local-history-bindings.json", {
        "directory": str(HERE), "files": history,
        "scope": "Full local five-member survey, all failures, complete raw external captures and manual-read projections retained by exact raw hashes. Local-only captures are not committed or described as raw dictionary slices."})
    write(PACKET / "failure-history.json", {
        "survey001": "XML serialization used utf8 declaration; reparse failed. Invalid output, original producer and memory preserved; successor uses utf-8.",
        "survey002": "All ten unescaped-Unicode URLs failed before HTTP request. Exact errors preserved; fresh percent-encoded captures succeeded in external-003.",
        "editorial001": "Finite coverage assertion caught missing 霜/負 and 霜/除 dispositions. Failed producer hash, exact assertion and memory retained; both independently decided in successor.",
        "authorGates001": "Quiz-safety rejected nine missing curated-choice Notes. Added actual distinctions and reran all checks.",
        "authorGates002": "All ten commands exited zero, but reading output disclosed two real 羊 Starter padded hits (ジョウ/ショウ). Not final safety acceptance.",
        "authorGates003": "After complete 川 source/card inspection, replaced non-Starter 石 with Starter 川 on all three targets. Strict wrapper now rejects nonzero production/padded hits. All ten commands pass; zero production/padded hits, six latent hypothetical-pool collisions disclosed.",
        "baselineAdaptation": "Three draft cards/strokes and four wrappers were authored just before verified addendum delivery. Nonoverlapping ordinary fast-forward preserved all local raw bytes; exact timing disclosed, original source scans unchanged.",
        "history": "No predecessor packet or failed output rewritten. Active pair/source/font successors use separate filenames; full raw source streams/captures remain local."})
    write(PACKET / "tool-bindings.json", {
        "leanTools": {name: sha((ROOT / "lean" / name).read_bytes()) for name in
                      ("n1lib.py", "n1_batch_tool.py", "quiz_safety.py", "n1_linkplan.py", "reading_exposure.py", "reading_options.py")},
        "environment": {"N1_REPO": str(REPO), "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1", "pythonFlag": "-B"},
        "guardPolicy": "Pinned >2GiB admission, 0.25s sample, abort <1GiB; own-child waits <=0.1s, terminate/kill <=10s each.",
        "rawEvidence": "Exact original bytes retained; runtime text/n1lib.parse normalizes CRLF to LF."})
    inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
                 for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "evidence-inventory.json", {
        "files": inventory, "selfExcluded": True, "producerSha256": sha(Path(__file__).read_bytes()),
        "limits": "Raw packet binding; final signed snapshot/runtime independently bound by local committed preservation receipts."})
    print(json.dumps({"filesBound": len(inventory), "localHistoryFilesBound": len(history), "quizWarnings": len(warnings),
                      "inventorySha256": sha((PACKET / "evidence-inventory.json").read_bytes())}))
finally:
    write(HERE / "packaging-memory-001.json", guard.finish())
