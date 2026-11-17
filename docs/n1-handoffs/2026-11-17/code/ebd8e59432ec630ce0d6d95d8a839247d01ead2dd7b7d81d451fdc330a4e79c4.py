"""B130 integration-aware delivery recorder.

record_b130_publication.py binds ledger["reviewedSnapshot"] and batch-130-closure. B130's confirmed
runtime is a later signed main-integration merge whose closure additively extends that ledger. This
successor validates the preserved original lineage, the integration merge, both pinned accepted
integration confirmations and the new archive before selecting the integrated snapshot. It keeps the
exact-manifest and contributor-only post-review invariants and leaves the original recorder unchanged.
"""
import json
import subprocess
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, json_bytes, load_batch, require, sha, start_guard, write_frozen
from confirm_v2 import clean
from record_b117_publication_v3 import validate_delivery
from record_b130_publication import FROZEN_PENDING, delivery_accounting, load_narrative
from verify_b130_payload import RUNNER
from verify_b130_sources import FINGERPRINT, Git, OWNER, TRAILER

ACTIVE = "37a53e75446bacad8ade4e212404b121d4a01af1"
PREVIOUS = "1ac4053c5da955c3afaafc1e879e63a98ee42526"
PARENTS = ["9151a6f6ad5bdba9b58178167fba4cabab876504", "153c6b833f68d99f59cbbce34b0bdc6d09a59bc7"]
RUNTIME = {"manifestSha256": "23583ae2a885bd67212f8a541415a08bd6411c05763e1813bbd13145a7399495",
           "contentVersion": "3df59f6cf1dee0f2", "runtimeEntries": 8730}
INTEGRATED_PATHS = {"articles/numbers-and-counters.md", "counters/age.json", "manifest.json"}
FINAL_RUNS = ["N1-B130-CLAUDE-CONFIRM-005", "N1-B130-GPT-CONFIRM-004"]
ACCEPTANCES = {
    "N1-B130-CLAUDE-CONFIRM-005": "2fda565acde87bea3b5d06c6ac9f8ffdeb93f81241342a8bdcb92a5fd974f6aa",
    "N1-B130-GPT-CONFIRM-004": "6f5026409b120973533ff183038bd2b2983d446fdf55f4f4c763d9be1e0bb3ae",
}
LEDGER = "docs/n1-sources/batch-130-progress.json"
ORIGINAL_CLOSURE = "docs/n1-reviews/batch-130-closure"
INTEGRATION_CLOSURE = "docs/n1-reviews/batch-130-integration-001"
INTEGRATION_KEYS = ("activeReviewedSnapshot", "integrationReview")
METADATA = ("provenance.json", "validation-provenance.json")


def head(config, commit):
    return git(config, "rev-list", "--parents", "-n", "1", commit).decode().split()


def tree(config, commit, path):
    return git(config, "rev-parse", f"{commit}:{path}").decode().strip()


def names(config, old, new):
    return set(git(config, "diff", "--name-only", "--no-renames", "-z", old, new)
               .decode("utf-8").split("\0")) - {""}


def tracked_tree(config, commit):
    entries = {}
    for row in filter(None, git(config, "ls-tree", "-r", "-z", commit).decode("utf-8").split("\0")):
        metadata, path = row.split("\t", 1)
        require(path not in entries, "Duplicate tracked path")
        entries[path] = tuple(metadata.split())
    return entries


def check_extension(before, after):
    require(LEDGER in before and set(before) <= set(after), "Closure removed an existing tracked path")
    require({path for path in before if before[path] != after[path]} == {LEDGER},
            "Closure changed an existing path other than its primary ledger")
    added = set(after) - set(before)
    require(added and all(path.startswith(INTEGRATION_CLOSURE + "/") for path in added),
            "Closure adds files outside its distinct integration archive")
    require(after[LEDGER][:2] == ("100644", "blob")
            and all(after[path][:2] == ("100644", "blob") for path in added),
            "Closure contains a non-regular file or mode change")
    return added


def owner_signature(config, commit, parents):
    require(git(config, "show", "-s", "--format=%P|%G?|%GF|%ae|%ce", commit).decode().strip()
            == f"{' '.join(parents)}|G|{FINGERPRINT}|{OWNER}|{OWNER}",
            "Commit parent, owner or signing key differs")
    require(TRAILER in git(config, "show", "-s", "--format=%B", commit), "Required trailer is missing")


def archive_blobs(config, commit, prefix):
    rows = git(config, "ls-tree", "-r", "-z", commit, "--", prefix).decode("utf-8").split("\0")
    oids = {}
    for row in filter(None, rows):
        meta, path = row.split("\t", 1)
        mode, kind, oid = meta.split()
        require(kind == "blob" and mode == "100644" and path.startswith(prefix + "/"),
                f"Unexpected archive entry: {path}")
        oids[path[len(prefix) + 1:]] = oid
    require(oids, "Integration archive is missing")
    guard, _ = start_guard("B130 committed review archive")
    try:
        objects = Git(config["repo"], RUNNER, guard).objects(list(oids.values()))
        blobs = {}
        for (path, oid), (actual_oid, raw) in zip(oids.items(), objects, strict=True):
            require(oid == actual_oid, f"Unreadable archive blob: {path}")
            blobs[path] = raw
            guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Archive read breached its RAM guard")
    return blobs


def verify_archive(blobs, candidate, closure_sha, validation_sha=None):
    require(set(METADATA) <= set(blobs), "Closure metadata is missing")
    closure_raw, validation_raw = (blobs[name] for name in METADATA)
    require(sha(closure_raw) == closure_sha
            and (validation_sha is None or sha(validation_raw) == validation_sha),
            "Closure metadata hash changed")
    closure, validation = json.loads(closure_raw), json.loads(validation_raw)
    require(validation["candidate"] == candidate and validation["reviewClosureSha256"] == closure_sha,
            "Closure validation describes another revision")
    recorded = {}
    for inventory in (closure["recordedFileSha256"], validation["recordedFileSha256"]):
        require(isinstance(inventory, dict), "Closure inventory is not a map")
        for path, digest in inventory.items():
            require(path not in METADATA and recorded.setdefault(path, digest) == digest,
                    f"Conflicting or cyclic closure inventory: {path}")
    require(set(recorded) | set(METADATA) == set(blobs), "Closure inventories do not cover the exact archive")
    for path, digest in recorded.items():
        require(sha(blobs[path]) == digest, f"Closure artifact changed: {path}")
    return closure, validation, recorded


def accepted_confirmations(config):
    reports = {}
    for run, digest in ACCEPTANCES.items():
        accepted = json.loads(frozen(Path(config["reviewDir"]) / "confirm" / f"{run}-acceptance.json", digest))
        require(accepted["run"] == run and accepted["candidate"] == ACTIVE
                and accepted["verdict"] == "CONFIRMED" and accepted["confirmationAccepted"] is True
                and accepted["reviewEvidenceAccepted"] is True
                and accepted["acceptedNewFindings"] == [] and accepted["openClaimIds"] == [],
                f"Integration confirmation is not accepted cleanly: {run}")
        report = frozen(Path(accepted["report"]["path"]), accepted["report"]["sha256"])
        reports[run] = sha(report)
    return reports


def api_output(config, *args):
    guard, _ = start_guard("B130 publication GitHub read")
    try:
        runner = Git(config["repo"], RUNNER, guard)
        process = subprocess.Popen(["gh", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = runner.wait(process)
        require(process.returncode == 0, f"GitHub read failed: {err.decode('utf-8', 'replace')}")
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "GitHub read breached its RAM guard")
    return out


def original_lineage(config, ledger, base_ledger):
    require(ledger["reviewedSnapshot"] == PREVIOUS, "Original reviewed snapshot changed")
    require(head(config, ACTIVE)[1:] == PARENTS, "Integration parents changed")
    owner_signature(config, ACTIVE, PARENTS)
    owner_signature(config, PARENTS[0], [PREVIOUS])
    owner_signature(config, PARENTS[1], [config["base"]])
    require(all(path.startswith("docs/") for path in names(config, PREVIOUS, PARENTS[0])),
            "Original closure is not contributor-only")
    require(git(config, "show", f"{PREVIOUS}:manifest.json") == git(config, "show", f"{PARENTS[0]}:manifest.json"),
            "Original closure changed the reviewed runtime")
    require(names(config, PARENTS[0], ACTIVE) == INTEGRATED_PATHS, "Integration delta changed")
    for path in INTEGRATED_PATHS - {"manifest.json"}:
        require(git(config, "show", f"{ACTIVE}:{path}") == git(config, "show", f"{PARENTS[1]}:{path}"),
                f"Integrated content differs from main: {path}")
    require(git(config, "show", f"{ACTIVE}:{LEDGER}") == base_ledger, "Integration merge changed the ledger")
    original = archive_blobs(config, PARENTS[0], ORIGINAL_CLOSURE)
    original_sha = ledger["review"]["closureProvenanceSha256"]
    verify_archive(original, PREVIOUS, original_sha)
    return original_sha


def select_reviewed_snapshot(config, commit, ledger, manifest_bytes):
    """Return the integrated publication context after validating both preserved lineages."""
    base_ledger = git(config, "show", f"{PARENTS[0]}:{LEDGER}")
    require({k: v for k, v in ledger.items() if k not in INTEGRATION_KEYS} == json.loads(base_ledger)
            and set(INTEGRATION_KEYS) <= set(ledger), "Ledger is not an exact additive integration extension")
    original_sha = original_lineage(config, ledger, base_ledger)
    review = ledger["integrationReview"]
    manifest = json.loads(manifest_bytes)
    runtime = {"manifestSha256": sha(manifest_bytes), "contentVersion": manifest["contentVersion"],
               "runtimeEntries": sum(len(v) for v in manifest.values() if isinstance(v, dict))}
    require(ledger["activeReviewedSnapshot"] == review["reviewedSnapshot"] == ACTIVE
            and review["previousReviewedSnapshot"] == PREVIOUS and review["parents"] == PARENTS
            and review["status"] == "closed-with-disclosed-limits" and review["finalRuns"] == FINAL_RUNS
            and review["closurePath"] == INTEGRATION_CLOSURE and review["runtimeCandidate"] == RUNTIME == runtime,
            "Integration review metadata does not match the confirmed snapshot")
    require(isinstance(review.get("limits"), list) and review["limits"]
            and all(isinstance(limit, str) and limit.strip() for limit in review["limits"]),
            "Integration review must disclose its limits")
    require(git(config, "show", f"{ACTIVE}:manifest.json") == manifest_bytes,
            "Published teaching differs from the confirmed integrated revision")
    owner_signature(config, commit, [ACTIVE])
    before, after = tracked_tree(config, ACTIVE), tracked_tree(config, commit)
    added = check_extension(before, after)
    require(tree(config, commit, ORIGINAL_CLOSURE) == tree(config, PARENTS[0], ORIGINAL_CLOSURE),
            "Original closure archive changed")
    blobs = archive_blobs(config, commit, INTEGRATION_CLOSURE)
    require({INTEGRATION_CLOSURE + "/" + path for path in blobs} == added,
            "Integration archive is not the exact added file set")
    closure, validation, recorded = verify_archive(
        blobs, ACTIVE, review["closureProvenanceSha256"], review["validationProvenanceSha256"])
    present = set(recorded.values())
    require(sha(base_ledger) in present, "Pre-integration ledger copy is missing")
    reports = accepted_confirmations(config)
    require(set(reports.values()) <= present, "Accepted integration reports are not archived byte-exactly")
    return {"reviewedSnapshot": ACTIVE, "previousReviewedSnapshot": PREVIOUS, "parents": PARENTS,
            "runtime": runtime, "finalRuns": FINAL_RUNS, "limits": review["limits"],
            "integrationClosure": {"path": INTEGRATION_CLOSURE,
                                   "provenanceSha256": review["closureProvenanceSha256"],
                                   "validationProvenanceSha256": review["validationProvenanceSha256"],
                                   "files": len(blobs)},
            "originalClosure": {"path": ORIGINAL_CLOSURE, "provenanceSha256": original_sha,
                                "tree": tree(config, commit, ORIGINAL_CLOSURE)}}


def comment_body(batch, members, commit, url, ci_url, archive, counts, narrative):
    tree_url = f"https://github.com/stop-cran/learning-japanese/tree/{commit}/docs/n1-reviews"
    return (
        f"B{batch} **{'・'.join(members)}** is published at [{commit[:8]}]({url}). "
        f"{narrative['reviewIdentity']} {narrative['changeSummary']}\n\n"
        f"[CI passed]({ci_url}); the exact served ZIP preserves all "
        f"**{archive['verifiedRuntimeHashes']:,} runtime hashes**, content version "
        f"`{archive['contentVersion']}`, and existing archive limits. Review evidence: "
        f"[integration]({tree_url}/batch-{batch}-integration-001) and "
        f"[original closure]({tree_url}/batch-{batch}-closure).\n\n"
        f"**{counts['delivered']:,}/{FROZEN_PENDING:,} delivered** ({counts['n1Additions']} N1 additions "
        f"and {counts['n2Placements']} earlier N2 placements); **{counts['remaining']} remain**. "
        "Native/phone and arbitrary-pool acceptance remain outstanding. Next is the next bounded serial "
        "batch after this delivery checkpoint; this does not close the full N1 task."
    )


def main(batch, commit, run_id, archive_path, narrative_path):
    require(int(batch) == 130, "This integration recorder is specific to B130")
    config = load_batch(batch)
    config["reviewDir"] = str(WS / "scratch-130" / "review")
    narrative = load_narrative(narrative_path)
    clean(config, commit)
    repo = Path(config["repo"])
    api = lambda *args: api_output(config, *args)
    require(json.loads(api("api", "user"))["login"] == "stop-cran", "Wrong publishing account")
    require(git(config, "ls-remote", "origin", "refs/heads/main").decode().split()[0] == commit,
            "Remote main is not the claimed publication")
    remote = json.loads(api("api", f"repos/stop-cran/learning-japanese/commits/{commit}"))
    require(remote["sha"] == commit and remote["commit"]["verification"]["verified"]
            and remote["author"]["login"] == remote["committer"]["login"] == "stop-cran",
            "GitHub did not verify the owner-signed publication")
    ci_bytes = api("run", "view", run_id, "--repo", "stop-cran/learning-japanese", "--json",
                   "databaseId,headSha,status,conclusion,url,workflowName,jobs,createdAt,updatedAt")
    ci = json.loads(ci_bytes)
    archive_bytes = archive_path.read_bytes()
    archive = json.loads(archive_bytes)
    manifest_bytes = git(config, "show", f"{commit}:manifest.json")
    validate_delivery(commit, manifest_bytes, ci, archive)
    ledger_path = repo / LEDGER
    old_ledger = git(config, "show", f"{commit}:{LEDGER}")
    ledger = json.loads(old_ledger)
    require(ledger["status"] == "textual-review-closed-publication-pending"
            and not ledger["published"] and ledger_path.read_bytes() == old_ledger
            and str(ledger["batch"]) == str(batch) and ledger["membership"] == config["members"],
            "Unexpected delivery ledger state")
    counts = delivery_accounting(ledger)
    context = select_reviewed_snapshot(config, commit, ledger, manifest_bytes)
    index = json.loads(git(config, "show", f"{commit}:docs/n1-sources/source-index.json"))
    pending = {row["kanji"] for row in index if row["statusAtFreeze"] == "pending"}
    manifest = json.loads(manifest_bytes)
    present = {Path(path).stem for values in manifest.values() if isinstance(values, dict)
               for path in values if path.startswith("kanji/")}
    require(len(pending) == FROZEN_PENDING and len(pending & present) == counts["delivered"],
            "Delivery membership mismatch")

    out = repo / "docs" / "n1-reviews" / f"batch-{batch}-publication"
    require(not out.exists(), "Preserve the existing publication receipt")
    out.mkdir()
    write_frozen(out / ".gitattributes", b"* -text\n")
    write_frozen(out / "ci-run.json", ci_bytes)
    write_frozen(out / "zip-receipt.json", archive_bytes)
    limits = list(ledger["limits"]) + [
        "Scope of the integrated-snapshot textual reviews, not later publication checks: " + limit
        for limit in context["limits"] if limit not in ledger["limits"]]
    provenance = {
        "schemaVersion": 1, "batch": batch, "status": "published-verified-with-disclosed-review-limits",
        "publishedCommit": commit, "publishedCommitUrl": remote["html_url"],
        "base": config["base"], "initialSnapshot": config["candidate"],
        "reviewedSnapshot": context["reviewedSnapshot"],
        "previousReviewedSnapshot": context["previousReviewedSnapshot"],
        "integration": {key: context[key] for key in ("parents", "runtime", "finalRuns", "integrationClosure")},
        "originalClosure": context["originalClosure"],
        "method": "Normal owner-authenticated fast-forward; signed remote commit, CI and exact ZIP verified. "
                  "The integrated snapshot was selected only after validating the preserved original closure, "
                  "the owner-signed integration merge, both accepted integration confirmations and their archive.",
        "ci": {"url": ci["url"], "runId": ci["databaseId"], "receiptSha256": sha(ci_bytes)},
        "archive": {"zipSha256": archive["sha256"], "receiptSha256": sha(archive_bytes),
                    "verifiedRuntimeHashes": archive["verifiedRuntimeHashes"],
                    "contentVersion": archive["contentVersion"]},
        "reviewIdentity": narrative["reviewIdentity"],
        "sourceAccounting": {**counts, "overallN1TaskComplete": False},
        "limits": limits + [
            "This exact published runtime and ZIP are verified, not the remaining N1 set.",
            "A later contributor-only receipt commit needs its own CI and exported-tree equality check.",
        ],
    }
    freeze_json(out / "provenance.json", provenance)
    ledger.update(status=provenance["status"], published=ledger["membership"], runtimePublished=True)
    ledger["accounting"].update(publishedPendingRecordsWithCards=counts["delivered"],
                                publishedN1Additions=counts["n1Additions"],
                                undelivered=counts["remaining"])
    ledger["publication"] = {"commit": commit, "url": remote["html_url"],
                             "reviewedSnapshot": context["reviewedSnapshot"],
                             "receipt": f"../n1-reviews/batch-{batch}-publication/provenance.json"}
    ledger["limits"] = provenance["limits"]
    ledger_path.chmod(0o644)
    ledger_path.write_bytes(json_bytes(ledger))
    require(ledger_path.read_bytes() == json_bytes(ledger), "Ledger readback failed")
    body = comment_body(batch, ledger["membership"], commit, remote["html_url"], ci["url"],
                        archive, counts, narrative)
    freeze_json(WS / f"scratch-{batch}" / "issue60-publication-comment.json", {"body": body})
    print(json.dumps({"published": commit, "reviewedSnapshot": ACTIVE, **counts, "ci": ci["url"]}))


if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4]), Path(sys.argv[5]))
