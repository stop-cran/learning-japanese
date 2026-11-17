"""Capture verified correction artifacts and test new chain retention without archiving."""
import json

from archive_b124_chains_v2 import prepare
from common import WS, freeze_json, frozen, require, sha
from prepare_b125_confirmations_002 import capture_verified
from verify_b125_archive import verify_chain

scratch = WS / "scratch-125"
review = scratch / "review"
proof = json.loads(frozen(review / "reconciliation-003-independent-proof.json",
                          "b0429c6363d34443b3d7bc9e3d385c2b22d6c0ea40c8fc4a49f2306e15687ff5"))
captured = []
for mode, bindings in proof["gateSets"].items():
    directory = scratch / bindings["directory"]
    raw = capture_verified(directory / "summary.json", bindings["summary"])
    captured.append({"path": str(directory / "summary.json"), "sha256": sha(raw)})
    for row in proof["gates"][mode]:
        for extension, field in (("json", "receiptSha256"), ("log", "logSha256")):
            path = directory / f"{row['gate']}.{extension}"
            raw = capture_verified(path, row[field])
            captured.append({"path": str(path), "sha256": sha(raw)})
scripts = scratch / "reconciliation-003-scripts"
expected = {"extract.py", "gates.py", "guarded-evidence.py", "guarded-integrity.py",
            "guarded-inventory.py", "integrity.py", "inventory.py", "reading-model.py", "reading.py"}
require({path.name for path in scripts.glob("*.py")} == expected, "Unexpected author-script inventory")
for name in sorted(expected):
    path = scripts / name
    digest = sha(path.read_bytes())
    capture_verified(path, digest)
    captured.append({"path": str(path), "sha256": digest,
                     "scope": "Post-execution capture; not a claim of execution-time immutability."})
checks = []
for family in ("CLAUDE", "GPT"):
    path = review / "confirm" / f"N1-B125-{family}-CONFIRM-002-chain.json"
    manifest_raw = frozen(path)
    manifest = json.loads(manifest_raw)
    files, retention = prepare(manifest_raw, {
        segment["path"]: frozen(segment["path"], segment["sha256"]) for segment in manifest["segments"]
    })
    binding = {
        "manifestSha256": sha(manifest_raw), "retentionSha256": sha(files["retention.json"]),
        "segments": len(manifest["segments"]), "archivedSegmentIndices": retention["archivedSegmentIndices"],
        "localOnlySegmentIndices": [row["index"] for row in retention["localOnlySegments"]],
    }
    checks.append({"family": family, **verify_chain(files, binding)})
print(freeze_json(review / "closure-input-preflight-002.json", {
    "status": "PASS_PREPARATION_ONLY", "candidate": proof["candidate"], "captured": captured,
    "newChainRetention": checks, "archiveWritten": False, "confirmationAccepted": False,
    "limits": "Verified exact local inputs and actual chain retention in memory only. No report acceptance "
              "or archive created. Complete external captures and mixed segments remain local.",
}))
