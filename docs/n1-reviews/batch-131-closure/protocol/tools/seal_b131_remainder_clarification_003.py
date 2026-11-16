"""Preserve002 and clarify overlapping remainder-query provenance without changing packet or review scope."""
import json
from pathlib import Path

from b131_review_v2_common import HERE, PACKET, freeze_json, frozen, require, sha, start_guard
from b131_review_v2_derivations import verify_jm


def main():
    guard, _ = start_guard("B131002 exact remainder-query provenance clarification")
    try:
        original_path = HERE / "preparation-handoff-002.json"
        original_raw = frozen(original_path)
        original = json.loads(original_raw)
        partition = json.loads(frozen(HERE / "derivation-verification-002.json"))["jmdictPartition"]
        verify_jm(frozen(PACKET / "evidence/jmdict-families.xml"),
                  frozen(PACKET / "evidence/jmdict-review-core.xml"),
                  json.loads(frozen(PACKET / "eligibility-reference.json")),
                  json.loads(frozen(PACKET / "evidence/dictionary-index.json")), partition)
        groups = {name: {"records": len(row["ids"]), "recordBytes": row["recordBytes"]}
                  for name, row in partition["remainderClasses"].items()}
        require(sum(row["records"] for row in groups.values()) == 259, "Remainder count differs")
        keb = groups["undeclared-exact-keb"]
        shared = groups["undeclared-exact-keb-and-other-exact-reb"]
        reb = groups["other-exact-reb"]
        require(keb["records"] + shared["records"] == 160
                and keb["recordBytes"] + shared["recordBytes"] == 102039
                and reb == {"records": 99, "recordBytes": 51928}
                and len(partition["undeclaredComparisonCharacters"]) == 115, "Aggregate remainder estimate differs")
        detail = {
            "status": "VERIFIED_QUERY_PROVENANCE_CLARIFICATION_ONLY", "classes": groups,
            "undeclaredComparisonCharacters": len(partition["undeclaredComparisonCharacters"]),
            "scope": "No candidate, packet, core-chain, forecast, prompt, cap or runtime gate change.",
            "clarification": "The aggregate160 exact-keb-reached records/102039bytes matches the estimate, "
                "but 'reached ONLY by exact-keb queries' is not literal for all160: "
                + str(shared["records"]) + " records/" + str(shared["recordBytes"]) +
                "bytes also belong to other exact-reb queries. The other99/51928bytes have only other-exact-reb "
                "provenance. This mechanical query-provenance overlap does not alter the615/259 core partition "
                "or selected-character supplementation rule."}
        detail["memory"] = guard.finish()
        require(not detail["memory"]["breach"], "Clarification RAM breach")
        clarification = freeze_json(HERE / "remainder-query-clarification-003.json", detail)
        original["supersedes"] = {"path": str(original_path), "sha256": sha(original_raw),
                                  "reason": "Add exact overlapping remainder-query counts; no source/tool change."}
        original["remainderQueryClarification"] = clarification
        original["deviations"].append(detail["clarification"])
        original["files"]["preparation"].append(clarification)
        tool = Path(__file__)
        original["files"]["tools"].append({"path": str(tool), "sha256": sha(frozen(tool)),
                                           "bytes": tool.stat().st_size})
        binding = freeze_json(HERE / "preparation-handoff-003.json", original)
        print(json.dumps({"handoff": binding, "clarification": clarification, **detail}, ensure_ascii=False))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
