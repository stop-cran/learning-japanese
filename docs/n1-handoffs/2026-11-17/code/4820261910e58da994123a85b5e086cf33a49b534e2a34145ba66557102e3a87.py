"""Prepare the B121-local reviewer gates without touching the author's candidate."""
import json
import sys

from common import WS, freeze_json, require, review_dir, sha, write_frozen


def main():
    source = review_dir(120) / "guarded-test.py"
    raw = source.read_bytes()
    text = raw.decode("utf-8")
    replacements = [("b120-worktree", "b121-worktree", 1), ("scratch-120", "scratch-121", 2)]
    for before, after, count in replacements:
        require(text.count(before) == count and after not in text, f"Ambiguous replacement: {before}")
        text = text.replace(before, after)
    reverse = text
    for before, after, count in reversed(replacements):
        require(reverse.count(after) == count, f"Reverse count differs: {after}")
        reverse = reverse.replace(after, before)
    require(reverse.encode("utf-8") == raw, "Non-path changes to the inherited RAM guard")
    output = review_dir(121) / "guarded-test.py"
    compile(text, str(output), "exec")
    record = write_frozen(output, text.encode("utf-8"))
    record.update(source=str(source), sourceSha256=sha(raw), reverseExact=True,
                  substitutions=replacements, resourceLimitsUnchanged=True)
    freeze_json(review_dir(121) / "guarded-test-derivation.json", record)
    deriver = WS / "review-tools" / "derive-tooling.py"
    require(sha(deriver.read_bytes()) == "daf932df4bc3022cdd7dc7495807900906d5d73cf385d270368c9178ba0122aa",
            "Review gate deriver changed from the prior verified version")
    print(json.dumps({"guardedRunner": record, "gateDeriver": str(deriver),
                      "nextCommand": [sys.executable, "-B", str(output),
                                      str(review_dir(121) / "derive-review-tools-001"),
                                      sys.executable, "-B", str(deriver), "121"]}))


if __name__ == "__main__":
    main()
