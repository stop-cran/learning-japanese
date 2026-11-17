"""Bind the second signed handoff without changing earlier evidence."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha
from confirm_v2 import clean
from verify_b123_followup_selection import verify as verify_selection
from verify_b123_reconciliation_selection import unique_object
from verify_b123_revision_v3 import PARENT, verify as verify_revision

CANDIDATE = "047970a055903c0337d73823288695938648dd1d"
REVIEW = WS / "scratch-123" / "review"
SCRATCH = WS / "scratch-123" / "reconciliation-002"
INVENTORY_SHA = "6891e15a8d2a04a249cda6dd59fc6667d69818ac02a449785be2f49a72167725"
PRIOR_INVENTORY_SHA = "0ea13ace2b904651b4aa7f476b33ef2e53aa3999cd414173969867aa43dbdda0"
QUERY_SHA = "ca94517799cd5b9b89c299f8c60b95dd98f6fa7214a9ac8e6a0a1fab97eff16a"


def main():
    config = load_batch(123)
    clean(config, CANDIDATE)
    inventory_path = SCRATCH / "changed-file-inventory.json"
    raw = inventory_path.read_bytes()
    require(sha(raw) == INVENTORY_SHA, "Author inventory changed")
    inventory = json.loads(raw, object_pairs_hook=unique_object)
    require(inventory["head"] == CANDIDATE and inventory["parent"] == PARENT
            and inventory["initialCandidate"] == config["candidate"]
            and inventory["publishedBaseline"] == config["base"]
            and inventory["previousInventorySha256"] == PRIOR_INVENTORY_SHA,
            "Inventory revision or ancestry differs")
    for parent, key in ((PARENT, "immediateParentToFinal"),
                        (config["candidate"], "initialToFinal")):
        names = git(config, "diff", "--name-only", "--no-renames", "-z",
                    parent, CANDIDATE).decode("utf-8").split("\0")
        require(set(filter(None, names)) == set(inventory[key]), "Signed path inventory differs")
    require(set(inventory["initialToFinal"]) == set(inventory["changedFiles"]),
            "Initial-to-final hash inventory is incomplete")
    for path, item in inventory["changedFiles"].items():
        data = git(config, "show", f"{CANDIDATE}:{path}")
        require(sha(data) == item["sha256"] and len(data) == item["bytes"],
                f"Signed inventory binding differs: {path}")
    prior = json.loads(frozen(SCRATCH.parent / "reconciliation-001" /
                             "changed-file-inventory.json", PRIOR_INVENTORY_SHA))
    for group in ("scratchEvidenceSha256", "externalSourceSha256"):
        for path, digest in prior[group].items():
            require(Path(path).is_relative_to(WS) and sha(Path(path).read_bytes()) == digest,
                    f"Earlier evidence changed: {path}")
    bindings = inventory["scratchEvidenceSha256"]
    for path, digest in bindings.items():
        require(Path(path).is_relative_to(SCRATCH) and sha(Path(path).read_bytes()) == digest,
                f"New handoff evidence changed or escapes scope: {path}")
    # Freeze only after every handoff hash has been verified.
    for path, digest in {str(inventory_path): INVENTORY_SHA, **bindings}.items():
        Path(path).chmod(0o444)
        frozen(Path(path), digest)
    print(json.dumps(freeze_json(REVIEW / "reconciliation-handoff-bindings-002.json", {
        "batch": 123, "status": "PASS", "candidate": CANDIDATE,
        "inventory": {"path": str(inventory_path), "sha256": INVENTORY_SHA},
        "priorEvidencePreserved": True, "artifacts": bindings,
        "signedChangedFiles": inventory["changedFiles"],
        "captureLimit": "Scratch bytes frozen after handoff against its inventory; "
                        "not retroactive execution-time immutability. Contains both response "
                        "bindings and must not be supplied to either reviewer.",
    })))
    verify_revision(CANDIDATE, SCRATCH / "committed-gates-001", SCRATCH / "run-checks.py",
                    REVIEW / "coordinator-reconciliation-verification-002.json")
    verify_selection(CANDIDATE, QUERY_SHA,
                     REVIEW / "coordinator-reconciliation-selection-002.json")


if __name__ == "__main__":
    main()
