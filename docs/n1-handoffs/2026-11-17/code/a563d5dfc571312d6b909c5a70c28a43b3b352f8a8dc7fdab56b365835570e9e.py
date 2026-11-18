import copy
import unittest

from common import TOOLS, load_module

v4 = load_module("build_prompts_v4", TOOLS / "build-prompts-v4.py")

QUARANTINE = {"run": "N1-B9-GPT-001", "status": "VOID_COORDINATOR_PHASE2_DELIVERY_MISMATCH",
              "reviewAccepted": False, "publicationAccepted": False, "candidate": "abc"}
AUTH = {"family": "gpt", "attempt": 2, "candidate": "abc", "userAuthorization": [{"content": "x"}],
        "predecessor": {"run": "N1-B9-GPT-001", "sha256": "q"}}


def check(quarantine=QUARANTINE, auth=AUTH, quarantine_sha="q", candidate="abc", previous="N1-B9-GPT-001",
          key="gpt", attempt=2):
    v4.check_predecessor(quarantine, auth, quarantine_sha, candidate, previous, key, attempt)


def changed(base, **values):
    out = copy.deepcopy(base)
    out.update(values)
    return out


class PredecessorGateTests(unittest.TestCase):
    def test_accepts_bound_void_quarantine(self):
        check()

    def test_rejects_non_void_or_accepted_predecessor(self):
        for quarantine in (changed(QUARANTINE, status="HOLD_STRUCTURE_FAILED"),
                           changed(QUARANTINE, reviewAccepted=True),
                           changed(QUARANTINE, publicationAccepted=None),
                           changed(QUARANTINE, candidate="other"),
                           changed(QUARANTINE, run="N1-B9-GPT-002")):
            with self.subTest(quarantine=quarantine), self.assertRaises(ValueError):
                check(quarantine=quarantine)

    def test_rejects_authorization_not_bound_to_this_attempt(self):
        for auth in (changed(AUTH, predecessor={"run": "N1-B9-GPT-001", "sha256": "other"}),
                     changed(AUTH, family="claude"), changed(AUTH, attempt=3), changed(AUTH, candidate="other"),
                     changed(AUTH, userAuthorization=[])):
            with self.subTest(auth=auth), self.assertRaises(ValueError):
                check(auth=auth)


if __name__ == "__main__":
    unittest.main()
