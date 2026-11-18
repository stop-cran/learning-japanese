"""Check actual prepared chains without creating or accepting a review closure."""
import json

from archive_b124_chains_v2 import is_local_only_source, prepare
from common import WS, freeze_json, frozen, require, sha, start_guard
from verify_b124_archive_v2 import verify_chain

ROOT = WS / "scratch-124" / "review"
CAPTURE = "6b04f0659911199f8553e154456753e4a17a3289f4dce7f1bdb1935ed1b4111f"
CHAINS = {
    "core-chain.json": "ab48edf849ec3f7cd1ad09a09f39189da9c16336d663ec62f0f8fa20237401c6",
    "confirm/N1-B124-CLAUDE-CONFIRM-001-chain.json":
        "e575edde41f60d3c06636b55299bf60726e4f00a68de48b8559afdb53580bce7",
    "confirm/N1-B124-GPT-CONFIRM-001-chain.json":
        "fb074631af77648b99f70f3d0e810f3d8747ba6e9d9ba8e857a5cfecb4efa4b3",
}


def main():
    results = []
    guard, _ = start_guard("B124 prepared-chain retention")
    try:
        for relative, digest in CHAINS.items():
            raw = frozen(ROOT / relative, digest)
            manifest = json.loads(raw)
            parts = [part for segment in manifest["segments"] for part in segment["parts"]]
            captures = [part for part in parts if part["sha256"] == CAPTURE]
            require(captures and all(is_local_only_source(part["source"]) for part in captures),
                    "Complete capture has an unrecognized publication label")
            require(all(part["sha256"] == CAPTURE for part in parts
                        if is_local_only_source(part["source"])),
                    "An additional external capture needs explicit inspection")
            files, retention = prepare(raw, {
                segment["path"]: frozen(segment["path"], segment["sha256"])
                for segment in manifest["segments"]
            })
            binding = {
                "manifestSha256": digest, "retentionSha256": sha(files["retention.json"]),
                "segments": len(manifest["segments"]),
                "archivedSegmentIndices": retention["archivedSegmentIndices"],
                "localOnlySegmentIndices": [row["index"] for row in retention["localOnlySegments"]],
            }
            results.append({"manifest": relative, **verify_chain(files, binding),
                            "localOnlySegmentIndices": binding["localOnlySegmentIndices"],
                            "captureSourceLabels": sorted({part["source"] for part in captures})})
            guard.check()
        freeze_json(ROOT / "prepared-chain-retention-verification-001.json", {
            "status": "PASS_PREPARATION_ONLY", "batch": 124, "captureSha256": CAPTURE,
            "chains": results,
            "limits": "In-memory publication representations of the actual prepared source chains. "
                      "No review acceptance, closure write or publication. The actual closure still "
                      "requires post-write verify_b124_archive_v2.py verification.",
        })
    finally:
        require(not guard.finish()["breach"], "Prepared-chain retention RAM guard breached")


if __name__ == "__main__":
    main()
