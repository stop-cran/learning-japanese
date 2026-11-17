"""Capture the actually received authorization and prepare requests; no review admission."""
import json
import sys
from pathlib import Path

TOOLS = Path(r"C:\Users\stop-\n1-kanji-workspace\review-tools")
sys.path.insert(0, str(TOOLS))
from common import freeze_json, frozen, sha, write_frozen

ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
EVENT = "69e8afe9-c16a-4322-843f-ade61ab30a8e"


def main():
    source = Path.home() / ".copilot" / "session-state" / "18d6f691-cddd-4198-94f4-e834456349d0" / "events.jsonl"
    matches = [line for line in source.read_bytes().splitlines(keepends=True)
               if json.loads(line).get("id") == EVENT]
    assert len(matches) == 1
    saved = write_frozen(ROOT / "authorization-event.jsonl", matches[0])
    print("AUTH_SHA=" + saved["sha256"])
    for family, old in (("claude", "revision-confirmation-claude-003"),
                        ("gpt", "revision-confirmation-gpt-002")):
        preflight_path = REVIEW / old / "preflight.json"
        preflight = json.loads(frozen(preflight_path))
        spec = json.loads(frozen(**{"path": preflight["spec"]["path"],
                                    "expected": preflight["spec"]["sha256"]}))
        spec["run"] = f"N1-B134-{family.upper()}-REVISION-002"
        spec["authorization"] = {"path": saved["path"], "sha256": saved["sha256"]}
        spec["continuation"] = {
            "kind": "same-claude-reconsideration" if family == "claude" else "same-gpt-full-dossier",
            "priorPreflight": {"path": str(preflight_path), "sha256": sha(frozen(preflight_path))},
            "originalObligationCount": 41,
            "authorizationIsProspective": True,
            "oldEvidenceRemainsHeld": True,
        }
        freeze_json(ROOT / f"request-{family}.json", spec)


if __name__ == "__main__":
    main()
