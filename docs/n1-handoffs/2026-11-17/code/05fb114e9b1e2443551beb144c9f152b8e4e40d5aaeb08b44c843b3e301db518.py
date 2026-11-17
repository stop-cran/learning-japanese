"""Specialize the frozen complete-source verifier for B129's observed packet schema."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
SOURCE = TOOLS / "verify_batch_sources_v2.py"
SOURCE_SHA = "2f6c7ea084b17022360031d6e17b491926c802d2ff0e3cc32ddfbc1a7130ce30"
OUTPUT = TOOLS / "verify_b129_sources.py"
RECORD = WS / "scratch-129" / "review" / "source-verifier-derivation-001.json"


def main():
    raw = frozen(SOURCE, SOURCE_SHA)
    schema_path = TOOLS / "b129_source_schema.py"
    schema_sha = sha(frozen(schema_path))
    fixture_path = TOOLS / "test_b129_source_schema.py"
    fixture_raw = frozen(fixture_path)
    require(not OUTPUT.exists() and not RECORD.exists(), "Preserve existing B129 verifier")
    guard, _ = start_guard("B129 complete-source verifier derivation")
    changes = []
    text = raw.decode("utf-8")

    def replace(before, after, count=1):
        nonlocal text
        require(text.count(before) == count and after not in text,
                f"Ambiguous verifier derivation: {before}")
        text = text.replace(before, after)
        changes.append({"before": before, "after": after, "count": count})

    try:
        replace(
            'import source_query_union\n',
            'import source_query_union\nimport b129_source_schema as schema\n'
            f'SCHEMA_SHA = "{schema_sha}"\n')
        replace(
            '    frozen(Path(source_query_union.__file__), QUERY_SHA)\n',
            '    frozen(Path(source_query_union.__file__), QUERY_SHA)\n'
            '    frozen(Path(schema.__file__), SCHEMA_SHA)\n')
        replace(
            '    facts = json.loads(raw)\n',
            '    facts = json.loads(raw)\n'
            '    require(facts["batch"] == 129, "B129 verifier requires batch 129")\n')
        start, end = text.index("def verify_scan("), text.index("def main(facts_path):")
        replace(text[start:end], "verify_scan = schema.verify_scan\n\n\n")
        replace(
            '        signed_rows = None\n'
            '        if len(members) == 1:\n'
            '            signed_rows = [json.loads(blob(prefix + "source-row.json"))]\n'
            '        selection = json.loads(blob(prefix + "selection.json"))\n'
            '        require([item["kanji"] for item in selection["membership"]] == members, "Selection order differs")\n',
            '        source_rows_raw = blob(prefix + "source-rows.json")\n'
            '        signed_rows = json.loads(source_rows_raw)\n'
            '        selection_raw = blob(prefix + "selection.json")\n'
            '        selection = json.loads(selection_raw)\n'
            '        membership = schema.verify_selection(selection, signed_rows, index, members, base)\n')
        replace('selection["membership"][position]["sourceRow"]',
                'membership[position]["sourceRow"]')
        replace('(signed_rows is None or signed_rows[0] == row)', 'signed_rows[position] == row')
        replace('scan["newKanji"] == char', 'scan["kanji"] == char')
        replace(
            '        "checkoutBound": facts["requireCheckout"],\n',
            '        "checkoutBound": facts["requireCheckout"],\n'
            '        "authorSchema": {"path": str(Path(schema.__file__)), "sha256": SCHEMA_SHA},\n'
            '        "selectionSha256": sha(selection_raw),\n'
            '        "sourceRowsSha256": sha(source_rows_raw),\n')
        replace("Usage: verify_batch_sources_v2.py", "Usage: verify_b129_sources.py")
        reverse = text
        for change in reversed(changes):
            require(reverse.count(change["after"]) == change["count"],
                    "Verifier reverse substitution count differs")
            reverse = reverse.replace(change["after"], change["before"])
        require(reverse.encode("utf-8") == raw, "Verifier derivation is not byte-reversible")
        compile(text, str(OUTPUT), "exec")
        compile(fixture_raw, str(fixture_path), "exec")
        guard.check()
        output = write_frozen(OUTPUT, text.encode("utf-8"))
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Verifier derivation RAM breach")
    print(json.dumps(freeze_json(RECORD, {
        "batch": 129, "status": "PREPARATION_ONLY",
        "source": {"path": str(SOURCE), "sha256": SOURCE_SHA},
        "output": output, "substitutions": changes, "reverseExact": True,
        "schema": {"path": str(schema_path), "sha256": schema_sha},
        "tests": {"path": str(fixture_path), "sha256": sha(fixture_raw)},
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "memory": memory,
        "limits": "Schema specialization only. No author files modified, candidate verified, "
                  "reviewer launched or publication approved. Signed-candidate facts remain required.",
    })))


if __name__ == "__main__":
    main()
