"""Recheck the source-only Q1/Q2 packet against the complete pinned dictionaries."""
import gzip
import hashlib
import json
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, start_guard
from run_b132_closure_checks import BASE, CANDIDATE, HERE, REPO
from verify_b132_packet import RUNNER
from verify_b132_sources import FINGERPRINT, OWNER, VERIFIER, VERIFIER_SHA, Git

PACKET = HERE / "source-reconciliation-001"
INVENTORY_SHA = "390ec9d4412633458b1333870461edad1f74630520cbf2ddf83914f9eccc7286"
OUTPUT = HERE / "review" / "source-reconciliation-verification-001.json"


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        data = self.stream.read(size)
        self.digest.update(data)
        return data


def main():
    require(not OUTPUT.exists(), "Preserve the previous source verification")
    guard, _ = start_guard("B132 Q1/Q2 complete source verification")
    try:
        inventory = json.loads(frozen(PACKET / "inventory.json", INVENTORY_SHA))
        require(inventory["candidate"] == CANDIDATE and len(inventory["files"]) == 59,
                "Unexpected source-only inventory")
        for name, binding in inventory["files"].items():
            path = PACKET / Path(name)
            require(path.resolve().is_relative_to(PACKET.resolve()), "Source path escapes packet")
            require(len(frozen(path, binding["sha256"])) == binding["bytes"], "Source byte count differs")
            guard.check()
        actual = {p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file()}
        require(actual == {*inventory["files"], "inventory.json"}, "Source inventory is incomplete")
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and git("show", "-s", "--format=%P", CANDIDATE).decode().strip() == BASE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate is changed or dirty")
        require(git("show", "-s", "--format=%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate signature/identity differs")
        for char in "\u5893\u6a19\u5854":
            require(frozen(PACKET / "candidate-cards" / f"{char}.md")
                    == git("show", f"{CANDIDATE}:kanji/{char}.md"), "Comparison article differs")
        initial = json.loads(frozen(PACKET / "dictionary-receipt.json"))
        extra = json.loads(frozen(PACKET / "referenced-receipt.json"))
        snapshot = json.loads(git("show", f"{CANDIDATE}:docs/n1-source-snapshot.json"))
        frozen(VERIFIER, VERIFIER_SHA)
        verifier = load_module("b132_supplement_record_verifier", VERIFIER)
        results = []
        for kind, (filename, compressed, decompressed, tag) in initial["inputs"].items():
            require(snapshot["inputs"][filename]["sha256"] == compressed, "Unpinned input")
            source = WS / "control" / "inputs" / filename
            with source.open("rb") as stream:
                reader = HashReader(stream, guard)
                while reader.read(1024 * 1024):
                    pass
            require(reader.digest.hexdigest() == compressed, "Compressed source differs")
            key = "ent_seq" if kind == "jmdict" else "literal"
            definitions = ([("jmdict-exact-families.xml", initial["exactSpellings"]),
                            ("jmdict-referenced-families.xml", extra["exactSpellings"])]
                           if kind == "jmdict" else
                           [("kanjidic2-exact-characters.xml", initial["exactCharacterLiterals"])])
            selections = [{"name": name, "mode": "exact", "queries": set(queries),
                           "expected": verifier.records(frozen(PACKET / name), tag, key)}
                          for name, queries in definitions]
            with gzip.open(source, "rb") as stream:
                reader = HashReader(stream, guard)
                matched = verifier.verify_stream(reader, tag, key, selections, guard)
            require(reader.digest.hexdigest() == decompressed, "Decompressed source differs")
            for selection, identities in zip(selections, matched, strict=True):
                results.append({"name": selection["name"], "records": len(identities),
                                "identities": identities, "queries": sorted(selection["queries"]),
                                "sourceCompressedSha256": compressed,
                                "sourceDecompressedSha256": decompressed})
        require({r["name"]: r["records"] for r in results}
                == {"jmdict-exact-families.xml": 23, "jmdict-referenced-families.xml": 5,
                    "kanjidic2-exact-characters.xml": 3}, "Unexpected complete record counts")
        captures = []
        for filename in ("external-captures.json", "referenced-external-captures.json"):
            captures.extend(json.loads(frozen(PACKET / filename))["captures"])
        failures = [item for item in captures if "error" in item]
        require(len(captures) == 20 and len(failures) == 1
                and failures[0]["term"] == "\u5893\u5854"
                and failures[0]["provider"] == "kotobank" and "404" in failures[0]["error"],
                "Capture attempt inventory differs")
        for item in captures:
            if "error" not in item:
                for field, digest, size in (("raw", "rawSha256", "rawBytes"),
                                            ("extraction", "extractionSha256", "extractionBytes")):
                    path = Path(item[field])
                    require(path.resolve().is_relative_to(PACKET.resolve()), "Capture outside packet")
                    require(len(frozen(path, item[digest])) == item[size], "Capture binding differs")
        verification = json.loads(frozen(PACKET / "verification.json"))
        for item in verification["external"]["reusedOriginalCapturesVerified"]:
            raw = Path(item["localRawCapture"])
            frozen(raw, item["rawSha256"])
            frozen(raw.with_suffix(".txt"), item["textSha256"])
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Candidate changed")
        result = {
            "status": "PASS", "candidate": CANDIDATE, "base": BASE,
            "sourceInventory": {"path": str(PACKET / "inventory.json"), "sha256": INVENTORY_SHA},
            "files": 59, "dictionarySelections": results, "captures": 20,
            "successfulCaptures": 19, "disclosedFailedCaptures": 1,
            "completeRecordVerifier": {"path": str(VERIFIER), "sha256": VERIFIER_SHA},
            "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "Mechanical source completeness and identity only. Captured pages are not "
                      "refetched; text-extraction logic was inspected, not independently re-executed. "
                      "No semantic approval, teaching change, reviewer confirmation or publication.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source verification RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(OUTPUT, result)))


if __name__ == "__main__":
    main()
