"""Prepare B120's candidate verifier from the verified B119 implementation."""
import hashlib
import json
import stat
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
SOURCE = WS / "scratch-119" / "review" / "prepare-source-contract.py"
EXPECTED = "5fd89d89cab717c195059bb1961840e7e9c44c200663f4ba0035c582d2af5961"
TARGET = WS / "scratch-120" / "review" / "prepare-source-contract.py"
RECEIPT = TARGET.with_name("source-contract-derivation.json")
PAIRS = (
    ("B119", "B120"),
    ("b119", "b120"),
    ("batch-119", "batch-120"),
    ("scratch-119", "scratch-120"),
    ('"batch": 119', '"batch": 120'),
    ("56405533e42e38c43b20ce443ee6292191ace78f", "aab6e2782f093ace1deb4f567c5e4dee8890cbf6"),
    ('MEMBERS = ["妥", "循"]', 'MEMBERS = ["逮"]'),
    ("ROWS = [225, 345]", "ROWS = [1080]"),
    ('WORDS = {"妥": "妥当", "循": "循環"}', 'WORDS = {"逮": "逮捕"}'),
    ("1239", "1240"),
    ("len(pending & represented(previous)) == 247", "len(pending & represented(previous)) == 249"),
    ("len(pending & represented(current)) == 249", "len(pending & represented(current)) == 250"),
    ('"sourceMembersPublishedBeforeBatch": 247', '"sourceMembersPublishedBeforeBatch": 249'),
    ('"sourceMembersInCandidate": 249', '"sourceMembersInCandidate": 250'),
)


def main():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise ValueError("Verified B119 candidate verifier changed")
    if TARGET.exists() or RECEIPT.exists():
        raise FileExistsError("Preserve the existing B120 verifier and derivation")
    result, substitutions = raw, []
    for before, after in PAIRS:
        old, new = before.encode("utf-8"), after.encode("utf-8")
        count = result.count(old)
        if not count or new in result:
            raise ValueError(f"Ambiguous candidate-verifier substitution: {before}")
        result = result.replace(old, new)
        substitutions.append({"before": before, "after": after, "count": count})
    reverse = result
    for item in reversed(substitutions):
        old, new = item["before"].encode("utf-8"), item["after"].encode("utf-8")
        if reverse.count(new) != item["count"]:
            raise ValueError("Candidate-verifier reverse count mismatch")
        reverse = reverse.replace(new, old)
    if reverse != raw:
        raise ValueError("Candidate-verifier derivation is not byte-reversible")
    compile(result, str(TARGET), "exec")
    proof = {
        "source": str(SOURCE),
        "sourceSha256": EXPECTED,
        "target": str(TARGET),
        "targetSha256": hashlib.sha256(result).hexdigest(),
        "substitutions": substitutions,
        "reverseExact": True,
        "scope": "Prepared for provisional selection-002: one 逮 card, row 1080, existing 逮捕 wrapper. No candidate or content acceptance. Do not execute unless the signed author handoff matches these bindings and the inherited source receipt schema.",
        "deriverSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    for path, content in (
        (TARGET, result),
        (RECEIPT, (json.dumps(proof, ensure_ascii=False, indent=2) + "\n").encode("utf-8")),
    ):
        with path.open("xb") as stream:
            stream.write(content)
        path.chmod(stat.S_IREAD)
        if path.read_bytes() != content:
            raise ValueError(f"Readback differs: {path}")
    print(json.dumps(proof, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
