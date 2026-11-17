"""Freeze byte-identical tested runtime copies; originals remain untouched here."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

HERE = Path(__file__).parent
success_path, receipt_path = map(Path, sys.argv[1:])
success, receipt = (json.loads(frozen(path)) if path == success_path else json.loads(path.read_bytes())
                    for path in (success_path, receipt_path))
require(success["syntheticOnly"] is True and success["actualReviewerAdmission"] is False
        and success["testsRun"] == 7 and receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
        and receipt["cleanupError"] is None and not receipt["memory"]["breach"]
        and receipt["runnerSha256"] == "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"
        and receipt["guardSha256"] == "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"
        and sha((receipt_path.parent / "output.log").read_bytes()) == receipt["logSha256"],
        "Current guarded controls required")
guard, _ = start_guard("B134 stage tested immutable runtime")
try:
    files = {}
    for name, digest in success["selectedTools"].items():
        raw = (WS / "review-tools" / name).read_bytes()
        require(sha(raw) == digest, "Tool changed since tested snapshot")
        files[name] = write_frozen(HERE / "selected-runtime-001" / name, raw)
        guard.check()
finally:
    memory = guard.finish()
require(not memory["breach"], "Runtime staging RAM breach")
freeze_json(HERE / "selected-runtime-001" / "index.json",
            {"files": files, "controls": {"path": str(success_path), "sha256": sha(frozen(success_path))},
             "receipt": {"path": str(receipt_path), "sha256": sha(receipt_path.read_bytes())}, "memory": memory})
