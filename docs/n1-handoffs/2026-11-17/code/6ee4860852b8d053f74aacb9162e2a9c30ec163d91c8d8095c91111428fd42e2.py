"""Verify the fresh runset and independently reproduce report-path rejection cases."""
import argparse
import copy
import json
import stat
from pathlib import Path
from unittest.mock import patch

from b131_review_v3_common import (
    DEFAULT_PREFLIGHT, HERE, IMMUTABLE_BINDINGS, OLD_PREP, RECORDS, TOOLS,
    freeze_json, frozen, require, sha, start_guard)
from b131_preflight_003 import validate_report_destination, verify_protocol, verify_subset
from b131_review_admission_003 import observe


PARTIAL = HERE / "partial-handoff-003.json"
PARTIAL_SHA = "a3b7112470da078c7bb14a1dc836d253168a49bf970991dd59b442eb0ce2453e"
OUTPUT = RECORDS / "preparation003-coordinator-verification-001.json"
FIXTURES = RECORDS / "preparation003-coordinator-path-controls-001"


def bound(path, digest):
    raw = frozen(path, digest)
    return {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}


def reject(call, expected):
    try:
        call()
    except ValueError as error:
        require(expected.lower() in str(error).lower(), "Unexpected rejection: " + str(error))
        return str(error)
    raise AssertionError("Invalid report destination was accepted")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    parser.add_argument("handoff_sha")
    parser.add_argument("validation", type=Path)
    parser.add_argument("validation_sha")
    parser.add_argument("path_proof", type=Path)
    parser.add_argument("path_proof_sha")
    args = parser.parse_args()
    require(not OUTPUT.exists() and not FIXTURES.exists(), "Preserve previous coordinator execution")
    guard, _ = start_guard("B131 fresh003 independent coordinator qualification")
    try:
        partial = json.loads(frozen(PARTIAL, PARTIAL_SHA))
        bindings = []
        for item in partial["files"]:
            value = bound(Path(item["path"]), item["sha256"])
            require(value["bytes"] == item["bytes"], "Partial handoff length differs")
            bindings.append(value)
            guard.check()
        for path, digest in IMMUTABLE_BINDINGS:
            bindings.append(bound(path, digest))
        for item in json.loads(frozen(HERE / "tooling-derivation-003.json"))["derivations"]:
            bound(Path(item["source"]), item["sourceSha256"])
            value = bound(Path(item["output"]["path"]), item["output"]["sha256"])
            require(value["bytes"] == item["output"]["bytes"], "Derived artifact length differs")

        preflight = json.loads(frozen(DEFAULT_PREFLIGHT))
        old = json.loads(frozen(
            OLD_PREP / "prompts" / "preflight-compact-002.json",
            "b27accc6688abbeb77a0d318f5bbfc32cca22cd5ac00663d73e728a7004e916a"))
        prompt_proofs = []
        for family in ("claude", "gpt"):
            before, after = old["runs"][family], preflight["runs"][family]
            expected = frozen(before["prompt"], before["promptSha256"])
            for key in ("prompt", "report", "run"):
                expected = expected.replace(before[key].encode(), after[key].encode())
            actual = frozen(after["prompt"], after["promptSha256"])
            require(actual == expected, "Prompt changed beyond exact run/path identity: " + family)
            kickoff = frozen(before["kickoff"]).replace(before["prompt"].encode(), after["prompt"].encode())
            require(frozen(after["kickoff"]) == kickoff, "Kickoff has a non-path change")
            require(after["launch"]["model"] == before["launch"]["model"]
                    and after["launch"]["contextTier"] == before["launch"]["contextTier"]
                    and after["launch"]["mode"] == before["launch"]["mode"],
                    "Model, context or reviewer mode differs")
            prompt_proofs.append({"family": family, "promptSha256": sha(actual),
                                  "changes": "Exact run, prompt path and report path only"})

        handoff_binding = bound(args.handoff, args.handoff_sha)
        handoff = json.loads(frozen(args.handoff, args.handoff_sha))
        require(handoff["status"] == "VERIFIED_FRESH003_PREPARATION_ONLY", "Final handoff is not ready")
        for item in handoff["files"]:
            value = bound(Path(item["path"]), item["sha256"])
            require(value["bytes"] == item["bytes"], "Final handoff length differs")
            guard.check()
        for key in ("qualification", "guardedCommands"):
            item = handoff[key]
            value = bound(Path(item["path"]), item["sha256"])
            require(value["bytes"] == item["bytes"], "Qualification/command binding differs")
        validation_binding = bound(args.validation, args.validation_sha)
        path_binding = bound(args.path_proof, args.path_proof_sha)
        paths = json.loads(frozen(args.path_proof, args.path_proof_sha))
        require(paths["status"] == "PASS" and not paths["memory"]["breach"], "Corrected path proof failed")
        previous = paths["supersedesInventoryOnly"]
        previous_paths = json.loads(frozen(Path(previous["path"]), previous["sha256"]))
        expected_inventory = copy.deepcopy(previous_paths["reviewerPathInventory"])
        for item in expected_inventory:
            item["extension"]["directory"] = str(HERE / "chains" / (f"b131-{item['run']}-extension-003"))
        require(paths["reviewerPathInventory"] == expected_inventory,
                "Path inventory changed beyond the corrected extension suffix")
        builder = paths["actualBuilder"]
        builder_source = frozen(Path(builder["path"]), builder["sha256"]).decode("utf-8")
        require(builder["expression"] == 'directory = HERE / "chains" / f"b131-{args.run}-extension-003"'
                and builder_source.count(builder["expression"]) == 1, "Inventory differs from actual builder")
        validation = json.loads(frozen(args.validation, args.validation_sha))
        require(validation["status"] == "PASS" and validation["tests"] == 32
                and validation["failures"] == validation["errors"] == 0
                and not validation["memory"]["breach"], "Full current validation did not pass")
        bound(Path(validation["testTool"]["path"]), validation["testTool"]["sha256"])
        bound(args.validation.parent / "output.log", validation["outputSha256"])

        evidence = verify_subset(guard, initial=True)
        protocol = verify_protocol(preflight)
        require(paths["reportDirectories"] == protocol["reportDestinations"],
                "Corrected readiness proof differs from actual report directories")
        FIXTURES.mkdir()
        controls = []
        spec = preflight["runs"]["claude"]
        for kind, expected in (("missing", "Missing report parent"),
                               ("not-directory", "Report parent is not a directory"),
                               ("present", "Report already present")):
            report = FIXTURES / kind / "parent" / "report.md"
            if kind == "not-directory":
                report.parent.parent.mkdir(parents=True)
                report.parent.write_bytes(b"fixture file, not directory\n")
            elif kind == "present":
                report.parent.mkdir(parents=True)
                report.write_bytes(b"existing fixture report\n")
            invalid = {**spec, "report": str(report)}
            candidate = copy.deepcopy(preflight)
            candidate["runs"]["claude"] = invalid
            controls.append({
                "case": kind,
                "preflight": reject(lambda: verify_protocol(candidate), expected),
                "admission": reject(lambda: observe(FIXTURES / "absent-request.json", {}, invalid, {}), expected)})

        parent = FIXTURES / "readonly"
        parent.mkdir()
        parent.chmod(stat.S_IREAD)
        try:
            controls.append({"case": "readonly", "result": reject(
                lambda: validate_report_destination({"report": str(parent / "report.md")}), "ReadOnly")})
        finally:
            parent.chmod(stat.S_IREAD | stat.S_IWRITE)
        parent = FIXTURES / "denied"
        parent.mkdir()
        with patch.object(Path, "open", side_effect=PermissionError("coordinator fixture ACL denial")):
            try:
                validate_report_destination({"report": str(parent / "report.md")})
            except PermissionError as error:
                controls.append({"case": "write-denied", "result": str(error)})
            else:
                raise AssertionError("Write denial was swallowed")
        require(not any(parent.iterdir()), "Write-denial fixture left an unexpected file")
        repeated = verify_protocol(preflight)
        require(repeated == protocol, "Actual report destinations changed during verification")
        memory = guard.finish()
        require(not memory["breach"], "Coordinator RAM breach")
        result = {
            "status": "PASS_PREPARATION_ONLY",
            "partial": bound(PARTIAL, PARTIAL_SHA),
            "handoff": handoff_binding, "validation": validation_binding, "pathProof": path_binding,
            "bindings": bindings, "promptIdentity": prompt_proofs, "evidence": evidence,
            "protocol": protocol, "independentPathControls": controls, "memory": memory,
            "tool": bound(Path(__file__), sha(frozen(Path(__file__)))),
            "limits": "Fresh startup admission, complete independent reviews and substantive adjudication "
                      "remain required. No reviewer launched and no teaching edited or published."
        }
        print(json.dumps(freeze_json(OUTPUT, result)))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
