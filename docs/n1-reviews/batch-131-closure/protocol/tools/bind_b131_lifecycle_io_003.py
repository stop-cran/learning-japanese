"""Bind the corrected child-output boundary before any reviewer launch."""
import json
from pathlib import Path

from b131_neutral_common_001 import (HERE, TOOLS, freeze_json, frozen, json_bytes,
                                     require, sha, start_guard, write_frozen)


def main():
    guard, _ = start_guard("B131 lifecycle output boundary binding")
    try:
        source = TOOLS / "step_b131_neutral_002.py"
        target = TOOLS / "step_b131_neutral_003.py"
        text = frozen(source).decode("utf-8")
        replacements = [
            ("from b131_lifecycle_process_001 import python", "from b131_lifecycle_process_002 import python"),
            ('"preflight-compact-002.json"', '"preflight-compact-003.json"'),
            ('str(TOOLS / "step_b131_neutral_002.py")', 'str(TOOLS / "step_b131_neutral_003.py")'),
            ('sha((TOOLS / "step_b131_neutral_002.py").read_bytes())',
             'sha((TOOLS / "step_b131_neutral_003.py").read_bytes())')]
        for before, after in replacements:
            require(text.count(before) == 1, "Lifecycle successor anchor differs")
            text = text.replace(before, after)
        compile(text, str(target), "exec")
        tool = write_frozen(target, text.encode("utf-8"))
        validation_source = TOOLS / "test_b131_neutral_preparation_002.py"
        validation_target = TOOLS / "test_b131_neutral_preparation_003.py"
        validation_text = frozen(validation_source).decode("utf-8")
        for before, after in (
            ('"preflight-compact-002.json"', '"preflight-compact-003.json"'),
            ('output = HERE / "validation-002"', 'output = HERE / "validation-003"'),
            ('    try:\n        result = unittest.TextTestRunner(verbosity=2).run(suite)',
             '    io_tests = module("b131_lifecycle_io_tests", TOOLS / "test_b131_lifecycle_io_003.py")\n'
             '    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(io_tests))\n'
             '    try:\n        result = unittest.TextTestRunner(verbosity=2).run(suite)')):
            require(validation_text.count(before) == 1, "Validation successor anchor differs")
            validation_text = validation_text.replace(before, after)
        compile(validation_text, str(validation_target), "exec")
        validation = write_frozen(validation_target, validation_text.encode("utf-8"))
        old = HERE / "prompts" / "preflight-compact-002.json"
        preflight = json.loads(frozen(old))
        for key in ("claude", "gpt"):
            spec = preflight["runs"][key]
            config = json.loads(frozen(spec["auditConfig"]))
            for item in config["files"]:
                if item["path"] == str(source):
                    item.update(path=tool["path"], sha256=tool["sha256"])
                elif item["path"] == str(TOOLS / "b131_lifecycle_process_001.py"):
                    item.update(path=str(TOOLS / "b131_lifecycle_process_002.py"),
                                sha256=sha(frozen(TOOLS / "b131_lifecycle_process_002.py")))
            config["files"].extend([
                {"path": validation["path"], "sha256": validation["sha256"]},
                {"path": str(TOOLS / "test_b131_lifecycle_io_003.py"),
                 "sha256": sha(frozen(TOOLS / "test_b131_lifecycle_io_003.py"))}])
            destination = HERE / "prompts" / f"audit-config-{spec['run']}-io-003.json"
            write_frozen(destination, json_bytes(config))
            spec["auditConfig"] = str(destination)
        preflight.update(predecessor={"path": str(old), "sha256": sha(frozen(old))},
                         lifecycleOutputBoundary="Exact child output; runner envelopes retained separately.")
        final_preflight = freeze_json(HERE / "prompts" / "preflight-compact-003.json", preflight)
        result = freeze_json(HERE / "lifecycle-io-binding-003.json", {
            "status": "PREPARED_REQUIRES_VALIDATION", "preflight": final_preflight,
            "lifecycle": tool, "validation": validation,
            "source": {"path": str(source), "sha256": sha(frozen(source))},
            "changes": replacements,
            "reason": "Code-path inspection found that the first adapter returned runner-envelope stdout "
                      "to consumers expecting child JSON. The successor returns verified raw child bytes, "
                      "while retaining the raw runner streams and actual memory/exit receipts separately. "
                      "The synthetic success/refusal test exercises the real adapter; no session is launched.",
            "supersededForLaunch": [str(old), str(source), str(TOOLS / "b131_lifecycle_process_001.py")]})
        print(json.dumps(result))
    finally:
        require(not guard.finish()["breach"], "Lifecycle IO binding RAM breach")


if __name__ == "__main__":
    main()
