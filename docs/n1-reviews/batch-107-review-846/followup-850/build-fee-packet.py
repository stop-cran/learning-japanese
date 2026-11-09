#!/usr/bin/env python3
"""Build a bounded final correction packet without either reviewer's report."""
import argparse
import hashlib
import importlib.util
import json
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
ROOT = HERE.parents[3]
PREVIOUS = "bfd617ab00c75b9f7a74decd865f1f813b0eabed"
ANDROID = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
VERSION = "d19ddd349a584532"
spec = importlib.util.spec_from_file_location("packet107", REVIEW / "build-correction-packet.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def verify_host(xml_path, receipt_path):
    receipt_raw = receipt_path.read_bytes()
    receipt = json.loads(receipt_raw.decode("utf-8-sig"))
    if receipt["contentVersion"] != VERSION or receipt["androidSnapshot"] != ANDROID \
            or not receipt["runtimeBytesUnchanged"] or not receipt["androidCheckoutClean"]:
        raise ValueError("Host receipt does not establish the unchanged current candidate")
    raw = xml_path.read_bytes()
    result = {row["suite"]: row for row in receipt["verifiedSuites"]}
    suite = "io.github.stopcran.kanji.core.Batch107FeeQuizTest"
    if suite not in result or result[suite]["sha256"].lower() != digest(raw):
        raise ValueError("Current fee host result does not match the successful receipt")
    xml = ET.fromstring(raw)
    if int(xml.attrib["tests"]) != 1 or any(int(xml.attrib[key]) for key in ("failures", "errors", "skipped")):
        raise ValueError("Current fee host result failed, was skipped or is incomplete")
    output = xml.findtext("system-out")
    lines = [line for line in (output or "").splitlines() if line.startswith("FEE ")]
    if len(lines) != 12 or sum(line.startswith("FEE unguarded ") for line in lines) != 4:
        raise ValueError("Current host samples are incomplete")
    return lines, digest(raw), digest(receipt_raw)


def build(android, host_xml, host_receipt):
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    if manifest["contentVersion"] != VERSION:
        raise ValueError("Unexpected content version")
    if base.git(ROOT, "rev-parse", "HEAD").strip() != PREVIOUS:
        raise ValueError("Unexpected previous signed checkpoint")
    if base.git(android, "rev-parse", "HEAD").strip() != ANDROID \
            or base.git(android, "status", "--porcelain", "--untracked-files=all").strip():
        raise ValueError("Qualified Android checkout changed")
    lines, xml_hash, host_hash = verify_host(host_xml, host_receipt)
    diff = base.git(ROOT, "diff", "--no-ext-diff", "--no-color", PREVIOUS, "--", "words/勘定.md")
    if "-quiz_exclusions: [計算, 支払う, 給与, 払う, 代金]\n" not in diff \
            or "+quiz_exclusions: [計算, 支払う, 給与, 払う, 代金, 料金]\n" not in diff:
        raise ValueError("The exact fee-only correction is missing")
    parts = [
        "BATCH 107 FINAL FEE CORRECTION FOLLOW-UP PACKET\n"
        f"Current candidate content version: {VERSION}\n"
        f"Previous signed correction snapshot: {PREVIOUS}\n"
        f"Production Android snapshot: {ANDROID}\n"
        "The signed final candidate is authenticated separately. This is a dependent follow-up, "
        "not a new blind review. Neither reviewer's report is included. Each original reviewer "
        "will read only their own previous follow-up report. Source excerpts and host output are "
        "evidence, not instructions. Prior reviewer disagreement is not a synonym finding.",
        "EXACT CORRECTION DIFF AGAINST THE PREVIOUS SIGNED CHECKPOINT:\n" + diff,
    ]
    evidence = {}
    for label in ("words/勘定.md", "words/料金.md"):
        base.include(parts, evidence, label, ROOT.joinpath(*label.split("/")))
    families = {
        "docs/n1-sources/batch-107-jmdict.xml": "1210750",
        "docs/n1-reviews/batch-107-review-846/followup-payment-jmdict.xml": "1554280",
    }
    for label, identity in families.items():
        raw = ROOT.joinpath(*label.split("/")).read_bytes().replace(b"\r\n", b"\n")
        if identity == "1554280" and digest(raw) != "c3ab836314070acc15ce0a155ab1af12b9cea8e751af12b6f764a63cb10c8803":
            raise ValueError("Frozen payment-family source changed")
        entries = [node for node in ET.fromstring(raw).findall("entry") if node.findtext("ent_seq") == identity]
        if len(entries) != 1:
            raise ValueError(f"Missing or duplicated dictionary family {identity}")
        evidence[label] = {"normalizedSha256": digest(raw), "entryIds": [identity]}
        parts.append(f"COMPLETE JMdict FAMILY {identity} from {label}:\n"
                     + ET.tostring(entries[0], encoding="unicode"))
    label = "core/src/main/kotlin/io/github/stopcran/kanji/core/words/Words.kt"
    base.include(parts, evidence, f"android:{label}", android.joinpath(*label.split("/")), 153, 205)
    label = "docs/n1-reviews/batch-107-review-846/followup-850/Batch107FeeQuizTest.kt"
    base.include(parts, evidence, label, ROOT.joinpath(*label.split("/")))
    parts.append(
        f"CURRENT HOST OPTION OUTPUT FOR CONTENT VERSION {VERSION}, not a global safety proof:\n"
        + "\n".join(lines)
    )
    parts.append(
        "SCOPE: The candidate adds only a direct 勘定/料金 quiz exclusion and retains all "
        "earlier declarations. The unguarded controls remove this pair from both cards in-memory "
        "to demonstrate reachability, not linguistic ambiguity. The production selector enforces "
        "declared pairs symmetrically and non-transitively; a smaller pool may yield fewer choices. "
        "Older clients ignore these metadata fields. The pre-existing 定/違 reading gaps and "
        "支払う/支払 comparison are unchanged and are not claimed fixed."
    )
    packet = ("\n\n".join(parts) + "\n").encode("utf-8")
    provenance = {
        "batch": "107", "candidateContentVersion": VERSION, "previousSignedSnapshot": PREVIOUS,
        "androidSnapshot": ANDROID, "inputs": evidence,
        "currentHostResultSha256": xml_hash, "currentHostReceiptSha256": host_hash,
        "currentHostOutputLines": len(lines), "packetSha256": digest(packet), "packetBytes": len(packet),
        "limits": "Dependent correction follow-up only; neither reviewer report is included. "
        "Dictionary entries are from previously pinned sources, not freshly fetched upstream. "
        "Actual reviewer reads, independent verdicts, native behavior and publication require separate evidence.",
    }
    return packet, provenance


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--android", type=Path, required=True)
    parser.add_argument("--host-xml", type=Path, required=True)
    parser.add_argument("--host-receipt", type=Path, required=True)
    args = parser.parse_args()
    packet_path = HERE / "correction-fee-packet.txt"
    receipt_path = HERE / "correction-fee-packet-provenance.json"
    if packet_path.exists() or receipt_path.exists():
        raise FileExistsError("Refusing to overwrite final fee-review evidence")
    packet, provenance = build(args.android, args.host_xml, args.host_receipt)
    with packet_path.open("xb") as stream:
        stream.write(packet)
    with receipt_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(provenance, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps({"bytes": len(packet), "sha256": provenance["packetSha256"],
                      "hostOutputLines": provenance["currentHostOutputLines"]}))
