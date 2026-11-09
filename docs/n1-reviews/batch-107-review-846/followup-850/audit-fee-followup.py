#!/usr/bin/env python3
"""Verify the additional, narrowly reviewed batch 107 fee safeguard."""
import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
ROOT = HERE.parents[3]
PREVIOUS = "bfd617ab00c75b9f7a74decd865f1f813b0eabed"
ORIGINAL = "6614e06e602f1cec6b894052812178b57c8890cb"
PACKET = "315fb0821206f8318f37b0cc129bc17967d60b02644c65546f74551842db793b"
EXPECTED = {
    "article": "words/勘定.md",
    "otherArticles": ["words/料金.md"],
    "before": ["計算", "支払う", "給与", "払う", "代金"],
    "after": ["計算", "支払う", "給与", "払う", "代金", "料金"],
    "beforeText": "quiz_exclusions: [計算, 支払う, 給与, 払う, 代金]",
    "afterText": "quiz_exclusions: [計算, 支払う, 給与, 払う, 代金, 料金]",
}
spec = importlib.util.spec_from_file_location("followup107", REVIEW / "audit-followup-exceptions.py")
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
require = prior.require


def verify_exception(before, after, row):
    require(all(row.get(key) == value for key, value in EXPECTED.items()),
            "Fee exception differs from the exact authorized delta")
    prior.base.reused_changes(before, after,
                              [{"before": EXPECTED["beforeText"], "after": EXPECTED["afterText"]}],
                              exclusions=EXPECTED["after"])


def verify_reviewers(receipt, raw_reports):
    require(receipt["reviewedCheckpoint"] == PREVIOUS and receipt["commonPacketSha256"] == PACKET,
            "Original reviewer checkpoint or packet differs")
    for label, digest in {
        "claude": "b8247ee375985a8f282c6075c563ced227ae10ced0e69f0a0b1a39bdabff1887",
        "gpt": "fdd46b7ad7e4218fb4b16b61d7945cd4ec75c39aa717ab782f0a1f9ab36ce5ee",
    }.items():
        report = receipt["reviewers"][label]
        require(hashlib.sha256(raw_reports[label]).hexdigest() == digest == report["reportSha256"],
                f"Original {label} follow-up report changed")
        require(report["mechanicalReadVerificationPassed"] is True and report["overlapCount"] == 0
                and report["multipleToolResponseCount"] == 0
                and report["reads"]["correctionPacket"]["returnedSha256"] == PACKET,
                f"Original {label} follow-up did not meet the serial-read contract")
    require(receipt["reviewers"]["claude"]["reportEventTimestamp"]
            < receipt["reviewers"]["gpt"]["reads"]["gitPointer"]["startedAt"],
            "Original reviewer sessions overlapped")


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(ROOT), *args])


def show(revision, name):
    return git("show", f"{revision}:{name}")


def audit():
    ledger = json.loads((HERE / "reconciliation.json").read_text(encoding="utf-8"))
    require(ledger["previousSignedCorrectionSnapshot"] == PREVIOUS, "Previous review snapshot differs")
    require(git("log", "-1", "--format=%G?", PREVIOUS).strip() == b"G",
            "Previous correction signature is not verified")
    subprocess.check_call(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PREVIOUS, "HEAD"])
    previous = json.loads(show(PREVIOUS, "manifest.json"))
    original = json.loads(show(ORIGINAL, "manifest.json"))
    current = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    require(previous["contentVersion"] == ledger["previousContentVersion"]
            and current["contentVersion"] == ledger["contentVersion"],
            "Expected content version differs")
    require(current == prior.base.build_manifest(ROOT), "Current manifest is stale")
    prior.base.runtime_delta(previous, current, set(), {"words/勘定.md"})
    prior.base.runtime_delta(original, current, set(), {"words/勘.md", "words/勘定.md"})
    row = ledger["additionalException"]
    before = show(PREVIOUS, EXPECTED["article"]).decode("utf-8")
    after = prior.base.path_at(ROOT, EXPECTED["article"]).read_text(encoding="utf-8")
    verify_exception(before, after, row)
    declared = prior.base.metadata(after)
    target = prior.base.metadata(prior.base.path_at(ROOT, "words/料金.md").read_text(encoding="utf-8"))
    require(declared["word"] == "勘定" and target["word"] == "料金"
            and target["word"] in declared["quiz_exclusions"], "Direct fee target differs")
    changed = git("diff", "--no-renames", "--name-status", "-z", PREVIOUS).decode("utf-8").split("\0")
    untracked = git("ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0")
    prior.verify_historical_changes(list(zip(changed[::2], changed[1::2])), untracked)
    receipt = json.loads((REVIEW / "followup-849" / "confirmation-provenance.json").read_text(encoding="utf-8"))
    reports = {name: (REVIEW / "followup-849" / f"confirmation-{name}.md").read_bytes()
               for name in ("claude", "gpt")}
    verify_reviewers(receipt, reports)
    extra_source = (REVIEW / "followup-payment-jmdict.xml").read_bytes()
    extra_receipt = json.loads((REVIEW / "followup-payment-jmdict-provenance.json").read_text(encoding="utf-8"))
    prior.verify_additional_source(extra_source, extra_receipt)
    return {
        "batch": "107", "previousSignedSnapshot": PREVIOUS, "originalTeachingSnapshot": ORIGINAL,
        "contentVersion": current["contentVersion"],
        "previousSignatureAndAncestryVerified": True, "manifestFresh": True,
        "onlyAdditionalRuntimePayload": "words/勘定.md", "additionalDirectPair": "勘定/料金",
        "allOtherRuntimePayloadsUnchanged": True, "priorEvidenceUnchanged": True,
        "originalFollowupReportsByteVerified": True, "originalFollowupReadsMechanicallyVerified": True,
        "priorSourceEvidenceSha256": prior.SOURCE_HASH,
        "limits": "Preservation and original review provenance only; confirmation of this final change, native behavior, merged-tree acceptance and publication remain separate.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=True))
