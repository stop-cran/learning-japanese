import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

from common import WS
from verify_b130_integration_runtime import CONTENT, check_trees, expected_manifest

sys.path.insert(0, str(WS / "b130-worktree" / "tools"))
from build_manifest import build_manifest


def object_id(value, mode="100644"):
    return (mode, "blob", value)


class IntegrationRuntimeTests(unittest.TestCase):
    def trees(self):
        base = {path: object_id("old-" + path) for path in CONTENT | {"manifest.json", "kanji/test.md"}}
        closure = {**base, "kanji/test.md": object_id("reviewed-card"),
                   "docs/closure.json": object_id("old-evidence"), "manifest.json": object_id("ours-manifest")}
        incoming = {**base, **{path: object_id("incoming-" + path) for path in CONTENT},
                    "manifest.json": object_id("incoming-manifest")}
        merged = {**closure, **{path: incoming[path] for path in CONTENT},
                  "manifest.json": object_id("combined-manifest")}
        return base, closure, incoming, merged

    def test_exact_merge_preserves_all_other_objects(self):
        check_trees(*self.trees())

    def test_rejects_card_changes_lost_counter_and_changed_evidence(self):
        base, closure, incoming, merged = self.trees()
        changes = [
            {"kanji/test.md": object_id("unreviewed")},
            {"docs/closure.json": object_id("rewritten")},
            {"counters/age.json": closure["counters/age.json"]},
        ]
        for delta in changes:
            with self.subTest(delta=delta), self.assertRaises(ValueError):
                check_trees(base, closure, incoming, {**merged, **delta})
        with self.assertRaises(ValueError):
            check_trees(base, closure, {**incoming, "kanji/test.md": object_id("incoming-extra")}, merged)

    def test_rejects_added_files_and_nonregular_counter(self):
        base, closure, incoming, merged = self.trees()
        with self.assertRaises(ValueError):
            check_trees(base, closure, incoming, {**merged, "extra": object_id("new")})
        incoming["counters/age.json"] = object_id("link", "120000")
        merged["counters/age.json"] = incoming["counters/age.json"]
        with self.assertRaises(ValueError):
            check_trees(base, closure, incoming, merged)

    def test_manifest_updates_only_incoming_hashes_and_recomputes_version(self):
        content = {"articles/numbers-and-counters.md": b"new\r\narticle\r\n",
                   "counters/age.json": b'{"answers": []}\n'}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in CONTENT | {"kanji/test.md"}:
                target = root / path
                target.parent.mkdir(exist_ok=True)
                target.write_bytes(b"old\n")
            previous = build_manifest(root)
            for path, raw in content.items():
                (root / path).write_bytes(raw)
            actual = build_manifest(root)
        original = copy.deepcopy(previous)
        result = json.loads(expected_manifest(previous, content))
        self.assertEqual(previous, original)
        self.assertEqual(result, actual)
        self.assertEqual(result["files"]["kanji/test.md"], previous["files"]["kanji/test.md"])
        self.assertEqual(result["files"]["articles/numbers-and-counters.md"],
                         hashlib.sha256(b"new\narticle\n").hexdigest())
        self.assertEqual(expected_manifest(previous, content),
                         (json.dumps(actual, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode())
        with self.assertRaises(ValueError):
            expected_manifest(previous, {**content, "kanji/extra.md": b"unreviewed"})
        previous["duplicate"] = {"articles/numbers-and-counters.md": "duplicate"}
        with self.assertRaises(ValueError):
            expected_manifest(previous, content)


if __name__ == "__main__":
    unittest.main()
