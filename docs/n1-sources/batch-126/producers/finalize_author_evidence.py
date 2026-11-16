import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from b126_common import BASE, HERE, PACKET, REPO, ROOT, git, sha, start_guard, write


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


guard = start_guard()
try:
    frozen = json.loads(git("show", f"{BASE}:docs/n1-sources/baseline-word-candidates.json"))
    candidates = [r for r in frozen if r["kanji"] == "傘"]
    assert len(candidates) == 1 and candidates[0]["word"] == "傘" and candidates[0]["primaryReading"] == "かさ"
    declaring, incidental = [], []
    for folder in ("kanji", "words"):
        for path in sorted((REPO / folder).glob("*.md")):
            guard.check()
            text = path.read_text(encoding="utf-8")
            if "傘" not in text:
                continue
            rel = folder + "/" + path.name
            if rel in ("kanji/傘.md", "words/傘.md"):
                continue
            incidental.append({"path": rel, "sha256": sha(path.read_bytes()), "disposition": "Incidental example/comparison, not a declared support-word identity; no wrapper required."})
    for path in sorted((REPO / "words").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^kanji: \[([^\]]*)\]$", text, re.M)
        if match and "傘" in [s.strip() for s in match.group(1).split(",")]:
            declaring.append({"path": "words/" + path.name, "reading": re.search(r"^reading: (.+)$", text, re.M).group(1), "sha256": sha(path.read_bytes()), "linkPresent": "[傘](../kanji/傘.md)" in text})
    assert len(declaring) == 1 and declaring[0]["path"] == "words/傘.md" and declaring[0]["linkPresent"]
    assert len(incidental) == 16
    write(PACKET / "support-audit.json", {
        "baseCommit": BASE, "frozenCandidateRecords": candidates, "allActiveDeclaringArticles": declaring,
        "requiredReciprocalPairs": [["傘", "傘"]], "incidentalOccurrences": incidental,
        "limits": "All active word metadata and literal occurrences checked; no requirement to link incidental examples.",
    })
    receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))
    source_checks = {}
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
        from extract_b126_reader import HashReader
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
                if name == "jmdict" and any("傘" in (k.text or "") for k in node.findall("k_ele/keb")):
                    applicable.add(key)
                if key in expected:
                    assert canonical(node) == expected[key], (name, key)
                    matched.add(key)
                node.clear()
                root.clear()
        assert matched == expected.keys()
        assert reader.digest.hexdigest() == receipt["dictionaryInputs"][name]["decompressedXmlSha256"]
        if name == "jmdict":
            assert applicable == expected.keys() and len(applicable) == 56
        source_checks[name] = {
            "compressedSha256": digest.hexdigest(), "decompressedXmlSha256": reader.digest.hexdigest(),
            "allCompleteRecordsCanonicalEqualToOriginal": True, "recordIdentities": sorted(matched),
            "allApplicableFamiliesIncluded": len(applicable) == 56 if name == "jmdict" else None,
            "comparison": "XML canonicalization with strip_text=True removes formatting whitespace only for field-completeness comparison; original output raw hashes remain distinct and unchanged.",
        }
    write(PACKET / "complete-source-verification.json", source_checks)
    write(PACKET / "selection-002.json", {
        "extends": "selection.json", "membership": [{"kanji": "傘", "sourceRow": 70}],
        "actualBaselineScan": "baseline-gloss-scan-002.json", "directMeaningGuards": ["被"],
        "curatedChoices": ["金", "全", "合"], "comparisonCards": sorted(p.stem for p in (PACKET / "comparison-cards").glob("*.md")),
        "sourceReadingAddendum": "JMdict 1774770 positively attests single-character spelling 傘/からかさ. Retained as separate whole-word reading, explicitly checked, not inserted into frozen on/kun metadata.",
    })
    for filename in (
        "b126_common.py", "candidate_inventory.py", "broader_inventory.py", "extract_b126.py",
        "expand_semantic_scan.py", "generate_b126.py", "check_reading_b126.py",
        "run_b126_gates.py", "preserve_b126.py", "extract_b126_reader.py",
        "finalize_author_evidence.py",
    ):
        write(PACKET / "producers" / filename, (HERE / filename).read_bytes())
    for folder in ("author-gates-001", "preservation-author-001"):
        for path in sorted((HERE / folder).iterdir()):
            if path.name == "runtime-hashes.json":
                continue
            if path.is_file():
                write(PACKET / folder / path.name, path.read_bytes())
    for filename in ("candidate-inventory-001.json", "candidate-inventory-memory-001.json", "broader-inventory-001.json", "broader-inventory-memory-001.json", "extraction-memory-001.json", "expanded-scan-memory-001.json", "generation-memory-001.json"):
        write(PACKET / "discovery-evidence" / filename, (HERE / filename).read_bytes())
    gates = json.loads((HERE / "author-gates-001" / "summary.json").read_text(encoding="utf-8"))
    integrity = json.loads((HERE / "preservation-author-001" / "summary.json").read_text(encoding="utf-8"))
    write(PACKET / "author-evidence.json", {
        "status": "author-gates-passed-independent-review-pending", "base": BASE,
        "gateDirectory": str(HERE / "author-gates-001"), "gateSummarySha256": sha((HERE / "author-gates-001" / "summary.json").read_bytes()),
        "preservationDirectory": str(HERE / "preservation-author-001"), "preservationSummarySha256": sha((HERE / "preservation-author-001" / "summary.json").read_bytes()),
        "tenSerialChecks": gates["checks"], "manifestSha256": gates["manifestSha256"],
        "contentVersion": integrity["contentVersion"], "runtimeEntries": integrity["candidateRuntimeCount"],
        "sourcePacket": "source-receipt.json", "completeRecordVerification": "complete-source-verification.json",
        "warnings": {"scopedLint": 0, "quizSafety": 0, "validationErrors": 0},
        "readingExposure": {"explicitExtra": "傘=からかさ", "productionHits": 0, "starterPaddingHits": 0, "latentCollisions": 0, "seedsPerPool": 100},
        "resourcePolicy": {"admitAboveBytes": 2147483648, "abortBelowBytes": 1073741824, "sampleSeconds": 0.25, "maxChildWaitSeconds": 0.1},
        "limits": "No independent review or publication. Committed checks and signature/cleanliness bind to a later final handoff outside this candidate, avoiding a self-referential commit hash.",
    })
    index = {p.relative_to(PACKET).as_posix(): {"bytes": p.stat().st_size, "sha256": sha(p.read_bytes())} for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "packet-files.json", {"hashMode": "raw bytes, no line-ending normalization", "files": index, "excludes": ["packet-files.json"]})
    print(json.dumps({"completeSources": source_checks, "packetFiles": len(index) + 1, "runtime": integrity["contentVersion"], "authorGateSummarySha256": sha((HERE / "author-gates-001" / "summary.json").read_bytes())}, ensure_ascii=False))
finally:
    write(HERE / "finalization-memory-001.json", guard.finish())
