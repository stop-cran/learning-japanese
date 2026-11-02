import hashlib
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

import freeze_n1_sources as freeze


class FrozenInputTest(unittest.TestCase):
    def test_exact_bytes_required_and_not_replaced(self):
        raw = b"frozen\r\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample"
            path.write_bytes(raw)
            with patch.dict(freeze.INPUTS, {"sample": hashlib.sha256(raw).hexdigest()}, clear=True):
                self.assertEqual(freeze.load_inputs(Path(directory)), {"sample": raw})
                path.write_bytes(b"frozen\n")
                with self.assertRaisesRegex(ValueError, "Frozen input hash mismatch"):
                    freeze.load_inputs(Path(directory))
                self.assertEqual(path.read_bytes(), b"frozen\n")


class CharacterExtractionTest(unittest.TestCase):
    def test_reading_order_affixes_and_stroke_annotations_preserved(self):
        element = ET.fromstring("""
            <character>
              <literal>氏</literal>
              <radical><rad_value rad_type="classical">83</rad_value></radical>
              <misc><grade>4</grade><stroke_count>4</stroke_count>
                <stroke_count>5</stroke_count><jlpt>1</jlpt></misc>
              <reading_meaning><rmgroup>
                <reading r_type="ja_on">シ</reading>
                <reading r_type="ja_on">シ</reading>
                <reading r_type="ja_kun">うじ</reading>
                <reading r_type="ja_kun">-うじ</reading>
                <meaning>family name</meaning>
                <meaning m_lang="fr">clan</meaning>
              </rmgroup><nanori>うぢ</nanori></reading_meaning>
            </character>
        """)
        result = freeze.metadata_record(element, {83: "氏"})
        self.assertEqual(result["onyomi"], ["シ", "シ"])
        self.assertEqual(result["kunyomi"], ["うじ", "-うじ"])
        self.assertEqual(result["strokes"], 4)
        self.assertEqual(result["strokeCountAnnotations"],
                         [{"count": 4, "attributes": {}}, {"count": 5, "attributes": {}}])
        self.assertEqual(result["meanings"], ["family name"])
        self.assertNotIn("nanori", result)
        self.assertNotIn("jlpt", result)

    def test_missing_classical_radical_is_an_error(self):
        with self.assertRaisesRegex(ValueError, "No classical radical"):
            freeze.metadata_record(ET.fromstring("<character><literal>氏</literal></character>"), {})

    def test_pilot_is_bounded_and_risk_stratified(self):
        self.assertLessEqual(len(freeze.PILOT), 15)
        risks = {risk for values in freeze.PILOT.values() for risk in values}
        self.assertIn("system-font fallback", risks)
        self.assertIn("maximum source stroke count", risks)
        self.assertIn("bound suffix", risks)
        self.assertIn("baseline support reuse", risks)


if __name__ == "__main__":
    unittest.main()
