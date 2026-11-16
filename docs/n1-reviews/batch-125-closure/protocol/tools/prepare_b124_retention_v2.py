"""Preserve the first adapter and fix the confirmation source-label wrapper."""
import json
from pathlib import Path

from archive_b124_chains import prepare as original_prepare
from common import freeze_json, frozen, json_bytes, require, sha
from derive_selected_followups import derive_file
from verify_b124_archive import verify_chain as original_verify

HERE = Path(__file__).resolve().parent
OLD_FILTER = (
    '            if part["source"].startswith("evidence/external-snapshots/")\n'
    '            and part["source"] != "evidence/external-snapshots/manifest.json"'
)
NEW_FILTER = '            if is_local_only_source(part["source"])'
PREDICATE = '''def is_local_only_source(source):
    source = source.removeprefix("original-packet/")
    return (source.startswith("evidence/external-snapshots/")
            and source != "evidence/external-snapshots/manifest.json")


'''


def main():
    frozen(HERE / "archive_b124_chains.py",
           "5a5eed9018e2227e110a8c45b711fe4abc965f9a37f57c7daef1422c4b698909")
    frozen(HERE / "verify_b124_archive.py",
           "5261df0d97fd3fa585c29c7a811d61ae74e67fb1eeb756de64e4d2740e2693cc")
    frozen(HERE / "close_b124.py",
           "38ae4a86cd2c8a8ca2e501b6d0c658cd829559f983dd6a1e86c002f3a4379531")
    confirmation_raw = frozen(HERE / "confirm_v2.py")
    require(b'sources.append((f"original-packet/{path}", data, None))' in confirmation_raw,
            "Confirmation source-label contract changed")
    raw = b"synthetic complete capture\n"
    path = r"C:\synthetic\01.txt"
    manifest_raw = json_bytes({"segments": [{
        "index": 1, "path": path, "sha256": sha(raw), "bytes": len(raw),
        "parts": [{"source": "original-packet/evidence/external-snapshots/01-extract.txt",
                   "sha256": sha(raw), "a": 1, "b": 1}],
    }]})
    files, retention = original_prepare(manifest_raw, {path: raw})
    before = original_verify(files, {
        "segments": 1, "manifestSha256": sha(manifest_raw),
        "retentionSha256": sha(files["retention.json"]),
        "archivedSegmentIndices": retention["archivedSegmentIndices"],
        "localOnlySegmentIndices": [item["index"] for item in retention["localOnlySegments"]],
    })
    require(before["archivedSegments"] == 1 and before["localOnlySegments"] == 0,
            "Expected original wrapper defect was not reproduced")
    derivations = [
        derive_file("archive_b124_chains.py", "archive_b124_chains_v2.py", [
            ("def prepare(manifest_raw, segment_bytes):", PREDICATE + "def prepare(manifest_raw, segment_bytes):"),
            (OLD_FILTER, NEW_FILTER),
        ]),
        derive_file("verify_b124_archive.py", "verify_b124_archive_v2.py", [
            ("from common import ", "from archive_b124_chains_v2 import is_local_only_source\nfrom common import "),
            (OLD_FILTER, NEW_FILTER),
        ]),
        derive_file("test_archive_b124_chains.py", "test_archive_b124_chains_v2.py", [
            ("from archive_b124_chains import prepare", "from archive_b124_chains_v2 import prepare"),
            ('if __name__ == "__main__":', '''    def test_confirmation_wrapper_keeps_complete_capture_local(self):
        manifest_raw, segments = self.fixture(
            "original-packet/evidence/external-snapshots/01-extract.txt")
        files, retention = prepare(manifest_raw, segments)
        self.assertEqual(set(files), {"manifest.json", "retention.json"})
        self.assertEqual(retention["localOnlySegments"][0]["index"], 1)

    def test_confirmation_wrapper_preserves_metadata_archive(self):
        manifest_raw, segments = self.fixture(
            "original-packet/evidence/external-snapshots/manifest.json")
        files, retention = prepare(manifest_raw, segments)
        self.assertEqual(gzip.decompress(files["01.txt.gz"]), next(iter(segments.values())))
        self.assertEqual(retention["localOnlySegments"], [])


if __name__ == "__main__":'''),
        ]),
        derive_file("test_verify_b124_archive.py", "test_verify_b124_archive_v2.py", [
            ("from archive_b124_chains import prepare", "from archive_b124_chains_v2 import prepare"),
            ("from verify_b124_archive import verify_chain", "from verify_b124_archive_v2 import verify_chain"),
            ("    def fixture(self):", '    def fixture(self, prefix=""):'),
            ('(2, private, "evidence/external-snapshots/01-extract.txt"),',
             '(2, private, prefix + "evidence/external-snapshots/01-extract.txt"),'),
            ('if __name__ == "__main__":', '''    def test_wrapped_capture_is_omitted_and_cannot_be_restored(self):
        files, binding, private = self.fixture("original-packet/")
        self.assertEqual(verify_chain(files, binding)["localOnlySegments"], 1)
        files["02.txt.gz"] = gzip.compress(private, mtime=0)
        with self.assertRaisesRegex(ValueError, "local-only segment published"):
            verify_chain(files, binding)


if __name__ == "__main__":'''),
        ]),
        derive_file("close_b124.py", "close_b124_v2.py", [
            ("from archive_b124_chains import prepare as prepare_public_chain",
             "from archive_b124_chains_v2 import prepare as prepare_public_chain"),
            ('                     "b124-closure-derivation.json"):',
             '                     "b124-closure-derivation.json", "close_b124_v2.py",\n'
             '                     "archive_b124_chains_v2.py", "test_archive_b124_chains_v2.py",\n'
             '                     "verify_b124_archive.py", "test_verify_b124_archive.py",\n'
             '                     "verify_b124_archive_v2.py", "test_verify_b124_archive_v2.py",\n'
             '                     "test_close_b124_v2.py", "prepare_b124_retention_v2.py",\n'
             '                     "b124-retention-v2-derivation.json"):'),
        ]),
        derive_file("test_close_b124.py", "test_close_b124_v2.py", [
            ("from close_b124 import require_confirmation, require_intermediate",
             "from close_b124_v2 import require_confirmation, require_intermediate"),
            ("        from close_b124 import archive", "        from close_b124_v2 import archive"),
        ]),
    ]
    print(json.dumps(freeze_json(HERE / "b124-retention-v2-derivation.json", {
        "derivations": derivations,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "confirmationBuilder": {"path": str(HERE / "confirm_v2.py"), "sha256": sha(confirmation_raw)},
        "reproducedOriginalDefect": before,
        "scope": "Only the documented original-packet/ wrapper is normalized for source retention. "
                 "One predicate is shared by archive preparation and post-write verification. "
                 "The original adapters and proofs remain unchanged. All original reviewer, "
                 "candidate, acceptance, lineage, context and resource gates are preserved. "
                 "No closure or confirmation is run by this producer.",
    })))


if __name__ == "__main__":
    main()
