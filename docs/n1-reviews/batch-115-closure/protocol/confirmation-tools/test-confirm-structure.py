"""Synthetic fixtures for check-confirm-structure.py. No session, IPC or delivery probe."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("check_confirm_structure", HERE / "check-confirm-structure.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

RUN = "N1-B115-TEST-CONFIRM-001"
COMMIT = "206f9893"
IDS = ["F1", "O1", "O2"]
CHAIN = {"sources": [{"source": "confirm-packet/CHANGES.md", "selectedLines": 40},
                     {"source": "original-packet/snapshot/kanji/x.md", "selectedLines": 30},
                     {"source": "initial-report/report.md", "selectedLines": 100}]}

CONFIRMED = """# B115 confirmation \u2014 N1-B115-TEST-CONFIRM-001

## Snapshot
Commit: 206f9893 (revised snapshot)
Model: fixture model; identity unverified

## Scope
Chain: segments 1-3 read in order
Fetches: none
All changed cards were read in full.

## Dispositions
- F1 - RESOLVED - the revised line fixes it
- O1 - DECLINE ACCEPTED - the stated reason holds
  continuation detail
- O2 - DISPUTE ACCEPTED - mis-attributed

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN - all eight cards
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: every item is accepted and no new defect was established

## Findings
None.

## Optional
None.

## Limits
- L1: Public sources were not fetched.
"""

FINDING = """### F1: Wrong gloss
- Facet: Correctness
- Severity: minor
- Confidence: high
- Citations: confirm-packet/CHANGES.md:3-4; original-packet/snapshot/kanji/x.md:2
- Evidence: the cited lines disagree
- Required change: correct the gloss
"""

OPTIONAL = """### O1: Shorter wording
- Facet: Comprehensibility
- Severity: optional
- Confidence: medium
- Citations: initial-report/report.md:10
- Evidence: long sentence
- Suggestion: shorten it
"""


def needs_fix():
    return (CONFIRMED.replace("Correctness: CLEAN", "Correctness: NEEDS FIX - x")
            .replace("Verdict: CONFIRMED", "Verdict: NEEDS FIX")
            .replace("## Findings\nNone.", "## Findings\n" + FINDING))


class CheckConfirmStructureTest(unittest.TestCase):
    def check(self, text, completion="CONFIRMED", ids=IDS):
        return module.check(text, RUN, COMMIT, ids, CHAIN, completion)

    def assertPass(self, result):
        self.assertEqual(result["status"], "PASS", result["errors"])

    def assertFail(self, result, fragment):
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(fragment in e for e in result["errors"]), result["errors"])

    def test_valid_reports_pass(self):
        self.assertPass(self.check(CONFIRMED))
        self.assertPass(self.check(CONFIRMED, "CONFIRMED\r\n"))
        self.assertPass(self.check(needs_fix().replace("## Optional\nNone.", "## Optional\n" + OPTIONAL),
                                   "NEEDS FIX\n"))
        unverified = (CONFIRMED.replace("O1 - DECLINE ACCEPTED", "O1 - DECLINE REJECTED")
                      .replace("Correctness: CLEAN", "Correctness: UNVERIFIED")
                      .replace("Verdict: CONFIRMED", "Verdict: UNVERIFIED").replace("Basis: every", "Basis: some"))
        self.assertPass(self.check(unverified, "UNVERIFIED"))
        self.assertPass(self.check(unverified.replace("Verdict: UNVERIFIED", "Verdict: NEEDS FIX"), "NEEDS FIX"))

    def test_markup_dashes_aliases_and_none_limits_pass(self):
        text = (CONFIRMED.replace("- F1 - RESOLVED - ", "- **F1** \u2014 RESOLVED \u2014 ")
                .replace("Consistency and quiz safety:", "Consistency/quiz safety:")
                .replace("- L1: Public sources were not fetched.", "None.")
                .replace("Basis: every item is accepted and no new defect was established\n", ""))
        self.assertPass(self.check(text))
        cited = needs_fix().replace("confirm-packet/CHANGES.md:3-4;",
                                    "confirm-packet\\CHANGES.md:3-4, 7, 9-10;")
        self.assertPass(self.check(cited, "NEEDS FIX"))

    def test_skeleton_errors(self):
        self.assertFail(self.check(CONFIRMED.replace(RUN, "OTHER")), "Line 1")
        self.assertFail(self.check(CONFIRMED.replace("## Optional\nNone.\n\n", "")), "Level-2 headings")
        swapped = CONFIRMED.replace("## Findings", "## TMP").replace("## Optional", "## Findings").replace(
            "## TMP", "## Optional")
        self.assertFail(self.check(swapped), "Level-2 headings")
        self.assertFail(self.check(CONFIRMED.replace("Fetches: none\n", "Fetches: none\n### Extra\n")),
                        "level-3 headings are not allowed")
        self.assertFail(self.check(CONFIRMED.replace("206f9893 (revised", "f36cd819 (old")), "Commit must name")
        self.assertFail(self.check(CONFIRMED.replace("Fetches: none\n", "")), "'Fetches:'")
        self.assertFail(self.check(CONFIRMED.replace("Basis: every", "Basis: one\nBasis: two")), "Basis")
        self.assertFail(self.check(CONFIRMED.replace("Verdict: CONFIRMED", "Verdict: CONFIRMED\nNote: x")),
                        "unexpected top-level line")

    def test_disposition_errors(self):
        self.assertFail(self.check(CONFIRMED, ids=IDS + ["O3"]), "exactly one line")
        self.assertFail(self.check(CONFIRMED.replace("- O2 - DISPUTE ACCEPTED - mis-attributed\n", "")),
                        "exactly one line")
        self.assertFail(self.check(CONFIRMED.replace("O2 - DISPUTE", "O1 - DISPUTE")), "more than once")
        self.assertFail(self.check(CONFIRMED.replace("RESOLVED - the", "FIXED - the")), "is not '- <ID>")
        self.assertFail(self.check(CONFIRMED.replace("O1 - DECLINE ACCEPTED - the stated reason holds",
                                                     "O1 - DECLINE ACCEPTED -")), "is not '- <ID>")
        self.assertFail(self.check(CONFIRMED.replace("  continuation detail", "continuation detail")),
                        "is not '- <ID>")
        self.assertFail(self.check(CONFIRMED.replace("- O2 - DISPUTE ACCEPTED - mis-attributed",
                                                     "- O2 - DISPUTE ACCEPTED - x\n- L1 - RESOLVED - y")),
                        "is not '- <ID>")

    def test_verdict_and_consistency_errors(self):
        self.assertFail(self.check(CONFIRMED.replace("Comprehensibility: CLEAN\n", "")), "exactly one line")
        self.assertFail(self.check(CONFIRMED.replace("Comprehensibility: CLEAN", "Comprehensibility: OK")),
                        "is not '<facet>")
        self.assertFail(self.check(CONFIRMED.replace("Comprehensibility: CLEAN", "Clarity: CLEAN")),
                        "is not '<facet>")
        self.assertFail(self.check(CONFIRMED.replace("Verdict: CONFIRMED", "Verdict: CLEAN")), "is not CONFIRMED")
        self.assertFail(self.check(CONFIRMED.replace("F1 - RESOLVED", "F1 - PARTIALLY RESOLVED")),
                        "CONFIRMED requires")
        self.assertFail(self.check(needs_fix().replace("Verdict: NEEDS FIX", "Verdict: CONFIRMED")),
                        "CONFIRMED requires")
        self.assertFail(self.check(CONFIRMED.replace("Verdict: CONFIRMED", "Verdict: NEEDS FIX"), "NEEDS FIX"),
                        "NEEDS FIX requires")
        self.assertFail(self.check(needs_fix().replace("Verdict: NEEDS FIX", "Verdict: UNVERIFIED"), "UNVERIFIED"),
                        "UNVERIFIED is not allowed")
        self.assertFail(self.check(needs_fix().replace("- Facet: Correctness", "- Facet: Comprehensibility"),
                                   "NEEDS FIX"), "not NEEDS FIX")
        self.assertFail(self.check(CONFIRMED.replace("Correctness: CLEAN", "Correctness: NEEDS FIX")
                                   .replace("Verdict: CONFIRMED", "Verdict: NEEDS FIX"), "NEEDS FIX"),
                        "without any F item")

    def test_item_errors(self):
        base = needs_fix()
        cases = {
            "F2: Wrong gloss": ("### F1: Wrong gloss", "### F2: Wrong gloss"),
            "missing or empty field Evidence": ("- Evidence: the cited lines disagree\n", ""),
            "severity": ("- Severity: minor", "- Severity: low"),
            "confidence": ("- Confidence: high", "- Confidence: sure"),
            "facet 'Accuracy'": ("- Facet: Correctness", "- Facet: Accuracy"),
            "unexpected top-level line": ("- Required change: correct the gloss",
                                          "- Required change: correct the gloss\nextra line"),
            "outside source lines": ("CHANGES.md:3-4", "CHANGES.md:39-41"),
            "not in the reviewer's chain": ("original-packet/snapshot/kanji/x.md:2", "repo/kanji/x.md:2"),
            "is not <source>:<line>": ("x.md:2", "x.md:two"),
        }
        for fragment, (old, new) in cases.items():
            with self.subTest(fragment=fragment):
                self.assertIn(old, base)
                self.assertFail(self.check(base.replace(old, new, 1), "NEEDS FIX"), fragment)
        self.assertFail(self.check(base.replace("## Optional\nNone.", "## Optional\n"
                                                + OPTIONAL.replace("optional\n", "minor\n")), "NEEDS FIX"),
                        "severity")
        self.assertFail(self.check(CONFIRMED.replace("## Findings\nNone.", "## Findings\nNothing.")), "None.")

    def test_limits_errors(self):
        self.assertFail(self.check(CONFIRMED.replace("- L1:", "- L2:")), "expected '- L1")
        self.assertFail(self.check(CONFIRMED.replace("- L1: Public sources were not fetched.", "")), "'None.'")

    def test_completion_message(self):
        for completion in (None, "NEEDS FIX", "CONFIRMED ", "CONFIRMED\n\n", "Confirmation: CONFIRMED"):
            with self.subTest(completion=completion):
                self.assertEqual(self.check(CONFIRMED, completion)["status"], "FAIL")

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            report, chain, audit = tmp / "r.md", tmp / "chain.json", tmp / "audit.json"
            report.write_bytes(CONFIRMED.encode("utf-8"))
            chain.write_text(json.dumps(CHAIN), encoding="utf-8")
            argv = ["--report", str(report), "--chain-manifest", str(chain), "--audit", str(audit), "--run", RUN,
                    "--commit", COMMIT, "--ids", ",".join(IDS)]
            audit.write_text(json.dumps({"messages": ["CONFIRMED\n"]}), encoding="utf-8")
            self.assertEqual(module.main(argv), 0)
            audit.write_text(json.dumps({"messages": ["CONFIRMED", "CONFIRMED"]}), encoding="utf-8")
            self.assertEqual(module.main(argv), 1)
            audit.write_text(json.dumps({"messages": ["CONFIRMED"]}), encoding="utf-8")
            report.unlink()
            self.assertEqual(module.main(argv), 1)


if __name__ == "__main__":
    unittest.main()
