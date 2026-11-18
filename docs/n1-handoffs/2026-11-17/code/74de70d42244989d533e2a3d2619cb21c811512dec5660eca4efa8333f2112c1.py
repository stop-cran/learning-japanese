"""Use a generated nil-UUID test fixture instead of publishing a literal unrelated UUID."""
from common import TOOLS, WS, freeze_json, frozen, sha, write_frozen
from derive_b133_closure_recorders_v2 import replace


def main():
    test = frozen(TOOLS / "test_b133_closure_retention.py")
    test = replace(test, "import unittest", "import unittest\nimport uuid")
    test = replace(test, 'b"12345678-1234-1234-1234-123456789abc"',
                   "str(uuid.UUID(int=0)).encode()")
    test_ref = write_frozen(TOOLS / "test_b133_closure_retention_v2.py", test)
    original = frozen(TOOLS / "close_b133_v3.py")
    raw = replace(original, '"test_b133_closure_retention.py"', '"test_b133_closure_retention_v2.py"')
    raw = replace(raw, '"close_b133_v3.py",\n', '"close_b133_v3.py", "close_b133_v4.py",\n')
    raw = replace(raw, '"closure-real-report-003.json"', '"closure-real-report-004.json"')
    compile(raw, "close_b133_v4.py", "exec")
    print(freeze_json(WS / "scratch-133" / "review" / "closure-v4-derivation.json", {
        "originalSha256": sha(original), "test": test_ref,
        "successor": write_frozen(TOOLS / "close_b133_v4.py", raw),
        "scope": "The preserved v3 dry run found the synthetic UUID in the archived test source. "
                 "Generate a nil UUID at test runtime instead. No real identity is hidden, "
                 "no publication allowlist or review/retention check is relaxed.",
    }))


if __name__ == "__main__":
    main()
