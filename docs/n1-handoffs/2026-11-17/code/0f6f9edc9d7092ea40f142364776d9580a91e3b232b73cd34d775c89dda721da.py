"""Derive delivery tools from the actual third-revision closure, not stale constants."""
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, write_frozen
from confirm_v2 import clean
from finalize_b123_v2 import check_history
from prepare_b122_publication_tools import replace
from prepare_b123_publication_tools import PINS


def main(published):
    require(re.fullmatch(r"[0-9a-f]{40}", published), "Full publication SHA required")
    config = load_batch(123)
    clean(config, published)
    closure = Path(config["repo"]) / "docs" / "n1-reviews" / "batch-123-closure"
    provenance = json.loads(frozen(closure / "provenance.json"))
    candidate = provenance["reviewedSnapshot"]
    check_history(provenance, candidate, config)
    proof = json.loads(frozen(closure / "verification" / "reconciliation-003.json"))
    require(proof["status"] == "PASS" and proof["candidate"] == candidate
            and git(config, "show", "-s", "--format=%P", published).decode().strip() == candidate,
            "Publication does not preserve the verified successor")
    manifest = git(config, "show", f"{published}:manifest.json")
    require(manifest == git(config, "show", f"{candidate}:manifest.json")
            and sha(manifest) == proof["manifestSha256"], "Publication manifest differs")
    changes = {
        "18ec8c757b0faae846ddec5317c37089cfbbae67": published,
        "e0787399ec3babfa": proof["contentVersion"],
        "B122": "B123", "batch-122": "batch-123", "load_batch(122)": "load_batch(123)",
        "8706": "8708", "252": "253", "246": "247", "976": "975", r"\u60a0": r"\u7bc4",
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
                        "output": write_frozen(WS / "scratch-123" / name, result.encode("utf-8")),
                        "substitutions": selected, "reverseExact": True})
    print(json.dumps(freeze_json(WS / "scratch-123" / "publication-tools-preflight.json", {
        "batch": 123, "publishedCommit": published, "reviewedSnapshot": candidate,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "derivations": records,
        "limits": "Preparation only. Receipt CI, exact ZIP/tree equality and owner checkpoint remain required.",
    })))


if __name__ == "__main__":
    main(sys.argv[1])
