import copy
import json
import unittest

from common import WS
from verify_b127_reconciliation import (
    CARD, MEMBER, OTHERS, PREFIX, check_claims, check_metadata, metadata,
)

ROOT = WS / "b127-worktree"


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.old = metadata((ROOT / PREFIX / f"comparison-cards/{MEMBER}.md").read_bytes())
        self.new = metadata((ROOT / CARD).read_bytes())
        self.table = json.loads((ROOT / PREFIX / "pair-dispositions.json").read_bytes())
        self.receipt = json.loads((ROOT / PREFIX / "source-receipt.json").read_bytes())
        self.cards = {char: metadata((ROOT / f"kanji/{char}.md").read_bytes()) for char in OTHERS}

    def test_missing_direct_guard_or_changed_reading_is_rejected(self):
        check_metadata(self.old, self.new)
        for field, value in (("quiz_exclusions", self.new["quiz_exclusions"][:-1]),
                             ("quizKunyomi", ["\u304f\u3089"])):
            with self.subTest(field=field):
                altered = copy.deepcopy(self.new)
                altered[field] = value
                with self.assertRaises(ValueError):
                    check_metadata(self.old, altered)

    def test_false_symmetric_endpoint_is_rejected(self):
        check_claims(self.table, self.receipt, self.old, self.new, self.cards)
        self.table["claims"][5]["declaredEndpointStatus"]["effectiveSymmetricGuard"] = True
        with self.assertRaisesRegex(ValueError, "declaring endpoint"):
            check_claims(self.table, self.receipt, self.old, self.new, self.cards)

    def test_wrong_source_family_or_missing_direction_is_rejected(self):
        for mutate in (
            lambda row: row["recordBindings"]["completeWordFamilies"]["entryIds"].pop(),
            lambda row: row["directions"].pop(next(iter(row["directions"]))),
        ):
            table = copy.deepcopy(self.table)
            mutate(table["claims"][0])
            with self.assertRaises(ValueError):
                check_claims(table, self.receipt, self.old, self.new, self.cards)


if __name__ == "__main__":
    unittest.main(verbosity=2)
