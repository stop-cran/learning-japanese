"""Focused controls for the B133 fresh-context Claude continuation (CONFIRM-003)."""
import json
import unittest

import b133_fresh_confirmation as first
import b133_fresh_confirmation_v2 as second
from admit_b133_source_reconciliation import INITIALS
from common import frozen
from confirm_b133_v2 import OUT

PRIOR = OUT / (first.PLANNED_RUN + "-spec.json")
FRESH = "928ed3cb-7f93-476e-85cb-1b7b6f05f1ef"
NEXT = "1" * 40
SOURCES = [
    {"source": second.PRIOR_REPORT_SOURCE,
     "path": r"C:\Users\stop-\n1-kanji-workspace\reports-133\N1-B133-CLAUDE-CONFIRM-002.md",
     "sha256": "9327ee1d95393fa26bacbadf26099f73a0be0091e1ce30c4fc5388aafaf76bb5"},
    {"source": second.ADJUDICATION_SOURCE, "path": str(second.adjudication_path()),
     "sha256": second.ADJUDICATION_SHA256},
]
RENDERED = ("Header: confirmation of your own adjudicated B133 initial report with open claims.\n"
            "Your own initial report: R\nThe chain contains your own unchanged initial report and more.\n"
            "Read your own full report, including changes not requested by you.\n")


def prior_spec():
    return json.loads(frozen(PRIOR))


def continuation(**extra):
    spec = {**prior_spec(), "run": second.CONTINUATION_RUN, "candidate": NEXT, "additionalSources": SOURCES}
    spec.update(extra)
    return spec


class ContinuationOrigin(unittest.TestCase):
    def test_prior_fresh_confirmation_still_validates_unchanged(self):
        spec = prior_spec()
        self.assertEqual(spec["session"], FRESH)
        self.assertTrue(second.fresh_origin(spec))
        self.assertEqual(second.fresh_bindings(spec), first.fresh_bindings(spec))
        self.assertEqual(second.replacement_prompt(RENDERED, spec), first.replacement_prompt(RENDERED))

    def test_first_module_refuses_the_continuation(self):
        with self.assertRaisesRegex(ValueError, "observed capacity replacement"):
            first.fresh_origin(continuation())

    def test_continuation_in_the_disclosed_session_is_accepted(self):
        spec = continuation()
        self.assertTrue(second.fresh_origin(spec))
        paths = [row["path"] for row in second.fresh_bindings(spec)]
        self.assertIn(str(second.prior_final_path()), paths)
        self.assertIn(str(second.adjudication_path()), paths)

    def test_refusals(self):
        cases = {
            "another fresh session": continuation(session="00000000-0000-4000-8000-000000000000"),
            "original reviewer": continuation(session=INITIALS["claude"]["session"]),
            "later run": continuation(run="N1-B133-CLAUDE-CONFIRM-004"),
            "same snapshot": continuation(candidate=first.CANDIDATE_002),
            "abbreviated snapshot": continuation(candidate="1" * 7),
            "other family": continuation(family="gpt"),
            "other original": continuation(originalSession=INITIALS["gpt"]["session"]),
            "other observation": continuation(contextObservation={**prior_spec()["contextObservation"],
                                                                  "sha256": "0" * 64}),
        }
        for name, spec in cases.items():
            with self.subTest(name), self.assertRaises((ValueError, KeyError)):
                second.fresh_origin(spec)


class ContinuationAttribution(unittest.TestCase):
    def test_truthful_trailer(self):
        text = second.replacement_prompt(RENDERED, continuation())
        self.assertEqual(text.count(second.TRAILER), 1)
        self.assertNotIn("You are a new same-family reviewer", text)
        self.assertIn("that wrote N1-B133-CLAUDE-CONFIRM-002 on " + first.CANDIDATE_002, text)
        self.assertIn(second.ADJUDICATION_SOURCE, text)
        self.assertNotIn("your own", text.lower())

    def test_requires_own_report_and_adjudication(self):
        for dropped in range(len(SOURCES)):
            kept = [row for index, row in enumerate(SOURCES) if index != dropped]
            with self.subTest(dropped), self.assertRaisesRegex(ValueError, "must supply"):
                second.replacement_prompt(RENDERED, continuation(additionalSources=kept))
        altered = [SOURCES[0], {**SOURCES[1], "sha256": "0" * 64}]
        with self.assertRaisesRegex(ValueError, "must supply"):
            second.replacement_prompt(RENDERED, continuation(additionalSources=altered))


class DerivedTools(unittest.TestCase):
    def test_controller_validates_continuation_and_prior(self):
        import confirm_b133_fresh_v2 as controller
        self.assertEqual(controller.validate_spec(continuation()), "claude")
        self.assertEqual(controller.validate_spec(prior_spec()), "claude")
        with self.assertRaises(ValueError):
            controller.validate_spec(continuation(session=INITIALS["claude"]["session"]))

    def test_controller_render_passes_spec(self):
        import inspect
        import confirm_b133_fresh_v2 as controller
        self.assertIn("prompt_path), spec)", inspect.getsource(controller.render))
        self.assertIs(controller.replacement_prompt, second.replacement_prompt)

    def test_collector_and_acceptor_use_continuation_origin(self):
        import accept_b133_fresh_confirmation_v2 as acceptor
        import b133_fresh_confirmation_records_v2 as records
        self.assertIs(records.fresh_origin, second.fresh_origin)
        self.assertIs(acceptor.collect_confirmation, records.collect_confirmation)
        self.assertEqual(acceptor.REASON, first.REASON)


if __name__ == "__main__":
    unittest.main(verbosity=2)
