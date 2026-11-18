import copy
import json
import unittest

from common import sha
from record_b117_publication import validate_delivery


class DeliveryAcceptanceTests(unittest.TestCase):
    def test_rejects_unverified_or_wrong_revision_delivery(self):
        manifest = json.dumps({"contentVersion": "v1", "kanji": {"kanji/test.md": "hash"}}).encode()
        ci = {"status": "completed", "conclusion": "success", "headSha": "commit"}
        archive = {
            "commit": "commit", "pendingChecks": [], "memory": {"breach": None},
            "manifestEqual": True, "manifestBytesEqualGitBlob": True, "zipNamesEqualExportedTree": True,
            "allPublishingBudgetsPassed": True, "contributorEvidenceExcluded": True,
            "perFileLimitsAndSafePathsPassed": True, "manifestSha256": sha(manifest),
            "contentVersion": "v1", "verifiedRuntimeHashes": 1,
        }
        validate_delivery("commit", manifest, ci, archive)
        for field, value in (("commit", "old"), ("pendingChecks", ["hashes"]),
                             ("manifestSha256", "old"), ("verifiedRuntimeHashes", 0),
                             ("allPublishingBudgetsPassed", False), ("memory", {"breach": True})):
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_delivery("commit", manifest, ci, {**copy.deepcopy(archive), field: value})
        for field, value in (("headSha", "old"), ("status", "in_progress"), ("conclusion", "failure")):
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_delivery("commit", manifest, {**ci, field: value}, archive)


if __name__ == "__main__":
    unittest.main()
