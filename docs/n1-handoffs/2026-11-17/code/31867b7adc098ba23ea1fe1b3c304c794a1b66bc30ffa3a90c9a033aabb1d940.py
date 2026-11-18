"""Bind B132 delta confirmations to the actual original-reviewer evidence."""
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

from b131_confirmation_routing_001 import check_roster
from b132_closure_records_v2 import collect_initial_record
from common import COORDINATOR, WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen
from run_b132_closure_checks import CANDIDATE, REPO, lineage
from verify_b132_packet import RUNNER
from verify_b132_sources import Git

ROOT = WS / "scratch-132" / "review"
OUT = ROOT / "confirmation-001"
PREP = ROOT / "neutral-preparation-002"
PROTOCOL = PREP / "protocol-001"
PREFLIGHT = PREP / "audit-configs-001" / "preflight.json"
PREFLIGHT_SHA = "c790a53590a8b6691c87a9d1290b5d0c914eb99c24e49eca2c1f394f9016e18f"
INITIALS = {
    "claude": {
        "session": "44f1f88b-5d6d-496a-8de6-8d5af486c486", "verdict": "CLEAN",
        "acceptanceSha256": "077281b32383186dccfcfcbc68703f31e512bddfaa9b8ef0319872f03f4ebda9",
        "finalSha256": "5958c14b3b5c38523832b0f4a903d26ff687ebefdbcf97a2e472438e0e156d44",
    },
    "gpt": {
        "session": "5aca1016-ad24-4875-9509-f3ffbe4ebe9c", "verdict": "UNVERIFIED",
        "acceptanceSha256": "bef20c8db081b8f7344f82ca995f463f090da16c22e9fa265e0f72cf11dd1ca4",
        "finalSha256": "8efeddfe5a024be4b1568af34b5c21d4d2cce620eff7db370e71150655d18130",
    },
}
sys.path.insert(0, str(PROTOCOL))
from b132_capacity import PROFILES, telemetry
from b132_runtime import verify_chain
from review_chain import build_chain


def binding(path, digest=None):
    return {"path": str(path), "sha256": sha(frozen(path, digest))}


def initial(family, session):
    require(family in INITIALS and INITIALS[family]["session"] == session,
            "Confirmation must use its original reviewer")
    known = INITIALS[family]
    run = "N1-B132-" + family.upper() + "-001"
    spec = {
        "family": family, "run": run, "role": "initial", "session": session,
        "snapshot": CANDIDATE, "verdict": known["verdict"],
        "acceptance": binding(PREP / (run + "-acceptance.json"), known["acceptanceSha256"]),
    }
    refs, _, claims = collect_initial_record(
        spec, binding(PREFLIGHT, PREFLIGHT_SHA),
        binding(PREP / (run + "-final.json"), known["finalSha256"]), frozen)
    original = frozen(refs["report"]["path"], refs["report"]["sha256"])
    ids = re.findall(r"(?m)^### ([FO]\d+):", original.decode("utf-8"))
    ids += claims["openClaimIds"] + claims["coordinatorClaimIds"]
    require(len(ids) == len(set(ids)), "Ambiguous disposition identity")
    return refs, original, ids


def context(raw, family):
    require(raw.endswith(b"\n"), "Incomplete event record")
    events = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    result = telemetry(events, None, family)
    require(result["status"] == "PASS", "Original-reviewer context failed: " + repr(result["errors"]))
    return {**result, "eventsSha256": sha(raw)}


def capacity(observed, chain, prompt_bytes):
    require(observed["status"] == "PASS" and chain["segments"], "Missing actual capacity inputs")
    total = sum(row["bytes"] for row in chain["segments"])
    peak = observed["lastInputTokens"] + total + prompt_bytes + 12000 + 30000
    limit = min(700000, PROFILES[observed["family"]]["maxPromptTokens"])
    require(peak < limit, f"Confirmation capacity exceeded: {peak} >= {limit}")
    return {
        "status": "PASS_PRE_CONFIRMATION_CAPACITY", "lastInputTokens": observed["lastInputTokens"],
        "chainBytes": total, "promptBytes": prompt_bytes, "driftAllowance": 12000,
        "reportAllowance": 30000, "projectedPeak": peak, "gate": limit,
        "method": "Conservative one estimated token per rendered byte; live telemetry still required.",
    }


def clean(git, candidate):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate), "Use full snapshot identity")
    require(git("rev-parse", "HEAD").decode().strip() == candidate
            and not git("status", "--porcelain=v1", "--untracked-files=all"),
            "Confirmation snapshot is not the clean checkout")
    require(lineage(git, candidate) > 0, "This protocol requires an owner-signed reconciliation")


def destination(report):
    report = Path(report)
    require(report.parent == WS / "reports-132" and not report.exists(), "Invalid/existing report")
    probe = report.with_suffix(".probe")
    with probe.open("xb") as stream:
        stream.write(b"B132 report readiness\n")
    try:
        require(probe.read_bytes() == b"B132 report readiness\n", "Report readback failed")
    finally:
        probe.unlink()


def render(spec, original_ref, chain, prompt_path, report):
    renderer = load_module("b132_confirmation_renderer_actual", OUT / "renderer.py")
    packet = {
        "candidate": spec["candidate"], "freeze": CANDIDATE,
        "originalReport": original_ref["path"], "report": str(report),
    }
    text = renderer.render_prompt(spec, packet, chain, prompt_path)
    if spec["family"] == "gpt":
        old = ("Your initial report remains UNVERIFIED and held for open claims, not accepted "
               "as a completed full-card review.")
        new = ("Your initial report was methodologically accepted as UNVERIFIED, not as teaching "
               "approval. Its consequential claims Q1/Q2 remain open.")
        require(text.count(old) == 1, "Unexpected renderer wording")
        text = text.replace(old, new)
        old = "The prior report and its hold are not rewritten or replaced by a claim of earlier acceptance."
        new = "The prior report and its unresolved status are preserved; this is not a rewritten initial pass."
        require(text.count(old) == 1, "Unexpected initial-status wording")
        text = text.replace(old, new)
    return text.encode("utf-8")


def build(spec_path):
    spec = json.loads(frozen(spec_path))
    family, run, candidate = spec["family"], spec["run"], spec["candidate"]
    require(re.fullmatch("N1-B132-" + family.upper() + r"-CONFIRM-[0-9]{3}", run), "Invalid run")
    refs, original, ids = initial(family, spec["session"])
    report = WS / "reports-132" / (run + ".md")
    destination(report)
    sources = [("initial-report/" + Path(refs["report"]["path"]).name, original, None)]
    bindings = [binding(spec_path), *refs.values()]
    guard, _ = start_guard(run + " preparation")
    try:
        git = Git(REPO, RUNNER, guard)
        clean(git, candidate)
        delta = git("diff", "--no-color", CANDIDATE, candidate, "--", ".",
                    ":(exclude)manifest.json", ":(exclude)docs")
        require(delta, "Missing teaching delta")
        bindings.append(write_frozen(OUT / run / "fix.patch", delta))
        sources.append(("diffs/fix.patch", delta, None))
        for name in spec["revisedSources"]:
            require(not Path(name).is_absolute() and ".." not in Path(name).parts, "Unsafe source")
            raw = git("show", candidate + ":" + name)
            require(raw == (REPO / name).read_bytes(), "Snapshot differs")
            bindings.append(write_frozen(OUT / run / "snapshot" / name, raw))
            sources.append(("snapshot/" + name, raw, None))
        for item in spec["additionalSources"]:
            raw = frozen(item["path"], item["sha256"])
            bindings.append({"path": item["path"], "sha256": item["sha256"]})
            sources.append((item["source"], raw, None))
        require(len(sources) == len({row[0] for row in sources}), "Duplicate source")
        chain_path = OUT / (run + "-chain.json")
        chain = build_chain(sources, WS / "review-chains" / run.lower(), chain_path, guard, run)
        verify_chain(chain, sources)
        prompt_path, kickoff_path = (OUT / (run + "-" + suffix + ".txt") for suffix in ("prompt", "kickoff"))
        prompt = render({**spec, "scope": ["\u5893"], "dispositionIds": ids}, refs["report"],
                        chain, prompt_path, report)
        kickoff = (f"Read {prompt_path} using one view call with forceReadLargeFiles: true and no view_range, "
                   "then follow its instructions. No other tool call may precede that read.").encode("ascii")
        bindings.extend([write_frozen(prompt_path, prompt), write_frozen(kickoff_path, kickoff),
                         binding(chain_path), binding(Path(__file__))])
        bindings.extend(binding(OUT / name) for name in ("renderer.py", "audit-confirm.py",
                                                        "check-confirm-structure.py"))
        for name in ("review_chain.py", "b132_capacity.py", "b132_runtime.py", "b132_common.py"):
            bindings.append(binding(PROTOCOL / name))
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
        clean(git, candidate)
        record = {
            "batch": 132, "run": run, "session": spec["session"], "candidate": candidate,
            "config": config_ref, "kickoff": binding(kickoff_path), "chain": binding(chain_path),
            "segments": len(chain["segments"]), "sources": len(sources), "capacity": forecast,
            "initialReport": refs["report"], "initialAcceptance": refs["acceptance"],
            "preparedOnly": True, "publicationAccepted": False,
        }
        print(json.dumps(freeze_json(OUT / (run + "-preflight.json"), record)))
    finally:
        require(not guard.finish()["breach"], "Confirmation preparation RAM breach")


def preflight(path):
    record = json.loads(frozen(path))
    config = json.loads(frozen(record["config"]["path"], record["config"]["sha256"]))
    require(record["run"] == config["run"] and record["candidate"] == config["candidate"],
            "Preflight identity differs")
    for item in config["files"]:
        frozen(item["path"], item["sha256"])
    chain = json.loads(frozen(config["chainManifest"]))
    for segment in chain["segments"]:
        frozen(segment["path"], segment["sha256"])
    return record, config, chain


def admit(path, request_path):
    record, config, chain = preflight(path)
    request_raw = frozen(request_path)
    request = json.loads(request_raw)
    status_raw, roster_raw = (frozen(request[key]) for key in ("statusPath", "rosterPath"))
    now = datetime.datetime.now(datetime.timezone.utc)
    check_roster(json.loads(status_raw), json.loads(roster_raw), record["session"],
                 datetime.datetime.fromisoformat(request["observedAt"]), now)
    guard, resource = start_guard(record["run"] + " admission")
    try:
        clean(Git(REPO, RUNNER, guard), record["candidate"])
        destination(config["report"])
        events = Path.home() / ".copilot" / "session-state" / record["session"] / "events.jsonl"
        raw = events.read_bytes()
        observed = context(raw, config["expectedFamily"])
        forecast = capacity(observed, chain, len(frozen(config["prompt"])))
        prefix = write_frozen(OUT / (record["run"] + "-pre-delivery-events.jsonl"), raw)
        now = datetime.datetime.now(datetime.timezone.utc)
        check_roster(json.loads(status_raw), json.loads(roster_raw), record["session"],
                     datetime.datetime.fromisoformat(request["observedAt"]), now)
        require(resource.available_ram() > 2 * 1024**3, "Startup RAM floor no longer met")
        result = {
            **record, "admitted": True, "admittedAt": now.isoformat(),
            "observedAt": request["observedAt"], "offset": len(raw), "prefixSha256": sha(raw),
            "prefix": prefix, "status": binding(request["statusPath"]),
            "roster": binding(request["rosterPath"]), "request": binding(request_path),
            "context": observed, "capacity": forecast, "freeRamBytes": resource.available_ram(),
        }
        print(json.dumps(freeze_json(OUT / (record["run"] + "-admission.json"), result)))
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
        checker = load_module("b132_confirm_structure_actual", OUT / "check-confirm-structure.py")
        structure = checker.check(frozen(report).decode("utf-8"), run, record["candidate"],
                                  config["dispositionIds"], json.loads(frozen(config["chainManifest"])),
                                  audit["messages"][0])
        result = {
            "run": run, "candidate": record["candidate"], "session": record["session"],
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
    if action == "build":
        build(Path(arguments[0]))
    elif action == "admit":
        admit(Path(arguments[0]), Path(arguments[1]))
    elif action == "final":
        final(Path(arguments[0]))
    else:
        raise SystemExit("build SPEC | admit PREFLIGHT REQUEST | final PREFLIGHT")
