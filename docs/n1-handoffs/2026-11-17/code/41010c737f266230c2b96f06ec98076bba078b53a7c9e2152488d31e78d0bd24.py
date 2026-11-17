"""Re-verify B134 fresh-review packet hashes, source unions, projection, indexes, and chain."""
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
FINAL = ROOT / "fresh-independent-002" / "projected-successor-008"
PACKET = FINAL / "packet"
CORE = FINAL / "fresh-independent-core-001.json"
REPO = WS / "b134-worktree"
CANDIDATE = "355cccb840d22e7313e79f234eb93d1367e00352"
BASE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
PUBLISHED = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
OWNER = "stop-cran@list.ru"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
sys.path.insert(0, str(WS / "review-tools"))
sys.path.insert(0, str(FINAL / "tools"))
from common import require, sha, start_guard, write_frozen
from capacity008 import project, xml_bytes, source_class


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def xml_map(raw, root_tag, record_tag, identity):
    root = ET.fromstring(raw)
    require(root.tag == root_tag, "XML root mismatch")
    result = {}
    for node in root:
        key = node.findtext(identity)
        require(node.tag == record_tag and key and key not in result, "Invalid or duplicate XML identity")
        result[key] = canonical(node)
    return result


def merged_equal(left_raw, right_raw, union_raw, root_tag, record_tag, identity):
    result, overlaps = {}, []
    for raw in (left_raw, right_raw):
        for key, value in xml_map(raw, root_tag, record_tag, identity).items():
            if key in result:
                require(result[key] == value, "Overlapping source records are not fully canonical-equal: " + key)
                overlaps.append(key)
            else:
                result[key] = value
    require(result == xml_map(union_raw, root_tag, record_tag, identity),
            "Merged union omits, alters, or adds source records")
    return {"originalRecords": len(xml_map(left_raw, root_tag, record_tag, identity)),
            "supplementalRecords": len(xml_map(right_raw, root_tag, record_tag, identity)),
            "canonicalEqualOverlaps": len(overlaps), "uniqueRecords": len(result)}


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), "-c", "core.quotepath=false", *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def verify_chain(core, guard):
    sums = json.loads((PACKET / "SHA256SUMS.json").read_text(encoding="utf-8"))
    source_rows = core["sources"]
    require(source_rows and len({row["source"] for row in source_rows}) == len(source_rows),
            "Core source list is empty or duplicated")
    sources = {}
    for row in source_rows:
        name = row["source"]
        raw = (PACKET / name).read_bytes()
        require(sha(raw) == row["sha256"] == sums[name], "Core source hash differs: " + name)
        sources[name] = raw.splitlines(keepends=True)
    rebuilt = {name: [] for name in sources}
    for index, segment in enumerate(core["segments"], 1):
        guard.check()
        raw = Path(segment["path"]).read_bytes()
        require(segment["index"] == index and sha(raw) == segment["sha256"]
                and len(raw) == segment["bytes"] < 16000, "Core segment binding differs")
        lines = raw.splitlines(keepends=True)
        for part in segment["parts"]:
            name = part["source"]
            require(name in sources and part["sha256"] == sha((PACKET / name).read_bytes()),
                    "Core part source binding differs")
            expected = b"".join(sources[name][part["a"] - 1:part["b"]])
            actual = b"".join(lines[part["segmentStart"] - 1:part["segmentEnd"]])
            require(expected == actual, "Core segment payload differs: " + name)
            rebuilt[name].append((part["a"], part["b"], expected))
    for name, raw_lines in sources.items():
        parts = sorted(rebuilt[name])
        next_line = 1
        assembled = []
        for start, end, raw in parts:
            require(start == next_line, "Core source has a missing or overlapping line range: " + name)
            assembled.append(raw)
            next_line = end + 1
        require(next_line == len(raw_lines) + 1 and b"".join(assembled) == b"".join(raw_lines),
                "Core source is incomplete: " + name)
    return {"sources": len(source_rows), "segments": len(core["segments"]),
            "totalSegmentBytes": sum(row["bytes"] for row in core["segments"])}


def verify_dictionary_index(packet, supplemental_ids):
    original = json.loads((packet / "evidence" / "source-selection-provenance-original.json").read_text(encoding="utf-8"))
    receipt = json.loads((packet / "evidence" / "reconciliation-query-receipt-neutral.json").read_text(encoding="utf-8"))
    membership = json.loads((packet / "evidence" / "reconciliation-query-membership.json").read_text(encoding="utf-8"))
    jm = ET.fromstring((packet / "evidence" / "jmdict-families.xml").read_bytes())
    queries = sorted({q for selection in original["selections"] if selection["file"].startswith("jmdict")
                      for q in selection.get("queries", [])})
    actual = {}
    for query in queries:
        kind, value = query.split(":", 1)
        if kind == "contains-keb":
            actual[query] = sorted({n.findtext("ent_seq") for n in jm
                                    if any(value in (k.text or "") for k in n.findall("k_ele/keb"))}, key=int)
        elif kind == "exact-keb":
            actual[query] = sorted({n.findtext("ent_seq") for n in jm
                                    if any(value == (k.text or "") for k in n.findall("k_ele/keb"))}, key=int)
        elif kind in {"exact-reading", "exact-reb"}:
            actual[query] = sorted({n.findtext("ent_seq") for n in jm
                                    if any(value == (r.text or "") for r in n.findall("r_ele/reb"))}, key=int)
        else:
            raise ValueError("Unknown original dictionary selector: " + query)
    for query in sorted(receipt["countsIncludingZero"]):
        kind, value = query.split(":", 1)
        key = "supplemental:" + query
        if kind == "exact-spelling":
            actual[key] = sorted({n.findtext("ent_seq") for n in jm
                                  if any(value == (k.text or "") for k in n.findall("k_ele/keb"))}, key=int)
        elif kind == "exact-reading":
            actual[key] = sorted({n.findtext("ent_seq") for n in jm
                                  if any(value == (r.text or "") for r in n.findall("r_ele/reb"))}, key=int)
        else:
            raise ValueError("Unknown supplemental dictionary selector: " + query)
    stored = json.loads((packet / "evidence" / "dictionary-index.json").read_text(encoding="utf-8"))
    require(actual == stored, "Complete selected-query dictionary index differs from merged records")
    require(len(original["zeroMatchQueries"]) == sum(not actual[q] for q in queries),
            "Original zero-match predicate count differs from the exact complete index")
    supplemental_zeroes = [key for key, identities in receipt["countsIncludingZero"].items()
                           if not identities]
    require(len(supplemental_zeroes) == sum(not actual["supplemental:" + key]
                                            for key in receipt["countsIncludingZero"]),
            "Supplemental zero-match predicate count differs from the exact complete index")
    require(set(membership) == supplemental_ids
            and all(isinstance(value, list) for value in membership.values()),
            "Supplemental query membership map is incomplete or malformed")
    for query in receipt["countsIncludingZero"]:
        indexed = set(actual["supplemental:" + query])
        selected = {identity for identity, queries in membership.items() if query in queries}
        require(indexed == selected, "Supplemental query membership differs: " + query)
    return {"originalPredicates": len(queries), "originalZeroMatches": len(original["zeroMatchQueries"]),
            "supplementalPredicates": len(receipt["countsIncludingZero"]),
            "supplementalZeroMatches": len(supplemental_zeroes),
            "indexedPredicates": len(actual), "indexedRecordMembershipRows": len(membership),
            "dictionaryIndexSha256": sha((packet / "evidence" / "dictionary-index.json").read_bytes())}


def main():
    guard, _ = start_guard("B134 fresh independent packet completeness verification")
    try:
        sums_raw = (PACKET / "SHA256SUMS.json").read_bytes()
        sums = json.loads(sums_raw)
        files = {path.relative_to(PACKET).as_posix(): path.read_bytes()
                 for path in PACKET.rglob("*") if path.is_file() and path.name != "SHA256SUMS.json"}
        require(set(files) == set(sums), "Frozen packet file inventory differs")
        for name, raw in files.items():
            guard.check()
            require(sha(raw) == sums[name], "Packet hash mismatch: " + name)
        candidate_identity = git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
        require(candidate_identity == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}",
                "Candidate signature or parent differs")
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate worktree changed")

        original_selection = json.loads((PACKET / "evidence" / "source-selection-provenance-original.json").read_text(encoding="utf-8"))
        original_jm = (PACKET / "evidence" / "jmdict-original-union-399.xml").read_bytes()
        supplemental_jm = (PACKET / "evidence" / "jmdict-supplemental-194.xml").read_bytes()
        merged_jm = (PACKET / "evidence" / "jmdict-families.xml").read_bytes()
        original_kd = (PACKET / "evidence" / "kanjidic2-original-union-59.xml").read_bytes()
        supplemental_kd = (PACKET / "evidence" / "kanjidic2-supplemental-37.xml").read_bytes()
        merged_kd = (PACKET / "evidence" / "kanjidic2-complete-union.xml").read_bytes()
        jm_stats = merged_equal(original_jm, supplemental_jm, merged_jm,
                                "JMdict", "entry", "ent_seq")
        kd_stats = merged_equal(original_kd, supplemental_kd, merged_kd,
                                "kanjidic2", "character", "literal")
        require(jm_stats == {"originalRecords": 399, "supplementalRecords": 194,
                             "canonicalEqualOverlaps": 71, "uniqueRecords": 522},
                "JMdict complete-union membership differs")
        require(kd_stats == {"originalRecords": 59, "supplementalRecords": 37,
                             "canonicalEqualOverlaps": 11, "uniqueRecords": 85},
                "KANJIDIC2 complete-union membership differs")

        expected_projection = xml_bytes(project(merged_kd))
        projected = (PACKET / "evidence" / "kanjidic2-review-projection.xml").read_bytes()
        require(expected_projection == projected, "KD projection is not exactly derived from full records")
        full_kd_map = xml_map(merged_kd, "kanjidic2", "character", "literal")
        units = {path.stem: path.read_bytes() for path in
                 (PACKET / "evidence" / "kanjidic2-full-records").glob("*.xml")}
        require(set(units) == set(full_kd_map), "Full KD optional-unit identity inventory differs")
        for literal, raw in units.items():
            unit_record = ET.fromstring(raw)
            require(unit_record.tag == "character" and unit_record.findtext("literal") == literal
                    and canonical(unit_record) == full_kd_map[literal],
                    "Full KD optional unit differs: " + literal)

        selections = original_selection["selections"]
        jm_original_ids = set().union(*(set(row["identities"]) for row in selections
                                       if row["file"].startswith("jmdict")))
        kd_original_ids = set().union(*(set(row["identities"]) for row in selections
                                       if row["file"].startswith("kanjidic2")
                                       or row["file"].startswith("supplement/kanjidic2")))
        require(len(jm_original_ids) == 399 and jm_original_ids == set(xml_map(original_jm, "JMdict", "entry", "ent_seq")),
                "Original JMdict selection membership differs")
        require(len(kd_original_ids) == 59 and kd_original_ids == set(xml_map(original_kd, "kanjidic2", "character", "literal")),
                "Original KANJIDIC2 selection membership differs")
        require(original_selection["queryCount"] == 182 and len(original_selection["zeroMatchQueries"]) == 6,
                "Original predicate/zero-match provenance is incomplete")
        receipt = json.loads((PACKET / "evidence" / "reconciliation-query-receipt-neutral.json").read_text(encoding="utf-8"))
        require(len(receipt["countsIncludingZero"]) == 140, "Supplemental predicate provenance incomplete")
        supplemental_jm_ids = set(xml_map(supplemental_jm, "JMdict", "entry", "ent_seq"))
        index_stats = verify_dictionary_index(PACKET, supplemental_jm_ids)

        candidate_articles = sorted((PACKET / "repo" / "kanji").glob("*.md"))
        candidate_paths = {path.name for path in candidate_articles}
        git_candidate_paths = {Path(p).name for p in git("ls-tree", "-r", "--name-only", CANDIDATE, "--", "kanji").decode().splitlines()
                               if p.endswith(".md")}
        git_parent_paths = {Path(p).name for p in git("ls-tree", "-r", "--name-only", BASE, "--", "kanji").decode().splitlines()
                            if p.endswith(".md")}
        git_published_paths = {Path(p).name for p in git("ls-tree", "-r", "--name-only", PUBLISHED, "--", "kanji").decode().splitlines()
                               if p.endswith(".md")}
        require(len(candidate_paths) == 1262 and candidate_paths == git_candidate_paths,
                "Candidate article packet is not the complete signed article set")
        require(len(git_published_paths) == 1261 and "紫.md" not in git_published_paths
                and len(git_parent_paths) == 1262 and "紫.md" in git_parent_paths
                and len(git_candidate_paths) == 1262 and "紫.md" in git_candidate_paths,
                "Published/parent/candidate article identities differ")
        title_index = (PACKET / "evidence" / "title-index.txt").read_bytes()
        parent_title_index = (PACKET / "evidence" / "parent-title-index-ba80.txt").read_bytes()
        published_title_index = (PACKET / "evidence" / "published-title-index-e17.txt").read_bytes()
        delta = json.loads((PACKET / "evidence" / "baseline-title-delta.json").read_text(encoding="utf-8"))
        parent_candidate_delta = json.loads((PACKET / "evidence" / "reconciliation-title-delta.json").read_text(encoding="utf-8"))
        purple_line = "紫 purple; violet\n".encode("utf-8")
        require(title_index == parent_title_index and delta["baselineCommit"] == PUBLISHED
                and delta["candidateCommit"] == BASE and delta["removedCompleteLinesUtf8"] == ["紫 purple; violet\n"]
                and delta["candidateSha256"] == sha(parent_title_index)
                and delta["reconstructedBaselineSha256"] == sha(published_title_index)
                and parent_title_index.replace(purple_line, b"", 1) == published_title_index
                and parent_candidate_delta["baselineCommit"] == BASE
                and parent_candidate_delta["candidateCommit"] == CANDIDATE
                and parent_candidate_delta["byteEqual"] is True,
                "Three-identity title-index binding differs")
        title_chars = [line.split(" ", 1)[0] for line in title_index.decode("utf-8").splitlines()]
        require(title_chars == sorted(title_chars, key=ord), "Title index order is not codepoint order")

        manifest = json.loads(files["repo/manifest.json"])
        parent_manifest = json.loads(files["parent/manifest.json"])
        published_manifest = json.loads(files["baseline/manifest.json"])
        group_names = ["audio", "curriculum", "files", "images", "listening", "listeningTaskAudio",
                       "listeningTaskImages", "listeningTasks", "scenes"]
        require(all(name in manifest for name in group_names), "Manifest group is missing")
        published_entries = sum(len(published_manifest[name]) for name in group_names)
        parent_entries = sum(len(parent_manifest[name]) for name in group_names)
        after_entries = sum(len(manifest[name]) for name in group_names)
        require((published_entries, parent_entries, after_entries) == (8745, 8747, 8747),
                "Published/parent/candidate runtime manifest entry counts differ")
        require(sha(files["baseline/manifest.json"]) == "f29fd2000d9ae078382df44711e3af1b5b5e81424160f5ab06c74ec8a416a11a"
                and sha(files["parent/manifest.json"]) == "2a3373ec1a529cfcd8f1b1bc5686915e4335facc62a1f593b94ed26914273a77"
                and sha(files["repo/manifest.json"]) == "d16cf5a73bcfd6f837bfab1b92ce7e8d683a5baf57610357ae9cf3c0a6493ca3",
                "Published/parent/candidate manifest hashes differ")
        baseline_identity = json.loads(files["evidence/published-baseline-identity.json"])
        parent_identity = json.loads(files["evidence/reconciliation-parent-identity.json"])
        require(baseline_identity["commit"] == PUBLISHED and baseline_identity["kanjiArticles"] == 1261
                and baseline_identity["kanjiPurpleArticle"] == "absent"
                and baseline_identity["titleIndexSha256"] == sha(published_title_index)
                and parent_identity["commit"] == BASE and parent_identity["kanjiArticles"] == 1262
                and parent_identity["titleIndexSha256"] == sha(parent_title_index),
                "Explicit baseline identity metadata differs")
        require(files["baseline/words/紫.md"] == git("show", f"{PUBLISHED}:words/紫.md")
                and files["parent/words/紫.md"] == git("show", f"{BASE}:words/紫.md")
                and files["snapshot/words/紫.md"] == git("show", f"{CANDIDATE}:words/紫.md")
                and files["parent/kanji/紫.md"] == git("show", f"{BASE}:kanji/紫.md")
                and files["snapshot/kanji/紫.md"] == git("show", f"{CANDIDATE}:kanji/紫.md"),
                "Support/card revision sources differ from their exact commits")
        binding = json.loads(files["evidence/signed-reconciliation-binding.json"])
        require(binding["candidate"] == CANDIDATE and binding["base"] == BASE
                and binding["candidateManifestSha256"] == sha(files["repo/manifest.json"])
                and binding["candidateCardSha256"] == sha(files["repo/kanji/紫.md"])
                and binding["baseSupportSha256"] == binding["candidateSupportSha256"]
                and binding["supportUnchanged"] is True,
                "Signed card/support/index binding differs")
        proof_bindings = json.loads(files["evidence/source-proof-bindings.json"])
        expected_proofs = {
            "reconciliationVerification": ROOT / "reconciliation-verification-001" / "verification.json",
            "reconciliationGateVerification": ROOT / "reconciliation-gate-verification-001" / "verification.json",
            "confirmationDossier": ROOT / "confirmation-dossier-002" / "dossier.json",
        }
        for label, proof_path in expected_proofs.items():
            record = proof_bindings["proofs"][label]
            proof_raw = proof_path.read_bytes()
            require(sha(proof_raw) == record["sha256"]
                    and str(proof_path) == record["path"], "Bound source proof differs: " + label)
            proof = json.loads(proof_raw)
            if label != "confirmationDossier":
                require(proof["status"] == "PASS" and proof["candidate"] == CANDIDATE,
                        "Reconciliation proof identity differs: " + label)
                if label == "reconciliationVerification":
                    require(proof["initialSnapshot"] == BASE,
                            "Reconciliation initial snapshot differs")
        packet_proof_path = ROOT / "packet-verification-001" / "verification.json"
        packet_proof_raw = packet_proof_path.read_bytes()
        require(sha(packet_proof_raw) == "fb95e655419fe9ecc0465ac565fb309397fb8843c22362b08cf5a1feda4d478a"
                and json.loads(packet_proof_raw)["status"] == "PASS",
                "Coordinator packet-verification proof is not the bound PASS proof")

        forbidden_paths = [name for name in files if any(token in name.lower() for token in
                           ("author-response", "pair-disposition", "scan-match", "prior-review",
                            "reports/", "comparison-recommendation"))]
        require(not forbidden_paths, "Blind-input exclusion violation: " + repr(forbidden_paths))
        core = json.loads(CORE.read_text(encoding="utf-8"))
        chain_stats = verify_chain(core, guard)
        class_fix = {
            "reconciliation/evidence/native-紫-kotobank-extract.txt": "extract",
            "reconciliation/checks/quiz-safety.log": "checks",
        }
        for path, expected in class_fix.items():
            require(source_class(path)[0] == expected, "Capacity source class differs: " + path)

        result = {
            "status": "PASS_COMPLETE_SOURCE_AND_PACKET_INTEGRITY",
            "candidate": CANDIDATE, "base": BASE, "publishedBaseline": PUBLISHED,
            "packetFiles": len(files), "packetInventorySha256": sha(sums_raw),
            "articleCounts": {"published": len(git_published_paths), "parent": len(git_parent_paths),
                              "candidate": len(candidate_paths)},
            "runtimeEntries": {"published": published_entries, "parent": parent_entries,
                               "candidate": after_entries},
            "coordinatorPacketVerificationSha256": sha(packet_proof_raw),
            "sourceUnions": {"jmdict": jm_stats, "kanjidic2": kd_stats},
            "originalSelections": {"jmdictIdentities": len(jm_original_ids),
                "kanjidic2Identities": len(kd_original_ids),
                "predicateCount": original_selection["queryCount"],
            "zeroMatchCount": len(original_selection["zeroMatchQueries"])},
            "supplementalPredicates": index_stats,
            "fullKDProjection": {"retainedRecords": len(full_kd_map),
                "optionalFullRecordUnits": len(units),
                "projectionSha256": sha(projected)},
            "titleIndexes": {"published": {"sha256": sha(published_title_index), "lines": 1261},
                "parent": {"sha256": sha(parent_title_index), "lines": 1262},
                "candidate": {"sha256": sha(title_index), "lines": 1262}, "codepointOrdered": True},
            "coreChain": chain_stats,
            "coreManifestSha256": sha(CORE.read_bytes()),
            "capacity": {"status": "NOT_MEASURED_BY_PACKET_VERIFIER",
                "reviewAdmission": "NOT_AUTHORIZED",
                "note": "The coordinator performs exact-current-tokenizer measurement separately."},
            "exclusions": {"authorResponseAndPriorReviewContent": "not present in packet"},
        }
        out = FINAL / "source-completeness-verification-009.json"
        print(json.dumps(write_frozen(out, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()),
                         ensure_ascii=False))
    finally:
        require(not guard.finish()["breach"], "Source completeness verification RAM breach")


if __name__ == "__main__":
    main()
