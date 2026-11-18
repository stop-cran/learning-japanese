import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import common
import run_b127_tool as runner
import verify_b127_sources as sources

COMPACT_DIGEST = "fd011d9d281180c1349f1d6ae13b3ef44733ba8ed092cd8057baa05184f6b5ef"


class CompactConfirmationTests(unittest.TestCase):
    def test_confirmation_engine_selects_compact_packet_with_bounded_git_and_shared_guard(self):
        path = common.TOOLS / "confirm_b130_compact.py"
        config = common.load_batch(130)
        guard = Mock()

        def execute(tool, run_name):
            self.assertEqual(Path(tool), path)
            module = common.load_module("b130_compact_confirmation_routing_test", path)
            self.assertEqual(module.git(config, "merge-base", "--is-ancestor", "base", "head"), b"bounded")
            self.assertEqual(module.start_guard("confirmation"), (guard, None))
            self.assertIs(sources.ACTIVE_GUARD, guard)
            packet, sums, digest = module.verify_packet(config)
            self.assertEqual(packet.name, "batch-130-ce1b5c89-compact-001")
            self.assertEqual(digest, COMPACT_DIGEST)
            self.assertTrue(sums)

        with patch.object(sys, "argv", ["run_b127_tool.py", str(path)]), \
                patch.object(common, "git"), \
                patch.object(common, "start_guard", return_value=(guard, None)), \
                patch.object(sources, "git", return_value=b"bounded") as bounded_git, \
                patch.object(runner.runpy, "run_path", side_effect=execute), \
                patch("subprocess.check_output", side_effect=AssertionError("Unbounded Git path")), \
                contextlib.redirect_stdout(io.StringIO()):
            runner.main()
            bounded_git.assert_called_once_with(
                "merge-base", "--is-ancestor", "base", "head", repo=Path(config["repo"]))
            self.assertIsNone(sources.ACTIVE_GUARD)


if __name__ == "__main__":
    unittest.main()
