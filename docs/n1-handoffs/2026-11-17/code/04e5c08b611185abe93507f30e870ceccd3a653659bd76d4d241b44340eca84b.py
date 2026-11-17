"""Exercise report readiness failures and real extension-preparer HOLD without outputs."""
import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import patch

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
HERE = ROOT / "neutral-preparation-001" / "projected-successor-001"
PROTOCOL = HERE / "protocol-001"
sys.path.insert(0, str(PROTOCOL))
from b134_common import frozen, require, sha, freeze_json, write_frozen, start_guard, validate_report_destination
from review_chain_with_optional import validate_selection

CASE = HERE / "readiness-and-hold-validation-001"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, PROTOCOL / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def must_fail(action, text):
    try:
        action()
    except ValueError as error:
        require(text in str(error), "Unexpected rejection: " + str(error))
        return str(error)
    raise ValueError("Invalid fixture was not rejected")


def main():
    require(not CASE.exists(), "Preserve control outputs")
    guard, _ = start_guard("B134 actual readiness and extension HOLD controls")
    try:
        fixture = module("b134_hold_fixture", "test-synthetic-protocol-b134-001.py")
        preflight = json.loads(frozen(HERE / "audit-configs-001" / "preflight.json"))
        config = json.loads(frozen(preflight["runs"]["gpt"]["auditConfig"]["path"]))
        core = json.loads(frozen(config["coreManifest"]))
        ref = json.loads(frozen(config["reference"]))
        failures = []
        report = CASE / "readiness" / "report.md"
        report.parent.mkdir(parents=True)
        spec = {"report": str(report)}
        validate_report_destination(spec)
        write_frozen(report.parent / "unrelated-fixture.txt", b"nonempty directory\n")
        failures.append(must_fail(lambda: validate_report_destination(spec), "not empty/writable"))
        existing = CASE / "existing" / "report.md"
        write_frozen(existing, b"existing output\n")
        failures.append(must_fail(lambda: validate_report_destination({"report": str(existing)}), "unavailable"))
        readonly = CASE / "readonly" / "report.md"
        readonly.parent.mkdir()
        readonly.parent.chmod(0o444)
        try:
            failures.append(must_fail(lambda: validate_report_destination({"report": str(readonly)}), "not empty/writable"))
        finally:
            readonly.parent.chmod(0o777)
        # Exact E10/E11 and D25/D26 controls use fabricated eligibility, not review choices.
        fake = {"newCards": ["甲"], "otherRequiredCards": [], "cards": [
            {"distractors": [], "quiz_exclusions": [chr(0x5100 + i) for i in range(11)]}]}
        e_lines = [f"E{i + 1} {chr(0x5100 + i)} - synthetic only" for i in range(11)]
        require(validate_selection("D: none\n" + "\n".join(e_lines[:10]) + "\nO: none", fake)["valid"],
                "E10 boundary rejected")
        require(not validate_selection("D: none\n" + "\n".join(e_lines) + "\nO: none", fake)["valid"],
                "E11 boundary accepted")
        reply = ("D: none\nE: none\nO1 evidence/font-cmap.json - synthetic\n"
                 "O2 evidence/xml-presentation.json - synthetic\n"
                 "O3 evidence/dictionary-index.json - synthetic")
        require(validate_selection(reply, ref)["valid"], "Over-allowance fixture syntax invalid")
        events = fixture.events_for(config, core)
        events[-3]["data"]["toolRequests"][0]["arguments"]["message"] = reply
        first = fixture.AUDIT.audit(events, config, core, ref)
        require(first["status"] == "PHASE1_READY", "Over-allowance first-phase audit failed")
        audit_dir = CASE / "over-allowance" / config["run"] / "phase1"
        raw = b"".join((json.dumps(e, ensure_ascii=False) + "\n").encode() for e in events)
        first["eventsSha256"] = sha(raw)
        write_frozen(audit_dir / "events.jsonl", raw)
        audit = freeze_json(audit_dir / "audit.json", first)
        reply_binding = write_frozen(audit_dir / "phase1-list.txt", reply.encode())
        cfg = freeze_json(CASE / "over-allowance" / "config.json", config)
        arguments = ["prepare-extension", "--config", cfg["path"], "--reply", reply_binding["path"],
                     "--phase1-audit", audit["path"]]
        with patch.object(fixture.PREPARE, "HERE", CASE / "over-allowance"), patch.object(sys, "argv", arguments):
            rejection = must_fail(fixture.PREPARE.main, "optional evidence allowance exceeded")
        for suffix in ("-extension.json", "-extension-preflight.json", "-phase2-message.txt"):
            require(not (CASE / "over-allowance" / (config["run"] + suffix)).exists(),
                    "Partial extension/preflight/message created on HOLD")
        require(not (CASE / "over-allowance" / "chains").exists(), "Partial chain created on HOLD")
        # The production controller must reject either missing/altered actual coordinator proof.
        proof_name = "packet-verification-001/verification.json"
        real_frozen = fixture.STEP.frozen
        proof_path = ROOT / proof_name
        proof_error = must_fail(lambda: real_frozen(proof_path, "0" * 64), "Changed input")
        output = {"status": "PASS_SYNTHETIC_READINESS_AND_ACTUAL_PREPARER_HOLD",
                  "reportReadinessNegativeControls": failures, "E10PassE11Reject": True,
                  "optionalOverAllowanceRejection": rejection, "noPartialOutputs": True,
                  "actualPacketProofWrongHashRejected": proof_error,
                  "limits": "Fabricated first-phase events only; no reviewer launched, no teaching adjudication."}
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Readiness/HOLD control RAM breach")
    output["memory"] = memory
    print(json.dumps(freeze_json(HERE / "readiness-and-hold-validation-001.json", output)))


if __name__ == "__main__":
    main()
