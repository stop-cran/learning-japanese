import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

root = WS / "scratch-134" / "review"
output = root / "closure-failed-launch-preparation-001"
execution = root / "closure-failed-launch-controls-001"
require(not output.exists(), "Preserve existing closure preparation")
receipt_raw = frozen(execution / "receipt.json")
receipt = json.loads(receipt_raw)
log = frozen(execution / "output.log", receipt["logSha256"])
require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
        and not receipt["memory"]["breach"] and receipt["cleanupError"] is None
        and b"Ran 20 tests" in log and log.rstrip().endswith(b"OK"),
        "Failed-launch retention controls did not pass")
files = {}
for name in ("close_b134.py", "test_close_b134.py"):
    files[name] = write_frozen(output / "tools" / name, frozen(WS / "review-tools" / name))
for name, raw in (("receipt.json", receipt_raw), ("output.log", log)):
    files[name] = write_frozen(output / "controls" / name, raw)
hold_path = root / "fresh-002-launch-hold-001" / "quarantine.json"
hold_raw = frozen(hold_path, "4b8eea0869cd6aaa64b3f7ec7b0418054e4c764459c1ae30b488887f5c340576")
hold = json.loads(hold_raw)
frozen(hold["events"]["path"], hold["events"]["sha256"])
files["producer"] = write_frozen(output / "producer.py", Path(__file__).read_bytes())
print(json.dumps(freeze_json(output / "index.json", {
    "status": "PREPARED_FAILED_LAUNCH_RETENTION_NOT_REVIEW_CLOSURE",
    "files": files, "controlsPassed": 20,
    "quarantine": {"path": str(hold_path), "sha256": sha(hold_raw)},
    "changes": "Archive the failed FRESH-002 prompt-only launch quarantine, retain its complete "
               "raw events and failed execution receipt locally, and exclude its run/session "
               "from fresh accepted reviews. Existing original history and full bootstrap "
               "retention remain unchanged.",
    "supersedes": "closure-host-events-preparation-001; its exact predecessor remains preserved.",
    "limits": "FRESH-003 interactive lifecycle and both actual reviews remain outstanding. "
              "No teaching edit, closure, signing, merge, push or publication.",
})))
