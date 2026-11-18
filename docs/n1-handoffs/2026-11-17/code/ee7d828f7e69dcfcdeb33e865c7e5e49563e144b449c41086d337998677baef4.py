import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

from b134_integration import CHANGED, CONTENT, REPO, check_incoming, check_merged, expected_manifest
from common import load_module

sys.path.insert(0, str(REPO / "tools"))
builder = load_module("b134_integration_builder", REPO / "tools" / "build_manifest.py")


class IntegrationPreservationTests(unittest.TestCase):
    def trees(self):
        base = {path: ("100644", "blob", "old-" + path)
                for path in CHANGED | {"kanji/example.md"}}
        incoming = {**base, **{path: ("100644", "blob", "new-" + path) for path in CHANGED}}
        closure = {**base, "kanji/example.md": ("100644", "blob", "reviewed-card"),
                   "docs/closure.json": ("100644", "blob", "review-history")}
        merged = {**closure, **{path: incoming[path] for path in CHANGED}}
        return base, incoming, closure, merged

    def test_exact_merge_and_concurrent_scope(self):
        base, incoming, closure, merged = self.trees()
        check_incoming(base, incoming)
        check_merged(closure, merged, incoming)

    def test_unrelated_changes_and_lost_incoming_content_reject(self):
        base, incoming, closure, merged = self.trees()
        for path in ("kanji/example.md", "docs/closure.json", "counters/kumiexpressions.json"):
            altered = {**merged, path: ("100644", "blob", "unexpected")}
            with self.subTest(path=path), self.assertRaises(ValueError):
                check_merged(closure, altered, incoming)
        with self.assertRaises(ValueError):
            check_incoming(base, {**incoming, "kanji/example.md": ("100644", "blob", "unreviewed")})
        with self.assertRaises(ValueError):
            check_merged(closure, {**merged, "extra": ("100644", "blob", "extra")}, incoming)
        with self.assertRaises(ValueError):
            check_incoming(base, {**incoming, "counters/kumiexpressions.json":
                                  ("120000", "blob", "symlink")})

    def test_expected_manifest_matches_actual_builder_and_preserves_input(self):
        content = {"articles/numbers-and-counters.md": b"new\r\narticle\r\n",
                   "counters/kumiexpressions.json": b'{"answers": []}\n'}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in CONTENT | {"kanji/example.md"}:
                target = root / path
                target.parent.mkdir(exist_ok=True)
                target.write_bytes(b"old\n")
            previous = builder.build_manifest(root)
            for path, raw in content.items():
                (root / path).write_bytes(raw)
            actual = builder.build_manifest(root)
        preserved = copy.deepcopy(previous)
        expected = expected_manifest(previous, content)
        self.assertEqual(previous, preserved)
        self.assertEqual(expected, (json.dumps(actual, ensure_ascii=False, indent=1,
                                              sort_keys=True) + "\n").encode())
        with self.assertRaises(ValueError):
            expected_manifest(previous, {**content, "kanji/extra.md": b"extra"})
        previous["duplicate"] = {"articles/numbers-and-counters.md": "duplicate"}
        with self.assertRaises(ValueError):
            expected_manifest(previous, content)


if __name__ == "__main__":
    unittest.main()
