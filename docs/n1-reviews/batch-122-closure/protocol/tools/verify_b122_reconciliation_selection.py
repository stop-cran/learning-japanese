"""Verify the exact selections and copied comparison cards in B122 supplements."""
import gzip
import hashlib
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, load_module, require, sha, start_guard
from confirm_v2 import clean

PREFIX = "docs/n1-sources/batch-122-reconciliation/"
RECEIPTS = {
    "neutral": "c9be0b714a74d9873a191a543caf52c259b5dd3177a9ab25a46f64350a7a3589",
    "additional": "465cefe21f8df394e80e337fc0a83f9bbc9db55ec2d60c8c5ea2d79c2decbe1a",
}


def main(candidate, output):
    config = load_batch(122)
    clean(config, candidate)
    checker_path = WS / "scratch-122" / "review" / "verify-source-records.py"
    checker_sha = "eaa065457bbf2fb04a66a50e57e8d2ed65f385570be3b676eb6596c685af222c"
    frozen(checker_path, checker_sha)
    checker = load_module("b122_exact_reconciliation_sources", checker_path)
    guard, _ = start_guard("B122 reconciliation exact selection")
    copies, selected = {}, []
    try:
        receipts = {}
        for label, digest in RECEIPTS.items():
            raw = git(config, "show", f"{candidate}:{PREFIX}{label}-receipt.json")
            require(sha(raw) == digest, "Signed supplement receipt differs")
            receipt = receipts[label] = json.loads(raw)
            require(receipt["candidate"] == config["candidate"] and receipt["status"] == "PASS"
                    and not receipt["memory"]["breach"], "Invalid supplement collection")
            for item in receipt["outputs"]:
                path = Path(item["path"])
                if path.suffix != ".md":
                    continue
                require(path.parent.name == "comparison-cards"
                        and path.resolve().is_relative_to(WS), "Unexpected comparison path")
                raw = frozen(path, item["sha256"])
                article = f"kanji/{path.stem}.md"
                require(raw == git(config, "show", f"{config['candidate']}:{article}")
                        == git(config, "show", f"{candidate}:{article}"),
                        f"Comparison changed: {article}")
                copies[article] = sha(raw)
                guard.check()
        for kind, (filename, digest, tag, key) in checker.INPUTS.items():
            source = WS / "control" / "inputs" / filename
            computed = hashlib.sha256()
            with source.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    computed.update(chunk)
                    guard.check()
            require(computed.hexdigest() == digest, "Pinned input changed")
            selections = []
            for label, receipt in receipts.items():
                matches = [item for item in receipt["outputs"]
                           if Path(item["path"]).name == f"{kind}-records.xml"]
                require(len(matches) == 1, "Missing or duplicate supplement extraction")
                item = matches[0]
                raw = git(config, "show", f"{candidate}:{PREFIX}{label}-{kind}.xml")
                require(sha(raw) == item["sha256"] and item["inputSha256"] == digest,
                        "Signed extraction or source binding differs")
                records = checker.records(raw, tag, key)
                require(sorted(records) == item["completeRecordIdentities"], "Record identity list differs")
                selections.append({"name": f"{label}-{kind}", "mode": "exact",
                                   "queries": set(item["queries"]), "expected": records,
                                   "sha256": sha(raw)})
            with gzip.open(source, "rb") as stream:
                matches = checker.verify_stream(stream, tag, key, selections, guard)
            for selection, identities in zip(selections, matches):
                selected.append({"name": selection["name"], "sha256": selection["sha256"],
                                 "queries": sorted(selection["queries"]), "identities": identities,
                                 "completeRecordsVerified": len(identities), "inputSha256": digest})
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Selection verification RAM breach")
    print(json.dumps(freeze_json(Path(output), {
        "batch": 122, "candidate": candidate, "status": "PASS", "receipts": RECEIPTS,
        "selections": selected, "comparisonCards": copies, "memory": memory,
        "checkerSha256": checker_sha, "verifierSha256": sha(Path(__file__).read_bytes()),
        "limits": "Exact selected membership, complete records and comparison bytes verified; "
                  "not a linguistic judgment, exhaustive lexical search or publication approval.",
    })))


if __name__ == "__main__":
    main(*sys.argv[1:])
