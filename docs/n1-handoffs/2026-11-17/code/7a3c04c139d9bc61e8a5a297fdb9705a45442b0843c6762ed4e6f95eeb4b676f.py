"""Preserve first validation and align explicit prompts/fixtures with stricter B131 controls."""
import copy
import json
from pathlib import Path

from b131_neutral_common_001 import (HERE, TOOLS, freeze_json, frozen, json_bytes,
                                     require, sha, start_guard, write_frozen)


def main():
    guard, _ = start_guard("B131 explicit-control successor preparation")
    changes = []

    def successor(source, target, replacements):
        raw = frozen(source)
        text = raw.decode("utf-8").replace("\r\n", "\n")
        for before, after in replacements:
            require(text.count(before) == 1, "Successor anchor differs: " + before[:90])
            text = text.replace(before, after)
        compile(text, str(target), "exec")
        result = write_frozen(target, text.encode("utf-8"))
        changes.append({"source": {"path": str(source), "sha256": sha(raw)},
                        "output": result, "replacements": replacements})
        return result

    try:
        failure_path = HERE / "validation-001" / "result.json"
        failure = json.loads(frozen(failure_path))
        require(failure["status"] == "FAIL" and len(failure["failures"]) == len(failure["errors"]) == 1,
                "Expected preserved first fixture-validation outcome")
        chain_fixture = successor(
            HERE / "test-review-chain.py", HERE / "test-review-chain-controls-002.py", [
                ('        self.assertTrue(result["valid"])\n'
                 '        self.assertEqual([e["character"] for e in result["entries"]], ["五", "五", "四"])',
                 '        self.assertFalse(result["valid"])\n'
                 '        self.assertIn("Duplicate comparison character", result["errors"])\n'
                 '        self.assertEqual([e["character"] for e in result["entries"]], ["五", "五", "四"])')])
        audit_fixture = successor(
            HERE / "test-review-audit.py", HERE / "test-review-audit-controls-002.py", [
                ('        path.write_bytes(json.dumps(config).encode("utf-8"))\n'
                 '        with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):',
                 '        path.write_bytes(json.dumps(config).encode("utf-8"))\n'
                 '        path.chmod(stat.S_IREAD)\n'
                 '        with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):')])
        lifecycle = successor(TOOLS / "step_b131_neutral_001.py", TOOLS / "step_b131_neutral_002.py", [
            ('"preflight-compact-001.json"', '"preflight-compact-002.json"'),
            ('str(TOOLS / "step_b131_neutral_001.py")',
             'str(TOOLS / "step_b131_neutral_002.py")'),
            ('sha((TOOLS / "step_b131_neutral_001.py").read_bytes())',
             'sha((TOOLS / "step_b131_neutral_002.py").read_bytes())')])
        validation = successor(TOOLS / "test_b131_neutral_preparation_001.py",
                               TOOLS / "test_b131_neutral_preparation_002.py", [
            ('"preflight-compact-001.json"', '"preflight-compact-002.json"'),
            ('output = HERE / "validation-001"', 'output = HERE / "validation-002"'),
            ('for name in ("test-review-chain.py", "test-report-structure.py", "test-review-audit.py"):',
             'for name in ("test-review-chain-controls-002.py", "test-report-structure.py", '
             '"test-review-audit-controls-002.py"):')])
        old_preflight_path = HERE / "prompts" / "preflight-compact-001.json"
        preflight = json.loads(frozen(old_preflight_path))
        outputs, rendered = {}, {}
        for key in ("claude", "gpt"):
            spec = preflight["runs"][key]
            old_prompt, old_kickoff = Path(spec["prompt"]), Path(spec["kickoff"])
            new_prompt = old_prompt.with_name(old_prompt.name.replace("-001.txt", "-002.txt"))
            new_kickoff = old_kickoff.with_name(old_kickoff.name.replace("-001.txt", "-002.txt"))
            prompt = frozen(old_prompt, spec["promptSha256"]).decode("utf-8")
            anchor = "Before sending your final D/E lists, check every entry against this reference."
            require(prompt.count(anchor) == 1, "Unique-entry disclosure anchor differs")
            prompt = prompt.replace(anchor, "Use each requested comparison character at most once across "
                                    "both lists; for a shared D candidate name all related new cards on "
                                    "its single line. Duplicate comparison characters invalidate the list.\n\n" + anchor)
            prompt = prompt.replace(str(old_prompt), str(new_prompt))
            kickoff = frozen(old_kickoff).decode("ascii").replace(str(old_prompt), str(new_prompt))
            rendered[key] = prompt.encode("utf-8")
            old_config_path = Path(spec["auditConfig"])
            audit = json.loads(frozen(old_config_path))
            bindings = []
            replacements = {
                str(TOOLS / "step_b131_neutral_001.py"): lifecycle,
                str(HERE / "test-review-chain.py"): chain_fixture,
                str(HERE / "test-review-audit.py"): audit_fixture}
            for binding in audit["files"]:
                path = binding["path"]
                if path == str(old_prompt):
                    bindings.append({"path": str(new_prompt), "sha256": sha(rendered[key])})
                elif path == str(old_kickoff):
                    bindings.append({"path": str(new_kickoff), "sha256": sha(kickoff.encode("ascii"))})
                else:
                    replacement = replacements.get(path, binding)
                    bindings.append({"path": replacement["path"], "sha256": replacement["sha256"]})
            audit.update(prompt=str(new_prompt), kickoff=str(new_kickoff), files=bindings)
            audit_path = old_config_path.with_name(old_config_path.stem + "-controls-002.json")
            outputs.update({new_prompt: rendered[key], new_kickoff: kickoff.encode("ascii"),
                            audit_path: json_bytes(audit)})
            spec.update(prompt=str(new_prompt), promptSha256=sha(rendered[key]),
                        kickoff=str(new_kickoff), kickoffText=kickoff, auditConfig=str(audit_path))
        require(rendered["claude"].replace(b"CLAUDE", b"GPT").replace(b"-claude-", b"-gpt-")
                == rendered["gpt"], "Successor prompts differ beyond identity")
        for path, data in outputs.items():
            write_frozen(path, data)
        preflight.update(
            predecessor={"path": str(old_preflight_path), "sha256": sha(frozen(old_preflight_path))},
            controlsRevision="Explicit duplicate-character refusal; no gate relaxed.",
            preparationOnly=True)
        preflight_binding = freeze_json(HERE / "prompts" / "preflight-compact-002.json", preflight)
        result = freeze_json(HERE / "protocol-controls-revision-002.json", {
            "status": "PREPARED_REQUIRES_VALIDATION", "batch": 131, "preflight": preflight_binding,
            "preservedFailure": {"path": str(failure_path), "sha256": sha(frozen(failure_path))},
            "changes": changes,
            "explanation": "The original generic fixture allowed duplicate characters; B131's stronger "
                           "validator rejects them. The successor prompt now makes that rejection explicit, "
                           "and the fixture expects rejection. The other fixture now freezes its incomplete "
                           "config so the existing missing-fetch-limit gate, not the earlier frozen-input "
                           "gate, is reached. No execution, report, context or fetch gate is relaxed.",
            "supersededForLaunch": [str(old_preflight_path), str(TOOLS / "step_b131_neutral_001.py")],
            "limits": "No reviewer has run; prior frozen preparation and failure remain unchanged."})
        print(json.dumps(result))
    finally:
        require(not guard.finish()["breach"], "Control-successor preparation RAM breach")


if __name__ == "__main__":
    main()
