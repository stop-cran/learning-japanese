"""B134 integration contracts; unlike linear B134, C->M->I retains incoming main.

v2 of b134_integrated_v1.py: REVIEWED comes from b134_integration_v2 (cc374051) and the
original ledger is validated by b134_revision_progress; all other contracts are unchanged.

C closes the original review; M has parents (C, INCOMING); I adds only an integration
archive and two ledger keys. Plans bind future confirmation evidence, never create it.
No signing/network/worktree writes occur in this module.
"""
import json
import re
import sys
from pathlib import Path, PurePosixPath

from b134_revision_progress import validate_progress
from b134_integration_v2 import CHANGED, CONTENT, INCOMING, REVIEWED, check_incoming, check_merged, expected_manifest
from common import GUARD_SHA, WS, frozen, require, sha
from run_b134_closure_checks import BASE, CLOSURE, HELPERS, ORDER, PROGRESS, lineage
from verify_b134_payload import runtime_entries
from verify_b134_sources import FINGERPRINT, OWNER, TRAILER

REPO = WS / "b134-worktree"
REVIEW = WS / "scratch-134" / "review"
SCRATCH = WS / "scratch-134"
INTEGRATION = "docs/n1-reviews/batch-134-integration-001/"
PUBLICATION = "docs/n1-reviews/batch-134-integration-publication-001/"
EXTENSION_KEYS = {"activeReviewedSnapshot", "integrationReview"}
HEX = re.compile(r"[0-9a-f]{40}")
TOOLS = ("b134_integrated_v2.py", "run_b134_integration_gates_v2.py",
         "verify_b134_integration_closure_v2.py", "deliver_b134_integration_v2.py",
         "record_b134_integration_publication_v2.py", "b134_integration_v2.py",
         "b134_revision_progress.py")


def full(*values):
    require(all(isinstance(value, str) and HEX.fullmatch(value) for value in values),
            "Full commit IDs required")


def relative(name):
    path = PurePosixPath(name)
    require(isinstance(name, str) and name and not path.is_absolute()
            and path.as_posix() == name and "\\" not in name and ":" not in name
            and all(part not in ("", ".", "..") for part in path.parts), "Unsafe inventory path")
    return name


def read_ref(ref):
    require(isinstance(ref, dict) and set(ref) == {"path", "sha256"}
            and Path(ref["path"]).is_absolute()
            and re.fullmatch(r"[0-9a-f]{64}", ref["sha256"]), "Invalid frozen reference")
    return frozen(ref["path"], ref["sha256"])


def blob(git, commit, path):
    return git("show", f"{commit}:{path}")


def tree(git, commit):
    result = {}
    for row in git("ls-tree", "-r", "-z", commit).split(b"\0"):
        if row:
            meta, path = row.split(b"\t", 1)
            name = relative(path.decode("utf-8"))
            require(name not in result, "Duplicate tree path")
            result[name] = tuple(meta.decode("ascii").split())
    return result


def identity(git, commit, parents):
    full(commit, *parents)
    require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", commit).decode().strip()
            == f"{' '.join(parents)}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
            and TRAILER in git("show", "-s", "--format=%B", commit),
            "Owner signature, parent order, identity or trailer differs")


def inventory(blobs, metadata=("provenance.json",)):
    require(set(metadata) <= set(blobs), "Missing archive metadata")
    recorded = {}
    for filename in metadata:
        rows = json.loads(blobs[filename])["recordedFileSha256"]
        require(isinstance(rows, dict), "Invalid archive inventory")
        for name, digest in rows.items():
            relative(name)
            require(name not in metadata and recorded.setdefault(name, digest) == digest,
                    "Cyclic/conflicting inventory")
    require(set(blobs) == set(recorded) | set(metadata), "Archive inventory is not exact")
    for name, digest in recorded.items():
        require(sha(blobs[name]) == digest, "Changed archive bytes: " + name)


def archive(git, commit, prefix):
    entries = tree(git, commit)
    result = {}
    for name, row in entries.items():
        if name.startswith(prefix):
            require(row[:2] == ("100644", "blob"), "Archive entry not regular")
            result[name[len(prefix):]] = blob(git, commit, name)
    require(result, "Missing archive: " + prefix)
    return result


def original(git, closure):
    full(closure)
    lineage(git, REVIEWED)
    identity(git, closure, [REVIEWED])
    before, after = tree(git, REVIEWED), tree(git, closure)
    require(set(before) <= set(after), "Original closure removed a path")
    delta = {p for p in before if before[p] != after[p]} | (after.keys() - before.keys())
    require(delta and all(p == PROGRESS or p.startswith(CLOSURE) for p in delta),
            "Original closure altered teaching")
    require(blob(git, REVIEWED, "manifest.json") == blob(git, closure, "manifest.json"),
            "Original closure changed manifest")
    records = archive(git, closure, CLOSURE)
    inventory(records)
    ledger = blob(git, closure, PROGRESS)
    counts = validate_progress(json.loads(ledger), REVIEWED,
                               blob(git, REVIEWED, "manifest.json"), records["provenance.json"])
    return ledger, counts


def merge(git, closure, merged=None, staged=None, manifest=None):
    """Verify signed graph and exact object delta; staged is a fully resolved merge index."""
    original(git, closure)
    identity(git, INCOMING, [BASE])
    before, incoming, base = (tree(git, rev) for rev in (closure, INCOMING, BASE))
    check_incoming(base, incoming)
    require(git("merge-base", closure, INCOMING).decode().strip() == BASE, "Wrong integration merge base")
    require(all(base[p] == before[p] for p in CONTENT), "Incoming content overlaps B134")
    if merged:
        identity(git, merged, [closure, INCOMING])
        after = tree(git, merged)
        manifest = blob(git, merged, "manifest.json")
    else:
        require(staged is not None and manifest is not None, "Missing staged merge")
        after = staged
    check_merged(before, after, incoming)
    incoming_bytes = {p: blob(git, INCOMING, p) for p in CONTENT}
    require(blob(git, INCOMING, "manifest.json") == expected_manifest(
                json.loads(blob(git, BASE, "manifest.json")), incoming_bytes),
            "Incoming deterministic manifest differs")
    require(manifest == expected_manifest(json.loads(blob(git, closure, "manifest.json")), incoming_bytes),
            "Merged deterministic manifest differs")
    builder = blob(git, BASE, "tools/build_manifest.py")
    require(all(blob(git, rev, "tools/build_manifest.py") == builder
                for rev in (closure, INCOMING)), "Manifest builder changed")
    old, new = (runtime_entries(json.loads(raw)) for raw in
                (blob(git, closure, "manifest.json"), manifest))
    require(old.keys() == new.keys() and len(new) == 8747
            and {p for p in old if old[p] != new[p]} == CONTENT
            and all(old[p][1] == new[p][1] for p in old), "Runtime membership/classification changed")
    return {"reviewedSnapshot": REVIEWED, "closure": closure, "incoming": INCOMING,
            "merge": merged, "manifestSha256": sha(manifest),
            "contentVersion": json.loads(manifest)["contentVersion"], "runtimeEntries": len(new)}


def load_plan(path):
    """Coordinator freezes this only after real merge gates and two accepted confirmations."""
    raw = frozen(path)
    plan = json.loads(raw)
    require(set(plan) == {"schemaVersion", "batch", "reviewedSnapshot", "signedClosure", "merge",
                         "incoming", "originalGates", "mergeGates", "confirmations", "toolInventory"}
            and plan["schemaVersion"] == 1 and plan["batch"] == 134
            and plan["reviewedSnapshot"] == REVIEWED and plan["incoming"] == INCOMING,
            "Invalid integration plan")
    full(plan["signedClosure"], plan["merge"])
    tools = json.loads(read_ref(plan["toolInventory"]))
    require(set(tools) == {"files"} and set(TOOLS) <= set(tools["files"]),
            "Tool inventory omits integration implementations")
    for name, digest in tools["files"].items():
        require(Path(name).name == name, "Tool inventory path escapes")
        frozen(Path(__file__).parent / name, digest)
    require(set(plan["originalGates"]) == {"closure", "committed"}
            and set(plan["mergeGates"]) == {"merge", "committed-merge"}
            and set(plan["confirmations"]) == {"claude", "gpt"}, "Missing evidence families/gates")
    return plan, raw


def accepted(plan):
    """B130 acceptance interface; future confirmation tooling must supply actual evidence."""
    sessions, runs, result = set(), set(), {}
    for family in ("claude", "gpt"):
        ref = plan["confirmations"][family]
        raw = read_ref(ref)
        value = json.loads(raw)
        require(value["batch"] == 134 and value["family"] == family
                and re.fullmatch(r"N1-B134-" + family.upper() + r"-INTEGRATION-[0-9]{3}", value["run"])
                and value["candidate"] == plan["merge"] and value["verdict"] == "CONFIRMED"
                and value["confirmationAccepted"] is True and value["reviewEvidenceAccepted"] is True
                and value["acceptedNewFindings"] == value["openClaimIds"] == []
                and value["session"] not in sessions and value["run"] not in runs,
                "Integration confirmation not independently accepted")
        sessions.add(value["session"])
        runs.add(value["run"])
        evidence = {key: read_ref(value[key]) for key in ("report", "final", "adjudication")}
        final, adjudication = (json.loads(evidence[key]) for key in ("final", "adjudication"))
        require(final["candidate"] == adjudication["candidate"] == plan["merge"]
                and final["session"] == adjudication["session"] == value["session"]
                and final["run"] == adjudication["run"] == value["run"]
                and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
                and final["report"] == value["report"] == adjudication["report"]
                and adjudication["verdict"] == "CONFIRMED"
                and adjudication["acceptedNewFindings"] == adjudication["openClaimIds"] == []
                and adjudication["rawAuditWasClean"] is True
                and adjudication["controlAdjudicationApplied"] is False,
                "Integration final/report/adjudication binding differs")
        result[family] = {"acceptance": raw, **evidence, "run": value["run"], "session": value["session"]}
    return result


def extension(before, after):
    require(before.keys() <= after.keys()
            and {p for p in before if before[p] != after[p]} == {PROGRESS},
            "Integration closure changed an old path other than ledger")
    added = after.keys() - before.keys()
    require(added and all(p.startswith(INTEGRATION) for p in added)
            and after[PROGRESS][:2] == ("100644", "blob")
            and all(after[p][:2] == ("100644", "blob") for p in added),
            "Integration closure adds non-regular/out-of-scope paths")
    return added


def closure_data(plan, before_ledger, ledger, blobs, manifest, confirmations):
    require(not (EXTENSION_KEYS & set(before_ledger)) and set(ledger) == set(before_ledger) | EXTENSION_KEYS
            and {k: v for k, v in ledger.items() if k not in EXTENSION_KEYS} == before_ledger,
            "Ledger must preserve every original value; exactly two additive keys allowed")
    inventory(blobs, ("provenance.json", "validation-provenance.json"))
    require(not any(name.endswith(".jsonl") for name in blobs), "Raw private event streams must remain local")
    provenance = json.loads(blobs["provenance.json"])
    validation = json.loads(blobs["validation-provenance.json"])
    runtime = {"manifestSha256": sha(manifest), "contentVersion": json.loads(manifest)["contentVersion"],
               "runtimeEntries": len(runtime_entries(json.loads(manifest)))}
    review = ledger["integrationReview"]
    expected_runs = [confirmations[f]["run"] for f in ("claude", "gpt")]
    require(ledger["activeReviewedSnapshot"] == review["reviewedSnapshot"] == plan["merge"]
            and review["previousReviewedSnapshot"] == REVIEWED
            and review["parents"] == [plan["signedClosure"], INCOMING]
            and review["status"] == "closed-with-disclosed-limits"
            and review["finalRuns"] == expected_runs
            and review["closurePath"] == INTEGRATION.rstrip("/")
            and review["runtimeCandidate"] == runtime
            and review["closureProvenanceSha256"] == sha(blobs["provenance.json"])
            and review["validationProvenanceSha256"] == sha(blobs["validation-provenance.json"]),
            "Integration ledger lineage/runtime differs")
    require(provenance["batch"] == 134 and provenance["reviewedSnapshot"] == plan["merge"]
            and provenance["previousReviewedSnapshot"] == REVIEWED
            and provenance["parents"] == [plan["signedClosure"], INCOMING]
            and provenance["runtimeCandidate"] == runtime and provenance["finalRuns"] == expected_runs
            and provenance["publication"] == "PENDING" and provenance["deliveryCredit"] == 0
            and validation["candidate"] == plan["merge"]
            and validation["reviewClosureSha256"] == sha(blobs["provenance.json"]),
            "Integration archive metadata differs")
    require(isinstance(review["limits"], list) and review["limits"]
            and all(isinstance(s, str) and s.strip() for s in review["limits"])
            and provenance["limits"] == review["limits"], "Explicit integration limits required")
    for family, evidence in confirmations.items():
        for key in ("acceptance", "report", "final", "adjudication"):
            require(blobs.get(f"runs/{evidence['run']}/{key}.{'md' if key == 'report' else 'json'}")
                    == evidence[key], f"Missing exact accepted {family} {key}")
    return {"activeReviewedSnapshot": plan["merge"], "runtime": runtime,
            "finalRuns": expected_runs, "integrationLimits": review["limits"]}


def verify_closure(git, plan, commit, signed=True, staged=None, read=None):
    merge(git, plan["signedClosure"], plan["merge"])
    if signed:
        identity(git, commit, [plan["merge"]])
        after = tree(git, commit)
        read = lambda name: blob(git, commit, name)
    else:
        require(staged is not None and read is not None, "Uncommitted closure inputs absent")
        after = staged
    added = extension(tree(git, plan["merge"]), after)
    manifest = blob(git, plan["merge"], "manifest.json")
    require(read("manifest.json") == manifest, "Integration closure changed manifest")
    before_raw = blob(git, plan["merge"], PROGRESS)
    require(before_raw == blob(git, plan["signedClosure"], PROGRESS), "Merge changed prior ledger")
    blobs = {name[len(INTEGRATION):]: read(name) for name in added}
    require(blobs.get("previous-progress.json") == before_raw, "Previous ledger not byte-exact")
    context = closure_data(plan, json.loads(before_raw), json.loads(read(PROGRESS)), blobs,
                           manifest, accepted(plan))
    return {**context, "closure": commit if signed else None, "archiveFiles": len(blobs)}


def expected_commands():
    lean = WS / "lean"
    commands = {
        "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", "\u7d2b"],
        "quiz-safety": [lean / "quiz_safety.py", "\u7d2b"],
        "linkplan": [lean / "n1_linkplan.py", "verify", BASE, "\u7d2b"],
        "reading-exposure": [SCRATCH / "check_reading_134.py"],
        "validate": [REPO / "tools" / "validate.py"],
        "manifest": [REPO / "tools" / "build_manifest.py"],
        "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
        "budget": [REPO / "tools" / "check_content_budget.py"],
        "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
        "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
    }
    return {name: [sys.executable, "-B", str(SCRATCH / "bounded_launch_134.py"), *map(str, args)]
            for name, args in commands.items()}


def gate_ref(ref, mode, closure, merged, head, manifest_sha):
    raw = read_ref(ref)
    summary = json.loads(raw)
    require(summary["status"] == "PASS" and summary["batch"] == 134
            and summary["mode"] == mode and summary["signedClosure"] == closure
            and summary["merge"] == merged and summary["head"] == head
            and summary["reviewedSnapshot"] == REVIEWED and summary["incoming"] == INCOMING
            and summary["checks"] == ORDER and summary["serial"] is True
            and summary["base"] == BASE
            and summary["manifestSha256"] == manifest_sha and summary["manifestReproducible"] is True
            and summary["commands"] == expected_commands()
            and summary["producerSha256"] == sha(
                Path(__file__).with_name("run_b134_integration_gates_v2.py").read_bytes())
            and not summary["memory"]["breach"] and set(summary["logs"]) == set(ORDER),
            "Integration host gates do not bind this tree")
    folder = Path(ref["path"]).parent
    for name in HELPERS:
        frozen(SCRATCH / name, summary["helperHashes"][name])
    previous_end = None
    for name in ORDER:
        item = summary["logs"][name]
        receipt = json.loads(frozen(folder / f"{name}.json", item["receiptSha256"]))
        log = frozen(folder / f"{name}.log", item["logSha256"])
        require(receipt["gate"] == name and receipt["exitCode"] == 0
                and receipt["childExitCodeAfterCleanup"] == 0 and not receipt["cleanupError"]
                and not receipt["activeError"] and not receipt["memory"]["breach"]
                and receipt["logSha256"] == sha(log) and receipt["base"] == BASE
                and receipt["cwd"] == str(REPO)
                and receipt["command"] == summary["commands"][name]
                and receipt["runnerSha256"] == summary["helperHashes"]["run_134_gates.py"]
                and receipt["commonHelperSha256"] == summary["helperHashes"]["common_134.py"]
                and receipt["boundedLauncherSha256"] == summary["helperHashes"]["bounded_launch_134.py"]
                and receipt["guardSha256"] == GUARD_SHA
                and receipt["waitTimeoutSeconds"] == .1 and receipt["cleanupTimeoutSecondsPerStage"] == 10
                and receipt["startedAt"] <= receipt["completedAt"]
                and (previous_end is None or previous_end <= receipt["startedAt"]),
                "Incomplete/changed gate execution: " + name)
        previous_end = receipt["completedAt"]
        if name in ("manifest", "manifest-rebuild"):
            require(receipt["manifestSha256"] == manifest_sha, "Gate manifest bytes differ")
        if name == "manifest-rebuild":
            require(receipt["manifestReproducible"] is True, "Manifest not reproduced")
    return raw


def plan_gates(git, plan):
    """Retain the original unchanged closure gates and exact pre/post-sign merge gates."""
    from deliver_b134 import gate
    manifest = blob(git, REVIEWED, "manifest.json")
    closure_raw = blob(git, plan["signedClosure"], CLOSURE + "provenance.json")
    for mode in ("closure", "committed"):
        ref = plan["originalGates"][mode]
        read_ref(ref)
        gate(ref["path"], mode, REVIEWED, plan["signedClosure"], manifest, closure_raw)
    merged_manifest = blob(git, plan["merge"], "manifest.json")
    for mode in ("merge", "committed-merge"):
        raw = gate_ref(plan["mergeGates"][mode], mode, plan["signedClosure"],
                       None if mode == "merge" else plan["merge"],
                       plan["signedClosure"] if mode == "merge" else plan["merge"], sha(merged_manifest))
        summary = json.loads(raw)
        from run_b134_integration_gates_v2 import tree_digest
        require(summary["treeInventorySha256"] == tree_digest(tree(git, plan["merge"])),
                "Merge gates describe a different tree")
        for name in HELPERS:
            require(summary["helperHashes"][name] == sha(blob(
                git, REVIEWED, f"docs/n1-sources/batch-134/producers/{name}")),
                "Gate producer differs from owner-signed helper")
