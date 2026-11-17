"""Regression: the real auditor CLI on exact actual phase1 bytes, not audit() fixtures.

Does not select comparisons, prepare extensions, send messages, or alter existing records.
Raw local evidence stays local; stdout reports only mechanical state and output references.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROTOCOL = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-134\review\fresh-independent-002\lifecycle-011\protocol-014")
sys.path.insert(0, str(PROTOCOL))
from b134_common import frozen, sha, freeze_json
from common import load_module


def main():
    frozen(ROOT / "audit-entry.py", "9e5b4466dc0f095dac12c505269b64c89401ae2366bc9c2e823a1f161f501479")
    events = ROOT / "phase1-events.jsonl"
    events_raw = frozen(events, "d825c0a0ac290ffa539a647e015c9550436c4ac51ff273b57c130ae6e93946f1")
    config = PROTOCOL.parent / "audit-configs-020" / "audit-claude-fresh-003.json"
    frozen(config, "05688385b07d0b00a9a98077014a26aae23a6e06713c7ddb29e78855a3d12d22")
    import contextlib
    import io
    entry = load_module("b134_actual_cli_regression", ROOT / "audit-entry.py")
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = entry.main(["--session", "83324022-f15a-43cd-b54a-b9da86b500ff",
                           "--config", str(config), "--events-file", str(events)])
    match = re.search(r"^Audit: (.+)$", output.getvalue(), re.M)
    assert match, "Real CLI did not produce an audit"
    path = Path(match[1].strip())
    raw = frozen(path)
    result = json.loads(raw)
    assert code == 0 and result["status"] == "PHASE1_READY", (
        result.get("status"), result.get("error"), result.get("breaches"))
    assert frozen(path.parent / "events.jsonl") == events_raw, "Actual raw audit bytes changed"
    assert result["coreRead"] == result["coreRequired"] == 90
    assert not result["breaches"] and result["unexpectedUserMessages"] == 0
    freeze_json(ROOT / "actual-cli-regression.json", {
        "status": "PASS_REAL_PHASE1_CLI", "audit": {"path": str(path), "sha256": sha(raw)},
        "eventsSha256": sha(events_raw), "eventsBytes": len(events_raw),
        "originalAuditorSha256": entry.OLD_AUDIT_SHA,
        "repairAuditorSha256": sha(frozen(ROOT / "audit-entry.py")),
        "originalConfigSha256": sha(frozen(config)),
        "coreRead": 90, "reviewAccepted": False, "extensionPrepared": False,
        "limits": "Import-only infrastructure repair; no semantic adjudication or phase2 delivery."})
    print("PASS: real CLI on exact actual phase1 snapshot; 90 complete sources; no extension delivery.")


if __name__ == "__main__":
    main()
