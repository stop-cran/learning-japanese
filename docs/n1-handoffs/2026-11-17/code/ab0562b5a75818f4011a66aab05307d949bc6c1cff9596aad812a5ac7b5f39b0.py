"""Derive neutral packet construction, preserving the accepted predecessor."""
import json
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
HERE = ROOT / "neutral-preparation-001"
sys.path.insert(0, str(WS / "review-tools"))
from common import frozen, require, sha, write_frozen, freeze_json

SOURCE = WS / "scratch-133" / "review" / "neutral-preparation-001" / "tools" / "prepare-b133-neutral-001.py"
raw = frozen(SOURCE)
text = raw.decode().replace("\r\n", "\n")
text = text[:text.index("\n\nDERIVATIONS = []")]
rules = [
    ("scratch-133", "scratch-134"), ("b133", "b134"), ("B133", "B134"),
    ('HERE = ROOT / "neutral-preparation-001"', 'HERE = ROOT / "neutral-preparation-001" / "complete-record-trial"'),
    ("6858fcfb069cc56a195c3f6ed938f92f657fe96b", "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"),
    ("ad047ace020579f81bde250ac948b9a4cb597887", "ba80afffc20a72d31be68b355b6f90aab36a5726"),
    ('MEMBERS = ["琴", "鉛", "滝"]', 'MEMBERS = ["紫"]'),
    ("03260517d250b9d8071e2e70ec76fdb3ffda906d4f947e4a049375ebb249e5eb",
     "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"),
    ('"source-verification-001.json"', '"source-proof-002.json"'),
    ("5d8c9aee7a31a35e5eeae047d35ff3a79aedb4ecc81cb7f72358d9515974cd12",
     "f3a80ee569a1bfd4f452e3f413a6377f5d01cac665e978dfc3e6db722c809393"),
    ('"payload-verification-001.json"', '"payload-proof-001.json"'),
    ("692ecc9d3af90157b97733ff29c2b11ebe4d271893308a2c6eb2cf4e9b61c2cb",
     "ec47228ee313a82d872e7235f6f4a6b048737f24254d26405418c840dbd65d1a"),
    ('"gate-verification-001/verification.json"', '"gate-verification-002/verification.json"'),
    ("65e292b34893b15862d70f37a9dfdb94bc22972bbc70044bc6431716349181fb",
     "1caed56d80a213605d59eac6cc7ecc69829083cbdaa606b684edd77fb9162694"),
    ('    "packet-verification-001/verification.json": "9ecbdbb9d2c0f90c1de9c1a4088a78655bb531f715e74ae07002ad797dcf9ebd",\n', ""),
    ('p["batch"] == 133', 'p["batch"] == 134'),
    ('"batch": 133', '"batch": 134'),
    ('source, payload, gates, evidence = (proofs[n] for n in PROOFS)',
     'source, payload, gates = (proofs[n] for n in PROOFS)'),
    ('        require(evidence["proofs"] == {k: v for k, v in PROOFS.items()\n'
     '                                       if k != "packet-verification-001/verification.json"},\n'
     '                "Actual coordinator packet proof graph mismatch")\n', ""),
    ('("jmdict", "entry", "ent_seq", 515)', '("jmdict", "entry", "ent_seq", 399)'),
    ('("kanjidic2", "character", "literal", 83)', '("kanjidic2", "character", "literal", 59)'),
    ('require(ids == proof["identities"] and len(ids) == proof["completeMatchingRecords"],',
     'require(sorted(ids) == sorted(proof["identities"]) and len(ids) == proof["completeMatchingRecords"],'),
    ('{"jmdict": 515, "kanjidic2": 83}', '{"jmdict": 399, "kanjidic2": 59}'),
    ('len(names) == 1261 and len(baseline) == 1258', 'len(names) == 1262 and len(baseline) == 1261'),
    ('== ["琴", "鉛筆", "滝"]', '== ["紫"]'),
    ('        require(sha(font_raw) == evidence["signedInputs"][PREFIX + "stroke-font-evidence.json"],\n'
     '                "Actual verified font evidence changed")\n',
     '        require(sha(font_raw) == facts["strokeFontEvidenceSha256"], "Signed font evidence changed")\n'),
    ('            binding = evidence["capturedInputs"]["external/" + name]\n'
     '            text_binding = evidence["capturedInputs"]["external/" + Path(name).with_suffix(".txt").name]\n'
     '            raw = frozen(binding["path"], binding["sha256"])\n'
     '            text_raw = frozen(text_binding["path"], text_binding["sha256"])\n',
     '            raw = frozen(item["localRawCapture"], item["rawSha256"])\n'
     '            text_raw = frozen(Path(item["localRawCapture"]).with_suffix(".txt"), item["textSha256"])\n'),
    ('require(len(snapshots) == 6', 'require(len(snapshots) == 2'),
    ('Six existing complete B132 survey captures', 'Two existing complete B132 survey captures'),
    ('"limits": "Actual source/payload/gate/finite packet proofs passed; mechanical evidence, not teaching acceptance."',
     '"limits": "Source/payload/gate proofs passed. Separate coordinator finite-packet proof is still required at reviewer admission; no teaching acceptance."'),
    ('"sourceRows": [707, 1120, 643], "baselineKanjiArticles": 1258, "candidateKanjiArticles": 1261',
     '"sourceRows": [831], "baselineKanjiArticles": 1261, "candidateKanjiArticles": 1262'),
    ('"completeDictionaryEntries": 515, "completeKanjidicRecords": 83',
     '"completeDictionaryEntries": 399, "completeKanjidicRecords": 59'),
    ('"baselineRuntimeEntries": 8739, "candidateRuntimeEntries": 8745',
     '"baselineRuntimeEntries": 8745, "candidateRuntimeEntries": 8747'),
    ('"unchangedRuntimeEntries": 8736, "externalCaptures": 6',
     '"unchangedRuntimeEntries": 7888, "externalCaptures": 2'),
    ('268/1228, 960 remaining; three local drafts are not delivery',
     '271/1228, 957 remaining; one local draft is not delivery'),
    ('            "actualCoordinatorPacketProof": {\n'
     '                "path": str(ROOT / "packet-verification-001" / "verification.json"),\n'
     '                "sha256": PROOFS["packet-verification-001/verification.json"]}',
     '            "actualCoordinatorPacketProof": {"path": str(ROOT / "packet-verification-001" / "verification.json"),\n'
     '                "status": "REQUIRED_SEPARATELY_BEFORE_ADMISSION"}'),
    ('range(1, 7)', 'range(1, 3)'),
]
for before, after in rules:
    require(before in text, "Missing derivation anchor: " + before[:160])
    text = text.replace(before, after)
start = text.index('        put("REVIEW.md", b"""')
end = text.index('        clean(git)', start)
review = """# B134 neutral evidence packet

Review only one new card (purple; violet), its complete stroke JSON, the complete
before/after existing support article and the exact scoped diff. The support has
one substantive reciprocal wrapper, unchanged identity and no prose exception.
The run-specific protocol controls access and independent selection.
Assess correctness, scoped coverage, consistency/quiz safety and comprehensibility.
CLEAN means bounded absence of an established defect, not exhaustive correctness.
No finding quota. Titles alone do not settle ambiguity; consider ordinary secondary
senses, restrictions, names, spelling and register. Exclusions are direct symmetric
pairs, not transitive. Distinguish character/word meanings and metadata/quiz readings.

All 399 complete JMdict families and all 59 complete KANJIDIC2 records are present.
Four original selections, all 182 JMdict query predicates and zero-result predicates
are preserved. Complete records are deduplicated only on canonical equality.
Both full code-point-ordered title indices are preserved: baseline 1261, candidate
1262. The complete candidate index plus exact one-line deletion delta represents
the full unchanged baseline; disclose that representation, not a raw-baseline read.
All 1262 actual candidate articles are available for independent D/E requests.
No author analysis, pair reasons/dispositions, scan matches or earlier reviews
are reviewer inputs. Candidate teaching and frontmatter are byte-unaltered.
Ten committed gate logs/receipts and the full-runtime companion are supplied.

The two complete Kotobank/Weblio extracts reuse B132 survey captures with their
actual URLs, retrieval dates and raw/text hashes; no new fetch is claimed.
Every named Weblio section and the complete Kotobank body are retained, including
positive secondary senses, historical readings and missing-glyph-image disclosures.
Raw HTML and original XML remain local; missing historical images are unavailable.

Author-gates-001 passed with 38 quiz-safety 'not mentioned in Notes' warnings and
is superseded. Author-gates-002 and committed-gates-001 have zero such warnings.
Eleven pre-existing fallback cards remain noted. Reading model: zero production
and zero padded-session hits; one latent smaller-pool collision on a historical
reading is not drawable in checked pools and its historical scope is unresolved.
All three bundled cmaps contain the target and components; search-only variant
U+8308 is absent in all three. Bounded cmap evidence is not rendered fallback
acceptance. Jitsu gives 11 strokes; pinned KANJIDIC2 and KanjiVG give 12; the
discrepancy is retained. The mnemonic is invented and non-etymological.
Default git diff --check flags CRLF; CR-at-EOL-aware check passed. The committed
byte and reading producers read local scratch-134 inputs; coordinator rechecked
them. No arbitrary/custom/multiple-borrow pool, Kotlin/native/device, rendering,
whole-set, linguistic or publication acceptance is claimed by this preparation.
Published progress remains 271/1228, 957 remaining. A local draft is not delivery.
"""
text = text[:start] + '        put("REVIEW.md", ' + repr(review.encode()) + ')\n' + text[end:]
anchor = '        reference = {"newCards": MEMBERS'
pos = text.index(anchor)
addition = '''        put("evidence/reading-keys.json", blob(PREFIX + "reading-keys.json"))
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
'''
text = text[:pos] + addition + text[pos:]
text = text.replace('"evidence/source-metadata.json", "evidence/xml-presentation.json"',
                    '"evidence/reading-keys.json", "checks/full-runtime-summary.json",\n'
                    '              "evidence/source-selection-provenance.json",\n'
                    '              "evidence/source-metadata.json", "evidence/xml-presentation.json"')
text = text.replace('"evidence/baseline-title-index.txt", "evidence/title-index.txt"',
                    '"evidence/baseline-title-delta.json", "evidence/title-index.txt"')
text += '\n\nif __name__ == "__main__":\n    packet()\n'
output = write_frozen(HERE / "tools" / "packet-builder-b134-001.py", text.encode())
freeze_json(HERE / "packet-builder-derivation-001.json", {
    "source": {"path": str(SOURCE), "sha256": sha(raw)}, "output": output,
    "rules": rules, "manualReplacements": [
        "B134-only neutral disclosure replaces B133 teaching-specific disclosure",
        "Add complete query provenance, reading keys, runtime summary and exact baseline index delta",
        "Finite coordinator packet proof deferred to admission, never synthesized here"]})
print(json.dumps(output))
