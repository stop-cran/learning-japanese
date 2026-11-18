"""Verify and freeze completed outer B133 execution records without changing their bytes."""
import json
import re
import sys

from common import WS, freeze_json, frozen, require, sha, start_guard

ROOT = WS / "scratch-133" / "review"
EXPECTED_FAILURES = {
    "claude003-build-run-001", "closure-v2-dry-run-001",
    "closure-v3-dry-run-001", "closure-push-run-001",
}
RUNNER_SHA = "03260517d250b9d8071e2e70ec76fdb3ffda906d4f947e4a049375ebb249e5eb"


def main(label, names):
    require(re.fullmatch(r"[a-z0-9-]+", label) and names and len(names) == len(set(names)),
            "Use a new label and distinct execution names")
    guard, _ = start_guard("B133 completed execution preservation")
    records = {}
    try:
        for name in names:
            require(re.fullmatch(r"[a-z0-9-]+", name), "Not a direct execution directory name")
            folder = ROOT / name
            raw = (folder / "receipt.json").read_bytes()
            receipt = json.loads(raw)
            log = (folder / "output.log").read_bytes()
            require(receipt["runnerSha256"] == RUNNER_SHA and receipt["finished"]
                    and receipt["exitCode"] == (1 if name in EXPECTED_FAILURES else 0)
                    and receipt["childExitCodeAfterCleanup"] == receipt["exitCode"]
                    and receipt["cleanupError"] is None and not receipt["memory"]["breach"]
                    and receipt["logSha256"] == sha(log), f"Execution binding differs: {name}")
            for filename, content in (("receipt.json", raw), ("output.log", log)):
                path = folder / filename
                path.chmod(0o444)
                require(frozen(path, sha(content)) == content, f"Preservation changed {path}")
            records[name] = {"receiptSha256": sha(raw), "logSha256": sha(log),
                             "exitCode": receipt["exitCode"]}
            guard.check()
        print(freeze_json(ROOT / (label + ".json"), {
            "batch": 133, "executions": records, "count": len(records),
            "qualification": "Expected failed attempts remain frozen failures; no acceptance inferred.",
        }))
    finally:
        require(not guard.finish()["breach"], "Preservation RAM breach")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
