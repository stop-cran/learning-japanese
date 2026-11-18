"""Reproduce the inspected neutral-source proof without replacing its output."""
import json

from common import WS, freeze_json, frozen, require, sha

ROOT = WS / "scratch-134" / "review"
PREPARATION = ROOT / "neutral-preparation-001"
HERE = PREPARATION / "projected-successor-001"
PRODUCER = PREPARATION / "tools" / "verify-complete-b134-001.py"
PRODUCER_SHA = "3b389d8ff9622c8dbab4128842e9f8cb8b2f1a22e3e5fcba47197906a1231ca9"
EXPECTED_PATH = HERE / "complete-verification-001.json"


def main():
    expected_raw = frozen(EXPECTED_PATH)
    expected = json.loads(expected_raw)
    require(expected["status"] == "PASS_NEUTRAL_BYTES_AND_SOURCE_COMPLETENESS_NOT_TEACHING_REVIEW"
            and expected["candidate"] == "ba80afffc20a72d31be68b355b6f90aab36a5726"
            and not expected["memory"]["breach"], "Unexpected neutral-source proof")
    namespace = {"__name__": "coordinator_reproduction", "__file__": str(PRODUCER)}
    exec(compile(frozen(PRODUCER, PRODUCER_SHA), str(PRODUCER), "exec"), namespace)
    captured = []

    def compare_only(path, result):
        require(path == EXPECTED_PATH and not result["memory"]["breach"],
                "Unexpected reproduction output or memory breach")
        require({k: v for k, v in result.items() if k != "memory"}
                == {k: v for k, v in expected.items() if k != "memory"},
                "Neutral-source proof did not reproduce")
        captured.append(result)
        return {"sourceProofReproduced": True}

    namespace["freeze_json"] = compare_only
    namespace["main"]()
    require(len(captured) == 1 and frozen(EXPECTED_PATH) == expected_raw,
            "Missing proof reproduction or changed original")
    result = {
        "status": "PASS_REPRODUCED_NEUTRAL_SOURCE_PROOF_NOT_REVIEW_ADMISSION",
        "candidate": expected["candidate"],
        "base": expected["base"],
        "producer": {"path": str(PRODUCER), "sha256": PRODUCER_SHA},
        "reproducedProof": {"path": str(EXPECTED_PATH), "sha256": sha(expected_raw)},
        "proof": captured[0],
        "limits": "Source/byte checks reproduced; independent capacity proof is separate. Final handoff and actual reviews remain required.",
    }
    print(json.dumps(freeze_json(ROOT / "independent-neutral-source-verification-001.json", result)))


if __name__ == "__main__":
    main()
