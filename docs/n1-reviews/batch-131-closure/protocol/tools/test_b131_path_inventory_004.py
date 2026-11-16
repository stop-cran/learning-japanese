"""Focused rejection of inventory/runtime drift; no actual reviewer state is opened."""
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from b131_review_v3_common import (
    DEFAULT_PREFLIGHT, HERE, freeze_json, frozen, require, sha, start_guard, write_frozen)
import b131_path_readiness_004 as inventory


class InventoryTests(unittest.TestCase):
    def test_inventory_matches_pinned_actual003_builder(self):
        records = inventory.path_inventory(json.loads(frozen(DEFAULT_PREFLIGHT)))
        for row in records:
            expected = HERE / "chains" / ("b131-" + row["run"] + "-extension-003")
            self.assertEqual(row["extension"]["directory"], str(expected))
        self.assertEqual(len(records), 2)

    def test_changed_builder_expression_rejected(self):
        source = frozen(inventory.BUILDER, inventory.BUILDER_SHA)
        changed = source.replace(b"-extension-003", b"-extension-999")
        with patch.object(inventory, "frozen", return_value=changed):
            with self.assertRaisesRegex(ValueError, "builder expression differs"):
                inventory.path_inventory(json.loads(frozen(DEFAULT_PREFLIGHT)))

    def test_corrected_proof_preserves_original_and_has_actual_paths(self):
        proof = json.loads(frozen(HERE / "path-readiness-004.json"))
        original = proof["supersedesInventoryOnly"]
        frozen(original["path"], original["sha256"])
        self.assertEqual(proof["actualBuilder"]["sha256"], inventory.BUILDER_SHA)
        self.assertEqual(proof["reviewerPathInventory"],
                         inventory.path_inventory(json.loads(frozen(DEFAULT_PREFLIGHT))))


def main():
    guard, _ = start_guard("B131003 inventory-only focused controls")
    try:
        root = HERE / "validation-paths-004"
        require(not root.exists(), "Preserve existing validation")
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(InventoryTests))
        text = stream.getvalue()
        write_frozen(root / "output.log", text.encode("utf-8"))
        memory = guard.finish()
        require(not memory["breach"], "Inventory controls RAM breach")
        record = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
                  "errors": len(result.errors), "failures": len(result.failures), "memory": memory,
                  "testTool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
                  "outputSha256": sha(text.encode("utf-8"))}
        print(text)
        print(json.dumps(freeze_json(root / "result.json", record)))
        return 0 if result.wasSuccessful() else 1
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    raise SystemExit(main())
