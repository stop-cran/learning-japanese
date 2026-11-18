"""Substantively accept the Claude-002 confirmation of the B118 reconciliation correction."""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import freeze_json, frozen, git, load_batch, require
from confirm_v2 import binding, clean

HERE = Path(__file__).resolve().parent
RUN = "N1-B118-CLAUDE-002-CONFIRM-002"
CANDIDATE = "fa2f64f2472cf9ef10b8ac5f48db14dcaa248cd2"
PARENT = "dc2ee12623b36eb059d147ece2f2cfa3f87dfad7"
spec_path, final_path = HERE / f"{RUN}-spec.json", HERE / f"{RUN}-final.json"
spec, final = json.loads(frozen(spec_path)), json.loads(frozen(final_path))
config = load_batch(118)
clean(config, CANDIDATE)
require(spec["candidate"] == CANDIDATE and spec["family"] == "claude", "Unexpected spec")
frozen(Path(spec["acceptance"]["path"]), spec["acceptance"]["sha256"])
require(final["run"] == RUN and final["candidate"] == CANDIDATE
        and final["session"] == spec["session"]
        and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
        and final["confirmation"] == "CONFIRMED", "Unexpected confirmation final")
audit, context, structure = (
    json.loads(frozen(Path(final[key]["path"]), final[key]["sha256"]))
    for key in ("audit", "context", "structure"))
require(context["status"] == structure["status"] == "PASS" and not context["compactions"]
        and not audit["breaches"] and audit["reviewerIdle"] and audit["fetches"] == 0
        and audit["chainRead"] == audit["chainRequired"] == 35
        and audit["eventsSha256"] == context["eventsSha256"]
        and structure["dispositions"] == {"F1": "RESOLVED", "O1": "RESOLVED", "O2": "RESOLVED"}
        and structure["findings"] == 0 and structure["optionalPoints"] == 0
        and structure["limits"] == 6 and not structure["nonAccepting"]
        and set(structure["facets"].values()) == {"CLEAN"}, "Confirmation gate mismatch")
report = frozen(Path(final["report"]["path"]), final["report"]["sha256"]).decode("utf-8").replace("\r\n", "\n")
require("## Findings\nNone." in report and "## Optional\nNone." in report
        and f"Commit: {CANDIDATE}" in report, "Report changed after substantive inspection")
changed = git(config, "diff", "--name-only", PARENT, CANDIDATE).decode("utf-8").split()
require("kanji/析.md" in changed and all(
    p == "kanji/析.md" or p == "manifest.json" or p.startswith("docs/") for p in changed),
    f"Unexpected runtime delta: {changed}")
card = git(config, "show", f"{CANDIDATE}:kanji/析.md").decode("utf-8")
require("quiz_exclusions: [分, 解, 割, 切, 破, 剖, 板, 別, 離, 刻, 盤]" in card, "Exclusions differ")
staged = hashlib.sha256(card.encode("utf-8")).hexdigest()
worktree = Path(config["repo"]) / "kanji" / "析.md"
normalized = hashlib.sha256(worktree.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
require(staged.startswith("9d33c5df") and normalized == staged, "L2 line-ending equivalence failed")
adjudication = {
    "run": RUN, "family": "claude", "session": final["session"], "candidate": CANDIDATE,
    "status": "ACCEPTED_BOUNDED_CONFIRMATION", "verdict": "CONFIRMED",
    "reviewEvidenceAccepted": True, "confirmationAccepted": True, "publicationAccepted": False,
    "final": binding(final_path), "report": final["report"],
    "audit": final["audit"], "context": final["context"], "structure": final["structure"],
    "actualResponseModels": audit["actualResponseModels"], "eventsSha256": audit["eventsSha256"],
    "acceptedDispositions": structure["dispositions"], "acceptedNewFindings": [], "openClaimIds": [],
    "prior": spec["acceptance"], "changedPaths": changed,
    "substantiveBasis": [
        "F1: 析 now directly excludes 別 and 離, preserving the original seven exclusions in order. Coordinator re-read KANJIDIC2 析 chop/divide/tear/analyze, 別 separate/branch off and 離 detach/separation; the overlap and the new Notes line are accurate and claim no interchangeability.",
        "O1: 盤 (board among tray/platter senses) is added and Notes qualify 板/盤 as precautionary guards for the separately sourced historical へぎ thin-board entry only.",
        "O2: The 切 rationale is narrowed to the explicit KANJIDIC2 chop gloss; 刻 (cut fine/chop/mince) is a conservative source-backed addition. Declining 断 and the other screened characters is consistent because no opened 析 source glosses their displayed senses.",
        "The runtime delta is confined to 析.md; distractors 新/本/休, readings, metadata and the linked word are unchanged and curated choices still fill all slots.",
    ],
    "optionalDispositions": {},
    "limitDispositions": {
        "L1": "Unread README/manifest/raw sources are bound by hash in the signed tree and the changed-file inventory; not relabelled as reviewed.",
        "L2": "Resolved by coordinator: core.autocrlf=true. The committed blob SHA-256 starts 9d33c5df and equals the CRLF-normalized worktree file; the reviewer read the committed content.",
        "L3": "Bounded host quiz models only; arbitrary pools, Kotlin/native/device execution and the older APK remain outside the claim.",
        "L4": "Editorial semantic judgment over supplied sources; no native-speaker certification.",
        "L5": "Whole-record citation ranges were confirmed by coordinator for 析/刻/盤/別/離 glosses.",
        "L6": "Unused content-format context is a scope note, not a defect.",
    },
    "acceptanceLimit": "Bounded textual confirmation only. GPT-001-CONFIRM-002 must also accept fa2f64f2 before source-bound closure, signed publication, CI and exact ZIP.",
    "spec": binding(spec_path), "tool": binding(Path(__file__)),
}
adj = freeze_json(HERE / f"{RUN}-adjudication.json", adjudication)
print(json.dumps(freeze_json(HERE / f"{RUN}-acceptance.json", {
    "run": RUN, "family": "claude", "batch": 118, "session": final["session"],
    "candidate": CANDIDATE, "verdict": "CONFIRMED",
    "reviewEvidenceAccepted": True, "confirmationAccepted": True,
    "openClaimIds": [], "acceptedNewFindings": [], "dispositions": structure["dispositions"],
    "report": final["report"], "final": binding(final_path), "adjudication": adj,
    "acceptanceLimit": adjudication["acceptanceLimit"],
})))
