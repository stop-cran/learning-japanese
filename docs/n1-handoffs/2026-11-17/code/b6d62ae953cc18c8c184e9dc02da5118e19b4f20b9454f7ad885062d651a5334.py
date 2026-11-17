"""Adapt the prepared finalizer to the author's minimal source-binding receipt."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).resolve().parent
original = frozen(HERE / "finalize_b119_v2.py",
                  "e60eaca268b1e6b21ed41448ee53bdcae65786d9b451920b0bdb7e46b03b4587")
changes = [
    ('"pair-dispositions.json", "source-extraction.json", "changed-file-inventory.json"',
     '"pair-dispositions.json", "source-bindings.json" if number == 3 else "source-extraction.json",\n'
     '                         "changed-file-inventory.json"'),
    ('"reconciliation": "batch-119/reconciliation-003/source-extraction.json"',
     '"reconciliation": "batch-119/reconciliation-003/source-bindings.json"'),
    ('"test_finalize_b119_v2.py", "record_publication.py"',
     '"test_finalize_b119_v2.py", "finalize_b119_v3.py", "test_finalize_b119_v3.py",\n'
     '                     "derive_b119_finalizer_v3.py", "prepare_b119_followup.py", "record_publication.py"'),
    ('        artifacts = {"revision-verification-003.json": frozen(proof_path),',
     '        source_proof_path = records / "revision-source-verification-003.json"\n'
     '        source_raw = frozen(source_proof_path,\n'
     '            "17cf4426a58c8a18a8803db4da7661a4c68886f9b0952a51639247535566f322")\n'
     '        source_proof = json.loads(source_raw)\n'
     '        require(source_proof["candidate"] == candidate and source_proof["status"] == "PASS"\n'
     '                and not source_proof["memory"]["breach"], "Pair-source proof differs")\n'
     '        artifacts = {"revision-source-verification-003.json": source_raw,\n'
     '                     "revision-verification-003.json": frozen(proof_path),'),
]
updated = original.decode("utf-8")
for before, after in changes:
    require(updated.count(before) == 1, f"Derivation anchor changed: {before}")
    updated = updated.replace(before, after, 1)
reversed_text = updated
for before, after in reversed(changes):
    require(reversed_text.count(after) == 1, "Reverse anchor changed")
    reversed_text = reversed_text.replace(after, before, 1)
require(reversed_text.encode() == original, "Derivation does not reverse exactly")
compile(updated, "finalize_b119_v3.py", "exec")
result = write_frozen(HERE / "finalize_b119_v3.py", updated.encode("utf-8"))
test = frozen(HERE / "test_finalize_b119_v2.py",
              "34509b61acc6f4f7773d0afd4e999143815f046e23597122f444af19aba10e2c")
require(test.count(b"from finalize_b119_v2 import") == 1, "Test anchor changed")
test_result = write_frozen(HERE / "test_finalize_b119_v3.py",
                          test.replace(b"from finalize_b119_v2 import", b"from finalize_b119_v3 import"))
runner_path = WS / "scratch-119" / "run-checks-closure-001.py"
runner = frozen(runner_path, "e4062b8be5d032e6fbed5f80f8f40d2807875a27ac69fcca6307d6701ae89ea6")
old, new = b"14662814559b9cb969bcb5768643748758cefffe", b"a399197c5d7eeec60263ad33de57b436fa25709e"
require(runner.count(old) == 1, "Closure runner snapshot anchor changed")
runner_result = write_frozen(runner_path.with_name("run-checks-closure-002.py"), runner.replace(old, new))
print(json.dumps(freeze_json(HERE / "b119-finalizer-v3-derivation.json", {
    "sourceSha256": sha(original), "output": result, "test": test_result,
    "closureRunner": runner_result, "reverseExact": True,
    "changes": "Use the actual minimal source-bindings filename, preserve source verification "
               "and include the finalizer/follow-up protocol tools. No acceptance condition removed.",
})))
