"""Verify B131's current and preserved predecessor union audits from pinned JMdict."""
import gzip
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, start_guard
from prepare_b131_source_facts import (
    CANDIDATE, CANDIDATE_BASE, FACTS, HERE, PREFIX, PROOF, REPO, RUNNER, SOURCE_BASE,
    SOURCE_VERIFIER_SHA, verify_output,
)
from verify_b131_sources import (
    FINGERPRINT, Git, ORIGIN, OWNER, SCAN_HELPER, SCAN_SHA, TRAILER, VERIFIER, VERIFIER_SHA,
)
from verify_b130_final_sources import LABELS, verify_membership, verify_stream

FINAL_HELPER_SHA = "6910aa8d05dc7da5b7e42c178add8853dc965601affa793533f1a5c278b8617a"


def query_labels(queries):
    return {LABELS[kind] + ":" + value for kind, value in (query.split(":", 1) for query in queries)}


def verify_audit(audit, *, total, membership, counts, kd, comparisons, inputs, producer, residual):
    expected = {
        "base": CANDIDATE_BASE, "originalSourceBase": SOURCE_BASE,
        "completeJmdictUnion": len(membership), "originalFamiliesRechecked": len(membership),
        "additionalFamilies": 0, "wholeJmdictEntriesScanned": total,
        "completeKanjidicRecordsRechecked": len(kd), "queryCountsIncludingAbsences": counts,
        "finalAdditionalOutput": {"sha256": sha(residual), "bytes": len(residual), "canonicalRecordHashes": {}},
        "dictionaryInputs": inputs, "comparisonCopies": len(comparisons), "producerSha256": sha(producer),
    }
    require(set(audit) == set(expected) | {"verification"}
            and isinstance(audit["verification"], str) and audit["verification"].strip()
            and all(audit[key] == value for key, value in expected.items()),
            "Final union audit counts, queries, inputs, bases or outputs differ")


def main():
    output = HERE / "source-union-verification-001.json"
    require(not output.exists(), "Preserve union verification output")
    for path, digest in (
        (Path(__file__).with_name("prepare_b131_source_facts.py"),
         "565218911dbe5f395a32eaa8f82a8c1ff91cf0b11adeea7bc9e9e45cab6691e9"),
        (Path(__file__).with_name("verify_b131_sources.py"), SOURCE_VERIFIER_SHA),
        (Path(__file__).with_name("verify_b130_final_sources.py"), FINAL_HELPER_SHA),
        (VERIFIER, VERIFIER_SHA), (SCAN_HELPER, SCAN_SHA),
    ):
        frozen(path, digest)
    facts_raw, proof_raw = frozen(FACTS), frozen(PROOF)
    facts, proof = json.loads(facts_raw), json.loads(proof_raw)
    require(proof["batch"] == facts["batch"] == 131 and proof["candidate"] == facts["candidate"] == CANDIDATE
            and proof["base"] == facts["base"] == CANDIDATE_BASE and proof["sourceBase"] == SOURCE_BASE
            and proof["status"] == "PASS" and proof["checkoutBound"] is True and not proof["memory"]["breach"]
            and proof["facts"]["sha256"] == sha(facts_raw) and proof["verifierSha256"] == SOURCE_VERIFIER_SHA,
            "Complete source proof does not bind this candidate and facts")
    verifier = load_module("b131_union_records", VERIFIER)
    helper = load_module("b131_union_reader", SCAN_HELPER)
    guard, _ = start_guard("B131 complete final-union verification")
    git = Git(REPO, RUNNER, guard)
    signed = {}

    def blob(name):
        raw = git("show", CANDIDATE + ":" + PREFIX + name)
        signed[PREFIX + name] = sha(raw)
        return raw

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout differs")

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{CANDIDATE_BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Wrong owner, signature or parent")
        signature = git("verify-commit", CANDIDATE, include_stderr=True)
        require(TRAILER in git("show", "-s", "--format=%B", CANDIDATE), "Missing trailer")
        jm = facts["jmdictSelections"]
        require([item["file"] for item in jm] == [
            "jmdict-complete-families.xml", "jmdict-supplemental-families.xml", "jmdict-manual-families.xml"],
            "Unexpected original family files")
        proven = {item["path"]: item for item in proof["sourceRecords"]}
        merged, originals = {}, []
        for item in jm:
            raw = blob(item["file"])
            require(sha(raw) == proven[PREFIX + item["file"]]["sha256"], "Verified source file changed")
            records = verifier.records(raw, "entry", "ent_seq")
            require(all(merged[key] == records[key] for key in merged.keys() & records.keys()),
                    "Duplicate families disagree")
            merged.update(records)
            originals.append(set(merged))
        queries = sorted(set().union(*(item["queries"] for item in jm)))
        tested = json.loads(blob("reading-keys.json"))["testedKeys"]
        require({"exact-reb:" + value for values in tested.values() for value in values} <= set(queries),
                "Final union omits tested reading keys")
        inputs = json.loads(blob("source-receipt.json"))["inputs"]
        for kind, (filename, compressed, tag, key) in verifier.INPUTS.items():
            require(inputs[kind] == [filename, compressed, proof["inputs"][kind]["decompressedXmlSha256"], tag],
                    "Dictionary input receipt differs")
        filename, compressed, _, _ = verifier.INPUTS["jmdict"]
        path = WS / "control" / "inputs" / filename
        with path.open("rb") as stream:
            reader = helper.HashedReader(stream, guard)
            while reader.read(65536):
                pass
        require(reader.digest.hexdigest() == compressed, "Compressed JMdict differs")
        with gzip.open(path, "rb") as stream:
            reader = helper.HashedReader(stream, guard)
            count, membership, counts = verify_stream(reader, queries, merged, {}, guard)
        require(reader.digest.hexdigest() == proof["inputs"]["jmdict"]["decompressedXmlSha256"],
                "Decompressed JMdict differs")
        summaries = []
        for suffix, selections, original, producer in (
            ("", jm[:2], originals[1], "final-sources-b131-001.py"),
            ("-002", jm, originals[2], "final_sources_b131.py"),
        ):
            labels = query_labels(set().union(*(item["queries"] for item in selections)))
            selected = {identity: [label for label in found if label in labels]
                        for identity, found in membership.items() if labels & set(found)}
            require(set(selected) == original, "Final predicates require unrecorded residual families")
            selected_counts = {label: n for label, n in counts.items() if label in labels}
            residual = blob(f"jmdict-final-families{suffix}.xml")
            audit = json.loads(blob(f"final-source-audit{suffix}.json"))
            verify_output(residual, audit["finalAdditionalOutput"])
            root = ET.fromstring(residual)
            require(root.tag == "JMdict" and not len(root), "Residual is not empty")
            verify_membership(json.loads(blob(f"final-query-membership{suffix}.json")), selected)
            manual = "\u5ddd"
            kd = {identity for item in proof["sourceRecords"]
                  if item["input"] == verifier.INPUTS["kanjidic2"][0]
                  and (suffix or not item["path"].endswith("kanjidic2-manual-comparisons.xml"))
                  for identity in item["identities"]}
            comparisons = set(proof["packetComparisonCards"])
            if not suffix:
                comparisons.remove(manual)
            verify_audit(audit, total=count, membership=selected, counts=selected_counts, kd=kd,
                         comparisons=comparisons, inputs=inputs, producer=blob("producers/" + producer),
                         residual=residual)
            summaries.append({"audit": f"final-source-audit{suffix}.json",
                              "families": len(selected), "kanjidicRecords": len(kd),
                              "comparisonCopies": len(comparisons), "queries": len(labels),
                              "absentQueries": sorted(label for label, n in selected_counts.items() if not n)})
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(output, {
        "batch": 131, "status": "PASS", "candidate": CANDIDATE, "base": CANDIDATE_BASE,
        "sourceBase": SOURCE_BASE, "sourceFacts": {"path": str(FACTS), "sha256": sha(facts_raw)},
        "sourceProof": {"path": str(PROOF), "sha256": sha(proof_raw)},
        "wholeJmdictEntriesScanned": count, "audits": summaries, "signedInputs": signed,
        "signatureOutputSha256": sha(signature), "memory": memory,
        "verifierSha256": sha(frozen(Path(__file__))), "streamHelperSha256": FINAL_HELPER_SHA,
        "limits": "Complete pinned-source union, per-family labels, absent-query counts and current/"
                  "superseded audit consistency. Does not retrospectively certify historical execution "
                  "timing. Linguistic adequacy, gates, reviews and publication remain separate.",
    })))


if __name__ == "__main__":
    main()
