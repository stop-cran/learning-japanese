"""Preserve the tested bootstrap-aware closure assembler, not review acceptance."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

root = WS / "scratch-134" / "review"
output = root / "closure-bootstrap-preparation-001"
execution = root / "closure-bootstrap-controls-execution-002"
require(not output.exists(), "Preserve the existing bootstrap assembler preparation")
receipt_raw = (execution / "receipt.json").read_bytes()
receipt = json.loads(receipt_raw)
log = (execution / "output.log").read_bytes()
require(sha(receipt_raw) == "154bdf54f17463d829332c293c777ab17df0a4f9dbcf93c2b8c3e57e629d0473"
        and receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
        and not receipt["memory"]["breach"] and receipt["cleanupError"] is None
        and sha(log) == receipt["logSha256"] and b"Ran 12 tests" in log and b"\nOK" in log,
        "Current bootstrap controls did not pass")
files = {}
for name, digest in {
    "close_b134.py": "0f750e78fbc0a9f4c2c70296e4478178851de46d0ccfbd02e0c6b6995eecd461",
    "test_close_b134.py": "acc809b3fb1dc81bd2ce25c5a2bae51386a726ed89b580f1a81ac7046d02e2cc",
}.items():
    files[name] = write_frozen(output / "tools" / name, frozen(WS / "review-tools" / name, digest))
for name, raw in (("receipt.json", receipt_raw), ("output.log", log)):
    files[name] = write_frozen(output / "controls" / name, raw)
files["producer"] = write_frozen(output / "producer.py", Path(__file__).read_bytes())
result = {
    "status": "PREPARED_BOOTSTRAP_BINDINGS_NOT_REVIEW_CLOSURE",
    "files": files,
    "controlsPassed": 12,
    "changes": "Archive prompt-only bootstrap and core authorization; bind run, session, snapshot, "
               "initial candidate base, exact config/model/context/prompt, and complete raw bootstrap "
               "prefix in final audited events. Raw events remain local.",
    "preservedEarlierAttempt": "closure-bootstrap-controls-execution-001 passed synthetic controls "
                               "but used an inaccurate profile/base fixture; execution-002 uses the "
                               "current lifecycle interface and supersedes it.",
    "limits": "Actual frozen lifecycle handoff and accepted-review assembly remain pending. "
              "No reviewer admitted, teaching changed, claim closed, commit made or publication credited.",
}
print(json.dumps(freeze_json(output / "index.json", result)))
