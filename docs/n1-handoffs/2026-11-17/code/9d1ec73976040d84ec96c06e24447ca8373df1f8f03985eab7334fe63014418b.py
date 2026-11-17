"""Admit the original author for the single 滝-液 precaution after GPT-CONFIRM-001 stayed UNVERIFIED on C6."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from admit_b133_source_reconciliation import AUTHOR, CANDIDATE, assess_snapshot, collect_initials
from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b133_payload import HERE, REPO, RUNNER
from verify_b133_sources import FINGERPRINT, Git, OWNER

REVISION = "110b4ffb6af078eb2adb00645db4c9e0bd6db188"
OUT = HERE / "teaching-reconciliation-admission-002"
TARGET = WS / "scratch-133" / "teaching-reconciliation-002"
BRIEF = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b"
             r"\files\b133-teaching-revision-002-brief.txt")
DECISION = (HERE / "gpt-confirm-001-adjudication-001.json",
            "987fb5f9fc5c793992b2d1d70d0ccf56086f8257656aa6837cfbcc0bc5b60adc")
BINDINGS = {
    "gptConfirmationReport": (WS / "reports-133" / "N1-B133-GPT-CONFIRM-001.md",
                              "23d4cd954ea8a588809ed9ed4359bbb9b1f052d4bebc3c71c67d612c54d72ef0"),
    "claudeConfirmationAcceptance": (HERE / "confirmation-002" / "N1-B133-CLAUDE-CONFIRM-001-acceptance.json", None),
    "coordinatorAdjudication": (HERE / "coordinator-adjudication-001.json",
                                "cc04c27c12c3fd9fcced0075acfb817f8f0427049c1cfdcc18db146ac1d4f549"),
    "revisionVerification": (HERE / "teaching-revision-verification-002" / "verification.json",
                             "0a95d56399cc78df0e7fd3fd9b2e0359267f5c4d564a1da39ab3079e00982d9c"),
}


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
    require(decision["candidate"] == REVISION and decision["confirmation"] == "UNVERIFIED"
            and decision["acceptedResidual"] == {"id": "C6", "pair": "滝-液",
                                                 "decision": "ADD_QUALIFIED_DIRECT_PRECAUTION",
                                                 "previousDecision": "RETAINED_DISTINCTION"},
            "Confirmation decision differs")
    require("append 液 to the existing quiz_exclusions".encode("utf-8") in brief
            and REVISION.encode() in brief and DECISION[1].encode() in brief, "Brief differs from decision")
    bindings = {}
    for name, (path, digest) in BINDINGS.items():
        raw = frozen(path, digest)
        bindings[name] = {"path": str(path), "sha256": sha(raw)}
    accepted = json.loads(frozen(BINDINGS["claudeConfirmationAcceptance"][0]))
    require(accepted["candidate"] == REVISION and accepted["confirmation"] == "CONFIRMED"
            and accepted["reviewAccepted"] is True, "Claude confirmation differs")
    guard, _ = start_guard("B133 bounded teaching revision 002 admission")
    try:
        initials = collect_initials()
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == REVISION
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Revision is changed or dirty")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", REVISION).decode().strip()
                == f"{CANDIDATE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Revision identity differs")
        require(b"quiz_exclusions: [\xe5\xb7\x9d" in git("show", REVISION + ":kanji/滝.md")
                and "液".encode("utf-8") not in git("show", REVISION + ":kanji/滝.md").split(b"\n")[13],
                "滝 exclusions already differ")
        guard.check()
        assess_snapshot(status, roster, observed, datetime.now(timezone.utc))
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    snapshots = {"status": write_frozen(OUT / "status.json", status_raw),
                 "roster": write_frozen(OUT / "roster.txt", roster_raw)}
    record = {
        "batch": 133, "parent": REVISION, "candidate": CANDIDATE, "session": AUTHOR,
        "purpose": "append-single-滝-液-precaution-and-owner-sign-no-push", "admitted": True,
        "observedAt": observed.isoformat(), "createdAt": datetime.now(timezone.utc).isoformat(),
        "sessionCount": count, "snapshots": snapshots, "initials": initials,
        "brief": {"path": str(BRIEF), "sha256": sha(brief)},
        "decision": {"path": str(DECISION[0]), "sha256": sha(decision_raw)}, "bindings": bindings,
        "memory": memory,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "limits": "Startup observation only, not a reservation. One existing author; one-pair signed teaching "
                  "revision. No push, reviewers, confirmation, publication or delivery credit.",
    }
    print(json.dumps(freeze_json(OUT / "admission.json", record)))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: admit_b133_teaching_reconciliation_v2.py STATUS ROSTER")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
