"""Verify B134's signed producers, bounded launcher, actual serial gates, preservation and bytes."""
import ast
import json
import re
import sys
from pathlib import Path

from common import GUARD_SHA, WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
HELPERS = {
    "verify_b134_payload.py": "422a44461c37f5478d8ab2e6f52da82ce6fa76405391c6305baeecb7013b2a5f",
    "verify_b134_sources.py": "794a75b0a4d0f89bd7ec1066d9d917a262148c95159f18a20a71cc4e1d926aee",
    "verify_b130_evidence_v3.py": "23228af0051d8e87a5ce1864671c668587c1554591cee6a841cb8a2ea303737f",
    "verify_b131_gate_evidence_v2.py": "d020a08e2a97b54ac54284f854d116a8751ffa314f6124788b10a673bb1b7411",
    "verify_b132_gates.py": "7cda33ace62becb4bee073ac6a8d89d2362e0aeaa130e0215e92824339c7c669",
}
for _name, _digest in HELPERS.items():
    frozen(TOOLS / _name, _digest)

from verify_b134_payload import (
    BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, LINK_HELPER, LINK_HELPER_SHA, runtime_entries)
from verify_b134_sources import FINGERPRINT, Git
from verify_b130_evidence_v3 import ORDER, verify_execution
from verify_b131_gate_evidence_v2 import memory_ok
from verify_b132_gates import verify_reading_output

SCRATCH = HERE.parent
# Author-reported handoff hashes (coordinator ledger handoff #2); bound, not trusted alone.
HANDOFF = {
    "committed-gates-001/summary.json": "710e8bc3b9bc293718c3a94de73b6420fc34e93be0b661f90607f1c256596cb8",
    "committed-preserve-001/summary.json": "bf90220233c16bc4fcb091a45193b9186bc5331bb58080130032cea80455caae",
    "committed-preserve-001/runtime-hashes.json": "9b1a6957e25c2957f1b6dad1af500552b953c52dc45d86b2ad4ffca3251133f0",
    "committed-bytes-001.json": "cfbf6713f50b648a7e41604a92927e20b50561ec8111a68b4a1e3de0ecaf1da8",
}
# (group, directory, mode, accepted, expected quiz-safety warnings)
GROUPS = (
    ("author-superseded", "author-gates-001", "author", False, 38),
    ("author", "author-gates-002", "author", True, 0),
    ("committed", "committed-gates-001", "committed", True, 0),
)
PRESERVATION = "committed-preserve-001"
PRODUCERS = ("common_134.py", "run_134_gates.py", "check_reading_134.py",
             "bounded_launch_134.py", "preserve_134.py")
ATTEMPTS = ("author-gates-attempt-001.stdout", "author-gates-attempt-001.stderr",
            "author-gates-attempt-002.stdout", "author-gates-attempt-002.stderr")
READING_KEYS = {"\u7d2b": ["\u3057", "\u3080\u3089\u3055\u304d", "\u3086\u304b\u308a",
                           "\u3055\u3044", "\u3064\u3064\u3080"]}
LATENT_LINE = ("attested reading \u3064\u3064\u3080 (card text) is offered by \u5305; it cannot be "
               "drawn in the N1 stack, All stack or Starter practice session pool")
ADDED = ["kanji/\u7d2b.md", "strokes/\u7d2b.json"]
CHANGED = ["words/\u7d2b.md"]
OWNER = {"author": ["Roman Konstantinovskiy", "stop-cran@list.ru"],
         "committer": ["Roman Konstantinovskiy", "stop-cran@list.ru"],
         "fingerprint": FINGERPRINT, "status": "G"}


def commands():
    lean = WS / "lean"
    targets = {
        "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", *MEMBERS],
        "quiz-safety": [lean / "quiz_safety.py", *MEMBERS],
        "linkplan": [lean / "n1_linkplan.py", "verify", BASE, *MEMBERS],
        "reading-exposure": [SCRATCH / "check_reading_134.py"],
        "validate": [REPO / "tools" / "validate.py"],
        "manifest": [REPO / "tools" / "build_manifest.py"],
        "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
        "budget": [REPO / "tools" / "check_content_budget.py"],
        "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
        "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
    }
    return {name: [SCRATCH / "bounded_launch_134.py", *args] for name, args in targets.items()}


def verify_summary(summary, admission, mode, candidate, manifest_sha, runner_sha, common_sha, launcher_sha):
    head = BASE if mode == "author" else candidate
    require(admission["base"] == BASE and admission["head"] == head and admission["mode"] == mode,
            "Gate admission binds another snapshot")
    memory_ok(admission["memory"])
    require(type(summary["batch"]) is int and summary["batch"] == 134
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
        prefix = "B134 bounded launcher memory: "
        records = [line[len(prefix):] for line in logs[name].splitlines() if line.startswith(prefix)]
        require(len(records) == 1, "Missing or duplicate inner-launcher memory receipt")
        memory_ok(json.loads(records[0]))


def verify_quiz(log, warnings):
    totals = re.findall(r"^(\d+) error\(s\), (\d+) warning\(s\)$", log, re.M)
    warns = [line for line in log.splitlines() if line.startswith("WARN")]
    require(totals == [("0", str(warnings))] and len(warns) == warnings
            and all(line.endswith("is not mentioned in Notes") for line in warns),
            "Quiz-safety warning count or kind differs")
    return warnings


def verify_reading(log, extras):
    require(extras == READING_KEYS, "Signed reading keys differ")
    latent = verify_reading_output(log, extras)
    require(latent == 1 and log.count(LATENT_LINE) == 1, "Latent reading collision disclosure differs")
    return latent


def verify_reading_source(source):
    tree = ast.parse(source)

    def assigned(name):
        return [node.value for node in tree.body if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)]

    packet = assigned("packet")
    extras = assigned("extras")
    expected_packet = ast.parse('HERE / "source-002"').body[0].value
    expected_extras = ast.parse(
        'json.loads((packet / "reading-keys.json").read_bytes())["testedKeys"]').body[0].value
    require(len(packet) == 1 and ast.dump(packet[0]) == ast.dump(expected_packet)
            and len(extras) == 1 and ast.dump(extras[0]) == ast.dump(expected_extras)
            and source.count(b'ET.parse(packet / "jmdict-complete-families.xml")') == 1,
            "Reading producer inputs differ from the expected local packet copy")


def verify_preservation(preservation, memory, files_map, manifest, baseline, candidate, manifest_sha,
                        producer_sha, inventory_sha):
    require(preservation["status"] == "PASS" and preservation["mode"] == "committed"
            and preservation["head"] == candidate and preservation["base"] == BASE
            and preservation["clean"] is True and preservation["ownerSignature"] == OWNER
            and preservation["manifestSha256"] == manifest_sha
            and preservation["contentVersion"] == manifest["contentVersion"]
            and preservation["producerSha256"] == producer_sha
            and preservation["evidenceInventorySha256"] == inventory_sha
            and preservation["memory"] == memory, "Committed preservation binding differs")
    memory_ok(memory)
    before, after = baseline["files"], manifest["files"]
    require(files_map == after, "Files-only preservation inventory differs")
    added = sorted(after.keys() - before.keys())
    removed = sorted(before.keys() - after.keys())
    changed = sorted(p for p in before.keys() & after.keys() if before[p] != after[p])
    require(added == ADDED and not removed and changed == CHANGED
            and preservation["added"] == added and preservation["removed"] == removed
            and preservation["changed"] == changed
            and preservation["baselineRuntimeCount"] == len(before)
            and preservation["candidateRuntimeCount"] == len(after)
            == preservation["allCandidateRuntimeHashesChecked"]
            and preservation["allOtherRuntimeEntriesUnchanged"] == len(before) - len(changed),
            "Preservation scope or counts differ")
    other = sorted(k for k, v in manifest.items() if isinstance(v, dict) and k != "files")
    require(other == sorted(k for k, v in baseline.items() if isinstance(v, dict) and k != "files")
            and all(manifest[k] == baseline[k] for k in other),
            "Non-files runtime groups changed")
    return {"filesChecked": len(after), "unchangedNonFilesGroups": {k: len(manifest[k]) for k in other}}


def main(proof_name, proof_sha, output_name):
    names = (proof_name, output_name)
    require(all(Path(name).name == name and name not in {"", ".", ".."} for name in names)
            and proof_name != output_name, "Direct distinct path names required")
    output = HERE / output_name
    require(not output.exists(), "Preserve gate-verification output")
    proof_raw = frozen(HERE / proof_name, proof_sha)
    payload = json.loads(proof_raw)
    require(payload["batch"] == 134 and payload["base"] == BASE and payload["status"] == "PASS"
            and payload["verifierSha256"] == HELPERS["verify_b134_payload.py"]
            and not payload["memory"]["breach"], "Wrong accepted payload proof")
    candidate, manifest_sha = payload["candidate"], payload["manifestSha256"]
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b134_gate_bindings", LINK_HELPER)
    guard, _ = start_guard("B134 committed gate, preservation and byte evidence")
    git = Git(REPO, RUNNER, guard)
    captured, signed, groups, quiz = {}, {}, {}, {}

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
                and git("rev-parse", candidate + "^@").decode().split() == [BASE]
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout differs")

    try:
        clean()
        for name in PRODUCERS:
            require((SCRATCH / name).read_bytes() == blob("producers/" + name),
                    "Executed producer differs from signed bytes: " + name)
        for name in ATTEMPTS:
            require(capture("attempts/" + name, SCRATCH / name) == blob("author-evidence/attempts/" + name),
                    "Signed author gate attempt differs: " + name)
        common_sha = signed[PREFIX + "producers/common_134.py"]
        runner_sha = signed[PREFIX + "producers/run_134_gates.py"]
        launcher_sha = signed[PREFIX + "producers/bounded_launch_134.py"]
        for group, directory_name, mode, accepted, warnings in GROUPS:
            directory = SCRATCH / directory_name
            admission_raw = capture(group + "/admission.json", directory / "admission.json")
            summary_raw = capture(group + "/summary.json", directory / "summary.json")
            admission, summary = json.loads(admission_raw), json.loads(summary_raw)
            run_manifest = summary["manifestSha256"]
            require((run_manifest == manifest_sha) is accepted, "Accepted gate run must bind the candidate manifest")
            verify_summary(summary, admission, mode, candidate, run_manifest, runner_sha, common_sha, launcher_sha)
            bindings = helper.gate_bindings(directory, {"repo": str(REPO)}, run_manifest, runner_sha, guard)
            receipts, logs = {}, {}
            for binding in bindings:
                gate = binding["gate"]
                for suffix, key in (("json", "receiptSha256"), ("log", "logSha256")):
                    name = f"{gate}.{suffix}"
                    raw = capture(group + "/" + name, directory / name)
                    require(sha(raw) == binding[key], "Gate changed during readback")
                    if mode == "author":
                        require(raw == blob(f"author-evidence/{directory_name}/{name}"),
                                "Signed author gate copy differs")
                receipt = json.loads(captured[group + f"/{gate}.json"])
                require(receipt["base"] == BASE, "Gate receipt base differs")
                receipts[gate] = receipt
                logs[gate] = captured[group + f"/{gate}.log"].decode("utf-8")
            verify_execution(receipts, commands(), common_sha)
            verify_launcher(receipts, logs, launcher_sha)
            quiz[group] = verify_quiz(logs["quiz-safety"], warnings)
            require(summary["logs"] == {r["gate"]: {key: r[key] for key in ("logSha256", "receiptSha256")}
                                        for r in bindings}, "Gate summary inventory differs")
            if mode == "author":
                for name, raw in (("admission.json", admission_raw), ("summary.json", summary_raw)):
                    require(raw == blob(f"author-evidence/{directory_name}/{name}"),
                            "Signed author admission or summary differs")
            else:
                require(sha(summary_raw) == HANDOFF[directory_name + "/summary.json"],
                        "Handoff gate binding differs")
            groups[group] = {"directory": str(directory), "summarySha256": sha(summary_raw),
                             "manifestSha256": run_manifest, "gates": bindings, "acceptedRun": accepted,
                             "signedCopy": mode == "author", "quizSafetyWarnings": warnings}
        reading_source = blob("producers/check_reading_134.py")
        verify_reading_source(reading_source)
        for name in ("reading-keys.json", "jmdict-complete-families.xml"):
            require(capture("reading-input/" + name, SCRATCH / "source-002" / name) == blob(name),
                    "Reading input differs from the signed packet: " + name)
        extras = json.loads(captured["reading-input/reading-keys.json"])["testedKeys"]
        latent = {group: verify_reading(captured[group + "/reading-exposure.log"].decode("utf-8"), extras)
                  for group, _, _, accepted, _ in GROUPS if accepted}
        for name in ("summary.json", "memory.json", "runtime-hashes.json"):
            capture("preservation/" + name, SCRATCH / PRESERVATION / name)
        for name in ("summary.json", "runtime-hashes.json"):
            require(sha(captured["preservation/" + name]) == HANDOFF[PRESERVATION + "/" + name],
                    "Handoff preservation binding differs")
        manifest_raw = git("show", candidate + ":manifest.json")
        require(sha(manifest_raw) == manifest_sha, "Signed manifest changed")
        manifest = json.loads(manifest_raw)
        baseline = json.loads(git("show", BASE + ":manifest.json"))
        preservation = verify_preservation(
            json.loads(captured["preservation/summary.json"]), json.loads(captured["preservation/memory.json"]),
            json.loads(captured["preservation/runtime-hashes.json"]), manifest, baseline, candidate,
            manifest_sha, signed[PREFIX + "producers/preserve_134.py"], sha(blob("evidence-inventory.json")))
        require(len(runtime_entries(manifest)) == payload["verifiedRuntimeEntries"]
                and len(runtime_entries(baseline)) == payload["baselineRuntimeEntries"],
                "Payload proof full-runtime scope differs")
        bytes_raw = capture("committed-bytes/committed-bytes-001.json", SCRATCH / "committed-bytes-001.json")
        bytes_memory = json.loads(capture("committed-bytes/committed-bytes-memory-001.json",
                                          SCRATCH / "committed-bytes-memory-001.json"))
        bytes_producer = capture("committed-bytes/verify_committed_bytes_134.py",
                                 SCRATCH / "verify_committed_bytes_134.py")
        require(sha(bytes_raw) == HANDOFF["committed-bytes-001.json"], "Handoff byte binding differs")
        committed_bytes = json.loads(bytes_raw)
        memory_ok(bytes_memory)
        paths = git("diff", "--name-only", "-z", BASE, candidate).decode().strip("\0").split("\0")
        require(committed_bytes["head"] == candidate and committed_bytes["base"] == BASE
                and committed_bytes["status"] == "PASS"
                and committed_bytes["producerSha256"] == sha(bytes_producer)
                and sorted(committed_bytes["paths"]) == sorted(paths) and len(paths) == len(set(paths)),
                "Committed-byte receipt scope differs")
        for path in paths:
            guard.check()
            raw = git("show", candidate + ":" + path)
            require(committed_bytes["paths"][path] == sha(raw) and (REPO / path).read_bytes() == raw,
                    "Committed bytes differ: " + path)
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    bindings = {name: write_frozen(output / name, raw) for name, raw in captured.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 134, "status": "PASS", "candidate": candidate, "base": BASE,
        "payloadProof": {"path": str(HERE / proof_name), "sha256": sha(proof_raw)},
        "handoff": HANDOFF, "signedInputs": signed, "capturedInputs": bindings, "gates": groups,
        "quizSafetyWarnings": quiz, "supplementalReadingKeys": extras, "observedLatentCollisions": latent,
        "preservation": {"directory": str(SCRATCH / PRESERVATION),
                         "summarySha256": sha(captured["preservation/summary.json"]), **preservation},
        "fullRuntime": {"baselineEntries": payload["baselineRuntimeEntries"],
                        "candidateEntries": payload["verifiedRuntimeEntries"],
                        "source": "Accepted payload proof plus direct non-files manifest-group equality."},
        "committedBytes": {"paths": len(paths), "recheckedAgainstWorktree": True,
                           "producer": "Local unsigned post-commit producer, captured and handoff-hash-bound."},
        "helpers": HELPERS, "memory": memory, "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "Actual serial command/receipt, bounded-launcher and signed-producer bindings; superseded "
                  "author run retained, not accepted; explicit reading keys; files-only preservation plus "
                  "payload-proof full runtime; independent committed-byte recheck. Reading inputs are "
                  "current local copies equal to signed bytes, not proof of run-time bytes. Latent "
                  "smaller-pool collision disclosed. Not independent linguistic, arbitrary-pool, "
                  "native/device, rendered or publication acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: verify_b134_gates.py PROOF SHA OUTPUT_DIR")
    main(*sys.argv[1:])
