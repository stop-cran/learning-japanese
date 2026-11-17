import json
import unittest
from unittest.mock import patch

from b129_closure_revision import bounded_void, confirmation_origin, replace_exact
from common import sha
from prepare_b129_initial_replacement import FAILED_RUN


class IdentityTests(unittest.TestCase):
    def test_original_must_retain_identity(self):
        args = ({"session": "old"}, {"session": "old"}, {"session": "old"},
                {}, {}, {"batch": 129}, None, "final", None)
        self.assertEqual(confirmation_origin(*args)["reviewerOrigin"], "original")
        changed = list(args)
        changed[1] = {"session": "fresh"}
        with self.assertRaises(ValueError):
            confirmation_origin(*changed)

    def test_replacement_requires_proven_lineage_and_explicit_attribution(self):
        spec = {"session": "fresh", "family": "claude", "originalSession": "old",
                "replayedFrom": {}, "unavailable": {}}
        accepted = {"reviewerOrigin": "fresh-context-replacement",
                    "replacesUnavailable": FAILED_RUN, "originalSession": "old"}
        args = (spec, {"session": "fresh"}, {"session": "old"}, accepted,
                {}, {"batch": 129}, None, "final", None)
        with patch("b129_closure_revision.verify_replacement") as verify:
            result = confirmation_origin(*args)
            verify.assert_called_once()
            self.assertEqual(result["replacementFor"], FAILED_RUN)
            for index, value in ((3, {}), (7, "intermediate"), (8, "prior")):
                invalid = list(args)
                invalid[index] = value
                with self.subTest(index=index), self.assertRaises(ValueError):
                    confirmation_origin(*invalid)
        with patch("b129_closure_revision.verify_replacement", side_effect=ValueError("lineage")):
            with self.assertRaisesRegex(ValueError, "lineage"):
                confirmation_origin(*args)

    def test_void_summary_retains_failure_without_raw_messages(self):
        audit = {"status": "VOID", "reviewerIdle": True, "writes": 0, "readbacks": 0,
                 "messages": ["UNVERIFIED"], "chainRead": 63, "chainRequired": 65,
                 "breaches": ["preserved failure"], "unexpectedUserMessages": ["raw stop"]}
        summary = bounded_void(audit, "a" * 64)
        self.assertEqual(summary["breachesCount"], 1)
        self.assertEqual(summary["chainRead"], 63)
        self.assertFalse(summary["reviewEvidenceAccepted"])
        self.assertNotIn("raw stop", json.dumps(summary))
        with self.assertRaises(ValueError):
            bounded_void({**audit, "writes": 1}, "a" * 64)

    def test_derivation_rejects_missing_or_ambiguous_anchor(self):
        self.assertEqual(replace_exact("before", [("before", "after")]), "after")
        for text in ("missing", "before before"):
            with self.assertRaises(ValueError):
                replace_exact(text, [("before", "after")])


class RetentionTests(unittest.TestCase):
    def test_new_complete_sources_are_local_and_verified(self):
        from archive_b129_chains import prepare, is_local_only_source
        from verify_b129_archive_v2 import verify_chain
        for source in ("external-reconciliation/01-complete-lexical.txt",
                       "original-source-sections/rainbow-wiktionary-japanese.txt",
                       "original-packet/evidence/external-snapshots/04-extract.txt"):
            self.assertTrue(is_local_only_source(source))
        self.assertFalse(is_local_only_source("evidence/reconciliation/query-membership.jsonl"))
        raw = b"complete external article plus co-located teaching card"
        segment = {"index": 1, "path": "segment-001.txt", "bytes": len(raw), "sha256": sha(raw),
                   "parts": [{"source": "external-reconciliation/01-complete-lexical.txt",
                              "sha256": "c" * 64, "a": 1, "b": 2}]}
        manifest_raw = json.dumps({"segments": [segment]}).encode()
        files, retention = prepare(manifest_raw, {"segment-001.txt": raw})
        self.assertEqual(set(files), {"manifest.json", "retention.json"})
        binding = {"manifestSha256": sha(manifest_raw), "retentionSha256": sha(files["retention.json"]),
                   "segments": 1, "archivedSegmentIndices": [], "localOnlySegmentIndices": [1]}
        self.assertEqual(verify_chain(files, binding)["localOnlySegments"], 1)
        with self.assertRaises(ValueError):
            verify_chain({**files, "segment-001.txt.gz": b"leaked"}, binding)


if __name__ == "__main__":
    unittest.main()
