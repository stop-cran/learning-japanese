"""Recheck immutable B131 preparation and signed checkout without admitting a reviewer."""
import json
import sys
from pathlib import Path

from b131_neutral_common_001 import (
    BASE, CANDIDATE, HERE, PACKET, PROOFS, RECORDS, REPO, RUNNER,
    freeze_json, frozen, load_batch, require, sha, start_guard, verify_packet)
from verify_b131_sources import FINGERPRINT, Git, OWNER


def main(output):
    output = Path(output).resolve()
    require(output.parent == HERE and not output.exists(), "Use a new direct preparation result path")
    manifest_path = HERE / "preparation-artifact-bindings-001.json"
    manifest_raw = frozen(manifest_path)
    bindings = json.loads(manifest_raw)
    guard, _ = start_guard("B131 final read-only preparation verification")
    git = Git(REPO, RUNNER, guard)
    try:
        for item in bindings["files"]:
            frozen(item["path"], item["sha256"])
            guard.check()
        root, sums, packet_sha = verify_packet(load_batch(131), guard)
        require(packet_sha == "454c924ce460d050d31eedca225b9553d42790a0060df474088e38c7ca049b39",
                "Frozen packet manifest differs")
        for name, digest in PROOFS.items():
            proof = json.loads(frozen(RECORDS / name, digest))
            require(proof["candidate"] == CANDIDATE and proof["base"] == BASE
                    and proof["status"] == "PASS" and not proof["memory"]["breach"], "Candidate proof differs")
        preflight = json.loads(frozen(HERE / "prompts" / "preflight-compact-003.json"))
        for spec in preflight["runs"].values():
            audit = json.loads(frozen(spec["auditConfig"]))
            for binding in audit["files"]:
                frozen(binding["path"], binding["sha256"])
            require(not Path(spec["report"]).exists()
                    and not (HERE / f"{spec['run']}-launch.json").exists()
                    and not (HERE / f"{spec['run']}-admission.json").exists(),
                    "This verifier is preparation-only; reviewer artifacts already exist")
        result = json.loads(frozen(HERE / "validation-003" / "result.json"))
        require(result["status"] == "PASS" and result["testsRun"] == 85
                and result["failures"] == result["errors"] == [] and not result["memory"]["breach"],
                "Focused validation did not pass")
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "B131 candidate no longer clean")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Signed owner candidate binding differs")
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Final preparation RAM breach")
    return freeze_json(output, {
        "status": "VERIFIED_PREPARATION_ONLY", "batch": 131, "candidate": CANDIDATE, "base": BASE,
        "artifactManifest": {"path": str(manifest_path), "sha256": sha(manifest_raw)},
        "packet": str(root), "packetManifestSha256": packet_sha, "packetFiles": len(sums),
        "tests": 85, "memory": memory, "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "No reviewer admission, startup, content-review acceptance or publication."})


if __name__ == "__main__":
    require(len(sys.argv) == 2, "Usage: verify_b131_preparation_001.py NEW_RESULT_JSON")
    print(json.dumps(main(sys.argv[1])))
