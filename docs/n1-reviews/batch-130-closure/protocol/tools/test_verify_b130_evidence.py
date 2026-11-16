import copy
import json
import sys
import unittest

from verify_b130_evidence import (BASE, MEMBERS, ORDER, REPO, check_facts, new_pair_sets, verify_excerpt,
                                  verify_execution, verify_pair_member, verify_query_map, verify_reading_keys)

A, B, C = MEMBERS
FACTS = {
    "batch": 130, "candidate": "0" * 40,
    "sourceProof": {"path": "p", "sha256": "s"}, "payloadProof": {"path": "p", "sha256": "s"},
    "inventory": "evidence-inventory.json", "supersededInventories": [],
    "queryMaps": {"jmdict.xml": "query-membership.json"},
    "receipts": {"source-receipt.json": "survey_b130.py"}, "expectedJmdictFamilies": 1,
    "pairDispositions": "pair-dispositions.json", "scanDirectories": ["scans-002"], "scanRows": 1251,
    "externalBindings": {"external-capture-bindings.json": 6}, "fontEvidence": "stroke-font-evidence.json",
    "producers": ["survey_b130.py", "b130_common.py", "check_reading_b130.py", "run_b130_gates.py",
                  "preserve_b130.py"],
    "commonHelper": "b130_common.py", "readingCheck": "check_reading_b130.py",
    "requiredReadingKeys": {C: ["\u305f\u3088\u308a"]},
    "linkplanArgs": ["verify", BASE, *MEMBERS], "wordProseExceptions": [], "summaryBatch": "130",
    "gates": {"author": {"directory": "author-gates-001", "runner": "run_b130_gates.py",
                         "signedCopy": "author-evidence/author-gates-001"},
              "committed": {"directory": "committed-gates-001", "runner": "run_b130_gates.py",
                            "signedCopy": None}},
    "preservation": {"directory": "preservation-001", "producer": "preserve_b130.py"},
    "output": "evidence-verification-001",
}


def pair(other, decision, match):
    return {"pair": [A, other], "decision": decision, "comparisonTitle": other.lower(),
            "baselineCardSha256": "h" + other, "scanMatch": match,
            "targetLabelOnComparison": "forward", "comparisonLabelOnTarget": "reverse"}


class EvidenceTests(unittest.TestCase):
    def test_facts_reject_unsafe_names_undeclared_tools_and_unbound_remarks(self):
        check_facts(FACTS)
        for change in (lambda f: f.update(output="..\\x"),
                       lambda f: f.update(scanDirectories=["../scans"]),
                       lambda f: f["producers"].remove("run_b130_gates.py"),
                       lambda f: f["gates"]["committed"].update(directory="author-gates-001"),
                       lambda f: f.update(extra=True),
                       lambda f: f.update(requiredReadingKeys={"X": ["x"]})):
            changed = copy.deepcopy(FACTS)
            change(changed)
            with self.assertRaises(ValueError):
                check_facts(changed)
        remarks = str(REPO / "docs" / "n1-sources" / "batch-130" / "stale-remarks.json")
        declared = copy.deepcopy(FACTS)
        declared.update(linkplanArgs=["verify", BASE, "--remarks", remarks, *MEMBERS],
                        wordProseExceptions=["words/x.md"])
        check_facts(declared)
        for args, exceptions in ((declared["linkplanArgs"], []),
                                 (["verify", BASE, "--skip", remarks, *MEMBERS], ["words/x.md"]),
                                 (["verify", BASE, *MEMBERS[:-1]], [])):
            changed = copy.deepcopy(FACTS)
            changed.update(linkplanArgs=args, wordProseExceptions=exceptions)
            with self.assertRaises(ValueError):
                check_facts(changed)

    def test_query_map_requires_all_matching_predicates(self):
        raw = b"<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>XY</keb></k_ele>" \
              b"<r_ele><reb>reading</reb></r_ele></entry></JMdict>"
        selection = {"mode": "union", "queries": ["contains-keb:X", "exact-reb:reading", "exact-keb:missing"]}
        verify_query_map(raw, selection, {"1": ["contains:X", "exact-reading:reading"]})
        with self.assertRaises(ValueError):
            verify_query_map(raw, selection, {"1": ["contains:X"]})

    def test_new_pairs_require_complete_order_and_symmetric_guards(self):
        items = [{"newMemberPair": [A, B], "decision": "guard", "bothDirections": True},
                 {"newMemberPair": [A, C], "decision": "distinct", "bothDirections": True},
                 {"newMemberPair": [B, C], "decision": "curated", "bothDirections": True}]
        guards, curated = new_pair_sets(items)
        self.assertEqual((guards[A], guards[B], guards[C]), ({B}, {A}, set()))
        self.assertEqual((curated[B], curated[C]), ({C}, {B}))
        for change in (lambda x: x.pop(), lambda x: x.reverse(),
                       lambda x: x[0].update(bothDirections=False), lambda x: x[1].update(decision="same")):
            changed = copy.deepcopy(items)
            change(changed)
            with self.assertRaises(ValueError):
                new_pair_sets(changed)

    def test_pairs_cover_every_scan_and_include_new_member_guards(self):
        comparisons = {"X": ("x", "hX"), "Y": ("y", "hY")}
        item = {"kanji": A, "targetTitle": "t", "pairs": [pair("X", "guard", False), pair("Y", "distinct", True)]}
        card = {"title": "t", "quiz_exclusions": ["X", B], "distractors": []}
        scans = [{"matches": ["X"]}, {"matches": ["Y"]}]
        verify_pair_member(item, card, scans, comparisons, {B}, set())
        with self.assertRaises(ValueError):
            verify_pair_member(item, card, scans, comparisons, set(), set())
        with self.assertRaises(ValueError):
            verify_pair_member(item, card, [{"matches": ["X", "Z"]}, scans[1]], comparisons, {B}, set())
        stale = copy.deepcopy(item)
        stale["pairs"][1]["scanMatch"] = False
        with self.assertRaises(ValueError):
            verify_pair_member(stale, card, scans, comparisons, {B}, set())
        new_member = copy.deepcopy(item)
        new_member["pairs"].append(pair(B, "guard", False))
        with self.assertRaises(ValueError):
            verify_pair_member(new_member, card, scans, comparisons, {B}, set())

    def test_reading_keys_bind_one_literal_map_and_its_log(self):
        extras = {C: ["\u305f\u3088\u308a", "x"]}
        producer = f"import json\nextras = {extras!r}\nother = {{'k': 1}}\n".encode()
        log = ("keys: " + json.dumps(extras, ensure_ascii=False) + "\r\n").encode()
        self.assertEqual(verify_reading_keys(producer, log, {C: ["\u305f\u3088\u308a"]}), extras)
        with self.assertRaises(ValueError):
            verify_reading_keys(producer, log, {C: ["missing"]})
        with self.assertRaises(ValueError):
            verify_reading_keys(producer, b"no keys", {C: ["x"]})
        with self.assertRaises(ValueError):
            verify_reading_keys(producer + f"second = {{{A!r}: ['y']}}\n".encode(), log, {})

    def test_excerpt_ignores_whitespace_only(self):
        verify_excerpt("\u2461\u305f\u3088\u308a\u3002\n \u77e5\u3089\u305b".encode(),
                       "\u2461\u305f\u3088\u308a\u3002\u77e5\u3089\u305b")
        with self.assertRaises(ValueError):
            verify_excerpt("\u305f\u3088\u308a".encode(), "\u77e5\u3089\u305b")

    def test_gate_execution_rejects_overlap_and_command_drift(self):
        commands = {name: [name] for name in ORDER}
        receipts = {name: {
            "startedAt": f"2026-11-16T07:{index:02d}:00+00:00",
            "completedAt": f"2026-11-16T07:{index:02d}:10+00:00",
            "command": [sys.executable, "-B", name], "commonHelperSha256": "hash",
            "cleanupTimeoutSecondsPerStage": 10, "activeError": None, "cleanupError": None,
        } for index, name in enumerate(ORDER)}
        verify_execution(receipts, commands, "hash")
        overlap = copy.deepcopy(receipts)
        overlap[ORDER[1]]["startedAt"] = receipts[ORDER[0]]["startedAt"]
        with self.assertRaises(ValueError):
            verify_execution(overlap, commands, "hash")
        drift = copy.deepcopy(receipts)
        drift["lint"]["command"].append("--skip")
        with self.assertRaises(ValueError):
            verify_execution(drift, commands, "hash")


if __name__ == "__main__":
    unittest.main()
