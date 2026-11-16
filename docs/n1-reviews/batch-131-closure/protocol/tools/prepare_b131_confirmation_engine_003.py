"""Route the protocol auditor's digest import to the already pinned shared chain."""
import json
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen
from prepare_b131_confirmation_engine_001 import SOURCE, SOURCE_SHA
from prepare_b131_confirmation_engine_002 import corrected_text

PREDECESSOR = TOOLS / "prepare_b131_confirmation_engine_002.py"
PREDECESSOR_SHA = "202068392f675d34010b8e285a5c3f0c0fd2e63ec5fff3ab5d6b516eee404380"
OUTPUT = TOOLS / "confirm_b131_003.py"
ROOT = WS / "scratch-131" / "review"


def final_text(source):
    text = corrected_text(source)
    require(text.count(' / "confirm-002"') == 2, "Unexpected recovered output routing")
    text = text.replace(' / "confirm-002"', ' / "confirm-003"')
    before = '        prefix = b""\n'
    after = (
        '        if name == "audit-confirm.py":\n'
        '            old_route = b"sys.path.insert(0, str(HERE.parent))"\n'
        '            new_route = b"sys.path.insert(0, str(HERE.parent / \'preparation-003\'))"\n'
        '            require(derived.count(old_route) == 1, "Unexpected auditor chain import")\n'
        '            derived = derived.replace(old_route, new_route)\n'
        '            require(derived.replace(new_route, old_route).replace(\n'
        '                f"B{batch}".encode("ascii"), b"B116") == selected,\n'
        '                "Auditor delta is not exactly batch label plus chain import namespace")\n'
        '        prefix = b""\n'
    )
    require(text.count(before) == 1, "Unexpected derivation prefix")
    text = text.replace(before, after)
    before = '"soleSelectedDelta": f"B116 to B{batch}"'
    after = ('"selectedDeltas": [f"B116 to B{batch}"] + (\n'
             '                                ["digest import: shared preparation-003 chain"]\n'
             '                                if name == "audit-confirm.py" else [])')
    require(text.count(before) == 1, "Unexpected derivation disclosure")
    return text.replace(before, after)


def main():
    frozen(PREDECESSOR, PREDECESSOR_SHA)
    text = final_text(frozen(SOURCE, SOURCE_SHA).decode("utf-8"))
    compile(text, str(OUTPUT), "exec")
    output = write_frozen(OUTPUT, text.encode("utf-8"))
    print(json.dumps(freeze_json(ROOT / "confirmation-engine-derivation-003.json", {
        "status": "PREPARATION_ONLY", "source": {"path": str(SOURCE), "sha256": SOURCE_SHA},
        "retainedPredecessor": {"path": str(PREDECESSOR), "sha256": PREDECESSOR_SHA},
        "output": output, "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "correction": "Attempt002's test failure is retained: the legacy auditor imported review_chain "
                      "from the batch root, where B131 has no such module. Its sole import-route change "
                      "now points to the pinned preparation-003 shared chain. All auditor functions "
                      "remain byte-identical apart from the B116-to-B131 label. Fresh confirm-003 "
                      "outputs preserve both failed protocol preparations.",
        "reviewersLaunched": False, "semanticAcceptance": False, "publicationAccepted": False,
    })))


if __name__ == "__main__":
    main()
