"""Check B129's author schema against independently reconstructed source facts."""
from common import require


def verify_selection(selection, source_rows, index, members, base):
    expected = [{"kanji": char, "row": index[char]["sourceRow"]} for char in members]
    require(selection["batch"] == "129" and selection["base"] == base
            and selection["members"] == expected,
            "B129 selection membership, order or base differs")
    require(source_rows == [index[char] for char in members],
            "B129 complete source rows differ from the frozen index")
    return [{"kanji": item["kanji"], "sourceRow": item["row"]} for item in expected]


def verify_scan(recorded, rows, meanings, title, base, helper, original=None):
    literal = helper.tokens(meanings)
    keywords = set(recorded["expandedKeywords"])
    require(recorded["base"] == base and recorded["tokenRegex"] == "[a-z]+"
            and recorded["literalKeywords"] == sorted(literal)
            and recorded["expandedKeywords"] == sorted(keywords)
            and literal <= keywords,
            "B129 scan identity, policy or literal coverage differs")
    if original is not None:
        require(recorded["kanji"] == original["kanji"]
                and set(original["expandedKeywords"]) <= keywords,
                "B129 expanded scan drops earlier keywords or changes member")
    matched = helper.matched_rows(rows, keywords)
    expected = [
        {
            "kanji": row["kanji"],
            "path": row["path"],
            "baselineBytesSha256": row["baselineGitBytesSha256"],
            "title": row["title"],
            "completeMeanings": row["meanings"],
            "matchedKeywords": row["matchedWords"],
        }
        for row in matched
    ]
    matches = [row["kanji"] for row in expected if row["matchedKeywords"]]
    require(recorded["rows"] == expected and recorded["matches"] == matches,
            "B129 whole-baseline scan does not reproduce")
    return {
        "tokens": sorted(keywords),
        "matches": matches,
        "scannedBaselineCards": len(expected),
        "targetTitleFromSignedCard": title,
        "titleBindingLimit": "The target title is read from the signed card, not an author scan field.",
    }
