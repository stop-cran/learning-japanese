"""Mechanical projection and conservative capacity arithmetic for preparation 004."""
import copy
import math
import xml.etree.ElementTree as ET

FIT = {"docs": .354, "jlpt": .374, "cards": .502, "evjson": .522,
       "extract": .446, "jmdict": .543, "titleidx": .531, "kd-projection": .65}
OPTIONAL = (
    "evidence/kanjidic2-records.xml",
    "evidence/xml-presentation.json",
    "evidence/font-cmap.json",
    "evidence/dictionary-index.json",
)
CAPS = ((25, 10), (20, 10), (15, 10), (10, 10), (10, 5))


def project(raw):
    root = ET.fromstring(raw)
    for character in root.findall("character"):
        for node in list(character):
            if node.tag in {"codepoint", "dic_number", "query_code"}:
                character.remove(node)
        for group in character.findall("reading_meaning/rmgroup"):
            for node in list(group):
                if ((node.tag == "meaning" and node.get("m_lang", "en") != "en")
                        or (node.tag == "reading" and node.get("r_type") in
                            {"pinyin", "korean_r", "korean_h", "vietnam"})):
                    group.remove(node)
    return root


def xml_bytes(root):
    return ("<" + root.tag + ">\n" + "\n".join(
        ET.tostring(node, encoding="unicode", short_empty_elements=True) for node in root)
        + "\n</" + root.tag + ">\n").encode("utf-8")


def projected_equal(full, projected):
    return ET.tostring(project(full)) == ET.tostring(ET.fromstring(projected))


def source_class(name):
    name = name.split(" [", 1)[0]
    if name == "evidence/kanjidic2-review-projection.xml":
        return "kd-projection", .715
    if name.endswith(".json") or name.startswith(("diffs/", "checks/")) or name.startswith("evidence/"):
        if name == "evidence/jmdict-families.xml":
            return "jmdict", .543 * 1.10
        if name == "evidence/kanjidic2-records.xml":
            return "full-kd", 1.0
        if name.endswith("-extract.txt"):
            return "extract", .446 * 1.10
        if name == "evidence/title-index.txt":
            return "titleidx", .531 * 1.10
        return "evjson", .522 * 1.10
    if name == "repo/docs/jlpt-levels.md":
        return "jlpt", .374 * 1.10
    if name.endswith(".md") and name.startswith(("repo/kanji/", "snapshot/", "baseline/")):
        return "cards", .502 * 1.10
    return "docs", .354 * 1.10


def source_tokens(name, raw):
    return math.ceil(len(raw) * source_class(name)[1])


def solo_envelope(raw):
    if not raw.endswith(b"\n"):
        raise ValueError("Source must end in LF")
    segments, size = 1, 0
    for line in raw.splitlines(keepends=True):
        if len(line) > 13900:
            raise ValueError("Source line exceeds bounded chain size")
        if size + len(line) > 13900:
            segments += 1
            size = 0
        size += len(line)
    return 2100 * (segments + 1)


def extension_upper(sources):
    envelope = 2100 + sum(solo_envelope(raw) for _, raw, _ in sources)
    return {"payloadBytes": sum(len(raw) for _, raw, _ in sources),
            "envelopeBytesUpper": envelope,
            "tokens": sum(source_tokens(name, raw) for name, raw, _ in sources)
                      + math.ceil(envelope * .574)}


def chain_cost(chain, sources):
    payload = sum(len(raw) for _, raw, _ in sources)
    total = sum(row["bytes"] for row in chain["segments"])
    if total < payload:
        raise ValueError("Negative chain envelope")
    return {"payloadBytes": payload, "chainBytes": total, "envelopeBytes": total - payload,
            "tokens": sum(source_tokens(name, raw) for name, raw, _ in sources)
                      + math.ceil((total - payload) * .574)}
