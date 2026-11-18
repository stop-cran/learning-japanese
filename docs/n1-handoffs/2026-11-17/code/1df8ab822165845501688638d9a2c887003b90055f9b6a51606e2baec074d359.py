"""Narrow the confirmation reread to the changed card and its four direct guards."""
import json
from pathlib import Path

from common import freeze_json, frozen, sha, write_frozen, json_bytes
from confirm_b132 import OUT, INITIALS, build
from prepare_b132_confirmation_dossiers import OUTPUT, REVISION


def main():
    original = json.loads(frozen(OUT / "N1-B132-CLAUDE-CONFIRM-001-spec.json"))
    presentation = json.loads(frozen(OUTPUT / "presentation.json"))
    presentation["unchangedArticlesNotReread"] = {
        "paths": ["kanji/暮.md", "kanji/募.md", "kanji/川.md", "words/墓.md"],
        "reason": "The original reviewed distractors and supporting article have no revised field or "
                  "meaning-guard role. Their bytes and all reading choices are independently verified unchanged. "
                  "This is a delta confirmation, not repeated initial review of those articles.",
    }
    presentation_ref = freeze_json(OUTPUT / "presentation-002.json", presentation)
    original["revisedSources"] = ["kanji/" + char + ".md" for char in "墓標塔埋石"]
    for row in original["additionalSources"]:
        if row["source"] == "verification/presentation.json":
            row.update(path=presentation_ref["path"], sha256=presentation_ref["sha256"])
    response = {
        "candidate": REVISION,
        "change": "Only two direct precautions, qualified Notes and related citations; generated "
                  "manifest and additive contributor evidence changed. No other teaching or source field changed.",
        "ownPriorItems": {
            "Q1": "Source gap addressed with independent complete 標/marker records; "
                  "direct precaution implemented. Verify the pair hypotheses.",
            "Q2": "Source gap addressed with independent complete 塔/stone-tower records; "
                  "direct precaution implemented. Verify restrictions and pair hypotheses.",
        },
        "acceptance": "Implementation claims only; no presumption of confirmation.",
    }
    ref = write_frozen(OUTPUT / "gpt-response-002.json", json_bytes(response))
    for family, item in INITIALS.items():
        spec = json.loads(json.dumps(original))
        spec.update(run="N1-B132-" + family.upper() + "-CONFIRM-002",
                    family=family, session=item["session"])
        if family == "gpt":
            spec.update(basis="adjudicated-initial", priorVerdict="UNVERIFIED")
            spec["additionalSources"][-1] = {
                "path": ref["path"], "sha256": ref["sha256"], "source": "author-response/own-response.json"}
        path = OUT / (spec["run"] + "-spec.json")
        freeze_json(path, spec)
        build(path)
    result = {
        "status": "PREPARED_NOT_ADMITTED", "candidate": REVISION,
        "runs": [json.loads(frozen(OUT / ("N1-B132-" + family.upper() + "-CONFIRM-002-preflight.json")))
                 for family in INITIALS],
        "preservedFailures": [
            "execution001: missing separate report directory, before chains.",
            "execution002: first-family projected703550 exceeded700000; no admission or reviewer delivery. "
            "Only unchanged original distractors and support are excluded from this narrower delta reread. "
            "All changed cards, actual guards and complete selected sources remain. The same change is used for both families.",
        ],
        "producerSha256": sha(frozen(Path(__file__))), "reviewersLaunched": False,
    }
    print(json.dumps(freeze_json(OUTPUT / "preparation-002.json", result)))


if __name__ == "__main__":
    main()
