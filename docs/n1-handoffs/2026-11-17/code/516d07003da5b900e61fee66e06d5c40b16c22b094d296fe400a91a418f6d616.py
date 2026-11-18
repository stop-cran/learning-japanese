import copy
import io
import json
import unittest

from common import frozen
from verify_b130_revision_sources import OBSERVATION, recover_selectors, selections, verify_stream
from test_verify_b129_revision_sources import CompleteCorrectionSources, Guard


class B130SourceContractTests(unittest.TestCase):
    def setUp(self):
        self.receipt = json.loads(frozen(OBSERVATION / "source-receipt.json"))
        self.membership = json.loads(frozen(OBSERVATION / "query-membership.json"))
        self.xml = {name: frozen(OBSERVATION / name) for name in self.receipt["outputs"]}
        self.producer = frozen(OBSERVATION / "reconcile_sources_b130.py")

    def selected(self):
        return selections(self.receipt, self.membership, self.xml, self.producer)

    def test_actual_producer_union_and_inverse_membership_are_complete(self):
        selected = self.selected()
        self.assertEqual(len(selected["jmdict"]["expected"]), 99)
        self.assertEqual(len(selected["kanjidic2"]["expected"]), 31)
        self.assertIn("exact-spelling:\u97f3\u8017", selected["jmdict"]["membership"]["zeroMatches"])
        for kind, name, tag, key in (
            ("jmdict", "jmdict-families.xml", "entry", "ent_seq"),
            ("kanjidic2", "kanjidic2-records.xml", "character", "literal"),
        ):
            result = verify_stream(io.BytesIO(self.xml[name]), tag, key, [selected[kind]], Guard())[0]
            self.assertEqual(set(result["identities"]), set(selected[kind]["expected"]))

    def test_removed_zero_query_or_changed_producer_is_not_silently_admitted(self):
        self.receipt["selectors"]["exactSpellings"].remove("\u97f3\u8017")
        with self.assertRaisesRegex(ValueError, "executed selection"):
            self.selected()
        with self.assertRaisesRegex(ValueError, "changed exact-spelling producer"):
            recover_selectors(self.producer.replace(b"set(COMPARISONS) |", b"set(COMPARISONS) -"))

    def test_false_count_duplicate_or_extra_membership_is_rejected(self):
        for change in ("count", "duplicate", "extra"):
            with self.subTest(change=change):
                receipt, membership = copy.deepcopy(self.receipt), copy.deepcopy(self.membership)
                if change == "count":
                    receipt["selectors"]["queryCountsIncludingZero"]["exact-spelling:\u97f3\u8017"] = 1
                elif change == "duplicate":
                    identity = next(iter(membership))
                    membership[identity].append(membership[identity][0])
                else:
                    membership["not-an-entry"] = ["unsupported-query:value"]
                with self.assertRaises(ValueError):
                    selections(receipt, membership, self.xml, self.producer)

    def test_receipt_bound_secondary_sense_cannot_be_removed(self):
        original = self.xml["jmdict-families.xml"]
        self.xml["jmdict-families.xml"] = original.replace(
            b">news</gloss>", b">redacted</gloss>", 1)
        self.assertNotEqual(self.xml["jmdict-families.xml"], original)
        with self.assertRaisesRegex(ValueError, "XML differs"):
            self.selected()


if __name__ == "__main__":
    unittest.main()
