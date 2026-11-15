"""Replace an unlaunched assignment after proven context exhaustion, not a verdict."""
import json
from pathlib import Path

from common import frozen, load_module, require, sha
from confirm_followup import run_number, verify_prior


def read(item):
    return json.loads(frozen(Path(item["path"]), item["sha256"]))


def require_identity(spec, source, unavailable):
    expected = {**source, "run": spec["run"], "session": spec["session"],
                "replayedFrom": spec["replayedFrom"], "unavailable": spec["unavailable"]}
    require(spec == expected and "reviewerOrigin" not in source,
            "Replacement changes the original assignment's scope or lineage")
    require(spec["batch"] == source["batch"] == 123
            and spec["session"] != source["session"] == unavailable["session"]
            and spec["family"] == source["family"] == unavailable["family"] == "claude"
            and source["run"] == unavailable["run"]
            and spec["candidate"] == source["candidate"] == unavailable["candidate"],
            "Replacement must use a fresh same-family context on the same snapshot")
    require(source["basis"] == "accepted-confirmation"
            and run_number(123, source["run"]) < run_number(123, spec["run"]),
            "Replacement must follow the unchanged accepted-snapshot assignment")
    require(unavailable["status"] == "UNLAUNCHED_CONTEXT_COMPACTION"
            and unavailable["reviewEvidenceAccepted"] is False
            and unavailable["confirmationAccepted"] is False,
            "Unavailable assignment is not an acceptance or an executed confirmation")


def verify_replacement(spec, config, records):
    source, unavailable = read(spec["replayedFrom"]), read(spec["unavailable"])
    require_identity(spec, source, unavailable)
    initial, prior, previous = verify_prior(source, config, records)
    require(spec["session"] != prior["session"], "Replacement reuses the exhausted context")
    context, void, receipt = (read(unavailable[key])
                              for key in ("context", "voidExecution", "admissionRefusal"))
    audit = read(void["audit"])
    require(context["status"] == "FAIL" and context["compactions"]
            and void["status"] == "VOID_EXECUTION"
            and void["reviewEvidenceAccepted"] is False and void["confirmationAccepted"] is False
            and void["candidate"] == spec["candidate"]
            and audit["session"] == source["session"] and audit["status"] == "VOID"
            and audit["breaches"] and audit["reviewerIdle"]
            and audit["eventsSha256"] == context["eventsSha256"],
            "Context-unavailability proof or preserved void execution differs")
    events = Path(void["audit"]["path"]).parent / "events.jsonl"
    frozen(events, audit["eventsSha256"])
    checker_path = records / "check-run-context.py"
    frozen(checker_path)
    checked = load_module("b123_unavailable_checker", checker_path).check(events)
    require(all(checked[key] == context[key] for key in
                ("status", "errors", "eventsSha256", "contextTiers", "maxPromptTokens", "compactions")),
            "Context diagnosis cannot be reproduced from the frozen audit")
    frozen(Path(void["report"]["path"]), void["report"]["sha256"])
    expected_preflight = records / "confirm" / f"{source['run']}-preflight.json"
    log = frozen(Path(unavailable["admissionLog"]["path"]), unavailable["admissionLog"]["sha256"])
    require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 1
            and receipt["memory"]["breach"] is None
            and str(expected_preflight) in receipt["command"]
            and receipt["logSha256"] == sha(log)
            and b"ValueError: Context failed or changed" in log,
            "No exact context-admission refusal for the unlaunched assignment")
    out = records / "confirm"
    require(not (out / f"{source['run']}-admission.json").exists()
            and not (out / f"{source['run']}-final.json").exists()
            and not (Path(config["repo"]).parent / "reports-123" / f"{source['run']}.md").exists(),
            "Do not relabel an admitted or executed assignment as unlaunched")
    return initial, prior, previous


def render_replacement_prompt(text):
    replacements = (
        ("confirmation of your own accepted B123 previous confirmation",
         "fresh same-family replacement review of a delta after an accepted B123 confirmation"),
        ("names your prior confirmation report", "names the original reviewer's confirmation report"),
        ("Your own previous confirmation report:", "Original reviewer's accepted confirmation report:"),
        ("your own unchanged previous confirmation report", "the original reviewer's unchanged confirmation report"),
        ("Read your own full report", "Read the supplied prior full report"),
        ("Your prior report has no numbered", "The prior report has no numbered"),
        ("including changes not requested by you", "including changes not requested in the prior report"),
        ("No other reviewer's report or held-run observations are supplied or authorized.",
         "Only the supplied same-family historical reports are context. "
         "No void-run conclusions or other-family reports are supplied or authorized."),
        ("Your prior CONFIRMED report remains accepted", "The prior reviewer's CONFIRMED report remains accepted"),
    )
    for old, new in replacements:
        require(text.count(old) == 1, f"Replacement prompt anchor changed: {old}")
        text = text.replace(old, new)
    return text + (
        "\nFRESH REVIEWER IDENTITY\n"
        "You did not author any historical report and have no retained firsthand review context. "
        "Re-establish the actual subsequent delta from the complete supplied sources. "
        "Earlier unchanged teaching is covered by the archived accepted reviews, not a new full-batch review. "
        "The original context is unavailable; its invalid later execution and conclusions are excluded. "
        "Preserve prior limits and report missing consequential evidence as UNVERIFIED.\n"
        "\nDEPENDENT OUTPUT OPERATIONS\n"
        "Creating the report and reading it back are dependent operations. Issue the creation call alone. "
        "Wait for its successful tool result before issuing the readback in a separate response. "
        "After a successful readback, send the sole verdict in another separate response. "
        "Never batch these calls or repair a failed call with a retry.\n"
    )
