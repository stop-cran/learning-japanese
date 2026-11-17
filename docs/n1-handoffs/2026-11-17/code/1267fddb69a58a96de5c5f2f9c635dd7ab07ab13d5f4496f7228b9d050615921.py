"""Derive B124's source verifier, including its separate comparison supplement."""
from common import freeze_json, frozen, require, review_dir, sha, write_frozen

SOURCE_SHA = "8c5165c17eded66fe4a0c7712acff01b36f65e7b7f5f7c41a06feaa56e4ebe21"
BASE = "2655539b587c1ab57e64ab74a97cddaf81bb81c6"
COMPARISONS = "富豊容補複満余"
QUERIES = ("余裕", "余猶", "裕福", "富裕", "富", "富む", "豊", "豊か",
           "豊富", "豊作", "余分", "余る")


def main():
    source = review_dir(123) / "verify-source-records.py"
    output = review_dir(124) / "verify-source-records.py"
    provenance = review_dir(124) / "source-verifier-derivation.json"
    require(not output.exists() and not provenance.exists(), "Preserve existing B124 source tools")
    text = frozen(source, SOURCE_SHA).decode("utf-8").replace("\r\n", "\n")
    substitutions = []

    def replace(before, after, expected=1):
        nonlocal text
        count = text.count(before)
        require(count == expected, f"Unexpected substitution count: {before!r}: {count}")
        text = text.replace(before, after)
        substitutions.append({"before": before, "after": after, "count": count})

    for before, after, count in (
        ("B123", "B124", 3),
        ("b123-worktree", "b124-worktree", 1),
        ("batch-123/", "batch-124/", 1),
        ('"batch": 123', '"batch": 124', 1),
        ("6e433d4046144f6eb2593ab2661cc7206c9139be", BASE, 1),
        ('MEMBER = "範"', 'MEMBER = "裕"', 1),
    ):
        replace(before, after, count)
    start, end = text.index("COMPARISONS = "), text.index("INPUTS = ")
    queries = "{" + ", ".join(repr(value) for value in sorted(QUERIES)) + "}"
    replace(text[start:end], f"COMPARISONS = set({COMPARISONS!r})\nQUERIES = {queries}\n")
    replace(
        "    found = [set() for _ in selections]\n",
        '    for selection in selections:\n'
        '        require(selection["mode"] in {"contains-member", "contains-any", "exact"},\n'
        '                f"Unsupported selection mode: {selection[\'mode\']}")\n'
        '        if selection["mode"] == "contains-any":\n'
        '            require(selection["queries"] and all(selection["queries"]),\n'
        '                    "Contains-any selection requires nonempty queries")\n'
        "    found = [set() for _ in selections]\n",
    )
    replace(
        '                        else bool(keys & selection["queries"]))\n',
        '                        else any(query in item for query in selection["queries"] for item in keys)\n'
        '                        if selection["mode"] == "contains-any"\n'
        '                        else bool(keys & selection["queries"]))\n',
    )
    replace(
        '            with gzip.open(source, "rb") as stream:\n',
        '            name = f"comparison-supplement-001/{kind}-records.xml"\n'
        '            raw = blob(PREFIX + name)\n'
        '            selections.append({\n'
        '                "name": name, "sha256": sha(raw),\n'
        '                "mode": "contains-any" if kind == "jmdict" else "exact",\n'
        '                "queries": {"厚", "財"}, "expected": records(raw, tag, key),\n'
        '            })\n'
        '            with gzip.open(source, "rb") as stream:\n',
    )
    require("範" not in text and "b123" not in text and "B123" not in text,
            "Predecessor selection leaked into B124 verifier")
    compile(text, str(output), "exec")
    binding = write_frozen(output, text.encode("utf-8"))
    print(freeze_json(provenance, {
        "batch": 124,
        "source": {"path": str(source), "sha256": SOURCE_SHA},
        "output": binding,
        "substitutions": substitutions,
        "selection": {
            "member": "裕", "comparisons": list(COMPARISONS), "exactQueries": list(QUERIES),
            "supplement": {"characters": ["厚", "財"], "jmdictMode": "contains-any"},
        },
        "scope": "Tool preparation only. No candidate, source, content-review or publication acceptance.",
    }))


if __name__ == "__main__":
    main()
