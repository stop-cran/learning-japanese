"""Bounded complete-record optional access; no complete KD-file access."""
import math
import xml.etree.ElementTree as ET
from capacity008 import CAPS, FIT, chain_cost as unused_chain_cost, project, xml_bytes
from capacity008 import source_class as base_source_class

DERIVED = ("evidence/xml-presentation.json", "evidence/font-cmap.json", "evidence/dictionary-index.json")


def full_units(raw):
    root = ET.fromstring(raw)
    lines = raw.splitlines(keepends=True)
    records = lines[1:-1]
    if len(records) != len(root) or len(root) != 85:
        raise ValueError("Full KD source is not one complete union record per line")
    units = {}
    for node, record in zip(root, records):
        if ET.tostring(ET.fromstring(record)) != ET.tostring(node).rstrip(b"\n"):
            raise ValueError("Record byte framing differs")
        literal = node.findtext("literal")
        name = f"evidence/kanjidic2-full-records/{literal}.xml"
        if name in units:
            raise ValueError("Duplicate KD literal")
        units[name] = record
    return units


def source_class(name):
    name = name.split(" [", 1)[0]
    if name.startswith("evidence/kanjidic2-full-records/"):
        return "full-kd-record", .60
    return base_source_class(name)


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
    # build_chain flushes before a <=13900-byte source that cannot wholly fit its current bucket.
    # Such a source cannot acquire an interaction split. Large sources retain 003's extra part.
    return 2100 * (segments if len(raw) <= 13900 else segments + 1)


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
