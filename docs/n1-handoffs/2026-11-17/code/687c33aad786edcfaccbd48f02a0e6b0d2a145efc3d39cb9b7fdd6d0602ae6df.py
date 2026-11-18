import unittest
from pathlib import Path

from common import load_module

repair = load_module("b134_native_transport_repair",
                     Path(__file__).with_name("b134_revision_confirmation_v4.py"))
native = load_module("b134_native_creation_controls",
                     Path(__file__).with_name("test-native-create.py"))
native.repair = repair


class NativeTransportTests(native.NativeCreateTests):
    def test_uniform_host_lf_to_crlf_expansion_is_bound(self):
        Path(self.path).write_bytes(self.text.replace("\n", "\r\n").encode("utf-8"))
        repair.check_native_create(self.events, self.path)

    def test_mixed_endings_bare_cr_and_content_changes_are_rejected(self):
        requested = b"first\nsecond\n"
        self.assertTrue(repair.transport_valid(requested, requested))
        self.assertTrue(repair.transport_valid(b"first\r\nsecond\r\n", requested))
        for stored in (b"first\r\nsecond\n", b"first\rsecond\r", b"first\nchanged\n",
                       b"first\nsecond", b"first\nsecond\n\n"):
            with self.subTest(stored=stored):
                self.assertFalse(repair.transport_valid(stored, requested))


if __name__ == "__main__":
    unittest.main()
