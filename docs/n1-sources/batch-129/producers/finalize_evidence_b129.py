import json
import subprocess
from pathlib import Path
from b129_common import HERE, PACKET, REPO, sha, start_guard, write

guard = start_guard()
try:
    # Formatting only: runtime hashes already use LF. Never normalize frozen evidence.
    formatting = {}
    for relative in ("docs/n1-authoring-notes.md", "words/茉莉花.md"):
        path = REPO / relative
        before = path.read_bytes()
        after = before.replace(b"\r\n", b"\n")
        path.write_bytes(after)
        formatting[relative] = {"rawBeforeSha256": sha(before), "rawAfterSha256": sha(after),
                                "crlfSequencesNormalized": before.count(b"\r\n"),
                                "normalizedRuntimeUnchanged": before.replace(b"\r\n", b"\n") == after}
    for name in ("preserve_b129_all.py", "finalize_evidence_b129.py"):
        write(PACKET / "producers" / name, (HERE / name).read_bytes())
    for path in sorted((HERE / "author-preservation-001").iterdir()):
        if path.is_file():
            write(PACKET / "author-evidence" / "author-preservation-001" / path.name, path.read_bytes())
    write(PACKET / "evidence-scope-revision-002.json", {
        "originalInventory": "evidence-inventory.json",
        "originalInventorySha256": sha((PACKET / "evidence-inventory.json").read_bytes()),
        "originalPreservation": str(HERE / "author-preservation-001"),
        "reason": "The original checker covered the manifest files group only (7862 baseline / 7868 candidate), not all manifest groups. Its all-runtime label was overbroad. Preserve that receipt unchanged; preserve_b129_all.py verifies every group, including media, scenes, listening and curriculum.",
        "formatting": formatting,
        "whitespaceAttempt": {"originalToolResult": "shell 3819: git diff --check reported CR-at-EOL as trailing whitespace in the inserted authoring subsection and one support-wrapper line.",
                              "disposition": "Normalize only those two edited prose files to LF. No normalized runtime content or manifest change; frozen source/report bytes untouched."},
        "authorGates": "All ten author-gates-002 results remain applicable to unchanged normalized runtime bytes.",
        "limits": "This revision is evidence-scope clarification, not independent review or publication."})
    inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
                 for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "evidence-inventory-002.json", {"files": inventory, "selfExcluded": True,
          "producerSha256": sha(Path(__file__).read_bytes()), "supersedesForFinalBinding": "evidence-inventory.json"})
    print(json.dumps({"files": len(inventory), "finalInventorySha256": sha((PACKET / "evidence-inventory-002.json").read_bytes()),
                      "formatting": formatting}, ensure_ascii=False))
finally:
    write(HERE / "finalization-memory-001.json", guard.finish())
