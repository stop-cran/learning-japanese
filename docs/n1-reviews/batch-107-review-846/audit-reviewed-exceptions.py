#!/usr/bin/env python3
"""Verify the exact post-review delta against the signed batch 107 snapshot."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
REVIEW = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools"))
from audit_n1_batch import reused_changes, runtime_delta
from build_manifest import build_manifest
from freeze_n1_sources import require

SNAPSHOT = "6614e06e602f1cec6b894052812178b57c8890cb"
SOURCE = "dfed2c150d7fe921aacdb1d616ff527df1935f3b"
EVIDENCE_TIP = "9d2827257c38e556404d5b585a1911bb5c596e37"
SIGNED_ADDITION = "docs/n1-sources/execution-845.json"
EXCEPTIONS = {
    "words/勘.md": {
        "otherArticles": ["words/感覚.md"],
        "before": [],
        "after": ["感覚"],
        "beforeText": "tags: [kango, noun, thinking]\n---",
        "afterText": "tags: [kango, noun, thinking]\nquiz_exclusions: [感覚]\n---",
    },
    "words/勘定.md": {
        "otherArticles": ["words/支払う.md", "words/給与.md"],
        "before": ["計算"],
        "after": ["計算", "支払う", "給与"],
        "beforeText": "quiz_exclusions: [計算]",
        "afterText": "quiz_exclusions: [計算, 支払う, 給与]",
    },
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def path_at(root, name):
    return root.joinpath(*name.split("/"))


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(ROOT), *args])


def show(name):
    return git("show", f"{SNAPSHOT}:{name}")


def metadata(text):
    return yaml.safe_load(text.replace("\r\n", "\n").split("---", 2)[1])


def verify_exception(old, new, row):
    name = row["article"]
    require(name in EXCEPTIONS, f"Unexpected reviewed exception: {name}")
    expected = EXCEPTIONS[name]
    require(all(row.get(key) == value for key, value in expected.items()),
            f"Reviewed exception differs from the authorized exact delta: {name}")
    require(metadata(old).get("quiz_exclusions", []) == expected["before"],
            f"Previous exclusions differ: {name}")
    reused_changes(old, new, [{"before": expected["beforeText"], "after": expected["afterText"]}],
                   exclusions=expected["after"])


def verify_original_audit(audit, manifest):
    require(audit["batch"] == "107" and audit["sourceSnapshot"] == SOURCE
            and audit["membership"] == ["勘"], "Original audit identity differs")
    for key in ("frozenInputHashesVerified", "decompressedDictionaryHashesVerified",
                "baselineMetadataPreserved", "allOtherBaselineRuntimeHashesPreserved", "manifestFresh"):
        require(audit[key] is True, f"Original audit did not establish {key}")
    require(audit["exactReusedEditsVerified"] == 5
            and audit["contentVersion"] == manifest["contentVersion"], "Original runtime audit differs")


def verify_source_changes(changed, untracked):
    source_changes = {(status, name) for status, name in changed if name.startswith("docs/n1-sources/")}
    require(source_changes == {("A", SIGNED_ADDITION)}
            and not any(name.startswith("docs/n1-sources/") for name in untracked),
            "Original source evidence changed or an unexpected addition appeared")


def audit(reaudit_path=None):
    ledger = json.loads((REVIEW / "reconciliation.json").read_text(encoding="utf-8"))
    require(ledger["reviewedSnapshot"] == SNAPSHOT and ledger["signedSourceSnapshot"] == SOURCE,
            "Reconciliation snapshot differs")
    require(git("log", "-1", "--format=%G?", SNAPSHOT).strip() == b"G",
            "Reviewed snapshot signature is not verified")
    original_manifest = json.loads(show("manifest.json"))
    original_audit_path = "docs/n1-sources/batch-107-runtime-audit.json"
    original_audit_blob = show(original_audit_path)
    original_audit_live = path_at(ROOT, original_audit_path).read_bytes()
    require(original_audit_live.replace(b"\r\n", b"\n") == original_audit_blob.replace(b"\r\n", b"\n"),
            "Original signed audit changed")
    verify_original_audit(json.loads(original_audit_blob), original_manifest)
    reaudit_hash = None
    if reaudit_path is not None:
        raw = reaudit_path.read_bytes()
        reaudit_hash = digest(raw)
        require(reaudit_hash == ledger["originalSnapshotReauditSha256"],
                "Fresh original-snapshot audit receipt differs")
        verify_original_audit(json.loads(raw), original_manifest)
    changes = git("diff", "--no-renames", "--name-status", "-z", SNAPSHOT).decode("utf-8").split("\0")
    changed = list(zip(changes[::2], changes[1::2]))
    untracked = git("ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0")
    verify_source_changes(changed, untracked)
    require(git("log", "-1", "--format=%G?", EVIDENCE_TIP).strip() == b"G",
            "Historical evidence commit signature is not verified")
    signed_addition = git("show", f"{EVIDENCE_TIP}:{SIGNED_ADDITION}")
    live_addition = path_at(ROOT, SIGNED_ADDITION).read_bytes()
    require(live_addition.replace(b"\r\n", b"\n") == signed_addition.replace(b"\r\n", b"\n"),
            "Signed historical denial evidence changed")
    current_manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    require(current_manifest == build_manifest(ROOT), "Current manifest is stale")
    rows = ledger["postReviewExclusionExceptions"]
    require(len(rows) == len(EXCEPTIONS)
            and {row["article"] for row in rows} == set(EXCEPTIONS),
            "Reviewed exception membership differs")
    runtime_delta(original_manifest, current_manifest, set(), set(EXCEPTIONS))
    for row in rows:
        name = row["article"]
        before = show(name).decode("utf-8")
        after = path_at(ROOT, name).read_text(encoding="utf-8")
        verify_exception(before, after, row)
        declared = metadata(after)
        require(declared["word"] == name.removeprefix("words/").removesuffix(".md"),
                f"Reused word identity differs: {name}")
        for other_name in row["otherArticles"]:
            other = metadata(path_at(ROOT, other_name).read_text(encoding="utf-8"))
            require(other["word"] in declared["quiz_exclusions"],
                    f"Direct exclusion target differs: {name} -> {other_name}")
    for entry in ("claude", "gpt"):
        report = ledger["initialReviews"][entry]
        require(digest((REVIEW / report["report"]).read_bytes()) == report["reportSha256"],
                f"Original {entry} report changed")
    return {
        "batch": "107",
        "reviewedSnapshot": SNAPSHOT,
        "reviewedSnapshotSignatureVerified": True,
        "originalAuditInSignedSnapshotVerified": True,
        "freshOriginalReauditSha256": reaudit_hash,
        "originalSourceEvidenceUnchanged": True,
        "signedHistoricalDenialEvidencePreserved": True,
        "exactPostReviewAdditiveExclusions": sorted(EXCEPTIONS),
        "allOtherRuntimePayloadsUnchanged": True,
        "originalReportsByteVerified": True,
        "manifestFresh": True,
        "contentVersion": current_manifest["contentVersion"],
        "runtimeHashCount": sum(len(value) for value in current_manifest.values() if isinstance(value, dict)),
        "limits": "Incremental source/runtime preservation only; all original-reviewer confirmations, production, native and publication gates remain separate.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--original-reaudit", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.original_reaudit)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=True))
