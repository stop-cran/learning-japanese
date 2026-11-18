import json
import unittest
from pathlib import Path
from unittest.mock import patch

import close_b134_v2 as closure
from common import frozen


class BoundProducerInputs(unittest.TestCase):
    def test_exact_pinned_external_inputs_are_readable(self):
        for path, digest in closure.EXTERNAL.items():
            with self.subTest(path=path):
                self.assertEqual(closure.read_review(path, digest), frozen(path, digest))

    def test_wrong_or_missing_digest_is_rejected(self):
        path = next(iter(closure.EXTERNAL))
        for digest in (None, "0" * 64):
            with self.subTest(digest=digest), self.assertRaisesRegex(ValueError, "exactly bound"):
                closure.read_review(path, digest)

    def test_unlisted_external_file_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "exactly bound"):
            closure.read_review(closure.SOURCE, closure.SOURCE_SHA)

    def test_review_data_retains_original_scope_and_hash_checks(self):
        path = closure.CONFIG_ROOT / "audit-claude-fresh-003.json"
        digest = closure.CONFIGS["claude"]
        self.assertEqual(closure.read_review(path, digest), closure.original_reader(path, digest))
        with self.assertRaisesRegex(ValueError, "Changed input"):
            closure.read_review(path, "0" * 64)

    def test_external_path_traversal_does_not_create_permission(self):
        path = closure.ROOT / ".." / ".." / "review-tools" / "close_b134.py"
        self.assertEqual(path.resolve(), closure.SOURCE.resolve())
        with self.assertRaisesRegex(ValueError, "exactly bound"):
            closure.read_review(path, closure.SOURCE_SHA)

    def test_entry_rejects_missing_or_mismatched_archived_adapter(self):
        for evidence in ([], [{"archivePath": "protocol/close_b134_v2.py",
                              "path": "retained.py", "sha256": "0" * 64}]):
            with self.subTest(evidence=evidence), \
                    patch.object(closure, "frozen", return_value=b"adapter"), \
                    patch.object(closure, "read_review", return_value=json.dumps(
                        {"evidence": evidence}).encode()), \
                    patch.object(closure.original, "main") as main:
                with self.assertRaisesRegex(ValueError, "retain this scope-repair"):
                    closure.main("dry", Path("request.json"), Path("output"))
                main.assert_not_called()

    def test_entry_routes_only_reader_and_restores_it_after_failure(self):
        raw = b"adapter"
        request = json.dumps({"evidence": [{
            "archivePath": "protocol/close_b134_v2.py",
            "path": "retained.py", "sha256": closure.sha(raw),
        }]}).encode()

        def stop(mode, request_path, output):
            self.assertIs(closure.original.read_review, reader)
            self.assertEqual((mode, request_path, output),
                             ("dry", Path("request.json"), Path("output")))
            raise RuntimeError("controlled assembly failure")

        with patch.object(closure, "frozen", return_value=raw), \
                patch.object(closure, "read_review", side_effect=[request, raw]) as reader, \
                patch.object(closure.original, "main", side_effect=stop):
            with self.assertRaisesRegex(RuntimeError, "controlled assembly failure"):
                closure.main("dry", Path("request.json"), Path("output"))
        self.assertIs(closure.original.read_review, closure.original_reader)


if __name__ == "__main__":
    unittest.main(verbosity=2)
