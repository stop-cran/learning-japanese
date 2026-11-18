"""Preserve v1 and derive the signed B130 schema adaptation with reversible edits."""
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen

ROOT = Path(__file__).resolve().parent
OLD_SHA = "a287e3380e72e322b4f339353b9e3463832f7f507491edc1f88dc15253701778"


def main():
    original = frozen(ROOT / "verify_b130_evidence.py", OLD_SHA)
    text = original.decode("utf-8").replace("\r\n", "\n")
    newline = "\r\n" if b"\r\n" in original else "\n"
    replacements = []

    def replace(old, new):
        nonlocal text
        require(text.count(old) == 1, "Derivation anchor is missing or ambiguous: " + old[:80])
        text = text.replace(old, new)
        replacements.append((old, new))

    helper = ROOT / "b130_signed_evidence.py"
    replace("from source_query_union import selects\n",
            "from source_query_union import selects\n"
            "from b130_signed_evidence import (FINAL_VERIFIER_SHA, RESIDUAL, receipt_outputs,\n"
            "                                  verify_final_proof, verify_progress)\n"
            f'SIGNED_HELPER_SHA = "{sha(helper.read_bytes())}"\n')
    replace('    "preservation", "output",\n',
            '    "preservation", "output", "finalSourceProof", "readingKeys",\n')
    replace('             *facts["scanDirectories"], *facts["externalBindings"], facts["fontEvidence"]]',
            '             *facts["scanDirectories"], *facts["externalBindings"], facts["fontEvidence"],\n'
            '             facts["readingKeys"]]')
    first = text.index("def reading_extras(")
    last = text.index("def verify_excerpt(", first)
    replace(text[first:last], "from b130_signed_evidence import verify_reading_keys\n\n\n")
    replace('    facts, facts_raw = load_facts(facts_path, facts_sha)\n',
            '    facts, facts_raw = load_facts(facts_path, facts_sha)\n'
            '    frozen(Path(__file__).with_name("b130_signed_evidence.py"), SIGNED_HELPER_SHA)\n')
    anchor = '    frozen(Path(__file__).with_name("verify_b130_sources.py"), source_proof["verifierSha256"])\n'
    replace(anchor,
            '    final_path, final_sha = facts["finalSourceProof"]["path"], facts["finalSourceProof"]["sha256"]\n'
            '    require(Path(final_path).resolve().parent == HERE, "Final proof must be frozen in B130 review")\n'
            '    final_proof = json.loads(frozen(final_path, final_sha))\n'
            '    verify_final_proof(final_proof, source_sha, candidate)\n'
            '    frozen(Path(__file__).with_name("verify_b130_final_sources.py"), FINAL_VERIFIER_SHA)\n' + anchor)
    replace('        jm = helper.merge_records([blob(record["path"]) for record in source_proof["sourceRecords"]\n'
            '                                   if record["input"] == "n1-implementation-JMdict_e.gz"], "entry", "ent_seq")',
            '        for name, digest in final_proof["signedInputs"].items():\n'
            '            require(sha(blob(name)) == digest, "Final source proof input changed")\n'
            '        jm = helper.merge_records([blob(record["path"]) for record in source_proof["sourceRecords"]\n'
            '                                   if record["input"] == "n1-implementation-JMdict_e.gz"]\n'
            '                                  + [source(RESIDUAL)], "entry", "ent_seq")')
    replace('            for name, binding in receipt["outputs"].items():',
            '            for name, binding in receipt_outputs(receipt).items():')
    replace('        require(bound_outputs == {record["path"].removeprefix(PREFIX) for record in source_proof["sourceRecords"]},',
            '        require(bound_outputs == {record["path"].removeprefix(PREFIX) for record in source_proof["sourceRecords"]}\n'
            '                | {RESIDUAL},')
    first = text.index('        require(progress["base"] == BASE')
    last = text.index("        excerpts = 0", first)
    replace(text[first:last], "        verify_progress(progress, facts, payload)\n")
    replace('                                     captures["committed/reading-exposure.log"], facts["requiredReadingKeys"])',
            '                                     source(facts["readingKeys"]),\n'
            '                                     captures["committed/reading-exposure.log"], facts["requiredReadingKeys"])')
    replace('        "payloadProof": {"path": payload_path, "sha256": payload_sha},',
            '        "payloadProof": {"path": payload_path, "sha256": payload_sha},\n'
            '        "finalSourceProof": {"path": final_path, "sha256": final_sha},')
    replace('Usage: verify_b130_evidence.py FROZEN_FACTS SHA256',
            'Usage: verify_b130_evidence_v2.py FROZEN_FACTS SHA256')
    restored = text
    for old, new in reversed(replacements):
        require(restored.count(new) == 1, "Reverse derivation is ambiguous")
        restored = restored.replace(new, old)
    require(restored.replace("\n", newline).encode("utf-8") == original, "Derivation is not byte-reversible")
    compile(text, "verify_b130_evidence_v2.py", "exec")
    output = write_frozen(ROOT / "verify_b130_evidence_v2.py", text.replace("\n", newline).encode("utf-8"))
    print(freeze_json(ROOT.parent / "scratch-130" / "review" / "evidence-v2-derivation.json", {
        "source": {"path": str(ROOT / "verify_b130_evidence.py"), "sha256": OLD_SHA},
        "output": output, "helperSha256": sha(helper.read_bytes()),
        "changes": replacements, "byteReversible": True,
        "limits": "Schema adaptation only. Tests and execution on the signed candidate remain required.",
    }))


if __name__ == "__main__":
    main()
