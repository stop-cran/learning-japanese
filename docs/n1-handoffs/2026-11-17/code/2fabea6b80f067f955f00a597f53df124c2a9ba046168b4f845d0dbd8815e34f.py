import copy
import unittest

import build_b134_revision_resolution as builder
from test_b134_revision_history import fixture


def scenario():
    closure, resolution, claims = fixture()
    original = [row for row in resolution["dispositions"] if "-FRESH-" not in row["run"]]
    fresh = [{**row, "evidence": [item["path"] for item in row["evidence"]]}
             for row in resolution["dispositions"] if "-FRESH-" in row["run"]]
    entries = closure["reviewLineage"]
    initial_refs = {row["run"]: row["adjudication"]["sha256"]
                    for row in entries if row["role"] == "initial"}
    fresh_refs = {row["run"]: row["adjudication"]
                  for row in entries if row["role"] == "replacement-independent"}
    confirmations = {}
    for row in entries:
        if row["role"] == builder.history.ROLE:
            confirmations[row["family"]] = {"run": row["run"], "ref": row["adjudication"]}
            closure["recordedFileSha256"]["confirmations/" + row["run"] + "/adjudication.json"] = (
                row["adjudication"]["sha256"])
    args = [original, initial_refs, fresh_refs, fresh, closure["recordedFileSha256"], confirmations]
    return closure, claims, args


class RevisionResolutionTests(unittest.TestCase):
    def test_built_resolution_retains_original29_and_fresh12_with_six_roles(self):
        closure, claims, args = scenario()
        before = copy.deepcopy((closure, claims, args))
        result = builder.build_resolution(*args)
        builder.history.validate_resolution(result, closure, builder.history.REVISED, claims)
        self.assertEqual((closure, claims, args), before)
        self.assertEqual(result["dispositions"][:29], args[0])
        self.assertEqual(len(result["adjudicationSha256"]), 6)

    def test_missing_claim_unbound_confirmation_and_substituted_family_rejected(self):
        changes = (
            lambda args: args[0].pop(),
            lambda args: args[3].pop(),
            lambda args: args[5].pop("gpt"),
            lambda args: args[5]["gpt"].update(run=args[5]["claude"]["run"]),
            lambda args: args[5]["gpt"]["ref"].update(sha256="0" * 64),
            lambda args: args[3][0].update(evidence=["missing"]),
            lambda args: args[3][0].update(status="unresolved"),
        )
        for change in changes:
            _, _, args = scenario()
            change(args)
            with self.subTest(change=change), self.assertRaises(ValueError):
                builder.build_resolution(*args)


if __name__ == "__main__":
    unittest.main()
