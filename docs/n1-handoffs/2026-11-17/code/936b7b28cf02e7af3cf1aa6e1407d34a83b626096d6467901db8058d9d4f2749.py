"""Keep the established review protocol while naming the actual source types."""
import json
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen


def main():
    here = Path(__file__).resolve().parent
    source = here / "build-prompts-v2.py"
    raw = frozen(source)
    original_request = (
        'Original user request: "Please find and inspect work items at stop-cran/learning-japanese '
        'related to creating N1 kanji cards. The work is ~30% complete. Fetch latest changes, find '
        'and read related repo work items, gather the context, plan the outstanding work and do it."'
        '\n\nAssigned slice: independent content review only. The frozen prompt supplies the exact '
        'snapshot, scope and access rules.\n\n'
    )
    replacements = [
        ("SUPPLIED complete Weblio source-section extract", "SUPPLIED complete cited-source extract"),
        ("build-prompts-v2.py", "build-prompts-b127.py"),
        ('kickoff = (f"Read {prompt_path}', 'kickoff = (' + repr(original_request) + ' + f"Read {prompt_path}'),
    ]
    text, changes = raw.decode("utf-8"), []
    for before, after in replacements:
        count = text.count(before)
        require(count > 0 and after not in text, f"Ambiguous prompt substitution: {before}")
        text = text.replace(before, after)
        changes.append({"before": before, "after": after, "count": count})
    restored = text
    for item in reversed(changes):
        require(restored.count(item["after"]) == item["count"], "Prompt reverse count differs")
        restored = restored.replace(item["after"], item["before"])
    require(restored.encode("utf-8") == raw, "Unexpected prompt changes")
    target = here / "build-prompts-b127.py"
    compile(text, str(target), "exec")
    binding = write_frozen(target, text.encode("utf-8"))
    print(json.dumps(freeze_json(here.parent / "scratch-127" / "review" / "prompt-builder-derivation.json", {
        "source": str(source), "sourceSha256": sha(raw), "target": binding,
        "substitutions": changes, "reverseExact": True,
        "scope": "Neutral source-type wording and verbatim original-user context. No author findings, "
                 "dispositions or other review evidence is supplied.",
    })))


if __name__ == "__main__":
    main()
