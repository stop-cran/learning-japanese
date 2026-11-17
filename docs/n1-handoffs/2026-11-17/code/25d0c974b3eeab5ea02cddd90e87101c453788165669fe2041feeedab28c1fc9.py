import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location(
    "fetch_snapshots_b128", Path(__file__).with_name("fetch-snapshots-b128.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Response:
    status = 200
    headers = {"Content-Type": "text/html; charset=utf-8"}

    def __init__(self, size=100):
        self.remaining = size
        self.read_sizes = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def geturl(self):
        return "https://www.kanjipedia.jp/kanji/example"

    def read(self, size):
        self.read_sizes.append(size)
        count = min(size, self.remaining)
        self.remaining -= count
        return b"x" * count


class SnapshotCaptureTests(unittest.TestCase):
    def run_capture(self, response):
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        root = Path(stack.enter_context(tempfile.TemporaryDirectory()))
        self.guard = Mock()
        self.guard.finish.return_value = {"breach": None}
        stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
        stack.enter_context(patch.object(module, "load_batch", return_value={
            "batch": 128, "candidate": "c" * 40, "members": ["\u501f"]}))
        stack.enter_context(patch.object(module, "review_dir", return_value=root))
        stack.enter_context(patch.object(module, "start_guard", return_value=(self.guard, None)))
        stack.enter_context(patch.object(module, "at_commit", return_value=(
            "[source](https://www.kanjipedia.jp/kanji/example)\n").encode("utf-8")))
        stack.enter_context(patch.object(module.urllib.request, "urlopen", return_value=response))
        stack.enter_context(patch.object(module, "write_frozen", return_value={"sha256": "raw"}))
        self.record = stack.enter_context(patch.object(
            module, "freeze_json", return_value={"sha256": "record"}))
        module.main(128)

    def test_cited_kanjipedia_source_is_captured_with_bounded_reads(self):
        response = Response()
        self.run_capture(response)
        record = self.record.call_args.args[1]
        self.assertEqual(len(record["results"]), 2)
        self.assertEqual(record["results"][0]["citedUrl"], "https://www.kanjipedia.jp/kanji/example")
        self.assertEqual(record["results"][0]["citedBy"][0]["card"], "snapshot/kanji/\u501f.md")
        self.assertEqual(set(response.read_sizes), {65536})
        self.guard.check.assert_called()

    def test_oversized_source_aborts_without_success_receipt(self):
        response = Response(4 * 1024**2 + 1)
        with self.assertRaisesRegex(ValueError, "bounded response allowance"):
            self.run_capture(response)
        self.record.assert_not_called()
        self.assertEqual(set(response.read_sizes), {65536})
        self.guard.finish.assert_called_once()


if __name__ == "__main__":
    unittest.main()
