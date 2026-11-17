"""Capture exact previously verified historical gates; do not rerun or relabel them."""
import json

from common import WS, freeze_json, frozen, require, sha
from finalize_b125_v2 import PROOFS
from prepare_b125_confirmations_002 import capture_verified
from verify_b125_reconciliation_001 import SUMMARY_HASHES
from verify_b125_reconciliation_002 import DRIVER_SHA, GATE_HASHES

scratch = WS / "scratch-125"
captured = []
for number in (1, 2):
    proof = json.loads(frozen(
        scratch / "review" / f"reconciliation-{number:03}-independent-proof.json", PROOFS[number]))
    for mode, gates in proof["gates"].items():
        directory = scratch / f"reconciliation-{number:03}-{mode}-gates-001"
        summary_sha = SUMMARY_HASHES[mode] if number == 1 else GATE_HASHES[mode]["summary"]
        bindings = {"summary.json": summary_sha}
        for row in gates:
            bindings[f"{row['gate']}.json"] = row["receiptSha256"]
            bindings[f"{row['gate']}.log"] = row["logSha256"]
        require(len(bindings) == 21, "Historical gate set is incomplete")
        for name, digest in bindings.items():
            path = directory / name
            raw = capture_verified(path, digest)
            captured.append({"path": str(path), "sha256": sha(raw)})
for name, digest in {
    "reconciliation-001-gates.py": "077b33ed341ae7a5417d676feafeb3b262edabe300b21fced3cfe6ac38036c9a",
    "reconciliation-002-gates.py": DRIVER_SHA,
}.items():
    path = scratch / name
    capture_verified(path, digest)
    captured.append({"path": str(path), "sha256": digest})
print(freeze_json(scratch / "review" / "historical-closure-input-capture-001.json", {
    "status": "PASS", "captured": captured,
    "reason": "Finalization001 refused a writable historical author summary before writing artifacts.",
    "limits": "Post-execution ReadOnly capture after exact original proof/verifier bindings. "
              "No execution-time immutability claim, new test execution or changed historical status.",
}))
