"""Derive B130's signed-payload checks from the frozen B129 implementation."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-130" / "review"
SOURCE_SHA = "e1c364c7b2652eeb9e71ca6006fd9eb3fb74531d60ae432375ea0051635281a6"
TEST_SHA = "07deec8dde24363d77591bdcedaed3a11d89bf8f1abaa1d943b67cca2fd1200d"


def derive(raw, changes):
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8").replace("\r\n", "\n")
    require(text.replace("\n", newline).encode("utf-8") == raw, "Mixed source line endings")
    substitutions = []
    for before, after in changes:
        count = text.count(before)
        require(count > 0 and after not in text, f"Ambiguous substitution: {before}")
        text = text.replace(before, after)
        substitutions.append({"before": before, "after": after, "count": count})
    reverse = text
    for change in reversed(substitutions):
        require(reverse.count(change["after"]) == change["count"], "Reverse count differs")
        reverse = reverse.replace(change["after"], change["before"])
    require(reverse.replace("\n", newline).encode("utf-8") == raw, "Derivation is not byte-reversible")
    return text.replace("\n", newline).encode("utf-8"), substitutions


def main():
    source_path = TOOLS / "verify_b129_payload.py"
    test_path = TOOLS / "test_verify_b129_payload.py"
    raw, test_raw = frozen(source_path, SOURCE_SHA), frozen(test_path, TEST_SHA)
    source_verifier_sha = sha(frozen(TOOLS / "verify_b130_sources.py",
                                    "222518f71e16878a49dbff51ecaa94ee2d9f6f471b8d9a5fa4fb9bd4b6d0a22b"))
    runner_sha = sha(frozen(HERE / "guarded-test-v3.py",
                            "f95c7bc6867cf08977e2ada07630564441790ad31a50141126fec8de3a7d8b84"))
    changes = [
        ("b129", "b130"), ("B129", "B130"), ("batch-129", "batch-130"),
        ("scratch-129", "scratch-130"), ("Batch 129", "Batch 130"),
        ('"20fda42f7b456889ae4ef82650dde227a139917c"',
         '"f237a8d590a4cb91029bc0b8485163933f44b403"'),
        ('MEMBERS = ["\\u8309", "\\u7d79", "\\u8679"]',
         'MEMBERS = ["\\u5840", "\\u62cd", "\\u8017"]'),
        ('SUPPORTS = {"\\u8309": ["\\u8309\\u8389\\u82b1"], "\\u7d79": ["\\u7d79"], "\\u8679": ["\\u8679"]}',
         'SUPPORTS = {"\\u5840": ["\\u5840"], "\\u62cd": ["\\u62cd\\u624b"], "\\u8017": ["\\u6d88\\u8017"]}'),
        ('"9fb0aa1b179679638865582eed251f2c4fd4c9a84707f56099383808b18d0b33"',
         f'"{source_verifier_sha}"'),
        ('"9326cabd53fb1ac18417dcc1f39d4316af8f1b0a945bf7523a9e73a7044a6848"',
         f'"{runner_sha}"'),
        ('proof["batch"] == 129', 'proof["batch"] == 130'),
        ('"batch": 129', '"batch": 130'),
        ("len(previous) == 8718 and len(current) == 8724",
         "len(previous) == 8724 and len(current) == 8730"),
    ]
    output = TOOLS / "verify_b130_payload.py"
    test_output = TOOLS / "test_verify_b130_payload.py"
    require(not output.exists() and not test_output.exists(), "Preserve existing derived tools")
    guard, _ = start_guard("B130 signed-payload verifier preparation")
    try:
        value, substitutions = derive(raw, changes)
        test_value, test_substitutions = derive(test_raw, [("verify_b129_payload", "verify_b130_payload")])
        compile(value, str(output), "exec")
        compile(test_value, str(test_output), "exec")
        guard.check()
        outputs = [write_frozen(output, value), write_frozen(test_output, test_value)]
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(HERE / "payload-verifier-derivation-001.json", {
        "batch": 130, "status": "PREPARATION_ONLY",
        "sources": [{"path": str(source_path), "sha256": SOURCE_SHA},
                    {"path": str(test_path), "sha256": TEST_SHA}],
        "outputs": outputs, "substitutions": substitutions, "testSubstitutions": test_substitutions,
        "reverseExact": True, "memory": memory,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "observedMembers": ["\u5840", "\u62cd", "\u8017"],
        "baselineSupportInspection": "All three complete baseline articles have a substantive "
            "component introduction and no now-false no-card sentence. Only one reciprocal wrapper "
            "per support is permitted; no prose exception.",
        "limits": "Candidate-specific membership is provisional until the author's signed handoff. "
                  "No author files changed, candidate accepted or reviewer launched.",
    })))


if __name__ == "__main__":
    main()
