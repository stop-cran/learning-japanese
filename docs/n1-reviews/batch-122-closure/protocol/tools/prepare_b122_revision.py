"""Derive B122 verification from the frozen, tested B121 revision checks."""
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).resolve().parent
SOURCES = (
    (
        "verify_b121_revision_v2.py",
        "80f5d0feb422d66ca6b051d56cabebe8cbd48c219f289f965c8437d7b9e89408",
        "verify_b122_revision.py",
        (
            (r"\u5fb3", r"\u60a0"),
            (r"words/\u9053\u60a0.md", r"words/\u60a0\u3005.md"),
            (r'("\u60a0", "\u30c8\u30af", "\u304a\u3057\u3048", "\u3068\u3063")',
             r'("\u60a0", "\u30e6\u30a6", "\u306f\u308b\u304b", "\u3068\u304a\u3044", "\u3086")'),
            (r"\u5e78\u8ca1\u5049", r"\u5e38\u7d9a"),
            ('allowed = {"distractors", "quiz_exclusions"}', 'allowed = {"quiz_exclusions"}'),
            ("batch-121/reconciliation-001/", "batch-122-reconciliation/"),
            ("B121", "B122"),
            ("load_batch(121)", "load_batch(122)"),
            ("len(current) == 8704", "len(current) == 8706"),
            ("count(runtime(before)) == 250 and count(current) == 251",
             "count(runtime(before)) == 251 and count(current) == 252"),
            ('"batch": 121', '"batch": 122'),
            ('"sourceMembersPublishedBeforeBatch": 250, "sourceMembersInCandidate": 251',
             '"sourceMembersPublishedBeforeBatch": 251, "sourceMembersInCandidate": 252'),
        ),
    ),
    (
        "test_verify_b121_revision.py",
        "25a8107f1478d375d031393fc46235ec662e102391c383cdebfb23b6f3cfad3f",
        "test_verify_b122_revision.py",
        (
            ("verify_b121_revision", "verify_b122_revision"),
            (r"\u30c8\u30af", r"\u30e6\u30a6"),
            (r"\u5e78\u8ca1\u5049", r"\u5e38\u7d9a"),
            (r'"\u8ca1"', r'"\u5e38"'),
            ("while_replacing_options", "while_preserving_options"),
            ('new = {**old, "distractors": ["d", "e", "f"],',
             'new = {**old, "distractors": ["a", "b", "c"],'),
            ('("distractors", ["d", "d", "f"]),',
             '("distractors", ["d", "e", "f"]),\n'
             '                           ("distractors", ["d", "d", "f"]),'),
        ),
    ),
    (
        "test_verify_b121_revision_v2.py",
        "305fd6c13ac295610f32a657994b80ef070bbbe83bb22e85c836b1270f7944ec",
        "test_verify_b122_revision_summary.py",
        (("verify_b121_revision_v2", "verify_b122_revision"),),
    ),
)


def main():
    derived = []
    for source_name, digest, output_name, replacements in SOURCES:
        source = HERE / source_name
        raw = frozen(source, digest)
        original = raw.decode("utf-8").replace("\r\n", "\n")
        text = original
        changes = []
        for old, new in replacements:
            count = text.count(old)
            require(count > 0, f"Expected source fragment absent: {source_name}: {old}")
            text = text.replace(old, new)
            changes.append({"old": old, "new": new, "count": count})
        reverse = text
        for change in reversed(changes):
            reverse = reverse.replace(change["new"], change["old"])
        require(reverse == original, f"Reverse derivation differs: {source_name}")
        compile(text, output_name, "exec")
        derived.append({
            "source": {"path": str(source), "sha256": digest},
            "output": write_frozen(HERE / output_name, text.replace("\n", "\r\n").encode("utf-8")),
            "changes": changes,
            "reverseExact": True,
        })
    freeze_json(WS / "scratch-122" / "review" / "revision-verifier-derivation.json", {
        "batch": 122,
        "derivations": derived,
        "producer": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
        "scope": "B122 identities, source directory, accounting and supplemental readings. "
                 "Preserve curated options as well as all original metadata and guards. "
                 "The original signed-delta, complete-record and committed-gate checks remain intact.",
        "publicationAccepted": False,
    })


if __name__ == "__main__":
    main()
