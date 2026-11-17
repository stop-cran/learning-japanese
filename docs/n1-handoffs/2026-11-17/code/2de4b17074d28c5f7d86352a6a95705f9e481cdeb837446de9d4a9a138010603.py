"""Freeze only the tested continuation adapter and unchanged tested proof binder."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

HERE = Path(__file__).parent
controls = HERE / "continuation-controls-e12ac73acc5d43ec8028d32727abfd06.json"
receipt = HERE.parent / "confirmation-continuation-v2-tests-001" / "receipt.json"
record, execution = json.loads(frozen(controls)), json.loads(receipt.read_bytes())
require(record["testsRun"] == 2 and execution["exitCode"] == execution["childExitCodeAfterCleanup"] == 0
        and not execution["memory"]["breach"] and execution["cleanupError"] is None
        and sha((receipt.parent / "output.log").read_bytes()) == execution["logSha256"],
        "Guarded continuation controls failed")
guard, _ = start_guard("B134 stage explicit continuation-v2")
try:
    files = {}
    for name, digest in record["tools"].items():
        raw = (WS / "review-tools" / name).read_bytes()
        require(sha(raw) == digest, "Continuation implementation changed since tested")
        files[name] = write_frozen(HERE / "selected-runtime-003" / name, raw)
        guard.check()
finally:
    memory = guard.finish()
require(not memory["breach"], "Continuation staging RAM breach")
freeze_json(HERE / "selected-runtime-003" / "index.json",
            {"files": files, "controls": {"path": str(controls), "sha256": sha(frozen(controls))},
             "receipt": {"path": str(receipt), "sha256": sha(receipt.read_bytes())}, "memory": memory})
