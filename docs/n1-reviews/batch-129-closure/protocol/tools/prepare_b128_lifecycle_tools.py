"""Derive B128 closure, finalization and publication tools from accepted B127 sources."""
import io
import json
import sys
import unittest
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, write_frozen

TOOLS = Path(__file__).resolve().parent
OUT = WS / "scratch-128" / "review"
SESSIONS = [("b1e90345-f8f3-4c8d-b776-09eb8d299ba9", "1f199715-ebef-41e0-9e84-fda61248555f"),
            ("3d1c4b40-90b0-466d-a565-32a96db5281c", "40f6292a-b52f-4d9a-ac86-25bbc5cad512")]
B128_TOOLS = ('"close_b128.py", "verify_b128_archive.py", "test_close_b128.py", '
              '"test_verify_b128_archive.py", "record_b128_confirmation_decision.py", '
              '"prepare_b128_lifecycle_tools.py", "b128_external_sources.py", '
              '"test_b128_external_sources.py", "step_b127.py"')
SOURCES = [
    ("close_b127_v2.py", "close_b128.py",
     "2300d35f6a1fecadbdb19361f3b9a02ca50fa3418483ee7d8ec25986de810f5c",
     [("B127", "B128"), ("batch == 127", "batch == 128"),
      ('"verify_b127_sources.py"):', '"verify_b127_sources.py", ' + B128_TOOLS + "):")]),
    ("verify_b127_archive.py", "verify_b128_archive.py",
     "c2e71819cd6c54b32be0dc4b3792d0336ef88661b57e71230eaa01a9e0495ea5",
     [("B127", "B128"), ("load_batch(127)", "load_batch(128)"),
      ("batch-127-closure", "batch-128-closure"),
      ('provenance["batch"] == 127', 'provenance["batch"] == 128'),
      ('"batch": 127', '"batch": 128')]),
    ("test_close_b127.py", "test_close_b128.py",
     "2a0a3a9ff240c878a0195f33a8ca534df67e355c61e255a0b3c581b95e03b523",
     [("close_b127", "close_b128"), ("B127", "B128")]),
    ("test_verify_b127_archive.py", "test_verify_b128_archive.py",
     "78bf4620623b4a7c497b90203062360cd6222472f921811f7969d0e70c670f4c",
     [("verify_b127_archive", "verify_b128_archive")]),
    ("record_b127_confirmation_decision.py", "record_b128_confirmation_decision.py",
     "8c0094a300d8a5935a0751ed22f8ec4dfc117028f6e70cff53007fc058508980",
     [("B127", "B128"), ("scratch-127", "scratch-128")]),
    ("finalize_b127.py", "finalize_b128.py",
     "b42be194de0d4fe54e6eec6be244136cfb496adb4d80f263974341e2ca07fec8",
     [("B127", "B128"), ("b127", "b128"), ("batch-127", "batch-128"),
      ('provenance["batch"] == 127', 'provenance["batch"] == 128'),
      ('proof["batch"] == 127', 'proof["batch"] == 128'),
      ("load_batch(127)", "load_batch(128)"), ('"batch": 127', '"batch": 128'),
      *SESSIONS,
      ('("CLEAN" if family == "claude" else "NEEDS FIX")',
       '("NEEDS FIX" if family == "claude" else "UNVERIFIED")'),
      (r"\u5009", r"\u5507"),
      ('old["sourceRows"] == [57]', 'old["sourceRows"] == [159]'),
      ('proof["runtimeEntries"] == 8716', 'proof["runtimeEntries"] == 8718'),
      ('["publishedPendingRecordsWithCards"] == 256', '["publishedPendingRecordsWithCards"] == 257'),
      ('["publishedN1Additions"] == 250', '["publishedN1Additions"] == 251'),
      ('["undelivered"] == 972', '["undelivered"] == 971'),
      ("reviewClosedPendingRecordsWithCards=257", "reviewClosedPendingRecordsWithCards=258"),
      ("notStarted=971", "notStarted=970"),
      ("Independent Claude CLEAN and GPT NEEDS FIX initials",
       "Independent Claude NEEDS FIX and GPT UNVERIFIED initials")]),
    ("test_finalize_b127.py", "test_finalize_b128.py",
     "223b4c73fe3c7a43ecce9df4d999bc0cd949047c1043185b1e917b66818db57f",
     [("finalize_b127", "finalize_b128"), ("B127FinalizerTests", "B128FinalizerTests"),
      (r"\u5009", r"\u5507"),
      ('"rawVerdict": "CLEAN" if family == "claude" else "NEEDS FIX"',
       '"rawVerdict": "NEEDS FIX" if family == "claude" else "UNVERIFIED"'),
      ('"batch": 127', '"batch": 128'), ('"sourceRows": [57]', '"sourceRows": [159]'),
      ('"publishedPendingRecordsWithCards": 256', '"publishedPendingRecordsWithCards": 257'),
      ('"publishedN1Additions": 250', '"publishedN1Additions": 251'),
      ('"undelivered": 972', '"undelivered": 971'),
      ('"runtimeEntries": 8716', '"runtimeEntries": 8718'),
      ('["publishedPendingRecordsWithCards"], 256)', '["publishedPendingRecordsWithCards"], 257)'),
      ('["undelivered"], 972)', '["undelivered"], 971)'),
      ('"delivered": 257, "n1Additions": 251, "n2Placements": 6, "remaining": 971',
       '"delivered": 258, "n1Additions": 252, "n2Placements": 6, "remaining": 970')]),
    ("run_b127_closure_checks.py", "run_b128_closure_checks.py",
     "f2a368c98da4ade8a3b68c57a41f15c585dc1873f94281965122e8a3319c7ee7",
     [("B127", "B128"), ("b127", "b128"), ("scratch-127", "scratch-128"),
      ("load_batch(127)", "load_batch(128)"), ("batch-127", "batch-128"),
      ('"batch": 127', '"batch": 128')]),
    ("prepare_b127_publication_tools.py", "prepare_b128_publication_tools.py",
     "4d53eb441d1bf26e100fa4981682a6622391e3de64e5c4bbedca34758f4c818e",
     [("B127", "B128"), ("load_batch(127)", "load_batch(128)"), ("batch-127", "batch-128"),
      ("finalize_b127", "finalize_b128"), ("scratch-127", "scratch-128"),
      ('"batch": 127', '"batch": 128'),
      ('"8706": "8716"', '"8706": "8718"'), ('"252": "257"', '"252": "258"'),
      ('"246": "251"', '"246": "252"'), ('"976": "971"', '"976": "970"'),
      (r'r"\u60a0": r"\u5009"', r'r"\u60a0": r"\u5507"')]),
]


def derive(source_name, target_name, expected, substitutions):
    source = TOOLS / source_name
    raw = frozen(source, expected)
    text = raw.decode("utf-8")
    for before, after in substitutions:
        require(before in text and after not in text, f"Ambiguous substitution in {source_name}: {before}")
        text = text.replace(before, after)
    # Only the closure tool keeps B127 names: its archived-protocol list deliberately retains them.
    require("127" not in text or target_name == "close_b128.py",
            f"Unreviewed B127 residue in {target_name}")
    restored = text
    for before, after in reversed(substitutions):
        restored = restored.replace(after, before)
    require(restored.encode("utf-8") == raw, f"Nonreversible derivation: {source_name}")
    compile(text, target_name, "exec")
    return {"source": {"path": str(source), "sha256": expected},
            "output": write_frozen(TOOLS / target_name, text.encode("utf-8")),
            "reverseExact": True,
            "substitutions": [{"before": a, "after": b} for a, b in substitutions]}


def main():
    frozen(Path(__file__))
    require(not (OUT / "lifecycle-tooling-preflight.json").exists(), "Preserve existing preflight")
    derivations = [derive(*item) for item in SOURCES]
    sys.path.insert(0, str(TOOLS))
    suite = unittest.TestSuite()
    for name in ("test_close_b128", "test_verify_b128_archive", "test_finalize_b128"):
        module = load_module(name, TOOLS / (name + ".py"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    require(suite.countTestCases() == 11, "Incomplete lifecycle fixture suite")
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    print(log.getvalue(), flush=True)
    tests = write_frozen(OUT / "lifecycle-tooling-tests.txt", log.getvalue().encode("utf-8"))
    print(json.dumps(freeze_json(OUT / "lifecycle-tooling-preflight.json", {
        "batch": 128, "status": "PASS_PREPARATION_ONLY" if result.wasSuccessful() else "HOLD",
        "derivations": derivations, "tests": tests, "testCount": result.testsRun,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "limits": "Tool derivation and fixtures only. No reconciliation verification, confirmation, "
                  "closure, ledger change or publication. Reconciliation verifier and confirmation "
                  "preparer require the actual signed handoff and are derived separately.",
    })), flush=True)
    require(result.wasSuccessful(), "Lifecycle fixtures failed")


if __name__ == "__main__":
    main()
