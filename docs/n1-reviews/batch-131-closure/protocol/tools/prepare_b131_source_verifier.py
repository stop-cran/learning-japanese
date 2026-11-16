"""Derive B131 source admission with separate signed-candidate and scan bases."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-131" / "review"
VERIFIER_SHA = "222518f71e16878a49dbff51ecaa94ee2d9f6f471b8d9a5fa4fb9bd4b6d0a22b"
SCHEMA_SHA = "91df923ee8ed6750b079a7ef35d0231560591fa699df15c6274e9919b9260ffa"
TESTS_SHA = "97864fc825c657af14b683525d2d2a0b1943ba412de7fb4f90d9b4e06bfd787e"
BRIDGE_SHA = "76c11728caa881ede7179266fd7060e97bb861e773933d898ce331d46dcb8c2b"


def derive(source, expected, target, substitutions):
    raw = frozen(TOOLS / source, expected)
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8").replace("\r\n", "\n")
    require(text.replace("\n", newline).encode("utf-8") == raw, "Mixed predecessor line endings")
    changes = []
    for before, after in substitutions:
        count = text.count(before)
        require(count > 0 and after not in text, "Ambiguous substitution: " + before)
        text = text.replace(before, after)
        changes.append({"before": before, "after": after, "count": count})
    reverse = text
    for change in reversed(changes):
        require(reverse.count(change["after"]) == change["count"], "Reverse count differs")
        reverse = reverse.replace(change["after"], change["before"])
    require(reverse.replace("\n", newline).encode("utf-8") == raw, "Derivation is not byte-reversible")
    compile(text, str(TOOLS / target), "exec")
    return {
        "source": {"path": str(TOOLS / source), "sha256": expected},
        "output": write_frozen(TOOLS / target, text.replace("\n", newline).encode("utf-8")),
        "substitutions": changes, "reverseExact": True,
    }


def main():
    outputs = ("b131_source_schema.py", "test_b131_source_schema.py", "verify_b131_sources.py")
    require(all(not (TOOLS / name).exists() for name in outputs), "Preserve existing derived tools")
    require(not (HERE / "source-verifier-derivation-001.json").exists(), "Preserve derivation record")
    frozen(TOOLS / "b131_base_binding_v2.py", BRIDGE_SHA)
    guard, _ = start_guard("B131 dual-baseline source-verifier preparation")
    try:
        schema = derive("b130_source_schema.py", SCHEMA_SHA, outputs[0], [
            ("B130", "B131"), ('== 130', '== 131'),
        ])
        tests = derive("test_b130_source_schema.py", TESTS_SHA, outputs[1], [
            ("b130_source_schema", "b131_source_schema"), ("B130", "B131"), ("130", "131"),
        ])
        verifier = derive("verify_b130_sources.py", VERIFIER_SHA, outputs[2], [
            ("import b130_source_schema as schema",
             "import b131_source_schema as schema\nimport b131_base_binding_v2 as base_bridge"),
            (f'SCHEMA_SHA = "{SCHEMA_SHA}"',
             f'SCHEMA_SHA = "{schema["output"]["sha256"]}"\nBRIDGE_SHA = "{BRIDGE_SHA}"'),
            ('    frozen(Path(schema.__file__), SCHEMA_SHA)\n',
             '    frozen(Path(schema.__file__), SCHEMA_SHA)\n'
             '    frozen(Path(base_bridge.__file__), BRIDGE_SHA)\n'),
            ('facts["batch"] == 130', 'facts["batch"] == 131'),
            ("B130 verifier requires batch 130", "B131 verifier requires batch 131"),
            ('        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing trailer")\n',
             '        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing trailer")\n'
             '        base_binding = base_bridge.verify_signed_binding(git, candidate)\n'
             '        source_base = base_binding["sourceBase"]\n'
             '        require(base == base_binding["candidateBase"], "Candidate facts use the wrong adapted base")\n'),
            ('git("ls-tree", "-rz", base, "--", "kanji")',
             'git("ls-tree", "-rz", source_base, "--", "kanji")'),
            ('baseline = json.loads(blob("manifest.json", base))["files"]',
             'baseline = json.loads(blob("manifest.json", source_base))["files"]'),
            ('schema.verify_selection(selection, signed_rows, index, members, base)',
             'schema.verify_selection(selection, signed_rows, index, members, source_base)'),
            ('title, base, helper', 'title, source_base, helper'),
            ('"batch": facts["batch"], "candidate": candidate, "base": base, "status": "PASS",',
             '"batch": facts["batch"], "candidate": candidate, "base": base, "status": "PASS",\n'
             '        "sourceBase": source_base, "baseBinding": base_binding,\n'
             '        "baseBridgeVerifier": {"path": str(Path(base_bridge.__file__)), "sha256": BRIDGE_SHA},'),
            ("Usage: verify_b130_sources.py", "Usage: verify_b131_sources.py"),
        ])
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(HERE / "source-verifier-derivation-001.json", {
        "batch": 131, "status": "PREPARATION_ONLY",
        "schema": schema, "tests": tests, "verifier": verifier,
        "baseBridge": {"path": str(TOOLS / "b131_base_binding_v2.py"), "sha256": BRIDGE_SHA},
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "memory": memory,
        "limits": "Executable admission preparation, not candidate acceptance. The actual signed "
                  "handoff must supply source facts and pass complete-record and scan reproduction. "
                  "Signature, parent and candidate payload remain bound to cb0; original selection, "
                  "scan reproduction and baseline manifest remain bound to 6da through the exact-tree bridge.",
    })))


if __name__ == "__main__":
    main()
