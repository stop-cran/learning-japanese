import copy
import unittest

from verify_b117_round4 import CHOICES, PARENT, POOLS, require_focused


class FocusedRegressionContractTests(unittest.TestCase):
    def setUp(self):
        pool = {
            "curatedCards": CHOICES, "outcomes": 1, "deficits": {"0": 1},
            "reachable": ["ぎん", "ご", "きゅう"], "fallback": {},
            "yuiReachable": False, "seededWitness": None,
            "seedRange": [0, 999], "seedsChecked": 1000,
            "sampledWrongOptions": ["ぎん", "ご", "きゅう"], "invalidSampleSeeds": [],
        }
        self.result = {
            "status": "PASS", "parent": PARENT, "failedPools": [],
            "pools": {name: copy.deepcopy(pool) for name in POOLS},
            "parentPositiveControl": {
                "yuiReachable": True, "curatedCards": [], "deficits": {"3": 1},
                "seededWitness": {"seed": 1, "wrongOptions": ["ゆい", "せい", "いん"]},
            },
            "currentTargetMetadata": {
                "distractors": CHOICES, "onyomi": ["イ"], "kunyomi": [],
                "quizOnyomi": ["イ"], "quizKunyomi": [], "quiz_exclusions": ["索"],
            },
        }

    def test_rejects_missing_pool_or_positive_control(self):
        require_focused(self.result)
        for mutate in (
            lambda r: r["pools"].pop("Starter+target+由"),
            lambda r: r["parentPositiveControl"].update(yuiReachable=False),
            lambda r: r.update(parent="different"),
            lambda r: r["currentTargetMetadata"]["quiz_exclusions"].append("ゆい"),
        ):
            result = copy.deepcopy(self.result)
            mutate(result)
            with self.assertRaises(ValueError):
                require_focused(result)

    def test_rejects_fallback_or_underchecked_pool(self):
        for patch in (
            {"fallback": {"1": ["ゆい"]}}, {"yuiReachable": True},
            {"seedsChecked": 999}, {"deficits": {"1": 1}},
            {"reachable": ["ぎん", "ご", "ゆい"]}, {"invalidSampleSeeds": [2]},
        ):
            with self.subTest(patch=patch):
                result = copy.deepcopy(self.result)
                result["pools"]["Starter+target+由"].update(patch)
                with self.assertRaises(ValueError):
                    require_focused(result)


if __name__ == "__main__":
    unittest.main()
