"""Verify unions of explicit spelling/reading selectors against complete XML records."""
import xml.etree.ElementTree as ET

from common import require
from verify_reconciliation_sources import element_value

PREFIXES = {"contains-keb", "exact-keb", "exact-reb"}


def validate(item):
    if item["mode"] == "union":
        require(all(":" in query and query.split(":", 1)[0] in PREFIXES
                    and query.split(":", 1)[1] for query in item["queries"]),
                "Invalid union selector")


def selects(node, tag, identity, mode, queries):
    keys = {identity} if tag == "character" else {
        item.text for item in node.findall("k_ele/keb") if item.text}
    if mode in {"contains-member", "contains-any"}:
        return any(query in key for query in queries for key in keys)
    if mode == "exact":
        return bool(keys & set(queries))
    require(mode == "union" and tag == "entry", "Unsupported source selector")
    readings = {item.text for item in node.findall("r_ele/reb") if item.text}
    for query in queries:
        kind, value = query.split(":", 1)
        if ((kind == "contains-keb" and any(value in key for key in keys))
                or (kind == "exact-keb" and value in keys)
                or (kind == "exact-reb" and value in readings)):
            return True
    return False


def verify_stream(stream, tag, key, selections, guard):
    for item in selections:
        validate(item)
    found = [set() for _ in selections]
    parser = ET.iterparse(stream, events=("start", "end"))
    _, root = next(parser)
    for event, node in parser:
        if event != "end" or node.tag != tag:
            continue
        identity = node.findtext(key)
        for item, seen in zip(selections, found):
            if selects(node, tag, identity, item["mode"], item["queries"]):
                require(identity not in seen, "Duplicate identity in pinned dictionary")
                require(identity in item["expected"], f"Missing applicable family: {item['name']}/{identity}")
                require(element_value(node) == item["expected"][identity],
                        f"Incomplete or altered record: {item['name']}/{identity}")
                seen.add(identity)
        node.clear()
        root.clear()
        guard.check()
    for item, seen in zip(selections, found):
        require(seen == set(item["expected"]), f"Unexpected or missing extracted record: {item['name']}")
    return [sorted(seen) for seen in found]
