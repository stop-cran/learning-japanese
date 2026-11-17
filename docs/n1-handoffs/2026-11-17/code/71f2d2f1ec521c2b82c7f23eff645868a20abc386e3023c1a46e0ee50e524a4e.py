"""Bind the B123 reconciliation handoff before running the independent verifiers."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha
from confirm_v2 import clean
from verify_b123_reconciliation_selection import main as verify_selection
from verify_b123_revision_v2 import verify as verify_revision

CANDIDATE = "65f04ca52a310d517ecb05fb17434cb4f41a118d"
REVIEW = WS / "scratch-123" / "review"
SCRATCH = WS / "scratch-123" / "reconciliation-001"
INVENTORY_SHA = "0ea13ace2b904651b4aa7f476b33ef2e53aa3999cd414173969867aa43dbdda0"
QUERY_SHA = "7806f421cf6b95c68206ade8af4b4000dd55330c3dda16f5d2ee00c67daae300"


def main():
    config = load_batch(123)
    clean(config, CANDIDATE)
    inventory_path = SCRATCH / "changed-file-inventory.json"
    raw = inventory_path.read_bytes()
    require(sha(raw) == INVENTORY_SHA, "Author inventory changed")
    inventory = json.loads(raw)
    require(inventory["head"] == CANDIDATE
            and inventory["parent"] == config["candidate"]
            and inventory["publishedBaseline"] == config["base"],
            "Inventory revision or ancestry differs")
    names = git(config, "diff", "--name-only", "--no-renames", "-z",
                config["candidate"], CANDIDATE).decode("utf-8").split("\0")
    require(set(filter(None, names)) == set(inventory["changedFiles"]),
            "Inventory does not cover the exact signed delta")
    for path, item in inventory["changedFiles"].items():
        data = git(config, "show", f"{CANDIDATE}:{path}")
        require(sha(data) == item["sha256"] and len(data) == item["bytes"],
                f"Signed inventory entry differs: {path}")
    bindings = []
    for group in ("scratchEvidenceSha256", "externalSourceSha256"):
        for path, digest in inventory[group].items():
            data = Path(path).read_bytes()
            require(sha(data) == digest, f"Handoff artifact changed: {path}")
            bindings.append({"path": path, "sha256": digest, "group": group})
    # Validate all hashes first; freezing is a post-handoff capture, not a historical claim.
    inventory_path.chmod(0o444)
    frozen(inventory_path, INVENTORY_SHA)
    for item in bindings:
        if item["group"] == "scratchEvidenceSha256":
            Path(item["path"]).chmod(0o444)
            frozen(Path(item["path"]), item["sha256"])
    tools = []
    for name in ("verify_b123_reconciliation_selection.py",
                 "test_verify_b123_reconciliation_selection.py",
                 "verify_b123_handoff.py"):
        path = Path(__file__).with_name(name)
        path.chmod(0o444)
        tools.append({"path": str(path), "sha256": sha(frozen(path))})
    proof = freeze_json(REVIEW / "reconciliation-handoff-bindings-001.json", {
        "batch": 123, "candidate": CANDIDATE, "status": "PASS",
        "inventory": {"path": str(inventory_path), "sha256": INVENTORY_SHA},
        "signedChangedFiles": inventory["changedFiles"], "artifacts": bindings, "tools": tools,
        "captureLimit": "Scratch artifacts frozen after handoff and matched to the author's "
                        "inventory; not retroactive execution-time immutability.",
        "linguisticAcceptance": False, "publicationAccepted": False,
    })
    print(json.dumps(proof))
    verify_revision(CANDIDATE, SCRATCH / "committed-gates-001", SCRATCH / "run-checks.py",
                    REVIEW / "coordinator-reconciliation-verification-001.json")
    verify_selection(CANDIDATE, QUERY_SHA,
                     REVIEW / "coordinator-reconciliation-selection-001.json")


if __name__ == "__main__":
    main()
