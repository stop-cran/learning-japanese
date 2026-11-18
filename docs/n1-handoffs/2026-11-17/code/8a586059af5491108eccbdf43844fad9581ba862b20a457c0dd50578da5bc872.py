"""Derive compact, hash-bound B133 confirmation context from frozen coordinator artifacts."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha

REVIEW = WS / "scratch-133" / "review"
ADJUDICATION = REVIEW / "coordinator-adjudication-001.json"
VERIFICATION = REVIEW / "teaching-revision-verification-002" / "verification.json"
DISPOSITION_FIELDS = ("pair", "claimIds", "decision", "reason", "resolutionStatus")
PROOF_FIELDS = ("status", "candidate", "parent", "base", "manifestSha256", "contentVersion",
                "runtimeEntries", "runtimeChanged", "unchangedRuntimeEntries", "articles",
                "committedGates", "supplementalReadingKeys", "latentCollisions",
                "signedInventorySha256", "signedInventoryFiles", "reviewAccepted",
                "publicationAccepted", "limits", "verifierSha256")


def dispositions(adjudication, digest):
    require(adjudication["batch"] == 133 and len(adjudication["decisions"]) == 18
            and adjudication["added"] == 11 and adjudication["retained"] == 7, "Unexpected adjudication")
    return {
        "derivedFrom": {"path": "coordinator-adjudication-001.json", "sha256": digest},
        "derivation": ("Mechanical subset: every decision with pair, claim IDs, decision, reason and status; "
                       "cross-pair, optional points, policy, change boundary, review disposition and limits. "
                       "Capture line pointers are omitted because the supplied publisher-section extracts "
                       "are the evidence available to this confirmation."),
        "candidate": adjudication["candidate"],
        "policy": adjudication["policy"],
        "decisions": [{field: row[field] for field in DISPOSITION_FIELDS} for row in adjudication["decisions"]],
        "crossPair": {field: adjudication["crossPair"][field]
                      for field in ("pair", "decision", "reason", "resolutionStatus")},
        "optionalPoints": adjudication["optionalPoints"],
        "changeBoundary": adjudication["changeBoundary"],
        "reviewDisposition": adjudication["reviewDisposition"],
        "limits": adjudication["limits"],
    }


def proof(verification, digest):
    require(verification["status"] == "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY"
            and verification["batch"] == 133, "Revision verification did not pass")
    return {
        "derivedFrom": {"path": "teaching-revision-verification-002/verification.json", "sha256": digest},
        "derivation": "Mechanical subset of the coordinator's mechanical revision verification.",
        **{field: verification[field] for field in PROOF_FIELDS},
        "changedPathCount": len(verification["changedPaths"]),
    }


def main(output, adjudication_sha, verification_sha):
    output = Path(output)
    require(output.parent == REVIEW and not output.exists(), "Use a new direct child of scratch-133/review")
    adjudication = json.loads(frozen(ADJUDICATION, adjudication_sha))
    verification = json.loads(frozen(VERIFICATION, verification_sha))
    rows = []
    for name, value in (("coordinator-dispositions.json", dispositions(adjudication, adjudication_sha)),
                        ("revision-proof.json", proof(verification, verification_sha))):
        ref = freeze_json(output / name, value)
        rows.append({"source": "evidence/" + name, "path": ref["path"], "sha256": ref["sha256"]})
    index = freeze_json(output / "index.json", {"batch": 133, "sources": rows,
                                                "tool": {"path": __file__, "sha256": sha(Path(__file__).read_bytes())}})
    print(json.dumps(index))


if __name__ == "__main__":
    main(*sys.argv[1:])
