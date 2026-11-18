"""Record substantive acceptance of the two independently completed successor confirmations."""
import json
import re
from pathlib import Path

from b130_context_confirmation import ROOT, binding
from b130_followup_lineage_v2 import require_followup_preflight
from common import freeze_json, frozen, load_batch, load_module, require
from confirm_b130_fresh_context import clean, preflight
from verify_b130_revision_runtime_v2 import GPT_OPEN

CANDIDATE = "1ac4053c5da955c3afaafc1e879e63a98ee42526"
OUT = ROOT / "confirm"
CASES = {
    "gpt": {
        "run": "N1-B130-GPT-CONFIRM-003",
        "finalSha": "74e42e693edbc8d8ef9402485861a721880c901efd2b460d1e1638b855ca2283",
        "reportSha": "3feb374216d74b8baf53f40a4a34063431dcb7c5880cea5fc988d79e70d25da8",
        "responseModel": "gpt-6.1-sol", "segments": 34, "limits": 8, "contextMax": 922000,
        "classifier": "adjudicate_b130_gpt003_control.py",
        "analysis": "The original D18/L1 quiz-safety question is addressed by the actual direct "
                    "precaution, not by resolving the rare-spelling lexical allocation. The report "
                    "checks both complete decisive entries and the actual counterpart, distinguishes "
                    "direct symmetric policy from native execution, and correctly retains the original "
                    "UNVERIFIED result and citation erratum. No new defect or consequential unprotected "
                    "claim remains within this successor delta.",
    },
    "claude": {
        "run": "N1-B130-CLAUDE-CONFIRM-004",
        "finalSha": "7c61eb4e1ba01bfa4dcf06d23007b602f74e81374c525a97ec7cdecbaf8ffabe",
        "reportSha": "8e011d97109cf9c94ea7d6dc0b3ab887517d1c398e2394cb3a6972848dbc60f1",
        "responseModel": "claude-opus-5-5", "segments": 19, "limits": 5, "contextMax": 952000,
        "classifier": "adjudicate_b130_claude004_control.py",
        "analysis": "The report independently accepts the actual added precaution and qualified Notes, "
                    "using the two complete decisive families. Its prior bounded-noncollision acceptance "
                    "remains historical, not automatically transferred. The reduced record selection "
                    "is expressly disclosed; no new reading, etymology or full-card approval is inferred. "
                    "Unchanged curated options and host outputs support the bounded quiz consequence, "
                    "not native execution or unrestricted pool safety.",
    },
}


def read(item):
    return json.loads(frozen(item["path"], item["sha256"]))


def accept(family, case):
    run = case["run"]
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
    require(audit["actualResponseModels"] == [case["responseModel"]]
            and audit["chainRead"] == audit["chainRequired"] == case["segments"]
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
            and audit["messages"] == ["CONFIRMED"] and audit["fetches"] == 0
            and audit["reviewerIdle"] and not audit["recordIncomplete"] and not audit["breaches"]
            and not audit["unexpectedUserMessages"], "Bounded access audit failed")
    require(context["status"] == structure["status"] == "PASS" and not context["compactions"]
            and context["contextTiers"] == ["long_context"]
            and context["maxPromptTokens"] == [case["contextMax"]]
            and context["eventsSha256"] == audit["eventsSha256"]
            and structure["confirmation"] == "CONFIRMED"
            and set(structure["facets"].values()) == {"CLEAN"}
            and structure["dispositions"] == {}
            and structure["findings"] == structure["optionalPoints"] == 0
            and structure["limits"] == case["limits"], "Structure or context differs")
    require(final["rawAudit"] == audit["rawAudit"]
            and final["controlAdjudication"] == audit["controlAdjudication"],
            "Control adjudication is not carried through the final result")
    raw_audit, control = read(final["rawAudit"]), read(final["controlAdjudication"])
    require(raw_audit["status"] == "HOLD" and raw_audit["unexpectedUserMessages"] == 1
            and raw_audit["eventsSha256"] == audit["eventsSha256"]
            and control["rawAudit"] == final["rawAudit"]
            and control["rawUnexpectedUserMessages"] == control["classifiedRuntimeCompletionReminders"] == 1,
            "Original control hold was hidden or relabelled")
    raw = frozen(control["events"]["path"], audit["eventsSha256"])
    events = [json.loads(line) for line in raw[raw_audit["offset"]:].splitlines()]
    classifier_path = Path(__file__).with_name(case["classifier"])
    require(control["producer"] == binding(classifier_path), "Control classifier changed")
    load_module("b130_accept_control_" + family, classifier_path).classify_control(events)
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
    citation_check = freeze_json(OUT / f"{run}-citation-check.json", {
        "report": final["report"], "chain": chain_binding, "citations": citations,
        "limits": "Source binding and line bounds only, not automatic semantic validation.",
    })
    prior = read(record["prior"])
    adjudication = freeze_json(OUT / f"{run}-adjudication.json", {
        "batch": 130, "run": run, "family": family, "candidate": CANDIDATE,
        "session": record["session"], "originalSession": record["originalSession"],
        "report": final["report"], "final": final_binding, "prior": record["prior"],
        "reportReadCompletely": True, "verdict": "CONFIRMED", "dispositions": {},
        "acceptedNewFindings": [], "openClaimIds": [], "citationCheck": citation_check,
        "claimCheck": case["analysis"],
        "coordinatorChecked": [
            "Full current拍 and響 cards; exact added direct guard and qualified Notes.",
            "Both complete decisive JMdict1238610/1408810 entries, including rare spelling and all senses.",
            "Actual runtime/source-reuse/integrated preservation proofs and unchanged curated choices.",
            "Both complete reviewer reports; own-prior lineage, bounded access and source/citation identities.",
        ],
        "lexicalAllocation": "UNRESOLVED_AND_GUARDED; no ordinary synonymy or new proved defect asserted",
        "historicalOriginalQuestions": list(GPT_OPEN) if family == "gpt" else [],
        "priorVerdictPreserved": prior["verdict"],
        "originalD18": "QUIZ_CONSEQUENCE_PROTECTED; LEXICAL_UNCERTAINTY_RETAINED",
        "limitsPreserved": [f"L{i}" for i in range(1, case["limits"] + 1)],
        "enduringLimits": "All prior historical glyph/rare spelling/source-allocation, index-only unread "
                          "comparison, font cmap/rendering, host-only/latent reading, custom/multiple-borrow "
                          "pool, native/device and older-APK limits remain. No whole-corpus safety claim.",
        "rawAudit": final["rawAudit"], "controlAdjudication": final["controlAdjudication"],
        "decision": "ACCEPT_CONFIRMATION_ON_THIS_SNAPSHOT_ONLY",
        "publicationAccepted": False, "deliveryCredit": 0, "producer": binding(__file__),
    })
    return freeze_json(OUT / f"{run}-acceptance.json", {
        "batch": 130, "run": run, "family": family, "session": record["session"],
        "originalSession": record["originalSession"], "candidate": CANDIDATE, "verdict": "CONFIRMED",
        "reviewEvidenceAccepted": True, "confirmationAccepted": True, "acceptedNewFindings": [],
        "openClaimIds": [], "report": final["report"], "final": final_binding,
        "adjudication": adjudication, "rawAudit": final["rawAudit"],
        "controlAdjudication": final["controlAdjudication"],
    })


def main():
    clean(load_batch(130), CANDIDATE)
    accepted = {family: accept(family, case) for family, case in CASES.items()}
    print(json.dumps(freeze_json(ROOT / "delta-confirmation-acceptances-001.json", {
        "candidate": CANDIDATE, "confirmations": accepted, "published": False,
        "delivered": 261, "remaining": 967, "deliveryCredit": 0,
        "next": "Six-run closure with prepared-only history and original/adjudicated control audits; "
                "then signed publication, CI, served runtime/archive equality and owner checkpoint.",
        "producer": binding(__file__),
    })))


if __name__ == "__main__":
    main()
