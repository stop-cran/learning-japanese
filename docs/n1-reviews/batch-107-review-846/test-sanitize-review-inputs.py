import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "batch107_redaction", Path(__file__).with_name("sanitize-review-inputs.py"))
redaction = importlib.util.module_from_spec(spec)
spec.loader.exec_module(redaction)


class ReviewInputRedactionTest(unittest.TestCase):
    def setUp(self):
        self.content = r"C:\workspace\content"
        self.git = r"C:\workspace\metadata"
        self.roots = [("CONTENT_ROOT", self.content), ("GIT_METADATA_ROOT", self.git)]

    def test_raw_and_json_escaped_paths_are_reversibly_redacted(self):
        text = f'{self.content}\\file.md\n"{self.git.replace(chr(92), chr(92) * 2)}\\\\HEAD"\nhttps://example.com/\n'
        output, counts = redaction.sanitize(text.encode("utf-8"), self.roots)
        self.assertNotIn(self.content, output.decode("utf-8"))
        self.assertIn(b"https://example.com/", output)
        self.assertEqual(1, counts["__CONTENT_ROOT__"])
        self.assertEqual(1, counts["__GIT_METADATA_ROOT_ESCAPED__"])

    def test_unrecognized_absolute_path_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "absolute path"):
            redaction.sanitize(b"C:\\other\\private.txt", self.roots)

    def test_credential_shaped_text_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Credential-shaped"):
            redaction.sanitize(("ghp_" + "A" * 25).encode("utf-8"), self.roots)

    def test_preexisting_placeholder_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "already occurs"):
            redaction.sanitize(b"__CONTENT_ROOT__", self.roots)


if __name__ == "__main__":
    unittest.main()
