import unittest

from common import CHECKS
from verify_b121_revision_v2 import check_summary


class CommittedSummaryTests(unittest.TestCase):
    def test_exact_committed_schema_and_revision_are_required(self):
        config = {"base": "base", "candidate": "initial"}
        summary = {"status": "PASS", "mode": "committed", "base": "base", "parent": "initial",
                   "head": "revision", "checks": list(CHECKS), "manifestSha256": "manifest",
                   "manifestReproducible": True}
        check_summary(summary, config, "revision", "manifest")
        for key, value in (
            ("status", "FAIL"), ("mode", "precommit"), ("base", "other"),
            ("parent", "other"), ("head", "other"), ("checks", list(CHECKS)[:-1]),
            ("checks", [*CHECKS, CHECKS[0]]), ("manifestSha256", "other"),
            ("manifestReproducible", False),
        ):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                check_summary({**summary, key: value}, config, "revision", "manifest")

    def test_prepared_field_cannot_substitute_for_actual_head(self):
        summary = {"status": "PASS", "mode": "committed", "base": "base", "parent": "initial",
                   "startingHead": "revision", "checks": list(CHECKS),
                   "manifestSha256": "manifest", "manifestReproducible": True}
        with self.assertRaises(KeyError):
            check_summary(summary, {"base": "base", "candidate": "initial"}, "revision", "manifest")


if __name__ == "__main__":
    unittest.main()
