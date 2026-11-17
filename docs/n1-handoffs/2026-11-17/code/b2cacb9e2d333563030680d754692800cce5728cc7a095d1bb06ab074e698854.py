import copy
import json
import unittest

from prepare_b133_source_facts import (
    BASE, BASELINE_CARDS, MEMBERS, SUPPORTS, initial_scope, union_selection,
    verify_query_counts, verify_query_membership,
)


class B133SourcePredicateTests(unittest.TestCase):
    def fixture(self):
        comparisons = ["A", "B", "C", "D"]
        rows = [{"kanji": name} for name in
                comparisons + [f"entry{i}" for i in range(BASELINE_CARDS - len(comparisons))]]
        documents = {}
        curated = {char: ["A", "B", "C"] for char in MEMBERS}
        readings = {char: [f"reading{i}"] for i, char in enumerate(MEMBERS)}
        for char in MEMBERS:
            documents[f"scans/{char}.json"] = json.dumps({
                "base": BASE, "kanji": char, "rows": copy.deepcopy(rows), "matches": ["D"],
            }).encode()
        for char in comparisons:
            documents[f"comparison-cards/{char}.md"] = b"[linked](../words/linked-word.md)\n"
        exact = set(comparisons) | set(MEMBERS) | {"linked-word"}
        exact.update(word for words in SUPPORTS.values() for word in words)
        initial = {
            "containsKeys": MEMBERS + ["\u7027"],
            "allExactSpellings": sorted(exact),
            "allExactReadings": sorted(value for values in readings.values() for value in values),
        }
        return documents, initial, curated, readings

    def test_comparison_word_links_and_all_member_readings_are_required(self):
        documents, initial, curated, readings = self.fixture()
        comparisons, exact, keys = initial_scope(documents.__getitem__, initial, curated, readings)
        self.assertEqual(comparisons, {"A", "B", "C", "D"})
        self.assertIn("linked-word", exact)
        self.assertEqual(keys, {"reading0", "reading1", "reading2"})
        for field, missing in (("containsKeys", "\u7027"), ("allExactSpellings", "linked-word"),
                               ("allExactReadings", "reading2")):
            altered = copy.deepcopy(initial)
            altered[field].remove(missing)
            with self.subTest(field=field), self.assertRaises(ValueError):
                initial_scope(documents.__getitem__, altered, curated, readings)

    def test_every_member_needs_the_same_complete_baseline(self):
        documents, initial, curated, readings = self.fixture()
        path = f"scans/{MEMBERS[-1]}.json"
        for change in ("drop-row", "duplicate-row", "different-baseline", "wrong-base", "wrong-member"):
            altered = dict(documents)
            scan = json.loads(altered[path])
            if change == "drop-row":
                scan["rows"].pop()
            elif change == "duplicate-row":
                scan["rows"][-1] = scan["rows"][-2]
            elif change == "different-baseline":
                scan["rows"][-1] = {"kanji": "different"}
            elif change == "wrong-base":
                scan["base"] = "wrong"
            else:
                scan["kanji"] = MEMBERS[0]
            altered[path] = json.dumps(scan).encode()
            with self.subTest(change=change), self.assertRaises(ValueError):
                initial_scope(altered.__getitem__, initial, curated, readings)

    def test_supplemental_union_preserves_overlapping_and_absent_predicates(self):
        raw = b"<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>AB</keb></k_ele></entry></JMdict>"
        selection = union_selection("supplement.xml", contains=["A", "missing"], spellings=["AB"])
        membership = {"1": ["contains:A", "exact-spelling:AB"]}
        verify_query_membership(raw, membership, selection)
        queries = ["contains:A", "contains:missing", "exact-spelling:AB"]
        counts = {"contains:A": 1, "contains:missing": 0, "exact-spelling:AB": 1}
        verify_query_counts(membership, queries, counts)
        with self.assertRaises(ValueError):
            verify_query_membership(raw, {"1": ["exact-spelling:AB"]}, selection)
        for altered in (
            {"contains:A": 1, "exact-spelling:AB": 1},
            {**counts, "contains:missing": 1},
            {**counts, "contains:A": True},
        ):
            with self.subTest(counts=altered), self.assertRaises(ValueError):
                verify_query_counts(membership, queries, altered)


if __name__ == "__main__":
    unittest.main()
