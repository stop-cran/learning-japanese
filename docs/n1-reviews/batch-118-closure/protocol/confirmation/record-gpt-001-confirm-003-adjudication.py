"""Record the coordinator's bounded adjudication of GPT's confirmation of the second B118 correction."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import WS, freeze_json, frozen, git, load_batch, require, sha
from confirm_v2 import binding, clean

HERE = Path(__file__).resolve().parent
RUN = "N1-B118-GPT-001-CONFIRM-003"
CANDIDATE = "a7b4edfb3d3c3bfcc061cfbdd0ee04de1e53204e"
GUARDS = "[分, 解, 割, 切, 破, 剖, 板, 別, 離, 刻, 盤, 研, 断, 絶, 折, 究, 査, 調, 察, 考, 討, 批]"
spec_path, final_path = HERE / f"{RUN}-spec.json", HERE / f"{RUN}-final.json"
spec = json.loads(frozen(spec_path, "b5e86f26391e8bba13b48ca2c4079f73a9b61f54ef43c2cbe031e5787bd740e6"))
final = json.loads(frozen(final_path, "28e4d9397293f5dde2db362ca0a3e6c000a51e05c302ee26999a707533cde903"))
config = load_batch(118)
clean(config, CANDIDATE)
require(spec["candidate"] == CANDIDATE and spec["family"] == "gpt"
        and spec["basis"] == "confirmation" and spec["openClaimIds"] == ["F1", "L2"],
        "Unexpected follow-up spec")
frozen(Path(spec["acceptance"]["path"]), spec["acceptance"]["sha256"])
prior = json.loads(frozen(Path(spec["prior"]["path"]), spec["prior"]["sha256"]))
require(prior["run"] == "N1-B118-GPT-001-CONFIRM-002" and prior["verdict"] == "NEEDS FIX"
        and prior["confirmationAccepted"] is False and prior["openClaimIds"] == ["F1", "L2"],
        "Earlier GPT evidence changed")
require(final["run"] == RUN and final["candidate"] == CANDIDATE
        and final["session"] == spec["session"] and final["confirmation"] == "CONFIRMED"
        and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
        "Unexpected confirmation result")
audit, context, structure = (
    json.loads(frozen(Path(final[key]["path"]), final[key]["sha256"]))
    for key in ("audit", "context", "structure"))
require(context["status"] == structure["status"] == "PASS" and not context["compactions"]
        and not audit["breaches"] and audit["reviewerIdle"] and not audit["recordIncomplete"]
        and audit["chainRead"] == audit["chainRequired"] == 46
        and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
        and audit["fetches"] == 0 and not audit["unexpectedUserMessages"]
        and audit["eventsSha256"] == context["eventsSha256"]
        and audit["actualResponseModels"] == ["gpt-6.1-sol"]
        and structure["dispositions"] == {"F1": "RESOLVED"} and structure["findings"] == 0
        and structure["optionalPoints"] == 0 and structure["limits"] == 9
        and not structure["nonAccepting"] and set(structure["facets"].values()) == {"CLEAN"},
        "Audit or structure changed")
report = frozen(Path(final["report"]["path"]), final["report"]["sha256"]).decode("utf-8").replace("\r\n", "\n")
require(f"Commit: {CANDIDATE}" in report and "## Findings\nNone." in report
        and "## Optional\nNone." in report and "- F1 - RESOLVED -" in report
        and "| 論 | argument; discourse | Accept bounded no-new-guard decision." in report,
        "Inspected report changed")
proof_path = WS / "scratch-118" / "revision-verification-002" / "revision-verification.json"
proof = json.loads(frozen(proof_path, "02288e9c86fa4b9009183171043c85013dfd7a5c0b0d823b63d1cd0ebfbd09f0"))
card = git(config, "show", f"{CANDIDATE}:kanji/析.md")
require(sha(card) == proof["targetCardSha256"], "Reviewed card differs from revision proof")
require(f"quiz_exclusions: {GUARDS}" in card.decode("utf-8"), "Exclusions differ")
sections = HERE.parent / "reconciliation-002" / "sections"
require("物事の本質をきわめる" in frozen(sections / "研.txt").decode("utf-8")
        and "筋道を立てて述べる" in frozen(sections / "論.txt").decode("utf-8"),
        "Inspected source sections changed")
adjudication = {
    "run": RUN, "family": "gpt", "session": spec["session"], "candidate": CANDIDATE,
    "status": "ACCEPTED_BOUNDED_CONFIRMATION", "verdict": "CONFIRMED",
    "reviewEvidenceAccepted": True, "confirmationAccepted": True, "publicationAccepted": False,
    "final": binding(final_path), "report": final["report"], "prior": spec["prior"],
    "audit": final["audit"], "context": final["context"], "structure": final["structure"],
    "actualResponseModels": audit["actualResponseModels"], "eventsSha256": audit["eventsSha256"],
    "acceptedDispositions": structure["dispositions"], "acceptedNewFindings": [], "openClaimIds": [],
    "resolvedPriorClaims": {
        "F1": "Resolved. 研 is now directly guarded on 析 while all eleven earlier guards remain in order. Coordinator read the 研 section: sense 2 物事の本質をきわめる supports close study as a broad description of analysis; Notes qualify the overlap without equating the words.",
        "L2": "Resolved. The reviewer individually assessed all twelve named comparisons against complete captured sections, citing positive senses for each of the eleven new guards. Coordinator previously read the same complete sections and now rechecked 論: its senses concern setting out reasoned statements, views and theories, a positive distinction supporting the bounded no-new-guard decision rather than gloss absence.",
    },
    "substantiveBasis": [
        "Complete report read. Each judgment cites the actual comparison card, complete Daijisen display section and stripped section, and the reviewed card line; it treats author dispositions as proposals, not proof.",
        "The reviewer assesses guards as precautionary displayed-answer protection, not claims of interchangeable words, and does not use third-card exclusions or option absence as semantic evidence.",
        "Scoped delta is only the exclusion list and two Notes bullets; metadata, readings, strokes, support word and curated distractors 新/本/休 remain unchanged. Gate logs are host evidence, not linguistic or publication acceptance.",
    ],
    "limitDispositions": {
        "L1": "Bounded same-reviewer confirmation, not a fresh initial review or corpus scan.",
        "L2": "Original title index and full articles for preserved guards and C distractors not reread; earlier limits preserved, no new exhaustive collision claim.",
        "L3": "Bounded source interpretation; terminal-LF display derivatives disclosed and hash-bound; no native certification.",
        "L4": "No new geometry, PDF-glyph or phonetic-history approval; those inputs are unchanged.",
        "L5": "Host models only; no arbitrary-pool, Kotlin/native/device or installed-APK acceptance. Two latent source-only reading collisions remain disclosed.",
        "L6": "Supporting-word and source-specific reading restrictions unchanged and preserved.",
        "L7": "Gate logs not rerun by the reviewer; coordinator verified them against the revision proof. Not linguistic or publication acceptance.",
        "L8": "Commit, signature and hash provenance supplied; coordinator independently verified committed 析 bytes match the revision proof.",
        "L9": "Textual confirmation only; publication, served ZIP and whole-N1 completion remain pending.",
    },
    "acceptanceLimit": "GPT acceptance applies to a7b4edfb only. With Claude CONFIRM-003, both original families accept this revision; publication still requires closure, owner signature, CI and exact-ZIP verification.",
    "sourceBindings": [binding(sections / "研.txt"), binding(sections / "論.txt")],
    "revisionProof": binding(proof_path), "spec": binding(spec_path), "tool": binding(Path(__file__)),
}
adj = freeze_json(HERE / f"{RUN}-adjudication.json", adjudication)
print(json.dumps(freeze_json(HERE / f"{RUN}-acceptance.json", {
    "run": RUN, "family": "gpt", "batch": 118, "session": spec["session"],
    "candidate": CANDIDATE, "verdict": "CONFIRMED",
    "reviewEvidenceAccepted": True, "confirmationAccepted": True,
    "openClaimIds": [], "acceptedNewFindings": [], "dispositions": structure["dispositions"],
    "report": final["report"], "final": binding(final_path), "adjudication": adj,
    "acceptanceLimit": adjudication["acceptanceLimit"],
})))
