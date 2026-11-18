import copy
import json
from pathlib import Path

from common_134 import BASE, HERE, canonical, records, sha, start_guard, write, xml_output

OUT = HERE / "supplement-001"
WANTED = "紫茈此糸止比"
guard = start_guard()
try:
    selected = {}
    for node in records("kanjidic2", guard):
        ch = node.findtext("literal")
        if ch in WANTED:
            assert ch not in selected
            selected[ch] = copy.deepcopy(node)
    assert set(selected) == set(WANTED)
    result = xml_output(OUT / "kanjidic2-components-variant.xml", "kanjidic2",
                        [selected[c] for c in WANTED])
    expected = result["canonicalRecordHashes"]
    actual = {}
    for node in records("kanjidic2", guard):
        ch = node.findtext("literal")
        if ch in WANTED:
            actual[ch] = sha(canonical(node).encode())
    assert actual == expected
    target_receipt = json.loads((HERE / "source-002" / "source-receipt.json").read_bytes())
    assert expected["紫"] == target_receipt["outputs"]["kanjidic2-targets.xml"]["canonicalRecordHashes"]["紫"]
    write(OUT / "receipt.json", {
        "base": BASE, "selection": list(WANTED),
        "predicate": "Exact KANJIDIC2 literal: target, search-only spelling variant and named modern components.",
        "output": result,
        "verification": "Second full-stream hash and canonical-record recomputation, plus target equality with source-002.",
        "producerSha256": sha(Path(__file__).read_bytes()),
        "transformation": "Complete parsed/reserialized records, not raw slices.",
    })
finally:
    write(OUT / "memory.json", guard.finish())
