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


class GrammarStatesCoverageTests(unittest.TestCase):
    FORMS = {
        "window": ("開ける", ("開けた", "あけた"), ("開けない", "あけない")),
        "lights": ("消す", ("消した", "けした"), ("消さない", "けさない")),
        "bags": ("持つ", ("持った", "もった"), ("持たない", "もたない")),
    }
    TARGETS = ("mama-result", "mama-undone")

    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        data = json.loads((root / "grammar" / "formal-nouns-states.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in data["exercises"]}

    def test_three_paired_examples_in_both_directions(self):
        self.assertEqual(
            {f"{target}-{frame}" for target in self.TARGETS for frame in self.FORMS},
            set(self.exercises),
        )
        counts = Counter(exercise["target"] for exercise in self.exercises.values())
        self.assertEqual({target: 3 for target in self.TARGETS}, counts)
        for exercise in self.exercises.values():
            self.assertEqual("mama-result-vs-undone", exercise["relationship"], exercise["id"])
            self.assertEqual(
                set(self.TARGETS), {option["id"] for option in exercise["options"]}, exercise["id"],
            )

    def test_answers_preserve_polarity_and_exclude_supplied_mama(self):
        for frame, (_, result, undone) in self.FORMS.items():
            for target, answers in zip(self.TARGETS, (result, undone)):
                exercise = self.exercises[f"{target}-{frame}"]
                self.assertEqual(target, exercise["target"], exercise["id"])
                self.assertIn("____まま", exercise["prompt"], exercise["id"])
                self.assertEqual(set(answers), set(exercise["acceptedAnswers"]), exercise["id"])

    def test_question_supplies_verb_and_form_limit(self):
        for frame, (verb, _, _) in self.FORMS.items():
            for target in self.TARGETS:
                exercise = self.exercises[f"{target}-{frame}"]
                self.assertIn(f"Use {verb} (", exercise["translation"], exercise["id"])
                self.assertIn("た or ない form only.", exercise["translation"], exercise["id"])


class GrammarBeforeAfterCoverageTests(unittest.TestCase):
    FORMS = {
        "mae-snack-cleaning": {"食べるまえ", "食べる前", "たべるまえ", "たべる前"},
        "ato-snack-cleaning": {"食べたあと", "食べた後", "たべたあと", "たべた後"},
        "mae-departure-call": {"出るまえ", "出る前", "でるまえ", "でる前"},
        "ato-departure-call": {"出たあと", "出た後", "でたあと", "でた後"},
        "mae-class-library": {"まえ", "前"},
        "ato-class-library": {"あと", "後"},
    }
    TARGETS = {"mae": "mae-before-event", "ato": "ato-after-event"}

    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        data = json.loads((root / "grammar" / "formal-nouns-before-after.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in data["exercises"]}

    def test_three_paired_examples_per_target(self):
        self.assertEqual(set(self.FORMS), set(self.exercises))
        counts = Counter(exercise["target"] for exercise in self.exercises.values())
        self.assertEqual({target: 3 for target in self.TARGETS.values()}, counts)
        for identifier, exercise in self.exercises.items():
            self.assertEqual(self.TARGETS[identifier.split("-")[0]], exercise["target"], identifier)
            self.assertEqual("before-vs-after", exercise["relationship"], identifier)
            self.assertEqual(
                set(self.TARGETS.values()), {option["id"] for option in exercise["options"]}, identifier,
            )

    def test_exact_blank_spans_accept_kana_and_kanji(self):
        for identifier, answers in self.FORMS.items():
            exercise = self.exercises[identifier]
            self.assertIn("____に", exercise["prompt"], identifier)
            self.assertEqual(answers, set(exercise["acceptedAnswers"]), identifier)

    def test_past_future_and_noun_contexts_are_retained(self):
        self.assertIn("昨日", self.exercises["mae-snack-cleaning"]["prompt"])
        self.assertIn("明日", self.exercises["ato-departure-call"]["prompt"])
        for prefix in self.TARGETS:
            self.assertIn("授業の____に", self.exercises[f"{prefix}-class-library"]["prompt"])

    def test_controlled_instruction_remains_question_visible(self):
        for identifier, exercise in self.exercises.items():
            if identifier.endswith("class-library"):
                instruction = "Use まえ or あと; の and に are already printed."
            else:
                verb = "食べる" if identifier.endswith("snack-cleaning") else "出る"
                self.assertIn(f"Use the dictionary or た form of {verb}", exercise["translation"], identifier)
                instruction = "+ まえ or あと; に is already printed."
            self.assertIn(instruction, exercise["translation"], identifier)


class GrammarTimeCoverageTests(unittest.TestCase):
    TARGET_COUNTS = {
        "uchi-before-change": 3,
        "uchi-change-during": 3,
        "aida-duration-topic": 3,
        "aida-event-within": 3,
        "toki-reference": 3,
        "koro-approximate": 3,
        "tabi-each-occasion": 3,
        "occasion-reference": 6,
    }
    UCHI_FORMS = {
        "uchi-before-rain-laundry": ("降る", {"降らない", "ふらない"}),
        "uchi-before-forgetting-number": ("忘れる", {"忘れない", "わすれない"}),
        "uchi-before-shop-crowds": ("混む", {"混まない", "込まない", "こまない"}),
        "uchi-during-reading-interest": ("読む", {"読んでいる", "よんでいる", "読んでる", "よんでる"}),
        "uchi-during-conversation-relaxing": ("話す", {"話している", "はなしている", "話してる", "はなしてる"}),
        "uchi-during-walking-familiarity": ("歩く", {"歩いている", "あるいている", "歩いてる", "あるいてる"}),
    }

    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent
        self.data = json.loads((self.root / "grammar" / "formal-nouns-time.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_target_counts_and_relationship_directions(self):
        counts = Counter(exercise["target"] for exercise in self.exercises.values())
        self.assertEqual(self.TARGET_COUNTS, counts)
        self.assertEqual(27, len(self.data["exercises"]))
        relationships = {
            relationship["id"]: set(relationship["constructions"])
            for relationship in self.data["relationships"]
        }
        self.assertEqual(4, len(relationships))
        for exercise in self.exercises.values():
            self.assertEqual(
                relationships[exercise["relationship"]],
                {option["id"] for option in exercise["options"]},
                exercise["id"],
            )

    def test_uchi_exact_forms_and_visible_restriction(self):
        for identifier, (verb, answers) in self.UCHI_FORMS.items():
            exercise = self.exercises[identifier]
            self.assertIn("____うちに", exercise["prompt"], identifier)
            self.assertEqual(answers, set(exercise["acceptedAnswers"]), identifier)
            self.assertIn(f"Use {verb} (", exercise["translation"], identifier)
            self.assertIn(
                "in its ない or ている form only; contractions accepted.",
                exercise["translation"],
                identifier,
            )

    def test_aida_pairs_include_particles_and_question_side_framing(self):
        frames = (("meeting-wait", "meeting-call"), ("nap-quiet", "nap-parcel"), ("train-seated", "train-message"))
        expected = {
            f"aida-{kind}-{frame}"
            for pair in frames
            for kind, frame in zip(("topic", "within"), pair)
        }
        actual = {identifier for identifier in self.exercises if identifier.startswith("aida-")}
        self.assertEqual(expected, actual)
        for identifier in expected:
            exercise = self.exercises[identifier]
            topic = exercise["target"] == "aida-duration-topic"
            self.assertEqual(
                {"あいだは", "間は"} if topic else {"あいだに", "間に"},
                set(exercise["acceptedAnswers"]),
                identifier,
            )
            self.assertIn("____、", exercise["prompt"], identifier)
            self.assertIn("Use あいだは or あいだに only.", exercise["translation"], identifier)
            self.assertIn(
                "a topic for" if topic else "not an interval-as-topic construction",
                exercise["translation"],
                identifier,
            )

    def test_toki_koro_spellings_and_non_duration_shortcut_cases(self):
        for exercise in self.exercises.values():
            if exercise["target"] not in {"toki-reference", "koro-approximate"}:
                continue
            approximate = exercise["target"] == "koro-approximate"
            self.assertEqual(
                {"ころ", "頃"} if approximate else {"とき", "時"},
                set(exercise["acceptedAnswers"]),
                exercise["id"],
            )
            self.assertIn("Use とき or ころ only.", exercise["translation"], exercise["id"])
            self.assertIn(
                "Explicitly" if approximate else "without",
                exercise["translation"],
                exercise["id"],
            )
        self.assertIn("四年間ずっと", self.exercises["toki-student-years"]["prompt"])
        self.assertIn("少し前", self.exercises["koro-arrival-rain"]["prompt"])
        self.assertIn("少しあと", self.exercises["koro-arrival-rain"]["prompt"])
        self.assertIn("静かな____", self.exercises["toki-quiet-reading"]["prompt"])

    def test_occasion_equivalents_share_one_option_and_keep_quantification_visible(self):
        models = Counter()
        for exercise in self.exercises.values():
            if exercise["relationship"] != "occasion-vs-each-time":
                continue
            self.assertIn(
                "Use one noun from たび／とき／おり／さい, in kana or kanji.",
                exercise["translation"],
                exercise["id"],
            )
            self.assertIn("____に", exercise["prompt"], exercise["id"])
            self.assertIn("explicitly", exercise["translation"].lower(), exercise["id"])
            if exercise["target"] == "occasion-reference":
                self.assertEqual(
                    {"とき", "時", "おり", "折", "さい", "際"},
                    set(exercise["acceptedAnswers"]),
                    exercise["id"],
                )
                self.assertIn("neutral and formal wording are both accepted", exercise["translation"])
                correct = next(option for option in exercise["options"] if option["id"] == exercise["answer"])
                models[correct["label"]] += 1
            else:
                self.assertEqual({"たび", "度"}, set(exercise["acceptedAnswers"]), exercise["id"])
        self.assertEqual({"おり": 3, "さい": 3}, models)

    def test_source_record_covers_the_actual_targets(self):
        sources = json.loads((self.root / "docs" / "grammar-time-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(self.data["id"], sources["setId"])
        self.assertEqual(self.data["article"], sources["article"])
        self.assertEqual(
            set(self.TARGET_COUNTS),
            {target for source in sources["sources"] for target in source["supports"]},
        )


class GrammarCausesCoverageTests(unittest.TestCase):
    TARGET_COUNTS = {
        "tame-purpose": 3, "tame-cause": 6, "okage-credit": 3, "sei-blame": 3,
        "kawari-substitution": 3, "tsuide-secondary": 3, "kawari-tradeoff": 3,
    }
    TAME_FORMS = {
        "printer": ("買う", {"買う", "かう"}, {"買った", "かった"}),
        "moving": (
            "引っ越す",
            {"引っ越す", "引越す", "引っこす", "ひっこす"},
            {"引っ越した", "引越した", "引っこした", "ひっこした"},
        ),
        "seminar": ("参加する", {"参加する", "さんかする"}, {"参加した", "さんかした"}),
    }
    KAWARI_SPELLINGS = {"かわり", "代わり", "代り", "替わり", "替り"}

    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent
        self.data = json.loads((self.root / "grammar" / "formal-nouns-causes.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_target_counts_and_relationship_directions(self):
        self.assertEqual(24, len(self.data["exercises"]))
        self.assertEqual(
            self.TARGET_COUNTS,
            Counter(exercise["target"] for exercise in self.exercises.values()),
        )
        relationships = {
            relationship["id"]: set(relationship["constructions"])
            for relationship in self.data["relationships"]
        }
        self.assertEqual(4, len(relationships))
        for exercise in self.exercises.values():
            self.assertEqual(
                relationships[exercise["relationship"]],
                {option["id"] for option in exercise["options"]},
                exercise["id"],
            )

    def test_tame_goal_and_realized_cause_keep_exact_verb_spans(self):
        for frame, (verb, purpose, cause) in self.TAME_FORMS.items():
            for kind, answers in (("purpose", purpose), ("cause", cause)):
                identifier = f"tame-{kind}-{frame}"
                exercise = self.exercises[identifier]
                self.assertEqual(f"tame-{kind}", exercise["target"], identifier)
                self.assertIn("____ために", exercise["prompt"], identifier)
                self.assertEqual(answers, set(exercise["acceptedAnswers"]), identifier)
                self.assertIn(f"Use {verb} (", exercise["translation"], identifier)
                self.assertIn("in dictionary or た form only", exercise["translation"], identifier)
        past_preparation = self.exercises["tame-purpose-seminar"]
        self.assertIn("来週", past_preparation["prompt"])
        self.assertIn("昨日", past_preparation["prompt"])
        self.assertIn("参加する", past_preparation["acceptedAnswers"])

    def test_credit_blame_accept_spellings_and_exclude_sarcasm_visibly(self):
        for exercise in self.exercises.values():
            if exercise["relationship"] != "credit-vs-blame":
                continue
            credit = exercise["target"] == "okage-credit"
            self.assertEqual(
                {"おかげ", "お陰", "お蔭", "御陰", "御蔭"} if credit else {"せい", "所為"},
                set(exercise["acceptedAnswers"]),
                exercise["id"],
            )
            self.assertIn("____で", exercise["prompt"], exercise["id"])
            self.assertIn(
                "Use おかげ or せい, in kana or kanji, literally and without sarcasm.",
                exercise["translation"],
                exercise["id"],
            )
        self.assertIn("雨の____で", self.exercises["okage-rain-flowers"]["prompt"])
        self.assertIn("雨の____で", self.exercises["sei-rain-concert"]["prompt"])
        self.assertIn("静かな____で", self.exercises["okage-quiet-room"]["prompt"])
        self.assertIn("うるさい____で", self.exercises["sei-noisy-room"]["prompt"])
        self.assertIn("忘れた____で", self.exercises["sei-forgotten-room-key"]["prompt"])

    def test_substitution_and_secondary_errands_keep_noun_and_verb_frames(self):
        for exercise in self.exercises.values():
            if exercise["relationship"] != "substitution-vs-secondary":
                continue
            substitution = exercise["target"] == "kawari-substitution"
            self.assertEqual(
                self.KAWARI_SPELLINGS if substitution else {"ついで", "序で", "序"},
                set(exercise["acceptedAnswers"]),
                exercise["id"],
            )
            self.assertIn("____に", exercise["prompt"], exercise["id"])
            self.assertIn(
                "Use かわり or ついで, in kana or kanji; に is already printed.",
                exercise["translation"],
                exercise["id"],
            )
        self.assertIn("買い物の____に", self.exercises["tsuide-shopping-post-office"]["prompt"])
        self.assertIn("返した____に", self.exercises["tsuide-library-card"]["prompt"])
        self.assertIn("散歩する____に", self.exercises["tsuide-walk-letter"]["prompt"])
        self.assertIn("not as payment or an exchange", self.exercises["tsuide-library-card"]["translation"])
        self.assertIn("田中さんの____に", self.exercises["kawari-colleague-meeting"]["prompt"])

    def test_cause_and_tradeoff_frames_preserve_present_adjective_causes(self):
        for frame in ("high-rent", "quiet-location", "infrequent-bus"):
            for target, answers in (("tame-cause", {"ため", "為"}), ("kawari-tradeoff", self.KAWARI_SPELLINGS)):
                identifier = f"{target}-{frame}"
                exercise = self.exercises[identifier]
                self.assertEqual(target, exercise["target"], identifier)
                self.assertEqual(answers, set(exercise["acceptedAnswers"]), identifier)
                self.assertIn(
                    "Use ため or かわり, in kana or kanji; に is already printed.",
                    exercise["translation"],
                    identifier,
                )
                self.assertIn(
                    "State a cause" if target == "tame-cause" else "without claiming",
                    exercise["translation"],
                    identifier,
                )
        self.assertIn("高い____に", self.exercises["tame-cause-high-rent"]["prompt"])
        self.assertIn("静かな____に", self.exercises["tame-cause-quiet-location"]["prompt"])
        self.assertIn("よく眠れます", self.exercises["tame-cause-quiet-location"]["prompt"])

    def test_sources_cover_all_declared_targets(self):
        sources = json.loads((self.root / "docs" / "grammar-causes-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(self.data["id"], sources["setId"])
        self.assertEqual(self.data["article"], sources["article"])
        self.assertEqual(
            set(self.TARGET_COUNTS),
            {target for source in sources["sources"] for target in source["supports"]},
        )


class GrammarConditionsCoverageTests(unittest.TestCase):
    TARGETS = {
        "kagiri-evidence-scope", "baai-case",
        "kagiri-maintained-condition", "kagiri-negative-condition",
    }
    VERB_FORMS = {
        "kagiri-maintained-clock": ("動く", {"動く", "うごく"}),
        "kagiri-maintained-promise": ("守る", {"守る", "まもる"}),
        "kagiri-unless-reservation": ("予約する", {"予約しない", "よやくしない"}),
        "kagiri-unless-fee": ("払う", {"払わない", "はらわない"}),
        "kagiri-unless-correction": ("直す", {"直さない", "なおさない"}),
    }

    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent
        self.data = json.loads((self.root / "grammar" / "formal-nouns-conditions.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_three_examples_per_function_and_complete_relationships(self):
        self.assertEqual(12, len(self.data["exercises"]))
        self.assertEqual(
            {target: 3 for target in self.TARGETS},
            Counter(exercise["target"] for exercise in self.exercises.values()),
        )
        relationships = {
            relationship["id"]: set(relationship["constructions"])
            for relationship in self.data["relationships"]
        }
        self.assertEqual(3, len(relationships))
        for exercise in self.exercises.values():
            self.assertEqual(
                relationships[exercise["relationship"]],
                {option["id"] for option in exercise["options"]},
                exercise["id"],
            )

    def test_scope_and_case_spellings_and_frames(self):
        for exercise in self.exercises.values():
            if exercise["relationship"] not in {"evidence-scope-vs-case", "maintained-condition-vs-case"}:
                continue
            kagiri = exercise["target"].startswith("kagiri-")
            self.assertEqual(
                {"かぎり", "限り"} if kagiri else {"ばあい", "場合"},
                set(exercise["acceptedAnswers"]),
                exercise["id"],
            )
            self.assertIn(
                "Use かぎり or ばあい, in kana or kanji.",
                exercise["translation"],
                exercise["id"],
            )
            if exercise["target"] == "kagiri-evidence-scope":
                span = "____では"
            elif exercise["target"] == "kagiri-maintained-condition":
                span = "____、"
            else:
                span = "____は"
            self.assertIn(span, exercise["prompt"], exercise["id"])
        self.assertIn("雨の____は", self.exercises["baai-rain-practice"]["prompt"])
        self.assertIn("忘れた____は", self.exercises["baai-forgotten-password"]["prompt"])
        self.assertIn("必要な____は", self.exercises["baai-necessary-registration"]["prompt"])
        self.assertIn("not a commitment continuing", self.exercises["baai-necessary-registration"]["translation"])
        for identifier in ("baai-necessary-registration", "kagiri-maintained-study"):
            exercise = self.exercises[identifier]
            self.assertEqual("maintained-condition-vs-case", exercise["relationship"], identifier)
            self.assertEqual(
                {"kagiri-maintained-condition", "baai-case"},
                {option["id"] for option in exercise["options"]},
                identifier,
            )

    def test_polarity_tasks_keep_exact_forms_and_visible_restriction(self):
        for identifier, (verb, answers) in self.VERB_FORMS.items():
            exercise = self.exercises[identifier]
            target = "kagiri-negative-condition" if identifier.startswith("kagiri-unless-") else "kagiri-maintained-condition"
            self.assertEqual(target, exercise["target"], identifier)
            self.assertEqual(answers, set(exercise["acceptedAnswers"]), identifier)
            self.assertIn("____かぎり", exercise["prompt"], identifier)
            self.assertIn(f"Use {verb} (", exercise["translation"], identifier)
            self.assertIn("in dictionary or ない form only", exercise["translation"], identifier)

    def test_negative_conditions_do_not_imply_sufficiency(self):
        additional_requirements = {
            "kagiri-unless-reservation": "身分証",
            "kagiri-unless-fee": "申込書",
            "kagiri-unless-correction": "必要な書類",
        }
        for identifier, requirement in additional_requirements.items():
            exercise = self.exercises[identifier]
            self.assertIn(requirement, exercise["prompt"], identifier)
            self.assertIn("unless", exercise["translation"], identifier)
            self.assertTrue(all(answer.endswith("ない") for answer in exercise["acceptedAnswers"]), identifier)

    def test_source_record_covers_declared_targets(self):
        sources = json.loads((self.root / "docs" / "grammar-conditions-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(self.data["id"], sources["setId"])
        self.assertEqual(self.data["article"], sources["article"])
        self.assertEqual(self.TARGETS, {target for source in sources["sources"] for target in source["supports"]})


class GrammarRelationsCoverageTests(unittest.TestCase):
    TARGETS = {"toori-conformity", "moto-governing-context", "ue-addition", "ue-prerequisite"}

    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent
        self.data = json.loads((self.root / "grammar" / "formal-nouns-relations.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_three_examples_per_function_and_reciprocal_relationships(self):
        self.assertEqual(12, len(self.data["exercises"]))
        self.assertEqual(
            {target: 3 for target in self.TARGETS},
            Counter(exercise["target"] for exercise in self.exercises.values()),
        )
        self.assertEqual(2, len(self.data["relationships"]))
        for relationship in self.data["relationships"]:
            exercises = [exercise for exercise in self.exercises.values() if exercise["relationship"] == relationship["id"]]
            self.assertEqual(
                {target: 3 for target in relationship["constructions"]},
                Counter(exercise["target"] for exercise in exercises),
            )
            for exercise in exercises:
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]},
                    exercise["id"],
                )

    def test_toori_spans_keep_voicing_and_noun_connector_alternatives(self):
        expected = {
            "toori-instruction-manual": ("説明書の____に", {"とおり", "通り"}),
            "toori-planned-departure": ("予定____に", {"どおり", "通り", "のとおり", "の通り"}),
            "toori-demonstrated-movement": ("した____に", {"とおり", "通り"}),
        }
        for identifier, (frame, answers) in expected.items():
            exercise = self.exercises[identifier]
            self.assertIn(frame, exercise["prompt"], identifier)
            self.assertEqual(answers, set(exercise["acceptedAnswers"]), identifier)
            self.assertEqual("toori-conformity", exercise["target"], identifier)

    def test_moto_guidance_and_conditions_accept_both_kanji_spellings(self):
        for identifier in ("moto-teacher-guidance", "moto-equal-conditions", "moto-supervised-work"):
            exercise = self.exercises[identifier]
            self.assertEqual("moto-governing-context", exercise["target"], identifier)
            self.assertEqual({"もと", "下", "許"}, set(exercise["acceptedAnswers"]), identifier)
            self.assertIn("の____で", exercise["prompt"], identifier)
        self.assertIn("温度も時間もそろえます", self.exercises["moto-equal-conditions"]["prompt"])

    def test_noun_tasks_keep_visible_list_and_connection_instruction(self):
        for exercise in self.exercises.values():
            if exercise["relationship"] != "conformity-vs-governing-context":
                continue
            self.assertIn(
                "Use とおり or もと (kanji allowed); include の or voicing only if needed.",
                exercise["translation"],
                exercise["id"],
            )

    def test_ue_particles_preserve_relationship_and_relative_time(self):
        for exercise in self.exercises.values():
            if exercise["relationship"] != "ue-addition-vs-prerequisite":
                continue
            additive = exercise["target"] == "ue-addition"
            self.assertEqual({"に"} if additive else {"で"}, set(exercise["acceptedAnswers"]), exercise["id"])
            self.assertEqual({"に", "で"}, {option["label"] for option in exercise["options"]}, exercise["id"])
            self.assertIn("うえ____", exercise["prompt"], exercise["id"])
            self.assertIn("Use に or で only; うえ is already printed.", exercise["translation"], exercise["id"])
        self.assertIn("安いうえ____", self.exercises["ue-addition-price-portions"]["prompt"])
        self.assertIn("静かなうえ____", self.exercises["ue-addition-quiet-location"]["prompt"])
        past_addition = self.exercises["ue-addition-shop-improvements"]
        self.assertIn("したうえ____", past_addition["prompt"])
        self.assertIn("without specifying an order", past_addition["translation"])
        future_step = self.exercises["ue-prerequisite-family-plan"]
        self.assertIn("相談したうえ____", future_step["prompt"])
        self.assertIn("明日", future_step["prompt"])
        self.assertIn("not fixed yet", future_step["translation"])
        self.assertIn("検討（けんとう）のうえ____", self.exercises["ue-prerequisite-considered-plan"]["prompt"])

    def test_source_record_covers_declared_targets(self):
        sources = json.loads((self.root / "docs" / "grammar-relations-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(self.data["id"], sources["setId"])
        self.assertEqual(self.data["article"], sources["article"])
        self.assertEqual(self.TARGETS, {target for source in sources["sources"] for target in source["supports"]})


class GrammarComparisonsCoverageTests(unittest.TestCase):
    TARGETS = {"hou-comparison", "hoka-addition", "hou-advice-do", "hou-advice-not-do"}
    ADVICE_FORMS = {
        "hou-advice-reserve-seat": ("予約する", "hou-advice-do", {"予約した", "よやくした"}),
        "hou-advice-visit-open-day": ("行く", "hou-advice-do", {"行った", "いった"}),
        "hou-advice-read-instructions": ("読む", "hou-advice-do", {"読んだ", "よんだ"}),
        "hou-advice-wait-to-reserve": ("予約する", "hou-advice-not-do", {"予約しない", "よやくしない"}),
        "hou-advice-avoid-closed-day": ("行く", "hou-advice-not-do", {"行かない", "いかない"}),
        "hou-advice-avoid-spoilers": ("読む", "hou-advice-not-do", {"読まない", "よまない"}),
    }

    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent
        self.data = json.loads((self.root / "grammar" / "formal-nouns-comparisons.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_three_examples_per_target_and_reciprocal_relationships(self):
        self.assertEqual(12, len(self.exercises))
        self.assertEqual(
            {target: 3 for target in self.TARGETS},
            Counter(exercise["target"] for exercise in self.exercises.values()),
        )
        self.assertEqual(2, len(self.data["relationships"]))
        for relationship in self.data["relationships"]:
            exercises = [exercise for exercise in self.exercises.values() if exercise["relationship"] == relationship["id"]]
            self.assertEqual(
                {target: 3 for target in relationship["constructions"]},
                Counter(exercise["target"] for exercise in exercises),
            )
            for exercise in exercises:
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]},
                    exercise["id"],
                )

    def test_noun_and_verb_frames_keep_exact_noun_spellings(self):
        for exercise in self.exercises.values():
            if exercise["relationship"] != "comparison-vs-addition":
                continue
            comparison = exercise["target"] == "hou-comparison"
            self.assertEqual(
                {"ほう", "方"} if comparison else {"ほか", "他", "外"},
                set(exercise["acceptedAnswers"]),
                exercise["id"],
            )
            self.assertIn("____が" if comparison else "____に", exercise["prompt"], exercise["id"])
            self.assertIn("Use ほう or ほか, in kana or kanji.", exercise["translation"], exercise["id"])
        self.assertIn("青いかばんの____が", self.exercises["hou-comparison-bag-weight"]["prompt"])
        self.assertIn("乗る____が", self.exercises["hou-comparison-bus-walk"]["prompt"])
        self.assertIn("パンの____に", self.exercises["hoka-addition-bakery-products"]["prompt"])
        self.assertIn("教えている____に", self.exercises["hoka-addition-teaching-interpreting"]["prompt"])

    def test_advice_keeps_both_directions_and_visible_form_restriction(self):
        for identifier, (verb, target, answers) in self.ADVICE_FORMS.items():
            exercise = self.exercises[identifier]
            self.assertEqual(target, exercise["target"], identifier)
            self.assertEqual(answers, set(exercise["acceptedAnswers"]), identifier)
            self.assertIn("____ほうがいい", exercise["prompt"], identifier)
            self.assertIn(f"Use {verb} (", exercise["translation"], identifier)
            self.assertIn("in た or ない form only", exercise["translation"], identifier)

    def test_comparison_facts_and_advice_reference_points_are_preserved(self):
        self.assertIn("赤いかばんは二キロ、青いかばんは一キロ", self.exercises["hou-comparison-bag-weight"]["prompt"])
        self.assertIn("昼は二十五度、夜は十五度", self.exercises["hou-comparison-day-night"]["prompt"])
        self.assertIn("歩くと三十分、バスなら十分", self.exercises["hou-comparison-bus-walk"]["prompt"])
        future_advice = self.exercises["hou-advice-visit-open-day"]
        self.assertIn("明日____", future_advice["prompt"])
        self.assertIn("行った", future_advice["acceptedAnswers"])
        self.assertIn("読んだ", self.exercises["hou-advice-read-instructions"]["acceptedAnswers"])
        self.assertIn("小説を読み終わるまで", self.exercises["hou-advice-avoid-spoilers"]["prompt"])

    def test_source_record_covers_declared_targets(self):
        sources = json.loads((self.root / "docs" / "grammar-comparisons-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(self.data["id"], sources["setId"])
        self.assertEqual(self.data["article"], sources["article"])
        self.assertEqual(self.TARGETS, {target for source in sources["sources"] for target in source["supports"]})


class GrammarExpectationsCoverageTests(unittest.TestCase):
    TARGET_COUNTS = {"wari-expectation": 3, "kuse-reproach": 3, "process-outcome": 6, "ue-addition": 3}
    OUTCOME_ANSWERS = {"すえ", "末", "あげく", "挙句", "挙げ句", "揚句", "揚げ句"}

    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent
        self.data = json.loads((self.root / "grammar" / "formal-nouns-expectations.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_target_counts_and_reciprocal_relationships(self):
        self.assertEqual(15, len(self.exercises))
        self.assertEqual(self.TARGET_COUNTS, Counter(exercise["target"] for exercise in self.exercises.values()))
        self.assertEqual(2, len(self.data["relationships"]))
        for relationship in self.data["relationships"]:
            exercises = [exercise for exercise in self.exercises.values() if exercise["relationship"] == relationship["id"]]
            self.assertEqual(set(relationship["constructions"]), {exercise["target"] for exercise in exercises})
            for exercise in exercises:
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]},
                    exercise["id"],
                )

    def test_expectation_reproach_tasks_keep_visible_scope_and_spellings(self):
        for exercise in self.exercises.values():
            if exercise["relationship"] != "expectation-vs-reproach":
                continue
            expectation = exercise["target"] == "wari-expectation"
            self.assertEqual(
                {"わり", "割", "割り"} if expectation else {"くせ", "癖"},
                set(exercise["acceptedAnswers"]),
                exercise["id"],
            )
            self.assertIn("____に", exercise["prompt"], exercise["id"])
            self.assertIn("Use わり or くせ, in hiragana or kanji.", exercise["translation"], exercise["id"])
            self.assertIn(
                "without a mocking or reproachful tone" if expectation else "construction that itself conventionally marks reproach",
                exercise["translation"],
                exercise["id"],
            )
        self.assertIn("値段の____に", self.exercises["wari-inexpensive-umbrella"]["prompt"])
        self.assertIn("作った____に", self.exercises["wari-first-cake"]["prompt"])
        self.assertIn("責任者の____に", self.exercises["kuse-avoiding-responsibility"]["prompt"])

    def test_sue_ageku_share_answers_with_three_model_options_each(self):
        models = Counter()
        for exercise in self.exercises.values():
            if exercise["target"] != "process-outcome":
                continue
            self.assertEqual(self.OUTCOME_ANSWERS, set(exercise["acceptedAnswers"]), exercise["id"])
            correct = next(option for option in exercise["options"] if option["id"] == exercise["answer"])
            models[correct["label"]] += 1
            self.assertIn("Describe the eventual outcome of the process", exercise["translation"], exercise["id"])
        self.assertEqual({"すえ": 3, "あげく": 3}, models)

    def test_outcome_noun_and_verb_frames_keep_literal_spans(self):
        noun_frames = {"process-outcome-cancelled-event", "process-outcome-failed-negotiation"}
        outcomes = [exercise for exercise in self.exercises.values() if exercise["target"] == "process-outcome"]
        self.assertEqual(6, len(outcomes))
        for exercise in outcomes:
            if exercise["id"] in noun_frames:
                frame = "の____に"
            elif exercise["id"] == "process-outcome-sold-out-tickets":
                frame = "だ____に"
            else:
                frame = "た____に"
            self.assertIn(frame, exercise["prompt"], exercise["id"])
        self.assertIn("話し合いの____に", self.exercises["process-outcome-cancelled-event"]["prompt"])
        self.assertIn("交渉の____に", self.exercises["process-outcome-failed-negotiation"]["prompt"])

    def test_additions_do_not_become_outcomes_from_tense_alone(self):
        for exercise in self.exercises.values():
            if exercise["relationship"] != "outcome-vs-addition":
                continue
            self.assertIn(
                "Use すえ, あげく or うえ, in hiragana or kanji; に is already printed.",
                exercise["translation"],
                exercise["id"],
            )
            self.assertIn("____に", exercise["prompt"], exercise["id"])
            if exercise["target"] == "ue-addition":
                self.assertEqual({"うえ", "上"}, set(exercise["acceptedAnswers"]), exercise["id"])
        self.assertIn("明るい____に", self.exercises["ue-addition-bright-spacious-room"]["prompt"])
        self.assertIn("平らな____に", self.exercises["ue-addition-flat-quiet-road"]["prompt"])
        past_addition = self.exercises["ue-addition-office-improvements"]
        self.assertIn("移した____に", past_addition["prompt"])
        self.assertIn("not an outcome of the move", past_addition["translation"])

    def test_source_record_covers_declared_targets(self):
        sources = json.loads((self.root / "docs" / "grammar-expectations-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(self.data["id"], sources["setId"])
        self.assertEqual(self.data["article"], sources["article"])
        self.assertEqual(set(self.TARGET_COUNTS), {target for source in sources["sources"] for target in source["supports"]})


class GrammarMonoCoverageTests(unittest.TestCase):
    TARGET_COUNTS = {
        "mono-characteristic": 3,
        "mono-recollection": 3,
        "mono-personal-reason": 3,
        "wake-conclusion": 3,
    }

    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent
        self.data = json.loads((self.root / "grammar" / "formal-nouns-mono.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_target_counts_and_reciprocal_relationships(self):
        self.assertEqual(12, len(self.exercises))
        self.assertEqual(self.TARGET_COUNTS, Counter(exercise["target"] for exercise in self.exercises.values()))
        self.assertEqual(2, len(self.data["relationships"]))
        for relationship in self.data["relationships"]:
            exercises = [exercise for exercise in self.exercises.values() if exercise["relationship"] == relationship["id"]]
            self.assertEqual(set(relationship["constructions"]), {exercise["target"] for exercise in exercises})
            for exercise in exercises:
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]},
                    exercise["id"],
                )

    def test_characteristic_recollection_pairs_preserve_exact_verb_forms(self):
        expected = {
            "mono-characteristic-unused-words": {"忘れる", "わすれる"},
            "mono-characteristic-gathering": {"集まる", "あつまる"},
            "mono-characteristic-winter-snow": {"降る", "ふる"},
            "mono-recollection-forgotten-umbrellas": {"忘れた", "わすれた"},
            "mono-recollection-festival-square": {"集まった", "あつまった"},
            "mono-recollection-childhood-snow": {"降った", "ふった"},
        }
        for exercise_id, answers in expected.items():
            exercise = self.exercises[exercise_id]
            self.assertEqual(answers, set(exercise["acceptedAnswers"]), exercise_id)
            self.assertIn("____ものです", exercise["prompt"], exercise_id)
            self.assertIn("dictionary or た form only; ものです is already printed.", exercise["translation"], exercise_id)

    def test_recollection_does_not_require_pleasantness_or_cessation(self):
        umbrella = self.exercises["mono-recollection-forgotten-umbrellas"]
        self.assertIn("recurring past experience", umbrella["translation"])
        self.assertIn("need not concern a pleasant habit", umbrella["explanation"])
        self.assertIn("ceased", umbrella["explanation"])
        snow = self.exercises["mono-recollection-childhood-snow"]
        self.assertIn("nostalgic recollection", snow["translation"])
        self.assertIn("does not by itself assert", snow["explanation"])
        self.assertIn("今も毎年そうです", self.exercises["mono-characteristic-winter-snow"]["prompt"])

    def test_personal_reasons_and_conclusions_keep_literal_ending_contract(self):
        for exercise in self.exercises.values():
            if exercise["relationship"] != "personal-reason-vs-conclusion":
                continue
            personal_reason = exercise["target"] == "mono-personal-reason"
            self.assertEqual(
                {"もの", "もん"} if personal_reason else {"わけだ"},
                set(exercise["acceptedAnswers"]),
                exercise["id"],
            )
            self.assertIn(
                "Use exactly one of these endings as written: もの, もん, わけだ.",
                exercise["translation"],
                exercise["id"],
            )
            self.assertIn(
                "Complete a casual personal justification" if personal_reason else "Express a conclusion",
                exercise["translation"],
                exercise["id"],
            )

    def test_first_time_reason_does_not_duplicate_printed_nanda(self):
        exercise = self.exercises["mono-reason-first-time"]
        self.assertIn("初めてなんだ____", exercise["prompt"])
        self.assertEqual({"もの", "もん"}, set(exercise["acceptedAnswers"]))
        self.assertIn("ん from explanatory の", exercise["explanation"])
        self.assertIn("contraction of もの", exercise["explanation"])

    def test_source_record_covers_declared_targets(self):
        sources = json.loads((self.root / "docs" / "grammar-mono-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(self.data["id"], sources["setId"])
        self.assertEqual(self.data["article"], sources["article"])
        self.assertEqual(set(self.TARGET_COUNTS), {target for source in sources["sources"] for target in source["supports"]})


class GrammarParticleCoverageTests(unittest.TestCase):
    TARGET_COUNTS = {
        "approximate-quantity": 6,
        "dake-limit": 3,
        "bakari-concentration": 3,
        "bakari-recent-completion": 3,
    }
    APPROXIMATION_ANSWERS = {"ほど", "程", "くらい", "ぐらい", "位", "ばかり", "許り", "許"}

    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent
        self.data = json.loads((self.root / "grammar" / "particle-neighbors.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_target_counts_and_reciprocal_relationships(self):
        self.assertEqual(15, len(self.exercises))
        self.assertEqual(self.TARGET_COUNTS, Counter(exercise["target"] for exercise in self.exercises.values()))
        self.assertEqual(2, len(self.data["relationships"]))
        for relationship in self.data["relationships"]:
            exercises = [exercise for exercise in self.exercises.values() if exercise["relationship"] == relationship["id"]]
            self.assertEqual(set(relationship["constructions"]), {exercise["target"] for exercise in exercises})
            for exercise in exercises:
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]},
                    exercise["id"],
                )

    def test_approximation_answers_are_shared_not_competing_options(self):
        models = Counter()
        for exercise in self.exercises.values():
            if exercise["target"] != "approximate-quantity":
                continue
            self.assertEqual(self.APPROXIMATION_ANSWERS, set(exercise["acceptedAnswers"]), exercise["id"])
            self.assertIn(
                "Use ほど, くらい, ぐらい, ばかり or だけ, uncontracted, in hiragana or kanji.",
                exercise["translation"],
                exercise["id"],
            )
            self.assertIn("Mark an approximate quantity, not an exclusive limit", exercise["translation"], exercise["id"])
            correct = next(option for option in exercise["options"] if option["id"] == exercise["answer"])
            models[correct["label"]] += 1
            distractors = {option["label"] for option in exercise["options"] if option["id"] != exercise["answer"]}
            self.assertTrue(self.APPROXIMATION_ANSWERS.isdisjoint(distractors), exercise["id"])
        self.assertEqual({"ほど": 3, "くらい": 2, "ぐらい": 1}, models)

    def test_limits_keep_their_narrower_visible_candidate_list(self):
        for exercise in self.exercises.values():
            if exercise["target"] != "dake-limit":
                continue
            self.assertEqual({"だけ", "丈"}, set(exercise["acceptedAnswers"]), exercise["id"])
            self.assertIn(
                "Use ほど, くらい, ぐらい or だけ, in hiragana or kanji.",
                exercise["translation"],
                exercise["id"],
            )
            self.assertIn("Mark an exclusive limit, not an estimate", exercise["translation"], exercise["id"])
        self.assertIn("三人目には別の券が必要", self.exercises["dake-limit-admission-ticket"]["prompt"])
        self.assertIn("二個でも四個でもなく、三個", self.exercises["dake-limit-three-balls"]["prompt"])
        self.assertIn("五分を過ぎたら", self.exercises["dake-limit-five-minute-break"]["prompt"])

    def test_bakari_pairs_keep_literal_te_ta_forms(self):
        expected = {
            "bakari-concentration-snacking": {"食べて", "たべて"},
            "bakari-concentration-holiday-reading": {"読んで", "よんで"},
            "bakari-concentration-weekend-play": {"遊んで", "あそんで"},
            "bakari-recent-completion-dinner": {"食べた", "たべた"},
            "bakari-recent-completion-yesterday-book": {"読んだ", "よんだ"},
            "bakari-recent-completion-play": {"遊んだ", "あそんだ"},
        }
        for exercise_id, answers in expected.items():
            exercise = self.exercises[exercise_id]
            self.assertEqual(answers, set(exercise["acceptedAnswers"]), exercise_id)
            self.assertIn("____ばかりです", exercise["prompt"], exercise_id)
            self.assertIn("て or た form only; ばかりです is already printed.", exercise["translation"], exercise_id)
            self.assertIn(
                "Describe activity that dominates" if exercise["target"] == "bakari-concentration" else "Describe recent completion",
                exercise["translation"],
                exercise_id,
            )

    def test_activity_and_recency_do_not_acquire_universal_tone_or_clock_limits(self):
        holiday = self.exercises["bakari-concentration-holiday-reading"]
        self.assertIn("楽しくて時間を忘れます", holiday["prompt"])
        self.assertIn("criticism is not mandatory", holiday["explanation"])
        book = self.exercises["bakari-recent-completion-yesterday-book"]
        self.assertIn("昨日、最後まで", book["prompt"])
        self.assertIn("does not impose a fixed seconds-or-minutes cutoff", book["explanation"])
        self.assertIn("いる is not required", self.exercises["bakari-concentration-snacking"]["explanation"])
        self.assertIn("食べたところです can also", self.exercises["bakari-recent-completion-dinner"]["explanation"])

    def test_source_record_covers_declared_targets(self):
        sources = json.loads((self.root / "docs" / "grammar-particles-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(self.data["id"], sources["setId"])
        self.assertEqual(self.data["article"], sources["article"])
        self.assertEqual(set(self.TARGET_COUNTS), {target for source in sources["sources"] for target in source["supports"]})


class GrammarDegreeExtentCoverageTests(unittest.TestCase):
    TARGET_COUNTS = {
        "hodo-stated-degree": 3,
        "hodo-below-standard": 3,
        "hodo-proportional-change": 3,
        "dake-desired-extent": 3,
    }

    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent
        self.data = json.loads((self.root / "grammar" / "particle-degree-extent.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_target_counts_and_reciprocal_relationships(self):
        self.assertEqual(12, len(self.exercises))
        self.assertEqual(self.TARGET_COUNTS, Counter(exercise["target"] for exercise in self.exercises.values()))
        self.assertEqual(2, len(self.data["relationships"]))
        for relationship in self.data["relationships"]:
            exercises = [exercise for exercise in self.exercises.values() if exercise["relationship"] == relationship["id"]]
            self.assertEqual(set(relationship["constructions"]), {exercise["target"] for exercise in exercises})
            for exercise in exercises:
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]},
                    exercise["id"],
                )

    def test_adjective_pairs_keep_the_visible_standard_form_contract(self):
        expected = {
            "hodo-stated-degree-heavy-box": {"重い", "おもい"},
            "hodo-stated-degree-expensive-watch": {"高い", "たかい"},
            "hodo-stated-degree-chattering-teeth": {"寒い", "さむい"},
            "hodo-below-standard-box-weights": {"重くない", "おもくない"},
            "hodo-below-standard-watch-prices": {"高くない", "たかくない"},
            "hodo-below-standard-warmer-day": {"寒くない", "さむくない"},
        }
        for exercise_id, answers in expected.items():
            exercise = self.exercises[exercise_id]
            self.assertEqual(answers, set(exercise["acceptedAnswers"]), exercise_id)
            self.assertIn("ほど____です", exercise["prompt"], exercise_id)
            self.assertIn(
                "standard plain nonpast affirmative or negative form, without added particles; です is already printed.",
                exercise["translation"],
                exercise_id,
            )

    def test_negation_location_and_comparison_direction_are_preserved(self):
        box_degree = self.exercises["hodo-stated-degree-heavy-box"]
        self.assertIn("持ち上げられないほど____", box_degree["prompt"])
        self.assertEqual("hodo-stated-degree", box_degree["answer"])
        self.assertIn("買えないほど____", self.exercises["hodo-stated-degree-expensive-watch"]["prompt"])
        boxes = self.exercises["hodo-below-standard-box-weights"]
        self.assertIn("赤い箱は十キロ、青い箱は二キロ", boxes["prompt"])
        self.assertIn("青い箱は赤い箱ほど____", boxes["prompt"])
        watches = self.exercises["hodo-below-standard-watch-prices"]
        self.assertIn("この時計は一万円、あの時計は十万円", watches["prompt"])
        self.assertIn("この時計はあの時計ほど____", watches["prompt"])
        self.assertIn("not an absolute claim", watches["explanation"])
        weather = self.exercises["hodo-below-standard-warmer-day"]
        self.assertIn("昨日より暖かく感じます", weather["prompt"])
        self.assertIn("not necessarily mean today is not cold at all", weather["explanation"])

    def test_full_patterns_accept_every_kana_kanji_combination(self):
        pairs = [
            ("hodo-proportional-novel", "dake-desired-extent-reading-time",
             ("読めば", "よめば"), ("読む", "よむ"), ("読みたい", "よみたい")),
            ("hodo-proportional-puzzling-problem", "dake-desired-extent-thinking-time",
             ("考えれば", "かんがえれば"), ("考える", "かんがえる"), ("考えたい", "かんがえたい")),
            ("hodo-proportional-familiar-tool", "dake-desired-extent-paper",
             ("使えば", "つかえば"), ("使う", "つかう"), ("使いたい", "つかいたい")),
        ]
        for proportional_id, desired_id, conditionals, verbs, desires in pairs:
            proportional = {
                conditional + verb + particle
                for conditional in conditionals for verb in verbs for particle in ("ほど", "程")
            }
            desired = {desire + particle for desire in desires for particle in ("だけ", "丈")}
            self.assertEqual(proportional, set(self.exercises[proportional_id]["acceptedAnswers"]), proportional_id)
            self.assertEqual(desired, set(self.exercises[desired_id]["acceptedAnswers"]), desired_id)
            self.assertEqual(8, len(proportional))
            self.assertEqual(4, len(desired))
            for exercise_id in (proportional_id, desired_id):
                self.assertIn(
                    "ば-form + dictionary form + ほど, or たい-form + だけ. Fill the whole pattern, in kana or kanji.",
                    self.exercises[exercise_id]["translation"],
                    exercise_id,
                )

    def test_change_and_desire_frames_keep_their_meanings_visible(self):
        for exercise in self.exercises.values():
            if exercise["relationship"] != "proportional-change-vs-desired-extent":
                continue
            self.assertIn(
                "Express correlated change, not a desired amount"
                if exercise["target"] == "hodo-proportional-change"
                else "Explicitly mark a desired amount, not correlated change",
                exercise["translation"],
                exercise["id"],
            )
        problem = self.exercises["hodo-proportional-puzzling-problem"]
        self.assertIn("かえって分からなくなります", problem["prompt"])
        self.assertIn("need not be beneficial", problem["explanation"])
        self.assertIn("does not say the amount must be small", self.exercises["dake-desired-extent-reading-time"]["explanation"])

    def test_source_record_covers_declared_targets_and_committed_baseline(self):
        sources = json.loads((self.root / "docs" / "grammar-degree-extent-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(self.data["id"], sources["setId"])
        self.assertEqual(self.data["article"], sources["article"])
        self.assertEqual(set(self.TARGET_COUNTS), {target for source in sources["sources"] for target in source["supports"]})
        self.assertEqual(197, sources["preservationBaseline"]["headExerciseCount"])
        self.assertEqual(0, sources["preservationBaseline"]["uncommittedExerciseCount"])


class GrammarPlansCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-plans.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_target_counts_and_reciprocal_relationships(self):
        self.assertEqual({
            "tsumori-current-plan": 3,
            "tsumori-negative-plan": 3,
            "tsumori-past-plan": 3,
            "tsumori-believed-completion": 3,
        }, Counter(exercise["target"] for exercise in self.exercises.values()))
        for relationship in self.data["relationships"]:
            exercises = [exercise for exercise in self.exercises.values() if exercise["relationship"] == relationship["id"]]
            self.assertEqual(set(relationship["constructions"]), {exercise["target"] for exercise in exercises})
            for exercise in exercises:
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]},
                    exercise["id"],
                )

    def test_current_plans_keep_the_visible_form_contract_and_spelling_pairs(self):
        pairs = [
            ("tsumori-plan-weekend-novel", "tsumori-negative-plan-novel",
             {"読む", "よむ"}, {"読まない", "よまない"}),
            ("tsumori-plan-next-year-bicycle", "tsumori-negative-plan-bicycle",
             {"買う", "かう"}, {"買わない", "かわない"}),
            ("tsumori-plan-camera", "tsumori-negative-plan-camera",
             {"使う", "つかう"}, {"使わない", "つかわない"}),
        ]
        for affirmative_id, negative_id, affirmative, negative in pairs:
            for exercise_id, answers in ((affirmative_id, affirmative), (negative_id, negative)):
                exercise = self.exercises[exercise_id]
                self.assertEqual(answers, set(exercise["acceptedAnswers"]), exercise_id)
                self.assertIn("____つもりです", exercise["prompt"], exercise_id)
                self.assertIn("Use only", exercise["translation"], exercise_id)
                self.assertIn(
                    "dictionary or ない form; つもりです is already printed.",
                    exercise["translation"], exercise_id,
                )
        self.assertIn("来年", self.exercises["tsumori-plan-next-year-bicycle"]["prompt"])
        camera = self.exercises["tsumori-plan-camera"]
        self.assertIn("スマートフォンではなく", camera["prompt"])
        self.assertEqual({"使う", "つかう"}, set(camera["acceptedAnswers"]))
        self.assertIn("スマートフォンで写真を撮ります", self.exercises["tsumori-negative-plan-camera"]["prompt"])

    def test_past_pairs_keep_outer_tense_constant_and_mental_stance_visible(self):
        pairs = [
            ("tsumori-past-plan-application", "tsumori-believed-completion-application",
             {"送る", "おくる"}, {"送った", "おくった"}),
            ("tsumori-past-plan-window", "tsumori-believed-completion-windows-confirmed",
             {"閉める", "しめる"}, {"閉めた", "しめた"}),
            ("tsumori-past-plan-room-realized", "tsumori-believed-completion-room-size",
             {"予約する", "よやくする"}, {"予約した", "よやくした"}),
        ]
        for plan_id, belief_id, planned, completed in pairs:
            for exercise_id, answers in ((plan_id, planned), (belief_id, completed)):
                exercise = self.exercises[exercise_id]
                self.assertEqual(answers, set(exercise["acceptedAnswers"]), exercise_id)
                self.assertIn("____つもりでした", exercise["prompt"], exercise_id)
                self.assertIn("Use only", exercise["translation"], exercise_id)
                self.assertIn(
                    "dictionary or た form; つもりでした is already printed.",
                    exercise["translation"], exercise_id,
                )
                self.assertIn(
                    "Report my intention at that past time, not a belief that the action was already completed."
                    if exercise_id == plan_id else
                    "Report my belief that the action was completed, not my past intention to act.",
                    exercise["translation"], exercise_id,
                )
            self.assertEqual(
                [option["label"] for option in self.exercises[plan_id]["options"]],
                [option["label"] for option in self.exercises[belief_id]["options"]],
            )

    def test_actual_outcome_does_not_replace_the_requested_viewpoint(self):
        plan = self.exercises["tsumori-past-plan-room-realized"]
        self.assertIn("先週の月曜日には、その週の金曜日に", plan["prompt"])
        self.assertIn("実際に金曜日に予約の手続きを済ませました", plan["prompt"])
        self.assertEqual({"予約する", "よやくする"}, set(plan["acceptedAnswers"]))
        confirmed = self.exercises["tsumori-believed-completion-windows-confirmed"]
        self.assertIn("やはり全部閉まっていました", confirmed["prompt"])
        self.assertEqual({"閉めた", "しめた"}, set(confirmed["acceptedAnswers"]))
        wrong_room = self.exercises["tsumori-believed-completion-room-size"]
        self.assertIn("予約を終えたときは、大きな会議室を", wrong_room["prompt"])
        self.assertIn("小さな部屋の番号", wrong_room["prompt"])
        self.assertEqual({"予約した", "よやくした"}, set(wrong_room["acceptedAnswers"]))


class GrammarYouCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-you.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_target_counts_and_reciprocal_relationships(self):
        self.assertEqual({
            "you-adverbial-comparison": 3,
            "you-noun-modifier": 3,
            "you-enabled-goal": 3,
            "you-prevented-goal": 3,
        }, Counter(exercise["target"] for exercise in self.exercises.values()))
        for relationship in self.data["relationships"]:
            exercises = [exercise for exercise in self.exercises.values() if exercise["relationship"] == relationship["id"]]
            self.assertEqual(set(relationship["constructions"]), {exercise["target"] for exercise in exercises})
            for exercise in exercises:
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]},
                    exercise["id"],
                )

    def test_modification_questions_keep_scope_visible_and_accept_only_the_ending(self):
        expected = {
            "you-manner-folding-model": ("に", "Describe how to fold"),
            "you-comparison-february-warmth": ("に", "Apply the comparison to the property 暖かい"),
            "you-manner-teacher-writing": ("に", "Describe how to write"),
            "you-example-fruit-jam": ("な", "directly modify 果物"),
            "you-resemblance-cloud-cushion": ("な", "directly modify 形"),
            "you-example-cooking-work": ("な", "directly modify 仕事"),
        }
        for exercise_id, (answer, scope) in expected.items():
            exercise = self.exercises[exercise_id]
            self.assertEqual([answer], exercise["acceptedAnswers"], exercise_id)
            self.assertIn("よう____", exercise["prompt"], exercise_id)
            self.assertIn("Use only に or な after the printed よう.", exercise["translation"], exercise_id)
            self.assertIn(scope, exercise["translation"], exercise_id)
        self.assertIn("よう____暖かいです", self.exercises["you-comparison-february-warmth"]["prompt"])
        self.assertIn("先生が書いたよう____", self.exercises["you-manner-teacher-writing"]["prompt"])
        self.assertIn("今日は、りんごを使います", self.exercises["you-example-fruit-jam"]["prompt"])
        self.assertIn("need not literally be a cloud", self.exercises["you-resemblance-cloud-cushion"]["explanation"])

    def test_goal_pairs_keep_the_potential_form_contract_and_all_model_spellings(self):
        pairs = [
            ("you-enabled-goal-readable-notice", "you-prevented-goal-private-letter",
             {"読める", "よめる"}, {"読めない", "よめない"}),
            ("you-enabled-goal-tool-instructions", "you-prevented-goal-phone-lock",
             {"使える", "つかえる"}, {"使えない", "つかえない"}),
            ("you-enabled-goal-venue-ramp", "you-prevented-goal-meeting-access",
             {"入れる", "はいれる"}, {"入れない", "はいれない"}),
        ]
        for enabled_id, prevented_id, enabled, prevented in pairs:
            for exercise_id, answers in ((enabled_id, enabled), (prevented_id, prevented)):
                exercise = self.exercises[exercise_id]
                self.assertEqual(answers, set(exercise["acceptedAnswers"]), exercise_id)
                self.assertIn("____ように", exercise["prompt"], exercise_id)
                self.assertIn(
                    "potential form ending in る or ない, without added words; ように is already printed.",
                    exercise["translation"], exercise_id,
                )
                self.assertIn("State the purpose:", exercise["translation"], exercise_id)
            self.assertEqual(
                [option["label"] for option in self.exercises[enabled_id]["options"]],
                [option["label"] for option in self.exercises[prevented_id]["options"]],
            )

    def test_goals_preserve_time_viewpoint_and_the_affected_people(self):
        notice = self.exercises["you-enabled-goal-readable-notice"]
        self.assertIn("ふりがなを付けました", notice["prompt"])
        self.assertEqual({"読める", "よめる"}, set(notice["acceptedAnswers"]))
        self.assertIn("rather than independently proving", notice["explanation"])
        ramp = self.exercises["you-enabled-goal-venue-ramp"]
        self.assertIn("車いすの人も", ramp["prompt"])
        self.assertIn("明日の朝までに", ramp["prompt"])
        self.assertIn("スロープを付けます", ramp["prompt"])
        self.assertIn("はいれる", ramp["explanation"])
        meeting = self.exercises["you-prevented-goal-meeting-access"]
        self.assertIn("関係のない人が", meeting["prompt"])
        self.assertIn("はいれない", meeting["explanation"])
        self.assertIn("not to every participant", meeting["evidence"])


class GrammarKiriCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "particle-kiri.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_both_sides_of_each_relationship_have_three_examples(self):
        self.assertEqual({
            "kiri-shared-limit": 3,
            "kiri-approximate-count": 3,
            "kiri-last-event": 3,
            "tabi-repeated-followup": 3,
        }, Counter(exercise["target"] for exercise in self.exercises.values()))
        for relationship in self.data["relationships"]:
            exercises = [exercise for exercise in self.exercises.values() if exercise["relationship"] == relationship["id"]]
            self.assertEqual(set(relationship["constructions"]), {exercise["target"] for exercise in exercises})
            for exercise in exercises:
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]},
                    exercise["id"],
                )

    def test_quantity_answers_group_equivalents_without_wrong_equivalent_buttons(self):
        estimates = {"ほど", "程", "くらい", "ぐらい", "位", "ばかり", "許り", "許"}
        limits = {"きり", "切り", "切", "限り", "限", "だけ", "丈", "のみ"}
        for exercise in self.exercises.values():
            if exercise["relationship"] != "kiri-limit-vs-estimate":
                continue
            expected = estimates if exercise["target"] == "kiri-approximate-count" else limits
            if exercise["id"] == "kiri-restricted-single-chance":
                expected = expected | {"かぎり"}
            self.assertEqual(expected, set(exercise["acceptedAnswers"]), exercise["id"])
            self.assertIn(
                "Use an uncontracted form from きり, だけ, のみ, かぎり, ほど, くらい／ぐらい or ばかり",
                exercise["translation"], exercise["id"],
            )
            self.assertIn(
                "Express an estimate" if expected == estimates else "Express an exclusive limit",
                exercise["translation"], exercise["id"],
            )
            for option in exercise["options"]:
                self.assertEqual(option["id"] == exercise["answer"], option["label"] in expected, exercise["id"])
        chance = self.exercises["kiri-restricted-single-chance"]
        self.assertIn("一度だけ", chance["explanation"])
        self.assertIn("一度のみ", chance["explanation"])
        self.assertIn("いちどかぎり", chance["explanation"])
        for exercise_id in ("kiri-restricted-alone-cooking", "kiri-restricted-private-pair"):
            self.assertIn("のみで", self.exercises[exercise_id]["explanation"])
            self.assertIn("かぎり", self.exercises[exercise_id]["explanation"])

    def test_temporal_pairs_keep_attachment_and_literal_accepted_spans(self):
        pairs = [
            ("kiri-last-event-unreturned-book", "tabi-followup-returned-books",
             ("借りた", "かりた"), ("借りる", "かりる")),
            ("kiri-last-event-still-out", "tabi-followup-travel-souvenirs",
             ("出かけた", "でかけた", "出掛けた"), ("出かける", "でかける", "出掛ける")),
            ("kiri-last-event-contact-resumed", "tabi-followup-asking-about-work",
             ("電話した", "でんわした"), ("電話する", "でんわする")),
        ]
        for last_id, recurring_id, past_forms, dictionary_forms in pairs:
            for exercise_id, forms, endings in (
                (last_id, past_forms, ("きり", "切り", "切", "限り", "限", "っきり", "っ切り")),
                (recurring_id, dictionary_forms, ("たびに", "度に")),
            ):
                exercise = self.exercises[exercise_id]
                self.assertEqual(
                    {form + ending for form in forms for ending in endings},
                    set(exercise["acceptedAnswers"]), exercise_id,
                )
                self.assertIn("____、", exercise["prompt"], exercise_id)
                self.assertIn(
                    "in either Vた＋きり or Vる＋たびに, without extra particles; colloquial っきり is also accepted.",
                    exercise["translation"], exercise_id,
                )
            self.assertEqual(
                [option["label"] for option in self.exercises[last_id]["options"]],
                [option["label"] for option in self.exercises[recurring_id]["options"]],
            )

    def test_last_event_does_not_require_first_ever_or_permanent_absence(self):
        loan = self.exercises["kiri-last-event-unreturned-book"]
        self.assertIn("兄はよく私の本を借ります", loan["prompt"])
        self.assertIn("まだ返してくれません", loan["prompt"])
        self.assertIn("returning the book", loan["explanation"])
        outing = self.exercises["kiri-last-event-still-out"]
        self.assertIn("昼になってもまだ戻っていません", outing["prompt"])
        self.assertIn("今夜は帰る予定です", outing["prompt"])
        call = self.exercises["kiri-last-event-contact-resumed"]
        self.assertIn("昨日まで連絡をくれませんでした", call["prompt"])
        self.assertIn("今日はまた電話がありました", call["prompt"])
        self.assertIn("does not contradict", call["explanation"])


class GrammarYouChangeEffortCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-you-change-effort.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_three_contexts_per_target_and_both_directions(self):
        self.assertEqual({
            "you-new-ability": 3,
            "you-new-habit": 3,
            "you-effort-do": 3,
            "you-effort-avoid": 3,
        }, Counter(exercise["target"] for exercise in self.exercises.values()))
        for relationship in self.data["relationships"]:
            exercises = [exercise for exercise in self.exercises.values() if exercise["relationship"] == relationship["id"]]
            self.assertEqual(set(relationship["constructions"]), {exercise["target"] for exercise in exercises})
            for exercise in exercises:
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]}, exercise["id"],
                )

    def test_change_pairs_keep_the_same_outer_tense_and_question_visible_focus(self):
        pairs = [
            ("you-new-ability-larger-display", "you-new-habit-bedtime-novels", {"読める", "よめる"}, {"読む", "よむ"}),
            ("you-new-ability-bicycle-balance", "you-new-habit-bicycle-commute", {"乗れる", "のれる"}, {"乗る", "のる"}),
            ("you-new-ability-conversation", "you-new-habit-neighbor-conversations", {"話せる", "はなせる"}, {"話す", "はなす"}),
        ]
        for ability_id, habit_id, ability_answers, habit_answers in pairs:
            for exercise_id, answers, focus in (
                (ability_id, ability_answers, "Report a newly possible action, not a new habit"),
                (habit_id, habit_answers, "Report a new habit, not a newly acquired ability"),
            ):
                exercise = self.exercises[exercise_id]
                self.assertEqual(answers, set(exercise["acceptedAnswers"]), exercise_id)
                self.assertIn("____ようになりました", exercise["prompt"], exercise_id)
                self.assertIn("dictionary or potential form, without added words", exercise["translation"], exercise_id)
                self.assertIn(focus, exercise["translation"], exercise_id)
            self.assertEqual(
                [option["label"] for option in self.exercises[ability_id]["options"]],
                [option["label"] for option in self.exercises[habit_id]["options"]],
            )

    def test_effort_pairs_keep_action_polarity_inside_the_supplied_pattern(self):
        pairs = [
            ("you-effort-do-read-instructions", "you-effort-avoid-work-email", {"読む", "よむ"}, {"読まない", "よまない"}),
            ("you-effort-do-use-stairs", "you-effort-avoid-bedtime-phone", {"使う", "つかう"}, {"使わない", "つかわない"}),
            ("you-effort-do-speak-slowly", "you-effort-avoid-sharing-private-story", {"話す", "はなす"}, {"話さない", "はなさない"}),
        ]
        for do_id, avoid_id, do_answers, avoid_answers in pairs:
            for exercise_id, answers in ((do_id, do_answers), (avoid_id, avoid_answers)):
                exercise = self.exercises[exercise_id]
                self.assertEqual(answers, set(exercise["acceptedAnswers"]), exercise_id)
                self.assertIn("____ようにしています", exercise["prompt"], exercise_id)
                self.assertIn("dictionary or ない form, without added words", exercise["translation"], exercise_id)
                self.assertIn("State the maintained practice:", exercise["translation"], exercise_id)
            self.assertEqual(
                [option["label"] for option in self.exercises[do_id]["options"]],
                [option["label"] for option in self.exercises[avoid_id]["options"]],
            )

    def test_changes_and_efforts_preserve_their_contextual_qualifications(self):
        display = self.exercises["you-new-ability-larger-display"]
        self.assertIn("文字の表示を大きくしたら", display["prompt"])
        self.assertIn("not only from learning a skill", display["explanation"])
        self.assertIn("簡単なことなら", self.exercises["you-new-ability-conversation"]["prompt"])
        for exercise_id, prior_ability in (
            ("you-new-habit-bedtime-novels", "前から漢字は読めました"),
            ("you-new-habit-bicycle-commute", "前から自転車には乗れました"),
            ("you-new-habit-neighbor-conversations", "以前から近所の人とは日本語で話せました"),
        ):
            self.assertIn(prior_ability, self.exercises[exercise_id]["prompt"])
        phone = self.exercises["you-effort-avoid-bedtime-phone"]
        self.assertIn("たまに見てしまう日もあります", phone["prompt"])
        self.assertIn("does not guarantee perfect success", phone["explanation"])
        self.assertIn("近い階へ行くとき", self.exercises["you-effort-do-use-stairs"]["prompt"])
        self.assertIn("本人の許可なく", self.exercises["you-effort-avoid-sharing-private-story"]["prompt"])


class GrammarSelfAssessmentCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-self-assessment.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}
        self.pairs = [
            ("tsumori-selfview-local-expert", "tsumori-becoming-local-expert",
             ("専門家", "せんもんか"), "の", "に", "followed by の or になる"),
            ("tsumori-selfview-working-professional", "tsumori-becoming-photography-professional",
             ("プロ", "ぷろ"), "の", "に", "followed by の or になる"),
            ("tsumori-selfview-cooking-skill", "tsumori-becoming-better-cook",
             ("上手", "じょうず"), "な", "に", "followed by な or になる"),
            ("tsumori-selfview-careful-checking", "tsumori-becoming-more-careful",
             ("慎重", "しんちょう"), "な", "に", "followed by な or になる"),
            ("tsumori-selfview-local-history", "tsumori-becoming-history-knowledgeable",
             ("詳し", "くわし", "委し", "精し"), "い", "く", "its unchanged form, or its く form followed by なる"),
            ("tsumori-selfview-shogi-strength", "tsumori-becoming-stronger-shogi-player",
             ("強", "つよ"), "い", "く", "its unchanged form, or its く form followed by なる"),
        ]

    def test_six_matched_predicates_cover_both_functional_targets(self):
        self.assertEqual({
            "tsumori-current-selfview": 6,
            "tsumori-becoming-plan": 6,
        }, Counter(exercise["target"] for exercise in self.exercises.values()))
        relationship = self.data["relationships"][0]
        for self_id, plan_id, *_ in self.pairs:
            self.assertEqual("tsumori-current-selfview", self.exercises[self_id]["target"])
            self.assertEqual("tsumori-becoming-plan", self.exercises[plan_id]["target"])
            for exercise_id in (self_id, plan_id):
                exercise = self.exercises[exercise_id]
                self.assertEqual(relationship["id"], exercise["relationship"])
                self.assertEqual(
                    set(relationship["constructions"]),
                    {option["id"] for option in exercise["options"]}, exercise_id,
                )
            self.assertEqual(
                [option["label"] for option in self.exercises[self_id]["options"]],
                [option["label"] for option in self.exercises[plan_id]["options"]],
            )

    def test_attachment_and_spelling_sets_fit_only_the_missing_span(self):
        for self_id, plan_id, stems, self_ending, change_link, _ in self.pairs:
            self.assertEqual(
                {stem + self_ending for stem in stems},
                set(self.exercises[self_id]["acceptedAnswers"]), self_id,
            )
            self.assertEqual(
                {stem + change_link + verb for stem in stems for verb in ("なる", "成る", "為る")},
                set(self.exercises[plan_id]["acceptedAnswers"]), plan_id,
            )

    def test_the_same_present_ending_keeps_both_task_frames_visible(self):
        for self_id, plan_id, _, _, _, form_instruction in self.pairs:
            for exercise_id, focus in (
                (self_id, "State my current self-assessment, not a future change:"),
                (plan_id, "State an intended future change, not a current self-assessment:"),
            ):
                exercise = self.exercises[exercise_id]
                self.assertIn("____つもりです", exercise["prompt"], exercise_id)
                self.assertIn(form_instruction, exercise["translation"], exercise_id)
                self.assertIn("Fill only the part before the printed つもりです.", exercise["translation"], exercise_id)
                self.assertIn(focus, exercise["translation"], exercise_id)

    def test_selfviews_and_plans_keep_accuracy_and_outcome_qualifications(self):
        professional = self.exercises["tsumori-selfview-working-professional"]
        self.assertIn("依頼主もプロとして仕事を任せてくれます", professional["prompt"])
        self.assertIn("supports that view", professional["explanation"])
        self.assertIn("二度確認しています", self.exercises["tsumori-selfview-careful-checking"]["prompt"])
        self.assertIn("何度か優勝しました", self.exercises["tsumori-selfview-shogi-strength"]["prompt"])
        self.assertIn("味が濃すぎる", self.exercises["tsumori-selfview-cooking-skill"]["prompt"])
        self.assertIn("まだ知らない話", self.exercises["tsumori-selfview-local-history"]["prompt"])
        self.assertIn("not guarantee", self.exercises["tsumori-becoming-local-expert"]["explanation"])
        self.assertIn("not a guarantee of winning", self.exercises["tsumori-becoming-stronger-shogi-player"]["explanation"])


class GrammarIntentionDenialCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-intention-denial.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}
        self.future_pairs = [
            ("tsumori-negative-keep-guitar", "tsumori-affirmed-sell-guitar",
             ("売る", "うる"), ("売らない", "うらない")),
            ("tsumori-negative-own-camera", "tsumori-affirmed-borrow-camera",
             ("借りる", "かりる"), ("借りない", "かりない")),
            ("tsumori-negative-no-second-copy", "tsumori-affirmed-buy-dictionary",
             ("買う", "かう"), ("買わない", "かわない")),
        ]
        self.past_pairs = [
            ("tsumori-denied-accidental-file-deletion", "tsumori-affirmed-blocked-file-deletion", "消す"),
            ("tsumori-denied-accidental-vase-movement", "tsumori-affirmed-completed-vase-movement", "動かす"),
            ("tsumori-denied-needed-receipt-disposal", "tsumori-affirmed-unfinished-receipt-disposal", "捨てる"),
        ]

    def test_reciprocal_pairs_cover_all_four_functions(self):
        self.assertEqual({
            "tsumori-shared-negative-intent": 3,
            "tsumori-affirmed-future-intent": 3,
            "tsumori-denied-past-intent": 3,
            "tsumori-affirmed-past-intent": 3,
        }, Counter(exercise["target"] for exercise in self.exercises.values()))
        for negative_id, positive_id, *_ in self.future_pairs + self.past_pairs:
            negative = self.exercises[negative_id]
            positive = self.exercises[positive_id]
            self.assertEqual(negative["relationship"], positive["relationship"])
            self.assertNotEqual(negative["target"], positive["target"])
            self.assertEqual(
                [option["label"] for option in negative["options"]],
                [option["label"] for option in positive["options"]],
            )

    def test_negative_plans_and_denials_share_complete_visible_pattern_answers(self):
        for negative_id, positive_id, verbs, negatives in self.future_pairs:
            negative = self.exercises[negative_id]
            expected = {verb + "つもりだ" for verb in negatives}
            expected.update(
                verb + "つもり" + ending
                for verb in verbs for ending in ("はない", "がない", "ではない", "じゃない")
            )
            self.assertEqual(expected, set(negative["acceptedAnswers"]), negative_id)
            self.assertEqual(
                {verb + "つもりだ" for verb in verbs},
                set(self.exercises[positive_id]["acceptedAnswers"]), positive_id,
            )
            for exercise_id in (negative_id, positive_id):
                self.assertIn(
                    "Vるつもりだ, Vないつもりだ, or Vるつもりは／が／では／じゃない",
                    self.exercises[exercise_id]["translation"],
                )
                self.assertIn("Write つもり and the endings in kana.", self.exercises[exercise_id]["translation"])
            self.assertIn("つもりだ", negative["explanation"])
            self.assertIn("じゃない", negative["explanation"])

    def test_past_endings_keep_the_printed_intention_not_a_completion_belief(self):
        for negative_id, positive_id, verb in self.past_pairs:
            self.assertEqual(
                {"はなかった", "がなかった", "ではなかった", "じゃなかった"},
                set(self.exercises[negative_id]["acceptedAnswers"]), negative_id,
            )
            self.assertEqual(["だった"], self.exercises[positive_id]["acceptedAnswers"])
            for exercise_id in (negative_id, positive_id):
                exercise = self.exercises[exercise_id]
                self.assertIn(verb + "つもり____", exercise["prompt"], exercise_id)
                self.assertIn("だった, or は／が／では／じゃなかった", exercise["translation"], exercise_id)
                self.assertIn("Report my intention at that time, not a belief", exercise["translation"], exercise_id)

    def test_outcomes_do_not_determine_intention_polarity(self):
        self.assertIn("消してしまった", self.exercises["tsumori-denied-accidental-file-deletion"]["prompt"])
        self.assertIn("ずれてしまった", self.exercises["tsumori-denied-accidental-vase-movement"]["prompt"])
        self.assertIn("捨ててしまった", self.exercises["tsumori-denied-needed-receipt-disposal"]["prompt"])
        self.assertIn("今も残っている", self.exercises["tsumori-affirmed-blocked-file-deletion"]["prompt"])
        self.assertIn("予定どおりそこへ移した", self.exercises["tsumori-affirmed-completed-vase-movement"]["prompt"])
        self.assertIn("捨てられなかった", self.exercises["tsumori-affirmed-unfinished-receipt-disposal"]["prompt"])
        self.assertIn("does not require a failed plan", self.exercises["tsumori-affirmed-completed-vase-movement"]["explanation"])
        self.assertIn("cannot be inserted", self.exercises["tsumori-denied-needed-receipt-disposal"]["explanation"])


class GrammarStateChangeCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-state-change.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}
        self.pairs = [
            ("mama-retained-student-status", "naru-became-student",
             ("学生", "がくせい"), "の", "に", "noun"),
            ("mama-retained-vacant-lot", "naru-became-vacant-lot",
             ("空き地", "あきち", "空地", "明き地"), "の", "に", "noun"),
            ("mama-retained-quiet-library", "naru-became-quiet-classroom",
             ("静か", "しずか", "閑か"), "な", "に", "na"),
            ("mama-retained-clean-floor", "naru-became-clean-floor",
             ("きれい", "綺麗", "奇麗", "キレイ"), "な", "に", "na"),
            ("mama-retained-cold-water", "naru-became-cold-water",
             ("冷た", "つめた", "つべた"), "い", "く", "i"),
            ("mama-retained-high-price", "naru-became-higher-price",
             ("高", "たか"), "い", "く", "i"),
        ]

    def test_six_matched_pairs_cover_both_functions_and_three_word_classes(self):
        self.assertEqual({
            "mama-retained-predicate": 6, "naru-changed-predicate": 6,
        }, Counter(exercise["target"] for exercise in self.exercises.values()))
        self.assertEqual({"noun": 2, "na": 2, "i": 2}, Counter(pair[-1] for pair in self.pairs))
        for retained_id, changed_id, *_ in self.pairs:
            retained, changed = self.exercises[retained_id], self.exercises[changed_id]
            self.assertEqual("mama-retained-predicate", retained["target"])
            self.assertEqual("naru-changed-predicate", changed["target"])
            self.assertEqual(retained["relationship"], changed["relationship"])
            self.assertEqual(
                [option["label"] for option in retained["options"]],
                [option["label"] for option in changed["options"]],
            )

    def test_predicate_forms_keep_class_connectors_and_accepted_variants(self):
        for retained_id, changed_id, stems, retained_link, change_link, _ in self.pairs:
            self.assertEqual(
                {stem + retained_link + "ままだった" for stem in stems},
                set(self.exercises[retained_id]["acceptedAnswers"]), retained_id,
            )
            self.assertEqual(
                {stem + change_link + "なった" for stem in stems},
                set(self.exercises[changed_id]["acceptedAnswers"]), changed_id,
            )

    def test_question_side_names_the_basic_patterns_and_reference_focus(self):
        for retained_id, changed_id, _, retained_link, _, word_class in self.pairs:
            for exercise_id in (retained_id, changed_id):
                translation = self.exercises[exercise_id]["translation"]
                self.assertIn("Write the supplied endings in kana", translation, exercise_id)
                self.assertIn("Report", translation, exercise_id)
                if word_class == "i":
                    self.assertIn("unchanged + ままだった, or its く form + なった", translation, exercise_id)
                else:
                    self.assertIn(retained_link + "ままだった or になった", translation, exercise_id)
            self.assertIn("unchanged", self.exercises[retained_id]["translation"], retained_id)

    def test_retention_is_property_and_interval_specific_not_always_unwanted(self):
        student = self.exercises["mama-retained-student-status"]
        self.assertIn("二年生から三年生へ進級", student["prompt"])
        self.assertIn("every other detail", student["explanation"])
        self.assertIn("草は刈られていた", self.exercises["mama-retained-vacant-lot"]["prompt"])
        clean = self.exercises["mama-retained-clean-floor"]
        self.assertIn("今朝は泥の足跡がついている", clean["prompt"])
        self.assertIn("does not require the floor to remain clean now", clean["explanation"])
        self.assertIn("need not be an unwanted condition", self.exercises["mama-retained-quiet-library"]["explanation"])
        self.assertIn("not necessarily an oversight", self.exercises["mama-retained-cold-water"]["explanation"])
        self.assertIn("not an absence of human action", self.exercises["naru-became-clean-floor"]["explanation"])
        self.assertIn("different aspects and time intervals", self.exercises["naru-became-cold-water"]["explanation"])


class GrammarHokaExclusionCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-hoka-exclusion.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}
        self.group_pairs = [
            ("hoka-only-three-key-holders", "naka-none-of-three-key-holders", "この三人"),
            ("hoka-only-four-spanish-speakers", "uchi-none-of-four-spanish-speakers", "この四人"),
            ("hoka-only-two-library-books", "naka-neither-of-two-library-books", "右の二冊"),
        ]
        self.verb_pairs = [
            ("hoka-only-option-wait-for-entry", "koto-no-need-wait-after-call", "待つ"),
            ("shika-only-option-redo-file", "koto-no-need-redo-accepted-file", "やり直す"),
            ("hoka-only-option-borrow-dictionary", "koto-no-need-borrow-extra-dictionary", "借りる"),
        ]

    def test_reciprocal_pairs_cover_both_group_scopes_and_action_meanings(self):
        self.assertEqual({
            "hoka-outside-exclusion": 3, "naka-uchi-within-exclusion": 3,
            "hoka-shika-no-alternative": 3, "koto-unnecessary-action": 3,
        }, Counter(exercise["target"] for exercise in self.exercises.values()))
        for first_id, second_id, _ in self.group_pairs + self.verb_pairs:
            first, second = self.exercises[first_id], self.exercises[second_id]
            self.assertEqual(first["relationship"], second["relationship"])
            self.assertNotEqual(first["target"], second["target"])
            self.assertEqual(
                [option["label"] for option in first["options"]],
                [option["label"] for option in second["options"]],
            )

    def test_group_answers_preserve_shared_equivalents_and_printed_particles(self):
        for outside_id, inside_id, group in self.group_pairs:
            self.assertEqual({"ほか", "他", "外"}, set(self.exercises[outside_id]["acceptedAnswers"]))
            self.assertEqual({"なか", "中", "うち", "内"}, set(self.exercises[inside_id]["acceptedAnswers"]))
            for exercise_id in (outside_id, inside_id):
                exercise = self.exercises[exercise_id]
                self.assertIn(group + "の____には", exercise["prompt"])
                self.assertIn("ほか, なか or うち, in kana or kanji", exercise["translation"])
                self.assertIn("の and には are already printed", exercise["translation"])
        for exercise_id in ("hoka-only-two-library-books", "naka-neither-of-two-library-books"):
            self.assertIn("この机の本について言えば", self.exercises[exercise_id]["prompt"])
        for exercise_id in ("hoka-only-four-spanish-speakers", "uchi-none-of-four-spanish-speakers"):
            self.assertIn("この展示会のスタッフは八人", self.exercises[exercise_id]["prompt"])
        self.assertIn("separately establish", self.exercises["hoka-only-three-key-holders"]["explanation"])
        self.assertIn("does not itself assert", self.exercises["naka-neither-of-two-library-books"]["explanation"])

    def test_no_alternative_endings_share_all_named_variants_not_wrong_buttons(self):
        expected = {
            prefix + "ほか" + particle + "ない"
            for prefix in ("", "より") for particle in ("", "に", "は", "には")
        } | {"しかない"}
        models = set()
        for only_id, no_need_id, verb in self.verb_pairs:
            only = self.exercises[only_id]
            self.assertEqual(expected, set(only["acceptedAnswers"]), only_id)
            self.assertEqual(["ことはない"], self.exercises[no_need_id]["acceptedAnswers"])
            models.add(next(option["label"] for option in only["options"] if option["id"] == only["answer"]))
            for exercise_id in (only_id, no_need_id):
                exercise = self.exercises[exercise_id]
                self.assertIn(verb + "____", exercise["prompt"])
                self.assertIn("optional より before ほか and に／は／には after it", exercise["translation"])
                self.assertIn("しかない, or ことはない, in kana", exercise["translation"])
                self.assertEqual(
                    1, sum(option["label"] in exercise["acceptedAnswers"] for option in exercise["options"]),
                )
        self.assertEqual({"ほかない", "しかない", "よりほかない"}, models)

    def test_no_option_has_goal_scope_and_no_need_allows_optional_actions(self):
        for only_id, _, _ in self.verb_pairs:
            self.assertIn("には", self.exercises[only_id]["prompt"])
        self.assertIn("not a guarantee", self.exercises["shika-only-option-redo-file"]["explanation"])
        self.assertIn("need not imply resentment", self.exercises["hoka-only-option-borrow-dictionary"]["explanation"])
        wait = self.exercises["koto-no-need-wait-after-call"]
        self.assertIn("今すぐ入ってよい", wait["prompt"])
        self.assertIn("never happens", wait["explanation"])
        redo = self.exercises["koto-no-need-redo-accepted-file"]
        self.assertIn("任意の改善はしてもよい", redo["prompt"])
        self.assertIn("not a prohibition", redo["explanation"])
        borrow = self.exercises["koto-no-need-borrow-extra-dictionary"]
        self.assertIn("借りてもかまわない", borrow["prompt"])
        self.assertIn("neither forbids borrowing", borrow["explanation"])


class GrammarPastExpectationCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-past-expectation.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}
        self.time_pairs = [
            ("hazu-earlier-delivery-postponed", "hazu-current-delivery-inference",
             ("届く", "とどく"), ("届いた", "とどいた")),
            ("hazu-earlier-course-postponed", "hazu-current-course-start-inference",
             ("始まる", "はじまる"), ("始まった", "はじまった")),
            ("hazu-recalled-light-timer-fulfilled", "hazu-current-light-timer-inference",
             ("消える", "きえる"), ("消えた", "きえた")),
        ]
        self.polarity_pairs = [
            ("hazu-recalled-visitor-expected-come", "hazu-recalled-visitor-expected-absent",
             ("来る", "くる"), ("来ない", "こない")),
            ("hazu-recalled-chime-expected-sound", "hazu-recalled-chime-expected-silent",
             ("鳴る", "なる"), ("鳴らない", "ならない")),
            ("hazu-recalled-rain-expected", "hazu-recalled-rain-not-expected",
             ("降る", "ふる"), ("降らない", "ふらない")),
        ]

    def test_pairs_cover_both_time_viewpoints_and_both_expectation_polarities(self):
        self.assertEqual({
            "hazu-earlier-forward-expectation": 3, "hazu-current-past-inference": 3,
            "hazu-recalled-occurrence": 3, "hazu-recalled-nonoccurrence": 3,
        }, Counter(exercise["target"] for exercise in self.exercises.values()))
        for first_id, second_id, *_ in self.time_pairs + self.polarity_pairs:
            first, second = self.exercises[first_id], self.exercises[second_id]
            self.assertEqual(first["relationship"], second["relationship"])
            self.assertNotEqual(first["target"], second["target"])
            self.assertEqual(
                [option["label"] for option in first["options"]],
                [option["label"] for option in second["options"]],
            )

    def test_time_patterns_keep_event_form_distinct_from_expectation_ending(self):
        for earlier_id, current_id, dictionary, past in self.time_pairs:
            self.assertEqual(
                {verb + "はずだった" for verb in dictionary},
                set(self.exercises[earlier_id]["acceptedAnswers"]), earlier_id,
            )
            self.assertEqual(
                {verb + "はずだ" for verb in past},
                set(self.exercises[current_id]["acceptedAnswers"]), current_id,
            )
            for exercise_id in (earlier_id, current_id):
                self.assertIn(
                    "dictionary form + はずだった, or た form + はずだ",
                    self.exercises[exercise_id]["translation"],
                )
                self.assertIn("Write はず and the endings in kana", self.exercises[exercise_id]["translation"])
        self.assertIn("まだ受取人に確認していない", self.exercises["hazu-current-delivery-inference"]["prompt"])
        self.assertIn("記録はまだ見ていない", self.exercises["hazu-current-course-start-inference"]["prompt"])
        self.assertIn("does not say whether the lights remained off", self.exercises["hazu-current-light-timer-inference"]["explanation"])

    def test_polarity_tasks_keep_recollection_context_and_irregular_negative(self):
        for positive_id, negative_id, dictionary, negative in self.polarity_pairs:
            self.assertEqual(set(dictionary), set(self.exercises[positive_id]["acceptedAnswers"]))
            self.assertEqual(set(negative), set(self.exercises[negative_id]["acceptedAnswers"]))
            for exercise_id in (positive_id, negative_id):
                exercise = self.exercises[exercise_id]
                self.assertIn("____はずだった", exercise["prompt"])
                self.assertIn("思い出した", exercise["prompt"])
                self.assertIn("確か", exercise["prompt"])
                self.assertIn("Reconstruct the recalled expectation, not the eventual outcome", exercise["translation"])
        self.assertIn("not an instruction forbidding attendance", self.exercises["hazu-recalled-visitor-expected-absent"]["explanation"])
        self.assertIn("not a statement that the equipment was incapable", self.exercises["hazu-recalled-chime-expected-silent"]["explanation"])

    def test_fulfilled_and_contradicted_outcomes_do_not_determine_expectation(self):
        fulfilled = self.exercises["hazu-recalled-light-timer-fulfilled"]
        self.assertIn("昨日の朝、開館前", fulfilled["prompt"])
        self.assertIn("思い出した", fulfilled["prompt"])
        self.assertIn("確か", fulfilled["prompt"])
        self.assertIn("実際に昨日の六時に消えていた", fulfilled["prompt"])
        self.assertIn("not evidence that every isolated", fulfilled["explanation"])
        for exercise_id in ("hazu-recalled-visitor-expected-come", "hazu-recalled-visitor-expected-absent"):
            self.assertIn("佐藤さんは会議に来た", self.exercises[exercise_id]["prompt"])
        self.assertIn("実際には鳴らなかった", self.exercises["hazu-recalled-chime-expected-sound"]["prompt"])
        self.assertIn("実際、チャイムは鳴らず", self.exercises["hazu-recalled-chime-expected-silent"]["prompt"])
        self.assertIn("雨が降り始めた", self.exercises["hazu-recalled-rain-expected"]["prompt"])
        self.assertIn("雨は一滴も降らなかった", self.exercises["hazu-recalled-rain-not-expected"]["prompt"])


class GrammarPossibleExtentCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-possible-extent.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}
        self.pairs = [
            ("extent-possible-reading-access", "extent-wanted-reading-choice",
             ("読める", "よめる"), ("読みたい", "よみたい")),
            ("extent-possible-writing-space", "extent-wanted-writing-choice",
             ("書ける", "かける"), ("書きたい", "かきたい")),
            ("extent-possible-transport-capacity", "extent-wanted-transport-choice",
             ("運べる", "はこべる"), ("運びたい", "はこびたい")),
            ("extent-possible-paper-supply", "extent-wanted-paper-choice",
             ("使える", "つかえる", "遣える"), ("使いたい", "つかいたい", "遣いたい")),
            ("extent-possible-photo-service", "extent-wanted-photo-selection",
             ("送れる", "おくれる"), ("送りたい", "おくりたい")),
            ("extent-possible-speaking-slot", "extent-wanted-speaking-choice",
             ("話せる", "はなせる", "咄せる"), ("話したい", "はなしたい", "咄したい")),
        ]

    def test_six_reciprocal_pairs_share_possible_extent_not_rival_particles(self):
        self.assertEqual({
            "kagiri-dake-possible-extent": 6, "dake-wanted-extent": 6,
        }, Counter(exercise["target"] for exercise in self.exercises.values()))
        models = []
        for possible_id, wanted_id, *_ in self.pairs:
            possible, wanted = self.exercises[possible_id], self.exercises[wanted_id]
            self.assertEqual(possible["relationship"], wanted["relationship"])
            self.assertNotEqual(possible["target"], wanted["target"])
            self.assertEqual(
                [option["label"] for option in possible["options"]],
                [option["label"] for option in wanted["options"]],
            )
            model = next(option["label"] for option in possible["options"] if option["id"] == possible["answer"])
            models.append("かぎり" if model.endswith("かぎり") else "だけ")
            for exercise in (possible, wanted):
                self.assertEqual(1, sum(option["label"] in exercise["acceptedAnswers"] for option in exercise["options"]))
        self.assertEqual({"かぎり": 3, "だけ": 3}, Counter(models))

    def test_all_supported_verb_and_particle_forms_fit_the_named_patterns(self):
        for possible_id, wanted_id, potentials, desires in self.pairs:
            self.assertEqual(
                {verb + particle for verb in potentials for particle in ("かぎり", "限り", "だけ", "丈")},
                set(self.exercises[possible_id]["acceptedAnswers"]), possible_id,
            )
            self.assertEqual(
                {verb + particle for verb in desires for particle in ("だけ", "丈")},
                set(self.exercises[wanted_id]["acceptedAnswers"]), wanted_id,
            )
            for exercise_id in (possible_id, wanted_id):
                translation = self.exercises[exercise_id]["translation"]
                self.assertIn("nonpast potential + かぎり or だけ, or たい form + だけ", translation)
                self.assertIn("do not repeat the following verb", translation)

    def test_contexts_keep_available_extent_distinct_from_desired_amount(self):
        possible = self.exercises["extent-possible-reading-access"]
        wanted = self.exercises["extent-wanted-reading-choice"]
        self.assertIn("三話全部を読み終えた", possible["prompt"])
        self.assertIn("まだ続きも読みたい", possible["prompt"])
        self.assertIn("今日は全部読める", wanted["prompt"])
        self.assertIn("三話で満足", wanted["prompt"])
        self.assertIn("書きたいことはまだ残っている", self.exercises["extent-possible-writing-space"]["prompt"])
        self.assertIn("五行書ける", self.exercises["extent-wanted-writing-choice"]["prompt"])
        self.assertIn("今日は一往復しかできない", self.exercises["extent-possible-transport-capacity"]["prompt"])
        self.assertIn("全部車に入る", self.exercises["extent-wanted-transport-choice"]["prompt"])
        self.assertIn("あと二十枚使いたかった", self.exercises["extent-possible-paper-supply"]["prompt"])
        self.assertIn("紙はまだ四十枚残っている", self.exercises["extent-wanted-paper-choice"]["prompt"])
        self.assertIn("残りも早く送りたい", self.exercises["extent-possible-photo-service"]["prompt"])
        self.assertIn("写真も十枚用意してある", self.exercises["extent-wanted-photo-selection"]["prompt"])
        self.assertIn("話したいことはまだたくさん残った", self.exercises["extent-possible-speaking-slot"]["prompt"])
        self.assertIn("三分で満足", self.exercises["extent-wanted-speaking-choice"]["prompt"])

    def test_extent_feedback_qualifies_scope_not_global_substitution_or_smallness(self):
        self.assertIn("not a promise to keep reading", self.exercises["extent-possible-reading-access"]["explanation"])
        self.assertIn("not the writer's general ability", self.exercises["extent-possible-writing-space"]["explanation"])
        self.assertIn("not the paper's useful lifetime", self.exercises["extent-possible-paper-supply"]["explanation"])
        self.assertIn("does not always mean a small amount", self.exercises["extent-wanted-paper-choice"]["explanation"])
        self.assertIn("not a claim that no other communication method exists", self.exercises["extent-possible-photo-service"]["explanation"])
        self.assertIn("does not require the fastest physically possible speech", self.exercises["extent-possible-speaking-slot"]["explanation"])
        self.assertIn("can sometimes describe the same actual amount", self.exercises["extent-wanted-speaking-choice"]["explanation"])


class GrammarKuraiDegreeMinimumCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "particle-kurai-degree-minimum.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_each_degree_or_minimum_group_has_reciprocal_counterexpectations(self):
        expected = {
            "illustrative-degree-vs-counterexpectation": {
                "kurai-hodo-illustrative-degree": 3, "noni-counterexpectation": 3,
            },
            "low-bar-vs-counterexpectation": {
                "kurai-low-bar": 3, "noni-counterexpectation": 3,
            },
        }
        for relationship, counts in expected.items():
            self.assertEqual(counts, Counter(
                exercise["target"] for exercise in self.exercises.values()
                if exercise["relationship"] == relationship
            ))
        for minimum, concession, noun in [
            ("kurai-minimum-own-name", "noni-own-name-field-mistake", "自分の名前"),
            ("kurai-minimum-practiced-greeting", "noni-practiced-greeting-hesitation", "短い挨拶"),
            ("kurai-minimum-familiar-tea", "noni-familiar-tea-different-taste", "お茶"),
        ]:
            for exercise_id in (minimum, concession):
                self.assertIn(noun + "____", self.exercises[exercise_id]["prompt"])

    def test_shared_spellings_optional_topic_and_noun_connector_fit_visible_tasks(self):
        for exercise in self.exercises.values():
            if exercise["target"] == "kurai-hodo-illustrative-degree":
                expected = {"くらい", "ぐらい", "位", "ほど", "程"}
            elif exercise["target"] == "kurai-low-bar":
                expected = {"くらい", "ぐらい", "位", "くらいは", "ぐらいは", "位は"}
            elif exercise["relationship"] == "low-bar-vs-counterexpectation":
                expected = {"なのに"}
            else:
                expected = {"のに"}
            self.assertEqual(expected, set(exercise["acceptedAnswers"]), exercise["id"])
            self.assertEqual(1, sum(
                option["label"] in expected for option in exercise["options"]
            ), exercise["id"])
            if exercise["relationship"] == "illustrative-degree-vs-counterexpectation":
                self.assertIn("bare くらい／ぐらい／ほど or connective のに", exercise["translation"])
                self.assertIn("do not add は", exercise["translation"])
            else:
                self.assertIn("with or without は", exercise["translation"])
                self.assertIn("plain noun-predicate ending なのに", exercise["translation"])
        tea = self.exercises["kurai-minimum-familiar-tea"]
        self.assertEqual("くらい", next(option["label"] for option in tea["options"] if option["id"] == tea["answer"]))

    def test_context_and_feedback_preserve_degree_stance_and_favorable_contrast(self):
        self.assertIn("熱気で寝つくのに時間がかかった", self.exercises["kurai-degree-muggy-bedroom"]["prompt"])
        self.assertIn("くらい does not mean", self.exercises["kurai-degree-muggy-bedroom"]["explanation"])
        self.assertIn("not proof that repeated viewings actually happened", self.exercises["kurai-degree-beautiful-video"]["explanation"])
        self.assertIn("私には難しくない", self.exercises["kurai-minimum-own-name"]["prompt"])
        self.assertIn("not necessarily for everyone", self.exercises["kurai-minimum-own-name"]["explanation"])
        self.assertIn("or impose a numerical lower bound", self.exercises["kurai-minimum-own-name"]["explanation"])
        self.assertIn("reproachful", self.exercises["kurai-minimum-practiced-greeting"]["explanation"])
        self.assertIn("慣れている", self.exercises["kurai-minimum-familiar-tea"]["prompt"])
        self.assertIn("helpful outcome", self.exercises["noni-voiceless-written-help"]["explanation"])
        self.assertIn("not a scientific claim", self.exercises["noni-familiar-tea-different-taste"]["explanation"])


class GrammarMixedRoutinesCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-mixed-routines.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_full_ending_selection_uses_one_common_pool_and_three_way_options(self):
        targets = {"mixed-changed-routine", "mixed-maintained-practice", "mixed-current-inference"}
        self.assertEqual({target: 4 for target in targets}, Counter(
            exercise["target"] for exercise in self.exercises.values()
        ))
        for topic in ("reading", "writing", "using", "speaking"):
            self.assertEqual(targets, {
                exercise["target"] for exercise in self.exercises.values()
                if exercise["id"].split("-")[2] == topic
            })
        instruction = (
            "Choose an appropriate form of ようになる, ようにする, ことにする, はずだ or ようだ. "
            "Fill the whole ending in hiragana, using one complete, uncontracted plain-form construction; "
            "keep any copula and do not add particles or auxiliary constructions. "
        )
        for exercise in self.exercises.values():
            self.assertTrue(exercise["translation"].startswith(instruction), exercise["id"])
            self.assertRegex(exercise["prompt"], r"(読む|書く|使う|話す)____。$")
            self.assertEqual(targets, {option["id"] for option in exercise["options"]})
            self.assertEqual("routine-change-practice-inference", exercise["relationship"])

    def test_shared_full_predicates_are_not_competing_wrong_buttons(self):
        answers = {
            "mixed-changed-routine": {"ようになった", "ようになっている"},
            "mixed-maintained-practice": {"ようにしている", "ことにしている", "ようにする"},
            "mixed-current-inference": {"はずだ", "ようだ", "はずである", "ようである"},
        }
        models = {target: set() for target in answers}
        for exercise in self.exercises.values():
            accepted = answers[exercise["target"]]
            self.assertEqual(accepted, set(exercise["acceptedAnswers"]), exercise["id"])
            self.assertEqual(1, sum(option["label"] in accepted for option in exercise["options"]), exercise["id"])
            model = next(option["label"] for option in exercise["options"] if option["id"] == exercise["answer"])
            models[exercise["target"]].add(model)
        self.assertEqual({"ようにしている", "ことにしている"}, models["mixed-maintained-practice"])
        self.assertEqual({"はずだ", "ようだ"}, models["mixed-current-inference"])
        self.assertEqual({"ようになった", "ようになっている"}, models["mixed-changed-routine"])

    def test_contexts_do_not_confuse_change_intention_evidence_and_perfect_success(self):
        diary = self.exercises["mixed-change-writing-established-diary"]
        self.assertIn("自分で決めて毎晩続けた結果", diary["prompt"])
        self.assertIn("なる does not mean nobody acted intentionally", diary["explanation"])
        self.assertIn("英語は以前から話せた", self.exercises["mixed-change-speaking-meeting-language"]["prompt"])
        for exercise_id, lapse in {
            "mixed-practice-reading-meeting-materials": "うっかり読み忘れる日もある",
            "mixed-practice-writing-ideas": "まだ忘れることもある",
            "mixed-practice-using-cloth-bag": "持っていくのを忘れることもある",
            "mixed-practice-speaking-conclusion-first": "細かい話から始めてしまうこともある",
        }.items():
            self.assertIn("以前から", self.exercises[exercise_id]["prompt"])
            self.assertIn(lapse, self.exercises[exercise_id]["prompt"])
        self.assertIn("Publication times do not guarantee writing times", self.exercises["mixed-inference-writing-public-diary"]["explanation"])
        self.assertIn("本人の方針やすべての買い物を確認したわけではない", self.exercises["mixed-inference-using-filled-cloth-bag"]["prompt"])
        self.assertIn("本人の方針やほかの場面は知らない", self.exercises["mixed-inference-speaking-recordings"]["prompt"])


class GrammarMixedCompletionStateCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-mixed-completion-state.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_shared_past_verbs_leave_the_whole_construction_to_choose(self):
        targets = {"mixed-recent-completion", "mixed-retained-result", "mixed-past-action-inference"}
        instruction = (
            "Choose an appropriate form of ところだ, ばかりだ, ままだ, はずだ or ようだ. "
            "Fill the whole ending in hiragana, using one complete, uncontracted plain-form construction; "
            "keep the copula and do not add particles or auxiliary constructions. "
        )
        for topic, verb in {"window": "開けた", "lights": "消した", "materials": "置いた", "coat": "掛けた"}.items():
            group = [exercise for exercise in self.exercises.values() if exercise["id"].endswith("-" + topic)]
            self.assertEqual(3, len(group), topic)
            self.assertEqual(targets, {exercise["target"] for exercise in group}, topic)
            for exercise in group:
                self.assertTrue(exercise["prompt"].endswith(verb + "____。"), exercise["id"])
                self.assertTrue(exercise["translation"].startswith(instruction), exercise["id"])
                self.assertEqual(targets, {option["id"] for option in exercise["options"]}, exercise["id"])

    def test_completion_and_inference_alternatives_share_one_correct_button(self):
        answers = {
            "mixed-recent-completion": {"ところだ", "ばかりだ", "ところである", "ばかりである"},
            "mixed-retained-result": {"ままだ", "ままである"},
            "mixed-past-action-inference": {"はずだ", "ようだ", "はずである", "ようである"},
        }
        models = {target: set() for target in answers}
        for exercise in self.exercises.values():
            accepted = answers[exercise["target"]]
            self.assertEqual(accepted, set(exercise["acceptedAnswers"]), exercise["id"])
            self.assertEqual(1, sum(option["label"] in accepted for option in exercise["options"]), exercise["id"])
            models[exercise["target"]].add(next(
                option["label"] for option in exercise["options"] if option["id"] == exercise["answer"]
            ))
        self.assertEqual({"ところだ", "ばかりだ"}, models["mixed-recent-completion"])
        self.assertEqual({"ままだ"}, models["mixed-retained-result"])
        self.assertEqual({"はずだ", "ようだ"}, models["mixed-past-action-inference"])

    def test_persistence_is_not_elapsed_time_repetition_or_complete_unchangeability(self):
        for exercise_id in ("mixed-completion-window", "mixed-retained-window"):
            self.assertIn("数秒前", self.exercises[exercise_id]["prompt"])
        self.assertIn("still left open", self.exercises["mixed-retained-window"]["translation"])
        self.assertIn("a week is not a universal disqualifier", self.exercises["mixed-retained-materials"]["explanation"])
        self.assertIn("lights remain off", self.exercises["mixed-retained-lights"]["translation"])
        self.assertIn("not necessarily careless", self.exercises["mixed-retained-lights"]["explanation"])
        self.assertIn("夕方の今も少し湿っている", self.exercises["mixed-retained-coat"]["prompt"])
        self.assertIn("every other property", self.exercises["mixed-retained-coat"]["explanation"])
        self.assertIn("not a guarantee", self.exercises["mixed-past-inference-coat"]["explanation"])
        self.assertIn("正確な時刻は確認していない", self.exercises["mixed-past-inference-materials"]["prompt"])
        self.assertIn("current inference", self.exercises["mixed-past-inference-lights"]["explanation"])


class GrammarMixedIntentionNecessityCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-mixed-intention-necessity.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_shared_verbs_use_the_same_whole_ending_selection_task(self):
        targets = {"mixed-current-intention", "mixed-unnecessary-action", "mixed-only-available-option"}
        instruction = (
            "Choose a complete plain nonpast ending from つもりだ, ことはない, 必要ない／必要はない／必要がない, "
            "ほかない or しかない. Write it in hiragana. For つもり, である is also allowed; for ほか, "
            "より before it and に／は／には after it are optional. "
            "Use no contractions or other added particles or auxiliary constructions. "
        )
        for topic, verb in {"send": "送る", "borrow": "借りる", "wait": "待つ", "redo": "やり直す"}.items():
            group = [exercise for exercise in self.exercises.values() if exercise["id"].endswith("-" + topic)]
            self.assertEqual(3, len(group), topic)
            self.assertEqual(targets, {exercise["target"] for exercise in group}, topic)
            for exercise in group:
                self.assertIn(verb + "____。", exercise["prompt"], exercise["id"])
                self.assertTrue(exercise["translation"].startswith(instruction), exercise["id"])
                self.assertEqual(targets, {option["id"] for option in exercise["options"]}, exercise["id"])

    def test_no_need_and_no_alternative_variants_are_not_wrong_buttons(self):
        answers = {
            "mixed-current-intention": {"つもりだ", "つもりである"},
            "mixed-unnecessary-action": {"ことはない", "ひつようない", "ひつようはない", "ひつようがない"},
            "mixed-only-available-option": {
                prefix + "ほか" + particle + "ない"
                for prefix in ("", "より") for particle in ("", "に", "は", "には")
            } | {"しかない"},
        }
        models = {target: set() for target in answers}
        for exercise in self.exercises.values():
            accepted = answers[exercise["target"]]
            self.assertEqual(accepted, set(exercise["acceptedAnswers"]), exercise["id"])
            self.assertEqual(1, sum(option["label"] in accepted for option in exercise["options"]), exercise["id"])
            models[exercise["target"]].add(next(
                option["label"] for option in exercise["options"] if option["id"] == exercise["answer"]
            ))
        self.assertEqual({"つもりだ"}, models["mixed-current-intention"])
        self.assertEqual({"ことはない", "ひつようはない", "ひつようがない"}, models["mixed-unnecessary-action"])
        self.assertEqual({"ほかない", "しかない", "よりほかない", "ほかにはない"}, models["mixed-only-available-option"])

    def test_optional_intentions_and_goal_relative_constraints_remain_distinct(self):
        self.assertIn("紙の書類を追加で出すかどうかは自由", self.exercises["mixed-plan-send"]["prompt"])
        self.assertIn("提出し直す必要はない", self.exercises["mixed-plan-redo"]["prompt"])
        self.assertIn("Optionality for one goal does not rule out necessity for another", self.exercises["mixed-plan-send"]["explanation"])
        self.assertIn("may not achieve the new artistic goal", self.exercises["mixed-plan-redo"]["explanation"])
        self.assertIn("送ってもかまわない", self.exercises["mixed-no-need-send"]["prompt"])
        self.assertIn("借りてもかまわない", self.exercises["mixed-no-need-borrow"]["prompt"])
        self.assertIn("そのままいてもよい", self.exercises["mixed-no-need-wait"]["prompt"])
        self.assertIn("待たずにほかの作業に移ってよい", self.exercises["mixed-no-need-wait"]["prompt"])
        self.assertIn("好みで整理するのは自由", self.exercises["mixed-no-need-redo"]["prompt"])
        self.assertIn("ほかの展示を見てから戻ってもよい", self.exercises["mixed-plan-wait"]["prompt"])
        self.assertIn("unavoidable passage of time", self.exercises["mixed-plan-wait"]["explanation"])
        self.assertIn("can do unrelated tasks", self.exercises["mixed-only-option-wait"]["explanation"])
        self.assertIn("Choosing not to exhibit", self.exercises["mixed-only-option-borrow"]["explanation"])
        self.assertIn("does not guarantee", self.exercises["mixed-only-option-redo"]["explanation"])


class GrammarMixedPastStanceCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-mixed-past-stance.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_shared_verbs_leave_the_whole_predicate_and_viewpoint_to_choose(self):
        targets = {"mixed-earlier-intention", "mixed-earlier-completion-belief", "mixed-current-completion-inference"}
        instruction = (
            "Complete the whole predicate using the supplied verb: dictionary form + つもりだった, "
            "た-form + つもりだった, or た-form + はずだ／ようだ. Write the verb and ending in hiragana. "
            "You may replace だった with であった and だ with である. "
            "Use no contractions, added particles or other auxiliary constructions. "
        )
        for topic, verb in {
            "save": "保存する（ほぞんする）", "lock": "掛ける（かける）",
            "pay": "払う（はらう）", "reserve": "予約する（よやくする）",
        }.items():
            group = [exercise for exercise in self.exercises.values() if exercise["id"].endswith("-" + topic)]
            self.assertEqual(3, len(group), topic)
            self.assertEqual(targets, {exercise["target"] for exercise in group}, topic)
            for exercise in group:
                self.assertTrue(exercise["prompt"].startswith("【動詞：" + verb + "】\n"), exercise["id"])
                self.assertIn("を____。", exercise["prompt"], exercise["id"])
                self.assertNotIn("つもり", exercise["prompt"], exercise["id"])
                self.assertNotIn("はず", exercise["prompt"], exercise["id"])
                self.assertTrue(exercise["translation"].startswith(instruction), exercise["id"])
                self.assertEqual(targets, {option["id"] for option in exercise["options"]}, exercise["id"])

    def test_complete_predicates_keep_all_named_copulas_and_shared_inferences(self):
        models = set()
        for topic, (dictionary, past) in {
            "save": ("ほぞんする", "ほぞんした"), "lock": ("かける", "かけた"),
            "pay": ("はらう", "はらった"), "reserve": ("よやくする", "よやくした"),
        }.items():
            answers = {
                "mixed-earlier-plan-": {dictionary + ending for ending in ("つもりだった", "つもりであった")},
                "mixed-earlier-belief-": {past + ending for ending in ("つもりだった", "つもりであった")},
                "mixed-now-inference-": {past + ending for ending in ("はずだ", "ようだ", "はずである", "ようである")},
            }
            for prefix, accepted in answers.items():
                exercise = self.exercises[prefix + topic]
                self.assertEqual(accepted, set(exercise["acceptedAnswers"]), exercise["id"])
                self.assertEqual(1, sum(option["label"] in accepted for option in exercise["options"]), exercise["id"])
                if prefix == "mixed-now-inference-":
                    model = next(option["label"] for option in exercise["options"] if option["id"] == exercise["answer"])
                    models.add(model.removeprefix(past))
        self.assertEqual({"はずだ", "ようだ"}, models)

    def test_outcomes_and_first_person_do_not_replace_the_attitude_distinction(self):
        self.assertIn("実際に夕方までに保存し", self.exercises["mixed-earlier-plan-save"]["prompt"])
        self.assertIn("予定どおり自分で払い", self.exercises["mixed-earlier-plan-pay"]["prompt"])
        self.assertIn("鍵を掛けないまま", self.exercises["mixed-earlier-plan-lock"]["prompt"])
        self.assertIn("その日は予約しなかった", self.exercises["mixed-earlier-plan-reserve"]["prompt"])
        self.assertIn("実際には保存されていなかった", self.exercises["mixed-earlier-belief-save"]["prompt"])
        self.assertIn("払ったのは教材費だけ", self.exercises["mixed-earlier-belief-pay"]["prompt"])
        self.assertIn("やはり鍵は掛かっていた", self.exercises["mixed-earlier-belief-lock"]["prompt"])
        self.assertIn("その部屋と日付が正しく載っていた", self.exercises["mixed-earlier-belief-reserve"]["prompt"])
        for topic in ("save", "pay"):
            inference = self.exercises["mixed-now-inference-" + topic]
            self.assertIn("覚えていない", inference["prompt"])
            self.assertIn("今", inference["prompt"])
            self.assertIn("私は", inference["prompt"])
        self.assertIn("not a guarantee", self.exercises["mixed-now-inference-lock"]["explanation"])
        self.assertIn("not the requested recollection", self.exercises["mixed-earlier-belief-reserve"]["options"][2]["rationale"])


class GrammarMixedNormsExpectationsCoverageTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / "grammar" / "formal-nouns-mixed-norms-expectations.json").read_text(encoding="utf-8"))
        self.exercises = {exercise["id"]: exercise for exercise in self.data["exercises"]}

    def test_common_pool_and_full_predicate_across_matched_verbs(self):
        targets = {"mixed-normative-judgment", "mixed-predicted-action", "mixed-goal-relative-necessity"}
        instruction = (
            "Complete the whole predicate in hiragana using the supplied verb + "
            "べきだ／ものだ／はずだ／ようだ／ほかない／しかない. "
            "You may use である for だ and すべき for するべき; with ほかない, "
            "より before ほか and に／は／には after it are optional. "
            "Use no other added particles, contractions, auxiliaries or tense changes. "
        )
        for topic, verb in {
            "return": "返す（かえす）", "wait": "待つ（まつ）",
            "contact": "連絡する（れんらくする）", "redo": "やり直す（やりなおす）",
        }.items():
            group = [exercise for exercise in self.exercises.values() if exercise["id"].endswith("-" + topic)]
            self.assertEqual(3, len(group), topic)
            self.assertEqual(targets, {exercise["target"] for exercise in group}, topic)
            for exercise in group:
                self.assertTrue(exercise["prompt"].startswith("【動詞：" + verb + "】\n"), exercise["id"])
                self.assertEqual(1, exercise["prompt"].count("____"), exercise["id"])
                self.assertIn("____。", exercise["prompt"], exercise["id"])
                self.assertTrue(exercise["translation"].startswith(instruction), exercise["id"])
                self.assertEqual(targets, {option["id"] for option in exercise["options"]}, exercise["id"])

    def test_all_equivalents_fit_whole_predicates_including_su_beki(self):
        hoka = {yori + "ほか" + particle + "ない" for yori in ("", "より") for particle in ("", "に", "は", "には")}
        prediction_models = set()
        for topic, verb in {
            "return": "かえす", "wait": "まつ", "contact": "れんらくする", "redo": "やりなおす",
        }.items():
            normative = {verb + base + copula for base in ("べき", "もの") for copula in ("だ", "である")}
            if topic == "contact":
                normative |= {"れんらくすべきだ", "れんらくすべきである"}
            answers = {
                "mixed-norm-": normative,
                "mixed-prediction-": {verb + base + copula for base in ("はず", "よう") for copula in ("だ", "である")},
                "mixed-necessary-": {verb + ending for ending in hoka | {"しかない"}},
            }
            for prefix, accepted in answers.items():
                exercise = self.exercises[prefix + topic]
                self.assertEqual(accepted, set(exercise["acceptedAnswers"]), exercise["id"])
                self.assertEqual(1, sum(option["label"] in accepted for option in exercise["options"]), exercise["id"])
                if prefix == "mixed-prediction-":
                    model = next(option["label"] for option in exercise["options"] if option["id"] == exercise["answer"])
                    prediction_models.add(model.removeprefix(verb))
        self.assertEqual({"はずだ", "ようだ"}, prediction_models)

    def test_compliance_and_opt_out_do_not_replace_message_or_goal(self):
        self.assertIn("過ぎても本を返していない", self.exercises["mixed-norm-return"]["prompt"])
        self.assertIn("そのまま次へ進んでしまう", self.exercises["mixed-norm-redo"]["prompt"])
        self.assertIn("全員が最後まで静かに", self.exercises["mixed-norm-wait"]["prompt"])
        self.assertIn("全員、事前に知らせていた", self.exercises["mixed-norm-contact"]["prompt"])
        self.assertIn("約束の日", self.exercises["mixed-prediction-return"]["prompt"])
        self.assertIn("決まりがある", self.exercises["mixed-prediction-contact"]["prompt"])
        self.assertIn("連絡先を開いている", self.exercises["mixed-prediction-contact"]["prompt"])
        self.assertIn("まだ貸出期間内", self.exercises["mixed-necessary-return"]["prompt"])
        self.assertIn("外で用事を済ませてもよく", self.exercises["mixed-necessary-wait"]["prompt"])
        self.assertIn("別の部屋を選んでもよい", self.exercises["mixed-necessary-contact"]["prompt"])
        redo = self.exercises["mixed-necessary-redo"]
        self.assertIn("できず、コピーもない", redo["prompt"])
        self.assertIn("応募をやめることもできる", redo["prompt"])
        self.assertIn("最初から____", redo["prompt"])
        self.assertIn("その部分の録音を____", self.exercises["mixed-norm-redo"]["prompt"])
        self.assertIn("not proof", self.exercises["mixed-prediction-contact"]["explanation"])
        self.assertIn("does not establish", self.exercises["mixed-prediction-redo"]["options"][2]["rationale"])


if __name__ == "__main__":
    unittest.main()
