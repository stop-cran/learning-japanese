"""Pinned external repair of protocol014's D/E inline citation extraction only.

Parentheses/backticks delimit prose citations; they are not source-path characters.
D/E requires at least one canonical citation, not that every shorthand source mention
is a formal citation. Every qualified path or recognized source is still passed to
the unchanged exact source-membership and line-range validator. F/O grammar is intact.
The original module filename, imports, CLI, report and config bindings stay unchanged.
"""
import re
import sys
from pathlib import Path

ORIGINAL = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-134\review\fresh-independent-002\lifecycle-011\protocol-014")
OLD_SHA = "f68265d947785a19aaa79480303bb1481b13ea5670ee2a25181ea50dba4aac2d"
sys.path.insert(0, str(ORIGINAL))
from b134_common import frozen, require, sha
from common import load_module

OLD = '''            references = [match.group(1) for cell in row[4:]
                          for match in re.finditer(
                              r"(?<!\\S)([^ \\t;|]+:\\d+(?:\\s*[-–]\\s*\\d+)?)(?=$|[\\s;,.])",
                              cell)]'''
NEW = "            references = inline_references(row[4:], sources)"
INLINE = re.compile(
    r"(?<![^\s(\[;|`])([^\s;|()\[\]`]+:\d+(?:\s*[-–]\s*\d+)?)(?=$|[\s;,.()\[\]`])")
PART = re.compile(r"(.+):(\d+)(?:\s*[-–]\s*(\d+))?")


def inline_references(cells, sources):
    result = []
    for cell in cells:
        for match in INLINE.finditer(cell):
            reference = match[1]
            source = PART.fullmatch(reference)[1].replace("\\", "/")
            if "/" in source or source in sources:
                result.append(reference)
    return result


def load_checker():
    source = ORIGINAL / "check-report-structure-b134-014.py"
    raw = frozen(source, OLD_SHA)
    text = raw.decode("utf-8")
    require(text.count(OLD) == 1, "Original D/E extractor differs; repair not applicable")
    repaired = text.replace(OLD, NEW, 1)
    checker = load_module("b134_report014_delimiter_repair", source)
    exec(compile(repaired, str(source), "exec"), checker.__dict__)
    checker.inline_references = inline_references
    original_check = checker.check

    def check(*args, **kwargs):
        result = original_check(*args, **kwargs)
        result["parserRepair"] = {
            "contract": "de-inline-delimiters-v1", "originalCheckerSha256": OLD_SHA,
            "repairEntrySha256": sha(Path(__file__).read_bytes()),
            "executedCheckerSha256": sha(repaired.encode("utf-8")),
            "scope": "D/E inline extraction only; canonical membership/ranges and F/O grammar unchanged."}
        return result

    checker.check = check
    return checker


if __name__ == "__main__":
    sys.exit(load_checker().main())
