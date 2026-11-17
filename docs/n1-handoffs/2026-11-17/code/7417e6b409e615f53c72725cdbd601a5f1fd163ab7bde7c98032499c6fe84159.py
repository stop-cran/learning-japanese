"""Derive B133 receipt/ledger validators with explicit, pinned fresh-review provenance."""
from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen


def replace(raw, old, new):
    newline = "\r\n" if b"\r\n" in raw else "\n"
    before = old.replace("\n", newline).encode()
    after = new.replace("\n", newline).encode()
    require(raw.count(before) == 1, "Derivation anchor missing or ambiguous")
    return raw.replace(before, after)


def main():
    original = frozen(TOOLS / "record_b133_publication.py",
                      "f37387e7a0154c0d67dafc05ba08853e05a1c1a243fd2f612fa929d40a2d6f7b")
    replacements = [
        ("from common import freeze_json",
         "from b133_closure_origins import validate_final_identity, validate_history\n"
         "from common import freeze_json"),
        ('and entry["session"] == originals[entry["family"]], "Final review identity/snapshot differs")',
         ', "Final review identity/snapshot differs")\n'
         '        validate_final_identity(entry, originals, closure["recordedFileSha256"])'),
        ('    checks = closure["publicationChecks"]',
         '    validate_history(closure)\n    checks = closure["publicationChecks"]'),
    ]
    raw = original
    for old, new in replacements:
        raw = replace(raw, old, new)
    restored = raw
    for old, new in reversed(replacements):
        restored = replace(restored, new, old)
    require(restored == original, "Recorder derivation not reversible")
    recorder = write_frozen(TOOLS / "record_b133_publication_v2.py", raw)
    original_records = frozen(TOOLS / "b133_closure_records.py")
    records = write_frozen(TOOLS / "b133_closure_records_v2.py",
                          replace(original_records, "from record_b133_publication import",
                                  "from record_b133_publication_v2 import"))
    print(freeze_json(WS / "scratch-133" / "review" / "closure-recorders-v2-derivation.json", {
        "recorder": recorder, "records": records, "originalRecorderSha256": sha(original),
        "originalRecordsSha256": sha(original_records),
        "originValidatorSha256": sha(frozen(TOOLS / "b133_closure_origins.py")),
        "scope": "Only add pinned fresh-Claude identity and complete accepted/unaccepted history. "
                 "Unchanged signing, CI, ZIP, runtime, gate and delivery-accounting checks.",
    }))


if __name__ == "__main__":
    main()
