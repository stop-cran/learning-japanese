"""Reject changes that would silently weaken B131's selected source coverage."""
import copy
import json
import unittest

from verify_b131_revision_sources_001 import (
    COMPARISONS, PREFIX, REPO, exact_words, source_selections)
from verify_b129_revision_sources import verify_stream


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        packet = REPO / PREFIX
        cls.receipt = json.loads((packet / "source-receipt.json").read_bytes())
        cls.membership = json.loads((packet / "query-membership.json").read_bytes())
        cls.xml = {name: (packet / name).read_bytes() for name in
                   ("jmdict-families.xml", "kanjidic2-records.xml")}
        cls.producer = (REPO.parent / "scratch-131" / "r131_sources.py").read_bytes()
        cls.cards = {char: (packet / f"comparison-cards/{char}.md").read_bytes()
                     for char in COMPARISONS}

    def selected(self, receipt=None, membership=None, xml=None):
        return source_selections(receipt if receipt is not None else self.receipt,
                                 membership if membership is not None else self.membership,
                                 xml if xml is not None else self.xml,
                                 self.producer, self.cards)

    def test_exact_selector_recovery(self):
        selected = self.selected()
        self.assertEqual(len(selected["jmdict"]["expected"]), 78)
        self.assertEqual(len(selected["kanjidic2"]["expected"]), 19)
        for producer in (b"WORDS = get_words()", b"WORDS = 'one one'.split()"):
            with self.assertRaises((ValueError, RuntimeError)):
                exact_words(producer)

    def test_missing_query_and_record_rejected(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["predicates"]["exactSpellings"].pop()
        with self.assertRaises((ValueError, RuntimeError)):
            self.selected(receipt=receipt)
        membership = copy.deepcopy(self.membership)
        membership.pop(next(iter(membership)))
        with self.assertRaises((ValueError, RuntimeError)):
            self.selected(membership=membership)

    def test_changed_sense_and_absence_rejected(self):
        xml = dict(self.xml)
        xml["jmdict-families.xml"] = xml["jmdict-families.xml"].replace(b"<gloss>", b"<gloss>changed ", 1)
        with self.assertRaises((ValueError, RuntimeError)):
            self.selected(xml=xml)
        receipt = copy.deepcopy(self.receipt)
        zero = next(q for q, count in receipt["queryCountsIncludingAbsences"].items() if not count)
        del receipt["queryCountsIncludingAbsences"][zero]
        with self.assertRaises((ValueError, RuntimeError)):
            self.selected(receipt=receipt)


if __name__ == "__main__":
    unittest.main()
