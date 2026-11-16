import json
from pathlib import Path
from b131_common import HERE, PACKET, sha, start_guard, write
from candidate_b131 import BASE

guard = start_guard()
try:
    for name in ("preserve_b131_002.py", "final_binding_b131.py"):
        write(PACKET / "producers" / name, (HERE / name).read_bytes())
    write(PACKET / "author-evidence" / "author-preservation-001-memory.json",
          (HERE / "author-preservation-001" / "memory.json").read_bytes())
    write(PACKET / "final-author-binding.json", {
        "base": BASE, "activePreservationProducer": "producers/preserve_b131_002.py",
        "activeEvidenceInventory": "evidence-inventory-002.json",
        "previousEvidenceInventory": {"file": "evidence-inventory.json", "sha256": sha((PACKET / "evidence-inventory.json").read_bytes())},
        "preservation001Failure": {
            "producer": "producers/preserve_b131.py", "producerSha256": sha((HERE / "preserve_b131.py").read_bytes()),
            "assertion": "FileNotFoundError for docs/wazawaza-sources.json at incoming-worktree-byte check.",
            "qualification": "Failure text recorded from tool output, not byte-for-byte redirected stderr. Actual failed producer and memory preserved; all preceding runtime/source/scan checks had succeeded.",
            "cause": "Incoming ledger is correctly skip-worktree in the existing sparse checkout, not missing from Git.",
            "resolution": "Successor first requires exact baseline/index blob equality for each incoming path; checks local bytes when present, otherwise requires actual S skip-worktree flag. No sparse/shared checkout configuration changed."
        },
        "lineEndings": "Existing touched text uses CRLF. Process-local git -c core.whitespace=cr-at-eol diff --check passes; no shared Git setting or unrelated line-ending rewrite.",
        "sourceAndRuntime": "No learner/runtime changes after author-gates-003. Later additions are evidence and the directly related authoring-notes insertion/progress ledger. Final pre-sign and committed gates/preservation remain required.",
        "boundaries": "Original failure and evidence inventory unchanged; successor adds a new inventory covering the historical inventory and new verifier. No signature/push/review/publication acceptance implied.",
        "producerSha256": sha(Path(__file__).read_bytes())})
    inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
                 for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "evidence-inventory-002.json", {
        "files": inventory, "selfExcluded": True, "producerSha256": sha(Path(__file__).read_bytes()),
        "limits": "Raw final packet binding including untouched predecessor inventory; final signed snapshot bound separately by local committed receipts."})
    print(json.dumps({"filesBound": len(inventory), "finalInventorySha256": sha((PACKET / "evidence-inventory-002.json").read_bytes())}))
finally:
    write(HERE / "final-binding-memory-001.json", guard.finish())
