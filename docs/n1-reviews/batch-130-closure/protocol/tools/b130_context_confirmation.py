"""Disclose a fresh-context confirmation before consuming a nearly full reviewer."""
import ast
import json
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, write_frozen
from prepare_b130_confirmations import REVIEWERS, ROOT
from verify_b130_revision_runtime_v3 import INITIAL_SHA, PARENT

ENGINE_SHA = "f18dd4515b7ea2f351f9064f69edc299db67c23507c2f697715b04ea4121bdf3"
OBSERVATION_SHA = "f9b3b3428f3a511de1cdec6bab4797b48f7ccbab0986948963d377ea519cff10"
OBSERVATION = ROOT / "confirmation-capacity-observation-001.json"


def binding(path):
    return {"path": str(path), "sha256": sha(frozen(path))}


def check_lineage(spec, source, config, accepted, launch, observation):
    family = spec["family"]
    require(family in REVIEWERS and spec["batch"] == source["batch"] == config["batch"] == 130
            and source["family"] == family and spec["run"] != source["run"]
            and source["run"] == f"N1-B130-{family.upper()}-CONFIRM-001"
            and source["session"] == spec["originalSession"] == launch["session"] == REVIEWERS[family]
            and spec["session"] != spec["originalSession"], "Incorrect fresh-reviewer attribution")
    expected = {**source, "run": spec["run"], "session": spec["session"],
                "originalSession": source["session"], "replayedFrom": spec["replayedFrom"],
                "contextObservation": spec["contextObservation"]}
    require(spec == expected, "Fresh context changed the frozen source assignment")
    require(accepted["reviewAccepted"] is True and accepted["candidate"] == config["candidate"] == PARENT
            and accepted["run"] == f"N1-B130-{family.upper()}-004"
            and spec["acceptance"]["sha256"] == INITIAL_SHA[family]
            and observation["candidate"] == spec["candidate"] == source["candidate"]
            and observation["status"] == "NOT_ADMITTED_CONTEXT_RISK",
            "Accepted initial or actual successor changed")
    row = observation["reviewers"][family]
    require(row["session"] == source["session"] and row["plannedRun"] == source["run"]
            and row["observedCompactions"] == []
            and 0 < row["lastUsage"]["inputTokens"] < row["lastUsage"]["maxPromptTokens"]
            and row["plannedSegments"] > 0 and row["plannedChainBytes"] > 0,
            "Actual pre-admission observation changed")


def verify_replacement(spec, config, accepted, launch, records):
    family = spec["family"]
    source_path = records / "confirm" / f"N1-B130-{family.upper()}-CONFIRM-001-spec.json"
    require(spec["replayedFrom"] == binding(source_path)
            and spec["contextObservation"] == binding(OBSERVATION), "Wrong retained pre-admission lineage")
    source = json.loads(frozen(source_path))
    observation = json.loads(frozen(OBSERVATION, OBSERVATION_SHA))
    check_lineage(spec, source, config, accepted, launch, observation)
    preflight_path = records / "confirm" / (source["run"] + "-preflight.json")
    preflight = json.loads(frozen(preflight_path))
    old_config = json.loads(frozen(preflight["config"]["path"], preflight["config"]["sha256"]))
    for item in old_config["files"]:
        frozen(item["path"], item["sha256"])
    chain = json.loads(frozen(preflight["chain"]["path"], preflight["chain"]["sha256"]))
    require(preflight["session"] == source["session"]
            and preflight["candidate"] == source["candidate"]
            and len(chain["segments"]) == observation["reviewers"][family]["plannedSegments"],
            "Prepared chain or source identity changed")
    require(not (records / "confirm" / (source["run"] + "-admission.json")).exists()
            and not Path(old_config["report"]).exists()
            and preflight["segments"] == observation["reviewers"][family]["plannedSegments"],
            "Prepared-only predecessor was executed; inspect rather than relabel it")
    return [binding(source_path), binding(OBSERVATION), binding(preflight_path),
            preflight["config"], preflight["chain"], binding(Path(__file__))]


def replacement_prompt(text):
    substitutions = (
        ("confirmation of your own accepted B130 initial review",
         "same-family fresh-context confirmation of the accepted B130 initial review"),
        ("Your own initial report:", "Original reviewer's initial report:"),
        ("your own unchanged initial report", "the original reviewer's unchanged initial report"),
        ("Read your own full report", "Read the original reviewer's full report"),
        ("including changes not requested by you", "including changes not requested in the original report"),
    )
    for before, after in substitutions:
        require(text.count(before) == 1, "Unexpected attribution wording")
        text = text.replace(before, after)
    require("your own" not in text, "Historical authorship remains misattributed")
    return text + (
        "\nFRESH CONTEXT AND HISTORICAL ATTRIBUTION\n"
        "You are a new same-family reviewer, not the author of the initial report. The initial "
        "report remains accepted historical evidence with its own limits. Its original session "
        "has a large retained context; this new session prevents a foreseeable compaction risk. "
        "The original session's prepared confirmation was never admitted or executed: it is NOT "
        "a failed or accepted review, and no new linguistic conclusions exist to carry forward. "
        "This is informed bounded confirmation, not a new blind initial review or a claim that "
        "you retain the original reviewer's firsthand context. Read the entire chain and "
        "independently assess the actual changes and every supplied proposed disposition, including "
        "qualified precautions and bounded noncollisions. No missing or consequential uncertain "
        "claim can support CONFIRMED. All source, access, context, reporting, isolation and final "
        "audit requirements remain unchanged. No publication or delivery credit is authorized.\n"
    )


def derive_text(text):
    original = text.replace("\r\n", "\n")
    substitutions = (
        ("PINS = {", "from b130_context_confirmation import verify_replacement, replacement_prompt\n\nPINS = {"),
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
         '              "replacementReason": "pre-admission-context-capacity",\n'
         '              "replayedFrom": spec["replayedFrom"], "contextObservation": spec["contextObservation"],\n'
         '              "run": run, "batch": spec["batch"], "session": spec["session"], "candidate": spec["candidate"],'),
    )
    result = original
    for before, after in substitutions:
        require(result.count(before) == 1, "Unexpected confirmation builder anchor")
        result = result.replace(before, after)
    functions = lambda value: {node.name: ast.dump(node) for node in ast.parse(value).body
                               if isinstance(node, ast.FunctionDef) and node.name != "build"}
    require(functions(original) == functions(result), "Access/final-audit mechanics changed")
    return result


def main():
    source = TOOLS / "confirm_b130_compact.py"
    derived = derive_text(frozen(source, ENGINE_SHA).decode("utf-8"))
    compile(derived, "confirm_b130_fresh_context.py", "exec")
    output = write_frozen(TOOLS / "confirm_b130_fresh_context.py", derived.encode("utf-8"))
    print(json.dumps(freeze_json(ROOT / "fresh-confirmation-tooling-001.json", {
        "source": binding(source), "output": output, "producer": binding(Path(__file__)),
        "capacityObservation": binding(OBSERVATION), "reviewersLaunched": False,
        "decision": "The user was unavailable and explicitly directed autonomous decisions. Use "
                    "fresh same-family contexts with fully disclosed attribution rather than launch "
                    "foreseeably overfull originals or truncate complete evidence. Existing reviewer "
                    "model/context settings are to be inherited, without overrides.",
        "scope": "Only builder lineage and accurate historical attribution differ. All other "
                 "engine functions are AST-identical. Unadmitted001 preparations remain local "
                 "prepared artifacts, not fabricated failed reviews. Closure support for this "
                 "explicit fresh-context origin must be added before acceptance/publication.",
    })))


if __name__ == "__main__":
    main()
