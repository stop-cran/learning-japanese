"""Preserve attempt001; explicitly load hyphenated protocol tests in a fresh namespace."""
import json
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen
from prepare_b131_confirmation_engine_001 import SOURCE, SOURCE_SHA, derive_text

PREDECESSOR = TOOLS / "prepare_b131_confirmation_engine_001.py"
PREDECESSOR_SHA = "c818cbcd2d9f808f7751d84400a1a29ef24501c67ee2e8ddef2984a6351a5891"
OUTPUT = TOOLS / "confirm_b131_002.py"
ROOT = WS / "scratch-131" / "review"


def corrected_text(source):
    text = derive_text(source)
    before = '    code, stdout, stderr = python("-m", "unittest", "discover", "-s", str(out), "-p", "test-*.py")'
    after = (
        '    command = ("import sys, unittest; sys.path.insert(0, " + repr(str(out)) + "); "\n'
        '               "unittest.main(module=None, argv=[\'unittest\', "\n'
        '               "\'test-audit-confirm\', \'test-confirm-structure\'])")\n'
        '    code, stdout, stderr = python("-c", command)\n'
        '    require(re.search(r"Ran [1-9][0-9]* tests", stdout + stderr),\n'
        '            "Protocol test execution did not run any tests")'
    )
    require(text.count(before) == 1, "Unexpected test command in retained derivation")
    text = text.replace(before, after)
    for before in ('review_dir(batch) / "confirm"', 'review_dir(spec["batch"]) / "confirm"'):
        require(text.count(before) == 1, "Unexpected confirmation output routing")
        text = text.replace(before, before.replace('"confirm"', '"confirm-002"'))
    return text


def main():
    frozen(PREDECESSOR, PREDECESSOR_SHA)
    text = corrected_text(frozen(SOURCE, SOURCE_SHA).decode("utf-8"))
    compile(text, str(OUTPUT), "exec")
    output = write_frozen(OUTPUT, text.encode("utf-8"))
    print(json.dumps(freeze_json(ROOT / "confirmation-engine-derivation-002.json", {
        "status": "PREPARATION_ONLY", "source": {"path": str(SOURCE), "sha256": SOURCE_SHA},
        "retainedPredecessor": {"path": str(PREDECESSOR), "sha256": PREDECESSOR_SHA},
        "output": output, "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "correction": "Attempt001 preserved: unittest discovery skipped hyphenated module names and "
                      "failed with NO TESTS RAN. Explicit module loading now matches the original "
                      "protocol runner, and a positive executed-test count is required. All new "
                      "protocol files use confirm-002; failed confirm outputs stay unchanged.",
        "reviewersLaunched": False, "semanticAcceptance": False, "publicationAccepted": False,
    })))


if __name__ == "__main__":
    main()
