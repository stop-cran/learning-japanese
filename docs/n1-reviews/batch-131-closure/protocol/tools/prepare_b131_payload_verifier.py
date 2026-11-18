"""Specialize the frozen payload verifier for B131's actual signed handoff."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-131" / "review"
frozen(TOOLS / "prepare_b131_source_verifier.py",
       "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5")
from prepare_b131_source_verifier import derive


def main():
    require(not (HERE / "payload-verifier-derivation-001.json").exists(), "Preserve derivation record")
    require(not (TOOLS / "verify_b131_payload.py").exists()
            and not (TOOLS / "test_verify_b131_payload.py").exists(), "Preserve derived tools")
    guard, _ = start_guard("B131 signed payload verifier preparation")
    try:
        verifier = derive(
            "verify_b130_payload.py",
            "f5d3791ae3b1ae301617ee90ab3625cb60aab9631724441200df22cca8ee2551",
            "verify_b131_payload.py", [
                ("b130", "b131"), ("B130", "B131"), ("batch-130", "batch-131"),
                ("scratch-130", "scratch-131"), ("Batch 130", "Batch 131"),
                ('"f237a8d590a4cb91029bc0b8485163933f44b403"',
                 '"cb0f5581bdda84f7e673225c19126c85e242e57b"'),
                ('MEMBERS = ["\\u5840", "\\u62cd", "\\u8017"]',
                 'MEMBERS = ["\\u885b", "\\u7f8a", "\\u971c"]'),
                ('SUPPORTS = {"\\u5840": ["\\u5840"], "\\u62cd": ["\\u62cd\\u624b"], "\\u8017": ["\\u6d88\\u8017"]}',
                 'SUPPORTS = {"\\u885b": ["\\u81ea\\u885b", "\\u885b\\u661f"], '
                 '"\\u7f8a": ["\\u7f8a\\u6bdb"], "\\u971c": ["\\u971c"]}'),
                ('"222518f71e16878a49dbff51ecaa94ee2d9f6f471b8d9a5fa4fb9bd4b6d0a22b"',
                 '"6efda73704e0ed665c540b5cba62d9de62613df5fc4c16ffe5ba52c834078e67"'),
                ('"f95c7bc6867cf08977e2ada07630564441790ad31a50141126fec8de3a7d8b84"',
                 '"da78564efadb90ac4c174dbf13e375327b611bc5e0fc77913c8b85c22c1aaf6b"'),
                ('proof["batch"] == 130', 'proof["batch"] == 131'),
                ('"batch": 130', '"batch": 131'),
                ("len(previous) == 8724 and len(current) == 8730",
                 "len(previous) == 8731 and len(current) == 8737"),
                ('binding["file"] == svg_name', 'binding["path"] == svg_name'),
            ])
        tests = derive(
            "test_verify_b130_payload.py",
            "dd5f9705cf16e00c7808b5f359baff2b35e2201c1fadf0514f07dd78b005951d",
            "test_verify_b131_payload.py", [("verify_b130_payload", "verify_b131_payload")])
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(HERE / "payload-verifier-derivation-001.json", {
        "batch": 131, "status": "PREPARATION_ONLY", "verifier": verifier, "tests": tests,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "memory": memory,
        "limits": "Specialization only; actual signed runtime, metadata, reciprocal wrapper and "
                  "stroke-converter verification must still execute.",
    })))


if __name__ == "__main__":
    main()
