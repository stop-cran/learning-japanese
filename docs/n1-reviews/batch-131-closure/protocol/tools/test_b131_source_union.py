import copy
import unittest
import xml.etree.ElementTree as ET

from common import sha
from prepare_b131_source_facts import CANDIDATE_BASE, SOURCE_BASE, verify_output
from verify_b131_source_union import verify_audit


class SourceUnionTests(unittest.TestCase):
    def test_source_receipt_cannot_hide_changed_fields_or_duplicate_records(self):
        raw = b"<JMdict><entry><ent_seq>1</ent_seq><sense><gloss>first</gloss></sense></entry></JMdict>"
        node = ET.fromstring(raw)[0]
        recorded = {
            "sha256": sha(raw), "bytes": len(raw),
            "canonicalRecordHashes": {
                "1": sha(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode()),
            },
        }
        verify_output(raw, recorded)
        changed = raw.replace(b"first", b"second")
        altered_receipt = dict(recorded, sha256=sha(changed), bytes=len(changed))
        with self.assertRaisesRegex(ValueError, "canonical hashes"):
            verify_output(changed, altered_receipt)
        duplicate = raw.replace(b"</JMdict>", ET.tostring(node) + b"</JMdict>")
        altered_receipt = dict(recorded, sha256=sha(duplicate), bytes=len(duplicate))
        with self.assertRaisesRegex(ValueError, "duplicate source identity"):
            verify_output(duplicate, altered_receipt)

    def test_empty_residual_with_complete_union_is_valid(self):
        audit, kwargs = self.fixture()
        verify_audit(audit, **kwargs)
        verify_output(kwargs["residual"], audit["finalAdditionalOutput"])

    def test_union_audit_cannot_omit_absences_or_relabel_the_source_base(self):
        original, kwargs = self.fixture()
        for mutation in ("source-base", "entry-count", "omit-absent-query", "residual", "comparison-count"):
            audit = copy.deepcopy(original)
            if mutation == "source-base":
                audit["originalSourceBase"] = CANDIDATE_BASE
            elif mutation == "entry-count":
                audit["wholeJmdictEntriesScanned"] -= 1
            elif mutation == "omit-absent-query":
                del audit["queryCountsIncludingAbsences"]["exact-reading:absent"]
            elif mutation == "residual":
                audit["additionalFamilies"] = 1
            else:
                audit["comparisonCopies"] += 1
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, "union audit"):
                verify_audit(audit, **kwargs)

    def fixture(self):
        residual, producer = b"<JMdict />", b"inspected producer"
        counts = {"exact-spelling:x": 1, "exact-reading:absent": 0}
        inputs = {"jmdict": ["source.gz", "compressed", "decompressed", "entry"]}
        audit = {
            "base": CANDIDATE_BASE, "originalSourceBase": SOURCE_BASE,
            "completeJmdictUnion": 1, "originalFamiliesRechecked": 1, "additionalFamilies": 0,
            "wholeJmdictEntriesScanned": 2, "completeKanjidicRecordsRechecked": 1,
            "queryCountsIncludingAbsences": counts,
            "finalAdditionalOutput": {"sha256": sha(residual), "bytes": len(residual), "canonicalRecordHashes": {}},
            "dictionaryInputs": inputs, "comparisonCopies": 1, "producerSha256": sha(producer),
            "verification": "Fixture complete union.",
        }
        return audit, {
            "total": 2, "membership": {"1": ["exact-spelling:x"]}, "counts": counts,
            "kd": {"x"}, "comparisons": {"x"}, "inputs": inputs, "producer": producer, "residual": residual,
        }


if __name__ == "__main__":
    unittest.main()
