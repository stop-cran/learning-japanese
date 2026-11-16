import copy
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from b127_common import GUARD_SHA, HERE, PACKET, REPO, ROOT, git, sha, start_guard, write

PARENT = "fcf8cb48d4e66b774189fe253dd799daadcc4015"
OUT = REPO / "docs" / "n1-sources" / "batch-127-reconciliation"
ATTEMPT = HERE / "reconciliation-sources-001"
BRIEF = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\b127-reconciliation-001-brief.txt")
CLAIMS = {
    "Q1": ("囲", ["囲う", "囲い", "囲む"]),
    "Q2": ("保", ["保つ", "保管", "保存", "保護"]),
    "Q3": ("預", ["預ける", "預かる", "預かり", "預け", "預金"]),
    "Q4": ("容", ["容れる", "容器", "収容"]),
    "Q5": ("留", ["留める", "留まる", "留め置く"]),
    "Q6": ("存", ["存する", "存ずる", "保存", "存続", "存在"]),
    "Q7": ("持", ["持つ", "持ち", "持てる", "保持"]),
    "Q8": ("忙", ["忙しい", "忙しない", "多忙", "慌てる", "倉卒"]),
    "Q9": ("速", ["速い", "速やか", "速める", "急ぐ", "急速", "倉皇"]),
    "Q10": ("死", ["死", "死ぬ", "亡ぶ", "滅ぶ", "亡びる", "滅びる"]),
    "Q11": ("延", ["延ばす", "延びる", "延べる", "延期", "お倉入り", "お蔵入り", "蔵入り"]),
    "Q12": ("止", ["止める", "止まる", "取り止める", "取りやめる", "中止"]),
    "Q13": ("停", ["停める", "停まる", "停止"]),
}
INPUTS = {
    "jmdict": ("n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d", "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4", "entry"),
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed", "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8", "character"),
}


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        chunk = self.stream.read(size)
        self.digest.update(chunk)
        return chunk


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def binding(path):
    raw = path.read_bytes()
    return {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}


def main():
    assert not OUT.exists() and not ATTEMPT.exists()
    ATTEMPT.mkdir()
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        bindings = {"brief": binding(BRIEF)}
        assert bindings["brief"]["sha256"] == "a76b709534e787a22c6ed036b6f2f2b3ff23fbc1aaa4ea3b834c1a4a5541581d"
        for label, path, digest in [
            ("claudeReport", ROOT / "reports-127" / "initial-claude-001.md", "50be326b5749afe14d4981dc58ed5da9d131f4afa696256116e89990f3dea91e"),
            ("gptReport", ROOT / "reports-127" / "initial-gpt-001.md", "2b06d4380bb0ae0eca8c15df897301fe175f4be96a8fb7111739aa300f9ef6b6"),
            ("gptAdjudication", HERE / "review" / "N1-B127-GPT-001-adjudication.json", "6ae8732d5e9d34917deea3f7dd4663a5ccf45045724af56e15d19d2bb7e1fb23"),
        ]:
            bindings[label] = binding(path)
            assert bindings[label]["sha256"] == digest
        bindings["claudeAdjudication"] = binding(HERE / "review" / "N1-B127-CLAUDE-001-adjudication.json")
        queries = {term for _, terms in CLAIMS.values() for term in terms}
        wanted = {"倉"} | {ch for ch, _ in CLAIMS.values()}
        selected, source_digests, canonical_inputs = {}, {}, {}
        memberships = {term: [] for term in sorted(queries)}
        for label, (filename, compressed_sha, xml_sha, tag) in INPUTS.items():
            path = ROOT / "control" / "inputs" / filename
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(65536), b""):
                    guard.check()
                    digest.update(chunk)
            assert digest.hexdigest() == compressed_sha
            records, originals = [], {}
            with gzip.open(path, "rb") as stream:
                reader = HashReader(stream, guard)
                context = ET.iterparse(reader, events=("start", "end"))
                _, root = next(context)
                for event, node in context:
                    if event != "end" or node.tag != tag:
                        continue
                    guard.check()
                    if label == "jmdict":
                        eid = node.findtext("ent_seq")
                        matches = queries & {k.findtext("keb") for k in node.findall("k_ele")}
                        for term in matches:
                            memberships[term].append(eid)
                        admit = bool(matches)
                    else:
                        eid = node.findtext("literal")
                        admit = eid in wanted
                    if admit:
                        records.append(copy.deepcopy(node))
                        originals[eid] = sha(canonical(node).encode())
                    node.clear()
                    root.clear()
            assert reader.digest.hexdigest() == xml_sha
            selected[label], canonical_inputs[label] = records, originals
            source_digests[label] = {"filename": filename, "compressedSha256": compressed_sha, "decompressedSha256": xml_sha}
        outputs, lines = {}, []
        for label, records in selected.items():
            tag = INPUTS[label][3]
            root = ET.Element("JMdict" if label == "jmdict" else "kanjidic2")
            root.extend(records)
            ET.indent(root, space="  ")
            raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
            name = label + "-comparison-records.xml"
            write(OUT / name, raw)
            reparsed = ET.fromstring(raw).findall(tag)
            actual = {(n.findtext("ent_seq") or n.findtext("literal")): sha(canonical(n).encode()) for n in reparsed}
            assert actual == canonical_inputs[label]
            outputs[name] = {"sha256": sha(raw), "bytes": len(raw), "canonicalCompleteRecordHashes": actual}
            if label == "kanjidic2":
                assert set(actual) == wanted
                for n in reparsed:
                    group = n.find("reading_meaning/rmgroup")
                    lines.append(n.findtext("literal") + " | " + "; ".join(m.text for m in group.findall("meaning") if m.get("m_lang") in (None, "en")))
            else:
                for n in reparsed:
                    lines.append("\nJMdict " + n.findtext("ent_seq"))
                    for child in n:
                        if child.tag != "ent_seq":
                            lines.append(ET.tostring(child, encoding="unicode").strip())
        write(ATTEMPT / "complete-record-readback.txt", "\n".join(lines).encode())
        for ch in sorted(wanted):
            write(OUT / "comparison-cards" / (ch + ".md"), git("show", f"{PARENT}:kanji/{ch}.md"))
        reused = {}
        for name in [
            "source-receipt.json", "source-row.json", "jmdict-selected-records.xml",
            "complete-source-verification-002.json", "baseline-gloss-scan.json",
            "baseline-gloss-scan-002.json", "pair-dispositions.json", "external-source-bindings.json",
            "packet-files-002.json", "stroke-font-evidence.json",
        ]:
            reused["batch-127/" + name] = binding(PACKET / name)
        snapshots = ROOT / "review-packets" / "batch-127-fcf8cb48" / "evidence" / "external-snapshots"
        external = {p.name: binding(p) for p in sorted(snapshots.iterdir()) if p.is_file()}
        write(OUT / "source-receipt.json", {
            "batch": "127", "revision": "reconciliation-001", "parent": PARENT,
            "publishedBase": "dd45f6fb7cd3ce579422e2333860aa6d245af898",
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "admissionBindings": bindings, "dictionaryInputs": source_digests,
            "selector": "Exact equality of any k_ele/keb to a listed query. Union complete entries, in source order; never filter by reading, sense, register, priority or preferred spelling.",
            "selectors": {qid: {"character": ch, "exactKebQueries": terms, "entryIds": sorted({eid for term in terms for eid in memberships[term]})} for qid, (ch, terms) in CLAIMS.items()},
            "exactQueryMembership": memberships, "zeroMatchQueries": [term for term, ids in memberships.items() if not ids],
            "kanjidicSelector": sorted(wanted), "outputs": outputs,
            "completeRecordVerification": "Every selected original canonical record hash equals its reserialized complete output. Input streams and compressed inputs hashed fully; full equality selectors evaluated over every entry.",
            "reusedImmutableEvidence": reused, "reusedExternalSnapshots": external,
            "externalPolicy": "No new captures. Complete external responses/extracts stay local. See original capture manifests for URLs/timestamps; only original summaries and short attributed quotations are committed.",
            "attribution": "JMdict/KANJIDIC2: Copyright James William Breen and EDRDG, CC BY-SA 4.0.",
            "producerSha256": sha(Path(__file__).read_bytes()), "guardSha256": GUARD_SHA,
        })
        print(json.dumps({"parent": PARENT, "records": {k: len(v) for k, v in selected.items()}, "memberships": memberships, "readback": str(ATTEMPT / "complete-record-readback.txt")}, ensure_ascii=False))
    finally:
        write(ATTEMPT / "memory.json", guard.finish())


if __name__ == "__main__":
    main()
