from b127_common import HERE, sha, start_guard, write

guard = start_guard()
try:
    raw = (HERE / "finalize_b127.py").read_bytes()
    write(HERE / "finalize_b127_attempt001.py", raw)
    write(HERE / "finalization-failure-001.json", {
        "producerSha256": sha(raw), "exitCode": 1,
        "failure": "UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f in position 455: character maps to <undefined>",
        "location": "finalize_b127.py line 59, default-encoding read_text of UTF-8 quiz-safety.log",
        "completedBeforeFailure": "complete-source-verification-002.json; all dictionary canonical comparisons passed.",
        "unchanged": "No producer archive, author-evidence, progress ledger or packet inventory had yet been written.",
        "recordType": "Exact exception and execution context transcribed from the tool result, not a redirected original stderr log.",
    })
finally:
    write(HERE / "finalizer-preservation-memory-001.json", guard.finish())
