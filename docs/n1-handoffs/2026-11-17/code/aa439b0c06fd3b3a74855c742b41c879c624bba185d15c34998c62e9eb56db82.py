import tempfile
import unittest
from pathlib import Path

from common import freeze_json, sha, write_frozen
from source_contract import load, read


class SourceContractTests(unittest.TestCase):
    def check_contract(self, transform=None, signed=b"signed original"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binding = write_frozen(root / "source.xml", b"<complete-record/>")
            contract = {
                "batch": 118, "candidate": "a" * 40, "base": "b" * 40,
                "signedSources": {"docs/source.xml": sha(b"signed original")},
                "files": {"normalized.xml": binding},
            }
            if transform:
                transform(contract)
            config = {"batch": 118, "candidate": "a" * 40, "base": "b" * 40,
                      "sourceContract": freeze_json(root / "contract.json", contract)}
            loaded = load(config, lambda path: signed)
            self.assertEqual(read(loaded, "normalized.xml"), b"<complete-record/>")

    def test_binds_normalized_and_original_bytes(self):
        self.check_contract()

    def test_rejects_another_candidate(self):
        with self.assertRaisesRegex(ValueError, "another snapshot"):
            self.check_contract(lambda c: c.update(candidate="c" * 40))

    def test_rejects_changed_signed_source(self):
        with self.assertRaisesRegex(ValueError, "Signed source changed"):
            self.check_contract(signed=b"changed original")

    def test_rejects_changed_normalized_source(self):
        with self.assertRaisesRegex(ValueError, "Changed input"):
            self.check_contract(lambda c: c["files"]["normalized.xml"].update(sha256="0" * 64))


if __name__ == "__main__":
    unittest.main()
