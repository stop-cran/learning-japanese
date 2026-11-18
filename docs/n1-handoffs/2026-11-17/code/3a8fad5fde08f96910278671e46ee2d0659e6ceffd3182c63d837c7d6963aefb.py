"""Build complete, compact, neutral B131 source contract and packet; never review or launch."""
import copy
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from b131_neutral_common_001 import (
    BASE, CANDIDATE, CHECKS, HERE, MEMBERS, PACKET, PROOFS, RECORDS, REPO, RUNNER,
    SNAP, SOURCE_BASE, TOOLS, WS, freeze_json, frozen, json_bytes, require, sha,
    start_guard, write_frozen)
from b129_confirmation_presentation import canonical, compact_xml
from b128_external_sources import extract as external_extract, METHOD as EXTERNAL_METHOD
from source_query_union import selects
from verify_b131_sources import FINGERPRINT, Git, OWNER

PREFIX = "docs/n1-sources/batch-131/"
JOYO_SHA = "cc740aed34751e40831e4ab526408401667a428cefcf0fdd0212848eb31d67cb"


def union_records(selections, tag, identity, read):
    merged, bindings = {}, []
    for item in selections:
        raw = read(item["file"])
        root = ET.fromstring(raw)
        records = root.findall(tag)
        require(len(records) == len(root), "Unexpected non-record dictionary child")
        ids = []
        for node in records:
            key = node.findtext(identity)
            require(key and key not in ids, "Missing or duplicate identity inside selection")
            ids.append(key)
            if key in merged:
                require(canonical(ET.tostring(node, encoding="utf-8"))
                        == canonical(ET.tostring(merged[key], encoding="utf-8")),
                        "Conflicting duplicate dictionary record: " + key)
            else:
                merged[key] = copy.deepcopy(node)
        bindings.append({**item, "sha256": sha(raw), "completeMatchingRecords": len(ids),
                         "identities": ids})
    return merged, bindings


def main():
    require(not HERE.exists() and not PACKET.exists(), "Preserve every existing preparation artifact")
    guard, _ = start_guard("B131 complete neutral source/packet construction")
    git = Git(REPO, RUNNER, guard)
    files, contract_files, signed = {}, {}, {}

    def put(name, raw):
        require(name not in files, "Duplicate packet member")
        files[name] = raw

    def blob(name, revision=CANDIDATE):
        guard.check()
        return git("show", revision + ":" + name)

    def source(name):
        raw = blob(PREFIX + name)
        signed[PREFIX + name] = sha(raw)
        return raw

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "B131 checkout is not the clean frozen candidate")

    try:
        clean()
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate signature/parent differs")
        proofs = {name: json.loads(frozen(RECORDS / name, digest)) for name, digest in PROOFS.items()}
        require(all(p["candidate"] == CANDIDATE and p["base"] == BASE and p["status"] == "PASS"
                    and not p["memory"]["breach"] for p in proofs.values()), "Unadmitted proof")
        source_proof = proofs["source-verification-001.json"]
        payload = proofs["payload-verification-001.json"]
        gate = proofs["gate-verification-002/verification.json"]
        packet_proof = proofs["packet-verification-002/verification.json"]
        facts = json.loads(frozen(source_proof["facts"]["path"], source_proof["facts"]["sha256"]))
        require(payload["sourceProof"]["sha256"] == PROOFS["source-verification-001.json"]
                and gate["payloadProofSha256"] == PROOFS["payload-verification-001.json"]
                and packet_proof["sourceUnionProofSha256"] == PROOFS["source-union-verification-001.json"],
                "Proof graph differs")

        def original(name):
            raw = source(name)
            contract_files["original/" + name] = raw
            expected = next(row["sha256"] for row in source_proof["sourceRecords"]
                            if row["path"] == PREFIX + name)
            require(sha(raw) == expected, "Source selection changed")
            return raw

        jm, jm_bindings = union_records(facts["jmdictSelections"], "entry", "ent_seq", original)
        kd, kd_bindings = union_records(facts["kanjidic2Selections"], "character", "literal", original)
        for name in ("jmdict-final-families.xml", "jmdict-final-families-002.xml"):
            raw = source(name)
            require(sha(raw) == proofs["source-union-verification-001.json"]["signedInputs"][PREFIX + name]
                    and len(ET.fromstring(raw)) == 0, "Expected verified empty final residual")
            contract_files["original/" + name] = raw
        require(len(jm) == 874 and len(kd) == 182, "Complete union record counts differ")
        presentations = {}
        for name, root_tag, tag, records in (
            ("jmdict-families.xml", "JMdict", "entry", [jm[k] for k in sorted(jm, key=int)]),
            ("kanjidic2-records.xml", "kanjidic2", "character",
             [kd[k] for k in MEMBERS] + [kd[k] for k in sorted(set(kd) - set(MEMBERS))])):
            root = ET.Element(root_tag)
            root.extend(records)
            original_raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
            compact = compact_xml(original_raw)
            require(canonical(original_raw) == canonical(compact)
                    and len(ET.fromstring(compact).findall(tag)) == len(records),
                    "Lossy XML presentation")
            require(max(map(len, compact.splitlines())) < 13900, "Complete record exceeds read budget")
            contract_files[name] = compact
            put("evidence/" + name, compact)
            presentations[name] = {"records": len(records), "sha256": sha(compact),
                                   "canonicalSha256": sha(canonical(original_raw).encode("utf-8")),
                                   "canonicalEqual": True, "oneCompleteRecordPerLine": True,
                                   "bytes": len(compact), "lines": len(compact.splitlines())}
        queries = sorted({q for selection in facts["jmdictSelections"] for q in selection["queries"]})
        dictionary_index = {q: sorted((key for key, node in jm.items()
                                      if selects(node, "entry", key, "union", [q])), key=int)
                            for q in queries}
        require({key for ids in dictionary_index.values() for key in ids} == set(jm),
                "Dictionary index omits records")
        put("evidence/dictionary-index.json", json_bytes(dictionary_index))
        put("evidence/xml-presentation.json", json_bytes({
            "representation": "Complete XML records, indentation removed, one complete record per line.",
            "method": "ElementTree canonicalize(strip_text=True). Canonical equality checks every ordered "
                      "element, attribute and text value. Readings, restrictions, language attributes, "
                      "secondary senses and complete records are retained; no semantic projection.",
            "files": presentations, "sourceSelections": jm_bindings + kd_bindings,
            "emptyResidualFiles": ["jmdict-final-families.xml", "jmdict-final-families-002.xml"],
            "limits": "Presentation line numbers differ from original source serialization. Original "
                      "selections remain in the immutable neutral source contract. Compactness does "
                      "not establish comprehension or prevent future context compaction."}))

        manifest_raw = blob("manifest.json")
        require(sha(manifest_raw) == payload["manifestSha256"], "Runtime manifest changed")
        manifest = json.loads(manifest_raw)
        kanji_names = sorted((name for name in manifest["files"] if name.startswith("kanji/")),
                             key=lambda name: ord(Path(name).stem))
        require(len(kanji_names) == 1257, "Candidate card count differs")
        for offset in range(0, len(kanji_names), 100):
            names = kanji_names[offset:offset + 100]
            for name, (_, raw) in zip(names, git.objects([CANDIDATE + ":" + n for n in names])):
                put("repo/" + name, raw)
            guard.check()
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        titles = []
        for name in kanji_names:
            metadata, _ = parse(files["repo/" + name].decode("utf-8").replace("\r\n", "\n"))
            titles.append((Path(name).stem, f"{Path(name).stem} {metadata['title']}"))
        put("evidence/title-index.txt", ("\n".join(line for _, line in titles) + "\n").encode("utf-8"))
        baseline_names = git("ls-tree", "-r", "--name-only", BASE, "--", "kanji").decode().splitlines()
        require(len(baseline_names) == 1254 and set(kanji_names) - set(baseline_names)
                == {f"kanji/{c}.md" for c in MEMBERS}, "Baseline title inventory differs")
        for offset in range(0, len(baseline_names), 100):
            names = baseline_names[offset:offset + 100]
            for name, (_, raw) in zip(names, git.objects([BASE + ":" + n for n in names])):
                require(files["repo/" + name] == raw, "Legacy article changed")
            guard.check()
        put("evidence/baseline-title-index.txt",
            ("\n".join(line for char, line in titles if char not in MEMBERS) + "\n").encode("utf-8"))
        changed_words = [item["path"] for item in payload["supportLinks"]]
        require(len(changed_words) == len(set(changed_words)) == 4, "Support inventory differs")
        for member in payload["members"]:
            char = member["kanji"]
            require(sha(files[f"repo/kanji/{char}.md"]) == member["articleSha256"], "Card changed")
            put(f"snapshot/kanji/{char}.md", files[f"repo/kanji/{char}.md"])
            put(f"snapshot/strokes/{char}.json", blob(f"strokes/{char}.json"))
        for item in payload["supportLinks"]:
            name = item["path"]
            before, after = blob(name, BASE), blob(name)
            require(sha(before) == item["beforeSha256"] and sha(after) == item["afterSha256"],
                    "Support snapshot changed")
            put("baseline/" + name, before)
            put("snapshot/" + name, after)
            put("repo/" + name, after)
        put("diffs/existing.diff", git("diff", "--no-color", BASE, CANDIDATE, "--", *changed_words))
        put("repo/manifest.json", manifest_raw)
        for name in ("docs/content-format.md", "docs/jlpt-levels.md"):
            put("repo/" + name, blob(name))
        for name in (".github/copilot-instructions.md",
                     ".github/instructions/content-structure.instructions.md"):
            put("rubric/" + Path(name).name, blob(name))
        rows = json.loads(source("source-rows.json"))
        require([r["sourceRow"] for r in rows] == [977, 870, 1174]
                and [r["kanji"] for r in rows] == MEMBERS, "Source rows differ")
        put("evidence/source-metadata.json", json_bytes({
            r["kanji"]: {**r["metadata"], "sourceRow": r["sourceRow"]} for r in rows}))
        font_raw = source("stroke-font-evidence-002.json")
        require(sha(font_raw) == packet_proof["signedInputs"][PREFIX + "stroke-font-evidence-002.json"],
                "Final cmap evidence changed")
        fonts = json.loads(font_raw)
        initial = json.loads(source("stroke-font-evidence.json"))
        put("evidence/font-cmap.json", font_raw)
        shapes = []
        for row in payload["generatedGeometry"]:
            filename = f"{ord(row['kanji']):05x}.svg"
            raw = source("kanjivg/" + filename)
            require(sha(raw) == row["svgSha256"], "Geometry SVG changed")
            put("evidence/kanjivg/" + filename, raw)
            shapes.append({**row, "revision": initial["kanjivgRevision"],
                           "converterSha256": payload["converterSha256"],
                           "groups": [dict(node.attrib) for node in
                                      ET.fromstring(raw).iter("{http://www.w3.org/2000/svg}g")],
                           "scope": "Reproduced geometry and bounded cmaps, not rendered/native/device acceptance."})
        put("evidence/shape-evidence.json", json_bytes(shapes))
        joyo_raw = (WS / "scratch-111" / "joyo-pages.json").read_bytes()
        require(sha(joyo_raw) == JOYO_SHA, "Pinned Joyo cache changed")
        pages = json.loads(joyo_raw)
        put("evidence/joyo-rows.json", json_bytes({
            "cacheSha256": JOYO_SHA,
            "rows": [{"kanji": char, "matches": [
                {"printedPage": int(page), "completeCachedPage": text}
                for page, text in pages.items()
                if re.search(r"(?m)^" + re.escape(char) + r"(?:[ \t\uff08(]|$)", text)]}
                for char in MEMBERS],
            "scope": "Complete cached pages with member-leading lines, not newly inspected PDF glyphs. "
                     "A missing exact row is not a reading or usage verdict."}))
        put("evidence/joyokanjihyo_20101130.pdf",
            (WS / "review-packets" / "_checks-109-fix" / "joyokanjihyo_20101130.pdf").read_bytes())

        gate_bindings = {}
        for name in CHECKS:
            receipt_binding = gate["capturedInputs"][f"committed/{name}.json"]
            log_binding = gate["capturedInputs"][f"committed/{name}.log"]
            receipt_raw = frozen(receipt_binding["path"], receipt_binding["sha256"])
            log = frozen(log_binding["path"], log_binding["sha256"])
            receipt = json.loads(receipt_raw)
            require(receipt["gate"] == name and receipt["exitCode"] == 0
                    and receipt["logSha256"] == sha(log) and not receipt["memory"]["breach"],
                    "Committed check receipt differs")
            put(f"checks/{name}.txt", log)
            put(f"checks/{name}.json", receipt_raw)
            gate_bindings[name] = {"receiptSha256": sha(receipt_raw), "logSha256": sha(log)}
        external_bindings = json.loads(source("external-capture-bindings.json"))
        snapshots = []
        for index, item in enumerate(external_bindings["captures"], 1):
            name = Path(item["localRawCapture"]).name
            binding = packet_proof["capturedInputs"]["external/" + name]
            raw = frozen(binding["path"], binding["sha256"])
            require(sha(raw) == item["rawSha256"] and len(raw) == item["rawBytes"],
                    "Captured response changed")
            text, problem = external_extract(raw, item["finalUrl"], [item["character"]])
            require(problem is None and text, "External complete-section extraction: " + str(problem))
            extract = text.encode("utf-8")
            require(max(map(len, extract.splitlines())) < 13900, "Complete external line exceeds read budget")
            put(f"{SNAP}/{index:02d}-response.html", raw)
            put(f"{SNAP}/{index:02d}-extract.txt", extract)
            snapshots.append({
                "index": index, "character": item["character"], "provider": item["provider"],
                "citedUrl": item["url"], "finalUrl": item["finalUrl"], "capturedAt": item["capturedAt"],
                "status": "SUPPLIED",
                "response": {"path": f"{SNAP}/{index:02d}-response.html", "sha256": sha(raw)},
                "extract": {"path": f"{SNAP}/{index:02d}-extract.txt", "sha256": sha(extract),
                            "bytes": len(extract), "lines": len(extract.splitlines())}})
            guard.check()
        put(f"{SNAP}/manifest.json", json_bytes({
            "candidate": CANDIDATE, "snapshotSet": "B131 complete captured external sections",
            "scope": "Six existing verified captures; no new fetch or author-selected passage.",
            "extractionMethod": EXTERNAL_METHOD.replace("B128", "B131"),
            "snapshots": snapshots, "limits": "HTML layout/images and rendered glyphs not visually verified."}))
        snapshot = json.loads(blob("docs/n1-source-snapshot.json"))
        put("evidence/provenance.json", json_bytes({
            "candidate": CANDIDATE, "base": BASE, "sourceBase": SOURCE_BASE,
            "baseBridge": "Original selection/scan base retained; signed adaptation bridges identical "
                          "1254-card baseline trees. Old scans are not relabelled.",
            "pinnedInputs": snapshot["inputs"], "familyCount": len(jm), "kanjidicRecords": len(kd),
            "dictionaryAttribution": snapshot["dictionaryAttribution"],
            "kanjivgAttribution": snapshot["kanjivgAttribution"],
            "kanjivgRevision": initial["kanjivgRevision"],
            "sourceNormalization": "Complete canonical-equal compact XML. Original selections preserved.",
            "fontScope": packet_proof["fontScope"],
            "proofs": {name: digest for name, digest in PROOFS.items()},
            "limits": "Mechanical reproduction only; no linguistic, native, device or delivered acceptance."}))
        put("eligibility-reference.json", json_bytes({
            "newCards": MEMBERS, "otherRequiredCards": [],
            "cards": [{"card": m["kanji"], "source": f"snapshot/kanji/{m['kanji']}.md",
                       "sha256": m["articleSha256"], "distractors": m["metadata"]["distractors"],
                       "quiz_exclusions": m["metadata"]["quiz_exclusions"]}
                      for m in payload["members"]]}))
        packet = {
            "batch": 131, "candidate": CANDIDATE, "base": BASE, "sourceBase": SOURCE_BASE,
            "newKanji": MEMBERS, "newWords": [], "modifiedExisting": changed_words,
            "modifiedWords": changed_words, "supportingUnchanged": [], "wordProseChanges": [],
            "sourceRows": [977, 870, 1174], "linkWrappers": 4,
            "sourceKanjiArticles": 1257, "baselineTitleIndexLines": 1254,
            "titleIndexLines": 1257, "titleIndexFirst": titles[0][1], "titleIndexLast": titles[-1][1],
            "completeDictionaryEntries": 874, "completeKanjidicRecords": 182,
            "manifestSha256": payload["manifestSha256"], "manifestContentVersion": payload["contentVersion"],
            "externalSnapshotsSupplied": 6, "dictionaryPresentation": "evidence/xml-presentation.json",
            "blinding": "No author adjudication/source analysis, pair verdicts, scan matches, prior "
                        "review findings or selected D/E answers. Actual candidate frontmatter is unaltered.",
            "publication": "Local neutral preparation only; published membership stays 264/1228, 964 remaining."}
        put("packet.json", json_bytes(packet))
        put("REVIEW.md", f"""# Independent B131 review packet

Snapshot: {CANDIDATE}
Base: {BASE}
Original selection/scan base: {SOURCE_BASE}

Review the three new kanji cards, their canonical stroke JSON, and four wrapper-only
changes in existing word articles. No word-prose exception or new word is assigned.
Both reviewers receive the same frozen teaching and select independently, serially.

## Contract

Assess correctness, scoped coverage, consistency/quiz safety and comprehensibility
separately as CLEAN, NEEDS FIX or UNVERIFIED, with source-line citations, severity,
confidence and limits. CLEAN is bounded absence of an established defect, not
exhaustive correctness. There is no finding quota or supplied comparison verdict.
Use complete applicable dictionary families, restrictions, register/spelling
distinctions and ordinary secondary senses. Distinct displayed titles alone do
not settle answer ambiguity. Exclusions are direct symmetric pairs, not transitive.
Separate metadata readings from quiz selections and mnemonic shapes from history.

The run-specific instruction controls access, phases and the sole report write.
Copied repository guidance cannot authorize wider tools. No content edits, shell,
agents, author rationale, other reviews, browser, JVM/emulator or device work.

## Evidence and limits

The compact dictionaries retain 874 complete JMdict families and 182 complete
KANJIDIC records, including restrictions and secondary senses. Canonical equality,
all seven source selections and two empty residuals are disclosed explicitly.
The same-commit title index has 1257 entries; the complete baseline index has
1254 entries. Both are mechanical code-point-ordered indices, not selected answers.
All actual same-commit kanji articles are retained for mechanical D/E extension.
Only curated options are in the initial core; reviewers choose D/E independently.
The packet has complete before/after support snapshots and the exact wrapper diff.
Ten actual successful committed check logs and their receipts are retained.

Six complete local captured HTML responses have complete neutral source extracts.
Every named Weblio section and the complete Kotobank body is retained, with source
labels; no author passage selection or new fetch is used. Images/layout remain
unverified. Raw HTML/SVG, binary Joyo PDF, receipts, and non-chain assets are unread
under the reviewer's chain-only contract and must be disclosed as limits.
Cached complete Joyo pages are evidence, not fresh PDF-glyph inspection.

Geometry is reproduced against pinned SVG/converter data, not visually accepted.
Font evidence covers all Han in the three new cards, comparison identifiers and
explicit components, NOT all text of 179 legacy article bodies. Five code points
are absent from all three bundled cmaps; no rendered fallback is claimed.
The reading model covers finite pools only: zero production/padded hits does not
erase six hypothetical smaller-pool collisions or establish arbitrary/custom,
multiple-borrow, Kotlin, native or device acceptance.

Mechanical source/gate preparation is not linguistic review or delivery.
Published membership remains 264/1228 with 964 remaining; B131 adds no delivery.
""".encode("utf-8"))
        clean()
        contract = {
            "batch": 131, "candidate": CANDIDATE, "base": BASE, "sourceBase": SOURCE_BASE,
            "completeRecordCounts": {"jmdict": 874, "kanjidic2": 182},
            "selections": jm_bindings + kd_bindings, "signedSources": signed,
            "method": "Verified signed selections; identity duplicates require complete canonical equality. "
                      "Compact complete ordered XML records, no projection/adjudication. Empty final residuals "
                      "retained, not confused with missing sources.",
            "proofs": PROOFS, "presentation": presentations,
            "files": {name: write_frozen(HERE / "source-contract" / name, raw)
                      for name, raw in contract_files.items()}}
        contract_binding = freeze_json(HERE / "source-contract.json", contract)
        for name, raw in files.items():
            write_frozen(PACKET / name, raw)
            guard.check()
        sums = freeze_json(PACKET / "SHA256SUMS.json", {name: sha(raw) for name, raw in sorted(files.items())})
        config = freeze_json(HERE / "batch.json", {
            "batch": 131, "candidate": CANDIDATE, "base": BASE, "sourceBase": SOURCE_BASE,
            "repo": str(REPO), "members": MEMBERS, "expectedKanji": 1257,
            "gates": str(RECORDS / "gate-verification-002" / "committed"),
            "sourceContract": contract_binding, "contentFormatLines": None})
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Packet construction RAM breach")
    result = freeze_json(HERE / "packet-build.json", {
        "status": "PREPARED_NOT_REVIEWED", "batch": 131, "candidate": CANDIDATE, "base": BASE,
        "packet": str(PACKET), "packetManifest": sums, "packetManifestSha256": sums["sha256"],
        "sourceContract": contract_binding, "batchConfig": config, "files": len(files),
        "gateBindings": gate_bindings, "externalCaptures": len(snapshots),
        "tool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "memory": memory, "limits": "Preparation only; no reviewer launched, admitted or accepted."})
    print(json.dumps(result))


if __name__ == "__main__":
    main()
