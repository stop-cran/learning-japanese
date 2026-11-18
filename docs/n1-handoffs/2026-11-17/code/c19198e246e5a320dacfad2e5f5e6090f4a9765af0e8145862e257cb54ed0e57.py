"""Bind B133 original-reviewer confirmations to the actual initial evidence and signed snapshot.

build SPEC freezes the chain, prompt, kickoff, config and preflight; admit PREFLIGHT STATUS ROSTER
freezes actual app-saved full status/roster outputs, checks the fresh serial gate and freezes the
reviewer's pre-delivery event prefix; final PREFLIGHT audits the actual post-kickoff slice. None of
these steps is substantive acceptance.
"""
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

from admit_b133_source_reconciliation import INITIALS, P, PREFLIGHT
from b133_closure_records import collect_initial_record
from b133_confirmation_capacity import confirmation_cost
from b133_confirmation_records import disposition_ids
from b133_fresh_confirmation_v2 import REASON, fresh_bindings, fresh_origin, replacement_prompt
from common import COORDINATOR, WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen
from run_b133_closure_checks import CANDIDATE, MEMBERS, REPO, lineage
from verify_b133_packet import RUNNER
from verify_b133_sources import Git

ROOT = WS / "scratch-133" / "review"
OUT = ROOT / "confirmation-002"
ADMISSION_INPUTS = ROOT / "confirmation-admission-inputs"
REPORTS = WS / "reports-133"
PROTOCOL = P / "protocol-003"
sys.path.insert(0, str(PROTOCOL))
from b133_capacity import PROFILES, telemetry  # noqa: E402
from b133_runtime import verify_chain  # noqa: E402
from review_chain import build_chain  # noqa: E402

SPEC_FIELDS = {"family", "run", "session", "candidate", "teachingChange", "scope", "revisedSources",
               "additionalSources", "basis", "priorVerdict", "basisText", "originalSession",
               "contextObservation"}
TOOLS = ("renderer.py", "audit-confirm.py", "check-confirm-structure.py")
PROTOCOL_MODULES = ("review_chain.py", "review_chain_with_optional.py", "b133_capacity.py",
                    "b133_runtime.py", "b133_common.py")
DRIFT_ALLOWANCE, REPORT_ALLOWANCE, STARTUP_GATE, PROMPT_LIMIT = 12000, 30000, 700000, 40000


def binding(path, digest=None):
    return {"path": str(path), "sha256": sha(frozen(path, digest))}


def safe_relative(name):
    path = Path(name)
    require(isinstance(name, str) and name and not path.is_absolute() and ".." not in path.parts
            and "\\" not in name, f"Unsafe source name: {name!r}")
    return name


def validate_spec(spec):
    require(set(spec) == SPEC_FIELDS, "Unexpected or missing confirmation spec fields")
    family = spec["family"]
    require(family in INITIALS and fresh_origin(spec),
            "Fresh confirmation must disclose its original reviewer")
    require(re.fullmatch("N1-B133-" + family.upper() + r"-CONFIRM-[0-9]{3}", spec["run"]), "Invalid run")
    require(re.fullmatch(r"[0-9a-f]{40}", spec["candidate"]), "Use the full snapshot identity")
    require(type(spec["teachingChange"]) is bool
            and (spec["teachingChange"] or spec["candidate"] == CANDIDATE),
            "A no-change confirmation must use the reviewed candidate")
    scope = spec["scope"]
    require(isinstance(scope, list) and scope and len(scope) == len(set(scope)) and set(scope) <= set(MEMBERS),
            "Scope must name distinct B133 members")
    revised = [safe_relative(name) for name in spec["revisedSources"]]
    require(len(revised) == len(set(revised)) and {f"kanji/{char}.md" for char in scope} <= set(revised),
            "Every scoped card must be supplied from the actual snapshot")
    names = [safe_relative(item["source"]) for item in spec["additionalSources"]]
    require(all(set(item) == {"source", "path", "sha256"} and re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
                for item in spec["additionalSources"]) and len(names) == len(set(names)),
            "Invalid additional source binding")
    require(spec["basis"] == "adjudicated-initial"
            and spec["priorVerdict"] == INITIALS[family]["verdict"]
            and isinstance(spec["basisText"], str) and spec["basisText"].strip()
            and "B132" not in spec["basisText"], "Invalid confirmation basis")
    return family


def initial(family, session):
    require(family in INITIALS and INITIALS[family]["session"] == session,
            "Confirmation must use its original reviewer")
    known = INITIALS[family]
    run = "N1-B133-" + family.upper() + "-001"
    spec = {
        "family": family, "run": run, "role": "initial", "session": session, "snapshot": CANDIDATE,
        "verdict": known["verdict"],
        "acceptance": {"path": str(P / (run + "-acceptance.json")), "sha256": known["acceptance"]},
    }
    final = {"path": str(P / (run + "-final.json")), "sha256": known["final"]}
    refs, _, claims = collect_initial_record(spec, PREFLIGHT, final, frozen)
    require(claims == known["claims"], "Initial consequential claims differ")
    original = frozen(refs["report"]["path"], refs["report"]["sha256"])
    return refs, original, disposition_ids(original, claims)


def context(raw, family):
    require(raw.endswith(b"\n"), "Incomplete event record")
    events = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    result = telemetry(events, None, family)
    require(result["status"] == "PASS", "Original-reviewer context failed: " + repr(result["errors"]))
    return {**result, "eventsSha256": sha(raw)}


def capacity(observed, chain, prompt_bytes):
    require(observed["status"] == "PASS" and chain["segments"] and type(prompt_bytes) is int
            and 0 < prompt_bytes <= PROMPT_LIMIT, "Missing or unbudgeted capacity inputs")
    measured = confirmation_cost(chain)
    total = measured["chainBytes"]
    peak = observed["lastInputTokens"] + measured["tokens"] + prompt_bytes + DRIFT_ALLOWANCE + REPORT_ALLOWANCE
    limit = min(STARTUP_GATE, PROFILES[observed["family"]]["maxPromptTokens"])
    require(peak < limit, f"Confirmation capacity exceeded: {peak} >= {limit}")
    return {
        "status": "PASS_PRE_CONFIRMATION_CAPACITY", "lastInputTokens": observed["lastInputTokens"],
        "chainBytes": total, "promptBytes": prompt_bytes, "driftAllowance": DRIFT_ALLOWANCE,
        "reportAllowance": REPORT_ALLOWANCE, "projectedPeak": peak, "gate": limit,
        "estimatedChainTokens": measured["tokens"], "calibration": measured,
        "method": measured["method"],
    }


def clean(git, candidate, teaching_change):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate), "Use full snapshot identity")
    require(git("rev-parse", "HEAD").decode().strip() == candidate
            and not git("status", "--porcelain=v1", "--untracked-files=all"),
            "Confirmation snapshot is not the clean checkout")
    depth = lineage(git, candidate)
    require(depth > 0 if teaching_change else (candidate == CANDIDATE and depth == 0),
            "Declared teaching change differs from the actual owner-signed lineage")
    return depth


def destination(report):
    report = Path(report)
    require(report.parent == REPORTS and report.suffix == ".md" and not report.exists(),
            "Invalid/existing report")
    REPORTS.mkdir(exist_ok=True)
    probe = report.with_suffix(".probe")
    with probe.open("xb") as stream:
        stream.write(b"B133 report readiness\n")
    try:
        require(probe.read_bytes() == b"B133 report readiness\n", "Report readback failed")
    finally:
        probe.unlink()


def render(spec, original_ref, chain, prompt_path, report, ids):
    renderer = load_module("b133_confirmation_renderer_actual", OUT / "renderer.py")
    packet = {"candidate": spec["candidate"], "freeze": CANDIDATE,
              "originalReport": original_ref["path"], "report": str(report)}
    text = replacement_prompt(renderer.render_prompt({**spec, "dispositionIds": ids}, packet, chain,
                                                     prompt_path), spec)
    require(text.count(spec["basisText"].rstrip("\n")) == 1 and "B132" not in text,
            "Rendered basis differs")
    return text.encode("utf-8")


def add_binding(bindings, ref):
    ref = {"path": str(ref["path"]), "sha256": ref["sha256"]}
    known = {row["path"]: row["sha256"] for row in bindings}
    require(known.get(ref["path"], ref["sha256"]) == ref["sha256"], "Conflicting input binding")
    if ref["path"] not in known:
        bindings.append(ref)


def no_change_record(candidate):
    return (json.dumps({
        "reviewedFreeze": CANDIDATE, "confirmationSnapshot": candidate, "teachingDelta": "none",
        "verification": "Clean checkout at the reviewed candidate; no owner-signed descendant commit.",
    }, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def build(spec_path):
    spec_raw = frozen(spec_path)
    spec = json.loads(spec_raw)
    family = validate_spec(spec)
    run, candidate = spec["run"], spec["candidate"]
    require(not (OUT / (run + "-preflight.json")).exists(), "Preserve existing preflight")
    refs, original, ids = initial(family, spec["originalSession"])
    report = REPORTS / (run + ".md")
    destination(report)
    sources = [("initial-report/" + Path(refs["report"]["path"]).name, original, None)]
    bindings = []
    for ref in ({"path": str(spec_path), "sha256": sha(spec_raw)}, *refs.values(), *fresh_bindings(spec)):
        add_binding(bindings, ref)
    guard, _ = start_guard(run + " preparation")
    try:
        git = Git(REPO, RUNNER, guard)
        depth = clean(git, candidate, spec["teachingChange"])
        if spec["teachingChange"]:
            delta = git("diff", "--no-color", CANDIDATE, candidate, "--", ".",
                        ":(exclude)manifest.json", ":(exclude)docs")
            require(delta, "Missing teaching delta")
            add_binding(bindings, write_frozen(OUT / run / "fix.patch", delta))
            sources.append(("diffs/fix.patch", delta, None))
        else:
            require(not git("diff", "--no-color", CANDIDATE, candidate), "Unexpected delta")
            record = no_change_record(candidate)
            add_binding(bindings, write_frozen(OUT / run / "no-change.json", record))
            sources.append(("diffs/no-change.json", record, None))
        for name in spec["revisedSources"]:
            raw = git("show", candidate + ":" + name)
            require(raw == (REPO / name).read_bytes(), "Snapshot differs")
            add_binding(bindings, write_frozen(OUT / run / "snapshot" / name, raw))
            sources.append(("snapshot/" + name, raw, None))
        for item in spec["additionalSources"]:
            raw = frozen(item["path"], item["sha256"])
            add_binding(bindings, item)
            sources.append((item["source"], raw, None))
        require(len(sources) == len({row[0] for row in sources}), "Duplicate source")
        chain_path = OUT / (run + "-chain.json")
        chain = build_chain(sources, WS / "review-chains" / run.lower(), chain_path, guard, run)
        chain_cost = verify_chain(chain, sources)
        prompt_path, kickoff_path = (OUT / (run + "-" + suffix + ".txt") for suffix in ("prompt", "kickoff"))
        prompt = render(spec, refs["report"], chain, prompt_path, report, ids)
        kickoff = (f"Read {prompt_path} using one view call with forceReadLargeFiles: true and no view_range, "
                   "then follow its instructions. No other tool call may precede that read.").encode("ascii")
        for ref in (write_frozen(prompt_path, prompt), write_frozen(kickoff_path, kickoff),
                    binding(chain_path), binding(Path(__file__)),
                    binding(Path(__file__).with_name("b133_confirmation_capacity.py")),
                    binding(P / "tools" / "capacity004.py"),
                    binding(P / "tools" / "capacity004_units.py"),
                    *(binding(OUT / name) for name in TOOLS),
                    *(binding(PROTOCOL / name) for name in PROTOCOL_MODULES)):
            add_binding(bindings, ref)
        config = {
            "run": run, "candidate": candidate, "prompt": str(prompt_path), "kickoff": str(kickoff_path),
            "report": str(report), "coordinator": COORDINATOR, "expectedFamily": family,
            "chainManifest": str(chain_path), "completionContract": "entire-message-enum-v1",
            "reportStructureContract": "confirm-structure-v1", "dispositionIds": ids,
            "maxWebFetches": 0, "files": bindings,
        }
        config_ref = freeze_json(OUT / (run + "-config.json"), config)
        events = Path.home() / ".copilot" / "session-state" / spec["session"] / "events.jsonl"
        forecast = capacity(context(events.read_bytes(), family), chain, len(prompt))
        require(clean(git, candidate, spec["teachingChange"]) == depth, "Snapshot changed during build")
        record = {
            "originalSession": spec["originalSession"], "replacementReason": REASON,
            "contextObservation": spec["contextObservation"],
            "batch": 133, "run": run, "session": spec["session"], "candidate": candidate,
            "teachingChange": spec["teachingChange"], "lineageDepth": depth,
            "config": config_ref, "kickoff": binding(kickoff_path), "chain": binding(chain_path),
            "segments": len(chain["segments"]), "sources": len(sources), "chainCost": chain_cost,
            "capacity": forecast, "dispositionIds": ids,
            "initialReport": refs["report"], "initialAcceptance": refs["acceptance"],
            "preparedOnly": True, "publicationAccepted": False,
        }
        print(json.dumps(freeze_json(OUT / (run + "-preflight.json"), record)))
    finally:
        require(not guard.finish()["breach"], "Confirmation preparation RAM breach")


def preflight(path):
    record = json.loads(frozen(path))
    config = json.loads(frozen(record["config"]["path"], record["config"]["sha256"]))
    require(record["batch"] == 133 and record["run"] == config["run"]
            and record["candidate"] == config["candidate"], "Preflight identity differs")
    for item in config["files"]:
        frozen(item["path"], item["sha256"])
    chain = json.loads(frozen(config["chainManifest"], record["chain"]["sha256"]))
    for segment in chain["segments"]:
        frozen(segment["path"], segment["sha256"])
    return record, config, chain


def check_snapshot(status, roster, session, observed, now):
    rows = status["sessions"]
    ids, roster_ids = [row["id"] for row in rows], [row["id"] for row in roster]
    require(rows and status["summary"]["total"] == len(rows) == len(roster)
            and len(set(ids)) == len(ids) and len(set(roster_ids)) == len(roster_ids)
            and set(ids) == set(roster_ids) and COORDINATOR in ids,
            "Incomplete, duplicate or mismatched app snapshots")
    require(observed.tzinfo is not None and now.tzinfo is not None
            and 0 <= (now - observed).total_seconds() < 120, "Stale or future observation")
    for row in rows:
        if row["id"] != COORDINATOR:
            require(row.get("activity", {}).get("status") == "idle" and row.get("is_running") is False
                    and not row.get("awaiting_user_input") and not row.get("awaiting_plan_approval"),
                    f"Session is not idle and unblocked: {row['id']}")
    matches = [row for row in rows if session in (row["id"], row.get("active_session_id"))]
    require(len(matches) == 1, "Original reviewer missing or ambiguous in the full snapshot")
    return len(rows)


def observed_at(paths):
    stamps = []
    for path in paths:
        match = re.fullmatch(r"([0-9]{13})-copilot-tool-output-[0-9a-f]+\.txt", Path(path).name)
        require(match, "Use actual app-saved full tool output")
        stamps.append(int(match[1]))
    return min(stamps), datetime.datetime.fromtimestamp(min(stamps) / 1000, datetime.timezone.utc)


def freeze_request(run, status_output, roster_output):
    stamp, observed = observed_at((status_output, roster_output))
    status = json.loads(Path(status_output).read_bytes())
    roster_raw = Path(roster_output).read_bytes()
    roster = json.loads(roster_raw[roster_raw.index(b"["):])
    output = ADMISSION_INPUTS / f"{run}-{stamp}"
    require(not output.exists(), "Preserve previous admission input")
    status_ref = freeze_json(output / "status.json", status)
    roster_ref = freeze_json(output / "roster.json", roster)
    write_frozen(output / "original-roster-output.txt", roster_raw)
    request_path = output / "request.json"
    freeze_json(request_path, {"statusPath": status_ref["path"], "rosterPath": roster_ref["path"],
                               "observedAt": observed.isoformat()})
    return request_path


def admit(path, status_output, roster_output):
    record, config, chain = preflight(path)
    run = record["run"]
    require(not (OUT / (run + "-admission.json")).exists(), "Preserve existing admission")
    request_path = freeze_request(run, status_output, roster_output)
    request = json.loads(frozen(request_path))
    status, roster = (json.loads(frozen(request[key])) for key in ("statusPath", "rosterPath"))
    observed = datetime.datetime.fromisoformat(request["observedAt"])
    count = check_snapshot(status, roster, record["session"], observed,
                           datetime.datetime.now(datetime.timezone.utc))
    guard, resource = start_guard(run + " admission")
    try:
        clean(Git(REPO, RUNNER, guard), record["candidate"], record["teachingChange"])
        destination(config["report"])
        events = Path.home() / ".copilot" / "session-state" / record["session"] / "events.jsonl"
        raw = events.read_bytes()
        observed_context = context(raw, config["expectedFamily"])
        forecast = capacity(observed_context, chain, len(frozen(config["prompt"])))
        prefix = write_frozen(OUT / (run + "-pre-delivery-events.jsonl"), raw)
        now = datetime.datetime.now(datetime.timezone.utc)
        check_snapshot(status, roster, record["session"], observed, now)
        require(resource.available_ram() > 2 * 1024**3, "Startup RAM floor no longer met")
        result = {
            **record, "admitted": True, "admittedAt": now.isoformat(),
            "observedAt": request["observedAt"], "sessionCount": count, "offset": len(raw),
            "prefixSha256": sha(raw), "prefix": prefix, "status": binding(request["statusPath"]),
            "roster": binding(request["rosterPath"]), "request": binding(request_path),
            "context": observed_context, "capacity": forecast, "freeRamBytes": resource.available_ram(),
        }
        print(json.dumps(freeze_json(OUT / (run + "-admission.json"), result)))
        print(frozen(config["kickoff"]).decode("ascii"))
    finally:
        require(not guard.finish()["breach"], "Confirmation admission RAM breach")


def final(path):
    record, config, _ = preflight(path)
    run = record["run"]
    admission = json.loads(frozen(OUT / (run + "-admission.json")))
    guard, _ = start_guard(run + " final")
    try:
        command = [sys.executable, "-B", str(OUT / "audit-confirm.py"), "--session", record["session"],
                   "--config", record["config"]["path"], "--offset", str(admission["offset"]),
                   "--prefix-sha256", admission["prefixSha256"], "--final"]
        child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=REPO)
        stdout, stderr = Git(REPO, RUNNER, guard).wait(child)
        write_frozen(OUT / (run + "-final-execution.txt"), stdout + stderr)
        match = re.search(r"^Audit: (.+)$", stdout.decode("utf-8"), re.M)
        require(child.returncode == 0 and match, (stdout + stderr).decode("utf-8", "replace"))
        audit_path = Path(match[1].strip())
        audit = json.loads(frozen(audit_path))
        require(audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and not audit["breaches"]
                and audit["reviewerIdle"] and audit["unexpectedUserMessages"] == audit["fetches"] == 0
                and audit["chainRead"] == audit["chainRequired"]
                and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
                and len(audit["messages"]) == 1, "Confirmation execution is not admissible")
        context_record = context(frozen(audit_path.parent / "events.jsonl", audit["eventsSha256"]),
                                 config["expectedFamily"])
        report = Path(config["report"])
        report.chmod(0o444)
        checker = load_module("b133_confirm_structure_actual", OUT / "check-confirm-structure.py")
        structure = checker.check(frozen(report).decode("utf-8"), run, record["candidate"],
                                  config["dispositionIds"], json.loads(frozen(config["chainManifest"])),
                                  audit["messages"][0])
        result = {
            "run": run, "batch": 133, "candidate": record["candidate"], "session": record["session"],
            "originalSession": record["originalSession"], "replacementReason": record["replacementReason"],
            "audit": binding(audit_path), "context": freeze_json(OUT / (run + "-context.json"), context_record),
            "structure": freeze_json(OUT / (run + "-structure.json"), structure),
            "report": binding(report), "confirmation": structure["confirmation"],
            "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            if structure["status"] == "PASS" else "HOLD",
        }
        print(json.dumps(freeze_json(OUT / (run + "-final.json"), result)))
        require(result["status"] != "HOLD", "Confirmation report structure failed")
    finally:
        require(not guard.finish()["breach"], "Confirmation final RAM breach")


if __name__ == "__main__":
    action, *arguments = sys.argv[1:]
    if action == "build" and len(arguments) == 1:
        build(Path(arguments[0]))
    elif action == "admit" and len(arguments) == 3:
        admit(Path(arguments[0]), Path(arguments[1]), Path(arguments[2]))
    elif action == "final" and len(arguments) == 1:
        final(Path(arguments[0]))
    else:
        raise SystemExit("build SPEC | admit PREFLIGHT STATUS_OUTPUT ROSTER_OUTPUT | final PREFLIGHT")
