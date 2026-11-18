"""Persist an independently authored B134 confirmation adjudication only after all real bindings pass."""
import datetime
import json
import re
import sys
from pathlib import Path

from b134_initial_records import INITIALS, P, PREFLIGHT
from b134_confirmation_records import collect_confirmation
from common import frozen, json_bytes, require, sha, write_frozen
from confirm_b134 import OUT, binding
from run_b134_closure_checks import CANDIDATE


def initial_binding(family):
    known = INITIALS[family]
    run = "N1-B134-" + family.upper() + "-001"
    spec = {"family": family, "run": run, "role": "initial", "snapshot": CANDIDATE,
            "session": known["session"], "verdict": known["verdict"],
            "acceptance": {"path": str(P / f"{run}-acceptance.json"), "sha256": known["acceptance"]}}
    return {"spec": spec, "preflight": PREFLIGHT,
            "final": {"path": str(P / f"{run}-final.json"), "sha256": known["final"]}}


def main(run, draft_path):
    match = re.fullmatch(r"N1-B134-(CLAUDE|GPT)-CONFIRM-[0-9]{3}", run)
    require(match, "Invalid confirmation run")
    family = match[1].lower()
    session = INITIALS[family]["session"]
    preflight_path, final_path = (OUT / (run + "-" + suffix + ".json") for suffix in ("preflight", "final"))
    preflight = json.loads(frozen(preflight_path))
    final = json.loads(frozen(final_path))
    candidate = preflight["candidate"]
    require(preflight["session"] == final["session"] == session and final["candidate"] == candidate,
            "Confirmation identity differs")
    draft_raw = frozen(draft_path)
    adjudication = json.loads(draft_raw)
    require(adjudication["run"] == run and adjudication["candidate"] == candidate
            and adjudication["finalSha256"] == sha(frozen(final_path))
            and adjudication["reportSha256"] == final["report"]["sha256"], "Draft binding differs")
    adjudication_path, acceptance_path = (OUT / (run + "-" + suffix + ".json")
                                          for suffix in ("adjudication", "acceptance"))
    require(not adjudication_path.exists() and not acceptance_path.exists(), "Preserve prior acceptance")
    acceptance = {
        "run": run, "batch": 134, "candidate": candidate, "session": session,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "reviewAccepted": True, "confirmation": "CONFIRMED", "report": final["report"],
        "final": binding(final_path),
        "adjudication": {"path": str(adjudication_path), "sha256": sha(draft_raw)},
        "tool": binding(Path(__file__)),
        "acceptanceLimit": "One original reviewer's bounded confirmation, not publication or whole-set acceptance.",
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
        "family": family, "role": "confirmation", "run": run, "session": session,
        "snapshot": candidate, "confirmation": "CONFIRMED",
        "acceptance": {"path": str(acceptance_path), "sha256": sha(acceptance_raw)},
        "preflight": binding(preflight_path),
        "admission": binding(OUT / (run + "-admission.json")),
        "events": binding(Path(final["audit"]["path"]).parent / "events.jsonl", audit["eventsSha256"]),
    }
    collect_confirmation(spec, initial_binding(family), read)
    write_frozen(adjudication_path, draft_raw)
    print(json.dumps(write_frozen(acceptance_path, acceptance_raw)))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "accept_b134_confirmation.py RUN DRAFT")
    main(sys.argv[1], Path(sys.argv[2]))
