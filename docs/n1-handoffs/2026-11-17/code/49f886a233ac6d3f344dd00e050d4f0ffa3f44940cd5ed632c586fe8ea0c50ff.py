import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "guarded_test_v3", Path(__file__).with_name("guarded-test-v3.py"))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class Guard:
    def __init__(self, breach=False):
        self.breach = breach
        self.problem = None
        self.finished = False

    def start(self):
        pass

    def check(self):
        if self.breach:
            self.problem = "Synthetic memory breach"
            raise MemoryError(self.problem)

    def finish(self):
        self.finished = True
        return {"breach": self.problem}


class ResistantChild:
    args = ["synthetic-child"]
    pid = 123

    def __init__(self, exits_on_kill=True):
        self.now = 0
        self.waits = []
        self.returncode = None
        self.terminated = 0
        self.killed = 0
        self.exits_on_kill = exits_on_kill

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        if timeout is None or not 0 < timeout <= 0.1:
            raise AssertionError(f"Unbounded subprocess wait: {timeout}")
        self.waits.append(timeout)
        if self.returncode is not None:
            return self.returncode
        self.now += timeout
        raise subprocess.TimeoutExpired(self.args, timeout)

    def terminate(self):
        self.terminated += 1

    def kill(self):
        self.killed += 1
        if self.exits_on_kill:
            self.returncode = -9


class GuardedCommandTests(unittest.TestCase):
    def run_child(self, output, code, guard):
        with contextlib.redirect_stdout(io.StringIO()):
            return runner.run_command(
                [sys.executable, "-B", "-c", code], output, output, os.environ, guard)

    def test_stops_live_child_before_normal_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            guard = Guard(breach=True)
            code = ("import time; from pathlib import Path; time.sleep(2); "
                    "Path('completed.txt').write_text('unexpected normal completion')")
            with self.assertRaisesRegex(MemoryError, "Synthetic"):
                self.run_child(output, code, guard)
            receipt = json.loads((output / "receipt.json").read_text())
            self.assertFalse((output / "completed.txt").exists())
            self.assertTrue(guard.finished)
            self.assertIsNone(receipt["exitCode"])
            self.assertIsNotNone(receipt["childExitCodeAfterCleanup"])
            self.assertIsNone(receipt["cleanupError"])
            self.assertEqual(receipt["memory"]["breach"], "Synthetic memory breach")

    def test_success_preserves_output_and_zero_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            guard = Guard()
            result = self.run_child(output, "print('completed')", guard)
            self.assertEqual(result["exitCode"], 0)
            self.assertEqual(result["childExitCodeAfterCleanup"], 0)
            self.assertEqual((output / "output.log").read_text().strip(), "completed")
            self.assertTrue(guard.finished)

    def test_nonzero_exit_is_not_success(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            guard = Guard()
            with self.assertRaisesRegex(RuntimeError, "Command failed"):
                self.run_child(output, "raise SystemExit(7)", guard)
            receipt = json.loads((output / "receipt.json").read_text())
            self.assertEqual(receipt["exitCode"], 7)
            self.assertEqual(receipt["childExitCodeAfterCleanup"], 7)
            self.assertTrue(guard.finished)

    def test_terminate_timeout_escalates_with_only_short_waits(self):
        child = ResistantChild()
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(runner.subprocess, "Popen", return_value=child), \
                patch.object(runner.time, "monotonic", side_effect=lambda: child.now), \
                patch.object(runner, "CLEANUP_SECONDS", 0.25):
            output = Path(directory)
            guard = Guard(breach=True)
            with self.assertRaisesRegex(MemoryError, "Synthetic"):
                self.run_child(output, "", guard)
            receipt = json.loads((output / "receipt.json").read_text())
            self.assertEqual(child.terminated, 1)
            self.assertEqual(child.killed, 1)
            self.assertAlmostEqual(child.now, 0.35)
            self.assertEqual(receipt["childExitCodeAfterCleanup"], -9)
            self.assertIsNone(receipt["cleanupError"])
            self.assertTrue(guard.finished)

    def test_post_kill_timeout_preserves_breach_and_failure_receipt(self):
        child = ResistantChild(exits_on_kill=False)
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(runner.subprocess, "Popen", return_value=child), \
                patch.object(runner.time, "monotonic", side_effect=lambda: child.now), \
                patch.object(runner, "CLEANUP_SECONDS", 0.25):
            output = Path(directory)
            guard = Guard(breach=True)
            with self.assertRaisesRegex(MemoryError, "Synthetic") as raised:
                self.run_child(output, "", guard)
            receipt = json.loads((output / "receipt.json").read_text())
            self.assertEqual(child.terminated, 1)
            self.assertEqual(child.killed, 1)
            self.assertAlmostEqual(child.now, 0.6)
            self.assertIsNone(receipt["childExitCodeAfterCleanup"])
            self.assertEqual(receipt["cleanupError"]["type"], "TimeoutExpired")
            self.assertEqual(receipt["memory"]["breach"], "Synthetic memory breach")
            self.assertIn("cleanup also failed", raised.exception.__notes__[0])
            self.assertTrue(guard.finished)

    def test_termination_error_preserves_breach_and_failure_receipt(self):
        child = ResistantChild()
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(runner.subprocess, "Popen", return_value=child), \
                patch.object(child, "terminate", side_effect=OSError("Access denied")):
            output = Path(directory)
            guard = Guard(breach=True)
            with self.assertRaisesRegex(MemoryError, "Synthetic"):
                self.run_child(output, "", guard)
            receipt = json.loads((output / "receipt.json").read_text())
            self.assertEqual(receipt["cleanupError"]["type"], "OSError")
            self.assertIn("Access denied", receipt["cleanupError"]["message"])
            self.assertIsNone(receipt["childExitCodeAfterCleanup"])
            self.assertTrue(guard.finished)


if __name__ == "__main__":
    unittest.main()
