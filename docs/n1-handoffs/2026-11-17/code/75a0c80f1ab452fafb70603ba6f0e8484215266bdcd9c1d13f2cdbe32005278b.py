"""Check exact-query membership as well as complete individual dictionary records."""
import ast
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET

from common import WS, freeze_json, git, load_batch, require, sha, start_guard
from confirm_v2 import clean
from verify_b121_revision import INPUTS
from verify_reconciliation_sources import element_value

CANDIDATE = "b7369b9502f7f5c14a4f2081fe9e6a0e2b276e42"
PREFIX = "docs/n1-sources/batch-121/reconciliation-001/"


def main():
    config = load_batch(121)
    clean(config, CANDIDATE)
    guard, _ = start_guard("B121 complete exact-query membership")
    try:
        selections = []
        for script, prefix in (("extract.py", ""), ("extract-starter.py", "starter-"),
                               ("extract-roads.py", "roads-")):
            raw = git(config, "show", f"{CANDIDATE}:{PREFIX}{script}")
            assignments = {node.targets[0].id: node.value for node in ast.parse(raw).body
                           if isinstance(node, ast.Assign) and len(node.targets) == 1
                           and isinstance(node.targets[0], ast.Name)}
            if not prefix:
                chars = set(ast.literal_eval(assignments["chars"].args[0]))
                expression = assignments["queries"].args[0]
                require(isinstance(expression, ast.Call) and expression.func.attr == "split",
                        "Unexpected exact-query expression")
                queries = set(ast.literal_eval(expression.func.value).split())
            else:
                chars = ast.literal_eval(assignments["targets"])
                expression = assignments["queries"]
                require(isinstance(expression, ast.BinOp) and isinstance(expression.op, ast.BitOr)
                        and expression.left.id == "targets", "Unexpected query union")
                queries = chars | ast.literal_eval(expression.right)
            for kind, needles in (("kanjidic2", chars), ("jmdict", queries)):
                extracted = git(config, "show", f"{CANDIDATE}:{PREFIX}{prefix}{kind}-records.xml")
                filename, digest, tag, key = INPUTS[kind]
                nodes = ET.fromstring(extracted).findall(tag)
                expected = {node.findtext(key): element_value(node) for node in nodes}
                require(len(expected) == len(nodes), "Duplicate extracted identity")
                selections.append({"kind": kind, "script": script, "scriptSha256": sha(raw),
                                   "file": prefix + kind + "-records.xml", "sha256": sha(extracted),
                                   "needles": needles, "expected": expected, "found": set()})
        for kind, (filename, digest, tag, key) in INPUTS.items():
            source = WS / "control" / "inputs" / filename
            computed = hashlib.sha256()
            with source.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    computed.update(chunk)
                    guard.check()
            require(computed.hexdigest() == digest, "Pinned compressed input changed")
            active = [selection for selection in selections if selection["kind"] == kind]
            with gzip.open(source, "rb") as stream:
                parser = ET.iterparse(stream, events=("start", "end"))
                _, root = next(parser)
                for event, node in parser:
                    if event != "end" or node.tag != tag:
                        continue
                    keys = ({node.findtext(key)} if kind == "kanjidic2"
                            else {item.text for item in node.findall("k_ele/keb")})
                    identifier = node.findtext(key)
                    for selection in active:
                        if keys & selection["needles"]:
                            require(identifier in selection["expected"]
                                    and element_value(node) == selection["expected"][identifier],
                                    f"Missing or altered exact-query match: {selection['file']}/{identifier}")
                            selection["found"].add(identifier)
                    node.clear()
                    root.clear()
                    guard.check()
        results = []
        for selection in selections:
            require(selection["found"] == set(selection["expected"]), "Extra or missing extracted entry")
            results.append({key: value for key, value in selection.items()
                            if key not in ("needles", "expected", "found")} |
                           {"queries": sorted(selection["needles"]),
                            "completeMatchingRecords": len(selection["found"])})
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source-selection RAM guard breached")
    print(json.dumps(freeze_json(WS / "scratch-121" / "review" / "source-selection-verification-001.json", {
        "candidate": CANDIDATE, "status": "PASS", "results": results, "memory": memory,
        "limit": "Complete exact-query sets, not exhaustive lexical applicability or linguistic acceptance.",
    })))


if __name__ == "__main__":
    main()
