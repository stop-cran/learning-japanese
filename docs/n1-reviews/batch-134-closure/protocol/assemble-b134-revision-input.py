"""Bind unchanged FRESH003 decisions to real same-reviewer revision confirmations."""
import copy
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

ROOT = WS / "scratch-134" / "review"
PRIOR = "355cccb840d22e7313e79f234eb93d1367e00352"
CANDIDATE = "cc374051efa75199212a87c9abf08d7391419055"
FAMILIES = ("claude", "gpt")
COLLECTIONS = {
    "claude": "fd9f3c289f6bff65af0b7119379eb350822a096e6dbd55484bfa9cd72f332162",
    "gpt": "af3c8e28b994e462882465106326c2669ceed8317fc8f1d058dc48b5c264a689",
}
PROOFS = {
    "scopeProof": ("revision002-scope-verification-001",
                   "6fa5d0d4cdfe4a8e2f9ca06f703c8e1bf7da0d9ce9576771174e818e6c636d6e"),
    "gateProof": ("revision002-gate-verification-001",
                  "8fa34d64fe16c821c8593778bd0af242c6420329cedea0c432b9f6294abe644a"),
}
REPAIRS = (
    ("coordinator-runtime-repair-retention-001",
     "ff68d6204a3da6e21cef9371debf8a9bf74f90b5d5a00be144bcaf6356759617"),
    ("coordinator-final-repairs-retention-001",
     "f3455d92e738103afca9efc6251a156f3b4276472f713b0b788b6487533179fd"),
)
STATUS = {
    "resolved": "RESOLVED",
    "withdrawn": "DISPUTE ACCEPTED",
    "optional": "DECLINE ACCEPTED",
}


def read_ref(ref):
    require(set(ref) == {"path", "sha256"}, "Expected an exact immutable reference")
    path = Path(ref["path"]).resolve()
    require(path.is_relative_to(ROOT), "Revision input escaped the review directory")
    return frozen(path, ref["sha256"])


def confirmation_dispositions(family, collection, original, accepted, final, decision):
    review = collection["review"]["spec"]
    run = "N1-B134-" + family.upper() + "-FRESH-003"
    require(collection["status"] == "PASS_ACCEPTED_REVIEW_COLLECTION_NOT_CLOSURE"
            and review["run"] == original["run"] == run
            and review["family"] == family and review["snapshot"] == PRIOR
            and original["candidate"] == PRIOR and original["claimsAdjudicated"] is True,
            "Original accepted FRESH003 evidence differs")
    require(accepted["batch"] == 134 and accepted["mode"] == final["mode"] == "revision"
            and re.fullmatch("N1-B134-" + family.upper() + r"-REVISION-\d{3}", accepted["run"])
            and accepted["confirmationAccepted"] is True
            and accepted["reviewEvidenceAccepted"] is True
            and accepted["verdict"] == decision["verdict"] == final["confirmation"] == "CONFIRMED"
            and accepted["acceptedNewFindings"] == accepted["openClaimIds"] == []
            and decision["acceptedNewFindings"] == decision["openClaimIds"] == []
            and accepted["publicationAccepted"] is False and accepted["deliveryCredit"] == 0,
            "A real accepted revision confirmation with no open findings is required")
    for record in (accepted, final, decision):
        require(record["candidate"] == CANDIDATE and record["session"] == review["session"]
                and record["family"] == family and record["run"] == accepted["run"]
                and record["scope"] == accepted["scope"]
                and record["priorRawVerdict"] == original["verdict"],
                "Confirmation substituted the reviewer, snapshot, scope or prior verdict")
    require(final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and decision["rawAuditWasClean"] is True
            and decision["controlAdjudicationApplied"] is False
            and decision["reportReadCompletely"] is True and decision["claimChecks"]
            and decision["limitsPreserved"]
            and decision["final"] == accepted["final"]
            and decision["report"] == final["report"] == accepted["report"]
            and accepted["producer"] == final["producer"] == decision["producer"],
            "Separate actual final/adjudication bindings are incomplete")
    rows = original["decisions"]
    expected = set(collection["requiredDispositionIds"])
    require(len(rows) == len(expected) and {row["id"] for row in rows} == expected
            and set(decision["dispositions"]) == expected,
            "Every original fresh obligation must survive exactly once")
    result = []
    for row in rows:
        identity = row["id"]
        status = row["status"]
        reason = row["reason"]
        if family == "gpt" and identity in ("F1", "F2"):
            require(status == "unresolved", "The immutable adopted finding was rewritten")
            status = "resolved"
            reason = (
                "The original adjudication remains unresolved at its original snapshot. "
                "At " + CANDIDATE + ", the signed narrow correction adds "
                + ("\u6fc3 with its historical deep-purple distinction." if identity == "F1"
                   else "\u98df with its broad foodstuff versus specific soy-sauce distinction.")
                + " The actual same-reviewer revision report and separate coordinator "
                "adjudication explicitly resolve this obligation."
            )
        require(status in STATUS and decision["dispositions"][identity] == STATUS[status]
                and reason.strip(), "Confirmation does not accept the claimed disposition")
        result.append({
            "run": run, "id": identity, "status": status, "reason": reason,
            "evidence": [
                "reviews/" + run + "/adjudication.json",
                "confirmations/" + accepted["run"] + "/report.md",
                "confirmations/" + accepted["run"] + "/adjudication.json",
            ],
        })
    return result


def main(request_path, output):
    require(output.parent == ROOT and not output.exists(), "Use a new review directory")
    request = json.loads(frozen(request_path))
    require(set(request) == set(FAMILIES), "Supply one actual acceptance ref per family")
    guard, _ = start_guard("B134 actual revision confirmation input assembly")
    try:
        reviews, adjudications, evidence, dispositions, confirmations = [], {}, [], [], {}
        for family in FAMILIES:
            collection = json.loads(frozen(
                ROOT / (family + "-fresh003-collector-001") / "review-input.json",
                COLLECTIONS[family]))
            original = json.loads(read_ref(collection["adjudication"]))
            acceptance_raw = read_ref(request[family])
            accepted = json.loads(acceptance_raw)
            final_raw = read_ref(accepted["final"])
            decision_raw = read_ref(accepted["adjudication"])
            report_raw = read_ref(accepted["report"])
            final, decision = json.loads(final_raw), json.loads(decision_raw)
            frozen(accepted["producer"]["path"], accepted["producer"]["sha256"])
            dispositions.extend(confirmation_dispositions(
                family, collection, original, accepted, final, decision))
            reviews.append(copy.deepcopy(collection["review"]))
            adjudications[original["run"]] = collection["adjudication"]
            confirmations[family] = request[family]
            for name, ref, raw in (
                ("acceptance.json", request[family], acceptance_raw),
                ("final.json", accepted["final"], final_raw),
                ("adjudication.json", accepted["adjudication"], decision_raw),
                ("report.md", accepted["report"], report_raw),
            ):
                require(sha(raw) == ref["sha256"], "Confirmation bytes changed")
                evidence.append({
                    "archivePath": "confirmations/" + accepted["run"] + "/" + name, **ref,
                })
            guard.check()
        require(len(dispositions) == 12
                and reviews[0]["spec"]["session"] != reviews[1]["spec"]["session"],
                "Expected twelve fresh obligations and two distinct original reviewers")
        for directory, digest in REPAIRS:
            for item in json.loads(frozen(ROOT / directory / "evidence.json", digest)):
                ref = {key: item[key] for key in ("path", "sha256")}
                read_ref(ref)
                evidence.append({"archivePath": item["archivePath"], **ref})
        proofs = {}
        for key, (directory, digest) in PROOFS.items():
            path = ROOT / directory / "verification.json"
            frozen(path, digest)
            proofs[key] = {"path": str(path), "sha256": digest}
        source = write_frozen(output / Path(__file__).name, Path(__file__).read_bytes())
        evidence.append({
            "archivePath": "protocol/" + Path(__file__).name,
            **{key: source[key] for key in ("path", "sha256")},
        })
        require(len({item["archivePath"] for item in evidence}) == len(evidence),
                "Duplicate archive evidence path")
        result = {
            "reviews": reviews, "adjudications": adjudications, "evidence": evidence,
            "protectedSources": [], "dispositions": dispositions,
            "revision": {
                "candidate": CANDIDATE, "priorSnapshot": PRIOR,
                "confirmations": confirmations, **proofs,
            },
            "limits": [
                "All original and FRESH003 raw verdicts and adjudications are preserved "
                "unchanged. The signed descendant and bounded confirmations are separate evidence.",
                "These twelve fresh dispositions supplement, never replace, the original "
                "twenty-nine obligations. Complete closure must account for all forty-one.",
                "Bounded confirmations do not establish exhaustive linguistic correctness, "
                "native/device/rendered-font or custom/multiple-borrow acceptance.",
                "The 51 Notes warnings and latent historical reading-pair limitation remain.",
                "No closure, integration, publication or delivery credit is granted by this input.",
            ],
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Revision input assembly RAM breach")
    result["assemblyMemory"] = memory
    print(json.dumps(freeze_json(output / "fresh-input.json", result)))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "assemble-b134-revision-input.py ACCEPTANCES_JSON NEW_REVIEW_OUTPUT")
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
