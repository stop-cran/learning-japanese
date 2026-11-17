"""Derive compact, hash-bound B133 CONFIRM-003 context from frozen coordinator artifacts.

Successor of derive_b133_confirmation_sources_v2.py for reconciliation-003. The frozen CONFIRM-002
dispositions are reproduced with only two changes required by the evidence-only adjudication of fresh
Claude CONFIRM-002: the 滝-液 reason drops the withdrawn "water from a waterfall" gloss, and one 滝-酒
precaution row is added. The mechanical proof and exact diffs come from verification-004.
Reviewer report text is never copied into these derivatives.
"""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen
from derive_b133_confirmation_sources import DISPOSITION_FIELDS, PROOF_FIELDS

REVIEW = WS / "scratch-133" / "review"
DISPOSITIONS = REVIEW / "confirmation-sources-004" / "coordinator-dispositions-002.json"
ADJUDICATION = REVIEW / "claude-confirm-002-adjudication-001.json"
VERIFICATION = REVIEW / "teaching-revision-verification-004" / "verification.json"
PARENT = "d7d6cff92afe8220c16a5daa76f1c3f00a2bef30"
LIQUID, SAKE = ["滝", "液"], ["滝", "酒"]
LIQUID_REASON = (
    "滝-extract.txt:29 and :31 (日本国語大辞典 滝 [1]) describe 滝 as water flowing violently down a slope or "
    "falling from a cliff; 滝-extract.txt:74 (字通) records the gloss ひたす、うるおす; 滝-extract.txt:33 "
    "(日本国語大辞典 滝 [2]) records an abbreviation of たきすい, which takisui-sections.txt:4-5 identifies as a "
    "drink, an Edo-period brand of sake. 液-extract.txt:12 and :17 define 液 as a formless flowing substance "
    "such as water or oil. The earlier gloss of the abbreviation as water from a waterfall is withdrawn by "
    "the coordinator's CONFIRM-002 adjudication and is not a ground. A qualified direct precaution is kept; "
    "it does not claim that 滝 means liquid generally or that every liquid is a waterfall.")
SAKE_REASON = (
    "滝-extract.txt:33-34 (日本国語大辞典 滝 [2]) records 滝 as an abbreviation of たきすい with the 1791 "
    "洒落本 example 「たきがあらばちっとわってくんねへ」; takisui-sections.txt:4-5 defines たきすい【滝水】 as a "
    "brand of sake sold by a 神田和泉町 sake shop in Edo, while takisui-sections.txt:6-9 assign the "
    "waterfall-water senses to the separate readings たきみず and ろうすい. The signed 酒 card is titled "
    "'alcohol; sake'. Following the conservative 霜-酒 precedent and the historical/secondary-sense guards "
    "遅, 円, 岩 and 険, a qualified direct precaution is added. It is not a synonymy claim and does not teach "
    "滝 as meaning alcohol.")
POINTER_NOTE = (
    "Coordinator correction: the CONFIRM-002 adjudication acknowledged reviewer point L8 that the 液 pointers "
    ":12 and :17 were offset by one. Rechecking the frozen 液-extract.txt (eb3107d6) and the CONFIRM-002 chain "
    "mapping (segment 9, source lines 1-19 = segment lines 129-147; definitions at segment lines 140 and "
    "145) shows that :12 and :17 are correct; that acknowledgement was mistaken. The frozen records are not "
    "rewritten.")


def amended(base, adjudication, digest, base_digest):
    require(adjudication["confirmation"] == "UNVERIFIED" and adjudication["candidate"] == PARENT
            and base["candidate"] == "ad047ace020579f81bde250ac948b9a4cb597887" and adjudication["findings"] == []
            and adjudication["acceptedResiduals"] == [
                {"id": "O1-gloss", "pair": None, "decision": "CORRECT_UNSUPPORTED_GLOSS",
                 "scope": "kanji/滝.md Meaning sentence and 液 Note rationale only"},
                {**adjudication["acceptedResiduals"][1], "id": "O1-sake", "pair": "滝-酒",
                 "decision": "ADD_QUALIFIED_DIRECT_PRECAUTION"}]
            and len(adjudication["acceptedResiduals"]) == 2, "Unexpected CONFIRM-002 adjudication")
    rows = [row for row in base["decisions"] if row["pair"] == LIQUID]
    require(len(rows) == 1 and rows[0]["decision"] == "ADD_QUALIFIED_DIRECT_PRECAUTION"
            and "supersedes" in rows[0] and not any(row["pair"] == SAKE for row in base["decisions"]),
            "Unexpected 滝-液/滝-酒 decisions")
    record = {"path": ADJUDICATION.name, "sha256": digest}
    decisions = []
    for row in base["decisions"]:
        if row["pair"] == LIQUID:
            row = {**row, "reason": LIQUID_REASON,
                   "reasonAmended": {"withdrawn": "Gloss of the 滝水 abbreviation as water from a waterfall.",
                                     "byCoordinatorRecord": record}}
        decisions.append(row)
        if row["pair"] == LIQUID:
            decisions.append({"pair": SAKE, "claimIds": ["Claude fresh CONFIRM-002 O1"],
                              "decision": "ADD_QUALIFIED_DIRECT_PRECAUTION", "reason": SAKE_REASON,
                              "resolutionStatus": "OPEN_PENDING_SIGNED_CHANGE_AND_CONFIRMATION",
                              "addedByCoordinatorRecord": record})
    added = sum(row["decision"] == "ADD_QUALIFIED_DIRECT_PRECAUTION" for row in decisions)
    require(len(decisions) == 19 and added == 13 and len(decisions) - added == 6, "Unexpected decision counts")
    boundary = json.loads(json.dumps(base["changeBoundary"], ensure_ascii=False))
    exclusions = boundary["quizExclusionsAdded"]["kanji/滝.md"]
    require(exclusions[-1] == "液" and "酒" not in exclusions, "Unexpected second change boundary")
    boundary["quizExclusionsAdded"]["kanji/滝.md"] = [*exclusions, "酒"]
    boundary["thirdReconciliation"] = (
        "Owner-signed reconciliation-003 changes only kanji/滝.md: 酒 is appended after 液 in quiz_exclusions "
        "with one qualified 酒 Note and a 滝水 citation; the Meaning sentence and the 液 Note rationale are "
        "corrected so that the 滝水 abbreviation is the Edo sake name, not waterfall water.")
    boundary["glossCorrection"] = {"decision": "CORRECT_UNSUPPORTED_GLOSS",
                                   "scope": "kanji/滝.md Meaning sentence and 液 Note rationale only",
                                   "byCoordinatorRecord": record}
    return {**base, "derivedFrom": {**base["derivedFrom"],
                                    "via": [{"path": "confirmation-sources-004/" + DISPOSITIONS.name,
                                             "sha256": base_digest}, record]},
            "decisions": decisions, "changeBoundary": boundary,
            "derivation": base["derivation"] + " For CONFIRM-003 the 滝-液 reason is amended and one 滝-酒 row "
                          "is added by the coordinator's evidence-only adjudication of fresh Claude CONFIRM-002; "
                          "all other rows are unchanged.",
            "pointerCorrection": POINTER_NOTE,
            "reviewDisposition": "Initial reports and earlier confirmation reports remain unchanged. Each final "
                                 "confirmation must assess the actual signed snapshot, including the amended "
                                 "滝-液 reason, the 滝-酒 precaution and the corrected 滝水 gloss.",
            "limits": "Coordinator adjudication only. No confirmation, publication, rendering, "
                      "Kotlin/native/device or whole-set acceptance."}


def proof(verification, digest):
    require(verification["status"] == "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY"
            and verification["batch"] == 133 and verification["lineageDepth"] == 3
            and verification["parent"] == PARENT
            and verification["runtimeChanged"] == ["kanji/滝.md"], "Revision verification did not pass")
    return {
        "derivedFrom": {"path": "teaching-revision-verification-004/verification.json", "sha256": digest},
        "derivation": "Mechanical subset of the coordinator's mechanical verification of reconciliation-003.",
        **{field: verification[field] for field in PROOF_FIELDS},
        "reviewedFreeze": verification["reviewedFreeze"], "lineageDepth": verification["lineageDepth"],
        "changedPathCount": len(verification["changedPaths"]),
    }


def main(output, dispositions_sha, adjudication_sha, verification_sha):
    output = Path(output)
    require(output.parent == REVIEW and not output.exists(), "Use a new direct child of scratch-133/review")
    base = json.loads(frozen(DISPOSITIONS, dispositions_sha))
    adjudication = json.loads(frozen(ADJUDICATION, adjudication_sha))
    verification = json.loads(frozen(VERIFICATION, verification_sha))
    files = verification["capturedExecutionFiles"]
    rows = []
    for name, value in (("coordinator-dispositions-003.json",
                         amended(base, adjudication, adjudication_sha, dispositions_sha)),
                        ("revision-proof-003.json", proof(verification, verification_sha))):
        ref = freeze_json(output / name, value)
        rows.append({"source": "evidence/" + name, "path": ref["path"], "sha256": ref["sha256"]})
    patch = files["teaching.patch"]
    ref = write_frozen(output / "reconciliation-003.patch", frozen(patch["path"], patch["sha256"]))
    rows.append({"source": "diffs/reconciliation-003.patch", "path": ref["path"], "sha256": ref["sha256"]})
    index = freeze_json(output / "index.json", {"batch": 133, "sources": rows,
                                                "fields": list(DISPOSITION_FIELDS),
                                                "tool": {"path": __file__, "sha256": sha(Path(__file__).read_bytes())}})
    print(json.dumps(index, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:])
