"""Derive the B121 finalizer that also archives the actual-schema revision verifier evidence."""
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).resolve().parent
SOURCE_SHA = "3571cbb4be88b8b9667454ba62a1fe7a43c0e144a334bb36c8da9c1cfd868349"
TEST_SHA = "5ae01ea3b26a487f73c872ee7c9793d7c0fe41f35ee59b03756372c4cb323f44"
OLD_VERIFICATION = '''        for name in ("coordinator-candidate-verification.json", "coordinator-runtime-glyph-check.json",
                     "source-contract.json"):
'''
NEW_VERIFICATION = '''        for name in ("coordinator-candidate-verification.json", "coordinator-runtime-glyph-check.json",
                     "source-contract.json", "revision-verifier-v2-derivation.json",
                     "source-selection-verification-001.json", "finalizer-v2-derivation.json"):
'''
OLD_TOOLS = '''        for name in ("verify_b121_revision.py", "test_verify_b121_revision.py",
                     "verify_reconciliation_sources.py", "finalize_b121.py", "test_finalize_b121.py",
                     "record_publication.py", "test_record_publication.py"):
'''
NEW_TOOLS = '''        for name in ("verify_b121_revision.py", "test_verify_b121_revision.py",
                     "verify_reconciliation_sources.py", "finalize_b121.py", "test_finalize_b121.py",
                     "record_publication.py", "test_record_publication.py",
                     "verify_b121_revision_v2.py", "test_verify_b121_revision_v2.py",
                     "prepare_b121_revision_v2.py", "verify_b121_source_selection.py",
                     "finalize_b121_v2.py", "test_finalize_b121_v2.py", "derive_b121_finalizer_v2.py"):
'''
OLD_IMPORT = "from finalize_b121 import "
NEW_IMPORT = "from finalize_b121_v2 import "


def load(name, digest):
    raw = frozen(HERE / name, digest)
    text = raw.decode("utf-8").replace("\r\n", "\n")
    require(text.replace("\n", "\r\n").encode("utf-8") == raw, f"Expected uniform CRLF endings: {name}")
    return text


def emit(name, text):
    compile(text, name, "exec")
    return write_frozen(HERE / name, text.replace("\n", "\r\n").encode("utf-8"))


def main():
    original = load("finalize_b121.py", SOURCE_SHA)
    require(original.count(OLD_VERIFICATION) == 1 and original.count(OLD_TOOLS) == 1,
            "Original finalizer differs")
    derived = original.replace(OLD_VERIFICATION, NEW_VERIFICATION).replace(OLD_TOOLS, NEW_TOOLS)
    require(derived.replace(NEW_VERIFICATION, OLD_VERIFICATION).replace(NEW_TOOLS, OLD_TOOLS) == original,
            "Reverse finalizer delta differs")
    test = load("test_finalize_b121.py", TEST_SHA)
    require(test.count(OLD_IMPORT) == 1, "Original finalizer test differs")
    derived_test = test.replace(OLD_IMPORT, NEW_IMPORT)
    require(derived_test.replace(NEW_IMPORT, OLD_IMPORT) == test, "Reverse test delta differs")
    finalizer = emit("finalize_b121_v2.py", derived)
    finalizer_test = emit("test_finalize_b121_v2.py", derived_test)
    freeze_json(WS / "scratch-121" / "review" / "finalizer-v2-derivation.json", {
        "sources": {"finalizer": {"path": str(HERE / "finalize_b121.py"), "sha256": SOURCE_SHA},
                    "test": {"path": str(HERE / "test_finalize_b121.py"), "sha256": TEST_SHA}},
        "outputs": {"finalizer": finalizer, "test": finalizer_test},
        "reverseExact": True,
        "reason": "Closure must also archive the actual-schema revision verifier v2, its test, producer and "
                  "derivation record, plus the independent source-selection verification. check_gate is "
                  "byte-identical in both verifiers, so the original import is retained. No check, "
                  "accounting or ledger field changes.",
        "producer": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
        "publicationAccepted": False,
    })


if __name__ == "__main__":
    main()
