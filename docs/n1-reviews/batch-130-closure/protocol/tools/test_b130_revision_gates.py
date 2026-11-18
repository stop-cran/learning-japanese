import copy
import json
import unittest

from b130_revision_gates import HERE, PARENT, check_context, commands, verify, verify_execution


class Guard:
    def check(self):
        pass


class B130RevisionGateTests(unittest.TestCase):
    def setUp(self):
        self.directory = HERE / "reconciliation-author-gates-002"
        self.summary = json.loads((self.directory / "summary.json").read_bytes())
        self.admission = json.loads((self.directory / "admission.json").read_bytes())
        self.candidate = "1" * 40
        self.args = (self.candidate, self.summary["manifestSha256"], self.summary["runnerSha256"],
                     self.summary["gateImplementationSha256"], self.summary["commonHelperSha256"])

    def test_actual_author_gates_have_distinct_wrapper_and_implementation_binding(self):
        self.assertNotEqual(self.args[2], self.args[3])
        record, captured = verify(self.directory, "author", *self.args, Guard())
        self.assertEqual(len(record["gates"]), 10)
        self.assertEqual(len(captured), 22)

    def test_wrong_parent_relabelled_committed_gate_or_swapped_runner_is_rejected(self):
        for field, value in (("parent", "0" * 40), ("publishedBase", PARENT),
                             ("mode", "committed"),
                             ("gateImplementationSha256", self.summary["runnerSha256"])):
            with self.subTest(field=field):
                summary = copy.deepcopy(self.summary)
                summary[field] = value
                with self.assertRaises(ValueError):
                    check_context(summary, self.admission, "author", *self.args)
        with self.assertRaises(ValueError):
            check_context(self.summary, self.admission, "committed", *self.args)

    def test_narrowed_base_command_or_overlapping_execution_is_rejected(self):
        receipts = {name: json.loads((self.directory / (name + ".json")).read_bytes())
                    for name in commands()}
        narrowed = copy.deepcopy(receipts)
        narrowed["lint"]["command"][5] = PARENT
        with self.assertRaises(ValueError):
            verify_execution(narrowed, commands(), self.args[-1])
        overlap = copy.deepcopy(receipts)
        overlap["quiz-safety"]["startedAt"] = overlap["lint"]["startedAt"]
        with self.assertRaises(ValueError):
            verify_execution(overlap, commands(), self.args[-1])


if __name__ == "__main__":
    unittest.main()
