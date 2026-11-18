import gzip
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from b128_common import BASE, HERE, PACKET, REPO, ROOT, git, sha, start_guard, write
from extract_b128 import HashReader, INPUTS, QUERIES, canonical

guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    checks = {}
    comparison_queries = json.loads((PACKET / "comparison-source-receipt.json").read_text(encoding="utf-8"))["exactKebOrRebQueries"]
    for label in ("jmdict", "kanjidic2"):
        files = ["jmdict-selected-records.xml", "jmdict-comparison-records.xml"] if label == "jmdict" else ["kanjidic2-selected-records.xml", "kanjidic2-comparison-records.xml", "kanjidic2-expanded-comparison-records.xml"]
        tag, identity = ("entry", "ent_seq") if label == "jmdict" else ("character", "literal")
        expected = {}
        for filename in files:
            for record in ET.parse(PACKET / filename).findall(tag):
                key, value = record.findtext(identity), canonical(record)
                assert key not in expected or expected[key] == value
                expected[key] = value
        path = ROOT / "control" / "inputs" / INPUTS[label][0]
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(65536), b""):
                guard.check()
                digest.update(chunk)
        assert digest.hexdigest() == INPUTS[label][1]
        matched, applicable, target_families = set(), set(), set()
        with gzip.open(path, "rb") as stream:
            reader = HashReader(stream, guard)
            context = ET.iterparse(reader, events=("start", "end"))
            _, root = next(context)
            for event, node in context:
                if event != "end" or node.tag != tag:
                    continue
                guard.check()
                key = node.findtext(identity)
                if label == "jmdict":
                    kebs = {k.text for k in node.findall("k_ele/keb")}
                    target_match = any("唇" in k or "脣" in k for k in kebs)
                    if target_match:
                        target_families.add(key)
                    if target_match or kebs & (QUERIES | (set(comparison_queries) - {"reading=ほとり"})) or "ほとり" in {r.text for r in node.findall("r_ele/reb")}:
                        applicable.add(key)
                if key in expected:
                    assert canonical(node) == expected[key], (label, key)
                    matched.add(key)
                node.clear()
                root.clear()
        assert matched == expected.keys()
        assert reader.digest.hexdigest() == INPUTS[label][2]
        if label == "jmdict":
            assert applicable == expected.keys() and len(applicable) == 103
        else:
            assert len(matched) == 46
        checks[label] = {
            "compressedSha256": digest.hexdigest(), "decompressedXmlSha256": reader.digest.hexdigest(),
            "completeRecordsCanonicalEqualToOriginal": True, "recordIdentities": sorted(matched),
            "allApplicableFamiliesIncluded": len(applicable) == 103 if label == "jmdict" else None,
            "targetContainingFamilies": len(target_families) if label == "jmdict" else None,
            "comparison": "Canonicalization strip_text=True removes formatting whitespace for field-completeness comparison. Raw output hashes remain distinct and unchanged.",
            "outputs": {name: {"sha256": sha((PACKET / name).read_bytes()), "bytes": (PACKET / name).stat().st_size} for name in files},
        }
    gates = json.loads((HERE / "author-gates-002" / "summary.json").read_text(encoding="utf-8"))
    integrity = json.loads((HERE / "preservation-author-001" / "summary.json").read_text(encoding="utf-8"))
    assert gates["status"] == integrity["status"] == "PASS"
    assert gates["manifestSha256"] == integrity["manifestSha256"] == sha((REPO / "manifest.json").read_bytes())
    for name in ("lint", "quiz-safety"):
        assert "0 error(s), 0 warning(s)" in (HERE / "author-gates-002" / (name + ".log")).read_text(encoding="utf-8")
    assert "0 production hit(s)" in (HERE / "author-gates-002" / "reading-exposure.log").read_text(encoding="utf-8")
    previous = json.loads(git("show", f"{BASE}:docs/n1-sources/batch-127-progress.json"))
    assert previous["accounting"]["publishedPendingRecordsWithCards"] == 257
    external = json.loads((HERE / "external-pages" / "receipt.json").read_text(encoding="utf-8"))
    for page in external:
        assert sha(Path(page["localCapture"]).read_bytes()) == page["rawSha256"]
    write(PACKET / "complete-source-verification-002.json", checks)
    for path in sorted(HERE.glob("*.py")):
        write(PACKET / "producers" / path.name, path.read_bytes())
    for folder in ("author-gates-001", "author-gates-002", "preservation-author-001", "pre-remarks-fix-001"):
        for path in sorted((HERE / folder).iterdir()):
            if path.name != "runtime-hashes.json" and path.is_file():
                write(PACKET / folder / path.name, path.read_bytes())
    for path in sorted(HERE.glob("*-memory-*.json")):
        write(PACKET / "execution-evidence" / path.name, path.read_bytes())
    for filename in ("fetch-001.json", "candidate-survey-001.json"):
        write(PACKET / "execution-evidence" / filename, (HERE / filename).read_bytes())
    write(PACKET / "author-evidence.json", {
        "status": "author-gates-passed-independent-review-pending", "base": BASE,
        "gateDirectory": str(HERE / "author-gates-002"), "gateSummarySha256": sha((HERE / "author-gates-002" / "summary.json").read_bytes()),
        "preservationDirectory": str(HERE / "preservation-author-001"), "preservationSummarySha256": sha((HERE / "preservation-author-001" / "summary.json").read_bytes()),
        "tenSerialChecks": gates["checks"], "manifestSha256": gates["manifestSha256"],
        "contentVersion": integrity["contentVersion"], "manifestMappedRuntimeEntries": integrity["candidateRuntimeCount"],
        "baselineMappedRuntimeEntries": integrity["baselineRuntimeCount"],
        "localArchiveBudget": {"entriesIncludingPackagingAndDirectories": 8740, "retainedBytes": 45446824, "inflatedBytes": 45715162, "localZipBytes": 30881842},
        "sourcePacket": "source-receipt.json", "completeRecordVerification": "complete-source-verification-002.json",
        "completeRecords": {"jmdict": 103, "kanjidic2": 46}, "scanBaselineCards": 1247, "scanPairs": 42, "actualComparisonCardsRead": 45,
        "warnings": {"finalScopedLint": 0, "finalQuizSafety": 0, "validationErrors": 0, "initialQuizSafety": 1, "fontMissing": "脣 U+8123 absent from all three bundled subsets; no rendered fallback acceptance"},
        "preservedFailures": [{"gate": "linkplan", "attempt": "author-gates-001", "cause": "Runner lacked existing --remarks allowance for the stale no-card sentence.", "disposition": "Use exact one-occurrence stale-remark input; no validator weakened. Original runner/logs/receipts preserved in pre-remarks-fix-001."}],
        "readingExposure": {"explicitExtras": ["唇=おどろく,ほとり,くちひる,ふるえる,しん"], "productionHits": 0, "starterPaddingHits": 0, "latentCollisions": 2, "seedsPerPool": 100, "scope": "Full N1/All and restricted Starter padding host model only; 石 is not Starter-tagged, leaving one analyzed fallback slot."},
        "resourcePolicy": {"admitAboveBytes": 2147483648, "abortBelowBytes": 1073741824, "sampleSeconds": 0.25, "maxChildWaitSeconds": 0.1, "cleanupTimeoutSecondsPerStage": 10},
        "limits": "No independent review or publication. Committed checks and signature/cleanliness bind separately in final scratch handoff, avoiding self-referential commit hashes. Vocabulary remains pilot-stage coverage 2122/2431, not whole-set closure.",
    })
    write(REPO / "docs" / "n1-sources" / "batch-128-progress.json", {
        "schemaVersion": 1, "batch": "128", "baseCommit": BASE,
        "membership": ["唇"], "sourceRows": [159],
        "status": "local-unreviewed-authoring-candidate", "drafted": ["唇"],
        "reviewClosed": [], "published": [], "runtimePublished": False,
        "accounting": {
            "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 257,
            "publishedN1Additions": 251, "n2Placements": 6, "undelivered": 971,
            "localUnreviewedDrafts": 1, "otherUndeliveredOutsideThisDraft": 970,
            "overallN1TaskComplete": False, "reviewClosedPendingRecordsWithCards": 257,
            "notStarted": 970,
        },
        "declaringWords": {"唇": ["唇"]}, "requiredReciprocalPairs": [["唇", "唇"]],
        "requiredLinkPairs": 1, "newWordArticles": 0,
        "sourceEvidence": "batch-128/source-receipt.json",
        "comparisonEvidence": ["batch-128/baseline-gloss-scan.json", "batch-128/baseline-gloss-scan-002.json", "batch-128/pair-dispositions.json"],
        "authorAudit": "batch-128/author-audit.md", "authorEvidence": "batch-128/author-evidence.json",
        "packetInventory": "batch-128/packet-files.json",
        "completeSourceVerification": "batch-128/complete-source-verification-002.json",
        "runtimeCandidate": {"manifestSha256": integrity["manifestSha256"], "contentVersion": integrity["contentVersion"], "manifestMappedRuntimeEntries": integrity["candidateRuntimeCount"]},
        "authorGates": {"status": "PASS", "summary": "batch-128/author-gates-002/summary.json", "summarySha256": sha((HERE / "author-gates-002" / "summary.json").read_bytes()), "committedChecks": "To be bound separately after signing; not claimed in advance."},
        "deferredCandidates": [{"kanji": "伯", "sourceRow": 33}, {"kanji": "憶", "sourceRow": 395}, {"kanji": "撲", "sourceRow": 461}],
        "limits": ["Independent review/publication remain with the coordinator.", "Host/static evidence only, not arbitrary/custom/multiple-borrow or Kotlin/native/device acceptance.", "Variant 脣 lacks bundled subset coverage; rendered fallback not checked.", "Not whole-set acceptance; local drafts are not delivered."],
    })
    index = {p.relative_to(PACKET).as_posix(): {"bytes": p.stat().st_size, "sha256": sha(p.read_bytes())} for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "packet-files.json", {"hashMode": "raw bytes, no line-ending normalization", "files": index, "excludes": ["packet-files.json"]})
    print(json.dumps({"completeSources": {k: {"records": len(v["recordIdentities"]), "targetContainingFamilies": v["targetContainingFamilies"]} for k, v in checks.items()}, "packetFiles": len(index) + 1, "runtime": integrity["contentVersion"], "authorGateSummarySha256": sha((HERE / "author-gates-002" / "summary.json").read_bytes())}, ensure_ascii=False))
finally:
    write(HERE / "finalization-memory-001.json", guard.finish())
