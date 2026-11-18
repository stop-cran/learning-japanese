"""Freeze evidence filenames and proof bindings from the signed B130 handoff."""
import json
from pathlib import Path

from common import freeze_json, frozen, require, sha
from verify_b130_payload import BASE, HERE, MEMBERS, PREFIX, REPO
from verify_b130_evidence_v3 import check_facts

CANDIDATE = "ce1b5c895fac90852143f322a115c2de4e768e20"
PACKET = REPO / PREFIX


def proof(name, digest):
    path = HERE / name
    data = json.loads(frozen(path, digest))
    require(data["candidate"] == CANDIDATE and data["status"] == "PASS", "Wrong signed proof")
    return {"path": str(path), "sha256": digest}


facts = {
    "batch": 130, "candidate": CANDIDATE,
    "sourceProof": proof("source-proof-001.json", "75d06c0408e76a5f56a64fc9b2134ccdf1e083f99b87f944f8d459022b5160ec"),
    "payloadProof": proof("payload-proof-001.json", "9519cac98cf5f4d05224dd3493db591e113b93ff040328718ba5151851e28f2a"),
    "finalSourceProof": proof("final-source-proof-001.json", "5ccfb3f5b9c033ac69ac47f5d595b5dba76273fa4cd63266e3558070517d9002"),
    "inventory": "evidence-inventory.json", "supersededInventories": [],
    "queryMaps": {"jmdict-complete-families.xml": "query-membership.json",
                  "jmdict-supplemental-families.xml": "supplemental-query-membership.json"},
    "receipts": {"source-receipt.json": "survey_b130.py",
                 "supplemental-source-receipt.json": "supplement_b130.py",
                 "final-source-audit.json": "final_sources_b130.py"},
    "expectedJmdictFamilies": 519, "pairDispositions": "pair-dispositions-002.json",
    "scanDirectories": ["scans", "scans-002"], "scanRows": 1251,
    "externalBindings": {"external-capture-bindings.json": 6, "supplemental-external-bindings.json": 1},
    "fontEvidence": "stroke-font-evidence.json",
    "producers": sorted(path.name for path in (PACKET / "producers").iterdir()),
    "commonHelper": "b130_common.py", "readingCheck": "check_reading_b130.py",
    "readingKeys": "reading-keys.json",
    "requiredReadingKeys": json.loads((PACKET / "reading-keys.json").read_bytes())["testedKeys"],
    "linkplanArgs": ["verify", BASE, *MEMBERS], "wordProseExceptions": [], "summaryBatch": "130",
    "gates": {
        "author": {"directory": "author-gates-002", "runner": "run_b130_gates.py",
                   "signedCopy": "author-evidence/author-gates-002"},
        "committed": {"directory": "committed-gates-001", "runner": "run_b130_gates.py", "signedCopy": None},
    },
    "preservation": {"directory": "committed-preserve-001", "producer": "preserve_b130.py"},
    "output": "evidence-verification-001",
}
check_facts(facts)
print(freeze_json(HERE / "evidence-facts-001.json", facts))
