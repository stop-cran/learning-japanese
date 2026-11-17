"""Record B133 delivery after the actual review closure, owner-signed main, CI and exact ZIP pass.

Usage: record_b133_publication.py REVIEWED COMMIT CI_RUN_ID ZIP_RECEIPT NARRATIVE
       CLOSURE_GATES COMMITTED_GATES

The two gate arguments name frozen summary.json files emitted by run_b133_closure_checks.py.
Git and gh subprocesses share that batch's bounded wait/cleanup and RAM guard.
"""
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

from common import freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen
from record_b117_publication_v3 import validate_delivery
from record_b130_publication import comment_body, delivery_accounting, load_narrative
from run_b133_closure_checks import BASE, BATCH, CANDIDATE, CLOSURE, HERE, MEMBERS, ORDER, PROGRESS, REPO, lineage
from verify_b133_packet import RUNNER
from verify_b133_sources import FINGERPRINT, OWNER, TRAILER, Git


def validate_reviews(closure, reviewed):
    require(closure["batch"] == BATCH and closure["members"] == MEMBERS
            and closure["base"] == BASE and closure["initialSnapshot"] == CANDIDATE
            and closure["reviewedSnapshot"] == reviewed and closure["publication"] == "PENDING",
            "Closure describes another batch or snapshot")
    entries = closure["reviewLineage"]
    by_run = {entry["run"]: entry for entry in entries}
    require(len(by_run) == len(entries), "Duplicate accepted review run")
    initials = [entry for entry in entries if entry["role"] == "initial"]
    require(len(initials) == 2 and {entry["family"] for entry in initials} == {"claude", "gpt"}
            and len({entry["session"] for entry in initials}) == 2
            and all(entry["snapshot"] == CANDIDATE and entry["reviewAccepted"] is True
                    for entry in initials), "Two independent same-snapshot initial reviews are required")
    originals = {entry["family"]: entry["session"] for entry in initials}
    runs = closure["finalRuns"]
    require(len(runs) == 2 and len(set(runs)) == 2 and all(run in by_run for run in runs),
            "Two distinct accepted final runs are required")
    finals = [by_run[run] for run in runs]
    require({entry["family"] for entry in finals} == {"claude", "gpt"}, "Final review families differ")
    for entry in finals:
        require(entry["reviewAccepted"] is True and entry["snapshot"] == reviewed
                and entry["session"] == originals[entry["family"]], "Final review identity/snapshot differs")
        require((entry["role"] == "initial" and entry["verdict"] == "CLEAN")
                or (entry["role"] == "confirmation" and entry["confirmation"] == "CONFIRMED"),
                "A final review is not clean or confirmed")
    inventory = closure["recordedFileSha256"]
    for entry in entries:
        for field in ("report", "final", "acceptance", "adjudication", "context", "structure"):
            ref = entry[field]
            require(inventory.get(ref["path"]) == ref["sha256"],
                    f"Review {field} is not bound to the closure inventory")
    checks = closure["publicationChecks"]
    require(checks["uuidFindings"] == checks["externalWindowFindings"] == 0,
            "Closure has unresolved publication findings")


def validate_progress(ledger, reviewed, manifest, closure_raw):
    closure = json.loads(closure_raw)
    validate_reviews(closure, reviewed)
    require(ledger["batch"] == BATCH and ledger["members"] == MEMBERS
            and ledger["base"] == BASE and ledger["initialSnapshot"] == CANDIDATE
            and ledger["reviewedSnapshot"] == reviewed
            and ledger["status"] == "textual-review-closed-publication-pending"
            and ledger["published"] == [] and ledger["runtimePublished"] is False
            and ledger["reviewClosed"] == MEMBERS, "Unexpected delivery ledger state")
    review = ledger["review"]
    require(review["closureProvenanceSha256"] == sha(closure_raw)
            and review["finalRuns"] == closure["finalRuns"]
            and review["remainingActionableFindings"] == []
            and review["remainingConsequentialClaims"] == [],
            "Review closure is unbound or has outstanding findings")
    require(ledger["manifestSha256"] == sha(manifest), "Ledger manifest differs")
    acc = ledger["accounting"]
    require(acc["publishedPendingRecordsWithCards"] == 268 and acc["publishedN1Additions"] == 262
            and acc["n2Placements"] == 6 and acc["undelivered"] == 960,
            "Publication baseline accounting differs")
    # B133's signed author/progress schema calls the membership field "members".
    return delivery_accounting({**ledger, "membership": ledger["members"]})


def validate_gate(summary, mode, reviewed, commit, manifest_sha, closure_sha, closure_files):
    require(summary["batch"] == BATCH and summary["status"] == "PASS"
            and summary["mode"] == mode and summary["base"] == BASE
            and summary["initialSnapshot"] == CANDIDATE and summary["reviewedSnapshot"] == reviewed
            and summary["head"] == (reviewed if mode == "closure" else commit)
            and summary["manifestReproducible"] is True and summary["manifestSha256"] == manifest_sha
            and summary["closureProvenanceSha256"] == closure_sha and summary["closureFiles"] == closure_files
            and summary["checks"] == ORDER and set(summary["logs"]) == set(ORDER),
            f"{mode} gates do not bind this exact closure")


def main(reviewed, commit, run_id, archive_path, narrative_path, closure_gates, committed_gates):
    require(run_id.isdigit(), "Use the numeric CI run ID")
    paths = {"closure": closure_gates, "committed": committed_gates}
    require(all(path.name == "summary.json" and path.parent.parent == HERE for path in paths.values()),
            "Use actual B133 direct-scratch gate summaries")
    out = REPO / "docs" / "n1-reviews" / f"batch-{BATCH}-publication"
    comment_path = HERE / "issue60-publication-comment.json"
    require(not out.exists() and not comment_path.exists(), "Preserve the existing publication attempt")
    narrative = load_narrative(narrative_path)
    guard, _ = start_guard("B133 publication receipt")
    try:
        git = Git(REPO, RUNNER, guard)

        def api(*args):
            process = subprocess.Popen(["gh", *args], cwd=REPO, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            raw, error = git.wait(process)
            require(process.returncode == 0, f"gh failed: {error.decode('utf-8', 'replace')}")
            return raw

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == commit
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Publication is not the clean HEAD")

        clean()
        lineage(git, reviewed)
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", commit).decode().strip()
                == f"{reviewed}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Publication identity/parent differs")
        require(TRAILER in git("show", "-s", "--format=%B", commit), "Publication lacks Copilot trailer")
        require(json.loads(api("api", "user"))["login"] == "stop-cran", "Wrong publishing account")
        require(git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == commit,
                "Remote main is not the claimed publication")
        remote = json.loads(api("api", f"repos/stop-cran/learning-japanese/commits/{commit}"))
        require(remote["sha"] == commit and remote["commit"]["verification"]["verified"]
                and remote["author"]["login"] == remote["committer"]["login"] == "stop-cran",
                "GitHub did not verify the owner-signed publication")
        ci_raw = api("run", "view", run_id, "--repo", "stop-cran/learning-japanese", "--json",
                     "databaseId,headSha,status,conclusion,url,workflowName,jobs,createdAt,updatedAt")
        ci = json.loads(ci_raw)
        require(ci["databaseId"] == int(run_id) and ci["workflowName"] == "Validate content",
                "Wrong CI workflow or run")
        archive_raw = frozen(archive_path)
        archive = json.loads(archive_raw)
        manifest = git("show", f"{commit}:manifest.json")
        validate_delivery(commit, manifest, ci, archive)
        require(git("show", f"{reviewed}:manifest.json") == manifest,
                "Published teaching differs from the reviewed snapshot")
        changes = git("diff", "--name-only", reviewed, commit).decode().splitlines()
        require(changes and all(name.startswith(CLOSURE) or name == PROGRESS for name in changes),
                "Post-review changes exceed the closure and progress ledger")
        ledger_raw = git("show", f"{commit}:{PROGRESS}")
        ledger_path = REPO / PROGRESS
        require(frozen(ledger_path) == ledger_raw, "Working progress differs from the signed blob")
        ledger = json.loads(ledger_raw)
        closure_path = REPO / CLOSURE
        closure_raw = frozen(closure_path / "provenance.json")
        closure = json.loads(closure_raw)
        counts = validate_progress(ledger, reviewed, manifest, closure_raw)
        inventory = closure["recordedFileSha256"]
        for index, (name, digest) in enumerate(inventory.items()):
            relative = PurePosixPath(name)
            require(not relative.is_absolute() and ".." not in relative.parts and "\\" not in name
                    and relative.as_posix() == name and name != "provenance.json",
                    "Noncanonical closure inventory path")
            frozen(closure_path / name, digest)
            if index % 50 == 0:
                guard.check()
        require(sorted(p.relative_to(closure_path).as_posix() for p in closure_path.rglob("*") if p.is_file())
                == sorted([*inventory, "provenance.json"]), "Closure tree differs from inventory")
        source_index = json.loads(git("show", f"{commit}:docs/n1-sources/source-index.json"))
        pending = {row["kanji"] for row in source_index if row["statusAtFreeze"] == "pending"}
        present = {Path(path).stem for value in json.loads(manifest).values() if isinstance(value, dict)
                   for path in value if path.startswith("kanji/")}
        require(len(pending) == 1228 and len(pending & present) == counts["delivered"]
                and set(MEMBERS) <= pending & present, "Delivery membership differs")
        gates = {}
        for mode, path in paths.items():
            raw = frozen(path)
            summary = json.loads(raw)
            validate_gate(summary, mode, reviewed, commit, sha(manifest), sha(closure_raw), len(inventory) + 1)
            for name in ORDER:
                ref = summary["logs"][name]
                frozen(path.parent / f"{name}.json", ref["receiptSha256"])
                frozen(path.parent / f"{name}.log", ref["logSha256"])
            gates[mode] = raw
        clean()
        require(git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == commit,
                "Remote main advanced during receipt verification")
        guard.check()

        write_frozen(out / ".gitattributes", b"* -text\n")
        write_frozen(out / "ci-run.json", ci_raw)
        write_frozen(out / "zip-receipt.json", archive_raw)
        for mode, raw in gates.items():
            write_frozen(out / "gates" / f"{mode}-summary.json", raw)
        limits = [item for item in ledger["limits"] if not item.startswith("No delivery or whole-set credit")] + [
            "This exact published runtime and ZIP are verified, not the remaining N1 set.",
            "A later contributor-only receipt commit needs its own CI and exported-tree equality check.",
        ]
        provenance = {
            "schemaVersion": 1, "batch": BATCH, "status": "published-verified-with-disclosed-review-limits",
            "publishedCommit": commit, "publishedCommitUrl": remote["html_url"],
            "base": BASE, "initialSnapshot": CANDIDATE, "reviewedSnapshot": reviewed,
            "method": "Owner-signed fast-forward main, matching Validate content CI, exact ZIP/runtime equality.",
            "ci": {"url": ci["url"], "runId": ci["databaseId"], "receiptSha256": sha(ci_raw)},
            "archive": {"zipSha256": archive["sha256"], "receiptSha256": sha(archive_raw),
                        "verifiedRuntimeHashes": archive["verifiedRuntimeHashes"],
                        "contentVersion": archive["contentVersion"]},
            "closureGates": {mode: {"path": f"gates/{mode}-summary.json", "sha256": sha(raw)}
                             for mode, raw in gates.items()},
            "closureProvenanceSha256": sha(closure_raw), "reviewIdentity": narrative["reviewIdentity"],
            "sourceAccounting": {**counts, "overallN1TaskComplete": False}, "limits": limits,
            "recorderSha256": sha(frozen(Path(__file__))),
        }
        freeze_json(out / "provenance.json", provenance)
        ledger.update(status=provenance["status"], published=MEMBERS, runtimePublished=True, limits=limits)
        ledger["accounting"].update(publishedPendingRecordsWithCards=counts["delivered"],
                                    publishedN1Additions=counts["n1Additions"], undelivered=counts["remaining"])
        ledger["publication"] = {"commit": commit, "url": remote["html_url"],
                                 "receipt": f"../n1-reviews/batch-{BATCH}-publication/provenance.json"}
        ledger_path.chmod(0o644)
        ledger_path.write_bytes(json_bytes(ledger))
        require(ledger_path.read_bytes() == json_bytes(ledger), "Progress readback failed")
        ledger_path.chmod(0o444)
        body = comment_body(BATCH, MEMBERS, commit, remote["html_url"], ci["url"], archive, counts, narrative)
        freeze_json(comment_path, {"body": body})
        print(json.dumps({"published": commit, **counts, "ci": ci["url"]}))
    finally:
        require(not guard.finish()["breach"], "B133 publication recorder RAM breach")


if __name__ == "__main__":
    if len(sys.argv) != 8:
        raise SystemExit(__doc__)
    main(*sys.argv[1:4], *(Path(value).resolve() for value in sys.argv[4:]))
