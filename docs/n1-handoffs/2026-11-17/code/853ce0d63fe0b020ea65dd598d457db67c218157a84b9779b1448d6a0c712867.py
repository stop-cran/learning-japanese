"""Prepare B129 confirmation and closure protocols without accepting any content."""
import io
import json
import unittest
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, load_module, require, sha, write_frozen

ROOT = WS / "scratch-129" / "review"
SOURCE = WS / "scratch-128" / "review" / "confirm" / "tooling-preflight.json"
SOURCE_SHA = "82523e34974a05eef8804faa65c8395243d4966d9656a5b5057e4805a5f14f95"
ADDED_PROTOCOL = (
    '"close_b129.py", "verify_b129_archive.py", "test_close_b129.py", '
    '"test_verify_b129_archive.py", "record_b129_confirmation_decision.py", '
    '"prepare_b129_postreview_tools.py", "b129_external_sources.py", '
    '"test_b129_external_sources.py"'
)
SOURCES = [
    ("close_b128.py", "close_b129.py",
     "2aa6bc352e2c9acc95de67ce780ba0a9ef0ce65ef87552a5217278730ffa0910",
     [("B128", "B129"), ("batch == 128", "batch == 129"),
      ('"step_b127.py"):', '"step_b127.py", ' + ADDED_PROTOCOL + "):")]),
    ("verify_b128_archive.py", "verify_b129_archive.py",
     "1134c8c644884af507ee3efa43e8cb0853283144b30baab7b917d7fe051c2ab6",
     [("B128", "B129"), ("load_batch(128)", "load_batch(129)"),
      ("batch-128-closure", "batch-129-closure"),
      ('provenance["batch"] == 128', 'provenance["batch"] == 129'),
      ('"batch": 128', '"batch": 129')]),
    ("test_close_b128.py", "test_close_b129.py",
     "be08f3f62c962acb13c3bdb6b5cf574e8b341742f77a482c7b59b392119776c2",
     [("close_b128", "close_b129"), ("B128", "B129")]),
    ("test_verify_b128_archive.py", "test_verify_b129_archive.py",
     "1602f7c5bfa0dd3be70d713000c1dc534969c4bb8c23402ea8d1e0d119081054",
     [("verify_b128_archive", "verify_b129_archive")]),
    ("record_b128_confirmation_decision.py", "record_b129_confirmation_decision.py",
     "ab30d6d72b50af9dc989a485022cce79250035c4811dd902163a492c081f2f57",
     [("B128", "B129"), ("scratch-128", "scratch-129")]),
]


def derive(source, target, digest, substitutions):
    raw = frozen(source, digest)
    text = raw.decode("utf-8")
    for before, after in substitutions:
        require(before in text and after not in text, f"Ambiguous substitution: {source}: {before}")
        text = text.replace(before, after)
    restored = text
    for before, after in reversed(substitutions):
        restored = restored.replace(after, before)
    require(restored.encode("utf-8") == raw, f"Nonreversible derivation: {source}")
    compile(text, str(target), "exec")
    return {
        "source": {"path": str(source), "sha256": digest},
        "output": write_frozen(target, text.encode("utf-8")),
        "reverseExact": True,
        "substitutions": [{"before": before, "after": after} for before, after in substitutions],
    }


def run_tests(modules, expected, output):
    suite = unittest.TestSuite()
    for name, path in modules:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(load_module(name, path)))
    require(suite.countTestCases() == expected, "Incomplete fixture suite")
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    print(log.getvalue(), flush=True)
    binding = write_frozen(output, log.getvalue().encode("utf-8"))
    require(result.wasSuccessful() and result.testsRun == expected, "Protocol fixtures failed")
    return binding


def main():
    producer = {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))}
    previous = json.loads(frozen(SOURCE, SOURCE_SHA))
    require(previous["status"] == "PASS_PREPARATION_ONLY" and previous["testCount"] == 25
            and previous["exitCode"] == 0, "Predecessor confirmation protocol did not pass")
    output = ROOT / "confirm"
    require(not output.exists() and not (ROOT / "postreview-tooling-preflight.json").exists(),
            "Preserve existing B129 outputs")
    require(all(not (TOOLS / name).exists() for _, name, _, _ in SOURCES),
            "Preserve existing B129 lifecycle tools")
    names = {"audit-confirm.py", "check-confirm-structure.py", "renderer.py",
             "test-audit-confirm-isolated.py", "test-confirm-structure.py"}
    require({Path(item["output"]["path"]).name for item in previous["derivations"]} == names,
            "Incomplete source confirmation protocol")
    derivations = [
        derive(Path(item["output"]["path"]), output / Path(item["output"]["path"]).name,
               item["output"]["sha256"], [("B128", "B129")])
        for item in previous["derivations"]
    ]
    engine = previous["engineDerivation"]
    for field in ("output", "helper"):
        frozen(engine[field]["path"], engine[field]["sha256"])
    helper_tests = previous["helperTests"]
    frozen(helper_tests["path"], helper_tests["sha256"])
    load_module("b129_confirmation_renderer", output / "renderer.py").self_test()
    modules = [
        ("b129_confirmation_audit_fixtures", output / "test-audit-confirm-isolated.py"),
        ("b129_confirmation_structure_fixtures", output / "test-confirm-structure.py"),
        ("b129_confirmation_process_fixtures", Path(helper_tests["path"])),
    ]
    tests = run_tests(modules, 25, output / "tooling-tests.txt")
    confirmation = freeze_json(output / "tooling-preflight.json", {
        "batch": 129, "status": "PASS_PREPARATION_ONLY",
        "sourcePreflight": {"path": str(SOURCE), "sha256": SOURCE_SHA},
        "derivations": derivations, "engineDerivation": engine,
        "engineReuse": "Unchanged batch-generic confirm_b127.py; use run_b127_tool.py for build/final "
                       "and scoped_confirmation_admission.py for admission, never unscoped admit/derive.",
        "exitCode": 0, "tests": tests, "testCount": 25, "protocolTestCount": 21,
        "boundedProcessTestCount": 4, "rendererChecks": 3,
        "helperTests": helper_tests, "producer": producer,
        "limits": "Tool preparation only. No revision, reviewer admission or semantic acceptance. "
                  "Family-isolated chains require actual review results and a verified signed snapshot.",
    })
    closure = [derive(TOOLS / old, TOOLS / new, digest, substitutions)
               for old, new, digest, substitutions in SOURCES]
    tests = run_tests([
        ("test_close_b129", TOOLS / "test_close_b129.py"),
        ("test_verify_b129_archive", TOOLS / "test_verify_b129_archive.py"),
    ], 8, ROOT / "postreview-tooling-tests.txt")
    print(json.dumps(freeze_json(ROOT / "postreview-tooling-preflight.json", {
        "batch": 129, "status": "PASS_PREPARATION_ONLY", "producer": producer,
        "confirmation": confirmation, "closureDerivations": closure,
        "closureTests": tests, "closureTestCount": 8, "totalTestCount": 33,
        "limits": "Protocol fixtures and reversible derivation only; no candidate changes, review "
                  "admission, reconciliation, closure, publication or delivery credit. Finalizer and "
                  "publication tools still require actual verdicts, reviewer IDs and signed successor.",
    })), flush=True)


if __name__ == "__main__":
    main()
