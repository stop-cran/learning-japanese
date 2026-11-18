"""Fabricated-only fixtures for check-report-structure.py (report-structure-v1).

No real review report, transcript, list or finding is used: cards, sources, lists and reports are
synthetic placeholders.
"""
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("check_report_structure", HERE / "check-report-structure.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)
from review_chain import validate_selection  # noqa: E402

RUN = "N1-FAKE-RUN-001"
REFERENCE = {"newCards": ["甲", "乙"], "otherRequiredCards": ["丙"],
             "cards": [{"card": "甲", "distractors": ["丁"], "quiz_exclusions": ["戊"]},
                       {"card": "乙", "distractors": ["己"], "quiz_exclusions": ["庚"]}]}
CORE = {"sources": [{"source": "REVIEW.md", "selectedLines": 60},
                    {"source": "snapshot/kanji/甲.md", "selectedLines": 70},
                    {"source": "snapshot/kanji/乙.md", "selectedLines": 70}]}
EXTENSION = {"sources": [{"source": "repo/kanji/辛.md [D1]", "selectedLines": 40},
                         {"source": "repo/kanji/戊.md [E1]", "selectedLines": 30}]}
LIST = "D1 辛 - 甲: fabricated overlap\nE1 戊 - 甲: fabricated exclusion check"
NONE_MISSING = "C:\\fake\\chain\\01-x.txt\nMissing entries: none"
D1_MISSING = "C:\\fake\\chain\\01-x.txt\nMissing entries:\nD1 辛 - 甲: fabricated overlap"

FINDING = """### F1: fabricated defect
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: snapshot/kanji/甲.md:12; repo/kanji/辛.md:3-5
- Evidence: placeholder evidence
  continued on an indented line
- Required change: placeholder change
"""
OPTIONAL = """### O1: fabricated polish
- Facet: Comprehensibility
- Severity: optional
- Confidence: low
- Citations: REVIEW.md:10
- Evidence: placeholder evidence
- Suggestion: placeholder suggestion
"""


def report(overall="NEEDS FIX", facets=("CLEAN", "CLEAN", "NEEDS FIX", "CLEAN"),
           cells=None, findings=FINDING, optional=OPTIONAL, de_rows=None, lists=None,
           limits="- L1: placeholder limit\n- L2: another placeholder limit\n", title=RUN, extra=""):
    names = checker.FACETS
    cells = cells or {"甲": ("CLEAN", "CLEAN", "NEEDS FIX", "CLEAN"), "乙": ("CLEAN",) * 4}
    if de_rows is None:
        de_rows = ("| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |\n"
                   "| --- | --- | --- | --- | --- | --- |\n"
                   "| D1 | 辛 | placeholder | 甲 | placeholder | placeholder |\n"
                   "| E1 | 戊 | placeholder | 甲 | placeholder | placeholder |\n")
    lists = lists or "D: D1 辛\nE: E1 戊\nMissing entries: none\n"
    facet_text = "".join(f"### {n}\nVerdict: {v}\nBasis: placeholder basis\n\n" for n, v in zip(names, facets))
    card_rows = "".join(f"| {c} | {' | '.join(v)} | placeholder |\n" for c, v in cells.items())
    return (f"# B115 initial review — {title}\n\n## Overall verdict\nVerdict: {overall}\n\n"
            f"## Facet verdicts\n{facet_text}## Segments read\nCore chain: 01-02\nExtension chain: 01\n\n"
            f"## Phase-1 D/E lists\n{lists}\n## D/E cards read\n{de_rows}\n"
            "## Per-card results\n| Card | Correctness | Scoped coverage | Consistency/quiz safety | "
            f"Comprehensibility | Evidence |\n| --- | --- | --- | --- | --- | --- |\n{card_rows}\n"
            f"## Findings\n{findings}\n## Optional points\n{optional}\n{extra}## Limits\n{limits}")


def run(text, completion="NEEDS FIX", list_text=LIST, phase2=NONE_MISSING):
    phase1 = validate_selection(list_text, REFERENCE)
    assert phase1["valid"], phase1
    return checker.check(text, RUN, CORE, EXTENSION, REFERENCE, phase1, phase2, completion)


class Passing(unittest.TestCase):
    def assertPass(self, result):
        self.assertEqual(result["status"], "PASS", result["errors"])

    def test_needs_fix_with_finding_and_optional_point(self):
        result = run(report(), "NEEDS FIX\n")
        self.assertPass(result)
        self.assertEqual((result["findings"], result["optionalPoints"], result["limits"]), (1, 1, 2))

    def test_clean_with_no_items(self):
        self.assertPass(run(report("CLEAN", ("CLEAN",) * 4, {"甲": ("CLEAN",) * 4, "乙": ("CLEAN",) * 4},
                                   "None.\n", "None.\n"), "CLEAN\r\n"))

    def test_unverified_facet_and_cell(self):
        self.assertPass(run(report("UNVERIFIED", ("UNVERIFIED", "CLEAN", "CLEAN", "CLEAN"),
                                   {"甲": ("UNVERIFIED", "CLEAN", "CLEAN", "CLEAN"), "乙": ("CLEAN",) * 4},
                                   "None.\n"), "UNVERIFIED"))

    def test_missing_entry_is_listed_and_not_tabulated(self):
        rows = ("| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |\n"
                "| --- | --- | --- | --- | --- | --- |\n| E1 | 戊 | placeholder | 甲 | placeholder | placeholder |\n")
        text = report(de_rows=rows, lists="D: D1 辛\nE: E1 戊\nMissing entries: D1\n",
                      findings=FINDING.replace("; repo/kanji/辛.md:3-5", ""))
        self.assertPass(run(text, phase2=D1_MISSING))

    def test_markup_backticks_and_crlf_tolerated(self):
        text = (report().replace("Verdict: NEEDS FIX", "Verdict: **NEEDS FIX**")
                .replace("- Facet:", "- **Facet:**")
                .replace("snapshot/kanji/甲.md:12", "`snapshot/kanji/甲.md:12`").replace("\n", "\r\n"))
        self.assertPass(run(text))

    def test_empty_lists_and_none_read(self):
        text = report(de_rows="None read.\n", lists="D: none\nE: none\nMissing entries: none\n",
                      findings=FINDING.replace("; repo/kanji/辛.md:3-5", ""))
        self.assertPass(run(text, list_text="D: none\nE: none"))

    def test_cli_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            files = {"report": report(), "core-manifest": json.dumps(CORE), "extension": json.dumps(EXTENSION),
                     "reference": json.dumps(REFERENCE), "phase1-list": LIST, "phase2-message": NONE_MISSING,
                     "audit": json.dumps({"messages": [LIST, "NEEDS FIX"]})}
            argv = ["--run", RUN]
            for name, content in files.items():
                (tmp / name).write_bytes(content.encode("utf-8"))
                argv += ["--" + name, str(tmp / name)]
            with redirect_stdout(io.StringIO()) as out:
                self.assertEqual(checker.main(argv), 0)
            self.assertEqual(json.loads(out.getvalue())["status"], "PASS")
            (tmp / "audit").write_text(json.dumps({"messages": ["NEEDS FIX"]}), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(checker.main(argv), 1)
            (tmp / "report").unlink()
            with redirect_stdout(io.StringIO()):
                self.assertEqual(checker.main(argv), 1)


class Failing(unittest.TestCase):
    def assertFails(self, result, fragment):
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(fragment in e for e in result["errors"]), result["errors"])

    def test_missing_facet_section(self):
        text = report().replace("### Comprehensibility\nVerdict: CLEAN\nBasis: placeholder basis\n\n", "")
        self.assertFails(run(text), "level-3 headings must be exactly")

    def test_facet_order(self):
        text = report().replace("### Correctness", "### TMP").replace("### Scoped coverage", "### Correctness")
        self.assertFails(run(text.replace("### TMP", "### Scoped coverage")), "level-3 headings must be exactly")

    def test_invalid_facet_verdict(self):
        self.assertFails(run(report(facets=("PASS", "CLEAN", "NEEDS FIX", "CLEAN"))), "is not CLEAN")

    def test_empty_basis(self):
        self.assertFails(run(report().replace("Basis: placeholder basis", "Basis:", 1)), "'Basis:' is empty")

    def test_overall_not_derived_from_facets(self):
        self.assertFails(run(report(overall="UNVERIFIED"), "UNVERIFIED"), "does not follow")

    def test_completion_differs_from_overall(self):
        self.assertFails(run(report(), "CLEAN"), "differs from the overall verdict")

    def test_completion_not_exact(self):
        self.assertFails(run(report(), "NEEDS FIX: see report"), "not an exact verdict")
        self.assertFails(run(report(), None), "not an exact verdict")

    def test_finding_without_citation(self):
        text = report(findings=FINDING.replace("- Citations: snapshot/kanji/甲.md:12; repo/kanji/辛.md:3-5\n", ""))
        self.assertFails(run(text), "missing or empty field Citations")

    def test_citation_without_line(self):
        self.assertFails(run(report(optional=OPTIONAL.replace("REVIEW.md:10", "REVIEW.md"))), "is not <source>:<line>")

    def test_citation_outside_chains(self):
        self.assertFails(run(report(optional=OPTIONAL.replace("REVIEW.md:10", "reports/other.md:1"))),
                         "not in the reviewer's chains")

    def test_citation_line_out_of_range(self):
        self.assertFails(run(report(optional=OPTIONAL.replace("REVIEW.md:10", "REVIEW.md:59-61"))),
                         "outside source lines")

    def test_missing_severity_and_confidence(self):
        text = report(findings=FINDING.replace("- Severity: medium\n", "").replace("- Confidence: high\n", ""))
        result = run(text)
        self.assertFails(result, "missing or empty field Severity")
        self.assertFails(result, "missing or empty field Confidence")

    def test_invalid_severity_and_confidence(self):
        text = report(findings=FINDING.replace("Severity: medium", "Severity: critical")
                      .replace("Confidence: high", "Confidence: certain"))
        result = run(text)
        self.assertFails(result, "severity 'critical'")
        self.assertFails(result, "confidence 'certain'")

    def test_optional_point_severity_must_be_optional(self):
        self.assertFails(run(report(optional=OPTIONAL.replace("Severity: optional", "Severity: low"))),
                         "must be optional")

    def test_finding_numbering_gap(self):
        self.assertFails(run(report(findings=FINDING.replace("### F1:", "### F2:"))), "must be 'F1:")

    def test_extra_top_level_bullet_in_item(self):
        self.assertFails(run(report(findings=FINDING + "- Note: extra\n")), "unexpected top-level line")

    def test_needs_fix_facet_without_finding(self):
        self.assertFails(run(report(findings="None.\n")), "no F item names it")

    def test_finding_names_clean_facet(self):
        text = report(findings=FINDING.replace("Facet: Consistency/quiz safety", "Facet: Correctness"))
        self.assertFails(run(text), "An F item names Correctness")

    def test_findings_section_free_text(self):
        self.assertFails(run(report(findings="Some prose instead of items.\n")), "write either the single line")

    def test_per_card_missing_card(self):
        self.assertFails(run(report(cells={"甲": ("CLEAN", "CLEAN", "NEEDS FIX", "CLEAN")})),
                         "exactly one row for each new card")

    def test_per_card_cell_inconsistent_with_facet(self):
        cells = {"甲": ("NEEDS FIX", "CLEAN", "NEEDS FIX", "CLEAN"), "乙": ("CLEAN",) * 4}
        self.assertFails(run(report(cells=cells)), "is NEEDS FIX for Correctness")
        cells = {"甲": ("CLEAN", "UNVERIFIED", "NEEDS FIX", "CLEAN"), "乙": ("CLEAN",) * 4}
        self.assertFails(run(report(cells=cells)), "is UNVERIFIED for Scoped coverage")

    def test_de_table_missing_or_reordered_row(self):
        rows = ("| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |\n"
                "| --- | --- | --- | --- | --- | --- |\n| E1 | 戊 | placeholder | 甲 | placeholder | placeholder |\n"
                "| D1 | 辛 | placeholder | 甲 | placeholder | placeholder |\n")
        self.assertFails(run(report(de_rows=rows)), "in phase-1 order")
        self.assertFails(run(report(de_rows="None read.\n")), "table row is required")

    def test_de_table_wrong_header(self):
        rows = "| ID | Character | Disposition |\n| --- | --- | --- |\n| D1 | 辛 | x |\n"
        self.assertFails(run(report(de_rows=rows)), "table header must be")

    def test_extra_level_two_heading(self):
        self.assertFails(run(report(extra="## Notes\nplaceholder\n\n")), "Level-2 headings must be exactly")

    def test_missing_limits(self):
        self.assertFails(run(report(limits="Nothing.\n")), "Limits:")

    def test_wrong_title(self):
        self.assertFails(run(report(title="N1-OTHER-RUN")), "Line 1 must be")

    def test_phase1_list_line_missing_id(self):
        self.assertFails(run(report(lists="D: none\nE: E1 戊\nMissing entries: none\n")),
                         "D line must list each sent D ID once")

    def test_missing_entries_mismatch(self):
        self.assertFails(run(report(), phase2=D1_MISSING), "Missing entries must name exactly")


if __name__ == "__main__":
    unittest.main(verbosity=2)
