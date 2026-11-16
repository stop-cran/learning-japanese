import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import common
import run_b127_tool as runner
import verify_b127_sources as sources
from b130_excluded_initials_v2 import archive_excluded as archive_v2
from b130_excluded_initials_v3 import archive_excluded, require_mismatch_hold

ROOT = common.WS / "scratch-130" / "review"
V4 = common.TOOLS / "close_b130_compact_v4.py"


class Attempt004ClosureTests(unittest.TestCase):
    def fixture(self):
        held = json.loads(common.frozen(ROOT / "N1-B130-CLAUDE-003-hold.json"))
        read = lambda key: json.loads(common.frozen(held[key]["path"], held[key]["sha256"]))
        parts = [read(key) for key in ("phase1", "final", "audit", "context", "structure")]
        events = common.frozen(held["events"]["path"], held["events"]["sha256"])
        phase2 = common.frozen(held["phase2Message"]["path"]).decode("utf-8")
        return held, parts, events, phase2

    def test_actual_mismatch_run_is_preservable_only_as_excluded(self):
        held, parts, events, phase2 = self.fixture()
        require_mismatch_hold(held, *parts, events, phase2, 130, held["candidate"])
        for field in ("reviewAccepted", "finalAcceptance"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_mismatch_hold({**held, field: True}, *parts, events, phase2, 130, held["candidate"])
        delivered = phase2.split("\n")[0]
        with self.assertRaises(ValueError):
            require_mismatch_hold(held, *parts, events, delivered, 130, held["candidate"])
        for field, value in (("eventIndex", 10), ("sha256", "0" * 64), ("missingSuffix", "")):
            with self.subTest(delivered=field), self.assertRaises(ValueError):
                require_mismatch_hold({**held, "deliveredPhase2": {**held["deliveredPhase2"], field: value}},
                                      *parts, events, phase2, 130, held["candidate"])
        status = {**parts[1], "status": "MECHANICAL_PASS"}
        with self.assertRaises(ValueError):
            require_mismatch_hold(held, parts[0], status, *parts[2:], events, phase2, 130, held["candidate"])

    def test_all_three_real_excluded_initials_archive_without_acceptance(self):
        held, *_ = self.fixture()
        paths = [ROOT / f"N1-B130-CLAUDE-00{n}-hold.json" for n in (1, 2, 3)]
        copied, bound, dumped = Mock(), Mock(), Mock()
        chained = Mock(return_value={"segments": 1})
        support = Mock()
        support.bounded_audit.return_value = {"status": "VOID"}
        args = (130, held["candidate"], set(), copied, bound, dumped, chained, support, ROOT)
        result = archive_excluded(paths, *args)
        self.assertEqual([r["status"] for r in result], ["HOLD_CONTEXT_COMPACTED", "VOID_PREMATURE_SELECTION",
                                                         "VOID_COORDINATOR_PHASE2_MESSAGE_MISMATCH"])
        self.assertFalse(any(r["reviewAccepted"] or r["finalAcceptance"] for r in result))
        names = [call.args[1] for call in bound.call_args_list]
        self.assertIn("excluded-initials/N1-B130-CLAUDE-003/report.md", names)
        self.assertIn("excluded-initials/N1-B130-CLAUDE-003/phase2-message.txt", names)
        with self.assertRaisesRegex(ValueError, "accepted or duplicated"):
            archive_excluded(paths[2:], 130, held["candidate"], {"N1-B130-CLAUDE-003"},
                             copied, bound, dumped, chained, support, ROOT)
        with self.assertRaisesRegex(ValueError, "accepted or duplicated"):
            archive_excluded([paths[2], paths[2]], *args)
        with self.assertRaises((ValueError, KeyError)):
            archive_v2(paths[2:], *args)

    def test_v4_keeps_bounded_routing_and_rejects_bad_additional_tools(self):
        config = common.load_batch(130)
        guard = Mock()

        def execute(tool, run_name):
            module = common.load_module("b130_attempt004_closure_routing_test", Path(tool))
            self.assertEqual(module.git(config, "merge-base", "--is-ancestor", "base", "head"), b"bounded")
            self.assertEqual(module.start_guard("closure"), (guard, None))
            packet, _, digest = module.verify_packet(config)
            self.assertEqual(packet.name, "batch-130-ce1b5c89-compact-001")
            self.assertEqual(digest, "fd011d9d281180c1349f1d6ae13b3ef44733ba8ed092cd8057baa05184f6b5ef")
            self.assertIs(module.archive_excluded, archive_excluded)
            for bad in (("a.py", "a.py"), ("close_b130_compact_v4.py",), ("x\\y.py",), ("notes.txt",)):
                with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "Additional tools"):
                    module.archive(130, "0" * 40, ("a", "b"), preflight_path=Path("x"), additional_tools=bad)

        with patch.object(sys, "argv", ["run_b127_tool.py", str(V4)]), \
                patch.object(common, "git"), \
                patch.object(common, "start_guard", return_value=(guard, None)), \
                patch.object(sources, "git", return_value=b"bounded"), \
                patch.object(runner.runpy, "run_path", side_effect=execute), \
                patch("subprocess.check_output", side_effect=AssertionError("Unbounded Git path")), \
                contextlib.redirect_stdout(io.StringIO()):
            runner.main()


if __name__ == "__main__":
    unittest.main()
