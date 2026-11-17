"""Check finite B130 source/card/claim bindings, never their semantic acceptance."""
import json
import re
import sys
from pathlib import Path

from common import WS, frozen, require, sha
from verify_b130_revision_runtime_v2 import (BASE, GPT_OPEN, INITIAL_SHA, MEMBERS, PARENT,
                                           ROOT, check_initial)

FINDINGS = {
    "claude": {"F1": ["\u8017/\u64e6", "\u8017/\u6469"], "F2": ["\u8017/\u524a"]},
    "gpt": {"F1": ["\u8017/\u4fbf"], "F2": ["\u8017/\u64e6"],
            "F3": ["\u8017/\u524a"], "F4": ["\u62cd/\u7a81"]},
}
DECISIONS = ("guard", "precaution", "bounded-noncollision")
TEXT_FIELDS = ("positiveSourceBasis", "comparisonLabelOnTarget",
               "targetLabelOnComparison", "qualification")


def load_initials():
    result = {}
    for family, digest in INITIAL_SHA.items():
        path = ROOT / f"N1-B130-{family.upper()}-004-acceptance.json"
        accepted = json.loads(frozen(path, digest))
        adjudication = json.loads(frozen(accepted["adjudication"]["path"],
                                       accepted["adjudication"]["sha256"]))
        final = json.loads(frozen(accepted["final"]["path"], accepted["final"]["sha256"]))
        frozen(accepted["report"]["path"], accepted["report"]["sha256"])
        check_initial(family, accepted, adjudication, final)
        require(accepted["acceptedFindings"] == list(FINDINGS[family]),
                "Accepted finding inventory differs")
        result[family] = {
            "accepted": accepted, "adjudication": adjudication,
            "bindings": [accepted["report"], accepted["adjudication"],
                         {"path": str(path), "sha256": digest}],
        }
    return result


def expected_pairs(initials):
    pairs = {tuple(pair.split("/")) for findings in FINDINGS.values()
             for names in findings.values() for pair in names}
    for question in initials["gpt"]["adjudication"]["unresolvedComparisons"]:
        require(len(question["relatedNewCards"]) == 1, "Ambiguous original comparison")
        pairs.add((next(iter(question["relatedNewCards"])), question["card"]))
    require(len(pairs) == 28 and all(target in MEMBERS and len(other) == 1 for target, other in pairs),
            "Unexpected finite reconciliation scope")
    return pairs


def check_table(table, expected, metadata, comparisons, receipt, membership):
    rows = table["rows"]
    actual = [tuple(row["pair"]) for row in rows]
    require(table["parent"] == PARENT and table["publishedBase"] == BASE
            and len(actual) == len(set(actual)) == len(expected) and set(actual) == expected,
            "Finite pair inventory differs")
    require(table["counts"] == {value: sum(row["decision"] == value for row in rows)
                                for value in DECISIONS},
            "Pair decision counts differ")
    required = {pair for findings in FINDINGS.values() for names in findings.values() for pair in names}
    family_hashes = receipt["outputs"]["jmdict-families.xml"]["canonicalRecordHashes"]
    character_hashes = receipt["outputs"]["kanjidic2-records.xml"]["canonicalRecordHashes"]
    for row in rows:
        target, other = row["pair"]
        require(row["decision"] in DECISIONS
                and all(isinstance(row[field], str) and row[field].strip() for field in TEXT_FIELDS)
                and type(row["openQuizHold"]) is bool
                and type(row["directExclusionOnNewEndpoint"]) is bool,
                "Missing bidirectional rationale, decision or hold")
        guarded = other in metadata[target]["quiz_exclusions"]
        require(row["targetDisplayedTitle"] == metadata[target]["title"]
                and row["comparisonDisplayedTitle"] == comparisons[other]["title"]
                and row["directExclusionOnNewEndpoint"] is guarded
                and guarded == (row["decision"] in ("guard", "precaution"))
                and other not in metadata[target]["distractors"],
                "Displayed titles or direct guard differ from actual cards")
        if "/".join(row["pair"]) in required:
            require(guarded, "An accepted required direct pair is missing")
        if not guarded:
            require(target not in comparisons[other].get("quiz_exclusions", []),
                    "Bounded noncollision is actually declared at the other endpoint")
        require(row["completeComparisonCard"] == receipt["comparisonCards"][other],
                "Comparison source binding differs")
        queries = row["exactQueries"]
        require(isinstance(queries, list) and queries and len(queries) == len(set(queries))
                and set(queries) <= set(receipt["selectors"]["exactSpellings"]),
                "Unknown or duplicate pair source query")
        query_names = {"exact-spelling:" + query for query in queries}
        expected_families = {identity: family_hashes[identity]
                             for identity, predicates in membership.items()
                             if query_names.intersection(predicates)}
        require(expected_families and row["completeFamilyCanonicalHashes"] == expected_families
                and row["completeCharacterRecords"] == {char: character_hashes[char]
                                                        for char in row["pair"]},
                "Pair source family/character inventory is incomplete")
    require(table["openQuizHolds"] == [row["pair"] for row in rows if row["openQuizHold"]],
            "Open pair holds were lost")
    require(isinstance(table["remainingLexicalUncertainty"], str)
            and table["remainingLexicalUncertainty"].strip(), "Lexical uncertainty was omitted")
    return {"/".join(row["pair"]): row for row in rows}


def check_mapping(family, mapping, initial, rows, table_sha):
    accepted, adjudication = initial["accepted"], initial["adjudication"]
    require(mapping["run"] == accepted["run"] and mapping["parent"] == PARENT
            and mapping["originalBindings"] == initial["bindings"]
            and mapping["originalOpenClaimIds"] == adjudication["openClaimIds"]
            and mapping["independentConfirmation"] is False
            and mapping["publicationAccepted"] is False,
            "Response changed its independent initial or acceptance boundary")
    require(set(mapping["findings"]) == set(FINDINGS[family]),
            "A required finding response is missing")
    for identifier, pairs in FINDINGS[family].items():
        finding = mapping["findings"][identifier]
        require(finding["authorStatus"] == "addressed-awaiting-independent-confirmation"
                and finding["neutralPairs"] == pairs and finding["neutralTableSha256"] == table_sha
                and all(rows[pair]["directExclusionOnNewEndpoint"] for pair in pairs),
                "Required finding is not bound to its actual direct guard")
    questions = adjudication.get("unresolvedComparisons", []) if family == "gpt" else []
    dispositions = mapping["comparisonDispositions"]
    require([row["id"] for row in dispositions] == [row["id"] for row in questions]
            == (GPT_OPEN if family == "gpt" else []),
            "Open comparison IDs were omitted, duplicated or reordered")
    for question, disposition in zip(questions, dispositions):
        pair = [next(iter(question["relatedNewCards"])), question["card"]]
        key = "/".join(pair)
        row = rows[key]
        require(disposition["initialQuestion"] == question and disposition["pair"] == pair
                and disposition["neutralRow"] == key and disposition["neutralTableSha256"] == table_sha
                and disposition["authorDisposition"] == row["decision"]
                and disposition["openQuizHold"] is row["openQuizHold"]
                and disposition["independentConfirmation"] == "not performed",
                "A historical question was changed or linked to another pair")
    require(set(mapping["optionalPoints"]) == {f"O{i}" for i in range(1, 6 if family == "claude" else 2)}
            and set(mapping["limits"]) == {f"L{i}" for i in range(1, 8 if family == "claude" else 11)}
            and all(isinstance(text, str) and text.strip()
                    for entries in (mapping["optionalPoints"], mapping["limits"])
                    for text in entries.values()), "Optional points or declared limits were lost")


def verify(source, card_source):
    sys.path.insert(0, str(WS / "lean"))
    from n1lib import parse

    initials = load_initials()
    table_raw = source("pair-dispositions-001.json")
    table_sha = sha(table_raw)
    table = json.loads(table_raw)
    receipt = json.loads(source("source-receipt.json"))
    membership_raw = source("query-membership.json")
    require(sha(membership_raw) == receipt["membershipSha256"], "Source membership binding differs")
    membership = json.loads(membership_raw)
    expected = expected_pairs(initials)
    metadata = {}
    for character in MEMBERS:
        metadata[character], _ = parse(card_source(character).decode("utf-8").replace("\r\n", "\n"))
        require(metadata[character] is not None and metadata[character]["kanji"] == character,
                "Wrong target card")
    comparisons = {}
    require(set(receipt["comparisonCards"]) == {other for _, other in expected},
            "Comparison card inventory differs")
    for character, item in receipt["comparisonCards"].items():
        require(item["path"] == f"comparison-cards/{character}.md", "Wrong comparison path")
        raw = source(item["path"])
        require(sha(raw) == item["sha256"], "Comparison copy hash differs")
        comparisons[character], _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
        require(comparisons[character] is not None and comparisons[character]["kanji"] == character,
                "Wrong comparison card identity")
    rows = check_table(table, expected, metadata, comparisons, receipt, membership)
    require(not re.search(rb"\b(?:claude|gpt|N1-B130-(?:CLAUDE|GPT))\b", table_raw, re.I),
            "Shared pair table names a review family")
    mappings = {}
    for family in initials:
        name = f"responses/{family}-mapping-001.json"
        raw = source(name)
        mapping = json.loads(raw)
        check_mapping(family, mapping, initials[family], rows, table_sha)
        response = source(f"responses/{family}-response-001.md")
        opposite = b"gpt" if family == "claude" else b"claude"
        require(not re.search(rb"\b" + opposite + rb"\b", raw + response, re.I),
                "Family response contains the other review-family name")
        mappings[family] = {"mappingSha256": sha(raw), "responseSha256": sha(response),
                            "initialOpenClaimIds": list(mapping["originalOpenClaimIds"])}
    return {
        "pairCount": len(rows), "pairTableSha256": table_sha, "counts": table["counts"],
        "requiredDirectPairs": sorted({pair for findings in FINDINGS.values()
                                      for names in findings.values() for pair in names}),
        "claimedDirectGuards": {target: [row["pair"][1] for row in table["rows"]
                                        if row["pair"][0] == target and row["directExclusionOnNewEndpoint"]]
                               for target in MEMBERS},
        "boundedNoncollisionPairs": [row["pair"] for row in table["rows"]
                                    if row["decision"] == "bounded-noncollision"],
        "authorOpenQuizHolds": table["openQuizHolds"], "responses": mappings,
        "semanticAcceptance": False, "independenceAccepted": False, "publicationAccepted": False,
        "limits": "Exact finite question/pair/card/source bindings and family-name token checks only. "
                  "All 24 initial questions remain historical; their proposed dispositions require "
                  "source-backed substantive review and isolated confirmations. Complete dictionary "
                  "proof, external captures, prose independence and gates are separate requirements.",
    }
