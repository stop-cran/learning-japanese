"""Persist an independently authored adjudication only after all real bindings pass."""
import datetime
import json
import sys
from pathlib import Path

from b132_confirmation_records import collect_confirmation
from common import frozen, json_bytes, require, sha, write_frozen
from confirm_b132 import INITIALS, OUT, binding
from verify_b132_teaching_revision import REVISION


def main(family, draft_path):
    require(family in INITIALS, "Unknown family")
    run = "N1-B132-" + family.upper() + "-CONFIRM-002"
    final_path = OUT / (run + "-final.json")
    final = json.loads(frozen(final_path))
    draft_raw = frozen(draft_path)
    adjudication = json.loads(draft_raw)
    require(adjudication["run"] == run and adjudication["candidate"] == REVISION
            and adjudication["finalSha256"] == sha(frozen(final_path))
            and adjudication["reportSha256"] == final["report"]["sha256"], "Draft binding differs")
    adjudication_path, acceptance_path = (OUT / (run + "-" + suffix + ".json")
                                        for suffix in ("adjudication", "acceptance"))
    require(not adjudication_path.exists() and not acceptance_path.exists(), "Preserve prior acceptance")
    acceptance = {
        "run": run, "batch": 132, "candidate": REVISION, "session": INITIALS[family]["session"],
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "reviewAccepted": True, "confirmation": "CONFIRMED", "report": final["report"],
        "final": binding(final_path),
        "adjudication": {"path": str(adjudication_path), "sha256": sha(draft_raw)},
        "tool": binding(Path(__file__)),
        "acceptanceLimit": "One original reviewer's bounded delta confirmation, not publication or whole-set acceptance.",
    }
    acceptance_raw = json_bytes(acceptance)
    pending = {str(adjudication_path): draft_raw, str(acceptance_path): acceptance_raw}

    def read(path, digest):
        if str(path) in pending:
            raw = pending[str(path)]
            require(sha(raw) == digest, "In-memory final binding differs")
            return raw
        return frozen(path, digest)

    audit = json.loads(frozen(final["audit"]["path"], final["audit"]["sha256"]))
    spec = {
        "family": family, "role": "confirmation", "run": run, "session": INITIALS[family]["session"],
        "snapshot": REVISION, "confirmation": "CONFIRMED",
        "acceptance": {"path": str(acceptance_path), "sha256": sha(acceptance_raw)},
        "preflight": binding(OUT / (run + "-preflight.json")),
        "admission": binding(OUT / (run + "-admission.json")),
        "events": binding(Path(final["audit"]["path"]).parent / "events.jsonl", audit["eventsSha256"]),
    }
    collect_confirmation(spec, read)
    write_frozen(adjudication_path, draft_raw)
    print(json.dumps(write_frozen(acceptance_path, acceptance_raw)))


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]))
