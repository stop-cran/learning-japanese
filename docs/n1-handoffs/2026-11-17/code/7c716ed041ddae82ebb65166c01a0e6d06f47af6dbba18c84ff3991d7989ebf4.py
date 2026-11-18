"""Derive B123 reviewer tooling from the repaired, frozen B122 runner."""
import json
from pathlib import Path

from common import (
    WS, freeze_json, frozen, require, review_dir, sha, start_guard, write_frozen,
)


def main():
    guard, _ = start_guard("B123 review-tool preparation")
    try:
        source = review_dir(122) / "guarded-test-v2.py"
        raw = frozen(source, "5cf7751ef3b87ed7bbfd07b412b811fe0e31212d1f3fdb7ebbd1d3ec1b6029ab")
        text = raw.decode("utf-8")
        replacements = [
            ("b122-worktree", "b123-worktree", 1),
            ("scratch-122", "scratch-123", 1),
        ]
        for before, after, count in replacements:
            require(text.count(before) == count and after not in text,
                    f"Ambiguous substitution: {before}")
            text = text.replace(before, after)
        reverse = text
        for before, after, count in reversed(replacements):
            require(reverse.count(after) == count, f"Reverse count differs: {after}")
            reverse = reverse.replace(after, before)
        require(reverse.encode("utf-8") == raw, "Unexpected runner changes")
        output = review_dir(123) / "guarded-test-v2.py"
        compile(text, str(output), "exec")
        fixture_source = review_dir(122) / "test-guarded-test-v2.py"
        fixtures = frozen(
            fixture_source,
            "b8f6ef0f40764802110c68318335ac9389642dbf097bbbf857199c92d11dc976")
        fixture_output = output.with_name(fixture_source.name)
        compile(fixtures, str(fixture_output), "exec")
        deriver = WS / "review-tools" / "derive-tooling.py"
        deriver_sha = "daf932df4bc3022cdd7dc7495807900906d5d73cf385d270368c9178ba0122aa"
        require(sha(deriver.read_bytes()) == deriver_sha, "Generic review deriver changed")
        guard.check()
        runner_record = write_frozen(output, text.encode("utf-8"))
        fixture_record = write_frozen(fixture_output, fixtures)
        runner_record.update(
            source=str(source), sourceSha256=sha(raw), substitutions=replacements,
            reverseExact=True, resourceLimitsUnchanged=True,
            boundedWaitSeconds=0.1)
        fixture_record.update(source=str(fixture_source), sourceSha256=sha(fixtures),
                              byteIdentical=True)
        guard.check()
    finally:
        memory = guard.finish()
    require(memory["breach"] is None, "Tool preparation breached RAM limits")
    record = {
        "batch": 123, "guardedRunner": runner_record,
        "guardedRunnerTests": fixture_record,
        "genericDeriver": {"path": str(deriver), "sha256": deriver_sha},
        "memory": memory, "producerSha256": sha(Path(__file__).read_bytes()),
        "scope": "Coordinator tooling only; no author-worktree edits or content acceptance.",
    }
    result = freeze_json(review_dir(123) / "guarded-test-derivation.json", record)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
