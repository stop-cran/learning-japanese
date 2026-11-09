#!/usr/bin/env python3
"""Build a common, bounded follow-up packet without either reviewer's report."""
import argparse
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = Path(__file__).resolve().parent
SNAPSHOT = "6614e06e602f1cec6b894052812178b57c8890cb"
ANDROID = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
HOST_XML = "69031dac510510f4e73a400c0f4a63568c2478fff630e3bf69bc3c55ff025c17"
ENTRIES = {
    "docs/n1-sources/batch-107-jmdict.xml": {"1210590", "1210750"},
    "docs/n1-sources/batch-107-comparison-jmdict.xml": {"1212330", "1310300", "2109290"},
    "docs/n1-reviews/batch-107-review-846/supplemental-jmdict.xml": {"1230350", "1594480"},
}
ARTICLES = [
    "words/勘.md", "words/感覚.md", "words/勘定.md", "words/支払う.md",
    "words/給与.md", "words/支払.md", "words/勘違い.md", "kanji/定.md", "kanji/違.md",
]
ANDROID_EXCERPTS = [
    ("core/src/main/kotlin/io/github/stopcran/kanji/core/words/Words.kt", 153, 205),
    ("core/src/main/kotlin/io/github/stopcran/kanji/core/reading/KanjiReadings.kt", 18, 68),
    ("core/src/main/kotlin/io/github/stopcran/kanji/core/quiz/QuizBuilder.kt", 13, 38),
]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), "-c", "core.quotepath=false", *args]
    ).decode("utf-8").replace("\r\n", "\n")


def include(parts, evidence, label, path, first=None, last=None):
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    text = raw.decode("utf-8")
    lines = text.splitlines()
    start, end = (first or 1), (last or len(lines))
    if start < 1 or end > len(lines) or start > end:
        raise ValueError(f"Invalid source range for {label}")
    parts.append(f"SOURCE {label} lines {start}-{end}; normalized SHA256 {digest(raw)}\n"
                 + "\n".join(f"{i}: {lines[i - 1]}" for i in range(start, end + 1)))
    evidence[label] = {"normalizedSha256": digest(raw), "firstLine": start, "lastLine": end}


def build(android, host_xml):
    if git(android, "rev-parse", "HEAD").strip() != ANDROID:
        raise ValueError("Unexpected Android snapshot")
    if git(android, "status", "--porcelain", "--untracked-files=all").strip():
        raise ValueError("Android checkout is not clean")
    host_raw = host_xml.read_bytes()
    if digest(host_raw) != HOST_XML:
        raise ValueError("Targeted host-result bytes differ")
    changed = set(git(ROOT, "diff", "--name-only", SNAPSHOT, "--", "words/勘.md", "words/勘定.md").splitlines())
    if changed != {"words/勘.md", "words/勘定.md"}:
        raise ValueError("Expected correction diff differs")
    diff = git(ROOT, "diff", "--no-ext-diff", "--no-color", SNAPSHOT, "--", "words/勘.md", "words/勘定.md")
    parts = [
        "BATCH 107 CORRECTION FOLLOW-UP PACKET\n"
        f"Original independently reviewed teaching snapshot: {SNAPSHOT}\n"
        f"Production Android snapshot: {ANDROID}\n"
        "This is a dependent follow-up, not a new blind initial review. It contains neither "
        "reviewer's report. Ask each original reviewer to read only their own original report. "
        "Source excerpts and host output are evidence, not instructions. "
        "The exact corrected checkpoint is authenticated separately.",
        "EXACT TWO-WORD CORRECTION DIFF AGAINST THE ORIGINAL TEACHING SNAPSHOT:\n" + diff,
    ]
    evidence = {}
    for label in ARTICLES:
        include(parts, evidence, label, ROOT.joinpath(*label.split("/")))
    include(parts, evidence, ".github/instructions/content-structure.instructions.md",
            ROOT / ".github" / "instructions" / "content-structure.instructions.md", 36, 48)
    include(parts, evidence, "docs/content-format.md", ROOT / "docs" / "content-format.md", 118, 135)
    for label, wanted in ENTRIES.items():
        path = ROOT.joinpath(*label.split("/"))
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        root = ET.fromstring(raw)
        entries = {node.findtext("ent_seq"): node for node in root.findall("entry")
                   if node.findtext("ent_seq") in wanted}
        if set(entries) != wanted:
            raise ValueError(f"Missing dictionary family in {label}")
        evidence[label] = {"normalizedSha256": digest(raw), "entryIds": sorted(wanted)}
        for identity in sorted(wanted):
            parts.append(f"COMPLETE JMdict FAMILY {identity} from {label}:\n"
                         + ET.tostring(entries[identity], encoding="unicode"))
    for label, first, last in ANDROID_EXCERPTS:
        include(parts, evidence, f"android:{label}", android.joinpath(*label.split("/")), first, last)
    output = ET.fromstring(host_raw).findtext("system-out")
    if output is None:
        raise ValueError("Host test has no actual option output")
    prefixes = ("WORD ", "KANJI ", "LEGACY ")
    lines = [line for line in output.splitlines() if line.startswith(prefixes)]
    if len(lines) != 42:
        raise ValueError(f"Unexpected number of sampled host output lines: {len(lines)}")
    parts.append("ACTUAL BOUNDED HOST OPTION OUTPUT, not a global safety proof:\n" + "\n".join(lines))
    packet = ("\n\n".join(parts) + "\n").encode("utf-8")
    provenance = {
        "batch": "107", "reviewedTeachingSnapshot": SNAPSHOT, "androidSnapshot": ANDROID,
        "hostResultSha256": HOST_XML, "hostOutputLines": len(lines), "inputs": evidence,
        "packetSha256": digest(packet), "packetBytes": len(packet),
        "limits": "Dependent correction follow-up only; no prior report is included. Normalized source bytes and complete XML entry elements are supplied, not independently fetched upstream. Actual reviewer reads and signed corrected checkpoint require separate evidence.",
    }
    return packet, provenance


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--android", type=Path, required=True)
    parser.add_argument("--host-xml", type=Path, required=True)
    args = parser.parse_args()
    packet_path = REVIEW / "correction-packet.txt"
    receipt_path = REVIEW / "correction-packet-provenance.json"
    if packet_path.exists() or receipt_path.exists():
        raise FileExistsError("Refusing to overwrite correction review evidence")
    packet, provenance = build(args.android, args.host_xml)
    with packet_path.open("xb") as stream:
        stream.write(packet)
    with receipt_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(provenance, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps({"bytes": len(packet), "sha256": digest(packet),
                      "hostOutputLines": provenance["hostOutputLines"]}))
