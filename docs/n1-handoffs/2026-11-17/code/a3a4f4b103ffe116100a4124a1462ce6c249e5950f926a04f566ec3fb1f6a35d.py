import copy
import json
import unittest

from b130_revision_pairs import check_mapping, load_initials, verify
from common import frozen, sha
from verify_b130_revision_sources import OBSERVATION


class B130PairBindingTests(unittest.TestCase):
    def setUp(self):
        observation = json.loads(frozen(OBSERVATION / "observation.json"))
        self.files = {name: frozen(OBSERVATION / name, item["sha256"])
                      for name, item in observation["files"].items()}
        self.initials = load_initials()
        self.table_sha = sha(self.files["pair-dispositions-001.json"])
        table = json.loads(self.files["pair-dispositions-001.json"])
        self.rows = {"/".join(row["pair"]): row for row in table["rows"]}
        self.mapping = json.loads(self.files["responses/gpt-mapping-001.json"])

    def run_verify(self):
        return verify(self.files.__getitem__, lambda char: self.files[f"new-cards/{char}.md"])

    def test_all_24_real_questions_and_five_required_guards_are_bound(self):
        result = self.run_verify()
        self.assertEqual(len(result["responses"]["gpt"]["initialOpenClaimIds"]), 24)
        self.assertEqual(len(result["requiredDirectPairs"]), 5)
        self.assertEqual(result["counts"], {"guard": 8, "precaution": 16, "bounded-noncollision": 4})
        self.assertEqual(len(result["boundedNoncollisionPairs"]), 4)
        self.assertFalse(result["semanticAcceptance"])
        self.assertFalse(result["independenceAccepted"])

    def test_omitted_duplicate_retargeted_or_rewritten_question_is_rejected(self):
        for change in ("omit", "duplicate", "retarget", "rewrite", "accept"):
            with self.subTest(change=change):
                mapping = copy.deepcopy(self.mapping)
                rows = mapping["comparisonDispositions"]
                if change == "omit":
                    rows.pop()
                elif change == "duplicate":
                    rows[-1] = rows[0]
                elif change == "retarget":
                    rows[0]["neutralRow"] = rows[1]["neutralRow"]
                elif change == "rewrite":
                    rows[0]["initialQuestion"]["disposition"] = "harmless"
                else:
                    rows[0]["independentConfirmation"] = "confirmed"
                with self.assertRaises(ValueError):
                    check_mapping("gpt", mapping, self.initials["gpt"], self.rows, self.table_sha)

    def test_missing_direct_guard_or_complete_family_is_rejected(self):
        for change in ("guard", "family", "reverse"):
            with self.subTest(change=change):
                files = dict(self.files)
                if change == "guard":
                    name = "new-cards/\u8017.md"
                    original = files[name]
                    files[name] = original.replace(", \u6469".encode(), b"", 1)
                    self.assertNotEqual(files[name], original)
                else:
                    table = json.loads(files["pair-dispositions-001.json"])
                    if change == "family":
                        table["rows"][0]["completeFamilyCanonicalHashes"].popitem()
                    else:
                        table["rows"][0]["comparisonLabelOnTarget"] = ""
                    files["pair-dispositions-001.json"] = json.dumps(table).encode()
                with self.assertRaises(ValueError):
                    verify(files.__getitem__, lambda char: files[f"new-cards/{char}.md"])

    def test_foreign_family_response_cannot_enter_isolated_bundle(self):
        self.files["responses/claude-response-001.md"] += b"\nGPT finding F1 also required this."
        with self.assertRaisesRegex(ValueError, "other review-family"):
            self.run_verify()


if __name__ == "__main__":
    unittest.main()
