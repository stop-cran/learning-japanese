"""Focused negative checks for the bounded batch107 audit's extra scope."""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "batch107audit", Path(__file__).with_name("audit-batch-107-runtime.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class Batch107AuditTest(unittest.TestCase):
    def test_source_representation_requires_raw_receipt_and_exact_text(self):
        raw = b"source\r\n"
        audit.verify_source_bytes(raw, b"source\n", audit.sha(raw))
        with self.assertRaisesRegex(ValueError, "raw hash changed"):
            audit.verify_source_bytes(raw, b"source\n", audit.sha(b"source\n"))
        with self.assertRaisesRegex(ValueError, "differs from signed"):
            audit.verify_source_bytes(raw, b"changed\n", audit.sha(raw))
        with self.assertRaisesRegex(ValueError, "differs from signed"):
            audit.verify_source_bytes(raw, b"source\n", audit.sha(raw), binary=True)

    def test_missing_component_direction_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "kanji").mkdir()
            (root / "words").mkdir()
            (root / "kanji" / "定.md").write_text("[word](../words/勘定.md)", encoding="utf-8")
            (root / "words" / "勘定.md").write_text("unlinked component", encoding="utf-8")
            directions = [
                {"from": "kanji/定.md", "to": "words/勘定.md", "relative": "../words/勘定.md"},
                {"from": "words/勘定.md", "to": "kanji/定.md", "relative": "../kanji/定.md"},
            ]
            with self.assertRaisesRegex(ValueError, "Missing required direction"):
                audit.verify_directions(root, directions, {("定", "words/勘定.md")})

    def test_omitted_pair_is_rejected_before_reading(self):
        with self.assertRaisesRegex(ValueError, "enumerate every mapped pair"):
            audit.verify_directions(Path("."), [], {("違", "words/勘違い.md")})

    def test_frozen_full_reading_extension_is_rejected(self):
        plan = audit.load(audit.S / "batch-107-source-completion-plan.json")["kanjiPlan"]
        meta = audit.metadata(audit.R, "kanji/勘.md")
        raw = audit.ET.parse(audit.S / "batch-107-kanjidic2.xml").getroot().find("character")
        audit.verify_member(meta, plan, raw)
        changed = copy.deepcopy(meta)
        changed["kunyomi"] = ["かんが.える"]
        with self.assertRaisesRegex(ValueError, "metadata differs"):
            audit.verify_member(changed, plan, raw)

    def test_changed_generated_geometry_is_rejected(self):
        svg = (audit.S / "batch-107-kanjivg.svg").read_bytes()
        evidence = audit.load(audit.S / "batch-107-stroke-evidence.json")
        row = audit.load(audit.S / "batch-107-input-metadata.json")["sourceIndexRecord"]
        geometry = audit.load(audit.R / "strokes" / "勘.json")
        converter = (audit.R / "tools" / "generate_strokes.py").read_bytes()
        audit.verify_geometry(svg, geometry, evidence, row, converter)
        geometry["strokes"][0]["points"][0][0] += 0.1
        with self.assertRaisesRegex(ValueError, "Geometry differs"):
            audit.verify_geometry(svg, geometry, evidence, row, converter)

    def test_extra_reused_edit_is_rejected(self):
        plan = audit.load(audit.S / "batch-107-source-completion-plan.json")
        edit = plan["linkPlan"]["exactReusedChanges"][3]
        before = audit.git_bytes(audit.BASE, edit["article"]).decode("utf-8")
        after = (audit.R / edit["article"]).read_text(encoding="utf-8")
        audit.reused_changes(before, after, [edit])
        with self.assertRaisesRegex(ValueError, "exceeds recorded exact edits"):
            audit.reused_changes(before, after + "\nUnrelated teaching.\n", [edit])

    def test_new_word_and_empty_section_changes_are_rejected(self):
        before = {"schemaVersion": 1, "baseLanguage": "en", "files": {}, "images": {}}
        after = copy.deepcopy(before)
        after["files"]["words/duplicate.md"] = "hash"
        with self.assertRaisesRegex(ValueError, "Runtime additions differ"):
            audit.runtime_delta(before, after, {"kanji/勘.md", "strokes/勘.json"}, set())
        del after["images"]
        with self.assertRaisesRegex(ValueError, "sections changed"):
            audit.runtime_delta(before, after, set(), set())


if __name__ == "__main__":
    unittest.main()
