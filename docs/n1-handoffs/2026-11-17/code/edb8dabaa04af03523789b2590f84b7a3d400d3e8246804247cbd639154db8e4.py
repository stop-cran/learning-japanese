import copy
import unittest

from common import CHECKS
from verify_b124_reconciliation import CANDIDATE, RUNNER_SHA, check_metadata, check_query_index, check_summary


class ReconciliationTests(unittest.TestCase):
    def test_metadata_preserves_readings_and_requires_every_added_guard(self):
        old = {"title": "abundant", "quizOnyomi": ["ユウ"], "quiz_exclusions": ["厚"]}
        new = {**old, "quiz_exclusions": ["厚", "多", "楽", "広"]}
        check_metadata(old, new)
        for changed in ({**new, "quizOnyomi": ["ユ"]},
                        {**new, "quiz_exclusions": ["厚", "多", "広"]},
                        {**new, "quiz_exclusions": ["多", "楽", "広"]}):
            with self.assertRaises(ValueError):
                check_metadata(old, changed)

    def test_gate_summary_cannot_substitute_parent_mode_or_manifest(self):
        config = {"base": "b" * 40, "candidate": "a" * 40}
        summary = {"batch": "124", "reconciliation": 1, "status": "PASS", "mode": "committed",
                   "publishedBase": config["base"], "reconciliationParent": config["candidate"],
                   "startingHead": CANDIDATE, "checks": list(CHECKS),
                   "manifestSha256": "m", "runnerSha256": RUNNER_SHA}
        check_summary(summary, config, "committed", "m")
        for key, value in (("startingHead", config["candidate"]), ("mode", "author"),
                           ("manifestSha256", "other"), ("publishedBase", "x" * 40)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_summary({**summary, key: value}, config, "committed", "m")

    def test_exact_query_index_does_not_accept_dropped_or_extra_membership(self):
        raw = b"<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>a</keb></k_ele></entry></JMdict>"
        metadata = {"recordSelectors": {"1": ["a"]},
                    "matchedEntryIdsByQuery": {"a": ["1"], "b": []}, "unmatchedExactQueries": ["b"]}
        check_query_index(metadata, raw, {"a", "b"})
        for identities in ([], ["1", "2"]):
            changed = copy.deepcopy(metadata)
            changed["matchedEntryIdsByQuery"]["a"] = identities
            with self.assertRaises(ValueError):
                check_query_index(changed, raw, {"a", "b"})


if __name__ == "__main__":
    unittest.main()
