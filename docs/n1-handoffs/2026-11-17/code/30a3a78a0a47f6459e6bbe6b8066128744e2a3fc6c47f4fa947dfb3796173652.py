"""Resume the unlaunched preparation after creating its report directory."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, sha, write_frozen, json_bytes
from confirm_b132 import OUT, INITIALS, build
from prepare_b132_confirmation_dossiers import OUTPUT, REVISION


def main():
    (WS / "reports-132").mkdir(exist_ok=True)
    first = OUT / "N1-B132-CLAUDE-CONFIRM-001-spec.json"
    spec = json.loads(frozen(first))
    build(first)
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
    ref = write_frozen(OUTPUT / "gpt-response.json", json_bytes(response))
    spec.update(run="N1-B132-GPT-CONFIRM-001", family="gpt", session=INITIALS["gpt"]["session"],
                basis="adjudicated-initial", priorVerdict="UNVERIFIED")
    spec["additionalSources"][-1] = {
        "path": ref["path"], "sha256": ref["sha256"], "source": "author-response/own-response.json"}
    second = OUT / (spec["run"] + "-spec.json")
    freeze_json(second, spec)
    build(second)
    result = {
        "status": "PREPARED_NOT_ADMITTED", "candidate": REVISION,
        "runs": [json.loads(frozen(OUT / ("N1-B132-" + family.upper() + "-CONFIRM-001-preflight.json")))
                 for family in INITIALS],
        "preservedFailure": "confirmation-dossiers-execution-001 stopped before any chain or prompt "
                            "because the separate reports-132 directory did not yet exist. Frozen shared "
                            "source bytes and first spec reused unchanged; no reviewer was admitted.",
        "producerSha256": sha(frozen(Path(__file__))), "reviewersLaunched": False,
    }
    print(json.dumps(freeze_json(OUTPUT / "preparation.json", result)))


if __name__ == "__main__":
    main()
