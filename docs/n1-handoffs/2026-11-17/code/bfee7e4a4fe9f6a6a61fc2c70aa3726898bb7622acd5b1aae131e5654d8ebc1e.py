import hashlib
import unittest

import prepare_b127_candidate_v2 as module
import test_prepare_b127_candidate as original_tests

original_tests.module = module
GateBindingTests = original_tests.GateBindingTests


class RuntimeHashingTests(unittest.TestCase):
    def test_binary_task_assets_preserve_crlf_bytes(self):
        raw = b"\x00binary\r\npayload\xff"
        digest = hashlib.sha256(raw).hexdigest()
        manifest = {
            "listeningTaskAudio": {"task-audio/sample.ogg": digest},
            "listeningTaskImages": {"task-images/sample.webp": digest},
        }
        for expected, binary in module.runtime_entries(manifest).values():
            self.assertTrue(binary)
            self.assertEqual(hashlib.sha256(raw if binary else raw.replace(b"\r\n", b"\n")).hexdigest(), expected)
        self.assertNotEqual(hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest(), digest)

    def test_text_tasks_still_normalize_crlf(self):
        raw = b'{"text": "sample"}\r\n'
        expected = hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
        entries = module.runtime_entries({"listeningTasks": {"listening-tasks/sample.json": expected}})
        digest, binary = entries["listening-tasks/sample.json"]
        self.assertFalse(binary)
        self.assertEqual(hashlib.sha256(raw if binary else raw.replace(b"\r\n", b"\n")).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
