"""Regression tests for the grammar exercise authoring format."""
import copy
from collections import Counter
import json
import tempfile
import unittest
from pathlib import Path

from validate_grammar import check_grammar


VALID = {
    "schemaVersion": 1,
    "id": "sample-set",
    "title": "Sample",
    "article": "articles/sample.md",
    "constructions": [{"id": "alpha", "label": "甲"}, {"id": "beta", "label": "乙"}],
    "relationships": [{"id": "alpha-vs-beta", "label": "contrast", "constructions": ["alpha", "beta"]}],
    "exercises": [
        {
            "id": "alpha-example", "target": "alpha", "relationship": "alpha-vs-beta", "prompt": "A ____.", "translation": "A.",
            "evidence": "Context.", "explanation": "Reason.", "answer": "alpha", "acceptedAnswers": ["甲"],
            "options": [{"id": "alpha", "label": "甲", "rationale": "Fits."}, {"id": "beta", "label": "乙", "rationale": "Does not fit."}],
        },
        {
            "id": "beta-example", "target": "beta", "relationship": "alpha-vs-beta", "prompt": "B ____.", "translation": "B.",
            "evidence": "Context.", "explanation": "Reason.", "answer": "beta", "acceptedAnswers": ["乙"],
            "options": [{"id": "alpha", "label": "甲", "rationale": "Does not fit."}, {"id": "beta", "label": "乙", "rationale": "Fits."}],
        },
    ],
}


class GrammarValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "grammar").mkdir()
        (self.root / "articles").mkdir()
        (self.root / "articles" / "sample.md").write_text("# Sample\n", encoding="utf-8")

    def check(self, mutate=None):
        data = copy.deepcopy(VALID)
        if mutate:
            mutate(data)
        (self.root / "grammar" / "sample-set.json").write_text(json.dumps(data), encoding="utf-8")
        problems = []
        count = check_grammar(lambda path, message: problems.append(message), self.root)
        return count, problems

    def test_valid_set(self):
        count, problems = self.check()
        self.assertEqual(1, count)
        self.assertEqual([], problems)

    def test_rejects_incomplete_relationship_coverage(self):
        _, problems = self.check(lambda data: data["exercises"].pop())
        self.assertTrue(any("every construction" in message for message in problems), problems)

    def test_rejects_multiple_blanks_and_missing_alternative_rationale(self):
        def mutate(data):
            data["exercises"][0]["prompt"] = "A ____ and ____."
            data["exercises"][0]["options"][1]["rationale"] = ""
        _, problems = self.check(mutate)
        self.assertTrue(any("exactly one" in message for message in problems), problems)
        self.assertTrue(any("rationale" in message for message in problems), problems)

    def test_rejects_missing_article(self):
        (self.root / "articles" / "sample.md").unlink()
        _, problems = self.check()
        self.assertTrue(any("does not exist" in message for message in problems), problems)

    def test_malformed_nested_values_report_errors_instead_of_crashing(self):
        def mutate(data):
            data["relationships"][0]["constructions"] = [["not", "an", "id"]]
            data["exercises"][0]["target"] = []
            data["exercises"][0]["options"][0]["id"] = {}
        _, problems = self.check(mutate)
        self.assertTrue(problems)

    def test_rejects_distractor_that_is_an_accepted_equivalent(self):
        def mutate(data):
            data["exercises"][0]["acceptedAnswers"].append("乙")
        _, problems = self.check(mutate)
        self.assertTrue(any("distractor label" in message for message in problems), problems)

    def test_rejects_normalized_answer_collision(self):
        def mutate(data):
            data["exercises"][0]["acceptedAnswers"].append(" Ａ ")
            data["exercises"][0]["options"][1]["label"] = "A"
        _, problems = self.check(mutate)
        self.assertTrue(any("distractor label" in message for message in problems), problems)

    def test_rejects_normalized_duplicate_option_labels(self):
        def mutate(data):
            data["exercises"][0]["options"][0]["label"] = "Ａ"
            data["exercises"][0]["options"][1]["label"] = " A "
            data["exercises"][0]["acceptedAnswers"] = ["Ａ"]
        _, problems = self.check(mutate)
        self.assertTrue(any("option labels must remain distinct" in message for message in problems), problems)


class GrammarFoundationsCoverageTests(unittest.TestCase):
    def test_foundations_has_three_examples_per_function(self):
        root = Path(__file__).resolve().parent.parent
        data = json.loads((root / "grammar" / "formal-nouns-foundations.json").read_text(encoding="utf-8"))
        counts = Counter(exercise["target"] for exercise in data["exercises"])
        expected = {
            "koto-activity", "no-perception", "koto-no-need", "wake-constraint",
            "inferred-impossibility", "non-necessary-inference",
        }
        self.assertEqual(expected, set(counts))
        self.assertTrue(all(count >= 3 for count in counts.values()), counts)
        self.assertTrue(any("行かない____" in exercise["prompt"] for exercise in data["exercises"]))

    def test_pilot_exercise_identities_are_retained(self):
        root = Path(__file__).resolve().parent.parent
        data = json.loads((root / "grammar" / "formal-nouns-pilot.json").read_text(encoding="utf-8"))
        identities = {
            exercise["id"]: (exercise["target"], exercise["relationship"])
            for exercise in data["exercises"]
        }
        self.assertEqual({
            "koto-work-hours-fact": ("koto", "koto-vs-wake"),
            "koto-entry-rule": ("koto", "koto-vs-wake"),
            "wake-impossible-arrival": ("wake", "koto-vs-wake"),
            "wake-realization": ("wake", "koto-vs-wake"),
            "hazu-shipping-estimate": ("hazu", "hazu-vs-beki"),
            "hazu-scheduled-arrival": ("hazu", "hazu-vs-beki"),
            "beki-safety-report": ("beki", "hazu-vs-beki"),
            "beki-public-conduct": ("beki", "hazu-vs-beki"),
        }, identities)


class GrammarActionsCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-actions.json").read_text(encoding="utf-8"))

    def test_actions_has_three_examples_per_pattern(self):
        counts = Counter(exercise["target"] for exercise in self.data["exercises"])
        self.assertEqual({
            "koto-ability", "koto-occurrence", "koto-self-decision", "koto-outcome",
        }, set(counts))
        self.assertTrue(all(count >= 3 for count in counts.values()), counts)

    def test_occurrence_includes_experience_and_nonpast_events(self):
        exercises = {
            exercise["id"]: exercise for exercise in self.data["exercises"]
            if exercise["target"] == "koto-occurrence"
        }
        self.assertIn("見たこと____", exercises["koto-experience-drift-ice"]["prompt"])
        self.assertIn("見たこと____", exercises["koto-experience-noh-theater"]["prompt"])
        self.assertIn("食べること____", exercises["koto-occurrence-lunch-out"]["prompt"])

    def test_actions_keep_supplied_stems_out_of_typed_answers(self):
        for exercise in self.data["exercises"]:
            self.assertTrue(
                "こと____" in exercise["prompt"] or "ことに____" in exercise["prompt"],
                exercise["id"],
            )
            for answer in exercise["acceptedAnswers"]:
                self.assertNotIn("こと", answer, exercise["id"])

    def test_transfer_accepts_established_arrangement(self):
        exercise = next(
            item for item in self.data["exercises"] if item["id"] == "koto-outcome-branch-transfer"
        )
        self.assertTrue(
            {"なった", "なりました", "なっている", "なっています"} <= set(exercise["acceptedAnswers"])
        )


class GrammarIntentCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        data = json.loads((root / "grammar" / "formal-nouns-intent.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in data["exercises"]}

    def test_intent_has_three_examples_per_function(self):
        counts = Counter(exercise["target"] for exercise in self.exercises.values())
        self.assertEqual({
            "intended-meaning", "reasoned-inference", "normative-judgment",
        }, set(counts))
        self.assertTrue(all(count >= 3 for count in counts.values()), counts)

    def test_inference_items_preserve_noun_attachment_and_equivalents(self):
        for exercise in self.exercises.values():
            if exercise["target"] == "reasoned-inference":
                self.assertIn("の____だ", exercise["prompt"])
                self.assertTrue(
                    {"はず", "筈", "よう", "様"} <= set(exercise["acceptedAnswers"]),
                    exercise["id"],
                )

    def test_normative_forms_cover_past_and_negative_contexts(self):
        past = self.exercises["judgment-checking-station-exit"]
        negative = self.exercises["judgment-permission-before-publishing"]
        self.assertIn("確かめておく____だった", past["prompt"])
        self.assertIn("べき", past["acceptedAnswers"])
        self.assertIn("____ではない", negative["prompt"])
        self.assertTrue({"べき", "もの", "もん"} <= set(negative["acceptedAnswers"]))

    def test_normative_contexts_accept_no_and_n(self):
        for exercise in self.exercises.values():
            if exercise["target"] == "normative-judgment":
                self.assertTrue({"の", "ん"} <= set(exercise["acceptedAnswers"]), exercise["id"])


class GrammarStagesCoverageTests(unittest.TestCase):
    FORMS = {
        "lunch": (
            ("食べる", "たべる"),
            ("食べている", "たべている", "食べてる", "たべてる"),
            ("食べた", "たべた"),
        ),
        "letter": (
            ("書く", "かく"),
            ("書いている", "かいている", "書いてる", "かいてる"),
            ("書いた", "かいた"),
        ),
        "novel": (
            ("読む", "よむ"),
            ("読んでいる", "よんでいる", "読んでる", "よんでる"),
            ("読んだ", "よんだ"),
        ),
    }
    STAGES = ("before", "during", "after")

    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        data = json.loads((root / "grammar" / "formal-nouns-stages.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in data["exercises"]}

    def test_each_lexical_frame_covers_every_stage(self):
        self.assertEqual(
            {f"tokoro-{stage}-{frame}" for stage in self.STAGES for frame in self.FORMS},
            set(self.exercises),
        )
        counts = Counter(exercise["target"] for exercise in self.exercises.values())
        self.assertEqual({f"tokoro-{stage}": 3 for stage in self.STAGES}, counts)
        directions = Counter(
            (exercise["target"], option["id"])
            for exercise in self.exercises.values()
            for option in exercise["options"]
            if option["id"] != exercise["target"]
        )
        self.assertEqual({
            (f"tokoro-{target}", f"tokoro-{other}"): 3
            for target in self.STAGES for other in self.STAGES if target != other
        }, directions)

    def test_answers_are_exact_missing_forms_with_kana_and_contractions(self):
        for frame, forms in self.FORMS.items():
            for stage, answers in zip(self.STAGES, forms):
                exercise = self.exercises[f"tokoro-{stage}-{frame}"]
                self.assertEqual(f"tokoro-{stage}", exercise["target"], exercise["id"])
                self.assertIn("____ところです", exercise["prompt"], exercise["id"])
                self.assertEqual(set(answers), set(exercise["acceptedAnswers"]), exercise["id"])

    def test_controlled_form_instruction_is_visible_in_each_question(self):
        for frame, forms in self.FORMS.items():
            for stage in self.STAGES:
                exercise = self.exercises[f"tokoro-{stage}-{frame}"]
                self.assertIn(f"Use {forms[0][0]}", exercise["translation"], exercise["id"])
                self.assertIn(
                    "dictionary, ている or た form; contractions accepted.",
                    exercise["translation"],
                    exercise["id"],
                )


if __name__ == "__main__":
    unittest.main()
