"""Exact model/long-context/no-compaction checker; only the supplied audited snapshot."""
import json
import sys
from pathlib import Path
from b131_capacity_003 import load_forecast, telemetry
from b131_review_v4_common import sha

def check(path):
    raw = Path(path).read_bytes()
    result = telemetry([json.loads(line) for line in raw.decode("utf-8").splitlines()], load_forecast())
    return {**result, "status": "PASS" if result["status"] == "PASS" else "FAIL",
            "events": str(path), "eventsSha256": sha(raw)}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Expected one audited events path")
    result = check(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["status"] == "PASS" else 1)
