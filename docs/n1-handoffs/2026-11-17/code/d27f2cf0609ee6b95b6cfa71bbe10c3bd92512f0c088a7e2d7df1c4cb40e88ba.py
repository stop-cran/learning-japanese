"""Build B134 closure-request-002 for the authorized-confirmation assembler.

Request-001 is reused unchanged except for corrected limit wording and three retained
protocol files: the v3 closure assembler, its unit test and the pinned revision ledger.
"""
import copy
import json
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOOLS = Path(r"C:\Users\stop-\n1-kanji-workspace\review-tools")
BASE = (ROOT / "authorized-revision-resolution-001" / "closure-request.json",
        "e97762e048262037ff300a146a53c2aae13664bb9270e188433b606c8791307f")
COPIES = (
    ("protocol/close_b134_v3.py", "close_b134_v3.py",
     "5473ddaa5d3882cdf6f47d37a240aa595885d168ad471f5f7472250cbf9b8059"),
    ("protocol/test_close_b134_v3.py", "test_close_b134_v3.py",
     "6a2402143f8c224a7bb3c58fe2019db8780069fea6f50e603d94d787e7f754cf"),
    ("protocol/b134_revision_progress.py", "b134_revision_progress.py",
     "545e499a57a2b611c6e97073a55b30be33738b1a6ab2bc34e82327a8e9e770cb"),
)
EDITS = {
    0: ("Both original and FRESH003 raw verdicts remain unchanged; authorized same-FRESH003 descendant "
        "confirmations are separate roles, not original001 reviewer confirmations.",
        "Both original and FRESH-003 raw verdicts remain unchanged; authorized same-FRESH-003 descendant "
        "confirmations are separate roles, not original 001 reviewer confirmations."),
    1: ("Current correction cc374 retains58 exclusions; the prior355 snapshot had56. Readings, curated "
        "distractors and support article remain unchanged.",
        "Current correction cc374051 retains 58 exclusions; the prior 355cccb8 snapshot had 56. Readings, "
        "curated distractors and support article remain unchanged."),
    8: ("Original and FRESH003 raw verdicts/adjudications remain unchanged. Signed correction and authorized "
        "bounded confirmations are separate evidence.",
        "Original and FRESH-003 raw verdicts/adjudications remain unchanged. Signed correction and authorized "
        "bounded confirmations are separate evidence."),
    9: ("These twelve dispositions supplement, never replace, the original twenty-nine.",
        "The twelve confirmation dispositions supplement, never replace, the original twenty-nine."),
    11: ("Authorization, semantic-tail, source and execution validity remain requirements of the actual "
         "confirmation collector; schema compatibility grants no acceptance.",
         "Authorization, semantic-tail, source and execution validity were checked by the confirmation "
         "collectors and this closure assembler; schema compatibility alone grants no acceptance."),
    13: ("No native/device/rendered-font/custom-pool, closure, integration or publication credit.",
         "The confirmations grant no native, device, rendered-font, custom-pool or publication credit; "
         "delivery credit requires the signed push, CI and served-ZIP equality."),
}


def main():
    request = json.loads(frozen(*BASE))
    changed = copy.deepcopy(request)
    require(len(changed["limits"]) == 14, "Unexpected request-001 limits")
    for index, (old, new) in EDITS.items():
        require(changed["limits"][index] == old, "Request-001 limit differs: " + str(index))
        changed["limits"][index] = new
    present = {item["archivePath"] for item in changed["evidence"]}
    copies = []
    for archive, name, digest in COPIES:
        require(archive not in present, "Evidence already retained: " + archive)
        saved = write_frozen(HERE / name, frozen(TOOLS / name, digest))
        changed["evidence"].append({"archivePath": archive, "path": saved["path"], "sha256": saved["sha256"]})
        copies.append(saved)
    require({key: value for key, value in changed.items() if key not in ("limits", "evidence")}
            == {key: value for key, value in request.items() if key not in ("limits", "evidence")}
            and changed["evidence"][:len(request["evidence"])] == request["evidence"],
            "Request-002 changed more than limits and appended evidence")
    saved = freeze_json(HERE / "closure-request-002.json", changed)
    print(json.dumps({"status": "PASS", "baseSha256": BASE[1], "request": saved, "copies": copies,
                      "editedLimits": sorted(EDITS), "builderSha256": sha(Path(__file__).read_bytes())}))


if __name__ == "__main__":
    main()
