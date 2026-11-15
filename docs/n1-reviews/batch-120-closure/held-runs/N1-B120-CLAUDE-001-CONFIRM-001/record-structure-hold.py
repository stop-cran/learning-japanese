"""Preserve the structural hold and open claim; do not relabel it accepted."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import freeze_json, frozen, require
from confirm_v2 import binding

HERE = Path(__file__).resolve().parent
RUN = "N1-B120-CLAUDE-001-CONFIRM-001"
final_path = HERE / f"{RUN}-final.json"
final = json.loads(frozen(final_path, "bbfcb9bb32b1de37a65b389d21c913f479036f23d5ad7e892833c97d7f796b9c"))
audit, context, structure = [
    json.loads(frozen(Path(final[key]["path"]), final[key]["sha256"]))
    for key in ("audit", "context", "structure")
]
require(final["status"] == "HOLD" and final["confirmation"] == "UNVERIFIED"
        and context["status"] == "PASS" and not context["compactions"]
        and structure["status"] == "FAIL" and structure["errors"] == [
            "Optional O1: citation source 'coordinator/pair-dispositions-neutral.md' is not in the reviewer's chain"
        ] and audit["reviewerIdle"] and not audit["breaches"]
        and audit["chainRead"] == audit["chainRequired"] == 35
        and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
        and audit["fetches"] == 0 and audit["messages"] == ["UNVERIFIED"],
        "Inspected structural hold changed")
report = frozen(Path(final["report"]["path"]), final["report"]["sha256"])
chain = json.loads(frozen(HERE / f"{RUN}-chain.json"))
canonical = "coordinator/pair-dispositions-neutral.md (substitute for the author's pair-dispositions.md)"
require(sum(source["source"] == canonical for source in chain["sources"]) == 1,
        "Missing canonical source label")
record = {
    "run": RUN, "batch": 120, "family": "claude", "session": final["session"],
    "candidate": final["candidate"], "rawVerdict": "UNVERIFIED", "status": "HELD_STRUCTURE",
    "reviewEvidenceAccepted": False, "confirmationAccepted": False, "publicationAccepted": False,
    "final": binding(final_path), "report": final["report"],
    "audit": final["audit"], "context": final["context"], "structure": final["structure"],
    "actualResponseModels": audit["actualResponseModels"], "executionNotes": audit["notes"],
    "reason": "The source identifier contains a parenthetical display annotation. The report cites "
              "its shorter filename, so the unchanged exact-citation checker correctly rejects it. "
              "No source bytes were missing and the execution/context checks passed, but this is not a passing report.",
    "canonicalSource": canonical,
    "openClaimIds": ["O1/L1"],
    "openPair": ["\u902e", "\u62bc"],
    "sourceQueries": ["\u62bc\u3055\u3048\u308b", "\u53d6\u308a\u62bc\u3055\u3048\u308b"],
    "preservation": "Original report, chain, structure failure and audit remain untouched. "
                    "Use plain path-shaped source identifiers in subsequent dossiers; do not relax the checker.",
    "substantiveObservationsNotAcceptance": {
        "O1-O4": "The CRLF decline, optional Joyo example decline, source attribution and direct following "
                 "guard agree with the actual revised text and supplied source evidence.",
        "D1/L1-initial": "The added detention guard and complete retention evidence settle the initial "
                         "question within the bounded legal/English-label qualifications.",
        "O1/L1-this-confirmation": "The exact initial comparison card for the pushing character has no "
                                  "exclusions and explicitly teaches holding down. Source evidence for its "
                                  "seizing/apprehension readings is a concrete consequential question, "
                                  "not proof of a defect or grounds for assuming every secondary sense harmless.",
        "L2": "The categorical visible-target assertion is withdrawn; retain remaining screening limits.",
        "L3-L5": "Mechanical proof is coordinator evidence; native/fallback, arbitrary-pool, fresh "
                 "whole-corpus and publication acceptance are not claimed."
    },
    "requiredFollowup": "After the independent GPT confirmation, ask the sole author to extract complete "
                        "applicable dictionary families for the pushing/holding-down and apprehending "
                        "comparison, then disposition the direct pair against both actual labels. "
                        "Reassess on the signed revision with the original reviewers.",
    "tool": binding(Path(__file__))
}
print(json.dumps(freeze_json(HERE / f"{RUN}-structure-hold.json", record)))
