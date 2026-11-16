"""Run-lifecycle records for a batch review run; observation and verification only, never launches a reviewer.

Derived from step.py: an optional frozen prompts preflight selects a clean-path attempt, and child checkers
always run with UTF-8 stdout.

  python -B step_b127.py <batch> <claude|gpt> admit <get_sessions_status.json> [preflight]
  python -B step_b127.py <batch> <claude|gpt> launch <session-id> [preflight]
  python -B step_b127.py <batch> <claude|gpt> phase1 <session-id> [preflight]
  python -B step_b127.py <batch> <claude|gpt> final <session-id> [preflight]
  python -B step_b127.py <batch> <claude|gpt> accept <adjudication.json> [preflight]
"""
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from common import (COORDINATOR, GUARD, TOOLS, WS, freeze_json, frozen, load_batch, load_module, packet_dir, require,
                    review_dir, sha, write_frozen)

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse  # noqa: E402

EVENTS = Path.home() / ".copilot" / "session-state"


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def binding(path):
    data = frozen(path)
    return {"path": str(path), "sha256": sha(data)}


from b127_lifecycle_process import python


def audit(records, config_path, session, *extra):
    code, out, err = python(records / "audit-review.py", "--session", session, "--config", config_path, *extra)
    match = re.search(r"^Audit: (.+)$", out, re.M)
    require(match, f"Auditor produced no record (exit {code}): {out}\n{err}")
    path = Path(match[1].strip())
    return path, json.loads(frozen(path))


def context(records, events):
    code, out, err = python(records / "check-run-context.py", events)
    require(code in (0, 1), err)
    return json.loads(out)


def main(batch, key, action, argument, preflight=None):
    config = load_batch(batch)
    records = review_dir(batch)
    preflight_path = Path(preflight) if preflight else records / "prompts" / "preflight.json"
    require(preflight_path.parent == records / "prompts", "Preflight must be a frozen prompts record")
    preflight = json.loads(frozen(preflight_path))
    spec = preflight["runs"][key]
    run = spec["run"]
    config_path = Path(spec["auditConfig"])
    audit_config = json.loads(frozen(config_path))
    for item in audit_config["files"]:
        frozen(Path(item["path"]), item["sha256"])
    report = Path(spec["report"])
    extension = records / f"{run}-extension.json"
    phase2 = records / f"{run}-phase2-message.txt"
    record = {"run": run, "batch": config["batch"], "candidate": config["candidate"], "createdAt": now(),
              "preflightSha256": sha(preflight_path.read_bytes()),
              "preflight": str(preflight_path),
              "tool": {"path": str(TOOLS / "step_b127.py"), "sha256": sha((TOOLS / "step_b127.py").read_bytes())}}

    if action == "admit":
        order = preflight["order"]
        for earlier in order[:order.index(key)]:
            prior = json.loads(frozen(records / f"{preflight['runs'][earlier]['run']}-acceptance.json"))
            require(prior["reviewAccepted"] is True and prior["candidate"] == config["candidate"],
                    f"Earlier {earlier} run not accepted")
        source = Path(argument)
        raw = source.read_bytes()
        status = json.loads(raw)
        sessions = status.get("sessions", [])
        active = [{"id": s.get("id"), "name": s.get("name"), "activity": s.get("activity")} for s in sessions
                  if (s.get("activity") or {}).get("status") != "idle" or s.get("is_running")]
        others = [s for s in active if s["id"] not in (COORDINATOR, "e1ee36b6-cb53-4c64-854e-cec8a61c1dfb")]
        same_name = [s.get("name") for s in sessions if (s.get("name") or "").strip() == spec["launch"]["sessionName"]]
        resource = load_module("n1_ram_guard_admit", GUARD)
        ram = resource.available_ram()
        absent = {"report": not report.exists(), "extension": not extension.exists(),
                  "auditDirectory": not (records / run).exists()}
        record.update(freeRamBytes=ram, startupFloorMet=ram > 2 * 1024 ** 3, activeSessions=active,
                      otherBusySession=bool(others), sessionNamedForThisRunExists=bool(same_name),
                      absent=absent, launch=spec["launch"], kickoff=spec["kickoffText"],
                      note="Fresh observation only, not a reservation or permission to skip later guards.")
        record["admitted"] = bool(record["startupFloorMet"] and not others and not same_name and all(absent.values()))
        if not record["admitted"]:
            print(json.dumps(record, ensure_ascii=False, indent=1))
            raise SystemExit("Admission refused")
        record["statusSnapshot"] = write_frozen(records / f"{run}-admission-status.json", raw)
        out = records / f"{run}-admission.json"

    elif action == "launch":
        admission = binding(records / f"{run}-admission.json")
        events = [json.loads(line) for line in (EVENTS / argument / "events.jsonl").read_text("utf-8").splitlines()]
        start = [e["data"] for e in events if e.get("type") == "session.start"]
        users = [e["data"]["content"] for e in events if e.get("type") == "user.message"]
        require(len(start) == 1 and start[0].get("contextTier") == "long_context"
                and start[0].get("selectedModel") == spec["launch"]["model"], f"Launch mismatch: {start}")
        require(users and users[0] == spec["kickoffText"] and len(users) == 1, "First user message is not the kickoff")
        record.update(session=argument, runtimeStartedAt=start[0].get("startTime"), contextTier="long_context",
                      model=spec["launch"]["model"], mode=spec["launch"]["mode"], admission=admission,
                      kickoffSha256=sha(spec["kickoffText"].encode("ascii")),
                      verification="session.start has the long_context tier and the selected model; the only user "
                                   "message equals the frozen kickoff exactly.")
        out = records / f"{run}-launch.json"

    elif action == "phase1":
        launch = json.loads(frozen(records / f"{run}-launch.json"))
        require(launch["session"] == argument, "Session differs from launch")
        path, result = audit(records, config_path, argument)
        ctx = context(records, path.parent / "events.jsonl")
        record.update(session=argument, status=result["status"], auditDir=str(path.parent),
                      auditSha256=sha(path.read_bytes()), eventsSha256=result.get("eventsSha256"),
                      phase1ListSha256=result.get("phase1ListSha256"), breaches=result.get("breaches"),
                      notes=result.get("notes"), actualResponseModels=result.get("actualResponseModels"),
                      reviewerIdle=result.get("reviewerIdle"), coreRead=result.get("coreRead"),
                      coreRequired=result.get("coreRequired"), context=ctx)
        ready = result["status"] == "PHASE1_READY" and not result["breaches"] and ctx["status"] == "PASS"
        out = records / f"{run}-phase1.json"
        if ready:
            code, stdout, stderr = python(TOOLS / "prepare-chain.py", config["batch"], "--run", run,
                                          "--reply", path.parent / "phase1-list.txt", "--phase1-audit", path)
            record["extensionPreparation"] = {"exitCode": code, "stdout": stdout[-3000:], "stderr": stderr[-3000:]}
            ready = code == 0
        record["readyForPhase2"] = ready
        freeze_json(out, record)
        print(json.dumps({k: record[k] for k in ("status", "breaches", "notes", "readyForPhase2")}, ensure_ascii=False))
        print("PHASE1 LIST:\n" + (path.parent / "phase1-list.txt").read_text("utf-8")
              if (path.parent / "phase1-list.txt").exists() else "NO LIST")
        if ready:
            print("PHASE2 MESSAGE (send exactly):\n" + phase2.read_text("utf-8"))
        return 0 if ready else 1

    elif action == "final":
        phase1 = json.loads(frozen(records / f"{run}-phase1.json"))
        require(phase1["readyForPhase2"] and phase1["session"] == argument, "Phase 1 was not ready")
        phase1_list = Path(phase1["auditDir"]) / "phase1-list.txt"
        path, result = audit(records, config_path, argument, "--extension", extension, "--phase1-list", phase1_list,
                             "--phase2-message", phase2, "--final")
        problems = []
        if result["status"] != "FINAL_AUDIT_NEEDS_CLAIM_CHECK" or result.get("breaches"):
            problems.append(f"audit {result['status']} {result.get('breaches')}")
        else:
            if (result["unexpectedUserMessages"] or not result["reviewerIdle"]
                    or result["coreRead"] != result["coreRequired"]
                    or result["extensionRead"] != result["extensionRequired"] or result["writes"] != 1
                    or result["readbacks"] != 1 or not result["readbackVerified"] or result["fetches"]
                    or len(result["messages"]) != 2):
                problems.append("incomplete final execution")
            events = frozen(path.parent / "events.jsonl", result["eventsSha256"])
            if not events.startswith(frozen(Path(phase1["auditDir"]) / "events.jsonl")):
                problems.append("final events do not extend the phase-1 snapshot")
        ctx = context(records, path.parent / "events.jsonl")
        ctx.update(events=str(path.parent / "events.jsonl"),
                   checkerSha256=sha((records / "check-run-context.py").read_bytes()))
        context_record = freeze_json(records / f"{run}-context.json", ctx)
        if ctx["status"] != "PASS":
            problems.append("context " + "; ".join(ctx.get("errors", [])))
        structure = None
        if report.exists():
            report.chmod(0o444)
            code, stdout, stderr = python(
                records / "check-report-structure.py", "--report", report, "--core-manifest",
                audit_config["coreManifest"], "--extension", extension, "--reference", audit_config["reference"],
                "--phase1-list", phase1_list, "--phase2-message", phase2, "--audit", path, "--run", run)
            require(code in (0, 1) and stdout.strip(), f"Structure checker produced no result (exit {code}): {stderr}")
            structure = json.loads(stdout)
            structure_record = freeze_json(records / f"{run}-structure.json", structure)
            if structure["status"] != "PASS":
                problems.append("structure " + "; ".join(structure.get("errors", [])[:20]))
        else:
            problems.append("report missing")
        evidence = None
        if not problems:
            evidence = inspect(config, records, audit_config, report, extension)
        result_record = {**record, "session": argument, "finalAudit": binding(path), "context": context_record,
                         "structure": structure_record if structure else None, "problems": problems,
                         "evidenceCheck": evidence,
                         "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION" if not problems else "HOLD",
                         "execution": {k: result.get(k) for k in ("coreRead", "extensionRead", "writes", "readbacks",
                                                                  "fetches", "messages", "actualResponseModels")}}
        out = records / f"{run}-final.json"
        freeze_json(out, result_record)
        print(json.dumps({"status": result_record["status"], "problems": problems,
                          "messages": result.get("messages"), "report": str(report)}, ensure_ascii=False, indent=1))
        return 0 if not problems else 1

    elif action == "accept":
        final = json.loads(frozen(records / f"{run}-final.json"))
        require(final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION", "Final checks did not pass")
        adjudication_path = Path(argument)
        adjudication = json.loads(frozen(adjudication_path))
        require(adjudication["run"] == run and adjudication["report"]["sha256"] == sha(frozen(report)),
                "Adjudication is not bound to this report")
        record.update(reviewAccepted=True, verdict=adjudication["verdict"],
                      acceptedFindings=adjudication["acceptedFindings"],
                      report={"path": str(report), "sha256": sha(report.read_bytes())},
                      final=binding(records / f"{run}-final.json"), adjudication=binding(adjudication_path),
                      acceptanceLimit="Bounded independent evidence, not publication approval. Accepted findings "
                                      "require signed fixes and confirmation; the raw report is unchanged.")
        out = records / f"{run}-acceptance.json"
    else:
        raise SystemExit(__doc__)
    written = freeze_json(out, record)
    print(json.dumps({"record": written["path"], "sha256": written["sha256"]}, ensure_ascii=False))
    return 0


def inspect(config, records, audit_config, report, extension):
    root = packet_dir(config)
    report_raw = frozen(report)
    parts, sources = {}, {}
    for chain, manifest_path in (("core", Path(audit_config["coreManifest"])), ("extension", extension)):
        manifest = json.loads(frozen(manifest_path))
        for segment in manifest["segments"]:
            frozen(Path(segment["path"]), segment["sha256"])
            for part in segment["parts"]:
                name = re.sub(r"\s+\[[DE]\d+\]$", "", part["source"])
                sources[name] = frozen(root.joinpath(*name.split("/")), part["sha256"])
                parts.setdefault(name, []).append({"chain": chain, "segment": segment["index"],
                                                   "first": part["a"], "last": part["b"]})
    citations, rows, issues, item = [], [], [], None
    lines = report_raw.decode("utf-8").splitlines()
    for number, line in enumerate(lines, 1):
        heading = re.match(r"### ([FO]\d+):", line.replace("**", ""))
        if heading:
            item = heading[1]
        field = re.fullmatch(r"[-*] Citations:\s*(.*)", line.replace("**", "").strip()) if line[:1] in "-*" else None
        if not field:
            continue
        for citation in field[1].replace("`", "").split(";"):
            citation = citation.strip()
            match = re.fullmatch(r"(.+):(\d+)(?:\s*[-\u2013]\s*(\d+))?", citation)
            name = match[1].strip().replace("\\", "/") if match else None
            if not match or name not in parts:
                issues.append(f"{item}: citation {citation!r} is not an opened chain source")
                continue
            first, last = int(match[2]), int(match[3] or match[2])
            covered = {n for p in parts[name] for n in range(p["first"], p["last"] + 1)}
            opened = set(range(first, last + 1)) <= covered
            if not opened:
                issues.append(f"{item}: citation {citation!r} cites lines outside the opened ranges")
            citations.append({"item": item, "reportLine": number, "citation": citation, "opened": opened,
                              "exactSourceText": "\n".join(sources[name].decode("utf-8").splitlines()[first - 1:last])})
    reference = json.loads(frozen(Path(audit_config["reference"])))
    new_cards = reference["newCards"]

    def meta(name):
        fm, _ = parse(sources[name].decode("utf-8").replace("\r\n", "\n"))
        return str(fm["title"]).strip("\"'"), fm.get("quiz_exclusions") or []

    new_meta = {c: meta(f"snapshot/kanji/{c}.md") for c in new_cards}
    for number, line in enumerate(lines, 1):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not re.fullmatch(r"[DE]\d+", cells[0].replace("**", "")) or len(cells) != 6:
            continue
        label, card, title, related, reason, disposition = cells
        card = card.strip("`* ")
        name = f"repo/kanji/{card}.md"
        if name not in sources:
            issues.append(f"{label}: card {card} was not in the opened chains")
            continue
        actual, exclusions = meta(name)
        related_cards = [c for c in new_cards if c in related]
        if title.strip("`* ") != actual or not related_cards:
            issues.append(f"{label}: displayed title or related card does not match {name}")
        rows.append({"id": label, "card": card, "reportLine": number, "displayedTitle": actual,
                     "titleMatches": title.strip("`* ") == actual,
                     "relatedNewCards": {c: {"newEndpointDeclares": card in new_meta[c][1],
                                             "otherEndpointDeclares": c in exclusions} for c in related_cards},
                     "reason": reason, "disposition": disposition})
    verdict = re.search(r"^## Overall verdict\s*\nVerdict: (CLEAN|NEEDS FIX|UNVERIFIED)", report_raw.decode("utf-8"), re.M)
    result = {"run": audit_config["run"], "report": {"path": str(report), "sha256": sha(report_raw)},
              "verdict": verdict[1] if verdict else None, "formalCitations": citations, "issues": issues,
              "comparisons": rows, "sourceFilesRehashed": len(sources),
              "newTitles": {c: m[0] for c, m in new_meta.items()},
              "acceptanceLimit": "Mechanics and factual source bindings only; no linguistic verdict is inferred."}
    return freeze_json(records / f"{audit_config['run']}-evidence-check.json", result)


if __name__ == "__main__":
    if len(sys.argv) not in (5, 6) or sys.argv[2] not in ("claude", "gpt"):
        raise SystemExit(__doc__)
    sys.exit(main(*sys.argv[1:]))
