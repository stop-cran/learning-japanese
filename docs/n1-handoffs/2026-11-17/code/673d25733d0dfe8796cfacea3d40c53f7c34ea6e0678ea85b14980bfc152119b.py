"""Derive B126 reviewer tooling from the frozen B125 bounded runner."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, review_dir, sha, start_guard, write_frozen


def main():
    require((WS / "scratch-126").is_dir(), "Wait for the author to initialize scratch-126")
    guard, _ = start_guard("B126 review-tool preparation")
    try:
        source = review_dir(125) / "guarded-test-v2.py"
        raw = frozen(source, "72e4088803cdee36351a3ffadcc7a3d9632ea8522ebdc706233b4899ee65bcd7")
        text = raw.decode("utf-8")
        replacements = [
            ("b125-worktree", "b126-worktree", 1),
            ("scratch-125", "scratch-126", 1),
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
        output = review_dir(126) / "guarded-test-v2.py"
        compile(text, str(output), "exec")
        fixture_source = review_dir(125) / "test-guarded-test-v2.py"
        fixtures = frozen(fixture_source, "b8f6ef0f40764802110c68318335ac9389642dbf097bbbf857199c92d11dc976")
        fixture_output = output.with_name(fixture_source.name)
        compile(fixtures, str(fixture_output), "exec")
        deriver = WS / "review-tools" / "derive-tooling.py"
        deriver_sha = "daf932df4bc3022cdd7dc7495807900906d5d73cf385d270368c9178ba0122aa"
        require(sha(deriver.read_bytes()) == deriver_sha, "Generic review deriver changed")
        guard.check()
        runner_record = write_frozen(output, text.encode("utf-8"))
        fixture_record = write_frozen(fixture_output, fixtures)
        runner_record.update(source=str(source), sourceSha256=sha(raw), substitutions=replacements,
                             reverseExact=True, resourceLimitsUnchanged=True, boundedWaitSeconds=0.1)
        fixture_record.update(source=str(fixture_source), sourceSha256=sha(fixtures), byteIdentical=True)
        guard.check()
    finally:
        memory = guard.finish()
    require(memory["breach"] is None, "Tool preparation breached RAM limits")
    print(json.dumps(freeze_json(review_dir(126) / "guarded-test-derivation.json", {
        "batch": 126, "guardedRunner": runner_record, "guardedRunnerTests": fixture_record,
        "genericDeriver": {"path": str(deriver), "sha256": deriver_sha},
        "memory": memory, "producerSha256": sha(Path(__file__).read_bytes()),
        "scope": "Coordinator tooling only; no author-worktree edits or content acceptance.",
    })))


if __name__ == "__main__":
    main()
