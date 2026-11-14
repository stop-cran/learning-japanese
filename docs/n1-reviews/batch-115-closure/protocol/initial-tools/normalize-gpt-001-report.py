"""Coordinator-approved, citation-only normalization of the GPT-001 report into a new derivative.

Only the six '- Citations:' lines of F1-F6 change: each '<src>:<a>,<b>,...' part is expanded to
'<src>:<a>; <src>:<b>; ...' with the same sources, numbers and order. No other byte changes.
The raw report and its structure FAIL record are never written.
"""
import difflib
import hashlib
import json
import re
import stat
from pathlib import Path

WORKSPACE = Path(r"C:\Users\stop-\n1-kanji-workspace")
RAW = WORKSPACE / "reports-115" / "initial-gpt.md"
RAW_SHA = "34539b74c1ca2da17abe5e959f88151539a564d80a27417d7992b6bf7180d8b3"
FAIL = WORKSPACE / "scratch-115" / "N1-B115-GPT-001-report-structure.json"
FAIL_SHA = "bb6f86e129966f1bd5541ffa5d6e9b2a8bca85f55259d1c2cdf92d3c6588b61c"
OUT = WORKSPACE / "reports-115" / "initial-gpt-coordinator-normalized.md"
DIFF = WORKSPACE / "scratch-115" / "N1-B115-GPT-001-normalization.diff"
RECORD = WORKSPACE / "scratch-115" / "N1-B115-GPT-001-normalization.json"
EXPECTED_FINDINGS = ["F1", "F2", "F3", "F4", "F5", "F6"]
EXPECTED_EXPANSIONS = 17
MULTI = re.compile(r"(.+?):(\d+(?:-\d+)?(?:,\d+(?:-\d+)?)+)")
PREFIX = "- Citations: "


def sha(data):
    return hashlib.sha256(data).hexdigest()


def readonly(path):
    return bool(path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY)


def main():
    raw = RAW.read_bytes()
    assert sha(raw) == RAW_SHA and readonly(RAW), "raw report drifted or is writable"
    assert sha(FAIL.read_bytes()) == FAIL_SHA and readonly(FAIL), "FAIL record drifted or is writable"
    fail = json.loads(FAIL.read_bytes())
    assert fail["status"] == "FAIL" and len(fail["errors"]) == EXPECTED_EXPANSIONS
    assert all("is not <source>:<line> or <source>:<first>-<last>" in e for e in fail["errors"])
    for path in (OUT, DIFF, RECORD):
        assert not path.exists(), f"already exists: {path}"

    text = raw.decode("utf-8")
    assert "\r\n" in text and "\n" not in text.replace("\r\n", ""), "expected uniform CRLF"
    lines = text.split("\r\n")
    current, plan, out = None, [], []
    for index, line in enumerate(lines):
        heading = re.match(r"### (F\d+|O\d+):", line)
        if heading:
            current = heading[1]
        if not line.startswith(PREFIX):
            out.append(line)
            continue
        parts = line[len(PREFIX):].split("; ")
        assert "; ".join(parts) == line[len(PREFIX):]
        new_parts, groups = [], []
        for part in parts:
            match = MULTI.fullmatch(part)
            if match:
                items = match[2].split(",")
                new_parts += [f"{match[1]}:{item}" for item in items]
                groups.append({"original": part, "expanded": [f"{match[1]}:{item}" for item in items]})
            else:
                assert "," not in part.rsplit(":", 1)[-1], part
                new_parts.append(part)
                groups.append({"original": part, "expanded": [part]})
        new_line = PREFIX + "; ".join(new_parts)
        if new_line != line:
            assert current in EXPECTED_FINDINGS, f"unexpected change outside F1-F6 at line {index + 1}"
            plan.append({"item": current, "line": index + 1, "groups": groups,
                         "expansions": sum(1 for g in groups if len(g["expanded"]) > 1)})
        out.append(new_line)

    assert [p["item"] for p in plan] == EXPECTED_FINDINGS, [p["item"] for p in plan]
    assert sum(p["expansions"] for p in plan) == EXPECTED_EXPANSIONS
    derived = "\r\n".join(out).encode("utf-8")

    # Reversal proof: rebuild the original only from the derivative and the recorded groups.
    back = derived.decode("utf-8").split("\r\n")
    assert len(back) == len(lines)
    changed = {p["line"]: p for p in plan}
    for number, line in enumerate(back, 1):
        if number not in changed:
            assert line == lines[number - 1], f"unexpected change at line {number}"
            continue
        parts = line[len(PREFIX):].split("; ")
        rebuilt, cursor = [], 0
        for group in changed[number]["groups"]:
            take = parts[cursor:cursor + len(group["expanded"])]
            assert take == group["expanded"], (number, take, group)
            source = take[0].rsplit(":", 1)[0]
            assert all(t.rsplit(":", 1)[0] == source for t in take)
            rebuilt.append(source + ":" + ",".join(t.rsplit(":", 1)[1] for t in take))
            cursor += len(take)
        assert cursor == len(parts)
        back[number - 1] = PREFIX + "; ".join(rebuilt)
    restored = "\r\n".join(back).encode("utf-8")
    assert restored == raw, "reversal does not restore the raw report"

    diff = "".join(difflib.unified_diff(
        raw.decode("utf-8").splitlines(keepends=True), derived.decode("utf-8").splitlines(keepends=True),
        fromfile=f"a/{RAW.name}", tofile=f"b/{OUT.name}", n=0)).encode("utf-8")

    for path, data in ((OUT, derived), (DIFF, diff)):
        with path.open("xb") as stream:
            stream.write(data)
        path.chmod(stat.S_IREAD)
    record = {
        "run": "N1-B115-GPT-001",
        "authorization": "Coordinator e1ee36b6 decision toolu_015hdCtjkdomT9ZotA3gPqHx: citation-only normalization; "
                         "no reviewer contact; no further correction on failure.",
        "raw": {"path": str(RAW), "bytes": len(raw), "sha256": RAW_SHA, "readOnly": readonly(RAW)},
        "rawStructureFail": {"path": str(FAIL), "sha256": FAIL_SHA, "errors": len(fail["errors"])},
        "derived": {"path": str(OUT), "bytes": len(derived), "sha256": sha(derived)},
        "diff": {"path": str(DIFF), "bytes": len(diff), "sha256": sha(diff)},
        "bytesDelta": len(derived) - len(raw),
        "changedLines": [p["line"] for p in plan],
        "changedItems": [p["item"] for p in plan],
        "expansions": EXPECTED_EXPANSIONS,
        "plan": plan,
        "reversalRestoresRaw": True,
        "unchangedLines": len(lines) - len(plan),
        "lineEndings": "CRLF preserved",
        "limit": "Reporting-format normalization only; no verdict, finding, evidence or wording changed.",
    }
    data = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with RECORD.open("xb") as stream:
        stream.write(data)
    RECORD.chmod(stat.S_IREAD)
    print(json.dumps({"derivedSha256": sha(derived), "derivedBytes": len(derived), "diffSha256": sha(diff),
                      "recordSha256": sha(data), "changedLines": record["changedLines"],
                      "bytesDelta": record["bytesDelta"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
