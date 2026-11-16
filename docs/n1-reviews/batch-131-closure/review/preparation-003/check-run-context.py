"""Acceptance precondition: the reviewer ran in the long-context tier and its context was never compacted.

Usage: python -B check-run-context.py <events.jsonl>
Exit 0 on PASS, 1 on FAIL. Prints a JSON result. Reads only the given audited event log.
"""
import hashlib
import json
import sys
from pathlib import Path

STANDARD_LIMIT = 200000


def check(path):
    raw = Path(path).read_bytes()
    tiers, limits, compactions, starts = [], set(), [], 0
    for line in raw.decode("utf-8").splitlines():
        event = json.loads(line)
        kind, data = event.get("type"), event.get("data") or {}
        if kind == "session.start":
            starts += 1
            tiers.append(data.get("contextTier"))
        elif kind == "session.usage_record":
            limits.add((data.get("usage") or {}).get("maxPromptTokens"))
        elif kind and kind.startswith("session.compaction"):
            compactions.append({"type": kind, "currentTokens": data.get("currentTokens"),
                                "tokenLimit": data.get("tokenLimit")})
    errors = []
    if starts != 1 or tiers != ["long_context"]:
        errors.append(f"Expected one session.start with contextTier long_context, found {tiers}")
    if not limits or any(not isinstance(v, int) or v <= STANDARD_LIMIT for v in limits):
        errors.append(f"Every usage record must allow more than {STANDARD_LIMIT} prompt tokens, found {sorted(limits, key=str)}")
    if compactions:
        errors.append(f"Context compaction occurred: {compactions}")
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "events": str(path),
            "eventsSha256": hashlib.sha256(raw).hexdigest(), "contextTiers": tiers,
            "maxPromptTokens": sorted(limits, key=str), "compactions": compactions}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    result = check(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["status"] == "PASS" else 1)
