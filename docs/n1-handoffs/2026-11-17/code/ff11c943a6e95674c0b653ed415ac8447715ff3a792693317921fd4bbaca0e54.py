"""Seal the coordinator's substantive decisions against the verified final."""
import json
import re
import subprocess
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

ROOT = WS / "scratch-134" / "review"
LIFE = ROOT / "fresh-independent-002" / "lifecycle-011"
REPO = WS / "b134-worktree"
RUN = "N1-B134-CLAUDE-FRESH-003"
CANDIDATE = "355cccb840d22e7313e79f234eb93d1367e00352"
OUT = ROOT / "claude-fresh003-adjudication-001"


def ref(path, expected=None):
    raw = frozen(path, expected)
    return {"path": str(path), "sha256": sha(raw)}


def main():
    require(not OUT.exists(), "Preserve existing adjudication")
    draft = json.loads(Path(__file__).with_name(
        "b134-claude-fresh003-substantive-draft.json").read_bytes())
    final_ref = ref(LIFE / (RUN + "-final.json"),
                    "71c9bbf67a3301f79c0c4c715c72059672d07143378976e559381f09eba58ed0")
    final = json.loads(frozen(final_ref["path"], final_ref["sha256"]))
    report = frozen(final["report"]["path"], draft["reportSha256"])
    audit = json.loads(frozen(final["audit"]["path"], final["audit"]["sha256"]))
    require(final["candidate"] == draft["candidate"] == CANDIDATE
            and final["run"] == draft["run"] == RUN
            and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and final["problems"] == [] and final["structure"]["status"] == "PASS"
            and final["structure"]["overall"] == draft["verdict"]
            and final["report"]["sha256"] == draft["reportSha256"],
            "Final/report identity or status differs")
    require(audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK"
            and audit["breaches"] == [] and audit["reviewerIdle"] is True
            and audit["coreRead"] == audit["coreRequired"] == 64
            and audit["extensionRead"] == audit["extensionRequired"] == 4
            and audit["writes"] == audit["readbacks"] == 1
            and audit["readbackVerified"] is True and audit["fetches"] == 0
            and audit["unexpectedUserMessages"] == 0
            and audit["capacityTelemetry"]["status"] == "PASS"
            and audit["capacityTelemetry"]["compactions"] == [],
            "Actual execution evidence does not pass")
    ids = re.findall(r"(?m)^### ([FO]\d+):", report.decode("utf-8"))
    require(ids == [item["id"] for item in draft["decisions"]]
            and ids == draft["openClaimIds"], "Numbered claim accounting differs")
    bindings = []
    for relative in (
        "kanji/紫.md", ".github/copilot-instructions.md",
        ".github/instructions/content-structure.instructions.md", "docs/content-format.md",
        "docs/n1-sources/batch-134-reconciliation-001/dispositions.md",
    ):
        raw = subprocess.check_output(
            ["git", "--no-pager", "show", CANDIDATE + ":" + relative], cwd=REPO)
        require((REPO / relative).read_bytes() == raw, "Current source changed: " + relative)
        bindings.append({"repositoryPath": relative, "snapshot": CANDIDATE, "sha256": sha(raw)})
    quiz_raw = (WS / "lean" / "quiz_safety.py").read_bytes()
    quiz_ref = write_frozen(OUT / "quiz_safety.py", quiz_raw)
    repair = ROOT / "report-checker-repair-001"
    repair_evidence = []
    for name, archive, digest in (
        ("checker-entry.py", "protocol/report-checker-repair/checker-entry.py",
         "3f512c1b0fd5f96dc4bffa0e816b4be89faa8f77355ec43f1f5e7c24531cecf8"),
        ("controller-entry.py", "protocol/report-checker-repair/controller-entry.py",
         "8ed3318f4f11258f8d8e384bb10df961e5575586a77c6bc04b019894982fb25c"),
        ("validation.json", "verification/report-checker-repair-validation.json",
         "49d93c2d9f9e597a3e4f1cd2f6ddac1650493db7544efe387ce2e92cbbad2b4d"),
        ("inventory.json", "verification/report-checker-repair-inventory.json",
         "53a0ddc41da466ad426ef37da1e08674e6b34f4947ff28a9e234bb7c7c02f5c0"),
    ):
        repair_evidence.append({"archivePath": archive, **ref(repair / name, digest)})
    hold_ref = ref(LIFE / (RUN + "-final-hold-76012e64cadc4f0d989fde7a5f83cee6.json"),
                   "9b50c4a5bc689c0059f210b8c42ff288edbfd623e9a4ee42eecd7735bd428800")
    repair_evidence.extend((
        {"archivePath": "history/claude-fresh003-original-structure-hold.json", **hold_ref},
        {"archivePath": "protocol/report-checker-repair/original-checker.py",
         **ref(LIFE / "protocol-014" / "check-report-structure-b134-014.py",
               "f68265d947785a19aaa79480303bb1481b13ea5670ee2a25181ea50dba4aac2d")},
        {"archivePath": "verification/claude-fresh003-quiz-warning-producer.py", **quiz_ref},
    ))
    data = {key: value for key, value in draft.items() if key != "status"}
    data.update(claimsAdjudicated=True, finalSha256=final_ref["sha256"],
                signedSourceBindings=bindings, quizWarningProducer=quiz_ref,
                parserRepair=final["structure"]["parserRepair"], preservedFailedFinal=hold_ref)
    data["claimChecks"].insert(0, {
        "claim": "Actual identity, complete source reads, report binding and zero-compaction capacity.",
        "evidence": "Final " + final_ref["sha256"] + "; actual audit " + final["audit"]["sha256"]
                    + "; response models " + ", ".join(audit["actualResponseModels"])
                    + "; peak input " + str(audit["capacityTelemetry"]["actualPeakInputTokens"])
                    + "; 64/64 core and 4/4 extension reads, one write/readback, no fetches or unexpected messages.",
        "disposition": "Accepted mechanically with the independently verified delimiter-only checker repair. Report bytes and verdict are unchanged; the original failed structure result is preserved. No linguistic conclusion follows solely from these checks.",
    })
    data["limits"] = [
        "Review evidence acceptance is separate from semantic reconciliation and publication.",
        "The original NEEDS FIX verdict and its numbered claims remain unchanged; coordinator decisions differ on mandatory F1 status.",
        "All four numbered report claims remain explicit resolution-accounting obligations.",
        "The original import failure, checker failure and their external repair producers are preserved separately.",
        "No Kotlin/native/device/rendering, custom/multiple-borrow or whole-set acceptance.",
        "No teaching edit, commit, push or publication occurred; GPT must review the same signed snapshot independently.",
    ]
    adjudication = freeze_json(OUT / "adjudication.json", data)
    evidence = freeze_json(OUT / "additional-evidence.json", repair_evidence)
    print(json.dumps({"adjudication": adjudication, "additionalEvidence": evidence,
                      "claimChecks": len(data["claimChecks"]), "decisions": len(data["decisions"])}))


if __name__ == "__main__":
    main()
