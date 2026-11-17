"""Adapt the prepared verifier to B120's actual signed source layout."""
import hashlib
import json
import stat
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
SOURCE = WS / "scratch-120" / "review" / "prepare-source-contract.py"
TARGET = SOURCE.with_name("prepare-source-contract-v2.py")
RECEIPT = SOURCE.with_name("source-contract-derivation-v2.json")
EXPECTED = "b18fcf0b2dde72331700b0d7071711d98078c3e263fb0db361d4e16a554b609a"

HELPER = '''
def merge_jmdict_records(payloads):
    records = {}
    for raw in payloads:
        for record in ET.fromstring(raw).findall("entry"):
            key = record.findtext("ent_seq")
            require(key and key.isdigit(), "Missing or invalid JMdict entry identity")
            require(key not in records or element_value(records[key]) == element_value(record),
                    "Conflicting repeated JMdict record")
            records[key] = record
    root = ET.Element("JMdict")
    root.extend(records.values())
    return records, ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\\n"


'''

PAIRS = (
    ('def main(candidate, source_receipt_sha):', HELPER + 'def main(candidate, source_receipt_sha):'),
    ('selection = json.loads(source("selection.json"))',
     'selection = json.loads(source("selection-002.json"))'),
    ('rows = {r["kanji"]: r for r in index}',
     'rows = {r["kanji"]: r for r in index}\n'
     '        require(json.loads(source("source-row.json")) == rows["逮"], "Frozen source row differs")'),
    ('before, after = old(word_path), blob(word_path)',
     'before = old(word_path).replace(b"\\r\\n", b"\\n")\n'
     '            after = blob(word_path).replace(b"\\r\\n", b"\\n")'),
    ('require(sha(blob(path)) == current[path], f"Manifest differs from signed blob: {path}")',
     'require(sha(blob(path).replace(b"\\r\\n", b"\\n")) == current[path],\n'
     '                    f"Manifest differs from normalized signed text: {path}")'),
    ('for name in ("kanjidic2-initial-records.xml", "kanjidic2-comparison-records.xml"):',
     'for name in ("kanjidic2-alternative-records.xml", "kanjidic2-alternative-comparison-records-002.xml"):'),
    ('''        jm_raw = source("jmdict-initial-records.xml")
        jm_records = ET.fromstring(jm_raw).findall("entry")
        jm = {r.findtext("ent_seq"): r for r in jm_records}
        require(len(jm) == len(jm_records) and set(jm) == set(receipt["sources"]["jmdict"]["completeEntryIds"]),
                "Incomplete JMdict extraction")''',
     '''        selected_jm = source("jmdict-alternative-records.xml")
        comparisons_jm = source("jmdict-alternative-secondary-records.xml")
        jm, jm_raw = merge_jmdict_records([selected_jm, comparisons_jm])
        require(set(jm) == set(receipt["sources"]["jmdict"]["completeEntryIds"]),
                "Incomplete JMdict extraction")
        for kind, selected_name, comparison_name in (
            ("kanjidic2", "kanjidic2-alternative-records.xml",
             "kanjidic2-alternative-comparison-records-002.xml"),
            ("jmdict", "jmdict-alternative-records.xml", "jmdict-alternative-secondary-records.xml"),
        ):
            require(inputs[selected_name] == receipt["sources"][kind]["selectedRecordsSha256"]
                    and inputs[comparison_name] == receipt["sources"][kind]["comparisonRecordsSha256"],
                    f"Source receipt extraction hashes differ: {kind}")'''),
    ('for q in receipt["sources"]["jmdict"]["queries"]',
     'for q in receipt["sources"]["jmdict"]["comparisonQueries"]'),
    ('require(digest == snapshot["inputs"][filename]["sha256"], "Pinned dictionary changed")',
     'require(digest == snapshot["inputs"][filename]["sha256"], "Pinned dictionary changed")\n'
     '            kind = "kanjidic2" if tag == "character" else "jmdict"\n'
     '            require(digest == receipt["sources"][kind]["compressedSha256"],\n'
     '                    "Source receipt dictionary pin differs")'),
    ('next(item for item in kvg["files"] if item["kanji"] == c)',
     'next(item for item in [kvg["file"]] if item["kanji"] == c)'),
    ('require([r["kanji"] for r in joyo["rows"]] == MEMBERS, "Joyo membership differs")\n'
     '        for row in joyo["rows"]:',
     'joyo_rows = [joyo["row"]]\n'
     '        require([r["kanji"] for r in joyo_rows] == MEMBERS, "Joyo membership differs")\n'
     '        for row in joyo_rows:'),
    ('for r in joyo["rows"]],', 'for r in joyo_rows],'),
    ('"method": "Explicit coordinator normalization. Whole JMdict bytes are retained, including provisional "\n'
     '                  "selection records. Complete target KANJIDIC2 records are selected from verified complete "\n'
     '                  "signed records and reserialized. Selection, Joyo and SVG metadata are neutral derivatives. "\n'
     '                  "No author rationale or chosen comparison list is exported.",',
     '"method": "Explicit coordinator normalization. Complete JMdict records from the selected current "\n'
     '                  "family and comparison extraction are verified, merged and reserialized. Duplicate "\n'
     '                  "identities must be structurally identical. Complete target KANJIDIC2 records are "\n'
     '                  "selected from verified signed records. Deferred selection bytes remain preserved in "\n'
     '                  "Git but are not included as current teaching. Selection, Joyo and SVG metadata are "\n'
     '                  "neutral derivatives. No author rationale or chosen comparison list is exported.",'),
    ('"sourceMembersInCandidate": 250, "baselineRuntimePreservedExceptRequiredWrappers": True,',
     '"sourceMembersInCandidate": 250, "baselineRuntimePreservedExceptRequiredWrappers": True,\n'
     '             "runtimeTextHashing": "CRLF to LF, matching tools/build_manifest.py and the pinned ZIP verifier; "\n'
     '                                   "source artifacts and packet blobs retain their exact committed bytes.",\n'
     '             "runtimeBlobHashes": {p: {"raw": sha(blob(p)), "normalized": current[p],\n'
     '                                      "crlfCount": blob(p).count(b"\\r\\n")}\n'
     '                                   for p in sorted(additions | wrappers)},'),
)


def main():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise ValueError("Prepared B120 verifier changed")
    if TARGET.exists() or RECEIPT.exists():
        raise FileExistsError("Preserve existing actual-schema derivation")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8")
    substitutions = []
    for before, after in PAIRS:
        before, after = before.replace("\n", newline), after.replace("\n", newline)
        if text.count(before) != 1 or after in text:
            raise ValueError(f"Ambiguous actual-schema substitution: {before}")
        text = text.replace(before, after)
        substitutions.append({"before": before, "after": after, "count": 1})
    reverse = text
    for item in reversed(substitutions):
        if reverse.count(item["after"]) != 1:
            raise ValueError("Actual-schema reverse substitution mismatch")
        reverse = reverse.replace(item["after"], item["before"])
    if reverse.encode("utf-8") != raw:
        raise ValueError("Actual-schema derivation is not byte-reversible")
    result = text.encode("utf-8")
    compile(result, str(TARGET), "exec")
    proof = {
        "source": str(SOURCE), "sourceSha256": EXPECTED,
        "target": str(TARGET), "targetSha256": hashlib.sha256(result).hexdigest(),
        "substitutions": substitutions, "reverseExact": True,
        "deriverSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "reason": "Actual signed B120 uses selection-002, two current JMdict files and singular Joyo/KanjiVG bindings. Runtime text hashing follows the existing CRLF-normalized manifest and ZIP contract; contributor/source artifacts remain byte-exact.",
    }
    for path, content in (
        (TARGET, result),
        (RECEIPT, (json.dumps(proof, ensure_ascii=False, indent=2) + "\n").encode("utf-8")),
    ):
        with path.open("xb") as stream:
            stream.write(content)
        path.chmod(stat.S_IREAD)
        if path.read_bytes() != content:
            raise ValueError(f"Readback mismatch: {path}")
    print(json.dumps({"target": str(TARGET), "targetSha256": proof["targetSha256"],
                      "derivation": str(RECEIPT), "derivationSha256": hashlib.sha256(RECEIPT.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
