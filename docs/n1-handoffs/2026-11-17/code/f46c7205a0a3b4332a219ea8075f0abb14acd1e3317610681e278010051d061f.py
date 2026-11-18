"""Qualify historical review limitations without changing any publication acceptance gate."""
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen


def main():
    source = TOOLS / "record_b130_integration_publication.py"
    original = frozen(source, "1030d51405b16ea92a620f27dcfc0a012d0c595b477737926b2b17e5ff62b2d7")
    before = b'limits = list(ledger["limits"]) + [limit for limit in context["limits"] if limit not in ledger["limits"]]'
    after = (
        b'limits = list(ledger["limits"]) + [\n'
        b'        "Scope of the integrated-snapshot textual reviews, not later publication checks: " + limit\n'
        b'        for limit in context["limits"] if limit not in ledger["limits"]]'
    )
    require(original.count(before) == 1, "Review-limit qualification anchor differs")
    derived = original.replace(before, after)
    require(derived.replace(after, before) == original, "Qualification is not exactly reversible")
    target = TOOLS / "record_b130_integration_publication_v2.py"
    compile(derived, str(target), "exec")
    output = write_frozen(target, derived)
    print(freeze_json(WS / "scratch-130/review/integration-delivery-scope-derivation-001.json", {
        "sourceSha256": sha(original), "output": output, "reverseExact": True,
        "scope": "Qualify inherited integration-review limitations as review scope, not a denial "
                 "of subsequently completed publication/served-ZIP checks. All acceptance gates "
                 "and original historical ledger/closure metadata remain unchanged.",
        "producerSha256": sha(frozen(Path(__file__))),
    }))


if __name__ == "__main__":
    main()
