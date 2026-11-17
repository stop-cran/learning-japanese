import copy
import importlib.util
import unittest
from pathlib import Path

from common import TOOLS, sha

spec = importlib.util.spec_from_file_location("build_prompts_v3", TOOLS / "build-prompts-v3.py")
v3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v3)

PROMPTS = Path(r"C:\ws\scratch-9\review\prompts")
REPORT = r"C:\ws\reports-9\initial-claude-001.md"
PROMPT = (f"RUN N1-B9-CLAUDE-001\nWrite {REPORT} once.\nThis file: {PROMPTS}\\initial-claude-001.txt\n"
          "Unrelated -001 token stays.\n").encode("utf-8")
KICKOFF = f"Read {PROMPTS}\\initial-claude-001.txt using one view call.".encode("ascii")
SPEC = {"run": "N1-B9-CLAUDE-001", "prompt": str(PROMPTS / "initial-claude-001.txt"), "promptSha256": sha(PROMPT),
        "kickoff": str(PROMPTS / "kickoff-claude-001.txt"), "kickoffText": KICKOFF.decode("ascii"),
        "auditConfig": str(PROMPTS / "audit-config-N1-B9-CLAUDE-001.json"), "report": REPORT,
        "launch": {"model": "m", "sessionName": "B9 Claude review 001"}}
AUDIT = {"run": "N1-B9-CLAUDE-001", "files": [{"path": "tool.py", "sha256": "t"},
                                              {"path": SPEC["prompt"], "sha256": sha(PROMPT)},
                                              {"path": SPEC["kickoff"], "sha256": sha(KICKOFF)}]}


class AttemptDerivationTests(unittest.TestCase):
    def test_only_run_identity_changes(self):
        out = v3.derive(SPEC, AUDIT, PROMPT, KICKOFF, 9, "claude", 2, PROMPTS)
        prompt = out["prompt"][1].decode("utf-8")
        self.assertIn("RUN N1-B9-CLAUDE-002", prompt)
        self.assertIn("initial-claude-002.md", prompt)
        self.assertIn("Unrelated -001 token stays.", prompt)
        self.assertEqual(out["spec"]["launch"]["sessionName"], "B9 Claude review 002")
        self.assertEqual(out["spec"]["report"], r"C:\ws\reports-9\initial-claude-002.md")
        paths = [f["path"] for f in __import__("json").loads(out["audit"][1])["files"]]
        self.assertEqual(paths, ["tool.py", str(PROMPTS / "initial-claude-002.txt"),
                                 str(PROMPTS / "kickoff-claude-002.txt")])
        self.assertEqual(v3.reverse(out["prompt"][1], v3.identity_pairs(9, "CLAUDE", "claude", 2)), PROMPT)

    def test_rejects_preexisting_attempt_identity_or_missing_tokens(self):
        with self.assertRaises(ValueError):
            v3.derive(SPEC, AUDIT, PROMPT + b"N1-B9-CLAUDE-002", KICKOFF, 9, "claude", 2, PROMPTS)
        with self.assertRaises(ValueError):
            v3.derive(SPEC, AUDIT, PROMPT.replace(b"N1-B9-CLAUDE-001", b"N1-B9-X"), KICKOFF, 9, "claude", 2, PROMPTS)
        with self.assertRaises(ValueError):
            v3.derive(SPEC, AUDIT, PROMPT, b"Read nothing.", 9, "claude", 2, PROMPTS)

    def test_original_inputs_unchanged(self):
        spec, audit = copy.deepcopy(SPEC), copy.deepcopy(AUDIT)
        v3.derive(spec, audit, PROMPT, KICKOFF, 9, "claude", 3, PROMPTS)
        self.assertEqual((spec, audit), (SPEC, AUDIT))


if __name__ == "__main__":
    unittest.main()
