"""Preserve the GPT follow-up as accepted evidence, not publication acceptance."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import freeze_json, frozen, git, load_batch, require
from confirm_v2 import binding, clean

HERE = Path(__file__).resolve().parent
RUN = "N1-B118-GPT-001-CONFIRM-002"
CANDIDATE = "fa2f64f2472cf9ef10b8ac5f48db14dcaa248cd2"
spec_path, final_path = HERE / f"{RUN}-spec.json", HERE / f"{RUN}-final.json"
spec = json.loads(frozen(spec_path))
final = json.loads(frozen(final_path, "c5b787c4d8dc07fca02bbab91534cdf268d1401f635289dd1d225192e6cd10b6"))
config = load_batch(118)
clean(config, CANDIDATE)
require(spec["candidate"] == CANDIDATE and spec["family"] == "gpt", "Unexpected spec")
frozen(Path(spec["acceptance"]["path"]), spec["acceptance"]["sha256"])
require(final["run"] == RUN and final["candidate"] == CANDIDATE
        and final["session"] == spec["session"]
        and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
        and final["confirmation"] == "NEEDS FIX", "Unexpected confirmation final")
audit, context, structure = (
    json.loads(frozen(Path(final[key]["path"]), final[key]["sha256"]))
    for key in ("audit", "context", "structure"))
require(context["status"] == structure["status"] == "PASS" and not context["compactions"]
        and not audit["breaches"] and audit["reviewerIdle"] and audit["fetches"] == 0
        and audit["chainRead"] == audit["chainRequired"] == 35
        and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
        and not audit["unexpectedUserMessages"]
        and audit["eventsSha256"] == context["eventsSha256"]
        and audit["actualResponseModels"] == ["gpt-6.1-sol"]
        and structure["dispositions"] == {"F1": "RESOLVED"}
        and structure["findings"] == 1 and structure["optionalPoints"] == 0
        and structure["limits"] == 9 and not structure["nonAccepting"]
        and structure["facets"]["Consistency and quiz safety"] == "NEEDS FIX",
        "Confirmation gate mismatch")
report = frozen(Path(final["report"]["path"]), final["report"]["sha256"]).decode("utf-8")
require("### F1: Close-study option still overlaps analysis" in report
        and f"Commit: {CANDIDATE}" in report, "Report changed after substantive inspection")
card = git(config, "show", f"{CANDIDATE}:kanji/析.md").decode("utf-8")
require("quiz_exclusions: [分, 解, 割, 切, 破, 剖, 板, 別, 離, 刻, 盤]" in card, "Exclusions differ")
comparison = HERE.parent / "reconciliation-001" / "comparison-cards" / "研.md"
require("title: polish; study closely" in frozen(comparison).decode("utf-8"), "Comparison label differs")
adjudication = {
    "run": RUN, "family": "gpt", "session": final["session"], "candidate": CANDIDATE,
    "status": "ACCEPTED_BOUNDED_NEEDS_FIX_EVIDENCE", "verdict": "NEEDS FIX",
    "reviewEvidenceAccepted": True, "confirmationAccepted": False, "publicationAccepted": False,
    "final": binding(final_path), "report": final["report"],
    "audit": final["audit"], "context": final["context"], "structure": final["structure"],
    "actualResponseModels": audit["actualResponseModels"], "eventsSha256": audit["eventsSha256"],
    "acceptedDispositions": structure["dispositions"],
    "acceptedNewFindings": ["F1"], "openClaimIds": ["F1", "L2"],
    "prior": spec["acceptance"],
    "substantiveBasis": [
        "The initial GPT F1 (missing direct 別/離 guards) is resolved. Confirmation-local F1 is a distinct claim and must not be confused with the initial F1.",
        "Accept confirmation F1: the actual 研 title is polish; study closely. Its independent KANJIDIC2 record positively lists study of, while the independent 析 record lists analyze. Close study is a defensible broad description of analysis. This is a displayed-answer ambiguity, not a claim that the Japanese characters or compounds are interchangeable.",
        "Coordinator directly read the 研 comparison card, complete 研 and 析 records, target Daijisen section and revised 析 card. The direct 析/研 exclusion is absent at both endpoints. Preserve all existing guards and add this direct pair, preferably on the new 析 card to avoid changing baseline teaching.",
        "The remaining L2 boundaries are unresolved claims, not proven additional missing-pair findings. Complete metadata records and absence of identical English gloss strings do not alone prove harmlessness. Obtain positive source-backed sense discrimination, or add an independently justified direct guard, for each identified consequential pair.",
    ],
    "remainingComparisonScope": ["断", "絶", "折", "究", "査", "調", "察", "考", "討", "論", "批"],
    "sourceBindings": [
        binding(comparison),
        binding(HERE.parent / "reconciliation-001" / "kanjidic2-records.xml"),
        binding(HERE.parent.parent / "neutral-source-sections-001" / "daijisen.html"),
    ],
    "limitDispositions": {
        "L1": "Bounded same-reviewer confirmation; original index not freshly read. Preserve the original limitation.",
        "L2": "Open. Author must individually revisit the named consequential semantic boundaries; this is not a mandate to exclude every related operation.",
        "L3": "Comparison cards were read; separately cited character entries were not all supplied. Preserve that limit and supply relevant complete source sections for claims used in the next disposition.",
        "L4": "Unchanged source-only readings and geometry limitations; no native or stroke-rendering acceptance.",
        "L5": "Bounded host models only; no arbitrary-pool, Kotlin, native/device or installed-APK acceptance.",
        "L6": "Unchanged supporting-word and source-specific reading evidence remains bounded; no new defect identified.",
        "L7": "Verified gate receipts support the unchanged candidate but are not linguistic proof or publication acceptance.",
        "L8": "Coordinator previously resolved worktree/blob hash difference through CRLF normalization; original inventory/report remain unchanged. Reserialized XML and terminal-LF source-display derivatives remain explicitly disclosed.",
        "L9": "Publication is pending; delivered accounting remains 246/1228.",
    },
    "acceptanceLimit": "Accepted NEEDS FIX evidence only. Reconcile F1 and consequential L2 claims, obtain a new owner-signed candidate, then confirm the delta serially with both original families. The earlier Claude acceptance remains valid only for fa2f64f2.",
    "spec": binding(spec_path), "tool": binding(Path(__file__)),
}
adj = freeze_json(HERE / f"{RUN}-adjudication.json", adjudication)
print(json.dumps(freeze_json(HERE / f"{RUN}-acceptance.json", {
    "run": RUN, "family": "gpt", "batch": 118, "session": final["session"],
    "candidate": CANDIDATE, "verdict": "NEEDS FIX",
    "reviewEvidenceAccepted": True, "confirmationAccepted": False,
    "openClaimIds": ["F1", "L2"], "acceptedNewFindings": ["F1"],
    "dispositions": structure["dispositions"], "report": final["report"],
    "final": binding(final_path), "adjudication": adj,
    "acceptanceLimit": adjudication["acceptanceLimit"],
})))
