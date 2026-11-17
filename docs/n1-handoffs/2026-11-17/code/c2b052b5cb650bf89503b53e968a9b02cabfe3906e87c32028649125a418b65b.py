"""Derive B123 checkpoint and exact served-tree checks for its signed publication."""
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, write_frozen
from confirm_v2 import clean
from finalize_b123 import CANDIDATE
from prepare_b122_publication_tools import replace

PINS = {
    "checkpoint-publication.py": "5a3e0ba610236024e24fd85fc3cb215ec2b720f33fb5fd0237e87a4b18c452f8",
    "verify-served-tree-equality.py": "aa78a90f8b66e426adf1641af188dc08bcaba95ae2fc31de8a050bacdac8eae4",
}


def main(published):
    require(re.fullmatch(r"[0-9a-f]{40}", published), "Full publication SHA required")
    config = load_batch(123)
    clean(config, published)
    require(git(config, "show", "-s", "--format=%P", published).decode().strip() == CANDIDATE,
            "Publication must directly preserve the reviewed snapshot")
    manifest = git(config, "show", f"{published}:manifest.json")
    require(manifest == git(config, "show", f"{CANDIDATE}:manifest.json"),
            "Publication changed the reviewed manifest")
    require(json.loads(manifest)["contentVersion"] == "9c2cddbf8faec424",
            "Unexpected reviewed content version")
    changes = {
        "18ec8c757b0faae846ddec5317c37089cfbbae67": published,
        "e0787399ec3babfa": "9c2cddbf8faec424",
        "B122": "B123", "batch-122": "batch-123", "load_batch(122)": "load_batch(123)",
        "8706": "8708", "252": "253", "246": "247", "976": "975",
        r"\u60a0": r"\u7bc4",
    }
    records = []
    for name, digest in PINS.items():
        source = WS / "scratch-122" / name
        text = frozen(source, digest).decode("utf-8")
        selected = {old: new for old, new in changes.items() if old in text}
        result = replace(text, selected)
        require(replace(result, {new: old for old, new in selected.items()}) == text,
                "Derivation is not byte-reversible")
        compile(result, name, "exec")
        records.append({
            "source": {"path": str(source), "sha256": digest},
            "output": write_frozen(WS / "scratch-123" / name, result.encode("utf-8")),
            "substitutions": selected, "reverseExact": True,
        })
    print(json.dumps(freeze_json(WS / "scratch-123" / "publication-tools-preflight.json", {
        "batch": 123, "publishedCommit": published,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "derivations": records,
        "limits": "Preparation only. Receipt CI, exact ZIP/tree equality and owner checkpoint remain required.",
    })))


if __name__ == "__main__":
    main(sys.argv[1])
