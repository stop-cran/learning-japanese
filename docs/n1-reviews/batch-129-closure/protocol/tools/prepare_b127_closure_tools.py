"""Prepare B127 closure tools without closing or modifying the author candidate."""
import io
import json
import unittest
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, write_frozen

TOOLS = Path(__file__).resolve().parent
SOURCES = [
    ("close_b124_v2.py", "close_b127.py",
     "def776cb759c0e3f8f1d0dd54c7722c09a35afc1551f26f2acb5fec7195d24ba",
     [("B124", "B127"), ("batch == 124", "batch == 127"),
      ('"b124-retention-v2-derivation.json"):',
       '"b124-retention-v2-derivation.json", "close_b127.py", "verify_b127_archive.py", '
       '"test_close_b127.py", "test_verify_b127_archive.py", "prepare_b127_closure_tools.py", '
       '"record_b127_confirmation_decision.py", "confirm_b127.py", '
       '"prepare_b127_confirmation_tools.py", "verify_b127_confirmation_tools.py", '
       '"run_b127_tool.py", "b127_lifecycle_process.py", "verify_b127_sources.py"):')]),
    ("verify_b124_archive_v2.py", "verify_b127_archive.py",
     "5a782206eef96c614383fccd42d614d04e6af3e3492b4450663d246993b5f6f2",
     [("B124", "B127"), ("load_batch(124)", "load_batch(127)"),
      ("batch-124-closure", "batch-127-closure"),
      ('provenance["batch"] == 124', 'provenance["batch"] == 127'),
      ('"batch": 124', '"batch": 127')]),
    ("test_close_b124_v2.py", "test_close_b127.py",
     "1939fd778f5ffddcbe81bedda8e70dd0038d39044d61c20f1b7e929946e6a176",
     [("close_b124_v2", "close_b127"), ("B124", "B127")]),
    ("test_verify_b124_archive_v2.py", "test_verify_b127_archive.py",
     "2329879141cf79c69346c767a6ba2124f81d1d89a53f43a7c5931d08c906cc43",
     [("verify_b124_archive_v2", "verify_b127_archive")]),
    ("record_b125_confirmation_decision.py", "record_b127_confirmation_decision.py",
     "c18c8326cc2a709ee512d0cae666df3a8f6db7ae6ea8cb760605708638b71e1a",
     [("B125", "B127"), ("scratch-125", "scratch-127"), ("CONFIRM-002", "CONFIRM-001")]),
]


def main():
    frozen(Path(__file__))
    derivations = []
    for source_name, target_name, expected, substitutions in SOURCES:
        source = TOOLS / source_name
        raw = frozen(source, expected)
        text = raw.decode("utf-8")
        for before, after in substitutions:
            require(before in text and after not in text, f"Ambiguous substitution in {source_name}")
            text = text.replace(before, after)
        restored = text
        for before, after in reversed(substitutions):
            restored = restored.replace(after, before)
        require(restored.encode("utf-8") == raw, f"Nonreversible derivation: {source_name}")
        compile(text, target_name, "exec")
        derivations.append({
            "source": {"path": str(source), "sha256": expected},
            "output": write_frozen(TOOLS / target_name, text.encode("utf-8")),
            "reverseExact": True,
            "substitutions": [{"before": a, "after": b} for a, b in substitutions],
        })
    suite = unittest.TestSuite()
    for name in ("test_close_b127", "test_verify_b127_archive"):
        module = load_module(name, TOOLS / (name + ".py"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    require(suite.countTestCases() == 8, "Incomplete closure fixture suite")
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    log_text = log.getvalue()
    print(log_text, flush=True)
    root = WS / "scratch-127" / "review"
    log_binding = write_frozen(root / "closure-tooling-tests.txt", log_text.encode("utf-8"))
    print(json.dumps(freeze_json(root / "closure-tooling-preflight.json", {
        "batch": 127, "status": "PASS_PREPARATION_ONLY" if result.wasSuccessful() else "HOLD",
        "derivations": derivations, "tests": log_binding, "testCount": result.testsRun,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "limits": "No candidate changes, review acceptance, closure or publication. Same four-run "
                  "initial/confirmation path with optional historical confirmations retained. "
                  "Complete external-snapshot sections and mixed segments remain local. "
                  "Execution must use the bounded B127 Git adapter and RAM guard.",
    })), flush=True)
    require(result.wasSuccessful(), "Closure fixtures failed")


if __name__ == "__main__":
    main()
