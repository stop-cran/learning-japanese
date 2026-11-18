"""Freeze the unchanged author handoff locally without altering its source attributes."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-131" / "review"
HANDOFF_SHA = "082957e626558f66bbddb0f4d5bee1d1e8b25a91eb811414c73e817001b8db62"
frozen(TOOLS / "prepare_b131_source_verifier.py",
       "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5")
from prepare_b131_source_verifier import derive


def main():
    source = HERE.parent / "author-handoff-001.json"
    target = HERE / "author-handoff-observed-001.json"
    output = HERE / "gate-evidence-recovery-001.json"
    require(not target.exists() and not output.exists()
            and not (TOOLS / "verify_b131_gate_evidence_v2.py").exists(), "Preserve recovery artifacts")
    failed_raw = frozen(HERE / "gate-verification-execution-001" / "receipt.json")
    failed = json.loads(failed_raw)
    log = frozen(HERE / "gate-verification-execution-001" / "output.log", failed["logSha256"])
    require(failed["exitCode"] == 1 and b"ValueError: Writable frozen input:" in log
            and b"author-handoff-001.json" in log, "Unexpected predecessor failure")
    guard, _ = start_guard("B131 author handoff immutable capture")
    try:
        raw = source.read_bytes()
        require(sha(raw) == HANDOFF_SHA, "Author handoff bytes differ from reported hash")
        capture = write_frozen(target, raw)
        require(source.read_bytes() == raw, "Author handoff changed during capture")
        derived = derive(
            "verify_b131_gate_evidence.py",
            "327e54ef5a2af1b4c92667e08256e8d0f598f13fc5460b12ada530962f9e05eb",
            "verify_b131_gate_evidence_v2.py", [
                ('HERE / "gate-verification-001"', 'HERE / "gate-verification-002"'),
                ('frozen(SCRATCH / "author-handoff-001.json", HANDOFF_SHA)',
                 'frozen(HERE / "author-handoff-observed-001.json", HANDOFF_SHA)'),
            ])
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(output, {
        "status": "PREPARATION_ONLY", "capture": capture, "derivation": derived,
        "failedReceiptSha256": sha(failed_raw), "memory": memory,
        "producerSha256": sha(frozen(Path(__file__))),
        "qualification": "The original handoff had the reported bytes but was writable on disk. "
                         "Its bytes and attributes were left unchanged. This is a new exact immutable "
                         "capture, not a claim that the original file was previously ReadOnly.",
    })))


if __name__ == "__main__":
    main()
