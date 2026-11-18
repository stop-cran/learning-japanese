"""Admit a disclosed fresh-context reviewer with scoped serialization and unchanged RAM gates."""
import datetime
import json
import sys
from pathlib import Path

from common import (GUARD, GUARD_SHA, freeze_json, frozen, load_batch, load_module,
                    require, review_dir, sha, start_guard, write_frozen)
from confirm_v2 import clean, preflight
from scoped_admission import assess_status

SCOPE_SHA = "e40e5107ef31e3040c0b212786dbce0f680b1d718b3cdbb7bb9a086aeaea7df8"


def assess_confirmation_status(status, session_id, free_ram):
    assessment = assess_status(status, "", free_ram)
    matching = [s for s in status["sessions"] if s["id"] == session_id]
    require(len(matching) == 1, "Fresh reviewer absent or ambiguous")
    reviewer = matching[0]
    name = reviewer.get("name")
    require(isinstance(name, str) and name.strip(), "Fresh reviewer name is missing")
    require(sum(s.get("name") == name for s in status["sessions"]) == 1,
            "Duplicate fresh-reviewer session name")
    require(session_id in assessment["scope"]["sessionIds"], "Fresh reviewer outside N1 scope")
    require(not reviewer.get("awaiting_user_input") and not reviewer.get("awaiting_plan_approval"),
            "Fresh reviewer needs user input")
    return {
        "policy": "n1-fresh-reviewer-scoped-confirmation-v1",
        "scope": assessment["scope"],
        "activeSessions": assessment["activeSessions"],
        "blockingSessions": assessment["blockingSessions"],
        "unrelatedActiveSessions": assessment["unrelatedActiveSessions"],
        "freeRamBytes": free_ram,
        "startupFloorMet": assessment["startupFloorMet"],
        "reviewerSessionNameUnique": True,
        "reviewerSession": session_id,
        "statusAllowsAdmission": assessment["startupFloorMet"] and not assessment["blockingSessions"],
        "note": "A new same-family reviewer confirms the historical original review with disclosed attribution. Full unfiltered "
                "snapshot retained; only N1 descendants and same-content-repository activity block. "
                "Unrelated isolated work is disclosed, not a machine-wide reservation.",
    }


def admit(path, status_path):
    record, config = preflight(path)
    require(record.get("replacementReason") == "pre-admission-context-capacity"
            and record["session"] != record["originalSession"]
            and record["replayedFrom"] and record["contextObservation"],
            "Fresh-context origin missing")
    now = datetime.datetime.now(datetime.timezone.utc)
    require(abs(now.timestamp() - status_path.stat().st_mtime) < 180, "Status is stale")
    status_raw = status_path.read_bytes()
    scope_path = Path(__file__).with_name("scoped_admission.py")
    frozen(scope_path, SCOPE_SHA)
    frozen(GUARD, GUARD_SHA)
    resource = load_module("confirmation_admission_ram", GUARD)
    assessment = assess_confirmation_status(json.loads(status_raw), record["session"],
                                            resource.available_ram())
    require(assessment["statusAllowsAdmission"], json.dumps(assessment, ensure_ascii=False))
    clean(load_batch(record["batch"]), record["candidate"])
    require(not Path(config["report"]).exists(), "Report already exists")
    events = Path.home() / ".copilot" / "session-state" / record["session"] / "events.jsonl"
    raw = events.read_bytes()
    require(raw.endswith(b"\n"), "Incomplete event prefix")
    checker = load_module("scoped_confirmation_context",
                          review_dir(record["batch"]) / "check-run-context.py")
    context = checker.check(events)
    require(context["status"] == "PASS" and context["eventsSha256"] == sha(raw),
            "Context failed or changed")
    guard, _ = start_guard(record["run"])
    memory = guard.finish()
    require(not memory["breach"], "RAM guard breached")
    out = path.parent
    prefix = write_frozen(out / f"{record['run']}-pre-delivery-events.jsonl", raw)
    snapshot = write_frozen(out / f"{record['run']}-admission-status.json", status_raw)
    result = {
        **record, "admittedAt": now.isoformat(), "offset": len(raw), "prefixSha256": sha(raw),
        "prefix": prefix, "status": snapshot, "context": context, "memory": memory,
        "freeRamBytes": resource.available_ram(), "assessment": assessment,
        "tool": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
        "scopeTool": {"path": str(scope_path), "sha256": SCOPE_SHA},
    }
    print(json.dumps(freeze_json(out / f"{record['run']}-admission.json", result)))
    print(frozen(Path(record["kickoff"]["path"])).decode("ascii"))


if __name__ == "__main__":
    admit(Path(sys.argv[1]), Path(sys.argv[2]))
