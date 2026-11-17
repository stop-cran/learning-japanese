import importlib.util
import json
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "b131_incoming_main", Path(__file__).with_name("verify_b131_incoming_main.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class IncomingMainTests(unittest.TestCase):
    def trees(self):
        before = {path: ("100644", "blob", "old") for path in module.MODIFIED}
        before["kanji/unchanged.md"] = ("100644", "blob", "preserved")
        after = {**before, **{path: ("100644", "blob", "new")
                             for path in module.ADDED | module.MODIFIED}}
        return before, after

    def test_only_the_declared_word_delta_is_admitted(self):
        before, after = self.trees()
        self.assertEqual(module.tree_delta(before, after), 1)
        after["kanji/unchanged.md"] = ("100644", "blob", "changed")
        with self.assertRaisesRegex(ValueError, "existing-path"):
            module.tree_delta(before, after)

    def test_deleted_or_mode_changed_baseline_is_rejected(self):
        before, after = self.trees()
        del after["kanji/unchanged.md"]
        with self.assertRaisesRegex(ValueError, "added or removed"):
            module.tree_delta(before, after)
        before, after = self.trees()
        after["README.md"] = ("100755", "blob", "new")
        with self.assertRaisesRegex(ValueError, "modes"):
            module.tree_delta(before, after)

    def test_binary_manifest_deltas_cannot_hide_outside_files(self):
        before = {
            "files": {module.OLD_WORD: "old"},
            "audio": {"audio/preserved.ogg": "audio-old"},
        }
        after = {
            "files": {module.OLD_WORD: "new", module.NEW_WORD: "added"},
            "audio": {"audio/preserved.ogg": "audio-changed"},
        }
        with self.assertRaisesRegex(ValueError, "Existing runtime hashes"):
            module.manifest_delta(json.dumps(before).encode(), json.dumps(after).encode())


if __name__ == "__main__":
    unittest.main()
