import unittest

from prepare_b126_publication_tools_v2 import replace


class NumericSubstitutionTests(unittest.TestCase):
    def test_roundtrip_preserves_sha_identifiers(self):
        original = 'SHA256 equality_sha256 sha256 "delivered": 252 and == 246 and > 8706'
        changes = {"252": "256", "246": "250", "8706": "8714"}
        result = replace(original, changes)
        self.assertEqual(result, 'SHA256 equality_sha256 sha256 "delivered": 256 and == 250 and > 8714')
        self.assertEqual(replace(result, {v: k for k, v in changes.items()}), original)

    def test_longest_commit_binding_precedes_numeric_tokens(self):
        changes = {"old-252-hash": "new-256-hash", "252": "256"}
        original = "old-252-hash SHA256 252"
        result = replace(original, changes)
        self.assertEqual(result, "new-256-hash SHA256 256")
        self.assertEqual(replace(result, {v: k for k, v in changes.items()}), original)


if __name__ == "__main__":
    unittest.main()
