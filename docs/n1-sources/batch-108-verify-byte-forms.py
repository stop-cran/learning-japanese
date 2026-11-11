import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


EVIDENCE_COMMIT = "9d4af5cc2974b108d4aea87463c5cab644fd6f1a"
BASELINE_COMMIT = "eb7eb038e5bcff21754e158a2393c1b89b978757"
PREFIX = "docs/n1-sources/"
EVIDENCE_NAMES = (
    "batch-108-baseline-plan.json",
    "batch-108-comparison-article-snapshots.json",
    "batch-108-existing-article-snapshots.json",
    "batch-108-public-source-receipts.json",
    "batch-108-support-public-source-receipt.json",
    "batch-108-draft-861.py",
    "batch-108-character-public-text.txt",
    "batch-108-support-public-text.txt",
    "batch-108-character.html.gz",
    "batch-108-support-public.html.gz",
)
EXPECTED_COUNTS = {
    "baseline": 6210,
    "baselineCommittedRaw": 699,
    "baselineCrlfReconstruction": 5511,
    "comparisonSnapshots": 42,
    "existingSnapshots": 1,
    "publicSources": 2,
}


class VerificationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def logical_path(value):
    require(isinstance(value, str) and value, "Missing evidence path")
    path = PurePosixPath(value)
    require(
        not path.is_absolute()
        and str(path) == value
        and not any(part in (".", "..") for part in path.parts)
        and not any(char in value for char in "\\:\r\n\0"),
        "Unsafe evidence path: " + repr(value),
    )
    return value


def digest(value):
    require(isinstance(value, str) and re.fullmatch("[0-9a-f]{64}", value),
            "Invalid SHA-256")
    return value


def parse_batch(payload, paths):
    require(len(payload) <= 64 * 1024 * 1024, "Git batch exceeds byte limit")
    result = {}
    offset = 0
    for path in paths:
        end = payload.find(b"\n", offset, offset + 128)
        require(end >= 0, "Missing or oversized Git batch header")
        header = re.fullmatch(rb"([0-9a-f]{40}) blob ([0-9]{1,9})", payload[offset:end])
        require(header is not None, "Missing/non-blob Git object: " + path)
        size = int(header[2])
        require(size <= 16 * 1024 * 1024, "Git blob exceeds byte limit")
        start = end + 1
        body = payload[start:start + size]
        offset = start + size + 1
        require(len(body) == size and payload[start + size:offset] == b"\n",
                "Truncated/misframed Git blob: " + path)
        oid = hashlib.sha1(b"blob " + str(size).encode("ascii") + b"\0" + body).hexdigest()
        require(oid == header[1].decode("ascii"), "Git blob identity mismatch: " + path)
        result[path] = (oid, body)
    require(offset == len(payload), "Unexpected trailing Git batch data")
    return result


def run_git(repo, arguments, input_bytes=None):
    environment = dict(
        os.environ, GIT_OPTIONAL_LOCKS="0", GIT_NO_REPLACE_OBJECTS="1",
        GIT_NO_LAZY_FETCH="1",
    )
    process = subprocess.run(
        ["git", "--no-pager", "-C", str(repo), *arguments],
        input=input_bytes, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=120, env=environment, check=False,
    )
    require(process.returncode == 0 and not process.stderr,
            "Git acquisition failed: " + process.stderr.decode("utf-8", "backslashreplace"))
    return process.stdout


def read_blobs(repo, commit, paths):
    require(commit in (EVIDENCE_COMMIT, BASELINE_COMMIT), "Unpinned Git commit")
    require(len(paths) == len(set(paths)), "Duplicate requested Git paths")
    requests = "".join(commit + ":" + logical_path(path) + "\n" for path in paths)
    return parse_batch(run_git(repo, ["cat-file", "--batch"], requests.encode("utf-8")), paths)


def read_baseline_tree(repo):
    payload = run_git(
        repo, ["ls-tree", "-r", "-z", "--full-tree", BASELINE_COMMIT, "--", "kanji/", "words/"],
    )
    require(len(payload) <= 2 * 1024 * 1024 and payload.endswith(b"\0"),
            "Truncated/oversized baseline tree")
    tree = {}
    for record in payload[:-1].split(b"\0"):
        entry = re.fullmatch(rb"(100644|100755) blob ([0-9a-f]{40})\t(.+)", record)
        require(entry is not None, "Non-regular/malformed baseline tree entry")
        path = logical_path(entry[3].decode("utf-8", "strict"))
        require(path.startswith(("kanji/", "words/")) and path not in tree,
                "Duplicate/out-of-scope baseline tree entry")
        tree[path] = entry[2].decode("ascii")
    return tree


def assert_complete_inventory(inventory, tree):
    missing = sorted(set(tree) - set(inventory))
    extra = sorted(set(inventory) - set(tree))
    require(not missing and not extra,
            "Baseline inventory/tree mismatch; missing=" + repr(missing[:8])
            + "; extra=" + repr(extra[:8]))


def byte_forms(committed, captured_sha):
    digest(captured_sha)
    committed.decode("utf-8", "strict")
    lf = committed.replace(b"\r\n", b"\n")
    require(b"\r" not in lf, "Unexplained lone CR")
    crlf = lf.replace(b"\n", b"\r\n")
    if sha(committed) == captured_sha:
        relation = "committed-raw"
        reconstructed_capture = committed
    else:
        require(sha(crlf) == captured_sha, "Unexplained historical raw-byte digest")
        relation = "explicit-LF-to-CRLF-reconstruction"
        reconstructed_capture = crlf
    proof = {
        "recordedCapturedRawSha256": captured_sha,
        "committedRawSha256": sha(committed),
        "committedRawBytes": len(committed),
        "lfReconstructionSha256": sha(lf),
        "lfReconstructionBytes": len(lf),
        "crlfReconstructionSha256": sha(crlf),
        "crlfReconstructionBytes": len(crlf),
        "captureRelation": relation,
        "reconstructedCaptureBytes": len(reconstructed_capture),
        "rawOnly": False,
        "newCapture": False,
    }
    return proof, {"committed-raw": committed, "LF-reconstruction": lf,
                   "CRLF-reconstruction": crlf}


def raw_only_forms(committed, captured_sha, oid, pin):
    require(set(pin) == {"gitBlobOid", "rawSha256"}, "Raw-only pin fields changed")
    require(oid == pin["gitBlobOid"] and sha(committed) == digest(pin["rawSha256"])
            and captured_sha == pin["rawSha256"], "Raw-only identity/capture mismatch")
    committed.decode("utf-8", "strict")
    diagnostic = committed.replace(b"\r\n", b"\n")
    require(diagnostic.count(b"\r") == 1, "Raw-only exception shape changed")
    return {
        "recordedCapturedRawSha256": captured_sha,
        "committedRawSha256": sha(committed),
        "committedRawBytes": len(committed),
        "captureRelation": "committed-raw",
        "reconstructedCaptureBytes": len(committed),
        "rawOnly": True, "loneCrCount": 1,
        "noDerivedByteFormAccepted": True,
        "crlfPairReplacementOnlyDiagnosticSha256": sha(diagnostic),
        "diagnosticStillContainsLoneCr": True,
        "newCapture": False,
    }, {"committed-raw": committed}


def classify_observed(observed, forms):
    matches = [name for name, value in forms.items() if observed == value]
    require(matches, "Observed bytes match no exact pinned byte form")
    return matches


def json_without_duplicate_keys(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "Duplicate JSON key: " + key)
            result[key] = value
        return result

    return json.loads(data, object_pairs_hook=pairs)


def verify(repo, erratum, extract_directory=None):
    require(erratum["schema"] == "batch108-pinned-byte-forms-v1", "Unknown erratum schema")
    require(erratum["evidenceCommit"] == EVIDENCE_COMMIT
            and erratum["baselineCommit"] == BASELINE_COMMIT, "Snapshot pin changed")
    require(erratum["expectedCounts"] == EXPECTED_COUNTS, "Scope/count pin changed")
    raw_only = erratum["rawOnlyBaselineExceptions"]
    require(set(raw_only) == {"kanji/\u6bce.md", "words/\u884c\u304f.md"},
            "Raw-only exception scope changed")
    pins = erratum["committedEvidenceFiles"]
    require(set(pins) == {PREFIX + name for name in EVIDENCE_NAMES},
            "Original evidence pin set changed")
    originals = read_blobs(repo, EVIDENCE_COMMIT, list(pins))
    for path, expected in pins.items():
        require(sha(originals[path][1]) == digest(expected),
                "Original committed evidence digest mismatch: " + path)

    def document(name):
        return json_without_duplicate_keys(originals[PREFIX + name][1])

    plan = document("batch-108-baseline-plan.json")
    require(plan["baseCommit"] == BASELINE_COMMIT, "Historical baseline baseCommit changed")
    inventory = plan["inventory"]
    require(len(inventory) == EXPECTED_COUNTS["baseline"], "Baseline count mismatch")
    for path in inventory:
        logical_path(path)
        require(path.startswith(("kanji/", "words/")) and path.endswith(".md"),
                "Unexpected baseline article path")
    tree = read_baseline_tree(repo)
    assert_complete_inventory(inventory, tree)
    baseline = read_blobs(repo, BASELINE_COMMIT, sorted(inventory))
    baseline_rows = []
    baseline_forms = {}
    counts = {"committed-raw": 0, "explicit-LF-to-CRLF-reconstruction": 0}
    for path, item in sorted(inventory.items()):
        oid, committed = baseline[path]
        require(oid == tree[path], "Baseline tree/blob identity mismatch: " + path)
        try:
            if path in raw_only:
                proof, forms = raw_only_forms(committed, item["sha256"], oid, raw_only[path])
            else:
                proof, forms = byte_forms(committed, item["sha256"])
        except VerificationError as error:
            raise VerificationError(path + ": " + str(error)) from error
        baseline_forms[path] = forms
        baseline_rows.append({"path": path, "gitBlobOid": oid, **proof})
        counts[proof["captureRelation"]] += 1
    require(counts == {"committed-raw": 699, "explicit-LF-to-CRLF-reconstruction": 5511},
            "Baseline byte-form counts differ")

    snapshot_rows = []
    for name, expected_count in (
        ("batch-108-comparison-article-snapshots.json", 42),
        ("batch-108-existing-article-snapshots.json", 1),
    ):
        saved = document(name)
        rows = saved if isinstance(saved, list) else [saved]
        require(len(rows) == expected_count, "Saved snapshot count mismatch")
        seen = set()
        for index, row in enumerate(rows):
            article = logical_path(row["article"])
            require(article not in seen and article in baseline,
                    "Duplicate/unknown saved snapshot article")
            seen.add(article)
            text = row["text"].encode("utf-8")
            proof, forms = byte_forms(text, row["sha256"])
            require(sha(forms["CRLF-reconstruction"]) == row["sha256"],
                    "Snapshot is not the declared exact CRLF reconstruction")
            base_forms = baseline_forms[article]
            require("LF-reconstruction" in base_forms,
                    "Saved snapshot unexpectedly requires raw-only baseline normalization")
            require(forms["LF-reconstruction"] == base_forms["LF-reconstruction"],
                    "Saved text differs from baseline article: " + article)
            require(row["sha256"] == inventory[article]["sha256"],
                    "Saved raw digest differs from baseline captured digest")
            snapshot_rows.append({
                "receipt": PREFIX + name, "index": index, "article": article,
                "embeddedTextUtf8Sha256": proof.pop("committedRawSha256"),
                "embeddedTextUtf8Bytes": proof.pop("committedRawBytes"),
                "normalizedBaselineContentExactlyEqual": True, **proof,
            })
            if snapshot_rows[-1]["captureRelation"] == "committed-raw":
                snapshot_rows[-1]["captureRelation"] = "embedded-text-raw"

    source_rows = []
    for receipt_name, text_name, archive_name in (
        ("batch-108-public-source-receipts.json",
         "batch-108-character-public-text.txt", "batch-108-character.html.gz"),
        ("batch-108-support-public-source-receipt.json",
         "batch-108-support-public-text.txt", "batch-108-support-public.html.gz"),
    ):
        saved = document(receipt_name)
        receipts = saved if isinstance(saved, list) else [saved]
        require(len(receipts) == 1, "Public receipt count mismatch")
        receipt = receipts[0]
        require(receipt["extractedText"] == text_name and receipt["archive"] == archive_name,
                "Public source artifact identity changed")
        archive = originals[PREFIX + archive_name][1]
        require(sha(archive) == digest(receipt["archiveSha256"]),
                "Compressed HTML hash mismatch")
        html = gzip.decompress(archive)
        require(len(html) == receipt["rawBytes"] and sha(html) == digest(receipt["rawSha256"]),
                "Decompressed raw HTML hash/size mismatch")
        committed = originals[PREFIX + text_name][1]
        proof, forms = byte_forms(committed, receipt["extractedTextSha256"])
        require(committed == forms["LF-reconstruction"]
                and proof["captureRelation"] == "explicit-LF-to-CRLF-reconstruction",
                "Public source is not the declared LF/CRLF relation")
        record = {
            "receipt": PREFIX + receipt_name, "text": PREFIX + text_name, **proof,
            "archiveSha256": sha(archive), "rawHtmlSha256": sha(html),
            "rawHtmlBytes": len(html),
        }
        if extract_directory is not None:
            observed = (Path(extract_directory) / text_name).read_bytes()
            record["observedExactForms"] = classify_observed(observed, forms)
            record["observedRawSha256"] = sha(observed)
            record["observedMatchesHistoricalCapturedDigest"] = (
                sha(observed) == receipt["extractedTextSha256"]
            )
        source_rows.append(record)

    return {
        "schema": "batch108-pinned-byte-form-proof-v1", "passed": True,
        "evidenceCommit": EVIDENCE_COMMIT, "baselineCommit": BASELINE_COMMIT,
        "originalCommittedEvidencePins": pins, "baselineRows": baseline_rows,
        "baselineCounts": counts, "snapshotRows": snapshot_rows, "publicSourceRows": source_rows,
        "baselineRowsVerified": len(baseline_rows),
        "baselineInventoryExactlyEqualsCompleteGitTree": True,
        "baselineTreeEntryCount": len(tree),
        "baselineRawOnlyExceptionsVerified": sum(row["rawOnly"] for row in baseline_rows),
        "savedSnapshotRowsVerified": len(snapshot_rows),
        "savedSnapshotNormalizedBaselineContentVerified": len(snapshot_rows),
        "publicSourcesVerified": len(source_rows),
        "newSourceCapture": False, "historicalAuditReplay": False,
        "linuxRerun": False, "wholeAuditPortabilityFixed": False,
        "guestExecuted": False, "nativeOrPublicationCredit": False,
        "originalValidatorAndReceiptsChanged": False,
    }


def main():
    parser = argparse.ArgumentParser(description="Exact additive batch108 byte-form proof only")
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--erratum", type=Path,
                        default=Path(__file__).with_name("batch-108-byte-form-erratum.json"))
    parser.add_argument("--extract-directory", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    erratum_bytes = args.erratum.read_bytes()
    report = verify(args.repo, json_without_duplicate_keys(erratum_bytes), args.extract_directory)
    report["erratumSha256"] = sha(erratum_bytes)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=True)
        stream.write("\n")
    print(json.dumps({key: report[key] for key in (
        "passed", "baselineRowsVerified", "savedSnapshotRowsVerified",
        "publicSourcesVerified", "historicalAuditReplay", "guestExecuted",
    )}))


if __name__ == "__main__":
    try:
        main()
    except (VerificationError, OSError, subprocess.SubprocessError) as error:
        print("BYTE-FORM VERIFICATION FAILED: " + str(error), file=sys.stderr)
        sys.exit(1)
