import unittest

import run_b133_closure_checks as checks
from verify_b133_sources import FINGERPRINT, OWNER, TRAILER

C = checks.CANDIDATE
A = "a" * 40
B = "b" * 40
BODY = b"Fix\n\n" + TRAILER + b"\n"


def row(commit, parent, status="G", fingerprint=FINGERPRINT, author=OWNER, committer=OWNER):
    return f"{commit}|{parent}|{status}|{fingerprint}|{author}|{committer}"


class Lineage(unittest.TestCase):
    def test_accepts_unchanged_candidate_and_linear_signed_descendants(self):
        self.assertEqual(checks.validate_lineage([], [], C, C), 0)
        self.assertEqual(checks.validate_lineage([row(A, C), row(B, A)], [BODY, BODY], C, B), 2)

    def test_rejects_untrusted_or_nonlinear_lineage(self):
        cases = {
            "not linear": ([row(A, C), row(B, C)], [BODY, BODY], B),
            "merge": ([row(A, f"{C} {B}")], [BODY], A),
            "unsigned": ([row(A, C, status="N")], [BODY], A),
            "other key": ([row(A, C, fingerprint="0" * 40)], [BODY], A),
            "other author": ([row(A, C, author="romanko-ms@example.com")], [BODY], A),
            "other committer": ([row(A, C, committer="romanko-ms@example.com")], [BODY], A),
            "trailer": ([row(A, C)], [b"Fix\n"], A),
            "wrong end": ([row(A, C)], [BODY], B),
            "unchanged but claimed descendant": ([], [], A),
            "short id": ([], [], C[:8]),
        }
        for name, (rows, bodies, reviewed) in cases.items():
            with self.subTest(name), self.assertRaises(Exception):
                checks.validate_lineage(rows, bodies, C, reviewed)

    def test_rejects_bad_cli_output_before_running(self):
        for mode, output in (("author", checks.HERE / "x-new"), ("closure", checks.HERE / "review" / "x")):
            with self.subTest(mode=mode, output=str(output)), self.assertRaises(Exception):
                checks.main(mode, C, C, output)


if __name__ == "__main__":
    unittest.main()
