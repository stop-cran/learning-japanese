#!/usr/bin/env python3
"""Build the common correction packet without either original review report."""
import argparse
import hashlib
import importlib.util
import json
import xml.etree.ElementTree as ET
from pathlib import Path

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
OUT = REVIEW / "followup-849"
spec = importlib.util.spec_from_file_location("packet107", REVIEW / "build-correction-packet.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.ENTRIES["docs/n1-reviews/batch-107-review-846/followup-payment-jmdict.xml"] = {
    "1501620", "1411790", "1554280"
}
base.ARTICLES.extend(["words/払う.md", "words/代金.md", "words/料金.md"])


def build(android, previous_xml, current_xml, host_receipt):
    current = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    if current["contentVersion"] != "db93cd80ee101b73":
        raise ValueError("Unexpected follow-up content version")
    receipt = json.loads(host_receipt.read_text(encoding="utf-8-sig"))
    if receipt["contentVersion"] != current["contentVersion"] or not receipt["runtimeBytesUnchanged"]:
        raise ValueError("Host receipt does not establish the current unchanged content")
    host_raw = current_xml.read_bytes()
    host_hash = hashlib.sha256(host_raw).hexdigest()
    results = {row["suite"]: row for row in receipt["verifiedSuites"]}
    suite = "io.github.stopcran.kanji.core.Batch107FollowupQuizTest"
    if suite not in results or results[suite]["sha256"].lower() != host_hash:
        raise ValueError("Current host result does not match the successful receipt")
    xml = ET.fromstring(host_raw)
    if int(xml.attrib["tests"]) != 1 or any(int(xml.attrib[key]) for key in ("failures", "errors", "skipped")):
        raise ValueError("Current host result failed, was skipped or is incomplete")
    output = xml.findtext("system-out")
    if output is None:
        raise ValueError("Current host result has no option output")
    lines = [line for line in output.splitlines() if line.startswith("FOLLOWUP ")]
    if len(lines) != 28:
        raise ValueError(f"Unexpected number of current host output lines: {len(lines)}")
    packet, provenance = base.build(android, previous_xml)
    text = packet.decode("utf-8")
    text = text.replace(
        "BATCH 107 CORRECTION FOLLOW-UP PACKET\n",
        "BATCH 107 ADDITIONAL CORRECTION FOLLOW-UP PACKET\n"
        f"Current candidate content version: {current['contentVersion']}\n"
        "The signed candidate checkpoint is authenticated separately.\n",
        1,
    )
    text = text.replace(
        "ACTUAL BOUNDED HOST OPTION OUTPUT, not a global safety proof:",
        "HISTORICAL HOST OPTION OUTPUT FOR PREVIOUS CONTENT VERSION f7fbaaa4b8e78194, "
        "not a global safety proof:",
        1,
    )
    parts = [text.rstrip()]
    evidence = provenance["inputs"]
    for label in (
        "docs/n1-reviews/batch-107-review-846/followup-payment-jmdict-provenance.json",
        "docs/n1-reviews/batch-107-review-846/Batch107FollowupQuizTest.kt",
    ):
        base.include(parts, evidence, label, ROOT.joinpath(*label.split("/")))
    parts.append(
        "CURRENT FOLLOW-UP HOST OPTION OUTPUT FOR CONTENT VERSION db93cd80ee101b73, "
        "not a global safety proof:\n" + "\n".join(lines)
    )
    parts.append(
        "COMPARISON TO ASSESS: The candidate adds direct 勘定/払う and 勘定/代金 guards "
        "and retains the earlier guards. It does not add 勘定/料金: 料金's actual label is "
        "'fee; charge; fare' and its complete entry is supplied above. Independently determine "
        "whether either label is a defensible alternative for the other under the app's two "
        "quiz directions. Direct exclusions are non-transitive; do not infer equivalence merely "
        "because both words relate to another term."
    )
    result = ("\n\n".join(parts) + "\n").encode("utf-8")
    provenance.update({
        "candidateContentVersion": current["contentVersion"],
        "previousHostResultSha256": provenance.pop("hostResultSha256"),
        "previousHostContentVersion": "f7fbaaa4b8e78194",
        "currentHostResultSha256": host_hash,
        "currentHostReceiptSha256": hashlib.sha256(host_receipt.read_bytes()).hexdigest(),
        "currentHostOutputLines": len(lines),
        "packetSha256": hashlib.sha256(result).hexdigest(),
        "packetBytes": len(result),
        "limits": "Dependent correction follow-up only; neither reviewer report is included. Historical host output is explicitly distinguished from the current host output. Source entries are from the pinned dictionary; actual reviewer reads, independent verdicts, native behavior and publication require separate evidence.",
    })
    return result, provenance


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--android", type=Path, required=True)
    parser.add_argument("--previous-host-xml", type=Path, required=True)
    parser.add_argument("--current-host-xml", type=Path, required=True)
    parser.add_argument("--host-receipt", type=Path, required=True)
    args = parser.parse_args()
    packet_path = OUT / "correction-followup-packet.txt"
    receipt_path = OUT / "correction-followup-packet-provenance.json"
    if packet_path.exists() or receipt_path.exists():
        raise FileExistsError("Refusing to overwrite follow-up review evidence")
    packet, provenance = build(args.android, args.previous_host_xml, args.current_host_xml, args.host_receipt)
    with packet_path.open("xb") as stream:
        stream.write(packet)
    with receipt_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(provenance, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps({"bytes": len(packet), "sha256": provenance["packetSha256"],
                      "currentHostOutputLines": provenance["currentHostOutputLines"]}))
