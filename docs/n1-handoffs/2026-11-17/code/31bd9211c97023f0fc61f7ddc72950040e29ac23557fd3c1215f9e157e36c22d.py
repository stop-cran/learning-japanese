import json
import unittest

from prepare_b130_confirmations import FAMILIES, PREFIX, REPO, neutral, pair_lines


class B130ConfirmationIsolationTests(unittest.TestCase):
    def test_actual_complete_pair_presentation_roundtrips_all_fields(self):
        raw = (REPO / PREFIX / "pair-dispositions-001.json").read_bytes()
        lines = [json.loads(line) for line in pair_lines(raw).splitlines()]
        self.assertEqual(json.loads(raw), {**lines[0], "rows": lines[1:]})
        self.assertEqual(29, len(lines))
        self.assertTrue(neutral(pair_lines(raw)))

    def test_actual_family_responses_do_not_cross_the_isolation_boundary(self):
        for family, opposite in (("claude", "gpt"), ("gpt", "claude")):
            own_packet = []
            for kind, suffix in (("response", "md"), ("mapping", "json")):
                raw = (REPO / PREFIX / "responses" / f"{family}-{kind}-001.{suffix}").read_bytes()
                self.assertIsNone(FAMILIES[opposite].search(raw.decode()))
                own_packet.append(raw)
            self.assertFalse(neutral(b"\n".join(own_packet)))
        self.assertFalse(neutral(b"the GPT review"))
        self.assertFalse(neutral(b"Claude's findings"))


if __name__ == "__main__":
    unittest.main()
