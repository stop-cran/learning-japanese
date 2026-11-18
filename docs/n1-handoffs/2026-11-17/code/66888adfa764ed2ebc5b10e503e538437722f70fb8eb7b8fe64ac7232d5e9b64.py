"""Focused controls for the derived fresh-context B133 confirmation collector."""
import json
import unittest

import b133_confirmation_records as original_records
import b133_fresh_confirmation_records as fresh_records
from accept_b133_confirmation import initial_binding
from admit_b133_source_reconciliation import INITIALS
from common import frozen, sha
from confirm_b133_fresh import OUT

RUN = "N1-B133-GPT-CONFIRM-002"


def ref(path):
    return {"path": str(path), "sha256": sha(frozen(path))}


def gpt_spec(**extra):
    accepted = OUT / (RUN + "-acceptance.json")
    final = json.loads(frozen(json.loads(frozen(accepted))["final"]["path"]))
    audit = json.loads(frozen(final["audit"]["path"], final["audit"]["sha256"]))
    from pathlib import Path
    events = Path(final["audit"]["path"]).parent / "events.jsonl"
    return {"family": "gpt", "role": "confirmation", "run": RUN, "session": INITIALS["gpt"]["session"],
            "snapshot": final["candidate"], "confirmation": "CONFIRMED", "acceptance": ref(accepted),
            "preflight": ref(OUT / (RUN + "-preflight.json")), "admission": ref(OUT / (RUN + "-admission.json")),
            "events": {"path": str(events), "sha256": audit["eventsSha256"]}, **extra}


class FreshCollectorControls(unittest.TestCase):
    def test_original_collector_still_accepts_original_reviewer(self):
        refs, _, adjudication = original_records.collect_confirmation(gpt_spec(), initial_binding("gpt"), frozen)
        self.assertEqual(adjudication["run"], RUN)
        self.assertNotIn("contextObservation", refs)

    def test_fresh_collector_refuses_original_reviewer_relabelled(self):
        spec = gpt_spec(reviewerOrigin="fresh-context-replacement", originalSession=INITIALS["gpt"]["session"])
        with self.assertRaisesRegex(Exception, "Fresh confirmation must disclose"):
            fresh_records.collect_confirmation(spec, initial_binding("gpt"), frozen)

    def test_fresh_collector_refuses_undisclosed_origin(self):
        spec = gpt_spec(reviewerOrigin="original", originalSession=INITIALS["gpt"]["session"])
        with self.assertRaisesRegex(Exception, "Fresh confirmation must disclose"):
            fresh_records.collect_confirmation(spec, initial_binding("gpt"), frozen)

    def test_fresh_collector_refuses_cross_family_original(self):
        spec = gpt_spec(reviewerOrigin="fresh-context-replacement", originalSession=INITIALS["claude"]["session"],
                        session="00000000-0000-4000-8000-000000000000")
        with self.assertRaisesRegex(Exception, "Fresh confirmation must disclose"):
            fresh_records.collect_confirmation(spec, initial_binding("gpt"), frozen)


if __name__ == "__main__":
    unittest.main(verbosity=2)
