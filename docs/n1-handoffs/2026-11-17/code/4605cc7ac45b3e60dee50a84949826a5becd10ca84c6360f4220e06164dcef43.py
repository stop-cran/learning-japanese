"""Preserve every review limitation in B130's eventual publication receipt."""
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen

SOURCE_SHA = "8fe079fd0ace61b5e7c7c5f24e11fa7eb677a3b5f10cf749b8edae9486f44376"


def main():
    source = TOOLS / "record_publication.py"
    target = TOOLS / "record_b130_publication.py"
    raw = frozen(source, SOURCE_SHA)
    before = b'ledger["limits"][:2] + ['
    after = b'ledger["limits"] + ['
    require(raw.count(before) == 1 and after not in raw, "Publication limit anchor differs")
    derived = raw.replace(before, after)
    require(derived.replace(after, before) == raw, "Derivation is not byte-reversible")
    compile(derived, str(target), "exec")
    output = write_frozen(target, derived)
    print(freeze_json(WS / "scratch-130" / "review" / "delivery-recorder-derivation-001.json", {
        "batch": 130,
        "status": "PREPARATION_ONLY",
        "source": {"path": str(source), "sha256": SOURCE_SHA},
        "output": output,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "substitution": {"before": before.decode("ascii"), "after": after.decode("ascii")},
        "reverseExact": True,
        "scope": "Retain all ordered review limitations, rather than only the first two, in "
                 "both the publication provenance and updated progress ledger. Owner identity, "
                 "remote main, signatures, CI, served archive, reviewed runtime, source membership "
                 "and closure bindings retain the predecessor's unchanged checks.",
        "limits": "Preparation only; no review closure, publication or delivery credit. The future "
                  "closure ledger must distinguish enduring limitations from resolved lifecycle "
                  "gates; do not describe publication as pending in its enduring limits.",
    }))


if __name__ == "__main__":
    main()
