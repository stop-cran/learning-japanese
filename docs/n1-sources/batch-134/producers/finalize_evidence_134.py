import json
from pathlib import Path

from common_134 import HERE, PACKET, sha, start_guard, write

guard = start_guard()
try:
    for dirname in ("author-gates-001", "author-gates-002"):
        for path in sorted((HERE / dirname).rglob("*")):
            if path.is_file():
                write(PACKET / "author-evidence" / path.relative_to(HERE), path.read_bytes())
    for name in ("reading-preflight-001.log", "stroke-001.json", "stroke-001-memory.json",
                 "source-attempt-001.stdout", "source-attempt-001.stderr",
                 "source-attempt-002.stdout", "source-attempt-002.stderr",
                 "verify-attempt-001.stdout", "verify-attempt-001.stderr",
                 "verify-attempt-002.stdout", "verify-attempt-002.stderr",
                 "stroke-attempt-001.stdout", "stroke-attempt-001.stderr",
                 "supplement-attempt-001.stdout", "supplement-attempt-001.stderr",
                 "pairs-attempt-001.stdout", "pairs-attempt-001.stderr",
                 "prepare-attempt-001.stdout", "prepare-attempt-001.stderr",
                 "author-gates-attempt-001.stdout", "author-gates-attempt-001.stderr",
                 "author-gates-attempt-002.stdout", "author-gates-attempt-002.stderr"):
        write(PACKET / "author-evidence" / "attempts" / name, (HERE / name).read_bytes())
    write(PACKET / "author-evidence" / "history.json", {
        "notes": [
            "Source-001 and source-002 were separately retained and verified; source-002 is the expanded review selection.",
            "An exploratory interactive read incorrectly assumed compact JSONL had a k field and failed; it modified no data. Its tool transcript is historical, not a gate result.",
            "Author gates 001 passed but quiz-safety reported 38 missing Notes mentions. Grouped precaution documentation was added; gates 002 reran all ten and reported zero quiz-safety warnings.",
            "The original preflight exposed a latent smaller-pool 紫/包 collision for historical つつむ; it is not drawable in checked production/Starter single-borrow pools."
        ],
        "limits": "Raw external captures remain local and are independently hash-bound in the source packet."})
    write(PACKET / "producers" / "finalize_evidence_134.py", Path(__file__).read_bytes())
    files = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
             for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "evidence-inventory.json", {"files": files, "algorithm": "SHA-256 of exact repository evidence bytes",
                                               "limits": "Self file excluded to avoid a circular hash."})
    print(json.dumps({"files": len(files), "inventorySha256": sha((PACKET / "evidence-inventory.json").read_bytes())}))
finally:
    write(HERE / "finalize-evidence-memory-001.json", guard.finish())
