import copy
import datetime
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import confirm_b133 as module
from common import COORDINATOR, load_module

NOW = datetime.datetime(2026, 11, 17, 2, 0, tzinfo=datetime.timezone.utc)
CLAUDE = module.INITIALS["claude"]["session"]
GPT = module.INITIALS["gpt"]["session"]


def snapshot(reviewer=CLAUDE, **changes):
    rows = [{"id": COORDINATOR, "activity": {"status": "busy"}, "is_running": True},
            {"id": "11111111-1111-4111-8111-111111111111", "active_session_id": reviewer,
             "activity": {"status": "idle"}, "is_running": False},
            {"id": "22222222-2222-4222-8222-222222222222", "activity": {"status": "idle"},
             "is_running": False}]
    for index, change in changes.items():
        rows[int(index[1:])].update(change)
    return {"summary": {"total": len(rows)}, "sessions": rows}, [{"id": row["id"]} for row in rows]


def spec(**changes):
    value = {
        "family": "claude", "run": "N1-B133-CLAUDE-CONFIRM-001", "session": CLAUDE,
        "candidate": module.CANDIDATE, "teachingChange": False, "scope": ["\u7434"],
        "revisedSources": ["kanji/\u7434.md"], "additionalSources": [],
        "basis": "adjudicated-initial", "priorVerdict": "CLEAN",
        "basisText": "Synthetic B133 coordinator basis.",
    }
    value.update(changes)
    return value


class FakeGit:
    def __init__(self, head, dirty=b""):
        self.head, self.dirty = head, dirty

    def __call__(self, *args):
        return {"rev-parse": self.head.encode() + b"\n", "status": self.dirty}[args[0]]


class ConfirmB133Tests(unittest.TestCase):
    def test_snapshot_requires_every_other_session_explicitly_idle(self):
        status, roster = snapshot()
        self.assertEqual(module.check_snapshot(status, roster, CLAUDE, NOW, NOW), 3)
        for status, roster in (snapshot(r2={"activity": {"status": "busy"}}),
                               snapshot(r2={"is_running": None}),
                               snapshot(r1={"awaiting_user_input": {"question": "?"}}),
                               snapshot(r2={"awaiting_plan_approval": True})):
            with self.assertRaisesRegex(ValueError, "not idle"):
                module.check_snapshot(status, roster, CLAUDE, NOW, NOW)
        missing = copy.deepcopy(snapshot()[0])
        del missing["sessions"][2]["is_running"]
        with self.assertRaisesRegex(ValueError, "not idle"):
            module.check_snapshot(missing, snapshot()[1], CLAUDE, NOW, NOW)

    def test_snapshot_rejects_stale_future_mismatch_and_ambiguous_reviewer(self):
        status, roster = snapshot()
        for observed in (NOW - datetime.timedelta(seconds=120), NOW + datetime.timedelta(seconds=1),
                         NOW.replace(tzinfo=None)):
            with self.assertRaises((ValueError, TypeError)):
                module.check_snapshot(status, roster, CLAUDE, observed, NOW)
        with self.assertRaisesRegex(ValueError, "mismatched"):
            module.check_snapshot(status, roster[:-1], CLAUDE, NOW, NOW)
        with self.assertRaisesRegex(ValueError, "missing or ambiguous"):
            module.check_snapshot(status, roster, GPT, NOW, NOW)
        duplicate, roster = snapshot(r2={"id": CLAUDE})
        with self.assertRaisesRegex(ValueError, "missing or ambiguous"):
            module.check_snapshot(duplicate, roster, CLAUDE, NOW, NOW)

    def test_capacity_uses_live_tokens_chain_and_prompt(self):
        observed = {"status": "PASS", "family": "claude", "lastInputTokens": 551959}
        chain = {"segments": [{"bytes": 50000}, {"bytes": 40000}]}
        self.assertEqual(module.capacity(observed, chain, 8000)["projectedPeak"], 691959)
        for value, prompt in ((dict(observed, lastInputTokens=560000), 8000), (dict(observed, status="HOLD"), 8000),
                              (observed, module.PROMPT_LIMIT + 1), (observed, 0)):
            with self.assertRaises(ValueError):
                module.capacity(value, chain, prompt)

    def test_declared_change_must_match_actual_lineage(self):
        revision = "b" * 40
        with patch.object(module, "lineage", return_value=0):
            self.assertEqual(module.clean(FakeGit(module.CANDIDATE), module.CANDIDATE, False), 0)
            for git, candidate, change in ((FakeGit(module.CANDIDATE), module.CANDIDATE, True),
                                           (FakeGit(module.CANDIDATE, b" M kanji/x.md\n"), module.CANDIDATE, False),
                                           (FakeGit(revision), module.CANDIDATE, False)):
                with self.assertRaises(ValueError):
                    module.clean(git, candidate, change)
        with patch.object(module, "lineage", return_value=1):
            self.assertEqual(module.clean(FakeGit(revision), revision, True), 1)
            with self.assertRaises(ValueError):
                module.clean(FakeGit(revision), revision, False)

    def test_spec_validation(self):
        self.assertEqual(module.validate_spec(spec()), "claude")
        bad = (spec(session=GPT), spec(run="N1-B133-GPT-CONFIRM-001"), spec(candidate="b" * 40),
               spec(scope=["\u732b"]), spec(scope=[]), spec(revisedSources=["kanji/\u925b.md"]),
               spec(revisedSources=["kanji/\u7434.md", "../outside.md"]),
               spec(revisedSources=["kanji/\u7434.md", "C:/outside.md"]),
               spec(priorVerdict="UNVERIFIED"), spec(basisText=" "), spec(basisText="B132 wording"),
               spec(teachingChange=1),
               spec(additionalSources=[{"source": "claims.md", "path": "x", "sha256": "0" * 63}]),
               {**spec(), "extra": True})
        for value in bad:
            with self.assertRaises(ValueError):
                module.validate_spec(value)
        self.assertEqual(module.validate_spec(spec(candidate="b" * 40, teachingChange=True)), "claude")

    def test_actual_initial_bindings_include_coordinator_claims(self):
        refs, report, ids = module.initial("claude", CLAUDE)
        self.assertTrue(report and "report" in refs)
        self.assertEqual(ids[-3:], ["C1", "C2", "C3"])
        refs, report, ids = module.initial("gpt", GPT)
        self.assertEqual(ids[-7:], ["Q1", "Q2", "Q3", "Q4", "C4", "C5", "C6"])
        with self.assertRaisesRegex(ValueError, "original reviewer"):
            module.initial("gpt", CLAUDE)

    def test_renderer_uses_exact_basis_and_b133_contract(self):
        value = {**spec(basisText="Exact B133 basis.\nSecond line.\n"), "dispositionIds": ["O1", "C1"]}
        text = module.render(value, {"path": "own-report.md"}, {"segments": [{"path": "first.txt"}]},
                             Path("prompt.txt"), Path("report.md"), ["O1", "C1"]).decode("utf-8")
        self.assertEqual(text.count("Exact B133 basis.\nSecond line.\n"), 1)
        self.assertNotIn("B132", text)
        self.assertNotIn("held for open claims", text)
        self.assertIn("# B133 confirmation \u2014 N1-B133-CLAUDE-CONFIRM-001", text)
        self.assertIn("- C1 - <disposition>", text)
        self.assertIn("Scoped cards: \u7434", text)

    def test_checker_parses_coordinator_claim_dispositions(self):
        checker = load_module("b133_confirm_checker_test", module.OUT / "check-confirm-structure.py")
        report = f"""# B133 confirmation \u2014 N1-B133-GPT-CONFIRM-001

## Snapshot
Commit: {module.CANDIDATE}
Model: synthetic

## Scope
Chain: 1
Fetches: 0

## Dispositions
- Q1 - RESOLVED - Synthetic decision.
- C4 - DISPUTE ACCEPTED - Synthetic decision.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: Synthetic fixture, not review evidence.

## Findings
None.

## Optional
None.

## Limits
- L1: Synthetic fixture.
"""
        args = ("N1-B133-GPT-CONFIRM-001", module.CANDIDATE, ["Q1", "C4"], {"sources": []}, "CONFIRMED")
        self.assertEqual(checker.check(report, *args)["status"], "PASS")
        for broken in (report.replace("- C4 - DISPUTE ACCEPTED - Synthetic decision.\n", ""),
                       report.replace("C4 - DISPUTE ACCEPTED", "C4 - NOT RESOLVED"),
                       report.replace("B133 confirmation", "B132 confirmation")):
            self.assertEqual(checker.check(broken, *args)["status"], "FAIL")

    def test_bindings_are_unique_and_conflicts_fail(self):
        rows = []
        module.add_binding(rows, {"path": "a", "sha256": "1" * 64, "bytes": 3})
        module.add_binding(rows, {"path": "a", "sha256": "1" * 64})
        self.assertEqual(rows, [{"path": "a", "sha256": "1" * 64}])
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            module.add_binding(rows, {"path": "a", "sha256": "2" * 64})

    def test_admission_requires_actual_app_outputs(self):
        stamp, observed = module.observed_at(["1794871492638-copilot-tool-output-8d17.txt",
                                              "1794871492637-copilot-tool-output-6d7c.txt"])
        self.assertEqual(stamp, 1794871492637)
        self.assertEqual(observed.tzinfo, datetime.timezone.utc)
        with self.assertRaisesRegex(ValueError, "app-saved"):
            module.observed_at(["status.json"])

    def test_destination_is_fresh_report_under_reports_133(self):
        with tempfile.TemporaryDirectory() as root:
            reports = Path(root) / "reports-133"
            with patch.object(module, "REPORTS", reports):
                module.destination(reports / "N1-B133-CLAUDE-CONFIRM-001.md")
                self.assertEqual(list(reports.iterdir()), [])
                (reports / "existing.md").write_bytes(b"x")
                for path in (reports / "existing.md", Path(root) / "other.md", reports / "report.txt"):
                    with self.assertRaises(ValueError):
                        module.destination(path)

    def test_build_rejects_substituted_reviewer_before_writing(self):
        raw = json.dumps(spec(session=GPT)).encode()
        with patch.object(module, "frozen", return_value=raw), \
                patch.object(module, "write_frozen", side_effect=AssertionError("wrote")):
            with self.assertRaisesRegex(ValueError, "original reviewer"):
                module.build(Path("synthetic.json"))


if __name__ == "__main__":
    unittest.main()
