"""Prepare and audit bounded, same-reviewer N1 confirmations without launching reviewers."""
import ast
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

from common import (COORDINATOR, TOOLS, WS, at_commit, freeze_json, frozen, git, load_batch,
                    load_module, require, review_dir, sha, start_guard, verify_packet, write_frozen)

PINS = {
    "audit-confirm.py": "c6ec99949ef19057f432c052df3293184c3866e65ba7387e148a39505a3b2c9e",
    "check-confirm-structure.py": "ad3a204757e872e54b81745a028d040e4510ce551046a63ec6b70fcb0bddd31d",
    "test-audit-confirm.py": "21619257f2cbfd446a0f36a1f526c38d77dc0f98909f5e1fa8c4eaa4879537d9",
    "test-confirm-structure.py": "cb98ae269f1fa55689d107ada23a49677e81937f67fff030421179fbe5aafddb",
    "prepare-confirmation-v9.py": "ae0efcc5624c73bb9bd2a3e37131a572b771d2070bb868745aecff67dc321af5",
}


def binding(path):
    return {"path": str(path), "sha256": sha(frozen(path))}


def derive(batch):
    out = review_dir(batch) / "confirm"
    out.mkdir(exist_ok=False)
    derivations = []
    for name, expected in PINS.items():
        path = WS / "scratch-116" / "confirm" / name
        original = frozen(path, expected)
        selected = original
        if name == "prepare-confirmation-v9.py":
            text = original.decode("utf-8")
            selected = ("\n\n".join(ast.get_source_segment(text, node) for node in ast.parse(text).body
                                    if isinstance(node, ast.FunctionDef)
                                    and node.name in ("skeleton", "render_prompt", "self_test")) + "\n").encode("utf-8")
            name = "renderer.py"
        derived = selected.replace(b"B116", f"B{batch}".encode("ascii"))
        require(derived.replace(f"B{batch}".encode("ascii"), b"B116") == selected, "Reverse delta failed")
        prefix = b""
        if name == "renderer.py":
            prefix = (f"import re\nfrom pathlib import Path\nfrom common import COORDINATOR, require, "
                      f"load_module as load\nHERE = Path(__file__).resolve().parent\n\n").encode("ascii")
        compile(prefix + derived, name, "exec")
        derivations.append({"source": binding(path), "output": write_frozen(out / name, prefix + derived),
                            "reverseExact": True,
                            "selection": "three unchanged render/test functions" if prefix else "whole file",
                            "soleSelectedDelta": f"B116 to B{batch}"})
    renderer = load_module("n1_confirm_renderer", out / "renderer.py")
    renderer.self_test()
    run = subprocess.run([sys.executable, "-B", "-m", "unittest", "test-audit-confirm",
                          "test-confirm-structure"], cwd=out, capture_output=True)
    log = write_frozen(out / "tooling-tests.txt", run.stdout + run.stderr)
    freeze_json(out / "tooling-preflight.json", {"derivations": derivations, "exitCode": run.returncode,
                                               "tests": log, "rendererChecks": 3})
    print((run.stdout + run.stderr).decode("utf-8"))
    require(run.returncode == 0, "Confirmation gate regressions failed")


def clean(config, candidate):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate), "Candidate must be a full SHA")
    require(git(config, "rev-parse", "HEAD").decode().strip() == candidate, "Candidate is not HEAD")
    require(not git(config, "status", "--porcelain").strip(), "Candidate is dirty")
    proof = git(config, "show", "-s", "--format=%G?|%ae|%ce", candidate).decode().strip()
    require(proof == "G|stop-cran@list.ru|stop-cran@list.ru", "Candidate identity/signature mismatch")
    git(config, "merge-base", "--is-ancestor", config["candidate"], candidate)


def revision_diff(config, candidate):
    names = git(config, "diff", "--name-only", "--no-renames", "-z",
                config["candidate"], candidate).decode("utf-8").split("\0")
    omitted = [p for p in names if p == "manifest.json" or p.startswith("docs/")]
    # Contributor receipts can contain the other reviewer's findings.
    delta = git(config, "diff", "--no-color", config["candidate"], candidate, "--",
                ".", ":(exclude)manifest.json", ":(exclude)docs")
    require(delta, "No non-contributor revision to confirm")
    return delta, omitted


def build(spec_path):
    spec = json.loads(frozen(spec_path))
    config = load_batch(spec["batch"])
    out = review_dir(spec["batch"]) / "confirm"
    run = spec["run"]
    require(re.fullmatch(rf"N1-B{spec['batch']}-[A-Z0-9-]+-CONFIRM-\d{{3}}", run), "Invalid run")
    require(spec["family"] in ("claude", "gpt"), "Unknown family")
    clean(config, spec["candidate"])
    accepted = json.loads(frozen(Path(spec["acceptance"]["path"]), spec["acceptance"]["sha256"]))
    require(accepted.get("reviewAccepted") is True, "Initial review is not accepted")
    launch = json.loads(frozen(review_dir(spec["batch"]) / f"{accepted['run']}-launch.json"))
    require(launch["session"] == spec["session"] and accepted["candidate"] == config["candidate"],
            "Wrong original reviewer or freeze")
    original = frozen(Path(accepted["report"]["path"]), accepted["report"]["sha256"])
    ids = re.findall(r"(?m)^### ([FO]\d+):", original.decode("utf-8"))
    require(len(ids) == len(set(ids)), "Duplicate original dispositions")
    report = WS / f"reports-{spec['batch']}" / f"{run}.md"
    require(not report.exists(), "Report destination already exists")
    sources = [(f"initial-report/{Path(accepted['report']['path']).name}", original, None)]
    bindings = [binding(spec_path), spec["acceptance"], accepted["report"]]
    revised = dict(config, candidate=spec["candidate"])
    delta, omitted = revision_diff(config, spec["candidate"])
    diff_path = out / f"{run}-fix.patch"
    bindings.append(write_frozen(diff_path, delta))
    sources.append(("diffs/fix.patch", delta, None))
    guard, _ = start_guard(run)
    try:
        packet, sums, _ = verify_packet(config, guard)
        for path in spec["revisedSources"]:
            data = at_commit(revised, path)
            saved = out / run / "snapshot" / Path(path)
            bindings.append(write_frozen(saved, data))
            sources.append((f"snapshot/{path}", data, None))
        for path in spec["originalSources"]:
            require(path in sums, f"Unbound original source {path}")
            data = frozen(packet / Path(path), sums[path])
            bindings.append(binding(packet / Path(path)))
            sources.append((f"original-packet/{path}", data, None))
        for item in spec["additionalSources"]:
            data = frozen(Path(item["path"]), item["sha256"])
            bindings.append({"path": item["path"], "sha256": item["sha256"]})
            sources.append((item["source"], data, None))
        require(len(sources) == len({s[0] for s in sources}), "Duplicate source")
        chain_module = load_module("n1_confirm_chain", review_dir(spec["batch"]) / "review_chain.py")
        chain_path = out / f"{run}-chain.json"
        chain = chain_module.build_chain(sources, WS / "review-chains" / run.lower(), chain_path, guard, run)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM guard breached")
    renderer = load_module("n1_confirm_renderer", out / "renderer.py")
    prompt_path, kickoff_path = out / f"{run}-prompt.txt", out / f"{run}-kickoff.txt"
    renderer_spec = {**spec, "scope": config["members"], "dispositionIds": ids}
    packet_info = {"candidate": spec["candidate"], "freeze": config["candidate"],
                   "originalReport": accepted["report"]["path"], "report": str(report)}
    prompt = renderer.render_prompt(renderer_spec, packet_info, chain, prompt_path).encode("utf-8")
    kickoff = (f"Read {prompt_path} using one view call with forceReadLargeFiles: true and no view_range, "
               "then follow its instructions. No other tool call may precede that read.").encode("ascii")
    bindings.extend([write_frozen(prompt_path, prompt), write_frozen(kickoff_path, kickoff), binding(chain_path)])
    bindings.extend(binding(out / name) for name in ("renderer.py", "audit-confirm.py", "check-confirm-structure.py"))
    bindings.extend(binding(path) for path in (Path(__file__), review_dir(spec["batch"]) / "review_chain.py",
                                              review_dir(spec["batch"]) / "check-run-context.py"))
    audit_config = {"run": run, "prompt": str(prompt_path), "kickoff": str(kickoff_path), "report": str(report),
                    "coordinator": COORDINATOR, "expectedFamily": spec["family"], "chainManifest": str(chain_path),
                    "completionContract": "entire-message-enum-v1", "reportStructureContract": "confirm-structure-v1",
                    "dispositionIds": ids, "maxWebFetches": 0, "files": bindings}
    config_binding = freeze_json(out / f"{run}-config.json", audit_config)
    result = {"run": run, "batch": spec["batch"], "session": spec["session"], "candidate": spec["candidate"],
              "config": config_binding, "kickoff": binding(kickoff_path), "chain": binding(chain_path),
              "segments": len(chain["segments"]), "sourceCount": len(sources),
              "diffOmittedPaths": omitted,
              "diffScope": "All changes except generated manifest and contributor docs. "
                           "Reviewer-specific responses and neutral evidence are explicitly selected in the spec.",
              "memory": memory, "preparedOnly": True}
    print(json.dumps(freeze_json(out / f"{run}-preflight.json", result)))


def preflight(path):
    record = json.loads(frozen(path))
    config = json.loads(frozen(Path(record["config"]["path"]), record["config"]["sha256"]))
    for item in config["files"]:
        frozen(Path(item["path"]), item["sha256"])
    return record, config


def admit(path, status_path):
    record, config = preflight(path)
    now = datetime.datetime.now(datetime.timezone.utc)
    require(abs(now.timestamp() - status_path.stat().st_mtime) < 180, "Status is stale")
    status_raw = status_path.read_bytes()
    sessions = json.loads(status_raw)["sessions"]
    others = [s["id"] for s in sessions if s["id"] not in
              (COORDINATOR, "e1ee36b6-cb53-4c64-854e-cec8a61c1dfb") and
              ((s.get("activity") or {}).get("status") != "idle" or s.get("is_running"))]
    require(not others, f"Other active/unknown sessions: {others}")
    reviewer = next(s for s in sessions if s["id"] == record["session"])
    require(not reviewer.get("awaiting_user_input") and not reviewer.get("awaiting_plan_approval"),
            "Reviewer needs user input")
    clean(load_batch(record["batch"]), record["candidate"])
    require(not Path(config["report"]).exists(), "Report already exists")
    events = Path.home() / ".copilot" / "session-state" / record["session"] / "events.jsonl"
    raw = events.read_bytes()
    require(raw.endswith(b"\n"), "Incomplete event prefix")
    checker = load_module("n1_confirmation_context", review_dir(record["batch"]) / "check-run-context.py")
    context = checker.check(events)
    require(context["status"] == "PASS" and context["eventsSha256"] == sha(raw), "Context failed/changed")
    guard, resource = start_guard(record["run"])
    memory = guard.finish()
    require(not memory["breach"], "RAM guard breached")
    out = path.parent
    prefix = write_frozen(out / f"{record['run']}-pre-delivery-events.jsonl", raw)
    snapshot = write_frozen(out / f"{record['run']}-admission-status.json", status_raw)
    result = {**record, "admittedAt": now.isoformat(), "offset": len(raw), "prefixSha256": sha(raw),
              "prefix": prefix, "status": snapshot, "context": context, "freeRamBytes": resource.available_ram()}
    print(json.dumps(freeze_json(out / f"{record['run']}-admission.json", result)))
    print(frozen(Path(record["kickoff"]["path"])).decode("ascii"))


def final(path):
    record, config = preflight(path)
    out, run = path.parent, record["run"]
    admission = json.loads(frozen(out / f"{run}-admission.json"))
    command = [sys.executable, "-B", str(out / "audit-confirm.py"), "--session", record["session"],
               "--config", record["config"]["path"], "--offset", str(admission["offset"]),
               "--prefix-sha256", admission["prefixSha256"], "--final"]
    done = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    match = re.search(r"^Audit: (.+)$", done.stdout, re.M)
    require(match, done.stdout + done.stderr)
    audit_path = Path(match[1].strip())
    audit = json.loads(frozen(audit_path))
    require(audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and not audit["breaches"]
            and audit["reviewerIdle"] and not audit["unexpectedUserMessages"]
            and audit["chainRead"] == audit["chainRequired"] and audit["writes"] == audit["readbacks"] == 1
            and audit["readbackVerified"] and audit["fetches"] == 0 and len(audit["messages"]) == 1,
            f"Confirmation execution HOLD: {audit_path}")
    report = Path(config["report"])
    report.chmod(0o444)
    checker = load_module("n1_confirmation_context", review_dir(record["batch"]) / "check-run-context.py")
    context = checker.check(audit_path.parent / "events.jsonl")
    context_binding = freeze_json(out / f"{run}-context.json", context)
    structure_checker = load_module("n1_confirmation_structure", out / "check-confirm-structure.py")
    structure = structure_checker.check(frozen(report).decode("utf-8"), run, record["candidate"],
                                         config["dispositionIds"], json.loads(frozen(Path(config["chainManifest"]))),
                                         audit["messages"][0])
    structure_binding = freeze_json(out / f"{run}-structure.json", structure)
    result = {"run": run, "candidate": record["candidate"], "session": record["session"],
              "audit": binding(audit_path), "context": context_binding, "structure": structure_binding,
              "report": binding(report), "confirmation": structure["confirmation"],
              "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
              if context["status"] == structure["status"] == "PASS" else "HOLD"}
    print(json.dumps(freeze_json(out / f"{run}-final.json", result)))
    print(json.dumps({"status": result["status"], "structure": structure, "context": context}, ensure_ascii=False))


if __name__ == "__main__":
    action, *args = sys.argv[1:]
    if action == "derive":
        derive(int(args[0]))
    elif action == "build":
        build(Path(args[0]))
    elif action == "admit":
        admit(Path(args[0]), Path(args[1]))
    elif action == "final":
        final(Path(args[0]))
    else:
        raise SystemExit("derive <batch> | build <spec> | admit <preflight> <status> | final <preflight>")
