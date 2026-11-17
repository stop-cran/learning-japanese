"""Consume the coordinator's actual M/proof refs; no worktree writes."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import WS, freeze_json, frozen, sha

R = WS / "scratch-134" / "review"


def ref(path, expected=None):
    return {"path": str(path), "sha256": sha(frozen(path, expected))}


plan = {
    "candidate": "b140716f5df6d17fb872f477556ef77d2cd59b0e",
    "originalGates": {
        "closure": ref(WS / "scratch-134" / "closure-checks-001" / "summary.json"),
        "committed": ref(WS / "scratch-134" / "committed-checks-001" / "summary.json"),
    },
    "mergeGates": {
        "merge": ref(R / "integration-merge-gates-003" / "summary.json",
                     "a98414c42db1d604f8986f467405b40b3188a50590a401f12bdeaad95b3218e4"),
        "committed-merge": ref(R / "integration-merge-committed-gates-001" / "summary.json",
                               "fafc37792f32690c71b8708ad6be5ba71ce27b6619b0d7da1de2eb18652675c6"),
    },
    "preservationProof": ref(R / "integration-preservation-001" / "verification.json",
                             "1d399e894554de6c11ed66f06bdd46b89f2f181c72c108a8bab58612494edf23"),
}
print(json.dumps(freeze_json(Path(__file__).parent / "actual-plan-001.json", plan)))
