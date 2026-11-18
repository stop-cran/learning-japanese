from b127_common import HERE, sha, start_guard, write

guard = start_guard()
try:
    files = {}
    for name in ("b127_common.py", "run_b127_gates.py", "finalize_b127.py"):
        raw = (HERE / name).read_bytes()
        write(HERE / "pre-cleanup-fix-001" / name, raw)
        files[name] = sha(raw)
    write(HERE / "pre-cleanup-fix-001" / "receipt.json", {
        "reason": "Coordinator identified inherited exceptional-cleanup risk. Existing <=0.1-second individual waits lacked an aggregate post-kill deadline; preserve executed sources before adding deadlines and cleanup-error receipts.",
        "files": files, "historicalGateDirectories": ["author-gates-001", "author-gates-002"],
    })
finally:
    write(HERE / "runner-preservation-memory-001.json", guard.finish())
