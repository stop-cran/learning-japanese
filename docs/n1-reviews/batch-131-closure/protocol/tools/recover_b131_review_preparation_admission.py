"""Preserve the rejected heterogeneous roster read and use canonical status names."""
import json
from pathlib import Path

from common import freeze_json, frozen, require, sha
from prepare_b130_review_tools import derive
from prepare_b131_source_facts import HERE


def main():
    failed = HERE / "review-preparation-admission-execution-001"
    receipt_raw, log_raw = (failed / "receipt.json").read_bytes(), (failed / "output.log").read_bytes()
    receipt = json.loads(receipt_raw)
    require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 1
            and receipt["logSha256"] == sha(log_raw) and b"KeyError: 'name'" in log_raw
            and not receipt["cleanupError"] and not receipt["memory"]["breach"], "Failure differs")
    require(not (HERE / "review-preparation-admission-001.json").exists(), "Unexpected prior admission")
    for name in ("receipt.json", "output.log"):
        (failed / name).chmod(0o444)
    successor = derive("admit_b131_review_preparation.py", "admit_b131_review_preparation_v2.py", [
        ('[row["name"] for row in roster if "B131" in row["name"]]',
         '[row["name"] for row in status["sessions"] if "B131" in row["name"]]')
    ])
    print(json.dumps(freeze_json(HERE / "review-preparation-admission-recovery-001.json", {
        "status": "PREPARATION_ONLY", "derivation": successor,
        "failedReceipt": {"path": str(failed / "receipt.json"), "sha256": sha(frozen(failed / "receipt.json"))},
        "failedLog": {"path": str(failed / "output.log"), "sha256": sha(frozen(failed / "output.log"))},
        "producerSha256": sha(frozen(Path(__file__))),
        "reason": "The unfiltered roster uses title for chats and name for sessions. The full status "
                  "snapshot provides canonical names for both. V2 checks duplicates through those names "
                  "after unchanged exact roster/status ID and count equality. No row is omitted.",
        "limits": "No admission completed and no worker launched by this recovery.",
    })))


if __name__ == "__main__":
    main()
