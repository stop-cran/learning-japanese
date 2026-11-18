"""Derive exact B125 delivery checks from its signed, review-closed publication."""
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, write_frozen
from confirm_v2 import clean
from finalize_b125_v2 import CANDIDATE, check_history, check_proofs
from prepare_b122_publication_tools import replace
from prepare_b123_publication_tools import PINS


def main(published):
    require(re.fullmatch(r"[0-9a-f]{40}", published), "Full publication SHA required")
    config = load_batch(125)
    clean(config, published)
    closure = Path(config["repo"]) / "docs" / "n1-reviews" / "batch-125-closure"
    check_history(json.loads(frozen(closure / "provenance.json")), config)
    first, second, current = [json.loads(frozen(closure / "verification" / f"reconciliation-{n:03}.json"))
                              for n in (1, 2, 3)]
    check_proofs(first, second, current, config)
    require(git(config, "show", "-s", "--format=%P", published).decode().strip() == CANDIDATE,
            "Publication must directly preserve the reviewed candidate")
    manifest = git(config, "show", f"{published}:manifest.json")
    require(manifest == git(config, "show", f"{CANDIDATE}:manifest.json")
            and sha(manifest) == current["manifestSha256"], "Publication manifest differs")
    changes = {
        "18ec8c757b0faae846ddec5317c37089cfbbae67": published,
        "e0787399ec3babfa": current["contentVersion"],
        "B122": "B125", "batch-122": "batch-125", "load_batch(122)": "load_batch(125)",
        "8706": "8712", "252": "255", "246": "249", "976": "973", r"\u60a0": r"\u4fb5",
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
        records.append({"source": {"path": str(source), "sha256": digest},
                        "output": write_frozen(WS / "scratch-125" / name, result.encode("utf-8")),
                        "substitutions": selected, "reverseExact": True})
    print(freeze_json(WS / "scratch-125" / "publication-tools-preflight.json", {
        "batch": 125, "publishedCommit": published, "reviewedSnapshot": CANDIDATE,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "derivations": records,
        "limits": "Preparation only. Receipt CI, exact ZIP/tree equality and owner checkpoint remain required.",
    }))


if __name__ == "__main__":
    main(sys.argv[1])
