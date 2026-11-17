"""C/M/I-aware B134 delivery; no linear-tool globals are patched.

Reuses the original exact-ZIP verifier, served-entry hashing and owner identity rules.
Push I only over INCOMING, and receipt R only over I; both must be fast-forwards.
Signing is one bounded attempt, never retried. GH credentials are scoped to stop-cran
without changing global auth. Only explicit CLI sign/push/checkpoint commands write.

Usage:
  sign closure PLAN PRE_CLOSURE_GATES OUT
  sign receipt PLAN PUBLISHED OUT
  push closure PLAN I PRE_CLOSURE_GATES COMMITTED_CLOSURE_GATES OUT
  push receipt PLAN R OUT
  zip COMMIT OUT | ci COMMIT OUT
  equal PLAN I R I_ZIP_DIR R_ZIP_DIR R_CI OUT
  checkpoint PLAN I R R_CI EQUALITY COMMENT_REQUEST OUT
OUT is a new direct review child. sign receipt requires recorder-generated files.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import b134_integrated_v2 as contract
import deliver_b134 as linear
from common import GUARD, GUARD_SHA, freeze_json, frozen, json_bytes, load_module, require, sha, start_guard
from record_b117_publication_v3 import validate_delivery
from verify_b134_packet import RUNNER
from verify_b134_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

REPOSITORY = "stop-cran/learning-japanese"
STATUS = "published-verified-with-disclosed-review-limits"


def new_output(path):
    output = Path(path).resolve()
    require(output.parent == contract.REVIEW and not output.exists(), "Use a new direct review output")
    return output


def command(git, args, env=None, timeout=None, log=None):
    process = subprocess.Popen(args, cwd=contract.REPO, env=env,
                               stdout=log or subprocess.PIPE, stderr=subprocess.STDOUT if log else subprocess.PIPE)
    if timeout is None:
        raw, error = git.wait(process)
    else:
        deadline = time.monotonic() + timeout
        try:
            while process.poll() is None:
                git.guard.check()
                if time.monotonic() >= deadline:
                    raise TimeoutError("Signing stalled; preserve staged work and ask the user to sign again.")
                try:
                    process.wait(timeout=.1)
                except subprocess.TimeoutExpired:
                    continue
        finally:
            git.cleanup.stop_child(process)
        raw, error = b"", b""
    require(process.returncode == 0, "Command failed without retry: " + args[0]
            + (": " + error.decode("utf-8", "replace") if error else ""))
    return raw


def owner_env(git):
    token = command(git, ["gh", "auth", "token", "--hostname", "github.com", "--user", "stop-cran"]).decode().strip()
    require(bool(token) and "\n" not in token, "Owner credential unavailable")
    env = {**os.environ, "GH_TOKEN": token}
    require(json.loads(command(git, ["gh", "api", "user"], env))["login"] == "stop-cran",
            "Scoped account is not the repository owner")
    return env


def api(git, *args):
    return command(git, ["gh", *args], owner_env(git))


def clean(git, commit):
    require(git("rev-parse", "HEAD").decode().strip() == commit
            and not git("status", "--porcelain=v1", "--untracked-files=all"), "Wrong or dirty HEAD")
    require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")


def remote_commit(git, commit):
    remote = json.loads(api(git, "api", f"repos/{REPOSITORY}/commits/{commit}"))
    require(remote["sha"] == commit and remote["commit"]["verification"]["verified"] is True
            and remote["author"]["login"] == remote["committer"]["login"] == "stop-cran",
            "Remote owner signature not verified")
    return remote


def remote_head(git, expected):
    require(git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == expected,
            "Remote main differs; never force-push or silently substitute a new target")


def published_ledger(before, after, commit, proof):
    """Keep the original and additive integration review values even when credit advances."""
    counts = {"publishedPendingRecordsWithCards": 272, "publishedN1Additions": 266, "undelivered": 956}
    expected = json.loads(json.dumps(before))
    expected.update(status=STATUS, published=["\u7d2b"], runtimePublished=True, limits=proof["limits"])
    expected["accounting"].update(counts)
    expected["publication"] = {"commit": commit, "url": proof["publishedCommitUrl"],
                               "receipt": "../n1-reviews/batch-134-integration-publication-001/provenance.json"}
    require(after == expected and after["accounting"]["overallN1TaskComplete"] is False,
            "Receipt ledger changed historical values or publication accounting")


def publication_files(read):
    proof_raw = read(contract.PUBLICATION + "provenance.json")
    proof = json.loads(proof_raw)
    inventory = proof["recordedFileSha256"]
    require(isinstance(inventory, dict) and inventory, "Publication inventory missing")
    for path, digest in inventory.items():
        contract.relative(path)
        require(path != "provenance.json" and sha(read(contract.PUBLICATION + path)) == digest,
                "Publication evidence changed")
    return proof, proof_raw


def publication_proof(read, plan, published, manifest, plan_sha, git):
    proof, raw = publication_files(read)
    require(proof["batch"] == 134 and proof["base"] == contract.BASE
            and proof["publishedCommit"] == published and proof["activeReviewedSnapshot"] == plan["merge"]
            and proof["signedOriginalClosure"] == plan["signedClosure"] and proof["incoming"] == contract.INCOMING
            and proof["reviewedSnapshot"] == contract.REVIEWED and proof["status"] == STATUS
            and proof["planSha256"] == plan_sha, "Receipt publication identity differs")
    ci_raw, zip_raw = (read(contract.PUBLICATION + name) for name in ("ci-run.json", "zip-receipt.json"))
    ci, archive = json.loads(ci_raw), json.loads(zip_raw)
    validate_delivery(published, manifest, ci, archive)
    require(ci["workflowName"] == "Validate content" and proof["ci"] == {
                "runId": ci["databaseId"], "url": ci["url"], "sha256": sha(ci_raw)}
            and proof["archive"] == {
                "zipSha256": archive["sha256"], "receiptSha256": sha(zip_raw),
                "verifiedRuntimeHashes": archive["verifiedRuntimeHashes"], "contentVersion": archive["contentVersion"]}
            and proof["sourceAccounting"] == {"delivered": 272, "n1Additions": 266, "n2Placements": 6,
                                              "remaining": 956, "overallN1TaskComplete": False},
            "Publication CI/ZIP/accounting differs")
    from run_b134_integration_gates_v2 import tree_digest
    require(set(proof["gateRefs"]) == {"closure", "committed-closure"}, "Missing publication gates")
    for mode, head in (("closure", plan["merge"]), ("committed-closure", published)):
        ref = proof["gateRefs"][mode]
        summary = closure_gate(ref, mode, plan, head, manifest)
        require(read(contract.PUBLICATION + f"gates/{mode}/summary.json") == summary
                and json.loads(summary)["treeInventorySha256"] == tree_digest(contract.tree(git, published)),
                "Archived publication gates describe another tree")
        for name in contract.ORDER:
            for suffix in ("json", "log"):
                require(read(contract.PUBLICATION + f"gates/{mode}/{name}.{suffix}")
                        == frozen(Path(ref["path"]).parent / f"{name}.{suffix}"),
                        "Archived gate execution bytes differ")
    return proof, raw


def receipt_tree(git, plan, published, receipt, plan_sha):
    contract.verify_closure(git, plan, published)
    contract.identity(git, receipt, [published])
    before, after = contract.tree(git, published), contract.tree(git, receipt)
    require(before.keys() <= after.keys()
            and {p for p in before if before[p] != after[p]} == {contract.PROGRESS},
            "Receipt changed an existing path outside its ledger")
    added = after.keys() - before.keys()
    require(added and all(p.startswith(contract.PUBLICATION) and after[p][:2] == ("100644", "blob")
                          for p in added), "Receipt added out-of-scope/nonregular files")
    read = lambda name: contract.blob(git, receipt, name)
    manifest = contract.blob(git, published, "manifest.json")
    proof, raw = publication_proof(read, plan, published, manifest, plan_sha, git)
    require(added == {contract.PUBLICATION + n for n in proof["recordedFileSha256"]}
            | {contract.PUBLICATION + "provenance.json"}, "Publication inventory is not exact")
    published_ledger(json.loads(contract.blob(git, published, contract.PROGRESS)),
                     json.loads(read(contract.PROGRESS)), published, proof)
    return manifest, proof, raw


def closure_gate(ref, mode, plan, head, manifest):
    return contract.gate_ref(ref, mode, plan["signedClosure"], plan["merge"], head, sha(manifest))


def sign(kind, plan_path, evidence, out):
    require(kind in ("closure", "receipt"), "Invalid signing mode")
    plan, plan_raw = contract.load_plan(Path(plan_path))
    output = new_output(out)
    guard, _ = start_guard("B134 integrated signature")
    output.mkdir()
    result = {"mode": kind, "attempted": False, "planSha256": sha(plan_raw)}
    try:
        git = Git(contract.REPO, RUNNER, guard)
        parent = plan["merge"] if kind == "closure" else evidence
        contract.full(parent)
        require(git("rev-parse", "HEAD").decode().strip() == parent
                and git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Signing parent/origin differs")
        require(git("config", "user.email").decode().strip() == OWNER
                and git("config", "user.signingkey").decode().strip() == FINGERPRINT
                and git("config", "user.name").decode().strip()
                == git("show", "-s", "--format=%an", contract.REVIEWED).decode().strip(),
                "Wrong owner signing configuration")
        require(not git("diff", "--cached", "--name-only"), "Existing staged work must be preserved")
        from run_b134_integration_gates_v2 import tree_digest, working_tree
        working = working_tree(git, contract.REPO, guard)
        manifest = (contract.REPO / "manifest.json").read_bytes()
        if kind == "closure":
            contract.verify_closure(git, plan, parent, False, working,
                                    lambda name: (contract.REPO / name).read_bytes())
            contract.plan_gates(git, plan)
            gate_path = Path(evidence)
            ref = {"path": str(gate_path.resolve()), "sha256": sha(frozen(gate_path))}
            gate_raw = closure_gate(ref, "closure", plan, parent, manifest)
            require(json.loads(gate_raw)["treeInventorySha256"] == tree_digest(working),
                    "Pre-sign closure gates describe another tree")
            prefix = contract.INTEGRATION
        else:
            contract.verify_closure(git, plan, parent)
            proof, _ = publication_proof(lambda name: frozen(contract.REPO / name), plan,
                                         parent, manifest, sha(plan_raw), git)
            published_ledger(json.loads(contract.blob(git, parent, contract.PROGRESS)),
                             json.loads(frozen(contract.REPO / contract.PROGRESS)), parent, proof)
            prefix = contract.PUBLICATION
            # Validate the full pending receipt tree with the same exact scope as committed receipts.
            previous = contract.tree(git, parent)
            require(previous.keys() <= working.keys()
                    and {p for p in previous if previous[p] != working[p]} == {contract.PROGRESS}
                    and working.keys() - previous.keys()
                    == {prefix + n for n in proof["recordedFileSha256"]} | {prefix + "provenance.json"}
                    and all(working[p][:2] == ("100644", "blob") for p in
                            (working.keys() - previous.keys()) | {contract.PROGRESS}),
                    "Pending receipt exceeds its exact publication inventory")
        require(manifest == contract.blob(git, parent, "manifest.json"), "Signing changed runtime")
        git("add", "--sparse", "--", contract.PROGRESS, prefix)
        paths = git("diff", "--cached", "--name-only", "-z").decode().split("\0")
        for path in filter(None, paths):
            require(path == contract.PROGRESS or path.startswith(prefix), "Unexpected staged path")
            require(git("show", ":" + path) == (contract.REPO / path).read_bytes(), "Staging differs")
        git("-c", linear.WHITESPACE, "diff", "--cached", "--check")
        result.update(parent=parent, treeInventorySha256=tree_digest(working), attempted=True)
        freeze_json(output / "staged.json", result)
        with (output / "commit.log").open("xb") as log:
            command(git, ["git", "--no-pager", "commit", "-S", "-m",
                         "Close B134 integration review" if kind == "closure" else "Record B134 integrated delivery",
                         "-m", TRAILER.decode()], timeout=75, log=log)
        commit = git("rev-parse", "HEAD").decode().strip()
        contract.identity(git, commit, [parent])
        clean(git, commit)
        require(tree_digest(contract.tree(git, commit)) == tree_digest(working), "Signed tree differs")
        if kind == "closure":
            contract.verify_closure(git, plan, commit)
        else:
            receipt_tree(git, plan, parent, commit, sha(plan_raw))
        result.update(commit=commit, status="PASS_SIGNED_ONLY")
    finally:
        result["memory"] = guard.finish()
        log_path = output / "commit.log"
        if log_path.exists():
            log_path.chmod(0o444)
            result["logSha256"] = sha(frozen(log_path))
        freeze_json(output / "receipt.json", result)
    require(not result["memory"]["breach"], "Signing RAM breach")
    print(json.dumps(result))


def push(kind, plan_path, commit, pre_gates, committed_gates, out):
    require(kind in ("closure", "receipt"), "Invalid push mode")
    plan, plan_raw = contract.load_plan(Path(plan_path))
    output = new_output(out)
    output.mkdir()  # A failed attempt is retained and cannot be silently retried.
    result = {"mode": kind, "commit": commit, "planSha256": sha(plan_raw), "attempted": False}
    guard, _ = start_guard("B134 integrated fast-forward push")
    try:
        git = Git(contract.REPO, RUNNER, guard)
        clean(git, commit)
        contract.plan_gates(git, plan)
        if kind == "closure":
            contract.verify_closure(git, plan, commit)
            manifest = contract.blob(git, commit, "manifest.json")
            for mode, path, head in (("closure", pre_gates, plan["merge"]),
                                     ("committed-closure", committed_gates, commit)):
                ref = {"path": str(Path(path).resolve()), "sha256": sha(frozen(path))}
                raw = closure_gate(ref, mode, plan, head, manifest)
                from run_b134_integration_gates_v2 import tree_digest
                require(json.loads(raw)["treeInventorySha256"] == tree_digest(contract.tree(git, commit)),
                        "Closure gate tree does not equal published tree")
            expected = contract.INCOMING
        else:
            expected = git("show", "-s", "--format=%P", commit).decode().strip()
            manifest, _, _ = receipt_tree(git, plan, expected, commit, sha(plan_raw))
        remote_head(git, expected)
        git("merge-base", "--is-ancestor", expected, commit)
        env = owner_env(git)
        result.update(previousRemote=expected, attempted=True)
        freeze_json(output / "attempt.json", result)
        # No --force/--force-with-lease. Git's normal push rejects a concurrent non-FF advance.
        pushed = command(git, ["git", "--no-pager", "-c", "credential.helper=",
                             "-c", "credential.helper=!gh auth git-credential",
                             "push", "origin", "HEAD:refs/heads/main"], env).decode()
        remote_head(git, commit)
        remote = remote_commit(git, commit)
        result.update(status="PASS_PUSH_ONLY", url=remote["html_url"], pushOutput=pushed,
                      manifestSha256=sha(manifest))
    finally:
        result["memory"] = guard.finish()
        freeze_json(output / "receipt.json", result)
    require(not result["memory"]["breach"], "Push RAM breach")
    print(json.dumps(result))


def zip_check(commit, out):
    contract.full(commit)
    output = new_output(out)
    guard, _ = start_guard("B134 integrated exact ZIP")
    try:
        git = Git(contract.REPO, RUNNER, guard)
        clean(git, commit)
        frozen(GUARD, GUARD_SHA)
        verifier = load_module("b134_integrated_exact_zip", GUARD)
        def bounded_git(repo, *args):
            require(Path(repo) == contract.REPO, "ZIP Git escaped")
            return git(*args)
        verifier.git = bounded_git
        output.mkdir()
        receipt = verifier.verify(contract.REPO, commit, output, guard)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "ZIP RAM breach")
    receipt.update(memory=memory, verifierSha256=GUARD_SHA, wrapperSha256=sha(frozen(Path(__file__))))
    print(json.dumps(freeze_json(output / "receipt.json", receipt)))


def ci(commit, out):
    contract.full(commit)
    output = new_output(out)
    guard, _ = start_guard("B134 integrated CI")
    try:
        git = Git(contract.REPO, RUNNER, guard)
        runs = json.loads(api(git, "run", "list", "--repo", REPOSITORY, "--commit", commit,
                              "--workflow", "validate.yml", "--limit", "5", "--json",
                              "databaseId,headSha,status,conclusion,url,workflowName"))
        require(runs and all(row["headSha"] == commit for row in runs), "Exact CI not available")
        raw = api(git, "run", "view", str(runs[0]["databaseId"]), "--repo", REPOSITORY, "--json",
                  "databaseId,headSha,status,conclusion,url,workflowName,jobs,createdAt,updatedAt")
        value = json.loads(raw)
        require(value["headSha"] == commit and value["workflowName"] == "Validate content"
                and value["status"] == "completed" and value["conclusion"] == "success", "CI not successful yet")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "CI RAM breach")
    print(json.dumps(freeze_json(output / "ci.json", value)))


def equal(plan_path, published, receipt, first_zip, second_zip, ci_path, out):
    plan, plan_raw = contract.load_plan(Path(plan_path))
    output = new_output(out)
    guard, _ = start_guard("B134 integrated served-tree equality")
    try:
        git = Git(contract.REPO, RUNNER, guard)
        clean(git, receipt)
        manifest, proof, _ = receipt_tree(git, plan, published, receipt, sha(plan_raw))
        ci_raw = frozen(ci_path)
        committed_ci = json.loads(contract.blob(git, receipt, contract.PUBLICATION + "ci-run.json"))
        require(frozen(Path(first_zip) / "receipt.json")
                == contract.blob(git, receipt, contract.PUBLICATION + "zip-receipt.json"),
                "Published ZIP receipt differs from signed receipt")
        first, a = linear.entries(Path(first_zip), published, manifest, committed_ci, guard)
        second, b = linear.entries(Path(second_zip), receipt, manifest, json.loads(ci_raw), guard)
        result = {"publishedCommit": published, "receiptCommit": receipt, **linear.compare(first, second),
                  "publishedZipSha256": a["sha256"], "receiptZipSha256": b["sha256"],
                  "receiptCiSha256": sha(ci_raw), "planSha256": sha(plan_raw),
                  "manifestSha256": sha(manifest)}
        require(result["namesEqual"] and result["contentEqual"], "Served trees differ")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Served equality RAM breach")
    result.update(memory=memory, verifierSha256=sha(frozen(Path(__file__))))
    print(json.dumps(freeze_json(output / "equality.json", result)))


def checkpoint(plan_path, published, receipt, ci_path, equality_path, comment_path, out):
    plan, plan_raw = contract.load_plan(Path(plan_path))
    output = new_output(out)
    output.mkdir()  # Persist the attempt even if network admission fails.
    guard, _ = start_guard("B134 integrated issue checkpoint")
    try:
        git = Git(contract.REPO, RUNNER, guard)
        clean(git, receipt)
        manifest, proof, _ = receipt_tree(git, plan, published, receipt, sha(plan_raw))
        remote_head(git, receipt)
        remote = remote_commit(git, receipt)
        ci_raw, equal_raw = frozen(ci_path), frozen(equality_path)
        observed, equality = json.loads(ci_raw), json.loads(equal_raw)
        live = json.loads(api(git, "run", "view", str(observed["databaseId"]), "--repo", REPOSITORY,
                              "--json", "databaseId,headSha,status,conclusion,url,workflowName"))
        require(live["headSha"] == receipt and live["status"] == "completed"
                and live["conclusion"] == "success" and live["workflowName"] == "Validate content",
                "Receipt CI not successful")
        require(equality["publishedCommit"] == published and equality["receiptCommit"] == receipt
                and equality["planSha256"] == sha(plan_raw) and equality["manifestSha256"] == sha(manifest)
                and equality["receiptCiSha256"] == sha(ci_raw)
                and equality["namesEqual"] is True and equality["contentEqual"] is True
                and equality["differing"] == equality["onlyInPublished"] == equality["onlyInReceipt"] == []
                and not equality["memory"]["breach"]
                and equality["verifierSha256"] == sha(frozen(Path(__file__)))
                and equality["entries"][0] == equality["entries"][1] > 8747,
                "Equality evidence differs")
        request = json.loads(frozen(comment_path))
        require(request["publishedCommit"] == published and request["planSha256"] == sha(plan_raw),
                "Comment request describes another publication")
        body = linear.checkpoint_body(request["body"], remote["html_url"], live["url"], equality["entries"][0])
        matches, page = [], 1
        while True:
            comments = json.loads(api(git, "api", f"repos/{REPOSITORY}/issues/60/comments?per_page=100&page={page}"))
            matches.extend(row for row in comments if re.search(r"\bB134\b", row["body"]))
            if len(comments) < 100:
                break
            page += 1
        request_path = output / "request.json"
        freeze_json(request_path, {"body": body})
        if matches:
            require(len(matches) == 1 and matches[0]["body"] == body
                    and matches[0]["user"]["login"] == "stop-cran", "Existing checkpoint differs")
            posted = matches[0]
        else:
            posted = json.loads(api(git, "api", "--method", "POST",
                                    f"repos/{REPOSITORY}/issues/60/comments", "--input", str(request_path)))
        readback = json.loads(api(git, "api", f"repos/{REPOSITORY}/issues/comments/{posted['id']}"))
        require(readback["body"] == body and readback["user"]["login"] == "stop-cran", "Checkpoint differs")
        freeze_json(output / "receipt.json", {
            "comment": readback, "publishedCommit": published, "receiptCommit": receipt,
            "planSha256": sha(plan_raw), "equalitySha256": sha(equal_raw), "delivered": 272,
            "remaining": 956, "overallN1TaskComplete": False})
    finally:
        require(not guard.finish()["breach"], "Checkpoint RAM breach")


def dispatch(argv):
    action, *args = argv or [""]
    if action == "sign" and len(args) == 4:
        return sign, args
    if action == "push" and len(args) in (4, 6):
        require((args[0] == "closure") == (len(args) == 6), "Invalid push mode/arity")
        if args[0] == "receipt":
            args = [*args[:3], None, None, args[3]]
        return push, args
    commands = {("zip", 2): zip_check, ("ci", 2): ci, ("equal", 7): equal, ("checkpoint", 7): checkpoint}
    require((action, len(args)) in commands, __doc__)
    return commands[(action, len(args))], args


if __name__ == "__main__":
    operation, arguments = dispatch(sys.argv[1:])
    operation(*arguments)
