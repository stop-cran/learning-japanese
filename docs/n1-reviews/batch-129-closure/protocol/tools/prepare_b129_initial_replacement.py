"""Preserve an executed failed first confirmation while replacing unavailable context."""
import ast
import json
from pathlib import Path

from common import TOOLS, freeze_json, frozen, load_module, require, review_dir, sha, write_frozen

SOURCE_SHA = "2ac571eb72cdd73415a829bc4930082b311215e6785e3d4066b01edf214b633a"
FAILED_RUN = "N1-B129-CLAUDE-CONFIRM-003"
FAILURE_SHA = "b1b2ea43168e84848de43a2710648b22dc1e0727b466e94a78d563951bf86355"


def binding(path):
    return {"path": str(path), "sha256": sha(frozen(path))}


def read(item):
    return json.loads(frozen(Path(item["path"]), item["sha256"]))


def check_lineage(spec, source, config, initial, launch, failure, audit, context):
    require(source["batch"] == spec["batch"] == config["batch"] == 129
            and source["family"] == spec["family"] == failure["family"] == "claude",
            "Wrong batch or replacement family")
    require(source["run"] == failure["run"] == FAILED_RUN
            and spec["run"] != source["run"]
            and source["session"] == spec["originalSession"] == launch["session"]
            == failure["session"] == audit["session"] != spec["session"],
            "Replacement must identify its unavailable original, not impersonate it")
    require(initial.get("reviewAccepted") is True
            and initial["candidate"] == config["candidate"]
            and source["candidate"] == spec["candidate"] == failure["candidate"],
            "Unaccepted initial review or changed correction snapshot")
    expected = {**source, "run": spec["run"], "session": spec["session"],
                "originalSession": source["session"], "replayedFrom": spec["replayedFrom"],
                "unavailable": spec["unavailable"]}
    require(spec == expected, "Replacement changes the frozen source assignment")
    require(failure["status"] == "VOID_CONTEXT_COMPACTION"
            and failure["reviewEvidenceAccepted"] is False
            and failure["confirmationAccepted"] is False
            and failure["reportWritten"] is False
            and failure["linguisticVerdict"] is None,
            "Executed failed confirmation must remain unaccepted and reportless")
    require(audit["status"] == "VOID" and audit["reviewerIdle"] is True
            and audit["writes"] == audit["readbacks"] == 0
            and audit["messages"] == failure["rawCompletionMessage"] == ["UNVERIFIED"]
            and audit["chainRead"] == failure["chainRead"] < audit["chainRequired"]
            == failure["chainRequired"],
            "Stopped execution or incomplete read account differs")
    require(context["status"] == "FAIL" and context["compactions"]
            and context["eventsSha256"] == audit["eventsSha256"],
            "No matching audited context-exhaustion evidence")


def verify_replacement(spec, config, initial, launch, records):
    out = records / "confirm"
    source_path = out / f"{FAILED_RUN}-spec.json"
    failure_path = out / f"{FAILED_RUN}-superseded.json"
    require(spec["replayedFrom"] == binding(source_path)
            and spec["unavailable"] == binding(failure_path),
            "Replacement lineage paths differ")
    frozen(failure_path, FAILURE_SHA)
    source, failure = read(spec["replayedFrom"]), read(spec["unavailable"])
    audit, context = read(failure["audit"]), read(failure["context"])
    check_lineage(spec, source, config, initial, launch, failure, audit, context)
    old_preflight_path = out / f"{FAILED_RUN}-preflight.json"
    old_preflight = json.loads(frozen(old_preflight_path))
    require(old_preflight["session"] == source["session"]
            and old_preflight["candidate"] == source["candidate"],
            "Failed run preflight differs")
    require(not Path(read(old_preflight["config"])["report"]).exists(),
            "Unexpected failed-run report; preserve it and investigate")
    audit_path = Path(failure["audit"]["path"])
    events_path = audit_path.parent / "events.jsonl"
    require(sha(frozen(events_path)) == audit["eventsSha256"], "Failed transcript changed")
    checker = load_module("b129_replacement_context", records / "check-run-context.py")
    require(checker.check(events_path) == context, "Context diagnosis does not reproduce")
    return [spec["replayedFrom"], spec["unavailable"], failure["audit"], failure["context"],
            binding(events_path), binding(old_preflight_path), old_preflight["config"],
            binding(records / f"{initial['run']}-launch.json"),
            binding(Path(__file__)), binding(TOOLS / "confirm_b127.py")]


def replacement_prompt(text):
    substitutions = (
        ("confirmation of your own accepted B129 initial review",
         "same-family replacement confirmation of the accepted B129 initial review"),
        ("Your own initial report:", "Original reviewer's initial report:"),
        ("your own unchanged initial report", "the original reviewer's unchanged initial report"),
        ("Read your own full report", "Read the original reviewer's full report"),
        ("including changes not requested by you",
         "including changes not requested in the original report"),
    )
    for before, after in substitutions:
        require(text.count(before) == 1, f"Unexpected renderer wording: {before}")
        text = text.replace(before, after)
    require("your own" not in text, "Historical authorship remains misattributed")
    return text + (
        "\nREPLACEMENT IDENTITY AND SCOPE\n"
        "You are a fresh same-family reviewer, not the author of the historical initial report. "
        "The original session became unavailable through observed context compaction during its "
        "first confirmation; that stopped execution has no report or accepted conclusions. "
        "Its incomplete execution is preserved separately and supplies no teaching evidence. "
        "There is no accepted earlier confirmation to carry forward. This is informed bounded "
        "confirmation, not renewed blind initial review or a claim of retained firsthand context. "
        "Read the complete source chain and independently establish every current disposition. "
        "Historical initial-review coverage remains attributed to its original reviewer; do not "
        "claim a fresh full reread of omitted records, other-language KD meanings, or the whole set. "
        "Missing evidence stays UNVERIFIED. All access, ordering, report and completion rules above "
        "remain unchanged.\n"
    )


def derive_text(text):
    substitutions = (
        ('PINS = {',
         'from prepare_b129_initial_replacement import verify_replacement, replacement_prompt\n\nPINS = {'),
        ('    require(launch["session"] == spec["session"] and accepted["candidate"] == config["candidate"],\n'
         '            "Wrong original reviewer or freeze")',
         '    replacement_bindings = verify_replacement(spec, config, accepted, launch, out.parent)'),
        ('    bindings = [binding(spec_path), spec["acceptance"], accepted["report"]]',
         '    bindings = [binding(spec_path), spec["acceptance"], accepted["report"]] + replacement_bindings'),
        ('    prompt = renderer.render_prompt(renderer_spec, packet_info, chain, prompt_path).encode("utf-8")',
         '    prompt = replacement_prompt(renderer.render_prompt(\n'
         '        renderer_spec, packet_info, chain, prompt_path)).encode("utf-8")'),
        ('    result = {"run": run, "batch": spec["batch"], "session": spec["session"], "candidate": spec["candidate"],',
         '    result = {"originalSession": spec["originalSession"],\n'
         '              "replacementReason": "audited-original-context-compaction",\n'
         '              "replayedFrom": spec["replayedFrom"], "unavailable": spec["unavailable"],\n'
         '              "run": run, "batch": spec["batch"], "session": spec["session"], "candidate": spec["candidate"],'),
    )
    for before, after in substitutions:
        require(text.count(before) == 1, f"Unexpected builder anchor: {before}")
        text = text.replace(before, after)
    return text


def main():
    source = TOOLS / "confirm_b127.py"
    original = frozen(source, SOURCE_SHA).decode("utf-8")
    derived = derive_text(original)
    before = {node.name: ast.dump(node) for node in ast.parse(original).body
              if isinstance(node, ast.FunctionDef) and node.name != "build"}
    after = {node.name: ast.dump(node) for node in ast.parse(derived).body
             if isinstance(node, ast.FunctionDef) and node.name != "build"}
    require(before == after, "Non-builder mechanics changed")
    compile(derived, "confirm_b129_context_replacement.py", "exec")
    output = write_frozen(TOOLS / "confirm_b129_context_replacement.py", derived.encode("utf-8"))
    print(json.dumps(freeze_json(review_dir(129) / "context-replacement-tooling-001.json", {
        "source": binding(source), "output": output, "producer": binding(Path(__file__)),
        "unchangedFunctions": list(before), "failure": binding(
            review_dir(129) / "confirm" / f"{FAILED_RUN}-superseded.json"),
        "scope": "First-confirmation replacement of an executed VOID run, not an unlaunched run "
                 "or an accepted-confirmation follow-up. Exact source spec, initial attribution, "
                 "audited unavailable context and candidate preserved. Access/report/RAM/context/"
                 "structure/final audit functions unchanged.",
        "reviewersLaunched": False,
    })))


if __name__ == "__main__":
    main()
