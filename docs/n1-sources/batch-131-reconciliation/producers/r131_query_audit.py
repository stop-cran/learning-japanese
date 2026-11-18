import json
import re
from pathlib import Path
from r131_common import *

guard = start_guard()
try:
    receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf8"))
    occurrences = {i: [] for i in receipt["predicates"]["entryIdsFromCompleteComparisonCards"]}
    for path in sorted((PACKET / "comparison-cards").glob("*.md")):
        for line_number, line in enumerate(path.read_text(encoding="utf8").splitlines(), 1):
            for key in re.findall(r"\b\d{7}\b", line):
                occurrences[key].append({
                    "card": path.name, "line": line_number,
                    "kind": "URL-identifier" if re.search(r"https?://[^\s)]*" + key, line)
                            else "decimal-text-reference"})
    membership = json.loads((PACKET / "query-membership.json").read_text(encoding="utf8"))
    collateral = [key for key, rows in occurrences.items()
                  if rows and all(r["kind"] == "URL-identifier" for r in rows)]
    assert collateral == ["2786520"], collateral
    assert membership["2786520"] == ["entry-id:2786520"]
    table = json.loads((PACKET / "pair-dispositions-001.json").read_text(encoding="utf8"))
    assert not any(2786520 in r["sources"]["completeJmdictEntryIds"] for r in table["rows"])
    write(PACKET / "source-query-allocation-001.json", {
        "sourceReceiptSha256": sha((PACKET / "source-receipt.json").read_bytes()),
        "predicateClarification": "entryIdsFromCompleteComparisonCards means mechanically discovered seven-digit references, not verified exclusively JMdict citations. This companion preserves the original exact query/output bytes and discloses one over-selection.",
        "occurrences": occurrences,
        "collateralReferenceIds": collateral,
        "collateralDisposition": "2786520 identifies the 冴 Kotobank page, not its JMdict family. The coincident unrelated 式内社 JMdict family was selected by that mechanical predicate and retained in full among the 78 query outputs, but is not used as lexical support in any decision. Do not treat it as a 冴 sense.",
        "counts": {"completeQueryOutputs": 78, "collateralFamiliesNotUsedAsLexicalSupport": 1},
        "producerSha256": sha(Path(__file__).read_bytes())})
    print("78 complete query outputs retained; one collateral external URL identifier explicitly excluded from lexical support.")
finally:
    write(HERE / "query-audit-memory-001.json", guard.finish())
