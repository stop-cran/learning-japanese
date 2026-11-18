"""Admit the original author for reconciliation-003 after fresh Claude CONFIRM-002 stayed UNVERIFIED on the 滝水 gloss."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from admit_b133_source_reconciliation import AUTHOR, assess_snapshot, collect_initials
from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b133_payload import HERE, REPO, RUNNER
from verify_b133_sources import FINGERPRINT, Git, OWNER

REVISION = "d7d6cff92afe8220c16a5daa76f1c3f00a2bef30"
PARENT = "110b4ffb6af078eb2adb00645db4c9e0bd6db188"
OUT = HERE / "teaching-reconciliation-admission-003"
TARGET = WS / "scratch-133" / "teaching-reconciliation-003"
BRIEF = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b"
             r"\files\b133-teaching-revision-003-brief.txt")
DECISION = (HERE / "claude-confirm-002-adjudication-001.json",
            "8bba057dd162f4e32c8fa6e0c9243692643dc312fd2e4d2d8548ae1fe2ccf326")
SOURCES = HERE / "claude-confirm-002-adjudication-sources-001"
BINDINGS = {
    "claudeConfirmationReport": (WS / "reports-133" / "N1-B133-CLAUDE-CONFIRM-002.md",
                                 "9327ee1d95393fa26bacbadf26099f73a0be0091e1ce30c4fc5388aafaf76bb5"),
    "claudeConfirmationFinal": (HERE / "confirmation-002" / "N1-B133-CLAUDE-CONFIRM-002-final.json",
                                "8018b596365bfc6ebf8c35e06ef9327c38bd9a27cd4a651787d56a717c033e20"),
    "gptConfirmationAcceptance": (HERE / "confirmation-002" / "N1-B133-GPT-CONFIRM-002-acceptance.json",
                                  "bc3aa4beb22a883ba4298a502f52881e71e7828274e16c4bc87ec0ff1b45e734"),
    "gptConfirm001Adjudication": (HERE / "gpt-confirm-001-adjudication-001.json",
                                  "987fb5f9fc5c793992b2d1d70d0ccf56086f8257656aa6837cfbcc0bc5b60adc"),
    "coordinatorAdjudication": (HERE / "coordinator-adjudication-001.json",
                                "cc04c27c12c3fd9fcced0075acfb817f8f0427049c1cfdcc18db146ac1d4f549"),
    "revisionVerification": (HERE / "teaching-revision-verification-003" / "verification.json",
                             "3de9bf9e699364b37806c64a8fdf698b049b1aa572dd477a2376032ca5b95f94"),
    "takisuiCapture": (SOURCES / "takisui-kotobank.html",
                       "5100a307551e7d6bf0f92665c5783cdd010fe85c6a49b9cbdc618af3d440099f"),
    "takisuiSections": (SOURCES / "takisui-sections.txt",
                        "38244158be21a6a1aac5cfa5b5b94ad8493b0a9e45e606ec3bb269bba332d0c8"),
}
RESIDUALS = [
    {"id": "O1-gloss", "pair": None, "decision": "CORRECT_UNSUPPORTED_GLOSS",
     "scope": "kanji/滝.md Meaning sentence and 液 Note rationale only"},
    {"id": "O1-sake", "pair": "滝-酒", "decision": "ADD_QUALIFIED_DIRECT_PRECAUTION"},
]


def main(status_path, roster_path):
    require(not OUT.exists() and not TARGET.exists(), "Preserve existing admission or teaching outputs")
    status_raw, roster_raw = status_path.read_bytes(), roster_path.read_bytes()
    status = json.loads(status_raw)
    roster = json.loads(roster_raw[roster_raw.index(b"["):])
    observed = datetime.fromtimestamp(min(status_path.stat().st_mtime, roster_path.stat().st_mtime),
                                      timezone.utc)
    count = assess_snapshot(status, roster, observed, datetime.now(timezone.utc))
    brief = frozen(BRIEF)
    decision_raw = frozen(*DECISION)
    decision = json.loads(decision_raw)
    residuals = [{k: v for k, v in item.items() if k != "basis"} for item in decision["acceptedResiduals"]]
    require(decision["candidate"] == REVISION and decision["confirmation"] == "UNVERIFIED"
            and decision["status"] == "EVIDENCE_ONLY_NOT_ACCEPTED_AS_CONFIRMATION"
            and residuals == RESIDUALS, "Confirmation decision differs")
    require("append 酒 after 液".encode("utf-8") in brief
            and REVISION.encode() in brief and DECISION[1].encode() in brief, "Brief differs from decision")
    bindings = {}
    for name, (path, digest) in BINDINGS.items():
        raw = frozen(path, digest)
        bindings[name] = {"path": str(path), "sha256": sha(raw)}
    accepted = json.loads(frozen(BINDINGS["gptConfirmationAcceptance"][0]))
    require(accepted["candidate"] == REVISION and accepted["confirmation"] == "CONFIRMED"
            and accepted["reviewAccepted"] is True, "GPT confirmation differs")
    guard, _ = start_guard("B133 bounded teaching revision 003 admission")
    try:
        initials = collect_initials()
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == REVISION
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Revision is changed or dirty")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", REVISION).decode().strip()
                == f"{PARENT}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Revision identity differs")
        card = git("show", REVISION + ":kanji/滝.md")
        exclusions = card.split(b"\n")[13].rstrip(b"\r")
        require(exclusions.startswith(b"quiz_exclusions: [\xe5\xb7\x9d")
                and exclusions.endswith("険, 液]".encode("utf-8"))
                and "酒".encode("utf-8") not in exclusions
                and "滝水, water from a waterfall".encode("utf-8") in card
                and card.count("滝水".encode("utf-8")) == 2,
                "滝 card differs from the adjudicated state")
        guard.check()
        assess_snapshot(status, roster, observed, datetime.now(timezone.utc))
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    snapshots = {"status": write_frozen(OUT / "status.json", status_raw),
                 "roster": write_frozen(OUT / "roster.txt", roster_raw)}
    record = {
        "batch": 133, "parent": REVISION, "grandparent": PARENT, "session": AUTHOR,
        "purpose": "correct-滝水-gloss-append-滝-酒-precaution-and-owner-sign-no-push", "admitted": True,
        "observedAt": observed.isoformat(), "createdAt": datetime.now(timezone.utc).isoformat(),
        "sessionCount": count, "snapshots": snapshots, "initials": initials,
        "brief": {"path": str(BRIEF), "sha256": sha(brief)},
        "decision": {"path": str(DECISION[0]), "sha256": sha(decision_raw)}, "bindings": bindings,
        "memory": memory,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "limits": "Startup observation only, not a reservation. One existing author; one-card signed teaching "
                  "revision. No push, reviewers, confirmation, publication or delivery credit.",
    }
    print(json.dumps(freeze_json(OUT / "admission.json", record)))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: admit_b133_teaching_reconciliation_v3.py STATUS ROSTER")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
