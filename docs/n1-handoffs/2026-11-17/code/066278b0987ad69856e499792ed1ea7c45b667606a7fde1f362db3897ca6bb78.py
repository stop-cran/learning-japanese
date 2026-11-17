"""Derive correction-aware evidence verification without rewriting frozen v2."""
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).parent


def main():
    original = frozen(HERE / "verify_b129_evidence_v2.py",
                      "f19d587797ef3574e35498aa57b12e5939d9f7f7b74feb6670d60c8af4323d02")
    helper = frozen(HERE / "b129_correction_evidence.py")
    text = original.decode()
    changes = [
        ('from source_query_union import selects',
         'from source_query_union import selects\nimport b129_correction_evidence as correction\n'
         f'CORRECTION_HELPER_SHA = "{sha(helper)}"'),
        ('        inventory = json.loads(source("evidence-inventory-002.json"))',
         '        inventory = json.loads(source("evidence-inventory-003.json"))'),
        ('and inventory["supersedesForFinalBinding"] == "evidence-inventory.json"\n'
         '                and paths == set(inventory["files"]) | {"evidence-inventory-002.json"}',
         'and inventory["supersedesForFinalBinding"] == "evidence-inventory-002.json"\n'
         '                and paths == set(inventory["files"]) | {"evidence-inventory-003.json"}'),
        ('        original = json.loads(source("evidence-inventory.json"))',
         '        previous = json.loads(source("evidence-inventory-002.json"))\n'
         '        require(previous["selfExcluded"] is True\n'
         '                and previous["supersedesForFinalBinding"] == "evidence-inventory.json"\n'
         '                and all(inventory["files"].get(name) == digest\n'
         '                        for name, digest in previous["files"].items()),\n'
         '                "Final inventory does not preserve inventory 002")\n'
         '        original = json.loads(source("evidence-inventory.json"))'),
        ('        clean()\n    finally:\n        memory = guard.finish()',
         '        frozen(Path(correction.__file__), CORRECTION_HELPER_SHA)\n'
         '        corrected = correction.verify(git, blob, source, candidate, payload, SCRATCH,\n'
         '                                      gates_name, preservation_name, findings)\n'
         '        findings = []\n'
         '        clean()\n    finally:\n        memory = guard.finish()'),
        ('        "findings": findings,', '        "findings": findings, "verifiedCorrection": corrected,'),
    ]
    applied = []
    newline = "\r\n" if b"\r\n" in original else "\n"
    for before, after in changes:
        before, after = (value.replace("\n", newline) for value in (before, after))
        require(text.count(before) == 1, f"Ambiguous evidence adaptation: {before[:80]}")
        text = text.replace(before, after)
        applied.append({"before": before, "after": after, "count": 1})
    reverse = text
    for change in reversed(applied):
        require(reverse.count(change["after"]) == 1, "Ambiguous reverse adaptation")
        reverse = reverse.replace(change["after"], change["before"])
    require(reverse.encode() == original, "Evidence derivation is not byte-reversible")
    target = HERE / "verify_b129_evidence_v3.py"
    compile(text, str(target), "exec")
    result = write_frozen(target, text.encode())
    print(freeze_json(WS / "scratch-129" / "review" / "evidence-v3-derivation.json", {
        "sourceSha256": sha(original), "output": result, "helperSha256": sha(helper),
        "reverseExact": True, "substitutions": applied,
        "scope": "Checks final inventory 003 and the exact two-file correction; preserves v2, "
                 "historical findings and original bytes. No reviewer or publication acceptance.",
    }))


if __name__ == "__main__":
    main()
