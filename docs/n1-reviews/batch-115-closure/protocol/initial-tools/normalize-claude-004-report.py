"""Perform the two explicitly approved, byte-exact report-format corrections."""
import difflib
import hashlib
import json
import re
import stat
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent / "reports-115"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def freeze(path, data):
    with path.open("xb") as stream:
        stream.write(data)
    path.chmod(stat.S_IREAD)


def main():
    original = REPORTS / "initial-claude-004.md"
    derived = REPORTS / "initial-claude-004-coordinator-normalized.md"
    diff_path = HERE / "N1-B115-CLAUDE-004-normalization.diff"
    record_path = HERE / "N1-B115-CLAUDE-004-normalization.json"
    failed_check = HERE / "N1-B115-CLAUDE-004-report-structure.json"
    checker = HERE / "check-report-structure.py"
    for path in (derived, diff_path, record_path):
        assert not path.exists(), path
    for path in (original, failed_check, checker):
        assert not path.stat().st_mode & stat.S_IWRITE, path
    raw = original.read_bytes()
    assert sha(raw) == "e5a9cfc09d7744df3a89c0b6ef407ddc244931d271f5ccf15b9e6257a9a31983"
    assert sha(failed_check.read_bytes()) == "ae10eaefb383da3b5f0c3a9d4b95d3ce428abb9bc13e98c9a7f184fb27b6e9d4"
    assert sha(checker.read_bytes()) == "0b03424c7d4769c08b3d50a9b3fa6e3a716ce57474ee78afa78fe21e9a9a0c13"
    text = raw.decode("utf-8")
    facet = text.split("### Consistency/quiz safety", 1)[1].split("### Comprehensibility", 1)[0]
    assert re.search(r"(?m)^Verdict: NEEDS FIX\r?$", facet)
    start = raw.index(b"## Per-card results")
    end = raw.index(b"## Findings", start)
    edits = []
    for character, finding in (("卓", "F1"), ("寸", "F2")):
        block = re.search(r"(?ms)^### " + finding + r":.*?(?=^### [FO]\d+:|^## |\Z)", text)
        assert block and character in block[0].splitlines()[0]
        assert re.search(r"(?m)^- Facet: Consistency/quiz safety\r?$", block[0])
        assert re.search(r"(?m)^- Severity: medium\r?$", block[0])
        assert re.search(r"(?m)^- Confidence: high\r?$", block[0])
        assert re.search(r"(?m)^- Required change: \S", block[0])
        prefix = f"| {character} | CLEAN | CLEAN | NEEDS FIX ({finding}) | CLEAN |".encode("utf-8")
        assert raw.count(prefix) == 1
        row_offset = raw.index(prefix, start, end)
        removed = f" ({finding})".encode("ascii")
        offset = row_offset + prefix.index(removed)
        assert raw[offset:offset + len(removed)] == removed
        edits.append({"offset": offset, "removedUtf8": removed.decode("ascii"), "replacementUtf8": ""})
    edits.sort(key=lambda edit: edit["offset"])
    result, cursor = b"", 0
    for edit in edits:
        offset, removed = edit["offset"], edit["removedUtf8"].encode("ascii")
        result += raw[cursor:offset]
        cursor = offset + len(removed)
    result += raw[cursor:]
    restored = result
    for i in reversed(range(len(edits))):
        edit = edits[i]
        offset = edit["offset"] - sum(len(e["removedUtf8"]) for e in edits[:i])
        restored = restored[:offset] + edit["removedUtf8"].encode("ascii") + restored[offset:]
    assert restored == raw and len(raw) - len(result) == 10
    diff = "".join(difflib.unified_diff(text.splitlines(keepends=True),
                                      result.decode("utf-8").splitlines(keepends=True),
                                      fromfile=original.name, tofile=derived.name)).encode("utf-8")
    record = {
        "run": "N1-B115-CLAUDE-004",
        "label": "coordinator-normalized derivative of 004",
        "decisionOrigin": "Coordinator agent; no reviewer contact.",
        "decisionSourceToolCallIds": ["toolu_016SdDhitDUXQD3FFtPyXnFK", "toolu_0199dpFGjYX4RCMtKKcNYPre"],
        "original": {"path": str(original), "sha256": sha(raw), "bytes": len(raw)},
        "derived": {"path": str(derived), "sha256": sha(result), "bytes": len(result)},
        "diff": {"path": str(diff_path), "sha256": sha(diff)},
        "edits": edits,
        "exactByteRestorationVerified": True,
        "mappingsVerifiedFromOriginalReport": "F1 is for 卓 and F2 for 寸; both are required Consistency/quiz safety findings with medium severity and high confidence, consistent with NEEDS FIX.",
        "originalStructureClassification": "FAIL",
        "originalStructureRecordSha256": sha(failed_check.read_bytes()),
        "sameFrozenCheckerSha256": sha(checker.read_bytes()),
        "judgmentsChanged": False,
        "newEvidence": False,
        "reviewerContacted": False,
        "reviewAccepted": False,
        "remainingGates": ["Unchanged structure checker on derivative", "Normal claim adjudication"],
    }
    encoded_record = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    freeze(derived, result)
    freeze(diff_path, diff)
    freeze(record_path, encoded_record)
    assert derived.read_bytes() == result and original.read_bytes() == raw
    print(json.dumps(record, ensure_ascii=False))


if __name__ == "__main__":
    main()
