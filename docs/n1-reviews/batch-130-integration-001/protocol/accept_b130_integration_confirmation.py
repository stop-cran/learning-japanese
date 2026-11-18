"""Persist a separately written substantive decision after a clean integration audit."""
import json
import re
import sys
from pathlib import Path

from b130_context_confirmation import ROOT, binding
from b130_integration_lineage import CANDIDATE, RUNS, require_followup_preflight
from common import freeze_json, frozen, load_batch, require, sha
from confirm_b130_fresh_context import clean, preflight

OUT = ROOT / "confirm"


def read(item):
    return json.loads(frozen(item["path"], item["sha256"]))


def main(case_path):
    case = json.loads(frozen(case_path))
    family, run = case["family"], case["run"]
    require(family in RUNS and RUNS[family] == run, "Not an admitted integration followup")
    clean(load_batch(130), CANDIDATE)
    final_binding = binding(OUT / f"{run}-final.json")
    require(final_binding["sha256"] == case["finalSha"], "Observed mechanical final changed")
    final = read(final_binding)
    record, config = preflight(OUT / f"{run}-preflight.json")
    require_followup_preflight(record, config)
    require(final["candidate"] == record["candidate"] == CANDIDATE
            and final["session"] == record["session"]
            and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and final["confirmation"] == "CONFIRMED"
            and final["report"]["sha256"] == case["reportSha"], "Review identity or result differs")
    audit, context, structure = (read(final[key]) for key in ("audit", "context", "structure"))
    require("rawAudit" not in final and "controlAdjudication" not in final
            and audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK"
            and audit["actualResponseModels"] == [case["responseModel"]]
            and case["responseModel"].startswith("claude-" if family == "claude" else "gpt-")
            and audit["chainRead"] == audit["chainRequired"] == case["segments"]
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
            and audit["messages"] == ["CONFIRMED"] and audit["fetches"] == 0
            and audit["reviewerIdle"] and not audit["recordIncomplete"] and not audit["breaches"]
            and not audit["unexpectedUserMessages"], "Clean bounded-access audit failed")
    require(context["status"] == structure["status"] == "PASS" and not context["compactions"]
            and context["contextTiers"] == ["long_context"]
            and context["maxPromptTokens"] == [case["contextMax"]]
            and context["eventsSha256"] == audit["eventsSha256"]
            and structure["confirmation"] == "CONFIRMED"
            and set(structure["facets"].values()) == {"CLEAN"}
            and structure["dispositions"] == {}
            and structure["findings"] == structure["optionalPoints"] == 0
            and structure["limits"] == case["limits"], "Structure or context differs")
    frozen(Path(final["audit"]["path"]).parent / "events.jsonl", audit["eventsSha256"])
    chain_binding = binding(OUT / f"{run}-chain.json")
    sources = {}
    for segment in read(chain_binding)["segments"]:
        frozen(segment["path"], segment["sha256"])
        for part in segment["parts"]:
            value = (part["sha256"], part["sourceLines"])
            require(sources.setdefault(part["source"], value) == value, "Source identity differs")
    report = frozen(final["report"]["path"], case["reportSha"]).decode()
    citations = []
    for match in re.finditer(r"([\w./-]+\.(?:md|txt|xml|json|jsonl|log|patch)):(\d+)(?:-(\d+))?", report):
        source, first, last = match.groups()
        start, end = int(first), int(last or first)
        require(source in sources and 1 <= start <= end <= sources[source][1],
                "Unbound or out-of-range citation: " + match.group())
        citations.append({"source": source, "first": start, "last": end,
                          "sourceSha256": sources[source][0]})
    proof_binding = {"path": str(ROOT / "integration-evidence-001.json"),
                     "sha256": "ea21d87422c1af22703ae09d39c1a51747fe127db12a52293538e55a42836ffa"}
    proof = read(proof_binding)
    require(proof["candidate"] == CANDIDATE and proof["status"] == "PASS_INTEGRATION_BINDINGS_ONLY"
            and not proof["reviewAccepted"] and not proof["publicationAccepted"], "Mechanical proof differs")
    previous = json.loads(frozen(ROOT / "delta-evidence-001" / "verification.json",
                                  "0288e16198420c4e8b8b14a109ce6af2ac7cf4b8572468639b923aa59affa5a9"))
    old_logs = {row["gate"]: row["logSha256"] for row in previous["gateSets"]["committed"]["gates"]}
    changed_logs = [row["gate"] for row in proof["gateSets"]["committed"]["gates"]
                    if row["logSha256"] != old_logs[row["gate"]]]
    require(set(changed_logs) == {"unittest", "manifest", "manifest-rebuild", "budget"}
            and previous["retainedQuizSafetyWarnings"] == proof["retainedQuizSafetyWarnings"],
            "Actual changed gate output or warning set differs")
    runtime = read(proof["runtimeProof"])
    for name in ("incoming-article.md", "incoming-counter.json"):
        text = frozen(runtime["neutralInputs"][name]["path"], runtime["neutralInputs"][name]["sha256"]).decode()
        require(not any(char in text for char in "\u5840\u62cd\u8017"), "Incoming content contains a target character")
    citation_check = freeze_json(OUT / f"{run}-citation-check.json", {
        "report": final["report"], "chain": chain_binding, "citations": citations,
        "limits": "Source binding and line bounds only; semantic adjudication is recorded separately.",
    })
    adjudication = freeze_json(OUT / f"{run}-adjudication.json", {
        "batch": 130, "run": run, "family": family, "candidate": CANDIDATE,
        "session": record["session"], "originalSession": record["originalSession"],
        "report": final["report"], "final": final_binding, "prior": record["prior"],
        "reportReadCompletely": True, "verdict": "CONFIRMED", "dispositions": {},
        "acceptedNewFindings": [], "openClaimIds": [], "citationCheck": citation_check,
        "claimCheck": case["analysis"], "coordinatorChecked": case["coordinatorChecked"],
        "mechanicalProof": proof_binding, "actualChangedLogNames": changed_logs,
        "limitsPreserved": [f"L{i}" for i in range(1, case["limits"] + 1)],
        "scope": "Integration impact on the earlier N1 conclusions only. Incoming counter-language "
                 "correctness is not newly certified. Earlier snapshot-specific acceptance and all "
                 "lexical/image/unread-index/latent-reading/native/device/font/old-APK limits remain.",
        "decision": "ACCEPT_CONFIRMATION_ON_THIS_SNAPSHOT_ONLY",
        "rawAuditWasClean": True, "controlAdjudicationApplied": False,
        "publicationAccepted": False, "deliveryCredit": 0,
        "substantiveDecisionInput": binding(case_path), "producer": binding(__file__),
    })
    accepted = freeze_json(OUT / f"{run}-acceptance.json", {
        "batch": 130, "run": run, "family": family, "session": record["session"],
        "originalSession": record["originalSession"], "candidate": CANDIDATE, "verdict": "CONFIRMED",
        "reviewEvidenceAccepted": True, "confirmationAccepted": True, "acceptedNewFindings": [],
        "openClaimIds": [], "report": final["report"], "final": final_binding,
        "adjudication": adjudication,
    })
    print(json.dumps({"acceptance": accepted, "adjudication": adjudication}))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
