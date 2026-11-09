#!/usr/bin/env python3
"""Verify the additional, narrowly sourced batch 107 payment safeguards."""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
PREVIOUS = "03f68e8e796f497576e87337c557dcf6681a1a2f"
ORIGINAL = "6614e06e602f1cec6b894052812178b57c8890cb"
SOURCE_HASH = "c3ab836314070acc15ce0a155ab1af12b9cea8e751af12b6f764a63cb10c8803"
EXPECTED = {
    "article": "words/勘定.md",
    "otherArticles": ["words/払う.md", "words/代金.md"],
    "before": ["計算", "支払う", "給与"],
    "after": ["計算", "支払う", "給与", "払う", "代金"],
    "beforeText": "quiz_exclusions: [計算, 支払う, 給与]",
    "afterText": "quiz_exclusions: [計算, 支払う, 給与, 払う, 代金]",
}
spec = importlib.util.spec_from_file_location("reviewed107", REVIEW / "audit-reviewed-exceptions.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
require = base.require


def verify_exception(before, after, row):
    require(all(row.get(key) == value for key, value in EXPECTED.items()),
            "Additional exception differs from the exact authorized delta")
    base.reused_changes(before, after, [{"before": EXPECTED["beforeText"], "after": EXPECTED["afterText"]}],
                        exclusions=EXPECTED["after"])


def verify_historical_changes(changed, untracked):
    for status, name in changed:
        if name.startswith("docs/n1-sources/"):
            raise ValueError(f"Historical source evidence changed: {name}")
        if name.startswith("docs/n1-reviews/batch-107-review-846/") and status != "A":
            raise ValueError(f"Historical review evidence changed: {name}")
    require(not any(name.startswith("docs/n1-sources/") for name in untracked),
            "Unexpected untracked source evidence")


def verify_additional_source(raw, receipt):
    require(hashlib.sha256(raw).hexdigest() == SOURCE_HASH == receipt["outputSha256"],
            "Additional source evidence differs")
    require(receipt["entryIds"] == ["1501620", "1411790", "1554280"]
            and receipt["outputBytes"] == len(raw)
            and receipt["compressedSourceSha256"] == "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d",
            "Additional source provenance differs")
    entries = ET.fromstring(raw).findall("entry")
    require([entry.findtext("ent_seq") for entry in entries] == receipt["entryIds"],
            "Additional source entry identities differ")


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(ROOT), *args])


def show(revision, name):
    return git("show", f"{revision}:{name}")


def audit():
    ledger = json.loads((REVIEW / "reconciliation-followup.json").read_text(encoding="utf-8"))
    require(ledger["previousSignedCorrectionSnapshot"] == PREVIOUS
            and ledger["reviewedTeachingSnapshot"] == ORIGINAL,
            "Review snapshots differ")
    require(git("log", "-1", "--format=%G?", PREVIOUS).strip() == b"G",
            "Previous correction signature is not verified")
    subprocess.check_call(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PREVIOUS, "HEAD"])
    previous = json.loads(show(PREVIOUS, "manifest.json"))
    original = json.loads(show(ORIGINAL, "manifest.json"))
    current = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    require(previous["contentVersion"] == ledger["previousContentVersion"]
            and current["contentVersion"] == ledger["contentVersion"],
            "Expected content version differs")
    require(current == base.build_manifest(ROOT), "Current manifest is stale")
    base.runtime_delta(previous, current, set(), {"words/勘定.md"})
    base.runtime_delta(original, current, set(), {"words/勘.md", "words/勘定.md"})
    row = ledger["additionalException"]
    before = show(PREVIOUS, EXPECTED["article"]).decode("utf-8")
    after = base.path_at(ROOT, EXPECTED["article"]).read_text(encoding="utf-8")
    verify_exception(before, after, row)
    declared = base.metadata(after)
    require(declared["word"] == "勘定", "Reused word identity differs")
    for name in row["otherArticles"]:
        target = base.metadata(base.path_at(ROOT, name).read_text(encoding="utf-8"))
        require(target["word"] in declared["quiz_exclusions"], f"Missing direct target: {name}")
    changed = git("diff", "--no-renames", "--name-status", "-z", PREVIOUS).decode("utf-8").split("\0")
    untracked = git("ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0")
    verify_historical_changes(list(zip(changed[::2], changed[1::2])), untracked)
    raw = (REVIEW / "followup-payment-jmdict.xml").read_bytes()
    receipt = json.loads((REVIEW / "followup-payment-jmdict-provenance.json").read_text(encoding="utf-8"))
    verify_additional_source(raw, receipt)
    old_ledger = json.loads(show(PREVIOUS, "docs/n1-reviews/batch-107-review-846/reconciliation.json"))
    for key in ("claude", "gpt"):
        report = old_ledger["initialReviews"][key]
        require(base.digest((REVIEW / report["report"]).read_bytes()) == report["reportSha256"],
                f"Original {key} report changed")
    return {
        "batch": "107", "previousSignedSnapshot": PREVIOUS, "originalTeachingSnapshot": ORIGINAL,
        "contentVersion": current["contentVersion"],
        "previousSignatureAndAncestryVerified": True, "manifestFresh": True,
        "onlyAdditionalRuntimePayload": "words/勘定.md",
        "additionalDirectPairs": ["勘定/払う", "勘定/代金"],
        "allOtherRuntimePayloadsUnchanged": True, "historicalSourceAndReviewEvidenceUnchanged": True,
        "initialReportsByteVerified": True, "additionalSourceSha256": SOURCE_HASH,
        "limits": "Preservation and source identity only; this does not establish independent review, linguistic agreement, native behavior, merged-tree acceptance, or publication.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=True))
