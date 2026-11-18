"""Correct only the frozen path inventory's extension suffix; keep runtime/prompts/preflight unchanged."""
import json

from b131_review_v3_common import (
    DEFAULT_PREFLIGHT, HERE, TOOLS, freeze_json, frozen, require, sha, start_guard)
from b131_preflight_003 import path_inventory as prior_inventory

BUILDER = TOOLS / "prepare_chain_b131_003.py"
BUILDER_SHA = "f8317b00573bee1c4c298bfe696a2d5f7954eaa8e60244229cee05a6914478eb"
EXPRESSION = 'directory = HERE / "chains" / f"b131-{args.run}-extension-003"'


def path_inventory(preflight):
    source = frozen(BUILDER, BUILDER_SHA).decode("utf-8")
    require(source.count(EXPRESSION) == 1, "Actual extension-directory builder expression differs")
    records = prior_inventory(preflight)
    for row in records:
        row["extension"]["directory"] = str(HERE / "chains" / ("b131-" + row["run"] + "-extension-003"))
    return records


def main():
    guard, _ = start_guard("B131003 corrected path-readiness inventory")
    try:
        preflight = json.loads(frozen(DEFAULT_PREFLIGHT))
        inventory = path_inventory(preflight)
        original = HERE / "path-readiness-003.json"
        result = {
            "status": "PASS", "reportDirectories": [row["reportCreate"] for row in inventory],
            "reviewerPathInventory": inventory,
            "supersedesInventoryOnly": {"path": str(original), "sha256": sha(frozen(original))},
            "actualBuilder": {"path": str(BUILDER), "sha256": BUILDER_SHA, "expression": EXPRESSION},
            "correction": "The original inventory said extension-002, while the actual003 builder uses "
                          "extension-003. Only this metadata is corrected. Prompt/preflight/runtime, "
                          "evidence and all gates are unchanged. Both report parents were re-probed and left empty."}
        result["memory"] = guard.finish()
        require(not result["memory"]["breach"], "Path correction RAM breach")
        print(json.dumps(freeze_json(HERE / "path-readiness-004.json", result)))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
