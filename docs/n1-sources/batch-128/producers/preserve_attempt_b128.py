from b128_common import HERE, sha, start_guard, write

guard = start_guard()
try:
    out = HERE / "pre-remarks-fix-001"
    raw = (HERE / "run_b128_gates.py").read_bytes()
    write(out / "run_b128_gates.py", raw)
    write(out / "failure.json", {
        "attempt": "author-gates-001",
        "gate": "linkplan", "exitCode": 1,
        "cause": "Runner omitted the existing --remarks file interface for the intentionally removed stale no-card sentence.",
        "runnerSha256": sha(raw),
        "precedingResults": "Lint: 0 errors/0 warnings; quiz safety: 0 errors/1 warning (口 comparison not repeated in Notes).",
        "remedy": "Use the tool's existing exact one-occurrence stale-remark allowance; do not weaken linkplan or revert the necessary factual correction. Add the already-justified mouth comparison to Notes.",
    })
finally:
    write(HERE / "pre-remarks-fix-001" / "memory.json", guard.finish())
