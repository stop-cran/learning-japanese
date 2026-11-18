"""Derive B131 confirmation routing without changing report/access audit semantics."""
import ast
import json
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen

SOURCE = TOOLS / "confirm_b130_compact.py"
SOURCE_SHA = "f18dd4515b7ea2f351f9064f69edc299db67c23507c2f697715b04ea4121bdf3"
OUTPUT = TOOLS / "confirm_b131_001.py"
ROOT = WS / "scratch-131" / "review"


def derive_text(text):
    replacements = [
        ("from b130_compact_common import verify_packet",
         "from b131_review_v3_common import load_batch, verify_packet\n"
         "from b131_confirmation_routing_001 import (\n"
         "    CHAIN_PATH, admission_snapshot, capacity_check, check_context, initial_launch,\n"
         "    report_destination, routing_bindings)\n"
         "from b131_lifecycle_process_006 import python"),
        ('    run = subprocess.run([sys.executable, "-B", "-m", "unittest", "test-audit-confirm",\n'
         '                          "test-confirm-structure"], cwd=out, capture_output=True)\n'
         '    log = write_frozen(out / "tooling-tests.txt", run.stdout + run.stderr)',
         '    code, stdout, stderr = python("-m", "unittest", "discover", "-s", str(out), "-p", "test-*.py")\n'
         '    run = subprocess.CompletedProcess([], code, stdout.encode("utf-8"), stderr.encode("utf-8"))\n'
         '    log = write_frozen(out / "tooling-tests.txt", run.stdout + run.stderr)'),
        ('    launch = json.loads(frozen(review_dir(spec["batch"]) / f"{accepted[\'run\']}-launch.json"))',
         '    launch = initial_launch(spec, accepted, config)'),
        ('    require(not report.exists(), "Report destination already exists")',
         '    report_destination(report)'),
        ('review_dir(spec["batch"]) / "review_chain.py"', 'CHAIN_PATH'),
        ('    bindings.extend(binding(path) for path in (Path(__file__), CHAIN_PATH,\n'
         '                                              review_dir(spec["batch"]) / "check-run-context.py"))',
         '    bindings.append(binding(Path(__file__)))\n'
         '    bindings.extend(routing_bindings(spec["family"]))'),
        ('    require(abs(now.timestamp() - status_path.stat().st_mtime) < 180, "Status is stale")\n'
         '    status_raw = status_path.read_bytes()\n'
         '    sessions = json.loads(status_raw)["sessions"]\n'
         '    others = [s["id"] for s in sessions if s["id"] not in\n'
         '              (COORDINATOR, "e1ee36b6-cb53-4c64-854e-cec8a61c1dfb") and\n'
         '              ((s.get("activity") or {}).get("status") != "idle" or s.get("is_running"))]\n'
         '    require(not others, f"Other active/unknown sessions: {others}")\n'
         '    reviewer = next(s for s in sessions if s["id"] == record["session"])\n'
         '    require(not reviewer.get("awaiting_user_input") and not reviewer.get("awaiting_plan_approval"),\n'
         '            "Reviewer needs user input")',
         '    status_raw, roster_raw, request_raw = admission_snapshot(status_path, record["session"])'),
        ('    require(not Path(config["report"]).exists(), "Report already exists")',
         '    destination = report_destination(config["report"])'),
        ('    checker = load_module("n1_confirmation_context", review_dir(record["batch"]) / "check-run-context.py")\n'
         '    context = checker.check(events)',
         '    context = check_context(events, config["expectedFamily"])\n'
         '    capacity = capacity_check(context, json.loads(frozen(config["chainManifest"])))'),
        ('    snapshot = write_frozen(out / f"{record[\'run\']}-admission-status.json", status_raw)',
         '    snapshot = write_frozen(out / f"{record[\'run\']}-admission-status.json", status_raw)\n'
         '    roster = write_frozen(out / f"{record[\'run\']}-admission-roster.txt", roster_raw)\n'
         '    request = write_frozen(out / f"{record[\'run\']}-admission-request.json", request_raw)'),
        ('    result = {**record, "admittedAt": now.isoformat(), "offset": len(raw), "prefixSha256": sha(raw),',
         '    require(resource.available_ram() > 2 * 1024**3, "Startup RAM floor no longer met")\n'
         '    result = {**record, "admittedAt": now.isoformat(), "offset": len(raw), "prefixSha256": sha(raw),\n'
         '              "roster": roster, "request": request, "capacity": capacity, "reportDestination": destination,'),
        ('    from b127_lifecycle_process import python\n', ''),
        ('    checker = load_module("n1_confirmation_context", review_dir(record["batch"]) / "check-run-context.py")\n'
         '    context = checker.check(audit_path.parent / "events.jsonl")',
         '    context = check_context(audit_path.parent / "events.jsonl", config["expectedFamily"])'),
    ]
    result = text.replace("\r\n", "\n")
    for before, after in replacements:
        expected = 2 if before == 'review_dir(spec["batch"]) / "review_chain.py"' else 1
        require(result.count(before) == expected, "Unexpected B131 derivation anchor: " + before)
        result = result.replace(before, after)
    preserved = ("binding", "clean", "revision_diff", "preflight")
    functions = lambda value: {node.name: ast.dump(node) for node in ast.parse(value).body
                               if isinstance(node, ast.FunctionDef) and node.name in preserved}
    require(functions(text) == functions(result), "Unrelated engine mechanics changed")
    require(' / "check-run-context.py"' not in result, "Unqualified context namespace remains")
    return result


def main():
    original = frozen(SOURCE, SOURCE_SHA).decode("utf-8")
    text = derive_text(original)
    compile(text, str(OUTPUT), "exec")
    output = write_frozen(OUTPUT, text.encode("utf-8"))
    print(json.dumps(freeze_json(ROOT / "confirmation-engine-derivation-001.json", {
        "status": "PREPARATION_ONLY", "source": {"path": str(SOURCE), "sha256": SOURCE_SHA},
        "output": output, "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "routing": {"path": str(TOOLS / "b131_confirmation_routing_001.py"),
                    "sha256": sha(frozen(TOOLS / "b131_confirmation_routing_001.py"))},
        "changes": "B131 compact-002 source and core chain; exact accepted family-specific initial "
                   "namespaces, sessions and context profiles; bounded UTF-8 child execution; "
                   "full fresh status/roster admission; report-parent probe; conservative actual-chain "
                   "capacity gate. Existing access auditor and report checker remain mechanically derived.",
        "reviewersLaunched": False, "semanticAcceptance": False, "publicationAccepted": False,
    })))


if __name__ == "__main__":
    main()
