from b127_common import HERE, sha, start_guard, write

guard = start_guard()
try:
    out = HERE / "reconciliation-author-failure-001"
    producer = (HERE / "reconcile_author_b127.py").read_bytes()
    write(out / "reconcile_author_b127.py", producer)
    memory = (HERE / "reconciliation-author-001-memory.json").read_bytes()
    write(out / "memory.json", memory)
    write(out / "failure.json", {
        "operation": "First reconciliation author evidence producer",
        "exitCode": 1,
        "exception": "AttributeError: 'NoneType' object has no attribute 'group'",
        "location": "reconcile_author_b127.py:112",
        "cause": "Regex anchored with $ was applied to decoded raw CRLF instead of normalized LF. No card/record/ledger evidence outputs had been written by the failed producer.",
        "producerSha256": sha(producer), "memorySha256": sha(memory),
        "source": "Observed PowerShell execution output; original helper and finally receipt retained verbatim.",
    })
finally:
    write(HERE / "reconciliation-failure-preservation-memory-001.json", guard.finish())
