"""Derive the exact B122 publication checkpoint and served-tree checks."""
import re
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

PINS = {
    "checkpoint-publication.py": "8ff23641a537f8da8c34c2bdce1e770ebd2f432c9b9c0fac8793ac82509bb696",
    "verify-served-tree-equality.py": "bbbd2b8fb4d4166a2128ba007e8584844ff86328013f70e9395f16ffac7e65e5",
}
CHANGES = {
    "889e27a8def799e9b2da94f4df1a3f04a9bc9cfa": "18ec8c757b0faae846ddec5317c37089cfbbae67",
    "d709dbad2dcb1d6c": "e0787399ec3babfa",
    "B121": "B122",
    "batch-121": "batch-122",
    "load_batch(121)": "load_batch(122)",
    "8704": "8706",
    "251": "252",
    "245": "246",
    "977": "976",
    r"\u5fb3": r"\u60a0",
}


def replace(text, changes):
    pattern = re.compile("|".join(re.escape(k) for k in sorted(changes, key=len, reverse=True)))
    return pattern.sub(lambda match: changes[match[0]], text)


def main():
    records = []
    for name, expected in PINS.items():
        source = WS / "scratch-121" / name
        raw = frozen(source, expected)
        text = raw.decode("utf-8")
        selected = {old: new for old, new in CHANGES.items() if old in text}
        result = replace(text, selected)
        require(replace(result, {new: old for old, new in selected.items()}) == text,
                "Derivation is not byte-reversible")
        compile(result, name, "exec")
        records.append({
            "source": {"path": str(source), "sha256": expected},
            "output": write_frozen(WS / "scratch-122" / name, result.encode("utf-8")),
            "substitutions": selected, "reverseExact": True,
        })
    freeze_json(WS / "scratch-122" / "publication-tools-preflight.json", {
        "batch": 122, "publishedCommit": CHANGES["889e27a8def799e9b2da94f4df1a3f04a9bc9cfa"],
        "producer": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
        "derivations": records,
        "limits": "Preparation only. Full receipt CI, exact ZIP/tree equality and owner readback remain required.",
    })


if __name__ == "__main__":
    main()
