"""Derive a subprocess-import repair without modifying frozen review inputs."""
import ast
import json
from pathlib import Path

from b131_review_v3_common import RECORDS, TOOLS, freeze_json, frozen, require, sha, write_frozen


def replace_once(text, old, new):
    require(text.count(old) == 1, f"Expected exactly one replacement: {old!r}")
    return text.replace(old, new)


def main():
    helper_path = TOOLS / "b131_lifecycle_process_004.py"
    step_path = TOOLS / "step_b131_neutral_005.py"
    helper_raw = frozen(helper_path, "ddd66ed39fe811afd316b63696e37f06e9433276d2c8a696a958f4c4f71e1e6d")
    step_raw = frozen(step_path, "0d52040fa4208ddd3005784b0fc72d70f116743ffc55f9a8b8809a880937f08a")
    helper = replace_once(
        helper_raw.decode("utf-8"),
        '"PYTHONDONTWRITEBYTECODE": "1"})',
        '"PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(TOOLS)})',
    )
    step = step_raw.decode("utf-8").replace("step_b131_neutral_005.py", "step_b131_neutral_006.py")
    step = replace_once(step, "from b131_lifecycle_process_004 import python",
                        "from b131_lifecycle_process_005 import python")
    step = replace_once(step, 'records / f"{run}-context.json", ctx',
                        'records / f"{run}-context-{path.parent.name}.json", ctx')
    step = replace_once(step, 'records / f"{run}-structure.json", structure',
                        'records / f"{run}-structure-{path.parent.name}.json", structure')
    ast.parse(helper)
    ast.parse(step)
    outputs = [
        write_frozen(TOOLS / "b131_lifecycle_process_005.py", helper.encode("utf-8")),
        write_frozen(TOOLS / "step_b131_neutral_006.py", step.encode("utf-8")),
    ]
    proof = {
        "status": "DERIVED_NOT_YET_QUALIFIED",
        "inputs": [
            {"path": str(helper_path), "sha256": sha(helper_raw)},
            {"path": str(step_path), "sha256": sha(step_raw)},
        ],
        "outputs": outputs,
        "changes": [
            "Set child PYTHONPATH to the frozen shared review-tools directory so review_chain can import b131_capacity_002.",
            "Use the repaired helper and report the successor lifecycle tool identity.",
            "Bind context and structure filenames to the new audit directory, preserving prior partial-final outputs.",
        ],
        "unchanged": "Reviewer prompts, candidate, packet, chains, selection, raw report, checker code, acceptance checks and thresholds.",
        "failurePreserved": {
            "receipt": str(RECORDS / "preparation003-claude-final-execution-001" / "receipt.json"),
            "receiptSha256": "2eac7ec3b74086661c6dba4e1062e19b04a786e89bc21810669999d39de7242b",
            "logSha256": "b9d68a74a76e11f44036780244425472097afb2e671dd4548dc0a59b46c3169f",
        },
    }
    print(json.dumps(freeze_json(RECORDS / "preparation003-lifecycle006-derivation-001.json", proof)))


if __name__ == "__main__":
    main()
