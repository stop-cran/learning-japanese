"""Synthetic extension-mode checks in a temporary location; never touches the frozen core or real run outputs."""
import importlib.util
import io
import json
import stat
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from review_chain import digest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prepare_chain", HERE / "prepare-chain.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SUMS = json.loads((module.PACKET / "SHA256SUMS.json").read_bytes())
REFERENCE = json.loads((module.PACKET / "eligibility-reference.json").read_bytes())
INELIGIBLE = set(REFERENCE["newCards"]) | {c for row in REFERENCE["cards"] for c in row["distractors"] + row["quiz_exclusions"]}
PRESENT = [Path(k).stem for k in SUMS if k.startswith("repo/kanji/") and k.endswith(".md")]
ELIGIBLE = [c for c in PRESENT if c not in INELIGIBLE and len(c) == 1 and "\u4e00" <= c <= "\u9fff"]
ABSENT = next(chr(code) for code in range(0x9FA0, 0x4E00, -1) if chr(code) not in set(PRESENT) | INELIGIBLE)
DISTRACTORS = {c for row in REFERENCE["cards"] for c in row["distractors"]}
TARGET = next((c for row in REFERENCE["cards"] for c in row["quiz_exclusions"]
               if c not in set(REFERENCE["newCards"]) | DISTRACTORS and c in PRESENT), None)
NEW = REFERENCE["newCards"][0]


class ExtensionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.cleanup)
        self.count = 0

    def cleanup(self):
        for path in self.root.rglob("*"):
            if path.is_file():
                path.chmod(stat.S_IREAD | stat.S_IWRITE)
        self.temporary.cleanup()

    def prepare(self, text, status="PHASE1_READY", bound=True):
        self.count += 1
        run = f"SYNTH-EXT-{self.count:03d}"
        reply, audit = self.root / f"{run}-list.txt", self.root / f"{run}-audit.json"
        reply.write_bytes(text.encode("utf-8"))
        audit.write_bytes(json.dumps({"status": status, "breaches": [], "phase1ListSha256":
                                      digest(text.encode("utf-8") if bound else b"other")}).encode("utf-8"))
        for path in (reply, audit):
            path.chmod(stat.S_IREAD)
        with redirect_stdout(io.StringIO()):
            module.main(["--reply", str(reply), "--run", run, "--phase1-audit", str(audit),
                         "--records-root", str(self.root), "--chains-root", str(self.root / "chains")])
        preflight = json.loads((self.root / f"{run}-extension-preflight.json").read_bytes())
        message = (self.root / f"{run}-phase2-message.txt").read_bytes()
        return run, preflight, message

    def test_valid_selection_freezes_message_and_chain(self):
        lines = [f"D1 {ELIGIBLE[0]} - {NEW}: synthetic overlap", f"D2 {ABSENT} - {NEW}: synthetic overlap"]
        lines.append(f"E1 {TARGET} - synthetic exclusion check" if TARGET else "E: none")
        run, preflight, message = self.prepare("\n".join(lines))
        manifest = json.loads(Path(preflight["chainManifest"]).read_bytes())
        self.assertEqual(preflight["missingVerbatim"], [lines[1]])
        self.assertEqual(message, (preflight["firstSegment"] + "\nMissing entries:\n" + lines[1]).encode("utf-8"))
        self.assertFalse(message.endswith(b"\n"))
        self.assertEqual(preflight["phase2MessageSha256"], digest(message))
        self.assertEqual([s["source"] for s in manifest["sources"]],
                         [f"repo/kanji/{ELIGIBLE[0]}.md [D1]"] + ([f"repo/kanji/{TARGET}.md [E1]"] if TARGET else []))
        for segment in manifest["segments"]:
            path = Path(segment["path"])
            self.assertTrue(path.is_relative_to(self.root / "chains" / f"b114-{run}-extension"))
            self.assertEqual(digest(path.read_bytes()), segment["sha256"])
            self.assertFalse(path.stat().st_mode & stat.S_IWRITE)

    def test_empty_selection_builds_one_empty_segment(self):
        _, preflight, message = self.prepare("D: none\nE: none")
        self.assertEqual((preflight["segments"], preflight["sources"]), (1, 0))
        self.assertEqual(message, (preflight["firstSegment"] + "\nMissing entries: none").encode("utf-8"))

    def test_invalid_list_voids_without_extension(self):
        with self.assertRaises(ValueError):
            self.prepare(f"D1 {ELIGIBLE[0]} - no colon\nE: none")
        void = json.loads((self.root / "SYNTH-EXT-001-extension-void.json").read_bytes())
        self.assertEqual((void["status"], void["extensionBuilt"]), ("VOID", False))
        self.assertFalse((self.root / "chains").exists())

    def test_unready_or_unbound_audit_is_refused(self):
        for kwargs in ({"status": "PENDING"}, {"bound": False}):
            with self.subTest(**kwargs), self.assertRaises(AssertionError):
                self.prepare("D: none\nE: none", **kwargs)
        self.assertFalse((self.root / "chains").exists())


if __name__ == "__main__":
    unittest.main()
