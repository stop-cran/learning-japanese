import copy
import hashlib
import unittest

from b129_correction_evidence import FILES, verify_formatting
from common import sha


class FormattingCorrectionTests(unittest.TestCase):
    def fixture(self):
        blobs = {name: b"first\r\nsecond\r\n" for name in FILES}
        revision, historical = {"files": {}}, {"formatting": {}}
        for name, raw in blobs.items():
            before, after = sha(raw), sha(raw.replace(b"\r\n", b"\n"))
            revision["files"][name] = {
                "committedBlobSha256": before, "historicalTemporaryLfSha256": after,
                "committedBlobIdAtOriginalCandidate": hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest(),
                "equalsHistoricalRawBefore": True, "temporaryLfNormalizationWasReverted": True}
            historical["formatting"][name] = {"rawBeforeSha256": before, "rawAfterSha256": after}
        return revision, historical, blobs

    def test_accurate_restoration_is_accepted(self):
        revision, historical, blobs = self.fixture()
        verify_formatting(revision, historical, blobs, blobs)

    def test_normalized_blob_cannot_be_claimed_as_original(self):
        revision, historical, blobs = self.fixture()
        changed = copy.deepcopy(blobs)
        name = sorted(FILES)[0]
        changed[name] = changed[name].replace(b"\r\n", b"\n")
        with self.assertRaisesRegex(ValueError, "does not match"):
            verify_formatting(revision, historical, changed, blobs)

    def test_inaccurate_historical_after_hash_is_rejected(self):
        revision, historical, blobs = self.fixture()
        historical["formatting"][sorted(FILES)[0]]["rawAfterSha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "does not match"):
            verify_formatting(revision, historical, blobs, blobs)


if __name__ == "__main__":
    unittest.main()
