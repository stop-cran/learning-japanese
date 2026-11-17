"""Derive compact, hash-bound B133 CONFIRM-002 context from frozen coordinator artifacts.

Successor of derive_b133_confirmation_sources.py for reconciliation-002: the first adjudication's
18 decisions are reproduced with only the 滝-液 decision superseded by the coordinator's evidence-only
adjudication of the held GPT confirmation, and the mechanical proof comes from verification-003.
Reviewer report text is never copied into these derivatives.
"""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen
from derive_b133_confirmation_sources import DISPOSITION_FIELDS, PROOF_FIELDS, dispositions

REVIEW = WS / "scratch-133" / "review"
ADJUDICATION = REVIEW / "coordinator-adjudication-001.json"
FOLLOWUP = REVIEW / "gpt-confirm-001-adjudication-001.json"
VERIFICATION = REVIEW / "teaching-revision-verification-003" / "verification.json"
PAIR = ["滝", "液"]
REASON = ("滝-extract.txt:33 (Nihon Kokugo Daijiten 滝 [2]) records an abbreviation of 滝水, which the signed "
          "滝 card also teaches; 液-extract.txt:12 and :17 define 液 as a formless flowing substance such as "
          "water or oil. The earlier retention relied on the separate 水 guard, a third-card argument rather "
          "than a direct-pair justification. A qualified direct precaution is added; it does not claim that "
          "滝 means liquid generally or that every liquid is a waterfall.")
INITIAL = "ad047ace020579f81bde250ac948b9a4cb597887"
PARENT = "110b4ffb6af078eb2adb00645db4c9e0bd6db188"


def superseded(base, followup, digest):
    require(followup["acceptedResidual"] == {"id": "C6", "pair": "滝-液",
                                             "decision": "ADD_QUALIFIED_DIRECT_PRECAUTION",
                                             "previousDecision": "RETAINED_DISTINCTION"}
            and followup["candidate"] == PARENT and base["candidate"] == INITIAL
            and followup["findings"] == [] and followup["optionalPoints"] == [],
            "Unexpected follow-up adjudication")
    rows = [row for row in base["decisions"] if row["pair"] == PAIR]
    require(len(rows) == 1 and rows[0]["decision"] == "RETAIN_DISTINCTION", "Unexpected 滝-液 decision")
    decisions = []
    for row in base["decisions"]:
        if row["pair"] == PAIR:
            row = {**row, "decision": "ADD_QUALIFIED_DIRECT_PRECAUTION", "reason": REASON,
                   "resolutionStatus": "OPEN_PENDING_SIGNED_CHANGE_AND_CONFIRMATION",
                   "supersedes": {"decision": "RETAIN_DISTINCTION",
                                  "byCoordinatorRecord": {"path": FOLLOWUP.name, "sha256": digest}}}
        decisions.append(row)
    added = sum(row["decision"] == "ADD_QUALIFIED_DIRECT_PRECAUTION" for row in decisions)
    require(added == 12 and len(decisions) - added == 6, "Unexpected decision counts")
    boundary = json.loads(json.dumps(base["changeBoundary"], ensure_ascii=False))
    exclusions = boundary["quizExclusionsAdded"]["kanji/滝.md"]
    require("液" not in exclusions, "液 already in the first change boundary")
    boundary["quizExclusionsAdded"]["kanji/滝.md"] = [*exclusions, "液"]
    boundary["secondReconciliation"] = ("Owner-signed reconciliation-002 appends only 液 to kanji/滝.md "
                                        "quiz_exclusions with one qualified Note and a 液 citation; no other "
                                        "teaching edit.")
    return {**base, "decisions": decisions, "changeBoundary": boundary,
            "derivation": base["derivation"] + " The 滝-液 decision is superseded by the coordinator's "
                          "follow-up record; all other decisions are unchanged.",
            "reviewDisposition": "Initial reports remain unchanged. Each final confirmation must assess the "
                                 "actual signed snapshot, including the superseded 滝-液 decision.",
            "limits": "Coordinator adjudication only. No confirmation, publication, rendering, "
                      "Kotlin/native/device or whole-set acceptance."}


def proof(verification, digest):
    require(verification["status"] == "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY"
            and verification["batch"] == 133 and verification["lineageDepth"] == 2
            and verification["parent"] == PARENT
            and verification["runtimeChanged"] == ["kanji/滝.md"], "Revision verification did not pass")
    return {
        "derivedFrom": {"path": "teaching-revision-verification-003/verification.json", "sha256": digest},
        "derivation": "Mechanical subset of the coordinator's mechanical verification of reconciliation-002.",
        **{field: verification[field] for field in PROOF_FIELDS},
        "reviewedFreeze": verification["reviewedFreeze"], "lineageDepth": verification["lineageDepth"],
        "changedPathCount": len(verification["changedPaths"]),
    }


def main(output, adjudication_sha, followup_sha, verification_sha):
    output = Path(output)
    require(output.parent == REVIEW and not output.exists(), "Use a new direct child of scratch-133/review")
    base = dispositions(json.loads(frozen(ADJUDICATION, adjudication_sha)), adjudication_sha)
    followup = json.loads(frozen(FOLLOWUP, followup_sha))
    verification_raw = frozen(VERIFICATION, verification_sha)
    verification = json.loads(verification_raw)
    patch = verification["capturedExecutionFiles"]["teaching.patch"]
    patch_raw = frozen(patch["path"], patch["sha256"])
    rows = []
    for name, value in (("coordinator-dispositions-002.json", superseded(base, followup, followup_sha)),
                        ("revision-proof-002.json", proof(verification, verification_sha))):
        ref = freeze_json(output / name, value)
        rows.append({"source": "evidence/" + name, "path": ref["path"], "sha256": ref["sha256"]})
    ref = write_frozen(output / "reconciliation-002.patch", patch_raw)
    rows.append({"source": "diffs/reconciliation-002.patch", "path": ref["path"], "sha256": ref["sha256"]})
    index = freeze_json(output / "index.json", {"batch": 133, "sources": rows,
                                                "fields": list(DISPOSITION_FIELDS),
                                                "tool": {"path": __file__, "sha256": sha(Path(__file__).read_bytes())}})
    print(json.dumps(index, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:])
