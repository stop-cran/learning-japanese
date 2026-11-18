"""Verify exact pair/history changes without accepting their linguistic conclusions."""
import json
import re

from b130_followup_closure_history import PREVIOUS
from b130_revision_pairs import DECISIONS, TEXT_FIELDS, load_initials
from common import require, sha

PAIR = ["拍", "響"]


def check_table(previous_raw, table, metadata, receipt):
    previous = json.loads(previous_raw)
    require(table["parent"] == PREVIOUS and table["publishedBase"] == previous["publishedBase"]
            and len(table["rows"]) == len(previous["rows"]) == 28
            and [row["pair"] for row in table["rows"]] == [row["pair"] for row in previous["rows"]]
            and len({tuple(row["pair"]) for row in table["rows"]}) == 28
            and table["supersedes"] == {
                "path": "pair-dispositions-001.json", "sha256": sha(previous_raw),
                "historyPreserved": True, "changedPairOnly": PAIR},
            "Prior pair inventory or exact history differs")
    changed = [(old, new) for old, new in zip(previous["rows"], table["rows"]) if old != new]
    require(len(changed) == 1 and changed[0][0]["pair"] == changed[0][1]["pair"] == PAIR,
            "More than the unresolved pair changed")
    old, new = changed[0]
    allowed = {*TEXT_FIELDS, "decision", "directExclusionOnNewEndpoint", "completeFamilyCanonicalHashes"}
    require({key: value for key, value in old.items() if key not in allowed}
            == {key: value for key, value in new.items() if key not in allowed}
            and new["decision"] == "precaution" and new["directExclusionOnNewEndpoint"] is True
            and all(isinstance(new[field], str) and new[field].strip() for field in TEXT_FIELDS),
            "New precaution changed its source/card/question scope")
    hashes = receipt["outputs"]["jmdict-families.xml"]["canonicalRecordHashes"]
    require(new["completeFamilyCanonicalHashes"] == {
        **old["completeFamilyCanonicalHashes"], "1408810": hashes["1408810"]},
        "Complete effect family binding differs")
    require(table["counts"] == {decision: sum(row["decision"] == decision for row in table["rows"])
                                for decision in DECISIONS}
            == {"guard": 8, "precaution": 17, "bounded-noncollision": 3},
            "Finite pair counts differ")
    for row in table["rows"]:
        target, other = row["pair"]
        require(row["targetDisplayedTitle"] == metadata[target]["title"]
                and row["directExclusionOnNewEndpoint"] is (other in metadata[target]["quiz_exclusions"])
                and row["directExclusionOnNewEndpoint"] is (row["decision"] in ("guard", "precaution"))
                and other not in metadata[target]["distractors"], "Pair no longer matches runtime")
    require(table["openQuizHolds"] == [row["pair"] for row in table["rows"] if row["openQuizHold"]] == []
            and [row["pair"] for row in table["rows"] if row["decision"] == "bounded-noncollision"]
            == [["耗", "文"], ["耗", "研"], ["耗", "書"]],
            "Unprotected or noncollision inventory differs")
    for key in ("policy", "remainingLexicalUncertainty", "limits"):
        require(table[key] == previous[key], "Original qualification or limits changed")
    return {"pairCount": 28, "counts": table["counts"], "changedPairOnly": PAIR,
            "authorOpenQuizHolds": [], "semanticAcceptance": False, "publicationAccepted": False}


def check_responses(source, table_raw):
    initials = load_initials()
    result = {}
    for family in ("claude", "gpt"):
        previous_raw = source(f"responses/{family}-mapping-001.json")
        previous = json.loads(previous_raw)
        raw = source(f"responses/{family}-mapping-002.json")
        mapping = json.loads(raw)
        response = source(f"responses/{family}-response-002.md")
        require(mapping["parent"] == PREVIOUS
                and mapping["authorStatus"] == "unpublished-proposal-awaiting-two-independent-confirmations"
                and mapping["historicalMapping"] == {
                    "path": f"{family}-mapping-001.json", "sha256": sha(previous_raw)}
                and mapping["neutralPair"] == PAIR
                and mapping["neutralTable"] == "../pair-dispositions-002.json"
                and mapping["neutralTableSha256"] == sha(table_raw)
                and mapping["authorDisposition"] == "precaution"
                and mapping["lexicalAllocationResolved"] is False
                and mapping["ordinaryCollisionEstablished"] is False
                and mapping["oldSnapshotAcceptanceNotTransferred"] is True
                and mapping["reviewContactOrLaunch"] is False,
                "Response changed its historical or acceptance boundary")
        opposite = b"gpt" if family == "claude" else b"claude"
        require(not re.search(rb"\b" + opposite + rb"\b", raw + response, re.I),
                "Response names another review family")
        require(mapping["retainedConfirmationLimits"] == [
            f"L{i}" for i in range(1, 6 if family == "claude" else 9)], "Confirmation limits lost")
        if family == "gpt":
            initial = initials[family]["adjudication"]
            require(mapping["originalOpenClaimIds"] == initial["openClaimIds"]
                    and mapping["originalComparisonQuestions"] == initial["unresolvedComparisons"]
                    and mapping["historicalD18Disposition"] == next(
                        row for row in previous["comparisonDispositions"] if row["id"] == "D18")
                    and mapping["currentD18"] == {
                        "id": "D18", "confirmationLimit": "L1", "authorDisposition": "precaution",
                        "directPairProtected": True, "lexicalAllocationResolved": False,
                        "status": "author-addressed-awaiting-independent-confirmation"},
                    "Original questions or D18 history changed")
        result[family] = {"mappingSha256": sha(raw), "responseSha256": sha(response)}
    for name in ("source-reuse-002.json",):
        require(not re.search(rb"\b(?:claude|gpt|N1-B130-(?:CLAUDE|GPT))\b", source(name), re.I),
                "Shared source reuse evidence names a family")
    require(not re.search(rb"\b(?:claude|gpt|N1-B130-(?:CLAUDE|GPT))\b", table_raw, re.I),
            "Shared pair evidence names a family")
    return result
