"""Repair the preparer using each input's actual line endings."""
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, write_frozen

HERE = Path(__file__).parent


def main():
    source = HERE / "prepare_b129_evidence_v3.py"
    raw = frozen(source)
    newline = b"\r\n" if b"\r\n" in raw else b"\n"
    before = b"    for before, after in changes:" + newline
    after = newline.join((
        b'    newline = "\\r\\n" if b"\\r\\n" in original else "\\n"',
        b"    for before, after in changes:",
        b'        before, after = (value.replace("\\n", newline) for value in (before, after))',
        b"",
    ))
    require(raw.count(before) == 1 and after not in raw, "Ambiguous preparer repair")
    derived = raw.replace(before, after)
    require(derived.replace(after, before) == raw, "Preparer repair is not byte-reversible")
    target = HERE / "prepare_b129_evidence_v3_crlf.py"
    compile(derived, str(target), "exec")
    output = write_frozen(target, derived)
    freeze_json(WS / "scratch-129" / "review" / "evidence-preparer-crlf-repair.json", {
        "source": str(source), "sourceSha256": sha(raw), "output": output,
        "reverseExact": True, "change": "Preserve actual line endings in both preparer and verifier.",
    })
    load_module("b129_corrected_evidence_deriver", target).main()


if __name__ == "__main__":
    main()
