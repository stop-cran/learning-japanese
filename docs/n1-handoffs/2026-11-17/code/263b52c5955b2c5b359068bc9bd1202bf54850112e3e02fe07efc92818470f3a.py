"""Specialize the frozen complete-source verifier for B130's observed schema."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
SOURCE = TOOLS / "verify_b129_sources.py"
SOURCE_SHA = "9fb0aa1b179679638865582eed251f2c4fd4c9a84707f56099383808b18d0b33"
OUTPUT = TOOLS / "verify_b130_sources.py"
HERE = WS / "scratch-130" / "review"


def main():
    raw = frozen(SOURCE, SOURCE_SHA)
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8").replace("\r\n", "\n")
    require(text.replace("\n", newline).encode("utf-8") == raw, "Mixed source line endings")
    schema = TOOLS / "b130_source_schema.py"
    tests = TOOLS / "test_b130_source_schema.py"
    schema_sha, tests_sha = sha(frozen(schema)), sha(frozen(tests))
    require(not OUTPUT.exists(), "Preserve existing verifier")
    guard, _ = start_guard("B130 source-verifier preparation")
    changes = []

    def replace(before, after, count=1):
        nonlocal text
        require(text.count(before) == count and after not in text,
                f"Ambiguous source substitution: {before}")
        text = text.replace(before, after)
        changes.append({"before": before, "after": after, "count": count})

    try:
        replace("import b129_source_schema as schema", "import b130_source_schema as schema")
        replace('SCHEMA_SHA = "4d7c4f4187d405120d7fff38d2c3c18a1b2dbcde13306ef65d64ed792b4cb12c"',
                f'SCHEMA_SHA = "{schema_sha}"')
        replace('require(facts["batch"] == 129, "B129 verifier requires batch 129")',
                'require(facts["batch"] == 130 and facts["requireCheckout"] is True,\n'
                '            "B130 verifier requires batch 130 and its clean signed checkout")')
        replace(
            '            cards[char] = {"kanji": char, "path": name, "baselineGitBytesSha256": sha(raw), "title": metadata["title"]}\n',
            '            working = (Path(facts["repo"]) / name).read_bytes()\n'
            '            require(working.replace(b"\\r\\n", b"\\n") == raw.replace(b"\\r\\n", b"\\n"),\n'
            '                    f"Baseline working content differs: {name}")\n'
            '            cards[char] = {"kanji": char, "path": name, "baselineGitBytesSha256": sha(raw),\n'
            '                           "baselineWorkingBytesSha256": sha(working),\n'
            '                           "baselineNormalizedSha256": baseline[name], "title": metadata["title"]}\n')
        replace("Usage: verify_b129_sources.py", "Usage: verify_b130_sources.py")
        reverse = text
        for change in reversed(changes):
            require(reverse.count(change["after"]) == change["count"], "Reverse count differs")
            reverse = reverse.replace(change["after"], change["before"])
        require(reverse.replace("\n", newline).encode("utf-8") == raw, "Derivation is not byte-reversible")
        compile(text, str(OUTPUT), "exec")
        guard.check()
        output = write_frozen(OUTPUT, text.replace("\n", newline).encode("utf-8"))
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(HERE / "source-verifier-derivation-001.json", {
        "batch": 130, "status": "PREPARATION_ONLY",
        "source": {"path": str(SOURCE), "sha256": SOURCE_SHA},
        "output": output, "substitutions": changes, "reverseExact": True,
        "schema": {"path": str(schema), "sha256": schema_sha},
        "tests": {"path": str(tests), "sha256": tests_sha},
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "memory": memory,
        "limits": "Observed author schema only; final handoff may change. No signed candidate, "
                  "dictionary selection, scan, linguistic review or publication accepted.",
    })))


if __name__ == "__main__":
    main()
