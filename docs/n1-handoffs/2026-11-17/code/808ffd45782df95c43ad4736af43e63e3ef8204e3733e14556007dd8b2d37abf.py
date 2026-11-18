"""Derive B129 delivery checks from the signed, replacement-aware closure."""
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, start_guard, write_frozen
from confirm_v2 import clean
from finalize_b129 import MEMBERS, SIGNER, check_history, check_proof
from prepare_b123_publication_tools import PINS
from prepare_b126_publication_tools_v2 import replace
from record_publication import delivery_accounting


def main(published):
    require(re.fullmatch(r"[0-9a-f]{40}", published), "Full publication SHA required")
    config = load_batch(129)
    guard, _ = start_guard("B129 publication tooling preparation")
    try:
        clean(config, published)
        closure = Path(config["repo"]) / "docs" / "n1-reviews" / "batch-129-closure"
        provenance_raw = frozen(closure / "provenance.json")
        provenance = json.loads(provenance_raw)
        candidate = provenance["reviewedSnapshot"]
        proof = json.loads(frozen(closure / "verification" / "reconciliation-001.json"))
        check_history(provenance, candidate, config)
        check_proof(proof, candidate, config)
        require(git(config, "show", "-s", "--format=%P%n%G?|%GF|%ae|%ce", published).decode().strip()
                == f"{candidate}\nG|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru",
                "Publication is not the owner-signed direct reviewed-candidate child")
        changed = git(config, "diff", "--name-only", candidate, published).decode().splitlines()
        require(changed and all(path.startswith("docs/") for path in changed),
                "Publication changed runtime files")
        manifest = git(config, "show", f"{published}:manifest.json")
        require(manifest == git(config, "show", f"{candidate}:manifest.json")
                and sha(manifest) == proof["manifestSha256"], "Reviewed manifest changed")
        validation = json.loads(frozen(closure / "validation-provenance.json"))
        require(validation["candidate"] == candidate
                and validation["reviewClosureSha256"] == sha(provenance_raw),
                "Validation provenance differs")
        for inventory in (provenance, validation):
            for path, digest in inventory["recordedFileSha256"].items():
                frozen(closure / path, digest)
                guard.check()
        ledger = json.loads(git(config, "show", f"{published}:docs/n1-sources/batch-129-progress.json"))
        require(ledger["membership"] == MEMBERS and not ledger["runtimePublished"],
                "Unexpected publication ledger")
        counts = delivery_accounting(ledger)
        substitutions = {
            "18ec8c757b0faae846ddec5317c37089cfbbae67": published,
            "e0787399ec3babfa": proof["contentVersion"],
            "B122": "B129", "batch-122": "batch-129", "load_batch(122)": "load_batch(129)",
            "8706": str(proof["runtimeEntries"]), "252": str(counts["delivered"]),
            "246": str(counts["n1Additions"]), "976": str(counts["remaining"]),
            r'["\u60a0"]': json.dumps(MEMBERS),
        }
        records = []
        for name, digest in PINS.items():
            source = WS / "scratch-122" / name
            original = frozen(source, digest).decode("utf-8")
            selected = {old: new for old, new in substitutions.items() if old in original}
            derived = replace(original, selected)
            require(replace(derived, {new: old for old, new in selected.items()}) == original,
                    "Derivation is not byte-reversible")
            compile(derived, name, "exec")
            records.append({"source": {"path": str(source), "sha256": digest},
                            "output": write_frozen(WS / "scratch-129" / name, derived.encode("utf-8")),
                            "substitutions": selected, "reverseExact": True})
        print(freeze_json(WS / "scratch-129" / "publication-tools-preflight.json", {
            "batch": 129, "publishedCommit": published, "reviewedSnapshot": candidate,
            "members": MEMBERS, "sourceAccounting": counts,
            "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
            "derivations": records,
            "numericReplacementPolicy": "Complete numeric tokens; SHA256 identifiers remain unchanged.",
            "limits": "Preparation only. Receipt CI, exact ZIP/tree equality and owner checkpoint remain required.",
        }))
    finally:
        require(not guard.finish()["breach"], "Publication preparation RAM breach")


if __name__ == "__main__":
    main(sys.argv[1])
