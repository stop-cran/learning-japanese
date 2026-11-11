import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("byte_forms", HERE / "batch-108-verify-byte-forms.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
REPO = None


class ByteFormTests(unittest.TestCase):
    def test_exact_lf_and_crlf(self):
        lf = "title: \u4e00\nbody\n".encode("utf-8")
        crlf = lf.replace(b"\n", b"\r\n")
        for committed in (lf, crlf):
            proof, forms = verifier.byte_forms(committed, verifier.sha(crlf))
            self.assertEqual(verifier.classify_observed(lf, forms)[-1], "LF-reconstruction")
            self.assertIn("CRLF-reconstruction", verifier.classify_observed(crlf, forms))
            self.assertFalse(proof["newCapture"])

    def test_recorded_raw_is_not_rewritten(self):
        lf = b"a\nb\n"
        proof, _ = verifier.byte_forms(lf, verifier.sha(lf))
        self.assertEqual(proof["captureRelation"], "committed-raw")
        self.assertEqual(proof["recordedCapturedRawSha256"], verifier.sha(lf))

    def test_pinned_mixed_committed_bytes_preserved(self):
        raw = b"a\r\nb\n"
        proof, forms = verifier.byte_forms(raw, verifier.sha(raw))
        self.assertEqual(proof["captureRelation"], "committed-raw")
        self.assertIn("committed-raw", verifier.classify_observed(raw, forms))
        with self.assertRaises(verifier.VerificationError):
            verifier.classify_observed(b"a\nb\r\n", forms)

    def test_unexplained_capture_digest(self):
        with self.assertRaises(verifier.VerificationError):
            verifier.byte_forms(b"a\n", verifier.sha(b"different\r\n"))

    def test_observed_changes_are_not_normalized_away(self):
        _, forms = verifier.byte_forms(b"a\nb\n", verifier.sha(b"a\r\nb\r\n"))
        for changed in (
            b"a\r\nb\n", b"a\nb", b"a \nb\n", b"\xef\xbb\xbfa\nb\n",
            b"a\rb\r", b"a\nb\n\n", b"a\nB\n", b"\xff",
        ):
            with self.subTest(changed=changed):
                with self.assertRaises(verifier.VerificationError):
                    verifier.classify_observed(changed, forms)

    def test_unicode_is_not_normalized(self):
        raw = "caf\u00e9\n".encode("utf-8")
        _, forms = verifier.byte_forms(raw, verifier.sha(raw))
        with self.assertRaises(verifier.VerificationError):
            verifier.classify_observed("cafe\u0301\n".encode("utf-8"), forms)

    def test_lone_cr_and_invalid_utf8_fail(self):
        for raw in (b"a\rb\n", b"\xff\n"):
            with self.subTest(raw=raw):
                with self.assertRaises((verifier.VerificationError, UnicodeError)):
                    verifier.byte_forms(raw, verifier.sha(raw))

    def test_explicit_raw_only_accepts_no_reconstruction(self):
        raw = b"a\rb\r\n"
        oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        pin = {"gitBlobOid": oid, "rawSha256": verifier.sha(raw)}
        proof, forms = verifier.raw_only_forms(raw, verifier.sha(raw), oid, pin)
        self.assertTrue(proof["rawOnly"])
        self.assertEqual(verifier.classify_observed(raw, forms), ["committed-raw"])
        for changed in (raw.replace(b"\r\n", b"\n"), raw.replace(b"\r", b""), raw + b"x"):
            with self.subTest(changed=changed):
                with self.assertRaises(verifier.VerificationError):
                    verifier.classify_observed(changed, forms)
        for data, captured, identity in (
            (raw + b"x", verifier.sha(raw), oid),
            (raw, "0" * 64, oid), (raw, verifier.sha(raw), "0" * 40),
        ):
            with self.subTest(identity=identity, captured=captured):
                with self.assertRaises(verifier.VerificationError):
                    verifier.raw_only_forms(data, captured, identity, pin)

    def test_paths_and_duplicate_json_fail(self):
        for path in ("../x", "/x", "C:\\x", "a//b", "a\nb", "a/../b", "a\0b"):
            with self.subTest(path=path):
                with self.assertRaises(verifier.VerificationError):
                    verifier.logical_path(path)
        with self.assertRaises(verifier.VerificationError):
            verifier.json_without_duplicate_keys(b'{"x":1,"x":2}')

    def test_git_framing_identity_and_truncation(self):
        body = b"a\n"
        oid = hashlib.sha1(b"blob 2\0" + body).hexdigest().encode("ascii")
        frame = oid + b" blob 2\n" + body + b"\n"
        self.assertEqual(verifier.parse_batch(frame, ["kanji/x.md"])["kanji/x.md"][1], body)
        for changed in (
            frame[:-1], frame + b"x", frame.replace(b"blob", b"tree"),
            frame.replace(oid, b"0" * 40), frame.replace(b"a\n", b"b\n"),
            b"missing\n", oid + b" blob 99999999\n",
        ):
            with self.subTest(frame=changed):
                with self.assertRaises(verifier.VerificationError):
                    verifier.parse_batch(changed, ["kanji/x.md"])

    def test_git_exit_stderr_and_timeout_fail(self):
        for result in (
            subprocess.CompletedProcess([], 1, b"", b"failure"),
            subprocess.CompletedProcess([], 0, b"", b"unexpected stderr"),
        ):
            with mock.patch.object(verifier.subprocess, "run", return_value=result):
                with self.assertRaises(verifier.VerificationError):
                    verifier.read_blobs(REPO, verifier.BASELINE_COMMIT, ["kanji/x.md"])
        with mock.patch.object(verifier.subprocess, "run",
                               side_effect=subprocess.TimeoutExpired("git", 120)):
            with self.assertRaises(subprocess.TimeoutExpired):
                verifier.read_blobs(REPO, verifier.BASELINE_COMMIT, ["kanji/x.md"])

    def test_complete_tree_equality_not_count_or_subset(self):
        complete = {"kanji/x.md": "a" * 40, "words/y.md": "b" * 40}
        verifier.assert_complete_inventory(complete, complete)
        for inventory, tree in (
            ({"kanji/x.md": {}}, complete),
            ({**complete, "kanji/z.md": {}}, complete),
            ({"kanji/x.md": {}, "words/z.md": {}}, complete),
        ):
            with self.subTest(inventory=inventory):
                with self.assertRaises(verifier.VerificationError):
                    verifier.assert_complete_inventory(inventory, tree)

    def test_tree_framing_type_and_duplicates_fail(self):
        entry = b"100644 blob " + b"a" * 40 + b"\tkanji/x.md\0"
        with mock.patch.object(verifier, "run_git", return_value=entry):
            self.assertEqual(verifier.read_baseline_tree(REPO), {"kanji/x.md": "a" * 40})
        for changed in (
            entry[:-1], entry + entry, entry.replace(b"100644 blob", b"120000 blob"),
            entry.replace(b"kanji/x.md", b"outside/x.md"), b"",
        ):
            with self.subTest(entry=changed):
                with mock.patch.object(verifier, "run_git", return_value=changed):
                    with self.assertRaises(verifier.VerificationError):
                        verifier.read_baseline_tree(REPO)

    def test_scope_and_pin_tampering_fail(self):
        original = verifier.json_without_duplicate_keys(
            (HERE / "batch-108-byte-form-erratum.json").read_bytes()
        )
        for field, value in (
            ("schema", "unknown"), ("evidenceCommit", "0" * 40),
            ("baselineCommit", "0" * 40), ("expectedCounts", {}),
            ("committedEvidenceFiles", {}),
            ("rawOnlyBaselineExceptions", {}),
        ):
            changed = copy.deepcopy(original)
            changed[field] = value
            with self.subTest(field=field):
                with self.assertRaises(verifier.VerificationError):
                    verifier.verify(REPO, changed)
        changed = copy.deepcopy(original)
        path = verifier.PREFIX + "batch-108-public-source-receipts.json"
        changed["committedEvidenceFiles"][path] = "0" * 64
        with self.assertRaises(verifier.VerificationError):
            verifier.verify(REPO, changed)

    def test_all_pinned_historical_rows(self):
        erratum = verifier.json_without_duplicate_keys(
            (HERE / "batch-108-byte-form-erratum.json").read_bytes()
        )
        result = verifier.verify(REPO, erratum)
        self.assertEqual(result["baselineRowsVerified"], 6210)
        self.assertTrue(result["baselineInventoryExactlyEqualsCompleteGitTree"])
        self.assertEqual(result["baselineTreeEntryCount"], 6210)
        self.assertEqual(result["baselineCounts"], {
            "committed-raw": 699, "explicit-LF-to-CRLF-reconstruction": 5511,
        })
        self.assertEqual(result["savedSnapshotNormalizedBaselineContentVerified"], 43)
        self.assertEqual(result["baselineRawOnlyExceptionsVerified"], 2)
        self.assertEqual(result["publicSourcesVerified"], 2)
        self.assertFalse(result["historicalAuditReplay"])
        self.assertFalse(result["nativeOrPublicationCredit"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    REPO = args.repo
    outcome = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ByteFormTests)
    )
    sys.exit(0 if outcome.wasSuccessful() else 1)
