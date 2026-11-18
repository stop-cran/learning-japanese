"""Preserve literal confirmation tokens without changing earlier claim statuses."""
import copy
import json
import re
import sys
from pathlib import Path

from common import freeze_json, frozen, load_module, require, sha, start_guard, write_frozen

SOURCE = Path(__file__).with_name("assemble-b134-revision-input.py")
SOURCE_SHA = "18a4085d466f9ac01535fd38e6f9a69dfc25624d52becd6c874acb3a94e827e0"
frozen(SOURCE, SOURCE_SHA)
prior = load_module("b134_revision_input_pinned_v1", SOURCE)
ROOT, PRIOR, CANDIDATE = prior.ROOT, prior.PRIOR, prior.CANDIDATE
FAMILIES, COLLECTIONS, PROOFS, REPAIRS = prior.FAMILIES, prior.COLLECTIONS, prior.PROOFS, prior.REPAIRS
STATUS, read_ref = prior.STATUS, prior.read_ref


def confirmation_tokens(family, identity, status):
    if family == "claude" and identity == "F1" and status == "withdrawn":
        return {"DISPUTE ACCEPTED", "DECLINE ACCEPTED"}
    return {STATUS[status]} if status in STATUS else set()


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
        identity, status, reason = row["id"], row["status"], row["reason"]
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
        require(decision["dispositions"][identity] in confirmation_tokens(family, identity, status)
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
    require(request["claude"]["sha256"] !=
            "18eb73b8484e457d748f7abe64b44ddfed47a25121ae6682320bc4eedf09057c",
            "The held pre-authorization Claude acceptance cannot close the revision")
    guard, _ = start_guard("B134 actual revision confirmation input assembly")
    try:
        reviews, adjudications, evidence, dispositions, confirmations, tokens = [], {}, [], [], {}, {}
        for family in FAMILIES:
            collection = json.loads(frozen(
                ROOT / (family + "-fresh003-collector-001") / "review-input.json", COLLECTIONS[family]))
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
            tokens[accepted["run"]] = copy.deepcopy(decision["dispositions"])
            for name, item, raw in (
                ("acceptance.json", request[family], acceptance_raw),
                ("final.json", accepted["final"], final_raw),
                ("adjudication.json", accepted["adjudication"], decision_raw),
                ("report.md", accepted["report"], report_raw),
            ):
                require(sha(raw) == item["sha256"], "Confirmation bytes changed")
                evidence.append({"archivePath": "confirmations/" + accepted["run"] + "/" + name, **item})
            guard.check()
        require(len(dispositions) == 12
                and reviews[0]["spec"]["session"] != reviews[1]["spec"]["session"],
                "Expected twelve fresh obligations and two distinct original reviewers")
        for directory, digest in REPAIRS:
            for item in json.loads(frozen(ROOT / directory / "evidence.json", digest)):
                item_ref = {key: item[key] for key in ("path", "sha256")}
                read_ref(item_ref)
                evidence.append({"archivePath": item["archivePath"], **item_ref})
        proofs = {}
        for key, (directory, digest) in PROOFS.items():
            path = ROOT / directory / "verification.json"
            frozen(path, digest)
            proofs[key] = {"path": str(path), "sha256": digest}
        for path, digest in ((SOURCE, SOURCE_SHA), (Path(__file__), None)):
            saved = write_frozen(output / path.name, frozen(path, digest))
            evidence.append({"archivePath": "protocol/" + path.name,
                             **{key: saved[key] for key in ("path", "sha256")}})
        require(len({item["archivePath"] for item in evidence}) == len(evidence),
                "Duplicate archive evidence path")
        result = {
            "reviews": reviews, "adjudications": adjudications, "evidence": evidence,
            "protectedSources": [], "dispositions": dispositions,
            "revision": {
                "candidate": CANDIDATE, "priorSnapshot": PRIOR,
                "confirmations": confirmations, "literalDispositionTokens": tokens, **proofs,
            },
            "limits": [
                "Original and FRESH003 raw verdicts/adjudications remain unchanged. "
                "Signed correction and authorized bounded confirmations are separate evidence.",
                "These twelve dispositions supplement, never replace, the original twenty-nine.",
                "Claude F1 may accept the editorial decline while its original withdrawn status "
                "and literal new DECLINE ACCEPTED token both remain unchanged.",
                "Authorization, semantic-tail, source and execution validity remain requirements "
                "of the actual confirmation collector; schema compatibility grants no acceptance.",
                "The 51 Notes warnings and historical reading-pair limitation remain.",
                "No native/device/rendered-font/custom-pool, closure, integration or publication credit.",
            ],
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Revision input assembly RAM breach")
    result["assemblyMemory"] = memory
    print(json.dumps(freeze_json(output / "fresh-input.json", result)))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "assemble-b134-revision-input-v2.py ACCEPTANCES_JSON NEW_REVIEW_OUTPUT")
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
