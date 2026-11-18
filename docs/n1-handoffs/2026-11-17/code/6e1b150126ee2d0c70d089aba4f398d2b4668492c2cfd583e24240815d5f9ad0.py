import copy
import unittest

import b134_revision_history as records
from common import sha
from test_b134_review_history import fixture as prior_fixture


def fixture():
    closure, resolution, claims = prior_fixture()
    inventory = closure["recordedFileSha256"]

    def ref(name, digest=None):
        digest = digest or sha(name.encode())
        inventory[name] = digest
        return {"path": name, "sha256": digest}

    for row in closure["reviewLineage"]:
        if row["role"] == "replacement-independent":
            old_run = row["run"]
            row["run"] = old_run.replace("FRESH-002", "FRESH-003")
            row["session"] = records.SESSIONS[row["family"]]
            row["verdict"] = "NEEDS FIX"
            row["acceptedFindings"] = []
            row["openClaimIds"] = list(records.OBLIGATIONS[row["family"]])
    closure["finalRuns"] = [row["run"] for row in closure["reviewLineage"]
                            if row["role"] == "replacement-independent"]
    resolution["dispositions"] = [row for row in resolution["dispositions"]
                                  if "FRESH" not in row["run"]]
    first = closure["reviewLineage"][0]
    additions = ["C" + str(i) for i in range(2, 25)]
    first["coordinatorClaimIds"].extend(additions)
    for identity in additions:
        resolution["dispositions"].append({
            "run": first["run"], "id": identity, "status": "withdrawn",
            "reason": "Synthetic history fixture only.", "evidence": [ref("evidence/decision.json")],
        })
    for family in ("claude", "gpt"):
        entry = {
            "run": "N1-B134-" + family.upper() + "-REVISION-002", "role": records.ROLE,
            "family": family, "session": records.SESSIONS[family],
            "priorRun": "N1-B134-" + family.upper() + "-FRESH-003",
            "snapshot": records.REVISED, "priorSnapshot": records.PRIOR, "mode": "revision",
            "verdict": "CONFIRMED", "priorRawVerdict": "NEEDS FIX",
            "reviewAccepted": True, "confirmationAccepted": True,
            "originalReviewerConfirmation": False, "acceptedNewFindings": [], "openClaimIds": [],
            "publicationAccepted": False, "deliveryCredit": 0, "dispositions": {},
        }
        for field in (*records.prior.REVIEW_REFS, "authorization", "preflight", "admission"):
            entry[field] = ref("confirmations/" + entry["run"] + "/" + field)
        for identity in records.OBLIGATIONS[family]:
            entry["dispositions"][identity] = (
                "DECLINE ACCEPTED" if family == "claude"
                else "RESOLVED" if identity in ("F1", "F2") else "DISPUTE ACCEPTED")
            status = ("withdrawn" if family == "claude" and identity == "F1"
                      else "optional" if family == "claude"
                      else "resolved" if identity in ("F1", "F2") else "withdrawn")
            resolution["dispositions"].append({
                "run": entry["priorRun"], "id": identity, "status": status,
                "reason": "Synthetic confirmation fixture only.",
                "evidence": [entry["report"], entry["adjudication"]],
            })
        closure["reviewLineage"].append(entry)
    closure.update({
        "schemaVersion": 2, "reviewMode": records.MODE,
        "reviewedSnapshot": records.REVISED, "priorReviewedSnapshot": records.PRIOR,
        "confirmationRuns": [row["run"] for row in closure["reviewLineage"] if row["role"] == records.ROLE],
        "revisionProofs": {key: ref("verification/revision-" + key, digest)
                           for key, digest in records.PROOFS.items()},
        "continuationHistory": {"scopeHold": ref("history/scope-hold.json", records.HOLD_SHA)},
    })
    resolution.update({
        "mode": records.MODE, "reviewedSnapshot": records.REVISED, "priorReviewedSnapshot": records.PRIOR,
        "adjudicationSha256": {row["run"]: row["adjudication"]["sha256"]
                              for row in closure["reviewLineage"]},
    })
    return closure, resolution, claims


class RevisionHistoryTests(unittest.TestCase):
    def test_six_roles_four_sessions_forty_one_claims_preserved_without_mutation(self):
        closure, resolution, claims = fixture()
        before = copy.deepcopy((closure, resolution, claims))
        records.validate_resolution(resolution, closure, records.REVISED, claims)
        self.assertEqual((closure, resolution, claims), before)
        self.assertEqual(len(resolution["dispositions"]), 41)
        with self.assertRaises(ValueError):
            records.prior.validate_history(closure, records.REVISED)

    def test_substituted_relabelled_held_or_unbound_confirmation_fails(self):
        changes = (
            lambda c: c["reviewLineage"][-1].update(session=records.SESSIONS["claude"]),
            lambda c: c["reviewLineage"][-1].update(priorSnapshot=records.REVISED),
            lambda c: c["reviewLineage"][-1].update(originalReviewerConfirmation=True),
            lambda c: c["reviewLineage"][-1].update(confirmationAccepted=False),
            lambda c: c["reviewLineage"][-1].update(deliveryCredit=1),
            lambda c: c["reviewLineage"][-1]["authorization"].update(sha256="0" * 64),
            lambda c: c["reviewLineage"][-1]["dispositions"].update(F1="DECLINE ACCEPTED"),
            lambda c: c["reviewLineage"][-2]["acceptance"].update(originalSha256=records.HELD_CLAUDE_SHA),
            lambda c: c["continuationHistory"]["scopeHold"].update(originalSha256="0" * 64),
            lambda c: c["reviewLineage"][1].update(verdict="CLEAN"),
            lambda c: c["reviewLineage"].pop(),
        )
        for change in changes:
            closure, _, _ = fixture()
            change(closure)
            with self.subTest(change=change), self.assertRaises(ValueError):
                records.validate_history(closure, records.REVISED)

    def test_no_missing_claim_rewritten_status_or_other_family_evidence(self):
        changes = (
            lambda c, r: r["dispositions"].pop(),
            lambda c, r: r["dispositions"][-8].update(status="withdrawn"),
            lambda c, r: r["dispositions"][-12].update(status="optional"),
            lambda c, r: r["dispositions"][-1].update(evidence=[c["reviewLineage"][-2]["report"]]),
            lambda c, r: r["adjudicationSha256"].pop(c["confirmationRuns"][0]),
        )
        for change in changes:
            closure, resolution, claims = fixture()
            change(closure, resolution)
            with self.subTest(change=change), self.assertRaises(ValueError):
                records.validate_resolution(resolution, closure, records.REVISED, claims)


if __name__ == "__main__":
    unittest.main()
