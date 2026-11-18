"""Exact boundary controls for the original retained-continuation profiles."""
import copy
import json
import sys
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).parent
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
import b134_revision_confirmation_v2 as v2
from common import freeze_json, sha


class Boundaries(unittest.TestCase):
    def test_exact_family_boundaries(self):
        for family, expected in v2.EXPECTED.items():
            session = v2.legacy.OWN[family]
            input_tokens = expected["prePhase2Gate"] - 49000 - 1000
            events = [
                {"type": "session.start", "data": {"sessionId": session,
                  "selectedModel": expected["selectedModel"], "contextTier": "long_context"}},
                {"type": "session.usage_record", "data": {"usage": {
                  "model": expected["selectedModel"], "responseModel": expected["selectedModel"],
                  "inputTokens": input_tokens, "maxPromptTokens": expected["maxPromptTokens"]}}}]
            with self.subTest(family=family, boundary="exact"):
                result = v2.context(events, family, session, 1000)
                self.assertEqual(result["forecast"], result["limit"])
                self.assertEqual(result["originalStartupGateUnchanged"], 700000)
            events[1]["data"]["usage"]["inputTokens"] += 1
            with self.subTest(family=family, boundary="one-over"), self.assertRaises(ValueError):
                v2.context(events, family, session, 1000)

    def test_unknown_family_and_unpinned_profiles_rejected(self):
        with self.assertRaises(ValueError):
            v2.continuation_profile("unknown")
        _, _, capacity, _ = v2.legacy.modules()
        for family in v2.EXPECTED:
            changed = copy.deepcopy(capacity.PROFILES)
            changed[family]["prePhase2Gate"] += 1
            with self.subTest(family=family), patch.object(capacity, "PROFILES", changed), self.assertRaises(ValueError):
                v2.continuation_profile(family)
        with patch.object(v2, "PREFLIGHT_SHA", "0"*64), self.assertRaises(ValueError):
            v2.continuation_profile("claude")


if __name__ == "__main__":
    result = unittest.main(verbosity=2, exit=False).result
    if not result.wasSuccessful():
        raise SystemExit(1)
    print(json.dumps(freeze_json(HERE / ("continuation-controls-" + uuid.uuid4().hex + ".json"), {
        "testsRun": result.testsRun, "syntheticBoundaryControlsOnly": True,
        "tools": {name: sha((Path(v2.__file__).parent / name).read_bytes())
                  for name in ("b134_revision_confirmation_v2.py", "b134_revision_proofs_v1.py")},
        "preservedV1Sha256": v2.V1_SHA, "originalPreflightSha256": v2.PREFLIGHT_SHA})))
