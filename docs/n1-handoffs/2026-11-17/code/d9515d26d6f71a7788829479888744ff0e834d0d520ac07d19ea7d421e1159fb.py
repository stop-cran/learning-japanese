"""Recognize the exact additive notes block without requiring an append-only edit."""
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, write_frozen
from verify_b127_reconciliation import REVIEW


def main():
    source = TOOLS / "verify_b127_reconciliation_v2.py"
    original = frozen(source, "e812aceb2ddbee14f696c18ae3b581682734653b44196ca54bf9dc72340cfe39")
    before = b'notes in revised_notes and len(revised_notes) > len(notes)'
    addition = (
        "The [B127 reconciliation packet](n1-sources/batch-127-reconciliation/) adds\r\n"
        "complete finite comparison families, Q1-Q13 dispositions and qualified\r\n"
        "cancellation guards. Its [new ledger revision](n1-sources/batch-127-progress-002.json)\r\n"
        "keeps the original ledger historical and the revised candidate unconfirmed\r\n"
        "and unpublished; delivered accounting remains unchanged.\r\n\r\n"
    ).encode()
    literal = repr(addition).encode()
    after = b"revised_notes.count(" + literal + b") == 1 and revised_notes.replace(" + literal + b', b"", 1) == notes'
    require(original.count(before) == 1 and after not in original, "Unexpected notes check")
    derived = original.replace(before, after)
    require(derived.replace(after, before) == original, "Non-reversible derivation")
    compile(derived, "verify_b127_reconciliation_v3.py", "exec")
    target = write_frozen(TOOLS / "verify_b127_reconciliation_v3.py", derived)
    print(freeze_json(REVIEW / "reconciliation-verifier-v3-derivation.json", {
        "source": {"path": str(source), "sha256": sha(original)}, "output": target,
        "before": before.decode(), "after": after.decode(), "reverseExact": True,
        "reason": "The notes addition is inserted before B126, not appended. Removing exactly the "
                  "observed six-line CRLF block must recover every original byte.",
        "diagnostic": str(REVIEW / "reconciliation-notes-diagnostic-001"),
        "producerSha256": sha(Path(__file__).read_bytes()),
    }))


if __name__ == "__main__":
    main()
