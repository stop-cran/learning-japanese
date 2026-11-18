"""Preserve a diagnosed phase-two VOID without accepting or relabelling its report."""
import json
import re
from pathlib import Path

from closure_initials import archive_excluded as archive_structure_holds
from common import frozen, require, sha

STATUS = "VOID_COORDINATOR_PHASE2_DELIVERY_MISMATCH"

def bounded_void_audit(path):
    raw = frozen(path)
    original = json.loads(raw)
    require(original["status"] == "VOID" and original["breaches"]
            and original["final"] and original["reviewerIdle"]
            and not original["recordIncomplete"], "Not a completed VOID audit")
    fields = ("session", "eventsSha256", "eventsBytes", "eventsCount", "status", "breaches",
              "bootstrapVerified", "actualResponseModels", "reviewerIdle", "recordIncomplete",
              "final", "unexpectedUserMessages", "coreRead", "coreRequired", "extensionRead",
              "extensionRequired", "writes", "readbacks", "readbackVerified", "fetches")
    result = {key: original[key] for key in fields if key in original}
    result.update(originalAuditSha256=sha(raw), rawExecutionPayloadsRemainLocal=True,
                  reviewAccepted=False, publicationAccepted=False)
    result["calls"] = [
        {key: call[key] for key in ("id", "name", "event", "phase", "timestamp", "role", "success")
         if key in call} for call in original["calls"]
    ]
    return result



def require_phase2_void(quarantine, mechanics, audit, context, structure, diagnosis, batch, candidate):
    run, session = quarantine["run"], quarantine["session"]
    require(re.fullmatch(rf"N1-B{batch}-(CLAUDE|GPT)-\d{{3}}", run)
            and quarantine["status"] == STATUS
            and quarantine["reviewAccepted"] is False
            and quarantine["publicationAccepted"] is False
            and quarantine["candidate"] == mechanics["candidate"] == candidate
            and mechanics["batch"] == batch
            and mechanics["run"] == diagnosis["run"] == run
            and mechanics["session"] == audit["session"] == session,
            "Quarantine identity, status or nonacceptance differs")
    require(mechanics["status"] == "HOLD" and mechanics["problems"]
            and audit["status"] == "VOID" and audit["breaches"]
            and audit["final"] and audit["reviewerIdle"] and not audit["recordIncomplete"]
            and audit["unexpectedUserMessages"] == 1
            and context["status"] == structure["status"] == "PASS"
            and not context["compactions"],
            "Not a completed protocol-VOID execution with passing context and structure")
    require(all(quarantine["audit"][key] == mechanics["finalAudit"][key]
                for key in ("path", "sha256"))
            and quarantine["audit"]["eventsSha256"] == audit["eventsSha256"]
            == context["eventsSha256"] == diagnosis["eventsSha256"],
            "Quarantine audit or event bindings differ")
    messages = diagnosis["userMessages"]
    expected = diagnosis["expectedPhase2Message"]
    require(diagnosis["phase2ExactMatch"] is False and len(messages) == 2
            and expected.count("\n") == 1 and expected.endswith("\nMissing entries: none")
            and messages[1]["content"] == expected.split("\n")[0],
            "Recorded failure is not the omitted phase-two second line")


def archive_excluded(paths, batch, candidate, accepted_runs, copy, binding, dump, chain,
                     audit_support, records):
    excluded = []
    for source in paths:
        path = Path(source)
        quarantine = json.loads(frozen(path))
        run = quarantine["run"]
        used = accepted_runs | {item["run"] for item in excluded}
        require(run not in used, "An excluded run cannot also be accepted or duplicated")
        if quarantine["status"] == "HOLD_STRUCTURE_FAILED":
            excluded.extend(archive_structure_holds(
                [path], batch, candidate, used, copy, binding, dump, chain, audit_support, records))
            continue
        read = lambda item: json.loads(frozen(item["path"], item["sha256"]))
        mechanics = read(quarantine["final"])
        audit = read(quarantine["audit"])
        context, structure = (read(mechanics[field]) for field in ("context", "structure"))
        diagnosis = read(quarantine["diagnosis"])
        require_phase2_void(quarantine, mechanics, audit, context, structure, diagnosis, batch, candidate)
        prefix = f"excluded-initials/{run}"
        copy(path, f"{prefix}/quarantine.json")
        for field in ("report", "final", "diagnosis"):
            binding(quarantine[field], f"{prefix}/{field}.{'md' if field == 'report' else 'json'}")
        for field in ("structure", "context"):
            binding(mechanics[field], f"{prefix}/{field}.json")
        dump(f"{prefix}/audit-summary.json",
             bounded_void_audit(Path(quarantine["audit"]["path"])))
        for suffix in ("phase1", "launch", "admission"):
            copy(records / f"{run}-{suffix}.json", f"{prefix}/{suffix}.json")
        launch = json.loads(frozen(records / f"{run}-launch.json"))
        require(launch["session"] == quarantine["session"], "Excluded launch identity differs")
        config_path = records / "prompts" / f"audit-config-{run}.json"
        config = json.loads(frozen(config_path))
        require(config["run"] == run and config["report"] == quarantine["report"]["path"],
                "Excluded config/report mismatch")
        for item in config["files"]:
            frozen(item["path"], item["sha256"])
        copy(config_path, f"{prefix}/config.json")
        for field in ("prompt", "kickoff"):
            copy(config[field], f"{prefix}/{field}.txt")
        phase2 = records / f"{run}-phase2-message.txt"
        require(frozen(phase2).decode("utf-8") == diagnosis["expectedPhase2Message"],
                "Frozen phase-two message differs from diagnosis")
        copy(phase2, f"{prefix}/phase2-message.txt")
        chains = [chain(Path(config["coreManifest"]), f"{prefix}/chain"),
                  chain(records / f"{run}-extension.json", f"{prefix}/extension")]
        excluded.append({
            "run": run, "session": quarantine["session"], "snapshot": candidate,
            "status": quarantine["status"], "rawVerdict": structure["overall"],
            "reviewAccepted": False, "finalAcceptance": False,
            "quarantineSha256": sha(frozen(path)), "chains": chains,
            "eventsSha256": audit["eventsSha256"],
            "limits": "Preserved failed evidence only. Its report, verdict and observations "
                      "are not accepted review evidence or reconciliation inputs.",
        })
    return excluded
