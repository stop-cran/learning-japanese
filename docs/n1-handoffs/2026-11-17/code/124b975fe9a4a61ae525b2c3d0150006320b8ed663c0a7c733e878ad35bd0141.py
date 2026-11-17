"""Prepare B132 payload checks for the reported single-member scope."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-132" / "review"
frozen(TOOLS / "prepare_b131_source_verifier.py",
       "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5")
from prepare_b131_source_verifier import derive


def main():
    outputs = ("verify_b132_payload.py", "test_verify_b132_payload.py")
    require(all(not (TOOLS / name).exists() for name in outputs),
            "Preserve existing derived tools")
    require(not (HERE / "payload-verifier-derivation-001.json").exists(),
            "Preserve existing derivation")
    frozen(TOOLS / "verify_b132_sources.py",
           "43ee9a6ceaf4ae023d4c9739b0a5276bdfd0c9c8573b410f99c5c06970dfe861")
    frozen(HERE / "guarded-test-v3.py",
           "56eb7d1c12a9278e589d8adcf57652288934345dd80740e1b92fc9cffdbd0eeb")
    guard, _ = start_guard("B132 signed payload verifier preparation")
    try:
        verifier = derive(
            "verify_b131_payload.py",
            "0b225ae7ee2d0682b66fefae70e4cf4928914e676747ea73b76ca35d47abb678",
            outputs[0], [
                ("b131", "b132"), ("B131", "B132"), ("batch-131", "batch-132"),
                ("scratch-131", "scratch-132"), ("Batch 131", "Batch 132"),
                ('"cb0f5581bdda84f7e673225c19126c85e242e57b"',
                 '"2375ab9add0cc5d569c8ea35d229b82813fd8557"'),
                ('MEMBERS = ["\\u885b", "\\u7f8a", "\\u971c"]',
                 'MEMBERS = ["\\u5893"]'),
                ('SUPPORTS = {"\\u885b": ["\\u81ea\\u885b", "\\u885b\\u661f"], '
                 '"\\u7f8a": ["\\u7f8a\\u6bdb"], "\\u971c": ["\\u971c"]}',
                 'SUPPORTS = {"\\u5893": ["\\u5893"]}'),
                ('"6efda73704e0ed665c540b5cba62d9de62613df5fc4c16ffe5ba52c834078e67"',
                 '"43ee9a6ceaf4ae023d4c9739b0a5276bdfd0c9c8573b410f99c5c06970dfe861"'),
                ('"da78564efadb90ac4c174dbf13e375327b611bc5e0fc77913c8b85c22c1aaf6b"',
                 '"56eb7d1c12a9278e589d8adcf57652288934345dd80740e1b92fc9cffdbd0eeb"'),
                ('proof["batch"] == 131', 'proof["batch"] == 132'),
                ('"batch": 131', '"batch": 132'),
                ("len(previous) == 8731 and len(current) == 8737",
                 "len(previous) == 8737 and len(current) == 8739"),
            ])
        tests = derive(
            "test_verify_b131_payload.py",
            "9cd43e7a92ccfc418d1d7651494aca905503ca9b467e8270f8696886b377c3ff",
            outputs[1], [("verify_b131_payload", "verify_b132_payload")])
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(HERE / "payload-verifier-derivation-001.json", {
        "batch": 132, "status": "PREPARATION_ONLY",
        "verifier": verifier, "tests": tests,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "memory": memory,
        "scope": "Reported single-member selection with one existing support article. "
                 "The actual signed source proof and complete declared-support scan must agree.",
        "limits": "No candidate is supplied or accepted by preparation. This preserves the "
                  "prior verifier's owner-signature, runtime-preservation, complete metadata, "
                  "reciprocal-wrapper and stroke-converter checks. Candidate execution, source "
                  "coverage, gate evidence, independent reviews and publication remain pending.",
    })))


if __name__ == "__main__":
    main()
