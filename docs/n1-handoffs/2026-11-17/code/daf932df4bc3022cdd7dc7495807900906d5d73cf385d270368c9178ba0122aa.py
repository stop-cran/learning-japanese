"""Derive one batch's review gates from the frozen B116 modules by exact, reversible label substitution.

Usage: python -B derive-tooling.py <batch-number>
Writes scratch-<N>\\review\\{review_chain,audit-review,check-report-structure,check-run-context}.py and their
tests. Only batch labels change; each output is created exclusively, made ReadOnly and recorded with its
source hash, substitution counts and a reverse proof. B116 files are read, never modified.
"""
import hashlib
import json
import stat
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
B116 = WS / "scratch-116"
SOURCES = {
    "review_chain.py": ("review_chain.py", "2c02b506086b0698ccac49ead5ddfa87271b535f4deebbefdd9f28734bfb2109", []),
    "audit-review-v4.py": ("audit-review.py", "1577462aab29ece62423ba8b29fd26e06814d8471150a40d34af5abe1663261c",
                           [("Read-only B116 review-run audit", "Read-only {B} review-run audit")]),
    "check-report-structure.py": ("check-report-structure.py",
                                  "d41b3f0484dd285e93800efa2ca46eb455f6f15b2e0129e6029eb4a3e29171e0",
                                  [("a B116 initial-review report", "a {B} initial-review report"),
                                   ('r"# B116 initial review', 'r"# {B} initial review'),
                                   ("'# B116 initial review", "'# {B} initial review")]),
    "check-run-context.py": ("check-run-context.py",
                             "2555515b459b99ce50e8a999a6077622458f0636c34f39783400ddec8877a5e0", []),
    "test-review-chain.py": ("test-review-chain.py",
                             "b6e123d1c70c8a8f80ce8dc8b3eb4d1a76c16edefb8d6c8b469b1cfba9836e0e", []),
    "test-report-structure.py": ("test-report-structure.py",
                                 "d701ae1166f7c562f809acb58077a69363a49b8097028166af0e535b3eaeccc6",
                                 [('f"# B116 initial review', 'f"# {B} initial review')]),
    "test-review-audit-v4.py": ("test-review-audit.py",
                                "fdc700fb44d8896cfc2b2204dc6cf5255a1b9787ae73381ad62dfb63f6312d15",
                                [("audit-review-v4.py", "audit-review.py")]),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main(batch):
    if not batch.isdigit() or batch == "116":
        raise SystemExit("Batch must be a number other than 116")
    label = f"B{batch}"
    out_dir = WS / f"scratch-{batch}" / "review"
    out_dir.mkdir(parents=True, exist_ok=True)
    record = {"purpose": f"{label} review gates derived from frozen B116 modules", "derivations": []}
    outputs = {}
    for name, (target, expected, pairs) in SOURCES.items():
        raw = (B116 / name).read_bytes()
        if sha(raw) != expected:
            raise ValueError(f"B116 source changed: {name}")
        text = raw.decode("utf-8")
        counts = []
        for before, after in pairs:
            after = after.replace("{B}", label)
            count = text.count(before)
            if count < 1 or after in text:
                raise ValueError(f"Ambiguous substitution in {name}: {before}")
            text = text.replace(before, after)
            counts.append({"before": before, "after": after, "count": count})
        back = text
        for item in reversed(counts):
            if back.count(item["after"]) != item["count"]:
                raise ValueError(f"Reverse count mismatch in {name}")
            back = back.replace(item["after"], item["before"])
        if back.encode("utf-8") != raw:
            raise ValueError(f"Reverse proof failed: {name}")
        data = text.encode("utf-8")
        compile(data, target, "exec")
        outputs[out_dir / target] = data
        record["derivations"].append({
            "source": str(B116 / name), "sourceSha256": expected, "target": str(out_dir / target),
            "targetSha256": sha(data), "substitutions": counts, "reverseExact": True,
        })
    record["remainingB116Labels"] = {str(p): True for p, d in outputs.items() if b"B116" in d}
    if record["remainingB116Labels"]:
        raise ValueError(f"B116 label left: {record['remainingB116Labels']}")
    record["deriver"] = {"path": str(Path(__file__).resolve()), "sha256": sha(Path(__file__).read_bytes())}
    out = out_dir / "tooling-derivation.json"
    if out.exists() or any(p.exists() for p in outputs):
        raise FileExistsError("Derived tooling already exists")
    for path, data in outputs.items():
        with path.open("xb") as stream:
            stream.write(data)
        path.chmod(stat.S_IREAD)
    with out.open("xb") as stream:
        stream.write((json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    out.chmod(stat.S_IREAD)
    print(json.dumps({"out": str(out), "sha256": sha(out.read_bytes()),
                      "files": [d["target"] for d in record["derivations"]]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
