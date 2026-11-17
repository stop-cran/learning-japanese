"""Preserve the closure fix against complete real host bootstrap records."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

root = WS / "scratch-134" / "review"
output = root / "closure-host-events-preparation-001"
execution = root / "closure-bootstrap-host-events-controls-001"
require(not output.exists(), "Preserve existing host-events preparation")
receipt_raw = frozen(execution / "receipt.json",
                     "f640c4039d49b5bf946175716870f44598c471b5fe013af9fad610d70c068993")
receipt = json.loads(receipt_raw)
log = frozen(execution / "output.log", receipt["logSha256"])
require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
        and not receipt["memory"]["breach"] and receipt["cleanupError"] is None
        and b"Ran 18 tests" in log and log.rstrip().endswith(b"OK"),
        "Host-events controls did not pass")
files = {}
for name, digest in {
    "close_b134.py": "9a0e7571d444f96f7d224aaa0d964555dcc5e85b05240ca0411905f4f3563081",
    "test_close_b134.py": "d1dcb0f8550df016d0f974106be2ec45119447a48dea91a91ce1db63d8e58935",
}.items():
    files[name] = write_frozen(output / "tools" / name, frozen(WS / "review-tools" / name, digest))
for name, raw in (("receipt.json", receipt_raw), ("output.log", log)):
    files[name] = write_frozen(output / "controls" / name, raw)
snapshots = {}
for family, digest in (
    ("claude", "0332c7aa374ddaec83912b8b243a6cfed0aa1cf736bff5de00ffb9b0b0872924"),
    ("gpt", "75947d76dc4b6136ee30f1e9100b3867b94fb6fd2092d6a52a472e0bc0871dab"),
):
    path = root / f"meter-011-{family}-bootstrap-001" / "events.jsonl"
    raw = frozen(path, digest)
    events = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    snapshots[family] = {
        "path": str(path), "sha256": sha(raw), "bytes": len(raw), "events": len(events),
        "turnEnds": sum(event["type"] == "assistant.turn_end" for event in events),
        "lastType": events[-1]["type"], "rawEventsRemainLocal": True,
    }
files["producer"] = write_frozen(output / "producer.py", Path(__file__).read_bytes())
print(json.dumps(freeze_json(output / "index.json", {
    "status": "PREPARED_REAL_HOST_BOOTSTRAP_NOT_REVIEW_CLOSURE",
    "files": files, "controlsPassed": 18, "realMeterSnapshots": snapshots,
    "changes": "Require the single expected prompt response followed by turn completion. "
               "Bind the actual last event type and full raw snapshot, including trailing host "
               "bookkeeping; do not assume one model turn or truncate at assistant.turn_end.",
    "supersedes": "closure-bootstrap-preparation-001 used a synthetic-only terminal-event assumption. "
                  "Its files remain preserved but its assembler is not the current executable.",
    "limits": "Meter event shapes are regression inputs, not fresh review evidence. Matching lifecycle "
              "repair and frozen handoff remain required before reviewer admission. No teaching "
              "change, review closure, signing, push or publication.",
})))
