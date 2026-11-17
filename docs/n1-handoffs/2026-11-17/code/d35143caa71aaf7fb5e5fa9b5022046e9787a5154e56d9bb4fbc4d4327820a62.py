"""Retain a VOID audit honestly instead of using the success-only audit summarizer."""
import json
from pathlib import Path

from common import freeze_json, frozen, sha
from derive_selected_followups import derive_file

HERE = Path(__file__).resolve().parent

SUMMARY = '''
def bounded_void_audit(path):
    raw = frozen(path)
    original = json.loads(raw)
    require(original["status"] == "VOID" and original["breaches"]
            and original["final"] and original["reviewerIdle"]
            and not original["recordIncomplete"], "Not a completed VOID audit")
    fields = ("session", "eventsSha256", "eventsBytes", "eventsCount", "status", "breaches",
              "bootstrapVerified", "actualResponseModels", "reviewerIdle", "recordIncomplete",
              "final", "unexpectedUserMessages", "coreRead", "coreRequired", "extensionRead",
              "extensionRequired", "writes", "readbacks", "readbackVerified", "fetches")
    result = {key: original[key] for key in fields if key in original}
    result.update(originalAuditSha256=sha(raw), rawExecutionPayloadsRemainLocal=True,
                  reviewAccepted=False, publicationAccepted=False)
    result["calls"] = [
        {key: call[key] for key in ("id", "name", "event", "phase", "timestamp", "role", "success")
         if key in call} for call in original["calls"]
    ]
    return result

'''

TEST = '''
class VoidAuditSummaryTests(unittest.TestCase):
    def test_void_is_preserved_without_raw_arguments_or_success_relabelling(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from common import json_bytes, sha, write_frozen
        from closure_quarantine_v2 import bounded_void_audit
        audit = PhaseTwoQuarantineTests().fixture()[2]
        audit["calls"] = [{"name": "view", "event": 7,
                           "arguments": {"content": "local-only raw payload"}}]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "audit.json"
            raw = json_bytes(audit)
            write_frozen(path, raw)
            result = bounded_void_audit(path)
            self.assertEqual(result["status"], "VOID")
            self.assertEqual(result["breaches"], audit["breaches"])
            self.assertEqual(result["calls"], [{"name": "view", "event": 7}])
            self.assertEqual(result["originalAuditSha256"], sha(raw))
            self.assertFalse(result["reviewAccepted"])
            self.assertFalse(result["publicationAccepted"])
            audit["status"] = "FINAL_AUDIT_NEEDS_CLAIM_CHECK"
            other = Path(directory) / "successful.json"
            write_frozen(other, json_bytes(audit))
            with self.assertRaises(ValueError):
                bounded_void_audit(other)

'''


def main():
    previous = json.loads(frozen(HERE / "b125-closure-tools-derivation.json",
                                 "16e295522d84a25f717e7959ca355d19035d600d73418a35c3743a607b87c897"))
    for record in previous["derivations"]:
        frozen(record["output"]["path"], record["output"]["sha256"])
    frozen(previous["quarantineHelper"]["path"], previous["quarantineHelper"]["sha256"])
    helper = derive_file("closure_quarantine.py", "closure_quarantine_v2.py", [
        ('STATUS = "VOID_COORDINATOR_PHASE2_DELIVERY_MISMATCH"\n',
         'STATUS = "VOID_COORDINATOR_PHASE2_DELIVERY_MISMATCH"\n' + SUMMARY),
        ('audit_support.bounded_audit(Path(quarantine["audit"]["path"]))',
         'bounded_void_audit(Path(quarantine["audit"]["path"]))'),
    ])
    tests = derive_file("test_closure_quarantine.py", "test_closure_quarantine_v2.py", [
        ("from closure_quarantine import STATUS, require_phase2_void",
         "from closure_quarantine_v2 import STATUS, require_phase2_void"),
        ('if __name__ == "__main__":', TEST + '\nif __name__ == "__main__":'),
    ])
    closure = derive_file("close_b125.py", "close_b125_v2.py", [
        ("from closure_quarantine import archive_excluded",
         "from closure_quarantine_v2 import archive_excluded"),
        ('"b125-closure-tools-derivation.json",',
         '"b125-closure-tools-derivation.json", "close_b125_v2.py",\n'
         '                     "closure_quarantine_v2.py", "test_closure_quarantine_v2.py",\n'
         '                     "test_close_b125_v2.py", "prepare_b125_closure_tools_v2.py",\n'
         '                     "b125-closure-tools-v2-derivation.json",'),
    ])
    closure_tests = derive_file("test_close_b125.py", "test_close_b125_v2.py", [
        ("from close_b125 import require_confirmation, require_intermediate",
         "from close_b125_v2 import require_confirmation, require_intermediate"),
        ("from close_b125 import archive", "from close_b125_v2 import archive"),
    ])
    print(freeze_json(HERE / "b125-closure-tools-v2-derivation.json", {
        "derivations": [helper, tests, closure, closure_tests],
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "preservedFailure": "scratch-125/review/void-archive-preflight-execution-001",
        "scope": "Only excluded protocol-VOID audit summarization changes. The genuine breaches "
                 "and VOID status remain explicit, both acceptance flags remain false, and raw "
                 "arguments remain local. Original audit bytes are hash-bound. Existing successful "
                 "audit summarization and structure-held handling are unchanged. No closure is run.",
    }))


if __name__ == "__main__":
    main()
