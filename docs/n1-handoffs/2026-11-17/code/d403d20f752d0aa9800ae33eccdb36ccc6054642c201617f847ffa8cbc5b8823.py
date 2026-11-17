"""Preserve real context-held and prematurely selected initials without accepting either."""
import json
from pathlib import Path

from b130_context_held_initials import archive_excluded as archive_context_hold
from common import frozen, require, sha


def require_premature_hold(held, phase, audit, batch, candidate):
    require(batch == 130 and held["batch"] == phase["batch"] == batch
            and held["run"] == phase["run"] == "N1-B130-CLAUDE-002"
            and held["candidate"] == phase["candidate"] == candidate
            and held["session"] == phase["session"] == audit["session"]
            and held["status"] == "VOID_PREMATURE_SELECTION"
            and held["reviewAccepted"] is False and held["finalAcceptance"] is False
            and held["report"] is None
            and phase["status"] == audit["status"] == "VOID"
            and phase["breaches"] == audit["breaches"] == ["Selection sent before complete core coverage"]
            and phase["coreRead"] == audit["coreRead"] == 79
            and phase["coreRequired"] == audit["coreRequired"] == 87
            and phase["readyForPhase2"] is False
            and phase["context"]["status"] == "PASS"
            and phase["context"]["errors"] == phase["context"]["compactions"] == []
            and held["audit"]["sha256"] == phase["auditSha256"]
            and held["events"]["sha256"] == phase["eventsSha256"] == audit["eventsSha256"]
                == phase["context"]["eventsSha256"]
            and held["preflight"]["sha256"] == phase["preflightSha256"]
            and audit["reviewerIdle"] and audit["bootstrapVerified"]
            and not audit["recordIncomplete"] and audit["unexpectedUserMessages"] == 0
            and audit["fetches"] == audit["writes"] == audit["readbacks"] == audit["extensionRead"] == 0
            and len(audit["messages"]) == 1
            and phase["phase1ListSha256"] == audit["phase1ListSha256"],
            "Excluded initial is not its recorded premature-selection execution")


def archive_excluded(paths, batch, candidate, accepted_runs, copy, binding, dump, chain,
                     audit_support, records):
    excluded = []
    for path in paths:
        path = Path(path)
        held = json.loads(frozen(path))
        disallowed = set(accepted_runs) | {item["run"] for item in excluded}
        if held["status"] != "VOID_PREMATURE_SELECTION":
            excluded.extend(archive_context_hold(
                [path], batch, candidate, disallowed, copy, binding, dump, chain, audit_support, records))
            continue
        read = lambda item: json.loads(frozen(item["path"], item["sha256"]))
        phase, audit = read(held["phase1"]), read(held["audit"])
        require_premature_hold(held, phase, audit, batch, candidate)
        frozen(held["events"]["path"], held["events"]["sha256"])
        require(Path(held["audit"]["path"]) == Path(phase["auditDir"]) / "audit.json",
                "Excluded phase1 audit path differs")
        run = held["run"]
        require(run not in disallowed, "An excluded run cannot also be accepted or duplicated")
        preflight = read(held["preflight"])
        spec = preflight["runs"]["claude"]
        require(spec["run"] == run and held["preflight"]["path"] == phase["preflight"],
                "Excluded preflight identity differs")
        config_path = Path(spec["auditConfig"])
        config = json.loads(frozen(config_path))
        require(config["run"] == run and config["report"] == spec["report"]
                and config["coreManifest"] == held["core"]["path"]
                and not Path(spec["report"]).exists()
                and all(not (records / f"{run}-{suffix}").exists() for suffix in (
                    "acceptance.json", "extension.json", "phase2-message.txt", "final.json")),
                "Premature run advanced or changed its input binding")
        for item in config["files"]:
            frozen(item["path"], item["sha256"])
        frozen(held["core"]["path"], held["core"]["sha256"])
        launch = json.loads(frozen(records / f"{run}-launch.json"))
        require(launch["session"] == held["session"] and launch["run"] == run,
                "Excluded launch identity differs")
        prefix = f"excluded-initials/{run}"
        copy(path, f"{prefix}/hold.json")
        for key in ("phase1", "preflight"):
            binding(held[key], f"{prefix}/{key}.json")
        for key, item in held["failureExecution"].items():
            binding(item, f"{prefix}/failed-execution/{key}")
        dump(f"{prefix}/audit-summary.json", audit_support.bounded_audit(Path(held["audit"]["path"])))
        for suffix in ("launch", "admission"):
            copy(records / f"{run}-{suffix}.json", f"{prefix}/{suffix}.json")
        copy(config_path, f"{prefix}/config.json")
        for field in ("prompt", "kickoff"):
            copy(Path(config[field]), f"{prefix}/{field}.txt")
        excluded.append({
            "run": run, "session": held["session"], "snapshot": candidate, "status": held["status"],
            "rawVerdict": None, "reviewAccepted": False, "finalAcceptance": False,
            "holdSha256": sha(frozen(path)), "eventsSha256": held["events"]["sha256"],
            "coreRead": audit["coreRead"], "coreRequired": audit["coreRequired"],
            "chains": [chain(Path(config["coreManifest"]), f"{prefix}/chain")],
            "limits": "Incomplete core read. No phase2, extension or report exists. "
                      "The complete frozen input chain is preserved, not represented as fully read.",
        })
    return excluded
