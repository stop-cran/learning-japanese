"""Verify B132's actual serial gates and preservation against its signed payload."""
import ast
import json
import re
import sys
from pathlib import Path

from common import GUARD_SHA, WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
HELPERS = {
    "verify_b132_payload_v2.py": "af5091da5140b08e12dd1dd182f3a5db512751e808ed522f3a757d065cb6ecff",
    "verify_b130_evidence_v3.py": "23228af0051d8e87a5ce1864671c668587c1554591cee6a841cb8a2ea303737f",
    "verify_b131_gate_evidence_v2.py": "d020a08e2a97b54ac54284f854d116a8751ffa314f6124788b10a673bb1b7411",
}
for name, digest in HELPERS.items():
    frozen(TOOLS / name, digest)

from verify_b132_payload_v2 import (
    BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, LINK_HELPER, LINK_HELPER_SHA, runtime_entries)
from verify_b132_sources import Git
from verify_b130_evidence_v3 import ORDER, verify_execution
from verify_b131_gate_evidence_v2 import memory_ok

SCRATCH = HERE.parent


def commands():
    lean = WS / "lean"
    return {
        "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", *MEMBERS],
        "quiz-safety": [lean / "quiz_safety.py", *MEMBERS],
        "linkplan": [lean / "n1_linkplan.py", "verify", BASE, *MEMBERS],
        "reading-exposure": [SCRATCH / "check_reading_132.py"],
        "validate": [REPO / "tools" / "validate.py"],
        "manifest": [REPO / "tools" / "build_manifest.py"],
        "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
        "budget": [REPO / "tools" / "check_content_budget.py"],
        "vocabulary": [REPO / "tools" / "grammar_vocabulary.py", "check"],
        "manifest-rebuild": [REPO / "tools" / "build_manifest.py"],
    }


def verify_summary(summary, admission, mode, candidate, manifest_sha, runner_sha, common_sha):
    head = BASE if mode == "author" else candidate
    require(admission["base"] == BASE and admission["head"] == head and admission["mode"] == mode,
            "Gate admission binds another snapshot")
    memory_ok(admission["memory"])
    require(type(summary["batch"]) is int and summary["batch"] == 132
            and summary["mode"] == mode and summary["status"] == "PASS"
            and summary["base"] == BASE and summary["startingHead"] == head
            and summary["checks"] == list(ORDER) and summary["serial"] is True
            and summary["manifestSha256"] == manifest_sha
            and summary["runnerSha256"] == runner_sha and summary["commonHelperSha256"] == common_sha
            and summary["guardSha256"] == GUARD_SHA and summary["waitTimeoutSeconds"] == 0.1
            and summary["cleanupTimeoutSecondsPerStage"] == 10, "Gate summary differs")
    memory_ok(summary["finalMemory"])


def verify_reading_output(log, extras):
    lines = [line.split(": ", 1)[1] for line in log.splitlines()
             if line.startswith("Explicit supplemental reading keys: ")]
    production = re.findall(r"(\d+) production hit\(s\)", log)
    padded = re.findall(r"(\d+) padded-session hit\(s\)", log)
    latent = re.findall(r"(\d+) latent collision\(s\)", log)
    require(len(lines) == 1 and json.loads(lines[0]) == extras
            and production == padded == ["0"]
            and len(latent) == 1, "Explicit reading keys or bounded pool result differ")
    return int(latent[0])


def main(proof_name, proof_sha, author_name, committed_name, preservation_name, output_name):
    for name in (proof_name, author_name, committed_name, preservation_name, output_name):
        require(Path(name).name == name and name not in {"", ".", ".."}, "Direct path names required")
    require(len({author_name, committed_name, preservation_name, output_name}) == 4,
            "Input and output directory names must differ")
    output = HERE / output_name
    require(not output.exists(), "Preserve gate-verification output")
    proof_raw = frozen(HERE / proof_name, proof_sha)
    payload = json.loads(proof_raw)
    require(payload["batch"] == 132 and payload["base"] == BASE and payload["status"] == "PASS"
            and payload["verifierSha256"] == HELPERS["verify_b132_payload_v2.py"]
            and not payload["memory"]["breach"], "Wrong accepted payload proof")
    candidate, manifest_sha = payload["candidate"], payload["manifestSha256"]
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b132_gate_bindings", LINK_HELPER)
    guard, _ = start_guard("B132 committed gate and preservation evidence")
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
        for name in ("common_132.py", "run_132_gates.py", "check_reading_132.py", "preserve_132.py"):
            require((SCRATCH / name).read_bytes() == blob("producers/" + name),
                    "Executed producer differs from signed bytes: " + name)
        common_sha = signed[PREFIX + "producers/common_132.py"]
        runner_sha = signed[PREFIX + "producers/run_132_gates.py"]
        for group, directory_name in (("author", author_name),
                                      ("author-recheck", "author-gates-002"),
                                      ("committed", committed_name)):
            mode = "committed" if group == "committed" else "author"
            directory = SCRATCH / directory_name
            admission_raw = capture(group + "/admission.json", directory / "admission.json")
            summary_raw = capture(group + "/summary.json", directory / "summary.json")
            admission, summary = json.loads(admission_raw), json.loads(summary_raw)
            verify_summary(summary, admission, mode, candidate, manifest_sha, runner_sha, common_sha)
            bindings = helper.gate_bindings(directory, {"repo": str(REPO)}, manifest_sha, runner_sha, guard)
            receipts = {}
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
            verify_execution(receipts, commands(), common_sha)
            require(summary["logs"] == {r["gate"]: {key: r[key] for key in ("receiptSha256", "logSha256")}
                                        for r in bindings}, "Gate summary inventory differs")
            if group == "author":
                for name, raw in (("admission.json", admission_raw), ("summary.json", summary_raw)):
                    require(raw == blob(f"author-evidence/{directory_name}/{name}"),
                            "Signed author admission or summary differs")
            groups[group] = {"directory": str(directory), "summarySha256": sha(summary_raw),
                             "gates": bindings, "acceptedRun": True,
                             "signedCopy": group == "author"}
        extras = json.loads(blob("reading-keys.json"))["testedKeys"]
        reading_source = blob("producers/check_reading_132.py")
        expected = ast.parse(
            'extras = json.loads((PACKET / "reading-keys.json").read_text(encoding="utf-8"))["testedKeys"]'
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
                and preservation["producerSha256"] == signed[PREFIX + "producers/preserve_132.py"]
                and preservation["memory"] == json.loads(captured["preservation/memory.json"]),
                "Committed preservation binding differs")
        memory_ok(preservation["memory"])
        manifest_raw = git("show", candidate + ":manifest.json")
        require(sha(manifest_raw) == manifest_sha, "Signed manifest changed")
        runtime = {name: digest for name, (digest, _) in runtime_entries(json.loads(manifest_raw)).items()}
        require(json.loads(captured["preservation/runtime-hashes.json"]) == runtime
                and preservation["allCandidateRuntimeHashesChecked"] == len(runtime),
                "Preservation omits or changes actual runtime hashes")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    bindings = {name: write_frozen(output / name, raw) for name, raw in captured.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 132, "status": "PASS", "candidate": candidate, "base": BASE,
        "payloadProof": {"path": str(HERE / proof_name), "sha256": sha(proof_raw)},
        "signedInputs": signed, "capturedInputs": bindings, "gates": groups,
        "supplementalReadingKeys": extras, "observedLatentCollisions": latent,
        "preservation": {"directory": str(SCRATCH / preservation_name),
                         "summarySha256": sha(captured["preservation/summary.json"])},
        "helpers": HELPERS, "memory": memory, "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "Actual serial command/receipt and signed-producer bindings; explicit reading "
                  "keys and complete runtime preservation. Latent smaller-pool collisions are "
                  "disclosed, not erased by bounded production/padded passes. No independent "
                  "linguistic, arbitrary-pool, native/device, rendered or publication acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 7, "Usage: verify_b132_gates.py PROOF SHA AUTHOR_DIR COMMITTED_DIR PRESERVATION_DIR OUTPUT_DIR")
    main(*sys.argv[1:])
