import gzip
import hashlib
import json
import xml.etree.ElementTree as ET
from b127_common import BASE, HERE, PACKET, REPO, ROOT, git, sha, start_guard, write
from extract_b127 import HashReader, canonical

guard = start_guard()
try:
    receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))
    checks = {}
    for name in ("jmdict", "kanjidic2"):
        files = ["jmdict-selected-records.xml"] if name == "jmdict" else ["kanjidic2-selected-records.xml", "kanjidic2-comparison-records.xml", "kanjidic2-expanded-comparison-records.xml"]
        tag, identity = ("entry", "ent_seq") if name == "jmdict" else ("character", "literal")
        expected = {}
        for filename in files:
            for record in ET.parse(PACKET / filename).findall(tag):
                key, value = record.findtext(identity), canonical(record)
                assert key not in expected or expected[key] == value
                expected[key] = value
        path = ROOT / "control" / "inputs" / receipt["dictionaryInputs"][name]["filename"]
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(65536), b""):
                guard.check()
                digest.update(chunk)
        assert digest.hexdigest() == receipt["dictionaryInputs"][name]["compressedSha256"]
        matched, applicable = set(), set()
        with gzip.open(path, "rb") as stream:
            reader = HashReader(stream, guard)
            context = ET.iterparse(reader, events=("start", "end"))
            _, root = next(context)
            for event, node in context:
                if event != "end" or node.tag != tag:
                    continue
                guard.check()
                key = node.findtext(identity)
                if name == "jmdict" and any("倉" in (k.text or "") for k in node.findall("k_ele/keb")):
                    applicable.add(key)
                if key in expected:
                    assert canonical(node) == expected[key], (name, key)
                    matched.add(key)
                node.clear()
                root.clear()
        assert matched == expected.keys()
        assert reader.digest.hexdigest() == receipt["dictionaryInputs"][name]["decompressedXmlSha256"]
        if name == "jmdict":
            assert applicable == expected.keys() and len(applicable) == 78
        checks[name] = {
            "compressedSha256": digest.hexdigest(), "decompressedXmlSha256": reader.digest.hexdigest(),
            "completeRecordsCanonicalEqualToOriginal": True, "recordIdentities": sorted(matched),
            "allApplicableFamiliesIncluded": len(applicable) == 78 if name == "jmdict" else None,
            "comparison": "XML canonicalization strip_text=True removes formatting whitespace for field-completeness comparison. Raw output hashes remain distinct and unchanged.",
        }
    write(PACKET / "complete-source-verification-002.json", checks)
    gates = json.loads((HERE / "author-gates-002" / "summary.json").read_text(encoding="utf-8"))
    integrity = json.loads((HERE / "preservation-author-001" / "summary.json").read_text(encoding="utf-8"))
    assert "0 error(s), 0 warning(s)" in (HERE / "author-gates-002" / "lint.log").read_text()
    assert "0 error(s), 0 warning(s)" in (HERE / "author-gates-002" / "quiz-safety.log").read_text()
    for filename in (
        "b127_common.py", "extract_b127.py", "inspect_b127.py", "expand_scan_b127.py",
        "author_packet_b127.py", "generate_b127.py", "generate_b127_002.py",
        "check_reading_b127.py", "run_b127_gates.py", "preserve_b127.py",
        "finalize_b127.py", "commit_b127.py", "write_handoff_b127.py",
    ):
        write(PACKET / "producers" / filename, (HERE / filename).read_bytes())
    for folder in ("author-gates-001", "author-gates-002", "preservation-author-001"):
        for path in sorted((HERE / folder).iterdir()):
            if path.name != "runtime-hashes.json" and path.is_file():
                write(PACKET / folder / path.name, path.read_bytes())
    for path in sorted(HERE.glob("*-memory-*.json")):
        write(PACKET / "execution-evidence" / path.name, path.read_bytes())
    write(PACKET / "execution-evidence" / "font-diagnostic-001.json", (HERE / "font-diagnostic-001.json").read_bytes())
    write(PACKET / "author-evidence.json", {
        "status": "author-gates-passed-independent-review-pending", "base": BASE,
        "gateDirectory": str(HERE / "author-gates-002"), "gateSummarySha256": sha((HERE / "author-gates-002" / "summary.json").read_bytes()),
        "preservationDirectory": str(HERE / "preservation-author-001"), "preservationSummarySha256": sha((HERE / "preservation-author-001" / "summary.json").read_bytes()),
        "tenSerialChecks": gates["checks"], "manifestSha256": gates["manifestSha256"],
        "contentVersion": integrity["contentVersion"], "runtimeEntries": integrity["candidateRuntimeCount"],
        "sourcePacket": "source-receipt.json", "completeRecordVerification": "complete-source-verification-002.json",
        "warnings": {"finalScopedLint": 0, "finalQuizSafety": 0, "validationErrors": 0, "initialQuizSafety": 7, "fontContrastGlyphMissing": "宀 U+5B80 absent from all three bundled subsets; no rendered fallback acceptance"},
        "preservedFailures": [{"producer": "generate_b127.py", "result": "AssertionError at line 26 requiring all queried code points in every cmap; diagnostic established that contrast-only 宀 is missing. Original strokes were valid and verified byte-identical by attempt 002."}],
        "readingExposure": {"explicitExtras": ["倉=にわか,ほろぶ,もろし,おさめる,ひとや"], "productionHits": 0, "starterPaddingHits": 0, "latentCollisions": 0, "seedsPerPool": 100},
        "resourcePolicy": {"admitAboveBytes": 2147483648, "abortBelowBytes": 1073741824, "sampleSeconds": 0.25, "maxChildWaitSeconds": 0.1},
        "limits": "No independent review or publication. Committed checks and signature/cleanliness bind separately in the final scratch handoff, avoiding a self-referential commit hash. Vocabulary remains pilot-stage coverage, not whole-set closure.",
    })
    previous = json.loads(git("show", f"{BASE}:docs/n1-sources/batch-126-progress.json"))
    assert previous["accounting"]["publishedPendingRecordsWithCards"] == 256
    write(REPO / "docs" / "n1-sources" / "batch-127-progress.json", {
        "schemaVersion": 1, "batch": "127", "baseCommit": BASE,
        "membership": ["倉"], "sourceRows": [57],
        "status": "local-unreviewed-authoring-candidate", "drafted": ["倉"],
        "reviewClosed": [], "published": [], "runtimePublished": False,
        "accounting": {
            "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 256,
            "publishedN1Additions": 250, "n2Placements": 6, "undelivered": 972,
            "localUnreviewedDrafts": 1, "otherUndeliveredOutsideThisDraft": 971,
            "overallN1TaskComplete": False, "reviewClosedPendingRecordsWithCards": 256,
            "notStarted": 971,
        },
        "declaringWords": {"倉": ["倉庫"]}, "requiredReciprocalPairs": [["倉", "倉庫"]],
        "requiredLinkPairs": 1, "newWordArticles": 0,
        "sourceEvidence": "batch-127/source-receipt.json",
        "comparisonEvidence": ["batch-127/baseline-gloss-scan.json", "batch-127/baseline-gloss-scan-002.json", "batch-127/pair-dispositions.json"],
        "authorAudit": "batch-127/author-audit.md", "authorEvidence": "batch-127/author-evidence.json",
        "packetInventory": "batch-127/packet-files.json",
        "completeSourceVerification": "batch-127/complete-source-verification-002.json",
        "runtimeCandidate": {"manifestSha256": integrity["manifestSha256"], "contentVersion": integrity["contentVersion"], "runtimeEntries": integrity["candidateRuntimeCount"]},
        "authorGates": {"status": "PASS", "summary": "batch-127/author-gates-002/summary.json", "summarySha256": sha((HERE / "author-gates-002" / "summary.json").read_bytes()), "committedChecks": "To be bound separately after signing; not claimed in advance."},
        "deferredCandidates": [{"kanji": "伯", "sourceRow": 33}, {"kanji": "憶", "sourceRow": 395}, {"kanji": "撲", "sourceRow": 461}],
        "limits": ["Independent review/publication remain with the coordinator.", "Host/static evidence only, not arbitrary/custom/multiple-borrow or Kotlin/native/device acceptance.", "Contrast-only 宀 lacks bundled subset coverage; rendered fallback not checked.", "Not whole-set acceptance; local drafts are not delivered."],
    })
    index = {p.relative_to(PACKET).as_posix(): {"bytes": p.stat().st_size, "sha256": sha(p.read_bytes())} for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "packet-files.json", {"hashMode": "raw bytes, no line-ending normalization", "files": index, "excludes": ["packet-files.json"]})
    print(json.dumps({"completeSources": checks, "packetFiles": len(index) + 1, "runtime": integrity["contentVersion"], "authorGateSummarySha256": sha((HERE / "author-gates-002" / "summary.json").read_bytes())}, ensure_ascii=False))
finally:
    write(HERE / "finalization-memory-001.json", guard.finish())
