import copy
import json
import unittest

from common import CHECKS, git, load_batch
from verify_b124_reconciliation_002 import (
    CARD, COMPARISONS, PARENT, PREFIX, PREVIOUS_PREFIX, RUNNER_SHA,
    check_card, check_dispositions, check_summary, parse,
)

CANDIDATE = "be2aaeac504be19860a9a69de499d8202863bde9"


class SecondCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_batch(124)
        blob = lambda commit, path: git(cls.config, "show", f"{commit}:{path}")
        cls.old_card, cls.new_card = blob(PARENT, CARD), blob(CANDIDATE, CARD)
        cls.dispositions = json.loads(blob(CANDIDATE, PREFIX + "dispositions.json"))
        cls.old_dispositions = json.loads(blob(PARENT, PREVIOUS_PREFIX + "dispositions.json"))
        cls.receipt = json.loads(blob(PARENT, PREVIOUS_PREFIX + "source-receipt.json"))
        cls.titles = {char: parse(blob(CANDIDATE, f"kanji/{char}.md").decode("utf-8")
                                 .replace("\r\n", "\n"))[0]["title"]
                      for char in {"\u88d5", *COMPARISONS}}

    def test_preserves_card_body_and_rejects_changed_readings_or_missing_guards(self):
        check_card(self.old_card, self.new_card)
        for changed in (
            self.new_card.replace("quizOnyomi: [ユウ]".encode(), "quizOnyomi: [ユ]".encode()),
            self.new_card.replace("剰, 満".encode(), "満".encode()),
            self.new_card.replace(b"omits ", b"includes "),
            self.new_card.replace(b"do not assert synonymy", b"assert synonymy"),
        ):
            with self.assertRaises(ValueError):
                check_card(self.old_card, changed)

    def test_exact_labels_selectors_and_direct_endpoint_decisions(self):
        check_dispositions(self.dispositions, self.titles, self.receipt, self.old_dispositions)
        for field, value in (("candidateLabel", "normalized; label"), ("reviewFinding", True),
                             ("decision", "no-new-guard-retained"), ("endpointStatus", {})):
            changed = copy.deepcopy(self.dispositions)
            changed["dispositions"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_dispositions(changed, self.titles, self.receipt, self.old_dispositions)
        changed = copy.deepcopy(self.dispositions)
        changed["dispositions"][0]["evidence"]["selectors"]["1501020"] = ["unsupported"]
        with self.assertRaises(ValueError):
            check_dispositions(changed, self.titles, self.receipt, self.old_dispositions)

    def test_rejects_gate_snapshot_mode_and_manifest_substitution(self):
        summary = {"batch": "124", "reconciliation": 2, "status": "PASS", "mode": "committed",
                   "publishedBase": self.config["base"], "reconciliationParent": PARENT,
                   "startingHead": CANDIDATE, "checks": list(CHECKS),
                   "manifestSha256": "manifest", "runnerSha256": RUNNER_SHA}
        check_summary(summary, self.config, CANDIDATE, "committed", "manifest")
        for key, value in (("startingHead", PARENT), ("mode", "author"),
                           ("manifestSha256", "other"), ("reconciliation", 1)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_summary({**summary, key: value}, self.config, CANDIDATE, "committed", "manifest")


if __name__ == "__main__":
    unittest.main()
