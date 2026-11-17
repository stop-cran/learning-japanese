import gzip
import unittest

from close_b132 import WINDOW, publication_findings, put
from common import json_bytes


class Guard:
    def check(self):
        pass


class PublicationRetentionTests(unittest.TestCase):
    def test_external_windows_are_found_in_compressed_segments_and_json_strings(self):
        protected = "\u5893" * WINDOW
        files = {
            "chain.txt.gz": gzip.compress(protected.encode("utf-8")),
            "escaped.json": ('{"text":"' + "\\u5893" * WINDOW + '"}').encode("ascii"),
        }
        uuids, leaks = publication_findings(files, {protected}, set(), Guard())
        self.assertEqual(uuids, [])
        self.assertEqual({row["file"] for row in leaks}, set(files))

    def test_unrelated_sessions_rejected_but_review_identity_allowed(self):
        reviewer = "11111111-2222-4333-8444-555555555555"
        unrelated = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
        files = {"audit.json": json_bytes({"reviewer": reviewer, "other": unrelated})}
        uuids, leaks = publication_findings(files, set(), {reviewer}, Guard())
        self.assertEqual({row["uuid"] for row in uuids}, {unrelated})
        self.assertEqual(leaks, [])

    def test_raw_sources_events_and_conflicting_replacements_are_rejected(self):
        files = {}
        put(files, "review/report.md", b"bounded report")
        for name in ("../escape", ".", "provenance.json", "events.jsonl", "response.html"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                put(files, name, b"private input")
        with self.assertRaises(ValueError):
            put(files, "review/report.md", b"replacement")
        self.assertEqual(files, {"review/report.md": b"bounded report"})


if __name__ == "__main__":
    unittest.main()
