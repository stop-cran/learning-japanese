import unittest
import xml.etree.ElementTree as ET

from b129_confirmation_presentation import canonical
from prepare_b130_claude004 import require_unused_claude003, select_complete


class CompleteSelectionTests(unittest.TestCase):
    def test_complete_restrictions_and_languages_survive(self):
        raw = b'<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>A</keb><ke_inf>rare</ke_inf></k_ele><sense><stagk>A</stagk><gloss xml:lang="eng">touch</gloss><gloss xml:lang="ger">wirken</gloss></sense><sense><gloss>effect</gloss></sense></entry><entry><ent_seq>2</ent_seq><sense><gloss>else</gloss></sense></entry></JMdict>'
        data, facts = select_complete(raw, "entry", "ent_seq", ("1",))
        node = ET.fromstring(data).find("entry")
        self.assertEqual(canonical(ET.tostring(node)),
                         canonical(ET.tostring(ET.fromstring(raw).find("entry"))))
        self.assertEqual(facts["omittedRecordIds"], ["2"])
        self.assertFalse(facts["wholeInputDocumentPresented"])

    def test_missing_and_duplicate_identity_rejected(self):
        raw = b"<JMdict><entry><ent_seq>1</ent_seq></entry></JMdict>"
        for requested in (("2",), ("1", "1")):
            with self.subTest(requested=requested), self.assertRaises((ValueError, RuntimeError)):
                select_complete(raw, "entry", "ent_seq", requested)
        with self.assertRaises((ValueError, RuntimeError)):
            select_complete(raw.replace(b"</JMdict>", b"<entry><ent_seq>1</ent_seq></entry></JMdict>"),
                            "entry", "ent_seq", ("1",))

    def test_actual_prior_preparation_is_not_execution(self):
        prior = require_unused_claude003()
        self.assertEqual(prior["status"], "PREPARED_NOT_EXECUTED")
        self.assertEqual(prior["run"], "N1-B130-CLAUDE-CONFIRM-003")
        self.assertEqual(len(prior["files"]), 8)


if __name__ == "__main__":
    unittest.main()
