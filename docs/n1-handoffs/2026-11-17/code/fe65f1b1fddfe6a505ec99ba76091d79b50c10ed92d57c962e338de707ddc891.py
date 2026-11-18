"""Build isolated B134 neutral inputs; never reviews, launches, or changes teaching."""
import copy
import importlib.util
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
HERE = ROOT / "neutral-preparation-001" / "complete-record-trial"
PACKET = HERE / "packet"
PROTOCOL = HERE / "protocol-001"
OLD_ROOT = WS / "scratch-132" / "review"
OLD = OLD_ROOT / "neutral-preparation-002"
REPO = WS / "b134-worktree"
BASE = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
CANDIDATE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
MEMBERS = ["紫"]
RUNNER_SHA = "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"
RUNNER = {"path": str(ROOT / "guarded-test-v3.py"), "sha256": RUNNER_SHA}
PROOFS = {
    "source-proof-002.json": "f3a80ee569a1bfd4f452e3f413a6377f5d01cac665e978dfc3e6db722c809393",
    "payload-proof-001.json": "ec47228ee313a82d872e7235f6f4a6b048737f24254d26405418c840dbd65d1a",
    "gate-verification-002/verification.json": "1caed56d80a213605d59eac6cc7ecc69829083cbdaa606b684edd77fb9162694",
}
PREFIX = "docs/n1-sources/batch-133/"
sys.path.insert(0, str(WS / "review-tools"))
from common import CHECKS, SNAP, freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen
from verify_b134_sources import FINGERPRINT, Git, OWNER
from b129_confirmation_presentation import canonical, compact_xml
from b128_external_sources import extract, METHOD
from source_query_union import selects


def load(name, digest=None):
    return json.loads(frozen(name, digest))


def clean(git):
    require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
            and not git("status", "--porcelain=v1", "--untracked-files=all"),
            "Checkout is not the clean frozen candidate")
    require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
            == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Signature/parent/owner mismatch")


def core_names(payload, reference):
    names = ["REVIEW.md", "packet.json", "rubric/copilot-instructions.md",
             "rubric/content-structure.instructions.md", "repo/docs/content-format.md",
             "repo/docs/jlpt-levels.md"]
    for char in MEMBERS:
        names += [f"snapshot/kanji/{char}.md", f"snapshot/strokes/{char}.json"]
    for support in payload["supportLinks"]:
        names += ["baseline/" + support["path"], "snapshot/" + support["path"]]
    names += ["diffs/existing.diff", "diffs/runtime-content.diff"]
    for gate in CHECKS:
        names += [f"checks/{gate}.log", f"checks/{gate}.json"]
    names += ["evidence/reading-keys.json", "checks/full-runtime-summary.json",
              "evidence/source-selection-provenance.json",
              "evidence/source-metadata.json", "evidence/xml-presentation.json",
              "evidence/jmdict-families.xml", "evidence/kanjidic2-records.xml",
              "evidence/dictionary-index.json", "evidence/joyo-rows.json",
              "evidence/font-cmap.json", "evidence/shape-evidence.json", "evidence/provenance.json",
              "evidence/baseline-title-delta.json", "evidence/title-index.txt"]
    names += [f"repo/kanji/{c}.md" for c in dict.fromkeys(
        char for row in reference["cards"] for char in row["distractors"])]
    names += [f"{SNAP}/manifest.json"] + [f"{SNAP}/{i:02d}-extract.txt" for i in range(1, 3)]
    require(len(names) == len(set(names)), "Duplicate core source")
    return names


def packet():
    require(not PACKET.exists(), "Preserve existing packet")
    guard, _ = start_guard("B134 complete neutral packet")
    git = Git(REPO, RUNNER, guard)
    files, originals = {}, {}

    def put(name, raw):
        require(name not in files and raw, "Duplicate/empty packet member: " + name)
        files[name] = raw

    def blob(name, rev=CANDIDATE):
        guard.check()
        return git("show", rev + ":" + name)

    try:
        clean(git)
        proofs = {n: load(ROOT / n, d) for n, d in PROOFS.items()}
        require(all(p["batch"] == 134 and p["status"] == "PASS"
                    and p["candidate"] == CANDIDATE and p["base"] == BASE
                    and not p["memory"]["breach"] for p in proofs.values()), "Unadmitted proof")
        source, payload, gates = (proofs[n] for n in PROOFS)
        require(payload["sourceProof"]["sha256"] == PROOFS["source-proof-002.json"]
                and gates["payloadProof"]["sha256"] == PROOFS["payload-proof-001.json"],
                "Proof graph mismatch")
        facts = load(source["facts"]["path"], source["facts"]["sha256"])
        by_path = {r["path"]: r for r in source["sourceRecords"]}
        merged, bindings, index = {}, [], {}
        for kind, tag, identity, count in (("jmdict", "entry", "ent_seq", 399),
                                           ("kanjidic2", "character", "literal", 59)):
            records = {}
            for selection in facts[kind + "Selections"]:
                name = selection["file"]
                proof = by_path[PREFIX + name]
                raw = blob(PREFIX + name)
                require(sha(raw) == proof["sha256"]
                        and all(selection[k] == proof[k] for k in ("mode", "queries")),
                        "Selection provenance mismatch")
                original = write_frozen(HERE / "source-contract" / "original" / name, raw)
                originals[name] = original
                tree = ET.fromstring(raw)
                require(all(n.tag == tag for n in tree), "Unexpected dictionary child")
                ids = []
                for node in tree:
                    key = node.findtext(identity)
                    require(key and key not in ids, "Duplicate/missing source identity")
                    require(selects(node, tag, key, selection["mode"], selection["queries"]),
                            "Record does not match original query")
                    ids.append(key)
                    if key in records:
                        require(canonical(ET.tostring(node, encoding="utf-8")) ==
                                canonical(ET.tostring(records[key], encoding="utf-8")),
                                "Conflicting complete duplicate: " + key)
                    else:
                        records[key] = copy.deepcopy(node)
                require(sorted(ids) == sorted(proof["identities"]) and len(ids) == proof["completeMatchingRecords"],
                        "Complete selection membership mismatch")
                bindings.append({**selection, "sha256": sha(raw), "identities": ids,
                                 "completeMatchingRecords": len(ids)})
            require(len(records) == count, "Complete union count mismatch")
            merged[kind] = records
            root = ET.Element("JMdict" if kind == "jmdict" else "kanjidic2")
            root.extend(records[k] for k in sorted(records, key=int if kind == "jmdict" else None))
            full = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
            compact = compact_xml(full)
            require(canonical(full) == canonical(compact), "Lossy complete-record serialization")
            require(max(map(len, compact.splitlines())) < 13900, "Complete record exceeds read budget")
            name = "jmdict-families.xml" if kind == "jmdict" else "kanjidic2-records.xml"
            originals[name] = write_frozen(HERE / "source-contract" / name, compact)
            put("evidence/" + name, compact)
        jm = merged["jmdict"]
        for selection in facts["jmdictSelections"]:
            for q in selection["queries"]:
                index[q] = sorted((k for k, n in jm.items() if selects(n, "entry", k, "union", [q])), key=int)
        require({k for ids in index.values() for k in ids} == set(jm), "Query index omits records")
        put("evidence/dictionary-index.json", json_bytes(index))
        contract = freeze_json(HERE / "source-contract" / "contract.json", {
            "status": "COMPLETE_ORIGINAL_SELECTIONS_VERIFIED_NOT_REVIEWED", "batch": 134,
            "candidate": CANDIDATE, "base": BASE, "proofs": PROOFS,
            "facts": source["facts"], "selections": bindings, "files": originals,
            "counts": {"jmdict": 399, "kanjidic2": 59},
            "presentation": "Complete canonical-equal XML; indentation removed, no semantic projection.",
            "queryCount": len(index), "zeroMatchQueries": [q for q, ids in index.items() if not ids]})
        put("evidence/xml-presentation.json", json_bytes({
            "method": "Complete canonical-equal XML records, one record per line; no fields omitted.",
            "selections": bindings, "counts": {"jmdict": 399, "kanjidic2": 59},
            "sourceContractSha256": contract["sha256"],
            "zeroMatchQueries": [q for q, ids in index.items() if not ids],
            "limits": "Original complete selections retained locally; different serialization line numbers."}))
        manifest_raw = blob("manifest.json")
        require(sha(manifest_raw) == payload["manifestSha256"], "Manifest mismatch")
        manifest = json.loads(manifest_raw)
        names = sorted((n for n in manifest["files"] if n.startswith("kanji/")),
                       key=lambda n: ord(Path(n).stem))
        baseline = git("ls-tree", "-r", "--name-only", BASE, "--", "kanji").decode().splitlines()
        require(len(names) == 1262 and len(baseline) == 1261
                and set(names) - set(baseline) == {f"kanji/{c}.md" for c in MEMBERS}, "Article inventory differs")
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        titles = []
        for start in range(0, len(names), 100):
            batch = names[start:start + 100]
            for name, (_, raw) in zip(batch, git.objects([CANDIDATE + ":" + n for n in batch])):
                put("repo/" + name, raw)
                metadata, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
                titles.append((Path(name).stem, Path(name).stem + " " + metadata["title"]))
            guard.check()
        for start in range(0, len(baseline), 100):
            batch = baseline[start:start + 100]
            for name, (_, raw) in zip(batch, git.objects([BASE + ":" + n for n in batch])):
                require(files["repo/" + name] == raw, "Baseline article differs")
        put("evidence/title-index.txt", ("\n".join(line for _, line in titles) + "\n").encode())
        put("evidence/baseline-title-index.txt",
            ("\n".join(line for c, line in titles if c not in MEMBERS) + "\n").encode())
        require([m["kanji"] for m in payload["members"]] == MEMBERS, "Member order differs")
        for member in payload["members"]:
            c = member["kanji"]
            require(sha(files[f"repo/kanji/{c}.md"]) == member["articleSha256"], "Card changed")
            put(f"snapshot/kanji/{c}.md", files[f"repo/kanji/{c}.md"])
            stroke = blob(f"strokes/{c}.json")
            geometry = next(r for r in payload["generatedGeometry"] if r["kanji"] == c)
            require(sha(stroke) == geometry["strokeSha256"], "Stroke changed")
            put(f"snapshot/strokes/{c}.json", stroke)
        supports = payload["supportLinks"]
        require([r["word"] for r in supports] == ["紫"], "Support inventory mismatch")
        for row in supports:
            before, after = blob(row["path"], BASE), blob(row["path"])
            require(sha(before) == row["beforeSha256"] and sha(after) == row["afterSha256"], "Support changed")
            put("baseline/" + row["path"], before)
            put("snapshot/" + row["path"], after)
        support_names = [r["path"] for r in supports]
        content_names = [f"kanji/{c}.md" for c in MEMBERS] + [f"strokes/{c}.json" for c in MEMBERS] + support_names
        put("diffs/existing.diff", git("diff", "--no-color", BASE, CANDIDATE, "--", *support_names))
        put("diffs/runtime-content.diff", git("diff", "--no-color", BASE, CANDIDATE, "--", *content_names))
        for name in ("docs/content-format.md", "docs/jlpt-levels.md", "manifest.json"):
            put("repo/" + name, manifest_raw if name == "manifest.json" else blob(name))
        for name in (".github/copilot-instructions.md", ".github/instructions/content-structure.instructions.md"):
            put("rubric/" + Path(name).name, blob(name))
        font_raw = blob(PREFIX + "stroke-font-evidence.json")
        require(sha(font_raw) == facts["strokeFontEvidenceSha256"], "Signed font evidence changed")
        put("evidence/font-cmap.json", font_raw)
        font = json.loads(font_raw)
        put("evidence/source-metadata.json", blob(PREFIX + "source-rows.json"))
        shapes = []
        for row in payload["generatedGeometry"]:
            raw = blob(PREFIX + f"kanjivg/{ord(row['kanji']):05x}.svg")
            require(sha(raw) == row["svgSha256"], "SVG changed")
            put(f"evidence/kanjivg/{ord(row['kanji']):05x}.svg", raw)
            shapes.append({**row, "groups": [dict(n.attrib) for n in
                           ET.fromstring(raw).iter("{http://www.w3.org/2000/svg}g")]})
        put("evidence/shape-evidence.json", json_bytes({
            "geometry": shapes, "converterSha256": payload["converterSha256"],
            "kanjivgRevision": font["kanjivgRevision"],
            "limits": "Bounded SVG/converter/cmap evidence only, not rendered fallback/native/device acceptance."}))
        for gate in CHECKS:
            for ext in ("json", "log"):
                binding = gates["capturedInputs"][f"committed/{gate}.{ext}"]
                put(f"checks/{gate}.{ext}", frozen(binding["path"], binding["sha256"]))
            receipt = json.loads(files[f"checks/{gate}.json"])
            require(receipt["gate"] == gate and receipt["exitCode"] == 0
                    and receipt["logSha256"] == sha(files[f"checks/{gate}.log"])
                    and not receipt["memory"]["breach"], "Committed gate mismatch")
        external_raw = blob(PREFIX + "external-capture-bindings.json")
        external = json.loads(external_raw)
        snapshots, captured = [], {}
        for i, item in enumerate(external["captures"], 1):
            name = Path(item["localRawCapture"]).name
            raw = frozen(item["localRawCapture"], item["rawSha256"])
            text_raw = frozen(Path(item["localRawCapture"]).with_suffix(".txt"), item["textSha256"])
            require(sha(raw) == item["rawSha256"] and len(raw) == item["rawBytes"]
                    and sha(text_raw) == item["textSha256"], "Reused capture binding differs")
            text, error = extract(raw, item["finalUrl"], [item["character"]])
            require(error is None and text, "Complete capture extraction failed: " + str(error))
            value = text.encode("utf-8")
            require(max(map(len, value.splitlines())) < 13900, "External line exceeds chain budget")
            put(f"{SNAP}/{i:02d}-response.html", raw)
            put(f"{SNAP}/{i:02d}-extract.txt", value)
            captured[Path(item["localRawCapture"]).name] = {
                "rawSha256": sha(raw), "originalTextSha256": sha(text_raw), "extractSha256": sha(value)}
            snapshots.append({**{k: item[k] for k in ("character", "provider", "url", "finalUrl", "capturedAt")},
                              "index": i, "status": "SUPPLIED_REUSED_B132_SURVEY_NOT_NEW_FETCH",
                              "originalTextSha256": item["textSha256"],
                              "response": {"path": f"{SNAP}/{i:02d}-response.html", "sha256": sha(raw)},
                              "extract": {"path": f"{SNAP}/{i:02d}-extract.txt", "sha256": sha(value),
                                          "bytes": len(value)}})
        require(len(snapshots) == 2, "Capture count differs")
        put(f"{SNAP}/manifest.json", json_bytes({
            "candidate": CANDIDATE, "signedBindingsSha256": sha(external_raw), "extractionMethod": METHOD,
            "snapshots": snapshots, "reuse": "Two existing complete B132 survey captures; no new retrieval.",
            "limits": "Raw HTML retained locally. Images/layout not inspected; missing glyphs not reconstructed."}))
        joyo_raw = (WS / "scratch-111" / "joyo-pages.json").read_bytes()
        require(sha(joyo_raw) == "cc740aed34751e40831e4ab526408401667a428cefcf0fdd0212848eb31d67cb", "Joyo cache differs")
        pages = json.loads(joyo_raw)
        put("evidence/joyo-rows.json", json_bytes({
            "cacheSha256": sha(joyo_raw), "rows": [{"kanji": c, "matches": [
                {"printedPage": int(page), "completeCachedPage": text} for page, text in pages.items()
                if re.search(r"(?m)^" + re.escape(c) + r"(?:[ \t\uff08(]|$)", text)]} for c in MEMBERS],
            "limits": "Complete cached pages, not fresh visual inspection of PDF glyphs."}))
        snapshot = json.loads(blob("docs/n1-source-snapshot.json"))
        put("evidence/provenance.json", json_bytes({
            "candidate": CANDIDATE, "base": BASE, "sourceInputs": snapshot["inputs"],
            "dictionaryAttribution": snapshot["dictionaryAttribution"],
            "kanjivgAttribution": snapshot["kanjivgAttribution"], "proofs": PROOFS,
            "limits": "Source/payload/gate proofs passed. Separate coordinator finite-packet proof is still required at reviewer admission; no teaching acceptance."}))
        put("evidence/reading-keys.json", blob(PREFIX + "reading-keys.json"))
        companion = gates["capturedInputs"]["full-runtime/summary.json"]
        put("checks/full-runtime-summary.json", frozen(companion["path"], companion["sha256"]))
        put("evidence/source-selection-provenance.json", json_bytes({
            "selections": bindings, "queryCount": len(index),
            "zeroMatchQueries": [q for q, ids in index.items() if not ids],
            "factsSha256": sha(frozen(source["facts"]["path"], source["facts"]["sha256"])),
            "reStreamedProofSha256": PROOFS["source-proof-002.json"]}))
        full = files["evidence/title-index.txt"]
        baseline_bytes = files["evidence/baseline-title-index.txt"]
        removed = [line for line in full.splitlines(keepends=True)
                   if line.decode().split(" ", 1)[0] in MEMBERS]
        rebuilt = b"".join(line for line in full.splitlines(keepends=True) if line not in removed)
        require(rebuilt == baseline_bytes and len(removed) == 1, "Baseline delta differs")
        put("evidence/baseline-title-delta.json", json_bytes({
            "representation": "Complete candidate index plus exact one-new-card deletion delta.",
            "candidateSource": "evidence/title-index.txt", "candidateSha256": sha(full),
            "candidateLines": 1262, "removedCompleteLinesUtf8": [x.decode() for x in removed],
            "operation": "Delete precisely this complete byte-equal line; preserve every other byte and order.",
            "reconstructedBaselineSha256": sha(rebuilt), "baselineLines": 1261,
            "baselineFirstLine": rebuilt.decode().splitlines()[0],
            "baselineLastLine": rebuilt.decode().splitlines()[-1],
            "originalBaseline": "evidence/baseline-title-index.txt",
            "originalBaselinePreservedOutsideChain": True,
            "exactByteReconstructionVerified": True}))
        reference = {"newCards": MEMBERS, "otherRequiredCards": [], "cards": [
            {"card": m["kanji"], "source": f"snapshot/kanji/{m['kanji']}.md", "sha256": m["articleSha256"],
             "distractors": m["metadata"]["distractors"], "quiz_exclusions": m["metadata"]["quiz_exclusions"]}
            for m in payload["members"]]}
        put("eligibility-reference.json", json_bytes(reference))
        put("packet.json", json_bytes({
            "batch": 134, "candidate": CANDIDATE, "base": BASE, "newKanji": MEMBERS,
            "newWords": [], "modifiedExisting": support_names, "supportingUnchanged": [], "wordProseChanges": [],
            "sourceRows": [831], "baselineKanjiArticles": 1261, "candidateKanjiArticles": 1262,
            "completeDictionaryEntries": 399, "completeKanjidicRecords": 59,
            "manifestSha256": payload["manifestSha256"], "contentVersion": payload["contentVersion"],
            "baselineRuntimeEntries": 8745, "candidateRuntimeEntries": 8747,
            "unchangedRuntimeEntries": 7888, "externalCaptures": 2,
            "publishedProgress": "271/1228, 957 remaining; one local draft is not delivery",
            "blinding": "No author source analysis, pair dispositions/reasons, scan matches or earlier review material."}))
        put("REVIEW.md", b"# B134 neutral evidence packet\n\nReview only one new card (purple; violet), its complete stroke JSON, the complete\nbefore/after existing support article and the exact scoped diff. The support has\none substantive reciprocal wrapper, unchanged identity and no prose exception.\nThe run-specific protocol controls access and independent selection.\nAssess correctness, scoped coverage, consistency/quiz safety and comprehensibility.\nCLEAN means bounded absence of an established defect, not exhaustive correctness.\nNo finding quota. Titles alone do not settle ambiguity; consider ordinary secondary\nsenses, restrictions, names, spelling and register. Exclusions are direct symmetric\npairs, not transitive. Distinguish character/word meanings and metadata/quiz readings.\n\nAll 399 complete JMdict families and all 59 complete KANJIDIC2 records are present.\nFour original selections, all 182 JMdict query predicates and zero-result predicates\nare preserved. Complete records are deduplicated only on canonical equality.\nBoth full code-point-ordered title indices are preserved: baseline 1261, candidate\n1262. The complete candidate index plus exact one-line deletion delta represents\nthe full unchanged baseline; disclose that representation, not a raw-baseline read.\nAll 1262 actual candidate articles are available for independent D/E requests.\nNo author analysis, pair reasons/dispositions, scan matches or earlier reviews\nare reviewer inputs. Candidate teaching and frontmatter are byte-unaltered.\nTen committed gate logs/receipts and the full-runtime companion are supplied.\n\nThe two complete Kotobank/Weblio extracts reuse B132 survey captures with their\nactual URLs, retrieval dates and raw/text hashes; no new fetch is claimed.\nEvery named Weblio section and the complete Kotobank body are retained, including\npositive secondary senses, historical readings and missing-glyph-image disclosures.\nRaw HTML and original XML remain local; missing historical images are unavailable.\n\nAuthor-gates-001 passed with 38 quiz-safety 'not mentioned in Notes' warnings and\nis superseded. Author-gates-002 and committed-gates-001 have zero such warnings.\nEleven pre-existing fallback cards remain noted. Reading model: zero production\nand zero padded-session hits; one latent smaller-pool collision on a historical\nreading is not drawable in checked pools and its historical scope is unresolved.\nAll three bundled cmaps contain the target and components; search-only variant\nU+8308 is absent in all three. Bounded cmap evidence is not rendered fallback\nacceptance. Jitsu gives 11 strokes; pinned KANJIDIC2 and KanjiVG give 12; the\ndiscrepancy is retained. The mnemonic is invented and non-etymological.\nDefault git diff --check flags CRLF; CR-at-EOL-aware check passed. The committed\nbyte and reading producers read local scratch-134 inputs; coordinator rechecked\nthem. No arbitrary/custom/multiple-borrow pool, Kotlin/native/device, rendering,\nwhole-set, linguistic or publication acceptance is claimed by this preparation.\nPublished progress remains 271/1228, 957 remaining. A local draft is not delivery.\n")
        clean(git)
        sums = {}
        for name, raw in sorted(files.items()):
            sums[name] = write_frozen(PACKET / name, raw)["sha256"]
            guard.check()
        sum_binding = freeze_json(PACKET / "SHA256SUMS.json", sums)
        freeze_json(HERE / "packet-build.json", {
            "status": "COMPLETE_NEUTRAL_INPUTS_NOT_REVIEW_ADMISSION", "batch": 134,
            "candidate": CANDIDATE, "base": BASE, "packetManifest": sum_binding,
            "sourceContract": contract, "files": len(files), "captured": captured,
            "coreSources": core_names(payload, reference),
            "actualCoordinatorPacketProof": {"path": str(ROOT / "packet-verification-001" / "verification.json"),
                "status": "REQUIRED_SEPARATELY_BEFORE_ADMISSION"}})
        print(json.dumps({"files": len(files), "sums": sum_binding, "sourceContract": contract}))
    finally:
        require(not guard.finish()["breach"], "Packet construction RAM breach")


if __name__ == "__main__":
    packet()
