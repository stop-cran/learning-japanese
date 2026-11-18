"""Verify an accepted actual FRESH003 review and persist its closure input."""
import json
import sys
from pathlib import Path

from b134_initial_records import INITIALS, disposition_ids
from b134_replacement_records import collect_replacement_record
from close_b134 import require_fresh_inventory
from close_b134_v2 import read_review
from common import WS, freeze_json, frozen, require, sha

ROOT = WS / "scratch-134" / "review"
LIFE = ROOT / "fresh-independent-002" / "lifecycle-011"


def ref(path):
    raw = frozen(path)
    return {"path": str(path), "sha256": sha(raw)}


def main(family):
    require(family in ("claude", "gpt"), "Unknown reviewer family")
    run = "N1-B134-" + family.upper() + "-FRESH-003"
    out = ROOT / (family + "-fresh003-collector-001")
    require(not out.exists(), "Preserve existing collection")
    final_ref = ref(LIFE / (run + "-final.json"))
    final = json.loads(frozen(final_ref["path"], final_ref["sha256"]))
    acceptance = ref(LIFE / (run + "-acceptance.json"))
    item = {
        "spec": {
            "family": family, "run": run, "session": final["session"],
            "snapshot": final["candidate"], "role": "replacement-independent",
            "originalSession": INITIALS[family]["session"],
            "originalReviewerConfirmation": False,
            "verdict": final["structure"]["overall"], "acceptance": acceptance,
        },
        "preflight": ref(LIFE / "audit-configs-020" / "preflight.json"),
        "final": final_ref,
        "launch": ref(LIFE / (run + "-launch.json")),
        "phase1": ref(LIFE / (run + "-phase1.json")),
        "extension": ref(LIFE / (run + "-extension.json")),
    }
    refs, _, claims = collect_replacement_record(
        item["spec"], item["preflight"], item["final"], read_review)
    report = frozen(refs["report"]["path"], refs["report"]["sha256"])
    require_fresh_inventory(report, claims)
    result = {
        "status": "PASS_ACCEPTED_REVIEW_COLLECTION_NOT_CLOSURE",
        "review": item,
        "adjudication": refs["adjudication"],
        "claims": claims,
        "requiredDispositionIds": disposition_ids(report, claims),
        "limits": "Actual review evidence verified; all claim dispositions and both serial families are still required for closure.",
    }
    print(json.dumps(freeze_json(out / "review-input.json", result)))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "collect-b134-fresh003.py claude|gpt")
    main(sys.argv[1])
