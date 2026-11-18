import copy
import unittest

from verify_b134_packet import BASE, PAIR_PRODUCER_SHA, pair_coverage, tree

TARGET = "\u7d2b"


def fixture():
    comparisons = {"\u53e4": ("old", "a"), "\u5305": ("wrap", "b"), "\u672c": ("book", "c")}
    readbacks = {"\u53e4": "ra", "\u5305": "rb", "\u672c": "rc"}
    decisions = {"\u53e4": "curated", "\u5305": "guard", "\u672c": "distinct"}
    rows = [{
        "pair": [TARGET, other], "comparisonTitle": title, "decision": decisions[other],
        "comparisonLabelOnTarget": "x", "targetLabelOnComparison": "y",
        "baselineCardSha256": digest, "readbackSha256": readbacks[other], "scanMatch": other != "\u672c",
    } for other, (title, digest) in comparisons.items()]
    disposition = {"base": BASE, "producerSha256": PAIR_PRODUCER_SHA, "newMemberPairs": [],
                   "members": [{"kanji": TARGET, "targetTitle": "purple", "scanRows": 1261, "pairs": rows}]}
    cards = {TARGET: {"title": "purple", "quiz_exclusions": ["\u5305"], "distractors": ["\u53e4"]}}
    scans = {TARGET: {"rows": [{}] * 1261, "matches": ["\u53e4", "\u5305"]}}
    return disposition, cards, scans, comparisons, readbacks


class PairCoverageTests(unittest.TestCase):
    def test_accepts_complete_coverage(self):
        self.assertEqual(pair_coverage(*fixture()), (3, {"curated": 1, "distinct": 1, "guard": 1}))

    def assert_rejected(self, mutate):
        args = copy.deepcopy(fixture())
        mutate(*args)
        with self.assertRaises(ValueError):
            pair_coverage(*args)

    def test_rejects_guard_mismatch(self):
        self.assert_rejected(lambda d, c, s, cmp, r: c[TARGET]["quiz_exclusions"].append("\u672c"))

    def test_rejects_wrong_scan_flag(self):
        self.assert_rejected(lambda d, c, s, cmp, r: d["members"][0]["pairs"][2].update(scanMatch=True))

    def test_rejects_unlisted_scan_match(self):
        self.assert_rejected(lambda d, c, s, cmp, r: s[TARGET]["matches"].append("\u5ddd"))

    def test_rejects_readback_mismatch(self):
        self.assert_rejected(lambda d, c, s, cmp, r: r.update({"\u5305": "other"}))

    def test_rejects_extra_row_field(self):
        self.assert_rejected(lambda d, c, s, cmp, r: d["members"][0]["pairs"][0].update(note="z"))

    def test_rejects_unused_comparison(self):
        self.assert_rejected(lambda d, c, s, cmp, r: cmp.update({"\u5ddd": ("river", "d")}))

    def test_rejects_new_pairs(self):
        self.assert_rejected(lambda d, c, s, cmp, r: d["newMemberPairs"].append({}))

    def test_rejects_wrong_scan_row_count(self):
        self.assert_rejected(lambda d, c, s, cmp, r: d["members"][0].update(scanRows=1258))


class TreeTests(unittest.TestCase):
    def test_strips_text_and_preserves_attributes(self):
        import xml.etree.ElementTree as ET
        node = ET.fromstring('<a x="1">\n <b>t</b></a>')
        self.assertEqual(tree(node), ["a", {"x": "1"}, "", [["b", {}, "t", []]]])


if __name__ == "__main__":
    unittest.main()
