"""Preserve the raw membership response and add its terminal LF for chain rendering."""
import json
from pathlib import Path

from b131_confirmation_routing_001 import INITIALS, capacity_check, check_context
from common import WS, freeze_json, frozen, require, sha, write_frozen
from confirm_b131_003 import build, preflight

ROOT = WS / "scratch-131" / "review"
OUT = ROOT / "confirm-003"
RAW_SHA = "889faaefbec573e806f298766d2eee1300674c7b229bd973a35169cd2652cd73"


def main():
    failed = OUT / "N1-B131-GPT-CONFIRM-002-spec.json"
    spec = json.loads(frozen(failed))
    require(spec["run"] == "N1-B131-GPT-CONFIRM-002", "Wrong predecessor")
    item = next(row for row in spec["additionalSources"]
                if row["source"] == "evidence/community/n1-kanji-source-20261102.json")
    raw = frozen(item["path"], item["sha256"])
    require(sha(raw) == RAW_SHA and len(raw) == 7393 and not raw.endswith(b"\n"),
            "Inspect changed membership source formatting")
    presented = raw + b"\n"
    require(json.loads(presented) == json.loads(raw), "Membership presentation changed")
    directory = ROOT / "confirmation-003-membership"
    binding = write_frozen(directory / "membership.json", presented)
    disclosure = {
        "originalPath": item["path"], "originalSha256": RAW_SHA, "originalBytes": len(raw),
        "presentationSha256": binding["sha256"], "presentationBytes": len(presented),
        "method": "The original complete community array has no terminal newline. Exactly one LF "
                  "is appended solely for chain rendering; all original bytes are preserved as a prefix "
                  "and complete parsed JSON equality is verified. The raw original remains unchanged.",
    }
    note = freeze_json(directory / "presentation.json", disclosure)
    item["path"], item["sha256"] = binding["path"], binding["sha256"]
    spec["additionalSources"].append({
        "path": note["path"], "sha256": note["sha256"],
        "source": "verification/community-presentation.json",
    })
    spec["run"] = "N1-B131-GPT-CONFIRM-003"
    path = OUT / (spec["run"] + "-spec.json")
    freeze_json(path, spec)
    build(path)
    runs = []
    for family, run in (("claude", "N1-B131-CLAUDE-CONFIRM-002"),
                        ("gpt", "N1-B131-GPT-CONFIRM-003")):
        record, config = preflight(OUT / (run + "-preflight.json"))
        chain = json.loads(frozen(config["chainManifest"]))
        context = check_context(Path.home() / ".copilot" / "session-state" /
                                INITIALS[family]["session"] / "events.jsonl", family)
        runs.append({"run": run, "session": record["session"],
                     "preflight": {"path": str(OUT / (run + "-preflight.json")),
                                   "sha256": sha(frozen(OUT / (run + "-preflight.json")))},
                     "capacity": capacity_check(context, chain),
                     "segments": len(chain["segments"]), "sources": len(chain["sources"])})
    print(json.dumps(freeze_json(ROOT / "confirmation-003-preparation.json", {
        "status": "PREPARED_NOT_ADMITTED", "candidate": spec["candidate"], "runs": runs,
        "producerSha256": sha(frozen(Path(__file__))),
        "preservedFailures": [
            "confirmation-prepare-execution-001: over-capacity before any admission",
            "confirmation-prepare-execution-002: raw community response lacked terminal LF; no admission",
        ],
        "scope": "All selected semantic records and complete counterpart articles are unchanged "
                 "from preparation001. Preparation002 deduplicates external locator metadata and "
                 "does not repeat the independently verified unchanged-reading host log. This successor "
                 "adds only the disclosed lossless community-array presentation for the second family.",
        "reviewersLaunched": False, "publicationAccepted": False,
    })))


if __name__ == "__main__":
    main()
