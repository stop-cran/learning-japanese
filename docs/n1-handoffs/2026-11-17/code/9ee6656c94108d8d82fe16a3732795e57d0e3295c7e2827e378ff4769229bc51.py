import copy
import json
import unittest

from prepare_b134_source_facts import (
    BASE, BASELINE_CARDS, MEMBERS, SUPPORTS, VARIANT, curated_assignment, initial_scope,
)


class B134SourcePredicateTests(unittest.TestCase):
    def fixture(self):
        comparisons = ["A", "B", "C", "D"]
        rows = [{"kanji": name} for name in
                comparisons + [f"entry{i}" for i in range(BASELINE_CARDS - len(comparisons))]]
        documents = {}
        curated = {char: ["A", "B", "C"] for char in MEMBERS}
        readings = {char: [f"reading{i}", "shared"] for i, char in enumerate(MEMBERS)}
        additional = {"extra-word", "absent-word"}
        for char in MEMBERS:
            documents[f"scans/{char}.json"] = json.dumps({
                "base": BASE, "kanji": char, "rows": copy.deepcopy(rows), "matches": ["D"],
            }).encode()
        for char in comparisons:
            documents[f"comparison-cards/{char}.md"] = b"[linked](../words/linked-word.md)\r\n"
        exact = set(comparisons) | set(MEMBERS) | additional | {"linked-word"}
        exact.update(word for words in SUPPORTS.values() for word in words)
        initial = {
            "containsKeys": MEMBERS + [VARIANT],
            "allExactSpellings": sorted(exact),
            "allExactReadings": sorted({value for values in readings.values() for value in values}),
        }
        return documents, initial, curated, readings, additional

    def test_variant_additional_linked_and_reading_queries_are_required(self):
        documents, initial, curated, readings, additional = self.fixture()
        comparisons, exact, keys = initial_scope(documents.__getitem__, initial, curated, readings, additional)
        self.assertEqual(comparisons, {"A", "B", "C", "D"})
        self.assertTrue({"linked-word", "extra-word", "absent-word"} <= exact)
        self.assertEqual(keys, {"reading0", "shared"})
        for field, missing in (("containsKeys", VARIANT), ("allExactSpellings", "absent-word"),
                               ("allExactSpellings", "linked-word"), ("allExactReadings", "shared")):
            altered = copy.deepcopy(initial)
            altered[field].remove(missing)
            with self.subTest(field=field, missing=missing), self.assertRaises(ValueError):
                initial_scope(documents.__getitem__, altered, curated, readings, additional)
        for bad in ({"extra-word", ""}, ["extra-word", "absent-word"]):
            with self.subTest(additional=bad), self.assertRaises(ValueError):
                initial_scope(documents.__getitem__, initial, curated, readings, bad)

    def test_curated_reader_accepts_only_literal_or_string_list_values(self):
        raw = 'CURATED = {"x": list("abc"), "y": ["d", "e"]}\n'.encode()
        self.assertEqual(curated_assignment(raw), {"x": ["a", "b", "c"], "y": ["d", "e"]})
        for bad in ('CURATED = {"x": list(NAME)}\n', 'CURATED = {"x": sorted("abc")}\n',
                    'CURATED = {"x": list("a", "b")}\n', 'CURATED = {"x": "abc"}\n',
                    'CURATED = dict(x=["a"])\n', 'CURATED = {"x": ["a"]}\nCURATED = {}\n'):
            with self.subTest(source=bad), self.assertRaises(ValueError):
                curated_assignment(bad.encode())

    def test_scan_must_be_complete_unique_and_on_the_signed_base(self):
        documents, initial, curated, readings, additional = self.fixture()
        path = f"scans/{MEMBERS[0]}.json"
        for change in ("drop-row", "duplicate-row", "wrong-base", "wrong-member", "nonbaseline-match"):
            altered = dict(documents)
            scan = json.loads(altered[path])
            if change == "drop-row":
                scan["rows"].pop()
            elif change == "duplicate-row":
                scan["rows"][-1] = scan["rows"][-2]
            elif change == "wrong-base":
                scan["base"] = "wrong"
            elif change == "wrong-member":
                scan["kanji"] = "other"
            else:
                scan["matches"] = ["not-a-baseline-card"]
            altered[path] = json.dumps(scan).encode()
            with self.subTest(change=change), self.assertRaises(ValueError):
                initial_scope(altered.__getitem__, initial, curated, readings, additional)


if __name__ == "__main__":
    unittest.main()
