"""Version the B123 contract builder's missed source-receipt batch literal."""
import json
import re

from common import freeze_json, frozen, require, review_dir, sha, write_frozen


def main():
    directory = review_dir(123)
    derivation = json.loads(frozen(
        directory / "source-tool-derivation.json",
        "b1b2c99a329011a790fe4b422ecc2d59c55d752def90b00a73f4c7309c0261b7"))
    source = directory / "prepare-source-contract.py"
    binding = next(item for item in derivation["derivations"]
                   if item["target"] == str(source))
    raw = frozen(source, binding["targetSha256"])
    before, after = b'receipt["batch"] == "122"', b'receipt["batch"] == "123"'
    require(raw.count(before) == 1 and after not in raw, "Ambiguous batch-literal repair")
    updated = raw.replace(before, after)
    require(not re.search(rb"\b122\b", updated), "A stale batch identity remains")
    require(updated.replace(after, before) == raw, "Unexpected builder changes")
    output = directory / "prepare-source-contract-v2.py"
    compile(updated, str(output), "exec")
    written = write_frozen(output, updated)
    print(json.dumps(freeze_json(directory / "source-contract-v2-derivation.json", {
        "source": str(source), "sourceSha256": sha(raw), "output": written,
        "before": before.decode(), "after": after.decode(), "reverseExact": True,
        "reason": "The live binding correctly refused the old source-receipt batch literal. "
                  "The candidate and all other checks are unchanged; failed tooling and logs remain.",
    })))


if __name__ == "__main__":
    main()
