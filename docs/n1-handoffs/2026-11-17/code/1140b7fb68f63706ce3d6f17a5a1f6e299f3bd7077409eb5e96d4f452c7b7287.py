"""Prepare B130 confirmation and closure protocols without accepting content."""
import json
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, load_module, require, sha
from prepare_b129_postreview_tools import derive, run_tests

ROOT = WS / "scratch-130" / "review"
SOURCE = WS / "scratch-129" / "review" / "confirm" / "tooling-preflight.json"
SOURCE_SHA = "b97dafc9d1634c9dbe46271c74075c0d9e163e2e67eed48125ce8ed089ff1d22"
HELPER_SHA = "853ce0d63fe0b020ea65dd598d457db67c218157a84b9779b1448d6a0c712867"
RETENTION_SHA = "d97d5dcff345b972594894f6021d762d1fb46e968e2d1dd37850df9382b9e269"
ADDED_PROTOCOL = (
    '"close_b130.py", "verify_b130_archive.py", "test_close_b130.py", '
    '"test_verify_b130_archive.py", "record_b130_confirmation_decision.py", '
    '"prepare_b130_postreview_tools.py", "archive_b129_chains.py", '
    '"test_b130_archive_retention.py", "b130_external_sources.py", '
    '"test_b130_external_sources.py", "record_b130_publication.py", '
    '"prepare_b130_delivery_recorder.py", "test_record_b130_publication.py"'
)
SOURCES = [
    ("close_b129.py", "close_b130.py",
     "a3f8e53f30f29c3e80c2f846e869a70f363641d4554771d7157ba8d02d004f51",
     [("B129", "B130"), ("batch == 129", "batch == 130"),
      ("from archive_b124_chains_v2 import prepare as prepare_public_chain",
       "from archive_b129_chains import prepare as prepare_public_chain"),
      ('"test_b129_external_sources.py"):',
       '"test_b129_external_sources.py", ' + ADDED_PROTOCOL + "):")]),
    ("verify_b129_archive.py", "verify_b130_archive.py",
     "aa1fd4f264db2e162dd7090bbba13473e9c97a3a0938e8fbbd7046f475f8990d",
     [("B129", "B130"), ("load_batch(129)", "load_batch(130)"),
      ("batch-129-closure", "batch-130-closure"),
      ('provenance["batch"] == 129', 'provenance["batch"] == 130'),
      ('"batch": 129', '"batch": 130'),
      ("from archive_b124_chains_v2 import is_local_only_source",
       "from archive_b129_chains import is_local_only_source")]),
    ("test_close_b129.py", "test_close_b130.py",
     "408ab02c2ae1777178770fdef2a04e5825dc9accc389be9e274b61cfd86f971b",
     [("close_b129", "close_b130"), ("B129", "B130")]),
    ("test_verify_b129_archive.py", "test_verify_b130_archive.py",
     "d0db76363827528a2889254ec3d68ce6eb1db60d87316f734bd779ab3b2884e2",
     [("verify_b129_archive", "verify_b130_archive"),
      ("from archive_b124_chains_v2 import prepare",
       "from archive_b129_chains import prepare")]),
    ("record_b129_confirmation_decision.py", "record_b130_confirmation_decision.py",
     "fe21c3bd13b3ef95a100bf0bdcc06d9356d96795c64f431178ca7eb6033098e6",
     [("B129", "B130"), ("scratch-129", "scratch-130")]),
]


def main():
    frozen(TOOLS / "prepare_b129_postreview_tools.py", HELPER_SHA)
    frozen(TOOLS / "archive_b129_chains.py", RETENTION_SHA)
    producer = {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))}
    previous = json.loads(frozen(SOURCE, SOURCE_SHA))
    require(previous["status"] == "PASS_PREPARATION_ONLY" and previous["testCount"] == 25
            and previous["exitCode"] == 0, "Predecessor confirmation protocol did not pass")
    output = ROOT / "confirm"
    require(not output.exists() and not (ROOT / "postreview-tooling-preflight.json").exists(),
            "Preserve existing B130 outputs")
    require(all(not (TOOLS / name).exists() for _, name, _, _ in SOURCES),
            "Preserve existing B130 lifecycle tools")
    names = {"audit-confirm.py", "check-confirm-structure.py", "renderer.py",
             "test-audit-confirm-isolated.py", "test-confirm-structure.py"}
    require({Path(item["output"]["path"]).name for item in previous["derivations"]} == names,
            "Incomplete source confirmation protocol")
    derivations = [
        derive(Path(item["output"]["path"]), output / Path(item["output"]["path"]).name,
               item["output"]["sha256"], [("B129", "B130")])
        for item in previous["derivations"]
    ]
    engine = previous["engineDerivation"]
    for field in ("output", "helper"):
        frozen(engine[field]["path"], engine[field]["sha256"])
    helper_tests = previous["helperTests"]
    frozen(helper_tests["path"], helper_tests["sha256"])
    load_module("b130_confirmation_renderer", output / "renderer.py").self_test()
    tests = run_tests([
        ("b130_confirmation_audit_fixtures", output / "test-audit-confirm-isolated.py"),
        ("b130_confirmation_structure_fixtures", output / "test-confirm-structure.py"),
        ("b130_confirmation_process_fixtures", Path(helper_tests["path"])),
    ], 25, output / "tooling-tests.txt")
    confirmation = freeze_json(output / "tooling-preflight.json", {
        "batch": 130, "status": "PASS_PREPARATION_ONLY",
        "sourcePreflight": {"path": str(SOURCE), "sha256": SOURCE_SHA},
        "derivations": derivations, "engineDerivation": engine,
        "engineReuse": previous["engineReuse"],
        "exitCode": 0, "tests": tests, "testCount": 25, "protocolTestCount": 21,
        "boundedProcessTestCount": 4, "rendererChecks": 3,
        "helperTests": helper_tests, "producer": producer,
        "limits": "Protocol preparation only. Actual signed revision, family-specific findings "
                  "and source evidence, serial admission and substantive adjudication are required.",
    })
    closure = [derive(TOOLS / old, TOOLS / new, digest, substitutions)
               for old, new, digest, substitutions in SOURCES]
    tests = run_tests([
        ("test_close_b130", TOOLS / "test_close_b130.py"),
        ("test_verify_b130_archive", TOOLS / "test_verify_b130_archive.py"),
        ("test_b130_archive_retention", TOOLS / "test_b130_archive_retention.py"),
    ], 10, ROOT / "postreview-tooling-tests.txt")
    print(json.dumps(freeze_json(ROOT / "postreview-tooling-preflight.json", {
        "batch": 130, "status": "PASS_PREPARATION_ONLY", "producer": producer,
        "helpers": [
            {"path": str(TOOLS / "prepare_b129_postreview_tools.py"), "sha256": HELPER_SHA},
            {"path": str(TOOLS / "archive_b129_chains.py"), "sha256": RETENTION_SHA},
        ],
        "confirmation": confirmation, "closureDerivations": closure,
        "closureTests": tests, "closureTestCount": 10, "totalTestCount": 35,
        "limits": "No candidate changes or acceptance. Closure supports original-reviewer "
                  "confirmation only; any later replacement or failed-context history requires an "
                  "explicit successor preserving that actual history. Complete external extracts "
                  "and co-located material remain local. Actual review outcomes, finalizer, signed "
                  "publication, CI, exact archive checks and owner checkpoint remain outstanding.",
    })))


if __name__ == "__main__":
    main()
