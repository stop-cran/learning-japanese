"""Prepare B125 closure tooling with explicit nonaccepted protocol-VOID retention."""
from pathlib import Path

from common import freeze_json, frozen, sha
from derive_selected_followups import derive_file

HERE = Path(__file__).resolve().parent


def main():
    frozen(HERE / "close_b124_v2.py",
           "def776cb759c0e3f8f1d0dd54c7722c09a35afc1551f26f2acb5fec7195d24ba")
    frozen(HERE / "verify_b124_archive_v2.py",
           "5a782206eef96c614383fccd42d614d04e6af3e3492b4450663d246993b5f6f2")
    frozen(HERE / "test_close_b124_v2.py",
           "1939fd778f5ffddcbe81bedda8e70dd0038d39044d61c20f1b7e929946e6a176")
    frozen(HERE / "test_verify_b124_archive_v2.py",
           "2329879141cf79c69346c767a6ba2124f81d1d89a53f43a7c5931d08c906cc43")
    closure = derive_file("close_b124_v2.py", "close_b125.py", [
        ('"""Archive B124 review evidence with complete external-snapshot segments retained locally."""',
         '"""Archive B125 accepted evidence and separately labelled failed protocol evidence."""'),
        ("from closure_initials import archive_excluded",
         "from closure_quarantine import archive_excluded"),
        ('require(batch == 124, "This closure adapter is limited to B124")',
         'require(batch == 125, "This closure adapter is limited to B125")'),
        ('                     "b124-closure-derivation.json",',
         '                     "b124-closure-derivation.json", "close_b125.py",\n'
         '                     "closure_quarantine.py", "test_closure_quarantine.py",\n'
         '                     "test_close_b125.py", "prepare_b125_closure_tools.py",\n'
         '                     "verify_b125_archive.py", "test_verify_b125_archive.py",\n'
         '                     "prepare_b125_confirmation_tools.py",\n'
         '                     "b125-closure-tools-derivation.json",'),
    ])
    verifier = derive_file("verify_b124_archive_v2.py", "verify_b125_archive.py", [
        ('"""Verify published B124 chain bytes and explicit local-only source retention."""',
         '"""Verify B125 accepted and excluded chain bytes and local-only source retention."""'),
        ("config = load_batch(124)", "config = load_batch(125)"),
        ('"batch-124-closure"', '"batch-125-closure"'),
        ('provenance["batch"] == 124', 'provenance["batch"] == 125'),
        ('start_guard("B124 archived-chain verification")',
         'start_guard("B125 archived-chain verification")'),
        ('        for review in provenance["reviewLineage"]:',
         '        lineage = provenance["reviewLineage"]\n'
         '        excluded = provenance["excludedInitialRuns"]\n'
         '        require(not {row["run"] for row in lineage} & {row["run"] for row in excluded}\n'
         '                and all(row["reviewAccepted"] is False and row["finalAcceptance"] is False\n'
         '                        for row in excluded), "Excluded evidence was relabelled as accepted")\n'
         '        for review in [*lineage, *excluded]:'),
        ('"batch": 124, "status": "PASS"', '"batch": 125, "status": "PASS"'),
    ])
    tests = derive_file("test_close_b124_v2.py", "test_close_b125.py", [
        ("from close_b124_v2 import require_confirmation, require_intermediate",
         "from close_b125 import require_confirmation, require_intermediate"),
        ("from close_b124_v2 import archive", "from close_b125 import archive"),
        ('"limited to B124"', '"limited to B125"'),
    ])
    archive_tests = derive_file("test_verify_b124_archive_v2.py", "test_verify_b125_archive.py", [
        ("from verify_b124_archive_v2 import verify_chain",
         "from verify_b125_archive import verify_chain"),
    ])
    print(freeze_json(HERE / "b125-closure-tools-derivation.json", {
        "derivations": [closure, verifier, tests, archive_tests],
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "quarantineHelper": {"path": str(HERE / "closure_quarantine.py"),
                             "sha256": sha(frozen(HERE / "closure_quarantine.py"))},
        "scope": "B125 only; accepted initial selection and all final-review gates unchanged. "
                 "The separately labelled diagnosed protocol VOID is preserved, never relabelled "
                 "as a structure hold or accepted evidence. Actual archive verification also "
                 "covers excluded chains. Complete external captures and raw events stay local. "
                 "This producer does not execute closure or touch teaching.",
    }))


if __name__ == "__main__":
    main()
