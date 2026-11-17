"""Verify B133's signed producers, bounded launcher and actual serial gate runs."""
import ast
import json
import sys
from pathlib import Path

from common import GUARD_SHA, WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
HELPERS = {
    "verify_b133_payload.py": "b75726e35d93210a18fe72b953e5437b90d7f4efa0caedebcdc6c9f662b6b775",
    "verify_b133_sources.py": "84135cb99ff36f31bd6ac27fa9a82dd656c14dcf4d20c98c6852c45745cd5e71",
    "verify_b130_evidence_v3.py": "23228af0051d8e87a5ce1864671c668587c1554591cee6a841cb8a2ea303737f",
    "verify_b131_gate_evidence_v2.py": "d020a08e2a97b54ac54284f854d116a8751ffa314f6124788b10a673bb1b7411",
    "verify_b132_gates.py": "7cda33ace62becb4bee073ac6a8d89d2362e0aeaa130e0215e92824339c7c669",
}

from verify_b133_payload import (
    BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, LINK_HELPER, LINK_HELPER_SHA, runtime_entries)
from verify_b133_sources import Git
from verify_b130_evidence_v3 import ORDER, verify_execution
from verify_b131_gate_evidence_v2 import memory_ok
from verify_b132_gates import verify_reading_output

SCRATCH = HERE.parent


def commands():
    lean = WS / "lean"
    targets = {
        "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", *MEMBERS],
        "quiz-safety": [lean / "quiz_safety.py", *MEMBERS],
        "linkplan": [lean / "n1_linkplan.py", "verify", BASE, *MEMBERS],
        "reading-exposure": [SCRATCH / "check_reading_133.py"],
        "validate": [REPO / "tools" / "validate.py"],
        "manifest": [REPO / "tools" / "build_manifest.py"],
        "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
        "budget": [REPO / "tools" / "check_content_budget.py"],
        "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
        "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
    }
    return {name: [SCRATCH / "bounded_launch_133.py", *args] for name, args in targets.items()}


def verify_summary(summary, admission, mode, candidate, manifest_sha, runner_sha, common_sha, launcher_sha):
    head = BASE if mode == "author" else candidate
    require(admission["base"] == BASE and admission["head"] == head and admission["mode"] == mode,
            "Gate admission binds another snapshot")
    memory_ok(admission["memory"])
    require(type(summary["batch"]) is int and summary["batch"] == 133
            and summary["mode"] == mode and summary["status"] == "PASS"
            and summary["base"] == BASE and summary["startingHead"] == head
            and summary["checks"] == list(ORDER) and summary["serial"] is True
            and summary["manifestSha256"] == manifest_sha
            and summary["runnerSha256"] == runner_sha and summary["commonHelperSha256"] == common_sha
            and summary["boundedLauncherSha256"] == launcher_sha
            and summary["guardSha256"] == GUARD_SHA and summary["waitTimeoutSeconds"] == 0.1
            and summary["cleanupTimeoutSecondsPerStage"] == 10, "Gate summary differs")
    memory_ok(summary["finalMemory"])


def verify_launcher(receipts, logs, launcher_sha):
    for name in ORDER:
        require(receipts[name]["boundedLauncherSha256"] == launcher_sha,
                "Gate used another bounded launcher")
        prefix = "B133 bounded launcher memory: "
        records = [line[len(prefix):] for line in logs[name].splitlines() if line.startswith(prefix)]
        require(len(records) == 1, "Missing or duplicate inner-launcher memory receipt")
        memory_ok(json.loads(records[0]))


def verify_runtime_maps(manifest, files_map, full_map):
    runtime = {name: digest for name, (digest, _) in runtime_entries(manifest).items()}
    require(files_map == manifest["files"], "Files-only preservation inventory differs")
    require(full_map == runtime, "Full-runtime preservation omits or changes manifest entries")
    return runtime


def main(proof_name, proof_sha, author_name, recheck_name, committed_name, preservation_name,
         full_runtime_name, output_name):
    names = (proof_name, author_name, recheck_name, committed_name, preservation_name, full_runtime_name, output_name)
    require(all(Path(name).name == name and name not in {"", ".", ".."} for name in names),
            "Direct path names required")
    require(len(set(names)) == len(names), "Input and output names must differ")
    for name, digest in HELPERS.items():
        frozen(TOOLS / name, digest)
    output = HERE / output_name
    require(not output.exists(), "Preserve gate-verification output")
    proof_raw = frozen(HERE / proof_name, proof_sha)
    payload = json.loads(proof_raw)
    require(payload["batch"] == 133 and payload["base"] == BASE and payload["status"] == "PASS"
            and payload["verifierSha256"] == HELPERS["verify_b133_payload.py"]
            and not payload["memory"]["breach"], "Wrong accepted payload proof")
    candidate, manifest_sha = payload["candidate"], payload["manifestSha256"]
    handoff_raw = frozen(HERE / "author-handoff-observed-001.json",
                         "f2c951b0814b87202eb66117c425ac02bbc5a5847b21255c010ce6955ce8f4b2")
    handoff = json.loads(handoff_raw)
    require(handoff["candidate"] == candidate and handoff["base"] == BASE
            and handoff["manifestSha256"] == manifest_sha, "Handoff snapshot differs")
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b133_gate_bindings", LINK_HELPER)
    guard, _ = start_guard("B133 committed gate and preservation evidence")
    git = Git(REPO, RUNNER, guard)
    captured, signed, groups = {}, {}, {}

    def blob(name):
        raw = git("show", candidate + ":" + PREFIX + name)
        signed[PREFIX + name] = sha(raw)
        return raw

    def capture(name, path):
        raw = path.read_bytes()
        captured[name] = raw
        return raw

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout differs")

    try:
        clean()
        for name in ("common_133.py", "run_133_gates.py", "check_reading_133.py",
                     "bounded_launch_133.py", "preserve_133.py"):
            require((SCRATCH / name).read_bytes() == blob("producers/" + name),
                    "Executed producer differs from signed bytes: " + name)
        common_sha = signed[PREFIX + "producers/common_133.py"]
        runner_sha = signed[PREFIX + "producers/run_133_gates.py"]
        launcher_sha = signed[PREFIX + "producers/bounded_launch_133.py"]
        for group, directory_name in (("author", author_name), ("author-recheck", recheck_name),
                                      ("committed", committed_name)):
            mode = "committed" if group == "committed" else "author"
            directory = SCRATCH / directory_name
            admission_raw = capture(group + "/admission.json", directory / "admission.json")
            summary_raw = capture(group + "/summary.json", directory / "summary.json")
            admission, summary = json.loads(admission_raw), json.loads(summary_raw)
            verify_summary(summary, admission, mode, candidate, manifest_sha, runner_sha, common_sha, launcher_sha)
            bindings = helper.gate_bindings(directory, {"repo": str(REPO)}, manifest_sha, runner_sha, guard)
            receipts, logs = {}, {}
            for binding in bindings:
                gate = binding["gate"]
                for suffix, key in (("json", "receiptSha256"), ("log", "logSha256")):
                    name = f"{gate}.{suffix}"
                    raw = capture(group + "/" + name, directory / name)
                    require(sha(raw) == binding[key], "Gate changed during readback")
                    if group == "author":
                        require(raw == blob(f"author-evidence/{directory_name}/{name}"),
                                "Signed author gate copy differs")
                receipt = json.loads(captured[group + f"/{gate}.json"])
                require(receipt["base"] == BASE, "Gate receipt base differs")
                receipts[gate] = receipt
                logs[gate] = captured[group + f"/{gate}.log"].decode("utf-8")
            verify_execution(receipts, commands(), common_sha)
            verify_launcher(receipts, logs, launcher_sha)
            require(summary["logs"] == {r["gate"]: {key: r[key] for key in ("receiptSha256", "logSha256")}
                                        for r in bindings}, "Gate summary inventory differs")
            if group == "author":
                for name, raw in (("admission.json", admission_raw), ("summary.json", summary_raw)):
                    require(raw == blob(f"author-evidence/{directory_name}/{name}"),
                            "Signed author admission or summary differs")
            else:
                require(handoff["receipts"][directory_name]["directory"] == str(directory)
                        and handoff["receipts"][directory_name]["summarySha256"] == sha(summary_raw),
                        "Handoff gate binding differs")
            groups[group] = {"directory": str(directory), "summarySha256": sha(summary_raw),
                             "gates": bindings, "acceptedRun": True, "signedCopy": group == "author"}
        extras = json.loads(blob("reading-keys.json"))["testedKeys"]
        reading_source = blob("producers/check_reading_133.py")
        expected = ast.parse(
            'extras = json.loads((PACKET / "reading-keys.json").read_bytes())["testedKeys"]'
        ).body[0].value
        values = [node.value for node in ast.parse(reading_source).body if isinstance(node, ast.Assign)
                  and any(isinstance(target, ast.Name) and target.id == "extras" for target in node.targets)]
        require(len(values) == 1 and ast.dump(values[0]) == ast.dump(expected),
                "Reading producer does not consume the signed key map")
        latent = verify_reading_output(captured["committed/reading-exposure.log"].decode("utf-8"), extras)
        for name in ("summary.json", "memory.json", "runtime-hashes.json"):
            capture("preservation/" + name, SCRATCH / preservation_name / name)
        preservation = json.loads(captured["preservation/summary.json"])
        require(preservation["status"] == "PASS" and preservation["mode"] == "committed"
                and preservation["head"] == candidate and preservation["base"] == BASE
                and preservation["clean"] is True and preservation["manifestSha256"] == manifest_sha
                and preservation["producerSha256"] == signed[PREFIX + "producers/preserve_133.py"]
                and preservation["memory"] == json.loads(captured["preservation/memory.json"]),
                "Committed preservation binding differs")
        memory_ok(preservation["memory"])
        manifest_raw = git("show", candidate + ":manifest.json")
        require(sha(manifest_raw) == manifest_sha, "Signed manifest changed")
        for name in ("summary.json", "memory.json", "all-runtime-hashes.json"):
            capture("full-runtime/" + name, SCRATCH / full_runtime_name / name)
        full = json.loads(captured["full-runtime/summary.json"])
        local_producer = capture("full-runtime/full_runtime_133.py", SCRATCH / "full_runtime_133.py")
        manifest = json.loads(manifest_raw)
        baseline = json.loads(git("show", BASE + ":manifest.json"))
        runtime = verify_runtime_maps(manifest, json.loads(captured["preservation/runtime-hashes.json"]),
                                      json.loads(captured["full-runtime/all-runtime-hashes.json"]))
        before = runtime_entries(baseline)
        changed = sorted(name for name, (digest, _) in before.items() if runtime[name] != digest)
        require(preservation["allCandidateRuntimeHashesChecked"] == len(manifest["files"]),
                "Files-only preservation misstates its scope")
        require(full["status"] == "PASS" and full["mode"] == "committed"
                and full["head"] == candidate and full["base"] == BASE
                and full["manifestSha256"] == manifest_sha and full["contentVersion"] == manifest["contentVersion"]
                and full["producerSha256"] == sha(local_producer) == handoff["localFullRuntimeProducer"]["sha256"]
                and full["memory"] == json.loads(captured["full-runtime/memory.json"])
                and full["candidateRuntimeCount"] == len(runtime)
                and full["baselineRuntimeCount"] == len(before)
                and full["allOtherRuntimeEntriesUnchanged"] == len(before) - len(changed)
                and full["added"] == sorted(runtime.keys() - before.keys())
                and full["removed"] == sorted(before.keys() - runtime.keys()) and full["changed"] == changed
                and full["manifestGroups"] == {
                    key: {"baseline": len(baseline[key]), "candidate": len(values)}
                    for key, values in manifest.items() if isinstance(values, dict)}
                and full["allCandidateRuntimeHashesSha256"]
                == sha(captured["full-runtime/all-runtime-hashes.json"])
                == handoff["runtime"]["allCandidateRuntimeHashesSha256"],
                "Full-runtime companion snapshot, scope or hash binding differs")
        memory_ok(full["memory"])
        for key, directory_name in (("preservation", preservation_name), ("full-runtime", full_runtime_name)):
            require(handoff["receipts"][directory_name]["directory"] == str(SCRATCH / directory_name)
                    and handoff["receipts"][directory_name]["summarySha256"]
                    == sha(captured[key + "/summary.json"]), "Handoff preservation binding differs")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    bindings = {name: write_frozen(output / name, raw) for name, raw in captured.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 133, "status": "PASS", "candidate": candidate, "base": BASE,
        "payloadProof": {"path": str(HERE / proof_name), "sha256": sha(proof_raw)},
        "handoffSha256": sha(handoff_raw),
        "signedInputs": signed, "capturedInputs": bindings, "gates": groups,
        "supplementalReadingKeys": extras, "observedLatentCollisions": latent,
        "preservation": {"directory": str(SCRATCH / preservation_name),
                         "summarySha256": sha(captured["preservation/summary.json"])},
        "fullRuntime": {"directory": str(SCRATCH / full_runtime_name),
                        "summarySha256": sha(captured["full-runtime/summary.json"]),
                        "producer": "Local unsigned companion, captured and handoff-hash-bound; not a signed producer."},
        "helpers": HELPERS, "memory": memory, "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "Actual serial command/receipt, bounded-launcher and signed-producer bindings; "
                  "explicit reading keys and complete runtime preservation. Latent smaller-pool "
                  "collisions remain disclosed. Not independent linguistic, arbitrary-pool, "
                  "native/device, rendered or publication acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 9,
            "Usage: verify_b133_gates.py PROOF SHA AUTHOR_DIR RECHECK_DIR COMMITTED_DIR PRESERVATION_DIR FULL_RUNTIME_DIR OUTPUT_DIR")
    main(*sys.argv[1:])
