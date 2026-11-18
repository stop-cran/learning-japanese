import copy
import unittest

import b134_review_history as records
from b134_initial_records import INITIALS
from common import sha

REVIEWED = "355cccb840d22e7313e79f234eb93d1367e00352"


def fixture():
    inventory, entries, claims = {}, [], {}

    def ref(name, digest=None):
        digest = digest or sha(name.encode())
        inventory[name] = digest
        return {"path": name, "sha256": digest}

    for index, (family, known) in enumerate(INITIALS.items(), 1):
        run = "N1-B134-" + family.upper() + "-001"
        report = b"### O1: Optional point\n"
        claim = {"acceptedFindings": [], "openClaimIds": ["D1"], "coordinatorClaimIds": ["C1"]}
        claims[family] = {"report": report, "reportSha256": sha(report), "claims": claim}
        entry = {
            "run": run, "role": "initial", "family": family, "session": known["session"],
            "snapshot": records.CANDIDATE, "verdict": known["verdict"], "reviewAccepted": True,
            **claim,
        }
        for field in records.REVIEW_REFS:
            digest = sha(report) if field == "report" else known.get(field)
            entry[field] = ref(run + "/" + field, digest)
        entries.append(entry)
        fresh_run = "N1-B134-" + family.upper() + "-FRESH-002"
        fresh = {
            "run": fresh_run, "role": "replacement-independent", "family": family,
            "session": f"{index:08d}-1111-2222-3333-444444444444",
            "snapshot": REVIEWED, "verdict": "UNVERIFIED", "reviewAccepted": True,
            "originalSession": known["session"], "replacesInitialRun": run,
            "originalReviewerConfirmation": False,
            "acceptedFindings": [], "openClaimIds": ["L1"], "coordinatorClaimIds": [],
        }
        fresh.update({field: ref(fresh_run + "/" + field) for field in records.REVIEW_REFS})
        entries.append(fresh)
    evidence = ref("evidence/decision.json")
    closure = {
        "batch": records.BATCH, "base": records.BASE, "members": records.MEMBERS,
        "initialSnapshot": records.CANDIDATE, "reviewedSnapshot": REVIEWED,
        "publication": "PENDING", "reviewMode": records.MODE,
        "originalReviewerConfirmation": False, "reviewLineage": entries,
        "finalRuns": [row["run"] for row in entries if row["role"] == "replacement-independent"],
        "recordedFileSha256": inventory,
        "replacementBasis": {
            "reason": "original-reviewer-context-capacity", "status": "HOLD",
            "reviewAccepted": False, "measurement": ref("history/capacity.json", records.CAPACITY_SHA),
        },
        "nonAcceptedReviews": [{
            "session": records.FAILED_SESSION,
            "status": "REJECTED_PREPARATION_AND_LAUNCH_NOT_CARD_VERDICT",
            "reviewAccepted": False, "reportPresent": False,
            "rejection": ref("history/rejection.json", records.REJECTION_SHA),
        }],
    }
    resolution = {
        "batch": records.BATCH, "initialSnapshot": records.CANDIDATE, "reviewedSnapshot": REVIEWED,
        "mode": records.MODE, "originalReviewerConfirmation": False,
        "adjudicationSha256": {row["run"]: row["adjudication"]["sha256"] for row in entries},
        "remainingActionableFindings": [], "remainingConsequentialClaims": [],
        "dispositions": [],
    }
    for entry in entries:
        ids = ["O1", "D1", "C1"] if entry["role"] == "initial" else ["L1"]
        for claim_id in ids:
            resolution["dispositions"].append({
                "run": entry["run"], "id": claim_id,
                "status": "optional" if claim_id == "O1" else "resolved",
                "reason": "Synthetic evidence-based decision, not an actual review.",
                "evidence": [evidence],
            })
    return closure, resolution, claims


class ReplacementHistoryControls(unittest.TestCase):
    def test_explicit_replacement_keeps_raw_verdicts_and_all_claims(self):
        closure, resolution, claims = fixture()
        before = copy.deepcopy((closure, resolution, claims))
        records.validate_resolution(resolution, closure, REVIEWED, claims)
        self.assertEqual((closure, resolution, claims), before)
        self.assertEqual(closure["reviewLineage"][1]["verdict"], "UNVERIFIED")

    def test_history_cannot_erase_or_promote_prior_attempts(self):
        changes = (
            lambda c: c.update(originalReviewerConfirmation=True),
            lambda c: c["reviewLineage"][0].update(verdict="CLEAN"),
            lambda c: c["reviewLineage"][1].update(role="confirmation"),
            lambda c: c["reviewLineage"][1].update(confirmation="CONFIRMED"),
            lambda c: c["reviewLineage"][1].update(session=records.FAILED_SESSION),
            lambda c: c["reviewLineage"][1].update(session=INITIALS["claude"]["session"]),
            lambda c: c["reviewLineage"][1].update(originalSession=INITIALS["gpt"]["session"]),
            lambda c: c["reviewLineage"][1].update(snapshot=records.CANDIDATE),
            lambda c: c["reviewLineage"][3].update(family="claude"),
            lambda c: c.update(nonAcceptedReviews=[]),
            lambda c: c["nonAcceptedReviews"][0].update(verdict="UNVERIFIED"),
            lambda c: c["replacementBasis"].update(reviewAccepted=True),
            lambda c: c["replacementBasis"]["measurement"].update(originalSha256="0" * 64),
            lambda c: c["nonAcceptedReviews"][0]["rejection"].update(originalSha256="0" * 64),
        )
        for index, change in enumerate(changes):
            closure, _, _ = fixture()
            change(closure)
            with self.subTest(index=index), self.assertRaises(ValueError):
                records.validate_history(closure, REVIEWED)

    def test_missing_original_or_new_claim_cannot_be_hidden_by_clean_finals(self):
        closure, resolution, claims = fixture()
        for entry in closure["reviewLineage"]:
            if entry["role"] == "replacement-independent":
                entry["verdict"] = "CLEAN"
        for index in range(len(resolution["dispositions"])):
            altered = copy.deepcopy(resolution)
            altered["dispositions"].pop(index)
            with self.subTest(index=index), self.assertRaises(ValueError):
                records.validate_resolution(altered, closure, REVIEWED, claims)

    def test_unbound_unresolved_duplicated_or_substituted_claims_are_rejected(self):
        changes = (
            lambda c, r, h: r["dispositions"][0].update(status="partially resolved"),
            lambda c, r, h: r["dispositions"][0].update(reason=""),
            lambda c, r, h: r["dispositions"][0].update(evidence=[]),
            lambda c, r, h: r["dispositions"][0]["evidence"][0].update(sha256="0" * 64),
            lambda c, r, h: r["dispositions"][0]["evidence"][0].update(path="../outside.json"),
            lambda c, r, h: r["dispositions"].append(copy.deepcopy(r["dispositions"][0])),
            lambda c, r, h: r.update(remainingConsequentialClaims=["D1"]),
            lambda c, r, h: r.update(adjudicationSha256={}),
            lambda c, r, h: h["claude"].update(report=b"### O2: Replacement\n"),
            lambda c, r, h: h["claude"].update(claims={
                "acceptedFindings": [], "openClaimIds": [], "coordinatorClaimIds": []}),
            lambda c, r, h: h.pop("gpt"),
        )
        for index, change in enumerate(changes):
            closure, resolution, claims = fixture()
            change(closure, resolution, claims)
            with self.subTest(index=index), self.assertRaises(ValueError):
                records.validate_resolution(resolution, closure, REVIEWED, claims)


if __name__ == "__main__":
    unittest.main()
