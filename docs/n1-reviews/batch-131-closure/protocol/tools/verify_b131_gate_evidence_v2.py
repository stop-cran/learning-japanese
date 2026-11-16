"""Bind the actual B131 serial gate runs and preservation receipts to its signed tree."""
import ast
import json
import sys
from pathlib import Path

from common import GUARD_SHA, WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen
from prepare_b131_source_facts import CANDIDATE, CANDIDATE_BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER
from verify_b131_payload import LINK_HELPER, LINK_HELPER_SHA, runtime_entries
from verify_b131_sources import Git

SCRATCH = HERE.parent
HANDOFF_SHA = "082957e626558f66bbddb0f4d5bee1d1e8b25a91eb811414c73e817001b8db62"
PAYLOAD_SHA = "dc3f1068362350bd81fdc8ec94e20b32589b0fdcdb25248a911e4817ffb068d6"
EVIDENCE_HELPER_SHA = "23228af0051d8e87a5ce1864671c668587c1554591cee6a841cb8a2ea303737f"
ORDER = ("lint", "quiz-safety", "linkplan", "reading-exposure", "validate",
         "manifest", "unittest", "budget", "vocabulary", "manifest-rebuild")


def memory_ok(record):
    require(not record["breach"] and record["freeRamBeforeBytes"] > 2 * 1024**3
            and record["minimumObservedFreeRamBytes"] >= 1024**3
            and record["abortThresholdBytes"] == 1024**3 and record["samplingIntervalSeconds"] == 0.25,
            "Execution memory contract differs")


def commands():
    lean = WS / "lean"
    return {
        "lint": [lean / "n1_batch_tool.py", "lint", "--base", CANDIDATE_BASE, "--no-jmdict", *MEMBERS],
        "quiz-safety": [lean / "quiz_safety.py", *MEMBERS],
        "linkplan": [lean / "n1_linkplan.py", "verify", CANDIDATE_BASE, *MEMBERS],
        "reading-exposure": [SCRATCH / "check_reading_b131.py"],
        "validate": [REPO / "tools" / "validate.py"], "manifest": [REPO / "tools" / "build_manifest.py"],
        "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
        "budget": [REPO / "tools" / "check_content_budget.py"],
        "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
        "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
    }


def main():
    output = HERE / "gate-verification-002"
    require(not output.exists(), "Preserve gate-verification output")
    handoff_raw = frozen(HERE / "author-handoff-observed-001.json", HANDOFF_SHA)
    handoff = json.loads(handoff_raw)
    payload = json.loads(frozen(HERE / "payload-verification-001.json", PAYLOAD_SHA))
    require(handoff["candidate"] == payload["candidate"] == CANDIDATE
            and payload["base"] == handoff["base"] == CANDIDATE_BASE and payload["status"] == "PASS",
            "Handoff and verified payload differ")
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b131_gate_bindings", LINK_HELPER)
    evidence_path = Path(__file__).with_name("verify_b130_evidence_v3.py")
    frozen(evidence_path, EVIDENCE_HELPER_SHA)
    evidence = load_module("b131_serial_execution", evidence_path)
    guard, _ = start_guard("B131 committed gate and preservation evidence")
    git = Git(REPO, RUNNER, guard)
    captured, signed, groups = {}, {}, {}

    def blob(name):
        raw = git("show", CANDIDATE + ":" + PREFIX + name)
        signed[PREFIX + name] = sha(raw)
        return raw

    def capture(name, path):
        raw = path.read_bytes()
        captured[name] = raw
        return raw

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout differs")

    try:
        clean()
        for name in ("b131_common.py", "candidate_b131.py", "run_b131_gates.py", "check_reading_b131.py",
                     "preserve_b131.py", "preserve_b131_002.py"):
            require((SCRATCH / name).read_bytes() == blob("producers/" + name),
                    "Executed producer differs from signed bytes: " + name)
        common_sha = signed[PREFIX + "producers/b131_common.py"]
        runner_sha = signed[PREFIX + "producers/run_b131_gates.py"]
        constants_sha = signed[PREFIX + "producers/candidate_b131.py"]
        manifest_sha = payload["manifestSha256"]
        for mode, directory_name, signed_copy in (
            ("author", "author-gates-003", "author-evidence/author-gates-003"),
            ("committed", "committed-gates-002", None),
            ("incomplete", "committed-gates-001", None),
        ):
            directory = SCRATCH / directory_name
            admission = json.loads(capture(mode + "/admission.json", directory / "admission.json"))
            require(admission["base"] == CANDIDATE_BASE
                    and admission["head"] == (CANDIDATE_BASE if mode == "author" else CANDIDATE)
                    and admission["mode"] == ("author" if mode == "author" else "committed"),
                    "Gate admission binds the wrong snapshot")
            memory_ok(admission["memory"])
            bindings = helper.gate_bindings(directory, {"repo": str(REPO)}, manifest_sha, runner_sha, guard)
            receipts = {}
            for record in bindings:
                gate = record["gate"]
                for suffix, key in (("json", "receiptSha256"), ("log", "logSha256")):
                    name = f"{gate}.{suffix}"
                    raw = capture(mode + "/" + name, directory / name)
                    require(sha(raw) == record[key], "Gate bytes changed during verification")
                    if signed_copy:
                        require(raw == blob(signed_copy + "/" + name), "Signed author gate copy differs")
                receipt = json.loads(captured[mode + f"/{gate}.json"])
                require(receipt["base"] == CANDIDATE_BASE
                        and receipt["candidateConstantsSha256"] == constants_sha,
                        "Gate receipt base/constants differ")
                receipts[gate] = receipt
            evidence.verify_execution(receipts, commands(), common_sha)
            if mode == "incomplete":
                require(not (directory / "summary.json").exists(), "Incomplete predecessor gained a summary")
                groups[mode] = {"directory": str(directory), "gates": bindings, "acceptedRun": False,
                                "qualification": "Ten successful commands and missing summary verified. "
                                "Author reports final fresh RAM admission failure; that instant was not independently witnessed."}
                continue
            summary_raw = capture(mode + "/summary.json", directory / "summary.json")
            summary = json.loads(summary_raw)
            require(summary["batch"] == "131" and summary["mode"] == mode and summary["status"] == "PASS"
                    and summary["base"] == CANDIDATE_BASE and summary["startingHead"] == admission["head"]
                    and summary["checks"] == list(ORDER) and summary["serial"] is True
                    and summary["manifestSha256"] == manifest_sha and summary["runnerSha256"] == runner_sha
                    and summary["commonHelperSha256"] == common_sha
                    and summary["candidateConstantsSha256"] == constants_sha
                    and summary["guardSha256"] == GUARD_SHA and summary["waitTimeoutSeconds"] == 0.1
                    and summary["cleanupTimeoutSecondsPerStage"] == 10, "Gate summary differs")
            memory_ok(summary["finalMemory"])
            require(summary["logs"] == {r["gate"]: {k: r[k] for k in ("receiptSha256", "logSha256")}
                                       for r in bindings}, "Gate summary log inventory differs")
            if signed_copy:
                require(summary_raw == blob(signed_copy + "/summary.json"), "Signed summary differs")
            else:
                require(sha(summary_raw) == handoff["committedGates"]["summarySha256"],
                        "Committed gate summary differs from handoff")
            groups[mode] = {"directory": str(directory), "summarySha256": sha(summary_raw),
                            "gates": bindings, "acceptedRun": True}
        reading_raw = blob("reading-keys.json")
        extras = json.loads(reading_raw)["testedKeys"]
        source = blob("producers/check_reading_b131.py")
        expected = ast.parse(
            'extras = json.loads((PACKET / "reading-keys.json").read_text(encoding="utf8"))["testedKeys"]'
        ).body[0].value
        values = [node.value for node in ast.parse(source).body if isinstance(node, ast.Assign)
                  and any(isinstance(target, ast.Name) and target.id == "extras" for target in node.targets)]
        require(len(values) == 1 and ast.dump(values[0]) == ast.dump(expected),
                "Reading producer does not consume the signed key map")
        log = captured["committed/reading-exposure.log"].decode("utf-8")
        lines = [line.split(": ", 1)[1] for line in log.splitlines()
                 if line.startswith("Explicit supplemental reading keys: ")]
        require(len(lines) == 1 and json.loads(lines[0]) == extras
                and "0 production hit(s)" in log and "0 padded-session hit(s)" in log
                and "6 latent collision(s)" in log, "Reading result or explicit keys differ")
        preservation_dir = SCRATCH / "committed-preservation-001"
        for name in ("summary.json", "memory.json", "runtime-hashes.json"):
            capture("preservation/" + name, preservation_dir / name)
        preservation = json.loads(captured["preservation/summary.json"])
        require(sha(captured["preservation/summary.json"]) == handoff["preservation"]["summarySha256"]
                and sha(captured["preservation/runtime-hashes.json"]) == handoff["preservation"]["runtimeHashesSha256"]
                and preservation["status"] == "PASS" and preservation["head"] == CANDIDATE
                and preservation["base"] == CANDIDATE_BASE and preservation["clean"] is True
                and preservation["manifestSha256"] == manifest_sha
                and preservation["producerSha256"] == signed[PREFIX + "producers/preserve_b131_002.py"],
                "Preservation handoff binding differs")
        memory_ok(preservation["memory"])
        manifest = json.loads(git("show", CANDIDATE + ":manifest.json"))
        require(json.loads(captured["preservation/runtime-hashes.json"])
                == {name: digest for name, (digest, _) in runtime_entries(manifest).items()},
                "Preservation does not enumerate every verified runtime hash")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    captured_inputs = {name: write_frozen(output / name, raw) for name, raw in captured.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 131, "status": "PASS", "candidate": CANDIDATE, "base": CANDIDATE_BASE,
        "handoffSha256": HANDOFF_SHA, "payloadProofSha256": PAYLOAD_SHA, "signedInputs": signed,
        "capturedInputs": captured_inputs, "gates": groups, "supplementalReadingKeys": extras,
        "memory": memory, "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "Actual serial command/receipt and signed-producer binding, including explicit "
                  "reading keys and the incomplete predecessor. Not linguistic, arbitrary-pool, "
                  "rendered/native/device, independent-review or publication acceptance.",
    })))


if __name__ == "__main__":
    main()
