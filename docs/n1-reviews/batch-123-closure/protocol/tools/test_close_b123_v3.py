import unittest

from close_b123_v3 import ORIGINAL, REPLACEMENT_ORIGIN, confirmation_origin

REPLACED = "N1-B123-CLAUDE-CONFIRM-004"
PREVIOUS = "N1-B123-CLAUDE-CONFIRM-002"
INITIAL = "N1-B123-CLAUDE-001"


class ConfirmationOriginTests(unittest.TestCase):
    def call(self, spec, accepted, *, kind="final", family="claude", batch=123, session="fresh",
             verified=(INITIAL, PREVIOUS)):
        calls = []

        def verify(item):
            calls.append(item)
            return {"run": verified[0]}, {"run": verified[1]}, b"report"

        result = confirmation_origin(
            spec, {"session": session}, {"session": "original"}, accepted, INITIAL, kind=kind,
            family=family, batch=batch, previous=PREVIOUS, verify=verify,
            load=lambda item: {"run": REPLACED, "session": "original"}, prefix="runs/X")
        return result, calls

    def replacement(self):
        spec = {"session": "fresh", "replayedFrom": {"path": "s"}, "unavailable": {"path": "u"}}
        accepted = {"reviewerOrigin": REPLACEMENT_ORIGIN, "replacesUnavailable": REPLACED}
        return spec, accepted

    def test_original_reviewer_keeps_original_attribution(self):
        result, calls = self.call({"session": "original"}, {}, session="original")
        self.assertEqual(result, ORIGINAL)
        self.assertEqual(calls, [])
        for spec, accepted, session in (({"session": "other"}, {}, "other"),
                                        ({"session": "original"}, {}, "other"),
                                        ({"session": "original"}, {"reviewerOrigin": REPLACEMENT_ORIGIN},
                                         "original")):
            with self.subTest(spec=spec, accepted=accepted), self.assertRaises(ValueError):
                self.call(spec, accepted, session=session)

    def test_proven_replacement_is_attributed_and_never_original(self):
        spec, accepted = self.replacement()
        result, calls = self.call(spec, accepted)
        self.assertEqual(calls, [spec])
        self.assertEqual(result, {"reviewerOrigin": REPLACEMENT_ORIGIN, "replacementFor": REPLACED,
                                  "replayedFrom": "runs/X/replayed-from-spec.json",
                                  "originalSession": "original"})

    def test_rejects_unscoped_unproven_or_misattributed_replacements(self):
        spec, accepted = self.replacement()
        cases = [
            dict(kind="intermediate"), dict(family="gpt"), dict(batch=124),
            dict(session="original"), dict(verified=("other", PREVIOUS)), dict(verified=(INITIAL, "other")),
        ]
        for options in cases:
            same = {**spec, "session": options["session"]} if "session" in options else spec
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.call(same, accepted, **options)
        for broken in ({**accepted, "reviewerOrigin": "original"},
                       {**accepted, "replacesUnavailable": "N1-B123-CLAUDE-CONFIRM-003"}):
            with self.subTest(accepted=broken), self.assertRaises(ValueError):
                self.call(spec, broken)
        partial = {key: value for key, value in spec.items() if key != "unavailable"}
        with self.assertRaises(ValueError):
            self.call(partial, accepted)


if __name__ == "__main__":
    unittest.main()
