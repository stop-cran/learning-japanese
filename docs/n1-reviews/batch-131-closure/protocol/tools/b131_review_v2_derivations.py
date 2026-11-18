"""Pure, reproducible compact-002 projections and exact complete-family partition."""
import copy
import difflib
import json
import xml.etree.ElementTree as ET

from common import require, sha

REMOVED_CONTAINERS = {"codepoint", "dic_number", "query_code"}
REMOVED_READINGS = {"pinyin", "korean_r", "korean_h", "vietnam"}
CONTAINS = {"\u7f8a", "\u885b", "\u885e", "\u971c"}
DISPLAYED_READINGS = {"\u3048\u3044", "\u3048", "\u3088\u3046", "\u3072\u3064\u3058", "\u305d\u3046", "\u3057\u3082"}


def canonical_node(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode("utf-8")


def record_lines(raw, root_tag, record_tag):
    lines = raw.splitlines(keepends=True)
    require(lines[0] == ("<" + root_tag + ">\n").encode()
            and lines[-1] == ("</" + root_tag + ">\n").encode(), "Unexpected compact XML framing")
    require(all(line.endswith(b"\n") and b"\r" not in line for line in lines), "Unexpected XML line endings")
    root = ET.fromstring(raw)
    require(root.tag == root_tag and all(n.tag == record_tag for n in root)
            and len(root) == len(lines) - 2, "Not one complete record per line")
    for node, line in zip(root, lines[1:-1]):
        require(canonical_node(node) + b"\n" == line, "Original record line is not canonical")
    return root, lines[1:-1]


def remove_class(node):
    if node.tag in REMOVED_CONTAINERS:
        return node.tag
    if node.tag == "meaning" and "m_lang" in node.attrib:
        return "meaning@m_lang"
    if node.tag == "reading" and node.get("r_type") in REMOVED_READINGS:
        return "reading@" + node.get("r_type")
    return None


def kd_projection(raw):
    root, lines = record_lines(raw, "kanjidic2", "character")
    projected, audits = [], []
    for original, line in zip(root, lines):
        node = copy.deepcopy(original)
        removed = []

        def visit(parent, locator):
            for index, child in enumerate(list(parent)):
                path = locator + "/" + child.tag + "[" + str(index) + "]"
                reason = remove_class(child)
                if reason:
                    removed.append({"path": path, "class": reason,
                                    "sha256": sha(canonical_node(child))})
                    parent.remove(child)
                else:
                    visit(child, path)
        visit(node, "character")
        output = canonical_node(node)
        require(all(remove_class(child) is None for child in node.iter()), "Forbidden class remains")
        projected.append(output + b"\n")
        audits.append({"literal": original.findtext("literal"), "sourceSha256": sha(line),
                       "projectionSha256": sha(output + b"\n"), "removed": removed,
                       "retainedCanonicalSha256": sha(canonical_node(node))})
    return b"<kanjidic2>\n" + b"".join(projected) + b"</kanjidic2>\n", audits


def verify_kd(full, presented):
    expected, audits = kd_projection(full)
    require(presented == expected, "KANJIDIC projection is not the exact permitted removal")
    original, _ = record_lines(full, "kanjidic2", "character")
    projected, _ = record_lines(presented, "kanjidic2", "character")
    require([n.findtext("literal") for n in original] == [n.findtext("literal") for n in projected],
            "KANJIDIC records/order changed")
    return audits


def jm_partition(raw, reference, dictionary_index):
    root, lines = record_lines(raw, "JMdict", "entry")
    declared = set(reference["newCards"]) | {"\u885e"}
    declared |= {c for row in reference["cards"] for key in ("quiz_exclusions", "distractors") for c in row[key]}
    queries = {"contains-keb:" + c for c in CONTAINS}
    queries |= {"exact-keb:" + c for c in declared}
    queries |= {"exact-reb:" + r for r in DISPLAYED_READINGS}
    selected, remainder, reasons, classification = [], [], {}, {}
    seen = set()
    for node, line in zip(root, lines):
        identity = node.findtext("ent_seq")
        require(identity not in seen and identity, "Duplicate/missing JMdict ent_seq")
        seen.add(identity)
        kebs = [k.text for k in node.findall("k_ele/keb")]
        rebs = [r.text for r in node.findall("r_ele/reb")]
        matches = sorted(
            {"contains-keb:" + c for c in CONTAINS if any(c in keb for keb in kebs)}
            | {"exact-keb:" + keb for keb in kebs if keb in declared}
            | {"exact-reb:" + reb for reb in rebs if reb in DISPLAYED_READINGS})
        require(all(identity in dictionary_index.get(q, []) for q in matches),
                "Direct record rule disagrees with verified query membership")
        by_index = sorted(q for q in queries if identity in dictionary_index.get(q, []))
        require(matches == by_index, "JMdict rule/query index differs")
        reasons[identity] = matches
        if matches:
            selected.append((identity, line))
        else:
            remainder.append((identity, line))
            original_queries = [q for q, ids in dictionary_index.items() if identity in ids]
            require(original_queries, "Remainder lacks original query membership")
            has_keb = any(q.startswith("exact-keb:") for q in original_queries)
            has_reb = any(q.startswith("exact-reb:") for q in original_queries)
            classification[identity] = ("undeclared-exact-keb-and-other-exact-reb" if has_keb and has_reb else
                                        "undeclared-exact-keb" if has_keb else "other-exact-reb" if has_reb else
                                        "unexpected-query-class")
    core = b"<JMdict>\n" + b"".join(line for _, line in selected) + b"</JMdict>\n"
    metadata = {
        "total": len(root), "core": len(selected), "remainder": len(remainder),
        "coreIds": [key for key, _ in selected], "remainderIds": [key for key, _ in remainder],
        "declaredCharacters": sorted(declared), "containsCharacters": sorted(CONTAINS),
        "displayedReadings": sorted(DISPLAYED_READINGS), "ruleMatches": reasons,
        "remainderClasses": {label: {"ids": [key for key, _ in remainder if classification[key] == label],
                                     "recordBytes": sum(len(line) for key, line in remainder
                                                        if classification[key] == label)}
                             for label in sorted(set(classification.values()))},
        "undeclaredComparisonCharacters": sorted({q.removeprefix("exact-keb:") for q in dictionary_index
                                                  if q.startswith("exact-keb:") and
                                                  q.removeprefix("exact-keb:") not in declared}),
        "coreBytes": len(core), "coreRecordBytes": sum(len(line) for _, line in selected)}
    require(len(root) == len(selected) + len(remainder)
            and not set(metadata["coreIds"]) & set(metadata["remainderIds"]), "Invalid exact partition")
    return core, metadata


def verify_jm(full, presented, reference, dictionary_index, partition):
    expected, metadata = jm_partition(full, reference, dictionary_index)
    require(presented == expected and partition == metadata, "JMdict core/partition is not the exact rule")
    return metadata


def title_delta(baseline, candidate):
    before, after = baseline.decode("utf-8").splitlines(), candidate.decode("utf-8").splitlines()
    require(len(before) == 1254 and len(after) == 1257, "Title index counts differ")
    left, right = ({line.split(" ", 1)[0]: line for line in rows} for rows in (before, after))
    require(len(left) == len(before) and len(right) == len(after), "Duplicate title identity")
    added, removed = sorted(set(right) - set(left)), sorted(set(left) - set(right))
    changed = sorted(c for c in set(left) & set(right) if left[c] != right[c])
    require(set(added) == {"\u885b", "\u7f8a", "\u971c"} and not removed and not changed,
            "Title delta is not exactly the three additions")
    delta = "".join(difflib.unified_diff(baseline.decode().splitlines(keepends=True),
                                        candidate.decode().splitlines(keepends=True),
                                        fromfile="evidence/baseline-title-index.txt",
                                        tofile="evidence/title-index.txt", n=0)).encode("utf-8")
    return delta, {"added": [right[c] for c in added], "removed": removed, "changed": changed}


def verify_delta(baseline, candidate, presented):
    expected, result = title_delta(baseline, candidate)
    require(expected == presented, "Title delta differs from exact source recomputation")
    return result


def supplement_catalog(full, partition):
    root, lines = record_lines(full, "JMdict", "entry")
    core = set(partition["coreIds"])
    records, characters = {}, {}
    for node, line in zip(root, lines):
        identity = node.findtext("ent_seq")
        spellings = sorted({n.text for n in node.findall("k_ele/keb") if n.text and len(n.text) == 1})
        for char in spellings:
            row = characters.setdefault(char, {"matchingCoreIds": [], "matchingRemainderIds": []})
            row["matchingCoreIds" if identity in core else "matchingRemainderIds"].append(identity)
        if identity not in core:
            records[identity] = b"<JMdict>\n" + line + b"</JMdict>\n"
    return records, characters


def selected_supplements(full, partition, characters):
    root, lines = record_lines(full, "JMdict", "entry")
    core = set(partition["coreIds"])
    requested = set(characters)
    selected, matches = [], {char: {"matchingCoreIds": [], "matchingRemainderIds": []} for char in characters}
    for node, line in zip(root, lines):
        identity = node.findtext("ent_seq")
        hit = requested & {n.text for n in node.findall("k_ele/keb")}
        for char in hit:
            matches[char]["matchingCoreIds" if identity in core else "matchingRemainderIds"].append(identity)
        if hit and identity not in core:
            selected.append((identity, b"<JMdict>\n" + line + b"</JMdict>\n"))
    return selected, matches


def verify_supplements(full, partition, characters, supplied):
    expected, matches = selected_supplements(full, partition, characters)
    require(supplied == expected, "Selected extension omitted/altered/added matching complete JMdict records")
    return matches
