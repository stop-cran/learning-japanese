"""Record the coordinator's bounded adjudication of the second B118 correction."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import WS, freeze_json, frozen, git, load_batch, require, sha
from confirm_v2 import binding, clean

HERE = Path(__file__).resolve().parent
RUN = "N1-B118-CLAUDE-002-CONFIRM-003"
CANDIDATE = "a7b4edfb3d3c3bfcc061cfbdd0ee04de1e53204e"
spec_path, final_path = HERE / f"{RUN}-spec.json", HERE / f"{RUN}-final.json"
spec = json.loads(frozen(spec_path))
final = json.loads(frozen(final_path, "e74eb412d77fc793d9cc82b80042eed19fed64ab50486079180126092aca061e"))
config = load_batch(118)
clean(config, CANDIDATE)
require(spec["candidate"] == CANDIDATE and spec["family"] == "claude"
        and spec["basis"] == "accepted-confirmation", "Unexpected follow-up spec")
prior = json.loads(frozen(Path(spec["prior"]["path"]), spec["prior"]["sha256"]))
require(prior["confirmationAccepted"] and prior["verdict"] == "CONFIRMED"
        and prior["openClaimIds"] == [], "Earlier acceptance changed")
require(final["run"] == RUN and final["candidate"] == CANDIDATE
        and final["session"] == spec["session"] and final["confirmation"] == "CONFIRMED"
        and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
        "Unexpected confirmation result")
audit, context, structure = (
    json.loads(frozen(Path(final[key]["path"]), final[key]["sha256"]))
    for key in ("audit", "context", "structure"))
require(context["status"] == structure["status"] == "PASS" and not context["compactions"]
        and not audit["breaches"] and audit["reviewerIdle"]
        and audit["chainRead"] == audit["chainRequired"] == 44
        and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
        and audit["fetches"] == 0 and not audit["unexpectedUserMessages"]
        and audit["eventsSha256"] == context["eventsSha256"]
        and structure["dispositions"] == {} and structure["findings"] == 0
        and structure["optionalPoints"] == 1 and structure["limits"] == 5
        and not structure["nonAccepting"] and set(structure["facets"].values()) == {"CLEAN"},
        "Audit or structure changed")
require(audit["actualResponseModels"]
        and all("claude" in model.lower() for model in audit["actualResponseModels"]),
        "Claude response identity not verified")
report = frozen(Path(final["report"]["path"]), final["report"]["sha256"]).decode("utf-8").replace("\r\n", "\n")
require("## Findings\nNone." in report and "### O1: Broadened examination rationale" in report,
        "Inspected report changed")
proof_path = WS / "scratch-118" / "revision-verification-002" / "revision-verification.json"
proof = json.loads(frozen(proof_path, "02288e9c86fa4b9009183171043c85013dfd7a5c0b0d823b63d1cd0ebfbd09f0"))
card = git(config, "show", f"{CANDIDATE}:kanji/析.md")
require(sha(card) == proof["targetCardSha256"]
        == sha((Path(config["repo"]) / "kanji" / "析.md").read_bytes().replace(b"\r\n", b"\n")),
        "L2 normalization differs")
adjudication = {
    "run": RUN, "family": "claude", "session": spec["session"], "candidate": CANDIDATE,
    "status": "ACCEPTED_BOUNDED_CONFIRMATION", "verdict": "CONFIRMED",
    "reviewEvidenceAccepted": True, "confirmationAccepted": True, "publicationAccepted": False,
    "final": binding(final_path), "report": final["report"], "prior": spec["prior"],
    "audit": final["audit"], "context": final["context"], "structure": final["structure"],
    "actualResponseModels": audit["actualResponseModels"], "eventsSha256": audit["eventsSha256"],
    "acceptedDispositions": {}, "acceptedNewFindings": [], "openClaimIds": [],
    "substantiveBasis": [
        "Coordinator read the complete captured Daijisen text sections for all twelve comparisons and the target, the actual revised card and individual dispositions. The source-backed physical separation and analytic examination senses support the eleven new direct guards; Notes qualify overlap rather than asserting interchangeability.",
        "The source defines 論 as stating reasoned positions, opinions and theories, whereas 析 divides and disentangles material. The bounded no-new-guard decision is supported by this positive distinction, not mere absence of a matching English gloss.",
        "Earlier exclusions, metadata, strokes, support links and curated distractors remain unchanged. Verified runtime delta is only 析. Ten hash-bound gates and the unchanged modelled option fill support host-level consistency, not arbitrary-pool acceptance.",
    ],
    "optionalDispositions": {
        "O1": "Optional, not an established defect. The reviewer still judges 判/診/試 harmless and identifies no defensible wrong-labelled option. Precautionary extra guards do not establish a transitive equivalence or require every judgment/examination character to be guarded. No new teaching change is warranted from this low-confidence process suggestion."
    },
    "limitDispositions": {
        "L1": "Retain previous raw-source, geometry and manifest review limits. Hash verification is not a fresh reviewer read.",
        "L2": "Resolved mechanically: committed 析 bytes match the CRLF-normalized worktree and the revision proof's targetCardSha256.",
        "L3": "Host models only; no caller-built/multi-borrow, Kotlin/native/device, installed-APK or publication acceptance.",
        "L4": "Bounded editorial judgment, not native certification or exhaustive corpus review; unassessed pairs remain outside the claim.",
        "L5": "Exact HTML slices and reversible LF display derivatives remain hash-bound; author-stripped text does not replace those originals.",
    },
    "acceptanceLimit": "Claude acceptance applies to a7b4edfb only. GPT must independently confirm that revision before closure and publication.",
    "revisionProof": binding(proof_path), "spec": binding(spec_path), "tool": binding(Path(__file__)),
}
adj = freeze_json(HERE / f"{RUN}-adjudication.json", adjudication)
print(json.dumps(freeze_json(HERE / f"{RUN}-acceptance.json", {
    "run": RUN, "family": "claude", "batch": 118, "session": spec["session"],
    "candidate": CANDIDATE, "verdict": "CONFIRMED",
    "reviewEvidenceAccepted": True, "confirmationAccepted": True,
    "openClaimIds": [], "acceptedNewFindings": [], "dispositions": {},
    "report": final["report"], "final": binding(final_path), "adjudication": adj,
    "acceptanceLimit": adjudication["acceptanceLimit"],
})))
