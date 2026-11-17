"""Bind finite reconciliation claims to complete records and captured evidence."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, frozen, require, sha
from verify_b129_revision_runtime import PARENT, PREFIX, REVIEW, allowed_pairs

ORIGINAL = "docs/n1-sources/batch-129/"
JM_FILES = [ORIGINAL + name for name in (
    "jmdict-complete-families.xml", "jmdict-supplemental-comparisons-002.xml",
    "jmdict-final-comparisons.xml", "jmdict-additional-families.xml",
)] + [PREFIX + name for name in (
    "jmdict-complete-records.xml", "jmdict-supplement-complete-records.xml",
    "jmdict-noose-complete-records.xml",
)]
EXTERNAL_SHA = "6d563b35bc4c1657e4748166f2d2a2a58d9e63f13106d53ee7b73803d74216fd"
NOOSE_EXTERNAL_SHA = "9bc69d0bb67a20ae758511495e950e97dcd134d71af971dc9b07db0c6ba4af15"
NOOSE_PROOF_SHA = "f4f3eea2a8718a371348000a49e0c658de704316911eb5aa22e6709ebf8420d2"
NOOSE = "\u7f82\u7d22"


def compact(text):
    return re.sub(r"\s+", "", text)


def check_table(table, expected, metadata):
    rows = table["rows"]
    actual = [tuple(row["pair"]) for row in rows]
    require(len(actual) == len(set(actual)) == len(expected) and set(actual) == set(expected)
            and table["parent"] == PARENT and table["totalPairs"] == len(expected),
            "Finite comparison membership differs")
    require(all(type(row["guard"]) is bool for row in rows)
            and table["newDirectGuards"] == sum(row["guard"] for row in rows)
            and table["supportedNoncollisionPairs"] ==
            [row["pair"] for row in rows if not row["guard"]], "Disposition totals differ")
    for row in rows:
        target, other = row["pair"]
        require(row["claim"] == expected[(target, other)]
                and all(isinstance(row[key], str) and row[key].strip() for key in
                        ("strongestSecondary", "targetLabelOnComparison",
                         "comparisonLabelOnTarget", "disposition")),
                "Missing bidirectional disposition or wrong claim")
        require(row["guardDeclaration"] ==
                (f"kanji/{target}.md:quiz_exclusions" if row["guard"] else None)
                and (other in metadata[target]["quiz_exclusions"]) is row["guard"]
                and other not in metadata[target]["distractors"],
                "Declared guard does not match actual card")
    return rows


def external_evidence(blob, guard):
    original = json.loads(frozen(REVIEW / "reconciliation-external-001" / "manifest.json", EXTERNAL_SHA))
    extra = json.loads(frozen(REVIEW / "reconciliation-noose-external-001" / "manifest.json",
                              NOOSE_EXTERNAL_SHA))
    captures = [*original["captures"], extra]
    require(len(captures) == len({row["character"] for row in captures}) == 29,
            "External capture coverage differs")
    signed = json.loads(blob(PREFIX + "external-source-bindings.json"))
    declarations = signed["comparisonsAndExactFollowupNoun"]
    require(set(declarations) == {row["character"] for row in captures}, "Unbound external capture")
    result = {}
    for capture in captures:
        outputs = {name: frozen(binding["path"], binding["sha256"])
                   for name, binding in capture["outputs"].items()}
        character = capture["character"]
        receipt = json.loads(outputs["receipt.json"])
        require(receipt == declarations[character]
                and sha(outputs["raw.html"]) == receipt["rawSha256"]
                and len(outputs["raw.html"]) == receipt["rawBytes"]
                and sha(outputs["articles.json"]) == receipt["allArticleJsonSha256"]
                and sha(outputs["author-selected.txt"]) ==
                receipt["selectedCompleteArticleTextSha256"],
                f"Signed external source differs: {character}")
        result[character] = {"receipt": receipt, "outputs": outputs, "capture": capture}
        guard.check()
    require({item["character"] for item in signed["targets"]} == set("\u7d79\u8679"),
            "Target capture inventory differs")
    for item in signed["targets"]:
        frozen(item["path"], item["sha256"])
    require(signed["originalPacketInventory"]["path"] == ORIGINAL + "evidence-inventory-003.json"
            and sha(blob(signed["originalPacketInventory"]["path"])) ==
            signed["originalPacketInventory"]["sha256"], "Original inventory binding differs")
    return result


def verify_noose(blob):
    proof = json.loads(frozen(REVIEW / "revision-noose-source-observation-proof-001.json", NOOSE_PROOF_SHA))
    receipt_raw = blob(PREFIX + "noose-source-receipt.json")
    raw = blob(PREFIX + "jmdict-noose-complete-records.xml")
    require(proof["status"] == "PASS_OBSERVED_SOURCES_ONLY" and proof["candidate"] is None
            and not proof["memory"]["breach"] and sha(receipt_raw) == proof["receiptSha256"]
            and sha(raw) == proof["outputSha256"] and not ET.fromstring(raw).findall("entry"),
            "Separate zero-match proof does not bind final source")
    require(proof["results"] == [{
        "identities": [], "queries": {"exact-spelling:" + NOOSE: []},
        "zeroMatches": ["exact-spelling:" + NOOSE], "outputSha256": sha(raw),
    }], "Separate zero-match predicate differs")
    return {"proofSha256": NOOSE_PROOF_SHA, "receiptSha256": sha(receipt_raw),
            "outputSha256": sha(raw), "limits": "Zero exact-spelling matches, not a denial of senses."}


def verify(blob, adjudication, metadata, guard):
    sys.path.insert(0, str(WS / "lean"))
    from n1lib import parse
    expected = {tuple(pair): "F1" for pair in adjudication["findingAdjudication"]["F1"]["pairs"]}
    for item in adjudication["consequentialClaims"]:
        expected.update({tuple(pair): item["id"] for pair in item.get(
            "pairs", [[item.get("target"), other] for other in item.get("comparisons", [])])})
    allowed = allowed_pairs(adjudication)
    require(set(expected) == {(target, other) for target, others in allowed.items() for other in others},
            "Adjudication scope differs")
    table_raw = blob(PREFIX + "pair-dispositions.json")
    rows = check_table(json.loads(table_raw), expected, metadata)
    captures = external_evidence(blob, guard)
    noose = verify_noose(blob)
    families = {}
    for path in JM_FILES:
        identities = set()
        for node in ET.fromstring(blob(path)).findall("entry"):
            identity = node.findtext("ent_seq")
            require(identity and identity not in identities, f"Duplicate source family: {path}")
            identities.add(identity)
            digest = sha(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode())
            if identity not in families:
                families[identity] = {"canonicalSha256": digest, "completeRecordFiles": []}
            require(families[identity]["canonicalSha256"] == digest, "Conflicting complete family")
            families[identity]["completeRecordFiles"].append(path)
        guard.check()
    kd = {}
    for node in ET.fromstring(blob(PREFIX + "kanjidic2-complete-records.xml")).findall("character"):
        character = node.findtext("literal")
        require(character and character not in kd, "Duplicate character source")
        kd[character] = [m.text for m in node.findall("reading_meaning/rmgroup/meaning")
                         if m.get("m_lang") in (None, "en")]
    comparisons = json.loads(blob(PREFIX + "comparison-bindings.json"))
    require(len(comparisons) == len(rows) and len({tuple(c["pair"]) for c in comparisons}) == len(rows),
            "Comparison bindings differ")
    comparison_map = {tuple(c["pair"]): c for c in comparisons}
    for row in rows:
        target, other = row["pair"]
        binding = comparison_map[(target, other)]
        raw = blob(PREFIX + f"comparison-cards/{other}.md")
        require(raw == blob(f"kanji/{other}.md") and sha(raw) == binding["rawSha256"]
                and binding["path"] == f"kanji/{other}.md" and row["comparison"] == binding,
                f"Comparison bytes differ: {other}")
        card, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
        require(card["title"] == binding["title"]
                and row["comparisonEnglishMeaningsCompleteKANJIDIC2"] == kd[other],
                f"Comparison title/complete meanings differ: {other}")
        require(row["completeJmdictFamilies"] and all(families.get(identity) == record
                for identity, record in row["completeJmdictFamilies"].items()),
                f"Claim family binding differs: {target}/{other}")
        evidence, capture = row["sourceEvidence"], captures[other]
        articles = [a for a in json.loads(capture["outputs"]["articles.json"])
                    if a["class"] == evidence["articleClass"] and a["id"] == evidence["articleId"]]
        require(len(articles) == 1, f"Ambiguous source article: {other}")
        quote, article = compact(evidence["boundedExcerpt"]), compact(articles[0]["text"])
        require(quote and quote in article and article.index(quote) ==
                evidence["whitespaceNormalizedExcerptStart"] and quote in
                compact(capture["outputs"]["complete-extract.txt"].decode("utf-8"))
                and evidence["url"] == capture["receipt"]["url"]
                and evidence["rawCaptureSha256"] == capture["receipt"]["rawSha256"]
                and evidence["completeSelectedTextSha256"] ==
                capture["receipt"]["selectedCompleteArticleTextSha256"],
                f"Source excerpt binding differs: {other}")
        guard.check()
    return {
        "pairCount": len(rows), "addedGuards": {target: [
            row["pair"][1] for row in rows if row["pair"][0] == target and row["guard"]
        ] for target in allowed},
        "noncollisionPairs": [row["pair"] for row in rows if not row["guard"]],
        "pairTableSha256": sha(table_raw), "completeFamilyUnionCount": len(families),
        "completeCharacterCount": len(kd), "externalCaptureCount": len(captures),
        "externalManifestSha256": EXTERNAL_SHA, "additionalExternalManifestSha256": NOOSE_EXTERNAL_SHA,
        "nooseSource": noose, "semanticAcceptance": False,
        "limits": "Exact source/claim/card bindings only. Author coverage and semantic conclusions "
                  "remain hypotheses for independent reviewers. Complete original XML selections "
                  "must also be bound to the signed source proof, not accepted from hashes alone.",
    }
