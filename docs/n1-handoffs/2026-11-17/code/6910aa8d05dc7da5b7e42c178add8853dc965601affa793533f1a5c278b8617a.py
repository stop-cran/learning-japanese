"""Verify B130's residual final JMdict union against the complete pinned JMdict stream.

The frozen generic verifier (verify_b130_sources.py) proves the complete and supplemental
JMdict files as exact selections. The author's final pass widens the union with the tested
reading keys and writes only the families absent from those two files. This verifier proves
that the three files together hold exactly every pinned JMdict family the final predicates
select, with unchanged records, per-family labels, all query counts and every audit total.
"""
import gzip
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, start_guard
import source_query_union
from prepare_b129_source_facts import literal_assignment
from verify_b130_payload import SOURCE_VERIFIER_SHA
from verify_b130_sources import (FINGERPRINT, Git, ORIGIN, OWNER, QUERY_SHA, SCAN_HELPER, SCAN_SHA, TRAILER,
                                 VERIFIER, VERIFIER_SHA)
from verify_reconciliation_sources import element_value

HELPER_SHA = "a1f850826848325b2566c859353f424c8476fb6de05225cd1a79476722a989ea"
FACT_KEYS = {"batch", "base", "candidate", "sourceFacts", "sourceProof", "files", "residual", "membership",
             "audit", "readingKeys", "mode", "queries", "producer", "output"}
AUDIT_KEYS = {"base", "completeJmdictUnion", "originalFamiliesRechecked", "additionalFamilies",
              "wholeJmdictEntriesScanned", "completeKanjidicRecordsRechecked", "queryCountsIncludingAbsences",
              "finalAdditionalOutput", "dictionaryInputs", "verification", "producerSha256"}
LABELS = {"contains-keb": "contains", "exact-keb": "exact-spelling", "exact-reb": "exact-reading"}


def canonical_hash(node):
    return sha(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode("utf-8"))


def labels(node, queries):
    spellings = {item.text for item in node.findall("k_ele/keb") if item.text}
    readings = {item.text for item in node.findall("r_ele/reb") if item.text}
    found = []
    for query in queries:
        kind, value = query.split(":", 1)
        if ((kind == "contains-keb" and any(value in spelling for spelling in spellings))
                or (kind == "exact-keb" and value in spellings)
                or (kind == "exact-reb" and value in readings)):
            found.append(f"{LABELS[kind]}:{value}")
    return found


def check_final_facts(final, source_facts, proof, source_facts_sha):
    require(set(final) == FACT_KEYS, f"Final facts keys differ: {sorted(set(final) ^ FACT_KEYS)}")
    require(final["batch"] == source_facts["batch"] == proof["batch"] == 130 and final["mode"] == "union",
            "Final facts must describe B130's union")
    require(all(re.fullmatch("[0-9a-f]{40}", final[key]) for key in ("base", "candidate"))
            and source_facts["base"] == proof["base"] == final["base"]
            and source_facts["candidate"] == proof["candidate"] == final["candidate"],
            "Final facts, source facts and source proof bind different commits")
    require(final["sourceFacts"]["sha256"] == source_facts_sha and proof["facts"]["sha256"] == source_facts_sha
            and Path(proof["facts"]["path"]).resolve() == Path(final["sourceFacts"]["path"]).resolve(),
            "Source proof was produced from different facts")
    require(proof["status"] == "PASS" and proof["verifierSha256"] == SOURCE_VERIFIER_SHA,
            "Earlier selections lack a passing pinned source proof")
    jm = source_facts["jmdictSelections"]
    require([item["mode"] for item in jm] == ["union", "union"], "Final union needs both earlier union selections")
    names = [final["residual"], final["membership"], final["audit"], final["readingKeys"]]
    require(all(Path(name).name == name and name for name in names) and final["residual"].endswith(".xml")
            and all(name.endswith(".json") for name in names[1:]) and len(set(names)) == 4,
            "Final packet names must be distinct plain packet files")
    require(final["files"] == [jm[0]["file"], jm[1]["file"], final["residual"]]
            and len(set(final["files"])) == 3, "Final files must be the earlier JMdict files plus the residual")
    source_query_union.validate(final)
    earlier = set().union(*(item["queries"] for item in jm))
    queries = final["queries"]
    require(queries == sorted(set(queries)) and earlier <= set(queries)
            and all(query.startswith("exact-reb:") for query in set(queries) - earlier),
            "Final queries must add only exact readings to the earlier union")
    producer = final["producer"]
    require(set(producer) == {"name", "sha256"} and Path(producer["name"]).name == producer["name"]
            and re.fullmatch("[0-9a-f]{64}", producer["sha256"]), "Invalid final producer pin")
    records = {item["path"]: item["sha256"] for item in proof["sourceRecords"]}
    prefix = source_facts["prefix"]
    require(all(prefix + name in records for name in final["files"][:2]), "Source proof omits an earlier file")
    require(not Path(final["output"]).exists(), "Preserve existing verification output")
    return {name: records[prefix + name] for name in final["files"][:2]}


def merge(complete, supplemental, residual):
    for identity in complete.keys() & supplemental.keys():
        require(complete[identity] == supplemental[identity], f"Earlier files disagree on a family: {identity}")
    original = {**complete, **supplemental}
    require(residual and not residual.keys() & original.keys(), "Residual file must hold only new families")
    return {**original, **residual}, original


def verify_stream(stream, queries, merged, residual_hashes, guard):
    counts = {f"{LABELS[query.split(':', 1)[0]]}:{query.split(':', 1)[1]}": 0 for query in queries}
    membership, count = {}, 0
    parser = ET.iterparse(stream, events=("start", "end"))
    _, root = next(parser)
    for event, node in parser:
        if event != "end" or node.tag != "entry":
            continue
        count += 1
        identity = node.findtext("ent_seq")
        found = labels(node, queries)
        require(bool(found) == source_query_union.selects(node, "entry", identity, "union", queries),
                f"Label recomputation diverges from the pinned selector: {identity}")
        if found:
            require(identity and identity not in membership, f"Missing or duplicate pinned identity: {identity}")
            require(identity in merged, f"Missing final-union family: {identity}")
            require(element_value(node) == merged[identity], f"Incomplete or altered record: {identity}")
            require(identity not in residual_hashes or canonical_hash(node) == residual_hashes[identity],
                    f"Residual canonical hash differs from the pinned record: {identity}")
            membership[identity] = found
            for label in found:
                counts[label] += 1
        node.clear()
        root.clear()
        guard.check()
    require(set(membership) == set(merged),
            f"Unexpected final-union families: {sorted(set(merged) - set(membership))}")
    return count, membership, counts


def verify_membership(recorded, computed):
    require(set(recorded) == set(computed), "Final query membership has missing or extra families")
    for identity, found in computed.items():
        require(isinstance(recorded[identity], list) and len(recorded[identity]) == len(set(recorded[identity]))
                and set(recorded[identity]) == set(found), f"Per-family final predicates differ: {identity}")


def verify_audit(audit, *, base, merged, original, residual_raw, residual_hashes, count, counts, inputs,
                 producer_sha, kanjidic_records):
    require(set(audit) == AUDIT_KEYS, f"Final audit keys differ: {sorted(set(audit) ^ AUDIT_KEYS)}")
    require(audit["base"] == base and audit["completeJmdictUnion"] == len(merged)
            and audit["originalFamiliesRechecked"] == len(original)
            and audit["additionalFamilies"] == len(residual_hashes)
            and audit["wholeJmdictEntriesScanned"] == count
            and audit["completeKanjidicRecordsRechecked"] == kanjidic_records, "Final audit totals differ")
    require(audit["queryCountsIncludingAbsences"] == counts, "Final query counts, including absences, differ")
    require(audit["finalAdditionalOutput"] == {
        "source": "jmdict", "sha256": sha(residual_raw), "bytes": len(residual_raw),
        "canonicalRecordHashes": residual_hashes, "completeCanonicalEquality": True,
    }, "Residual output binding differs")
    require(audit["dictionaryInputs"] == inputs and audit["producerSha256"] == producer_sha,
            "Final audit inputs or producer differ")


def main(facts_path):
    facts_raw = frozen(Path(facts_path))
    final = json.loads(facts_raw)
    frozen(Path(source_query_union.__file__), QUERY_SHA)
    frozen(Path(__file__).with_name("prepare_b129_source_facts.py"), HELPER_SHA)
    frozen(Path(__file__).with_name("verify_b130_sources.py"), SOURCE_VERIFIER_SHA)
    frozen(VERIFIER, VERIFIER_SHA)
    frozen(SCAN_HELPER, SCAN_SHA)
    source_facts_raw = frozen(final["sourceFacts"]["path"], final["sourceFacts"]["sha256"])
    source_facts = json.loads(source_facts_raw)
    proof_raw = frozen(final["sourceProof"])
    proof = json.loads(proof_raw)
    earlier = check_final_facts(final, source_facts, proof, sha(source_facts_raw))
    verifier = load_module("b130_final_pinned_records", VERIFIER)
    helper = load_module("b130_final_pinned_scan_helper", SCAN_HELPER)
    filename, compressed_sha, tag, key = verifier.INPUTS["jmdict"]
    require((tag, key) == ("entry", "ent_seq") and proof["inputs"]["jmdict"]["filename"] == filename
            and proof["inputs"]["jmdict"]["compressedSha256"] == compressed_sha, "Pinned JMdict input differs")
    kanjidic = verifier.INPUTS["kanjidic2"][0]
    kanjidic_records = len({identity for item in proof["sourceRecords"] if item["input"] == kanjidic
                            for identity in item["identities"]})
    base, candidate, prefix = final["base"], final["candidate"], source_facts["prefix"]
    guard, _ = start_guard("B130 residual final-union source verification")
    git = Git(source_facts["repo"], source_facts["runner"], guard)
    signed = {}

    def blob(name):
        raw = git("show", f"{candidate}:{prefix}{name}")
        signed[prefix + name] = sha(raw)
        return raw

    def checkout():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate is not the unchanged clean checkout")

    try:
        checkout()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{base}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Wrong parent, signature or owner identity")
        signature = git("verify-commit", candidate, include_stderr=True)
        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing trailer")
        raws = [blob(name) for name in final["files"]]
        require([sha(raw) for raw in raws[:2]] == [earlier[name] for name in final["files"][:2]],
                "Earlier JMdict files differ from the passing source proof")
        complete, supplemental, residual = (verifier.records(raw, tag, key) for raw in raws)
        merged, original = merge(complete, supplemental, residual)
        residual_hashes = {node.findtext(key): canonical_hash(node) for node in ET.fromstring(raws[2]).findall(tag)}
        require(residual_hashes.keys() == residual.keys(), "Residual identities differ")
        producer = blob("producers/" + final["producer"]["name"])
        require(sha(producer) == final["producer"]["sha256"], "Final producer differs from its pin")
        tested = json.loads(blob(final["readingKeys"]))["testedKeys"]
        require(literal_assignment(producer, "KEYS") == tested, "Committed reading keys differ from the producer")
        earlier_queries = set().union(*(item["queries"] for item in source_facts["jmdictSelections"]))
        require(set(final["queries"]) == earlier_queries | {"exact-reb:" + reading for readings in tested.values()
                                                             for reading in readings},
                "Final queries differ from the earlier union plus the tested reading keys")
        receipt = json.loads(blob("source-receipt.json"))
        audit_raw = blob(final["audit"])
        membership_raw = blob(final["membership"])
        path = WS / "control" / "inputs" / filename
        with path.open("rb") as stream:
            reader = helper.HashedReader(stream, guard)
            while reader.read(65536):
                pass
        require(reader.digest.hexdigest() == compressed_sha, "Compressed JMdict differs")
        with gzip.open(path, "rb") as stream:
            reader = helper.HashedReader(stream, guard)
            count, computed, counts = verify_stream(reader, final["queries"], merged, residual_hashes, guard)
        require(reader.digest.hexdigest() == proof["inputs"]["jmdict"]["decompressedXmlSha256"],
                "Decompressed JMdict differs")
        verify_membership(json.loads(membership_raw), computed)
        verify_audit(json.loads(audit_raw), base=base, merged=merged, original=original, residual_raw=raws[2],
                     residual_hashes=residual_hashes, count=count, counts=counts,
                     inputs=receipt["dictionaryInputs"], producer_sha=final["producer"]["sha256"],
                     kanjidic_records=kanjidic_records)
        checkout()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(Path(final["output"]), {
        "batch": 130, "candidate": candidate, "base": base, "status": "PASS",
        "facts": {"path": str(Path(facts_path)), "sha256": sha(facts_raw)},
        "sourceFacts": final["sourceFacts"], "sourceProof": {"path": final["sourceProof"], "sha256": sha(proof_raw)},
        "signatureOutputSha256": sha(signature), "signedInputs": signed,
        "input": proof["inputs"]["jmdict"], "wholeJmdictEntriesScanned": count,
        "completeJmdictUnion": len(merged), "originalFamilies": len(original),
        "additionalFamilies": sorted(residual), "completeKanjidicRecords": kanjidic_records,
        "queries": len(final["queries"]), "absentQueries": sorted(label for label, n in counts.items() if not n),
        "memory": memory, "verifierSha256": sha(Path(__file__).read_bytes()),
        "reusedRecordVerifier": {"path": str(VERIFIER), "sha256": VERIFIER_SHA},
        "reusedSelector": {"path": str(Path(source_query_union.__file__)), "sha256": QUERY_SHA},
        "limits": "Complete pinned JMdict membership, record equality, canonical residual hashes, per-family labels, "
                  "query counts and audit totals for the final union. KANJIDIC2 records rely on the passing "
                  "earlier source proof. Linguistic adequacy, review and publication remain separate.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "Usage: verify_b130_final_sources.py <frozen-final-facts.json>")
    main(sys.argv[1])
