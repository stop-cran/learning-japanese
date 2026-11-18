"""Preserve a void dependent-call race and prepare source-backed serial retries."""
import copy
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen
from confirm_followup import build_followup
from confirm_v2 import binding
from verify_b123_revision_v4 import CAPTURE, CAPTURE_SHA, check_source_reference

REVIEW = WS / "scratch-123" / "review"
OUT = REVIEW / "confirm"
VOID_RUN = "N1-B123-CLAUDE-CONFIRM-003"
AUDIT = OUT / VOID_RUN / "audit-20261115T192518230263" / "audit.json"


def main():
    audit = json.loads(frozen(AUDIT))
    require(audit["status"] == "VOID" and audit["chainRead"] == audit["chainRequired"] == 21
            and audit["writes"] == 1 and audit["readbacks"] == 2
            and set(audit["breaches"]) == {
                "More than one tool call in one model response",
                "Tool call while a previous call is outstanding",
                "Invalid report readback",
            }, "Unexpected refusal; investigate instead of replacing its reason")
    calls = audit["calls"]
    write = next(call for call in calls if call["name"] == "create")
    failed = next(call for call in calls if call.get("role") == "report-readback" and not call["success"])
    require(write["event"] == failed["event"], "Dependent-call race not established")
    report_path = WS / "reports-123" / f"{VOID_RUN}.md"
    report = report_path.read_bytes()
    require(sha(report.decode("utf-8").replace("\r\n", "\n").encode("utf-8")) == write["writtenSha256"],
            "Void report no longer matches its audited write")
    report_path.chmod(0o444)
    report_copy = write_frozen(OUT / f"{VOID_RUN}-void-report.md", report)
    bounded = {key: value for key, value in audit.items() if key not in ("calls", "modelRecords")}
    bounded["representation"] = "Bounded derivative; complete frozen audit and events remain local."
    audit_copy = freeze_json(OUT / f"{VOID_RUN}-void-audit-summary.json", bounded)
    void = freeze_json(OUT / f"{VOID_RUN}-superseded.json", {
        "run": VOID_RUN, "candidate": "60db6255f5c74bc039884d13640966dbe74fee99",
        "status": "VOID_EXECUTION", "rawVerdict": "CONFIRMED",
        "reviewEvidenceAccepted": False, "confirmationAccepted": False,
        "reason": "Report creation and dependent readback were issued in one response; readback failed "
                  "before creation completed, then was retried. All 21 source reads succeeded, but the "
                  "serial execution contract was breached. No audit criterion is waived.",
        "audit": binding(AUDIT), "report": binding(report_path),
        "archivalCopies": [report_copy, audit_copy], "replacementRun": "N1-B123-CLAUDE-CONFIRM-004",
    })
    phrases_path = REVIEW / "followup-004-source-phrases.json"
    phrases = json.loads(phrases_path.read_bytes())
    capture = json.loads(frozen(CAPTURE, CAPTURE_SHA))
    signed_path = WS / "b123-worktree" / "docs" / "n1-sources" / "batch-123" / "reconciliation-003" / "source-manifest.json"
    references = json.loads(signed_path.read_bytes())["sources"]
    require(len(phrases["sources"]) == 9
            and {s["character"] for s in phrases["sources"]} == {s["character"] for s in capture["sources"]},
            "Source-phrase scope differs")
    for source in capture["sources"]:
        selected = next(s for s in phrases["sources"] if s["character"] == source["character"])
        signed = next(s for s in references if s["character"] == source["character"])
        reference = {**signed, **selected}
        check_source_reference(reference, source, frozen(source["extract"]["path"], source["extract"]["sha256"]))
    phrases_path.chmod(0o444)
    freeze_json(REVIEW / "followup-004-source-phrase-verification.json", {
        "sourcePhrases": binding(phrases_path), "capture": {"path": str(CAPTURE), "sha256": CAPTURE_SHA},
        "verifiedQuotes": sum(len(item["quotes"]) for item in phrases["sources"]),
        "completeCapturesRedistributed": False, "confirmationAccepted": False,
    })
    for family in ("claude", "gpt"):
        old = OUT / f"N1-B123-{family.upper()}-CONFIRM-003-spec.json"
        spec = copy.deepcopy(json.loads(frozen(old)))
        spec["run"] = f"N1-B123-{family.upper()}-CONFIRM-004"
        spec["additionalSources"].append({**binding(phrases_path), "source": "source-references/direct-phrases.json"})
        path = OUT / f"{spec['run']}-spec.json"
        freeze_json(path, spec)
        if family == "gpt":
            require(not (WS / "reports-123" / "N1-B123-GPT-CONFIRM-003.md").exists()
                    and not (OUT / "N1-B123-GPT-CONFIRM-003-admission.json").exists(),
                    "Do not supersede an admitted or completed assignment")
            freeze_json(OUT / "N1-B123-GPT-CONFIRM-003-superseded.json", {
                "run": "N1-B123-GPT-CONFIRM-003", "status": "UNLAUNCHED_SOURCE_SUPPLEMENT",
                "originalSpec": binding(old), "replacementSpec": binding(path),
                "reason": "Add verified short primary-source phrases alongside the original summaries; "
                          "same candidate, original reviewer and held CONFIRM-002 lineage.",
            })
        build_followup(path)
    print(json.dumps({"void": void, "newRuns": ["N1-B123-CLAUDE-CONFIRM-004", "N1-B123-GPT-CONFIRM-004"],
                      "reviewersLaunched": False}))


if __name__ == "__main__":
    main()
