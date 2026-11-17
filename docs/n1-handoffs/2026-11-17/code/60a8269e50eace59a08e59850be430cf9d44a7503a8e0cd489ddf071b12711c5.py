import copy
import io
import unittest
import xml.etree.ElementTree as ET

import prepare_b130_source_facts_v2 as prep
from verify_b130_final_sources import (canonical_hash, check_final_facts, merge, verify_audit, verify_membership,
                                       verify_stream)
from verify_b130_payload import SOURCE_VERIFIER_SHA
from verify_reconciliation_sources import element_value

WALL, FENCE = "\u5840", "\u304b\u304d"
STREAM = f"""<?xml version="1.0" encoding="UTF-8"?>
<JMdict>
<entry><ent_seq>1</ent_seq><k_ele><keb>{WALL}</keb></k_ele><r_ele><reb>\u3078\u3044</reb></r_ele>
<sense><gloss>wall</gloss></sense></entry>
<entry><ent_seq>2</ent_seq><k_ele><keb>\u677f{WALL}</keb></k_ele><r_ele><reb>\u3044\u305f\u3079\u3044</reb></r_ele>
<sense><gloss>board fence</gloss></sense></entry>
<entry><ent_seq>3</ent_seq><k_ele><keb>\u57a3</keb></k_ele><r_ele><reb>{FENCE}</reb></r_ele>
<sense><gloss>fence</gloss></sense></entry>
<entry><ent_seq>4</ent_seq><k_ele><keb>\u4ed6</keb></k_ele><r_ele><reb>\u307b\u304b</reb></r_ele>
<sense><gloss>other</gloss></sense></entry>
</JMdict>
""".encode("utf-8")
QUERIES = sorted([f"contains-keb:{WALL}", f"exact-reb:{FENCE}", "exact-reb:\u306a\u3044"])
NODES = {node.findtext("ent_seq"): node for node in ET.fromstring(STREAM)}
LABEL = {"1": [f"contains:{WALL}"], "2": [f"contains:{WALL}"], "3": [f"exact-reading:{FENCE}"]}
COUNTS = {f"contains:{WALL}": 2, f"exact-reading:{FENCE}": 1, "exact-reading:\u306a\u3044": 0}


class Guard:
    def check(self):
        pass


def records(*identities):
    return {identity: element_value(NODES[identity]) for identity in identities}


def residual_raw():
    root = ET.Element("JMdict")
    root.append(copy.deepcopy(NODES["3"]))
    return ET.tostring(root, encoding="utf-8")


def stream(merged, hashes):
    return verify_stream(io.BytesIO(STREAM), QUERIES, merged, hashes, Guard())


class FinalSourceTests(unittest.TestCase):
    def setUp(self):
        self.merged, self.original = merge(records("1"), records("1", "2"), records("3"))
        self.hashes = {"3": canonical_hash(NODES["3"])}
        raw = residual_raw()
        self.audit = {
            "base": "b" * 40, "completeJmdictUnion": 3, "originalFamiliesRechecked": 2, "additionalFamilies": 1,
            "wholeJmdictEntriesScanned": 4, "completeKanjidicRecordsRechecked": 7,
            "queryCountsIncludingAbsences": COUNTS,
            "finalAdditionalOutput": {"source": "jmdict", "sha256": prep.sha(raw), "bytes": len(raw),
                                      "canonicalRecordHashes": self.hashes, "completeCanonicalEquality": True},
            "dictionaryInputs": {"jmdict": "x"}, "verification": "text", "producerSha256": "p" * 64,
        }
        self.audit_args = dict(base="b" * 40, merged=self.merged, original=self.original, residual_raw=raw,
                               residual_hashes=self.hashes, inputs={"jmdict": "x"}, producer_sha="p" * 64,
                               kanjidic_records=7)

    def test_complete_union_labels_counts_and_audit_pass(self):
        count, computed, counts = stream(self.merged, self.hashes)
        self.assertEqual((count, computed, counts), (4, LABEL, COUNTS))
        verify_membership({key: list(reversed(value)) for key, value in LABEL.items()}, computed)
        verify_audit(self.audit, count=count, counts=counts, **self.audit_args)

    def test_merge_rejects_overlap_and_conflicting_earlier_records(self):
        with self.assertRaises(ValueError):
            merge(records("1"), records("2"), records("2", "3"))
        changed = records("1")
        changed["1"] = element_value(NODES["2"])
        with self.assertRaises(ValueError):
            merge(records("1"), changed, records("3"))
        with self.assertRaises(ValueError):
            merge(records("1"), records("2"), {})

    def test_stream_rejects_missing_extra_altered_and_rehashed_families(self):
        missing = dict(self.merged)
        del missing["3"]
        extra = {**self.merged, **records("4")}
        altered = {**self.merged, "3": element_value(NODES["4"])}
        for merged, hashes in ((missing, {}), (extra, self.hashes), (altered, self.hashes),
                               (self.merged, {"3": "0" * 64})):
            with self.assertRaises(ValueError):
                stream(merged, hashes)

    def test_membership_rejects_label_drift_and_family_drift(self):
        for change in (lambda m: m.update({"3": [f"contains:{WALL}"]}), lambda m: m.pop("2"),
                       lambda m: m.update({"4": ["exact-reading:\u307b\u304b"]}),
                       lambda m: m.update({"1": [f"contains:{WALL}", f"contains:{WALL}"]})):
            changed = copy.deepcopy(LABEL)
            change(changed)
            with self.assertRaises(ValueError):
                verify_membership(changed, LABEL)

    def test_audit_rejects_total_absence_hash_input_and_producer_drift(self):
        count, _, counts = stream(self.merged, self.hashes)
        for change in (lambda a: a.update(completeJmdictUnion=519), lambda a: a.update(additionalFamilies=2),
                       lambda a: a.update(wholeJmdictEntriesScanned=5),
                       lambda a: a.update(completeKanjidicRecordsRechecked=192),
                       lambda a: a["queryCountsIncludingAbsences"].pop("exact-reading:\u306a\u3044"),
                       lambda a: a["finalAdditionalOutput"]["canonicalRecordHashes"].update({"3": "0" * 64}),
                       lambda a: a["finalAdditionalOutput"].update(bytes=1),
                       lambda a: a.update(dictionaryInputs={}), lambda a: a.update(producerSha256="q" * 64),
                       lambda a: a.update(extra=True)):
            changed = copy.deepcopy(self.audit)
            change(changed)
            with self.assertRaises(ValueError):
                verify_audit(changed, count=count, counts=counts, **self.audit_args)


class FinalFactsTests(unittest.TestCase):
    def setUp(self):
        self.source = {"batch": 130, "base": "b" * 40, "candidate": "c" * 40, "prefix": "p/",
                       "jmdictSelections": [{"file": "complete.xml", "mode": "union", "queries": QUERIES[:1]},
                                            {"file": "supplemental.xml", "mode": "union",
                                             "queries": ["exact-keb:\u57a3"]}]}
        self.proof = {"batch": 130, "base": "b" * 40, "candidate": "c" * 40, "status": "PASS",
                      "verifierSha256": SOURCE_VERIFIER_SHA, "facts": {"path": "facts.json", "sha256": "f"},
                      "sourceRecords": [{"path": "p/complete.xml", "sha256": "1"},
                                        {"path": "p/supplemental.xml", "sha256": "2"}]}
        self.final = {"batch": 130, "base": "b" * 40, "candidate": "c" * 40,
                      "sourceFacts": {"path": "facts.json", "sha256": "f"}, "sourceProof": "proof.json",
                      "files": ["complete.xml", "supplemental.xml", "final.xml"], "residual": "final.xml",
                      "membership": "m.json", "audit": "a.json", "readingKeys": "k.json", "mode": "union",
                      "queries": sorted([*QUERIES[:1], "exact-keb:\u57a3", f"exact-reb:{FENCE}"]),
                      "producer": {"name": "final.py", "sha256": "0" * 64},
                      "output": "does-not-exist-final-proof.json"}

    def test_facts_accept_only_reading_additions_bound_to_a_passing_proof(self):
        self.assertEqual(check_final_facts(self.final, self.source, self.proof, "f"),
                         {"complete.xml": "1", "supplemental.xml": "2"})
        for target, change in (
                ("final", lambda f: f["queries"].append("exact-keb:\u4ed6")),
                ("final", lambda f: f["queries"].remove(QUERIES[0])),
                ("final", lambda f: f.update(files=["supplemental.xml", "complete.xml", "final.xml"])),
                ("final", lambda f: f.update(residual="../final.xml")),
                ("final", lambda f: f.update(extra=1)),
                ("proof", lambda p: p.update(verifierSha256="0" * 64)),
                ("proof", lambda p: p.update(status="FAIL")),
                ("proof", lambda p: p["facts"].update(sha256="g")),
                ("proof", lambda p: p.update(candidate="d" * 40))):
            final, proof = copy.deepcopy(self.final), copy.deepcopy(self.proof)
            change(final if target == "final" else proof)
            with self.assertRaises(ValueError):
                check_final_facts(final, self.source, proof, "f")

    def test_preparer_adds_tested_keys_and_rejects_changed_producer(self):
        jm = [{"mode": "union", "queries": ["contains-keb:x"]}, {"mode": "union", "queries": ["exact-reb:y"]}]
        tested = {member: [f"k{position}"] for position, member in enumerate(prep.MEMBERS)}
        self.assertEqual(prep.final_queries(jm, tested),
                         sorted(["contains-keb:x", "exact-reb:y", "exact-reb:k0", "exact-reb:k1", "exact-reb:k2"]))
        for bad in ({**tested, prep.MEMBERS[0]: []}, {**tested, prep.MEMBERS[0]: ["k", "k"]},
                    {key: value for key, value in tested.items() if key != prep.MEMBERS[0]}):
            with self.assertRaises(ValueError):
                prep.final_queries(jm, bad)
        blobs = {"source-receipt.json": b"{}", "supplemental-source-receipt.json": b"{}",
                 "final-source-audit.json": b'{"producerSha256": "%s"}' % prep.FINAL_PRODUCER_SHA.encode(),
                 "producers/final_sources_b130.py": b"KEYS = {}\n"}
        with self.assertRaisesRegex(ValueError, "Final producer changed"):
            prep.final_selection(blobs.__getitem__, jm, [])


if __name__ == "__main__":
    unittest.main()
