"""Preserve failed003 test artifacts; supply the synthetic final-audit fixture's isolated batch config."""
import json
from b131_review_v3_common import HERE, TOOLS, freeze_json, frozen, require, sha, start_guard, write_frozen


def main():
    guard, _ = start_guard("B131003 test-only fixture successor")
    try:
        source = HERE / "test-controls-003.py"
        raw = frozen(source)
        text = raw.decode("utf-8").replace('ROOT = HERE / "validation-001"', 'ROOT = HERE / "validation-002"')
        anchor = '        freeze_json(self.case / (run + "-phase1.json"), {"auditDir": str(audit_path.parent)})'
        require(text.count(anchor) == 1, "Synthetic fixture anchor differs")
        text = text.replace(anchor, anchor +
                            '\n        write_frozen(self.case / "batch.json", frozen(HERE / "batch.json"))')
        compile(text, "test-controls-004.py", "exec")
        controls = write_frozen(HERE / "test-controls-004.py", text.encode("utf-8"))
        test_source = TOOLS / "test_b131_preparation_003.py"
        test_raw = frozen(test_source)
        test_text = test_raw.decode("utf-8").replace('"validation-001"', '"validation-002"').replace(
            '"test-controls-003.py"', '"test-controls-004.py"')
        compile(test_text, "test_b131_preparation_004.py", "exec")
        tool = write_frozen(TOOLS / "test_b131_preparation_004.py", test_text.encode("utf-8"))
        print(json.dumps(freeze_json(HERE / "validation-fixture-successor-004.json", {
            "controlsSource": {"path": str(source), "sha256": sha(raw)}, "controls": controls,
            "testSource": {"path": str(test_source), "sha256": sha(test_raw)}, "testTool": tool,
            "reason": "Synthetic final-audit test relocates common.HERE; it must also supply the unchanged "
                      "batch.json at that isolated fixture path. Runtime code/gates/prompts are unchanged. "
                      "All32 tests rerun; failed validation001 is preserved."})))
    finally:
        require(not guard.finish()["breach"], "Fixture preparation RAM breach")


if __name__ == "__main__":
    main()
