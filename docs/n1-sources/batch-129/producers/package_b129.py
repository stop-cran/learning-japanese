import json
from pathlib import Path
from b129_common import HERE, PACKET, ROOT, sha, start_guard, write

guard = start_guard()
try:
    producers = [
        "b129_common.py", "extract_b129.py", "inspect_b129.py", "supplement_b129.py",
        "supplement_b129_attempt001.py", "readback_b129.py", "final_sources_b129.py",
        "final_sources_b129_attempt001.py", "additional_sources_b129.py", "generate_b129.py",
        "editorial_b129.py", "check_reading_b129.py", "run_b129_gates.py", "preserve_b129.py",
        "package_b129.py",
    ]
    for name in producers:
        write(PACKET / "producers" / name, (HERE / name).read_bytes())
    planning_files = {}
    for path in sorted((HERE / "planning-001").rglob("*")):
        if path.is_file():
            guard.check()
            planning_files[str(path.relative_to(HERE))] = sha(path.read_bytes())
    write(PACKET / "planning-history-bindings.json", {
        "localDirectory": str(HERE / "planning-001"), "files": planning_files,
        "scope": "Original five-card survey and pre-split producer snapshots. Historical local evidence only; not final three-card gate evidence."})
    for directory in ("author-gates-001", "author-gates-002"):
        for path in sorted((HERE / directory).iterdir()):
            if path.is_file():
                write(PACKET / "author-evidence" / directory / path.name, path.read_bytes())
    for name in ("supplement-failure-001.json", "final-source-failure-001.json"):
        write(PACKET / "author-evidence" / name, (HERE / name).read_bytes())
    memories = [
        "extraction-memory-001.json", "extraction-memory-002.json", "inspection-memory-001.json",
        "supplement-memory-001.json", "supplement-memory-002.json", "supplement-memory-003.json",
        "readback-memory-001.json", "final-source-memory-001.json", "final-source-memory-002.json",
        "generation-memory-001.json", "additional-source-memory-001.json", "editorial-memory-001.json",
    ]
    for name in memories:
        write(PACKET / "author-evidence" / name, (HERE / name).read_bytes())
    local_logs = {}
    for path in sorted(HERE.glob("*.log")):
        local_logs[path.name] = {"sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}
    write(PACKET / "failure-history.json", {
        "fiveMemberSupplementAttempt001": json.loads((HERE / "supplement-failure-001.json").read_text(encoding="utf8")),
        "finalSourceAttempt001": json.loads((HERE / "final-source-failure-001.json").read_text(encoding="utf8")),
        "authorGates001": {"status": "FAILED", "gate": "lint", "errors": 6,
                           "reason": "H1 hyphens and nonstandard facts lines; corrected to repository format. Original log/receipt preserved under author-evidence/author-gates-001."},
        "authorGates002": {"status": "PASS", "gates": 10, "directory": str(HERE / "author-gates-002"),
                           "summarySha256": sha((HERE / "author-gates-002" / "summary.json").read_bytes())},
        "localLogBindings": local_logs,
        "preservation": "No failed evidence directory is overwritten or relabelled; all complete external captures remain local."})
    lean = ROOT / "lean"
    write(PACKET / "tool-bindings.json", {
        "leanTools": {name: sha((lean / name).read_bytes()) for name in
                      ("n1lib.py", "n1_batch_tool.py", "quiz_safety.py", "n1_linkplan.py", "reading_exposure.py", "reading_options.py")},
        "environment": {"N1_REPO": str(ROOT / "b129-worktree"), "PYTHONIOENCODING": "utf-8",
                        "PYTHONDONTWRITEBYTECODE": "1", "pythonFlag": "-B"},
        "sourceByteHashes": "Original raw bytes; do not normalize frozen external/source evidence.",
        "runtimeTextHashes": "CRLF normalized to LF; n1lib.read normalizes before parse.",
        "guardPolicy": "Pinned RAM guard; >2 GiB admission, 0.25 s sampling, abort <1 GiB. Child wait <=0.1 s. Own-PID terminate and kill stages bounded at 10 s each."})
    inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
                 for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "evidence-inventory.json", {"files": inventory, "selfExcluded": True,
          "producerSha256": sha(Path(__file__).read_bytes()),
          "limits": "Raw-byte binding of the final contributor packet, excluding this inventory itself. Committed snapshot and runtime hashes are independently bound by local preservation receipts."})
    print(json.dumps({"packetFilesBound": len(inventory), "planningFilesBound": len(planning_files),
                      "inventorySha256": sha((PACKET / "evidence-inventory.json").read_bytes())}))
finally:
    write(HERE / "packaging-memory-001.json", guard.finish())
