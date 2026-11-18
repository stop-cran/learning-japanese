"""Derive B123 revision checks without changing frozen earlier-batch tools."""
import json
import os
import subprocess
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

TOOLS = Path(__file__).resolve().parent
REVIEW = WS / "scratch-123" / "review"


def replace_once(text, old, new):
    require(text.count(old) == 1, f"Expected one derivation anchor: {old!r}")
    return text.replace(old, new)


def main():
    source = TOOLS / "verify_b122_revision_v2.py"
    original = frozen(source)
    text = original.decode("utf-8").replace("B122", "B123")
    for old, new in (
        (r"\u60a0\u3005", r"\u7bc4\u56f2"),
        (r"\u60a0", r"\u7bc4"),
        (r"\u5e38\u7d9a", r"\u6a19\u7d00\u93e1\u69d8\u683c"),
        ("batch-122-reconciliation/", "batch-123/reconciliation-001/"),
        ("load_batch(122)", "load_batch(123)"),
        ("== 8706", "== 8708"),
        ("count(runtime(before)) == 251 and count(current) == 252",
         "count(runtime(before)) == 252 and count(current) == 253"),
        ('"batch": 122', '"batch": 123'),
        ('"sourceMembersPublishedBeforeBatch": 251, "sourceMembersInCandidate": 252',
         '"sourceMembersPublishedBeforeBatch": 252, "sourceMembersInCandidate": 253'),
    ):
        require(old in text, f"Missing derivation value: {old}")
        text = text.replace(old, new)
    text = replace_once(text, "from common import CHECKS, WS,",
                        "from common import CHECKS, GUARD_SHA, WS,")
    start = text.index("def check_gate(")
    end = text.index("\ndef verify_sources(", start)
    text = text[:start] + '''def check_gate(receipt, log, name, manifest_sha, repo, runner_sha):
    memory = receipt["memory"]
    require(receipt["gate"] == name and receipt["exitCode"] == 0
            and receipt["childExitCodeAfterCleanup"] == 0
            and receipt["cwd"] == repo and receipt["logSha256"] == sha(log)
            and receipt["logBytes"] == len(log)
            and receipt["runnerSha256"] == runner_sha
            and receipt["guardSha256"] == GUARD_SHA
            and 0 < receipt["waitTimeoutSeconds"] <= 0.1
            and not memory["breach"] and memory["freeRamBeforeBytes"] > 2 * 1024**3
            and memory["minimumObservedFreeRamBytes"] >= 1024**3
            and memory["abortThresholdBytes"] == 1024**3
            and memory["samplingIntervalSeconds"] == 0.25,
            f"Failed, weakened or changed gate: {name}")
    if name in ("manifest", "manifest-rebuild"):
        require(receipt["manifestSha256"] == manifest_sha, "Gate manifest differs")
    if name == "manifest-rebuild":
        require(receipt["manifestReproducible"] is True, "Manifest rebuild differs")
    if name == "reading-exposure":
        require(all(value.encode("utf-8") in log for value in
                    ("\\\\u7bc4", "\\\\u30cf\\\\u30f3", "\\\\u306e\\\\u308a", "\\\\u3059\\\\u3059\\\\u3080")),
                "Target or supplemental readings missing from exposure evidence")

''' + text[end:]
    start = text.index("def check_summary(")
    end = text.index("\ndef verify(", start)
    text = text[:start] + '''def check_summary(summary, config, candidate, manifest_sha, runner_sha):
    require(str(summary["batch"]) == "123"
            and summary["status"] == "PASS" and summary["mode"] == "committed"
            and summary["base"] == config["base"] and summary["startingHead"] == candidate
            and set(summary["checks"]) == set(CHECKS) and len(summary["checks"]) == len(CHECKS)
            and summary["manifestSha256"] == manifest_sha
            and summary["runnerSha256"] == runner_sha,
            "Gate summary is not for the exact committed revision")
    if "parent" in summary:
        require(summary["parent"] == config["candidate"], "Summary parent differs")
    if "manifestReproducible" in summary:
        require(summary["manifestReproducible"] is True, "Summary rebuild differs")

''' + text[end:]
    text = replace_once(text, "def verify(candidate, gates, output):",
                        "def verify(candidate, gates, runner, output):")
    text = replace_once(text, '    config = load_batch(123)\n',
                        '    config = load_batch(123)\n    runner_sha = sha(frozen(runner))\n')
    text = replace_once(text,
                        "check_summary(summary, config, candidate, sha(raw_manifest))",
                        "check_summary(summary, config, candidate, sha(raw_manifest), runner_sha)")
    text = replace_once(text,
                        'check_gate(json.loads(raw), log, name, sha(raw_manifest), config["repo"])',
                        'check_gate(json.loads(raw), log, name, sha(raw_manifest), config["repo"], runner_sha)')
    text = replace_once(text,
                        '"base": config["base"], "manifestSha256": sha(raw_manifest),',
                        '"base": config["base"], "manifestSha256": sha(raw_manifest),\n'
                        '            "runner": {"path": str(runner), "sha256": runner_sha},')
    text = replace_once(text,
                        'verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))',
                        'verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))')
    compile(text, "verify_b123_revision.py", "exec")
    verifier = write_frozen(TOOLS / "verify_b123_revision.py", text.encode("utf-8"))

    test_source = TOOLS / "test_verify_b122_revision.py"
    test_raw = frozen(test_source)
    tests = test_raw.decode("utf-8").replace("verify_b122_revision", "verify_b123_revision")
    tests = tests.replace(r"\u30e6\u30a6", r"\u30cf\u30f3")
    tests = tests.replace(r"\u5e38\u7d9a", r"\u6a19\u7d00\u93e1\u69d8\u683c")
    tests = tests.replace('"manifest", "repo")', '"manifest", "repo", "runner")')
    tests = replace_once(
        tests, '"manifestSha256": "manifest", "manifestReproducible": True,',
        '"manifestSha256": "manifest", "manifestReproducible": True,\n'
        '            "childExitCodeAfterCleanup": 0, "waitTimeoutSeconds": 0.1,\n'
        '            "runnerSha256": "runner", "guardSha256": GUARD_SHA, "logBytes": len(log),')
    tests = tests.replace("import unittest\n", "import unittest\n\nfrom common import GUARD_SHA\n")
    tests = tests.replace('("minimumObservedFreeRamBytes", 1024**3)',
                          '("minimumObservedFreeRamBytes", 1024**3 - 1)')
    inherited = write_frozen(TOOLS / "test_verify_b123_revision_sources.py", tests.encode("utf-8"))
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
    command = [sys.executable, "-B", "-m", "unittest", "-q",
               "test_verify_b123_revision_sources", "test_verify_b123_revision"]
    run = subprocess.run(command, cwd=TOOLS, env=env, capture_output=True)
    log = write_frozen(REVIEW / "b123-revision-tool-tests.log", run.stdout + run.stderr)
    require(run.returncode == 0, (run.stdout + run.stderr).decode("utf-8"))
    proof = freeze_json(REVIEW / "b123-revision-tooling.json", {
        "batch": 123, "status": "PASS",
        "sources": [{"path": str(source), "sha256": sha(original)},
                    {"path": str(test_source), "sha256": sha(test_raw)}],
        "derived": [verifier, inherited],
        "additionalTests": {"path": str(TOOLS / "test_verify_b123_revision.py"),
                            "sha256": sha((TOOLS / "test_verify_b123_revision.py").read_bytes())},
        "producer": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
        "command": command, "testLog": log,
        "limits": "Tooling preparation only. No candidate execution, source-selection or linguistic "
                  "acceptance. Actual author schema and runner must be read before revision verification.",
    })
    print(json.dumps(proof))


if __name__ == "__main__":
    main()
