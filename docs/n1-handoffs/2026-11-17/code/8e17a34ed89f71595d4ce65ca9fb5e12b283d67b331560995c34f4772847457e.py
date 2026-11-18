import contextlib
import io
import subprocess
import unittest
from unittest.mock import Mock, patch

import b127_lifecycle_process as module


class LifecycleProcessTests(unittest.TestCase):
    def setUp(self):
        self.guard = Mock()
        self.guard.finish.return_value = {"breach": None}
        self.cleanup = Mock()
        self.process = Mock(pid=123, returncode=1)
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
        self.stack.enter_context(patch.object(module, "frozen"))
        self.stack.enter_context(patch.object(module, "load_module", return_value=self.cleanup))
        self.stack.enter_context(patch.object(module, "start_guard", return_value=(self.guard, None)))
        self.popen = self.stack.enter_context(patch.object(module.subprocess, "Popen", return_value=self.process))

    def test_timeout_then_utf8_result_preserves_nonzero_exit(self):
        self.process.communicate.side_effect = [
            subprocess.TimeoutExpired("test", 0.1), ("\u5009".encode("utf-8"), b"diagnostic")]
        self.assertEqual(module.python("checker.py"), (1, "\u5009", "diagnostic"))
        self.assertEqual([call.kwargs["timeout"] for call in self.process.communicate.call_args_list], [0.1, 0.1])
        self.cleanup.stop_child.assert_called_once_with(self.process)
        self.guard.finish.assert_called_once()

    def test_extension_uses_bounded_git_adapter(self):
        self.process.communicate.return_value = (b"{}", b"")
        module.python(module.TOOLS / "prepare-chain.py", 127, "--run", "test")
        self.assertEqual(self.popen.call_args.args[0][2:5],
                         [str(module.TOOLS / "run_b127_tool.py"), str(module.TOOLS / "prepare-chain.py"), "127"])

    def test_start_failure_finishes_guard(self):
        self.popen.side_effect = OSError("start failed")
        with self.assertRaisesRegex(OSError, "start failed"):
            module.python("checker.py")
        self.cleanup.stop_child.assert_called_once_with(None)
        self.guard.finish.assert_called_once()

    def test_breach_and_cleanup_failure_preserve_original_error(self):
        error = MemoryError("RAM breach")
        self.guard.check.side_effect = error
        self.guard.finish.return_value = {"breach": "RAM breach"}
        self.cleanup.stop_child.side_effect = subprocess.TimeoutExpired("cleanup", 10)
        with self.assertRaises(MemoryError) as raised:
            module.python("checker.py")
        self.assertIs(raised.exception, error)
        self.assertIn("cleanup also failed", raised.exception.__notes__[0])
        self.guard.finish.assert_called_once()


if __name__ == "__main__":
    unittest.main()
