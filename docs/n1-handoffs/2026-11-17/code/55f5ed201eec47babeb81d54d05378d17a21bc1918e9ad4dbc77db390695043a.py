import copy
import json
import unittest

import record_b133_publication as recorder
from common import json_bytes, sha


def fixture():
    entries = []
    inventory = {}
    for family in ("claude", "gpt"):
        entry = {"run": family, "family": family, "role": "initial", "session": family,
                 "snapshot": recorder.CANDIDATE, "verdict": "CLEAN", "reviewAccepted": True}
        for field in ("report", "final", "acceptance", "adjudication", "context", "structure"):
            name = f"{family}/{field}.json"
            inventory[name] = sha(name.encode())
            entry[field] = {"path": name, "sha256": inventory[name]}
        entries.append(entry)
    closure = {
        "batch": recorder.BATCH, "members": recorder.MEMBERS, "base": recorder.BASE,
        "initialSnapshot": recorder.CANDIDATE, "reviewedSnapshot": recorder.CANDIDATE,
        "publication": "PENDING", "reviewLineage": entries, "finalRuns": ["claude", "gpt"],
        "recordedFileSha256": inventory, "publicationChecks": {"uuidFindings": 0, "externalWindowFindings": 0},
    }
    manifest = json_bytes({"files": {}, "contentVersion": "fixture"})
    ledger = {
        "batch": recorder.BATCH, "members": recorder.MEMBERS, "base": recorder.BASE,
        "initialSnapshot": recorder.CANDIDATE, "reviewedSnapshot": recorder.CANDIDATE,
        "status": "textual-review-closed-publication-pending", "published": [],
        "runtimePublished": False, "reviewClosed": recorder.MEMBERS, "manifestSha256": sha(manifest),
        "review": {"closureProvenanceSha256": sha(json_bytes(closure)), "finalRuns": ["claude", "gpt"],
                   "remainingActionableFindings": [], "remainingConsequentialClaims": []},
        "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 268,
                       "publishedN1Additions": 262, "n2Placements": 6, "undelivered": 960,
                       "reviewClosedPendingRecordsWithCards": 271, "notStarted": 957},
    }
    return closure, ledger, manifest


class PublicationControls(unittest.TestCase):
    def test_requires_two_independent_final_reviews_of_the_actual_snapshot(self):
        closure, _, _ = fixture()
        recorder.validate_reviews(closure, recorder.CANDIDATE)
        cases = {
            "same session": lambda value: value["reviewLineage"][1].update(session="claude"),
            "wrong family": lambda value: value["reviewLineage"][1].update(family="claude"),
            "needs fix": lambda value: value["reviewLineage"][1].update(verdict="NEEDS FIX"),
            "unverified": lambda value: value["reviewLineage"][1].update(verdict="UNVERIFIED"),
            "not accepted": lambda value: value["reviewLineage"][1].update(reviewAccepted=False),
            "different snapshot": lambda value: value["reviewLineage"][1].update(snapshot="a" * 40),
            "duplicate final": lambda value: value.update(finalRuns=["claude", "claude"]),
            "unbound report": lambda value: value["recordedFileSha256"].pop("claude/report.json"),
            "publication finding": lambda value: value["publicationChecks"].update(externalWindowFindings=1),
        }
        for name, edit in cases.items():
            value = copy.deepcopy(closure)
            edit(value)
            with self.subTest(name), self.assertRaises((ValueError, KeyError)):
                recorder.validate_reviews(value, recorder.CANDIDATE)

        reviewed = "a" * 40
        closure["reviewedSnapshot"] = reviewed
        for initial in list(closure["reviewLineage"]):
            final = copy.deepcopy(initial)
            final.update(run=initial["run"] + "-confirm", role="confirmation",
                         snapshot=reviewed, confirmation="CONFIRMED")
            closure["reviewLineage"].append(final)
        closure["finalRuns"] = ["claude-confirm", "gpt-confirm"]
        recorder.validate_reviews(closure, reviewed)
        closure["reviewLineage"][-1]["session"] = "replacement-not-adjudicated"
        with self.assertRaises(ValueError):
            recorder.validate_reviews(closure, reviewed)

    def test_rejects_double_credit_open_findings_and_inconsistent_accounting(self):
        closure, ledger, manifest = fixture()
        raw = json_bytes(closure)
        self.assertEqual(recorder.validate_progress(ledger, recorder.CANDIDATE, manifest, raw),
                         {"delivered": 271, "n1Additions": 265, "n2Placements": 6, "remaining": 957})
        cases = {
            "already published": lambda value: value.update(published=recorder.MEMBERS),
            "runtime published": lambda value: value.update(runtimePublished=True),
            "unreviewed": lambda value: value.update(status="local-unreviewed-author-candidate"),
            "open finding": lambda value: value["review"].update(remainingActionableFindings=["F1"]),
            "open claim": lambda value: value["review"].update(remainingConsequentialClaims=["Q1"]),
            "wrong closure": lambda value: value["review"].update(closureProvenanceSha256="0" * 64),
            "wrong manifest": lambda value: value.update(manifestSha256="0" * 64),
            "wrong baseline": lambda value: value["accounting"].update(publishedPendingRecordsWithCards=269),
            "wrong remaining": lambda value: value["accounting"].update(notStarted=956),
            "wrong increment": lambda value: value["accounting"].update(reviewClosedPendingRecordsWithCards=272),
        }
        for name, edit in cases.items():
            value = copy.deepcopy(ledger)
            edit(value)
            with self.subTest(name), self.assertRaises(ValueError):
                recorder.validate_progress(value, recorder.CANDIDATE, manifest, raw)

    def test_gate_receipts_must_bind_the_actual_closure_and_commit(self):
        reviewed, commit, manifest_sha, closure_sha = recorder.CANDIDATE, "a" * 40, "b" * 64, "c" * 64
        value = {"batch": recorder.BATCH, "status": "PASS", "mode": "closure", "base": recorder.BASE,
                 "initialSnapshot": reviewed, "reviewedSnapshot": reviewed, "head": reviewed,
                 "manifestReproducible": True, "manifestSha256": manifest_sha,
                 "closureProvenanceSha256": closure_sha, "closureFiles": 13,
                 "checks": recorder.ORDER, "logs": {name: {} for name in recorder.ORDER}}
        for mode, head in (("closure", reviewed), ("committed", commit)):
            good = {**value, "mode": mode, "head": head}
            recorder.validate_gate(good, mode, reviewed, commit, manifest_sha, closure_sha, 13)
            for key, bad in (("head", "d" * 40), ("mode", "author"), ("checks", recorder.ORDER[::-1]),
                             ("manifestReproducible", False), ("closureFiles", 12),
                             ("manifestSha256", "d" * 64), ("closureProvenanceSha256", "d" * 64),
                             ("logs", {})):
                with self.subTest(mode=mode, key=key), self.assertRaises(ValueError):
                    recorder.validate_gate({**good, key: bad}, mode, reviewed, commit,
                                           manifest_sha, closure_sha, 13)


if __name__ == "__main__":
    unittest.main()
