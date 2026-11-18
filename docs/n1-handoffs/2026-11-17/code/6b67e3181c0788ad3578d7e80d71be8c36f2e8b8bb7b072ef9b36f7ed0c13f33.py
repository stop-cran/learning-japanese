"""Verify B132 membership and scans without trusting author-supplied row hashes."""
from common import require


def verify_selection(selection, source_rows, index, members, base):
    require(type(selection["batch"]) is int and selection["batch"] == 132
            and selection["base"] == base and selection["members"] == members,
            "B132 selection membership, order or base differs")
    require(source_rows == [index[char] for char in members],
            "B132 complete source rows differ from the frozen index")
    return [{"kanji": char, "sourceRow": index[char]["sourceRow"]} for char in members]


def verify_scan(recorded, rows, meanings, title, base, helper, original=None):
    literal = helper.tokens(meanings)
    keywords = set(recorded["expandedKeywords"])
    require(recorded["base"] == base and recorded["tokenRegex"] == "[a-z]+"
            and recorded["literalKeywords"] == sorted(literal)
            and recorded["expandedKeywords"] == sorted(keywords)
            and literal <= keywords,
            "B132 scan identity, policy or literal coverage differs")
    if original is not None:
        require(recorded["kanji"] == original["kanji"]
                and set(original["expandedKeywords"]) <= keywords,
                "B132 expanded scan drops earlier keywords or changes member")
    matched = helper.matched_rows(rows, keywords)
    expected = [
        {
            "kanji": row["kanji"],
            "path": row["path"],
            "baselineWorkingBytesSha256": row["baselineWorkingBytesSha256"],
            "baselineNormalizedSha256": row["baselineNormalizedSha256"],
            "title": row["title"],
            "completeMeanings": row["meanings"],
            "matchedKeywords": row["matchedWords"],
        }
        for row in matched
    ]
    matches = [row["kanji"] for row in expected if row["matchedKeywords"]]
    require(recorded["rows"] == expected and recorded["matches"] == matches,
            "B132 whole-baseline scan does not reproduce")
    return {
        "tokens": sorted(keywords),
        "matches": matches,
        "scannedBaselineCards": len(expected),
        "targetTitleFromSignedCard": title,
        "titleBindingLimit": "The target title is read from the signed card, not an author scan field.",
        "baselineHashLimit": "Working bytes are independently read and normalized against signed Git "
                             "bytes and the baseline manifest; raw Git and checkout hashes are distinct.",
    }
