import copy
import gzip
import hashlib
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from recon_common import *
from extract_b129 import HashReader, INPUTS, PageText, canonical

FROZEN = {
    ROOT / "reports-129" / "initial-claude-001.md": "70884d9a68aa150e61db692a8d68babf4dc80c287cdfa82261b63efe00522049",
    ROOT / "reports-129" / "initial-gpt-001.md": "3c28f2bffefde633e39ed07eaad713e0dbb128727a8e6b968e6a00abdab47c84",
    AUTHOR / "review" / "N1-B129-CLAUDE-001-adjudication.json": "50c581ddc63afea8e23d1e5bb6df04a9726212bb6eaf25f67b9712df403f89b4",
    AUTHOR / "review" / "N1-B129-GPT-001-adjudication.json": "ed55cd42a4dd8312b3685c685808bc7752ad1bb72583b2c226dc822b87177b0f",
    AUTHOR / "review" / "reconciliation-001-admission.json": "5e9533cf48b59789c405816d5bf0255e1f4f1a12b625bc7b55242f3d8f2a6038",
    AUTHOR / "review" / "N1-B129-CLAUDE-001-citation-erratum.json": "cb67d51517dca32ace7a731c5f437d6fea7713fe9bf4fecd6deeccaec4df05bd",
    AUTHOR / "review" / "reading-check-supplemental-gu-derivation-001.json": "d471bfcfa3770ad6ddb8e02928c7db27c2a3e4c91286e209c4622734cb300045",
    AUTHOR / "review" / "supplemental-gu-execution-001" / "receipt.json": "61c84296e5dd718a1586856c1146f6fad2516c13b606d39ff277e930a55fc37e",
    AUTHOR / "review" / "supplemental-gu-execution-001" / "output.log": "a9b3b60c06762b1164f4cef54b0d4653e572212c75a75a22d1c7b620b34904f1",
}
EXACT = set("".join("".join(v) for v in PAIRS.values()))
EXACT.update("絹 虹 絡む 絡まる 絡める 線 索 緒 結ぶ 結う 結わえる 括る 括れる 容れる 缶 罐 対する 抵抗 責める 攻める 争う 乱れる 羂 羂る 油皿 訌 議論 談ずる 談じる 撃つ 騒ぐ 騒ぎ 動く 動かす 罪 圧す 圧さえる 抗う 反る 曲がる 曲げる 器 皿".split())
READINGS = set("からむ からまる からめる さく お いとぐち せん すじ むすぶ ゆう ゆわえる くくる くびれる いる いれる かん かま つい たい せめる あらそう みだれる わな あぶらざら ぐ".split())

guard = start_guard()
try:
    assert not PACKET.exists()
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    assert git("remote", "get-url", "origin").decode().strip() == "https://github.com/stop-cran/learning-japanese.git"
    assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
    assert git("config", "user.signingkey").decode().strip() == "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
    assert not git("ls-tree", "-r", "--name-only", PARENT, "--", "kanji/網.md")
    frozen = []
    for path, digest in FROZEN.items():
        assert sha(path.read_bytes()) == digest, path
        frozen.append({"path": str(path), "sha256": digest, "bytes": path.stat().st_size})
    write(PACKET / "frozen-input-bindings.json", {
        "parent": PARENT, "originalBase": BASE, "inputs": frozen,
        "D4": {"path": "kanji/網.md", "gitLsTreeMatches": [], "disposition": "Absent; no fabricated read or new card."},
        "supplementaryQualification": "The citation erratum and gu execution are coordinator supplements. Neither initial reviewer read the gu supplement. The initial reading log omitted グ.",
    })
    ids = set()
    comparison_rows = []
    for target, comparisons in PAIRS.items():
        for ch in comparisons:
            rel = f"kanji/{ch}.md"
            data = git("show", f"{PARENT}:{rel}")
            assert (REPO / rel).read_bytes() == data
            text = data.replace(b"\r\n", b"\n").decode()
            write(PACKET / "comparison-cards" / f"{ch}.md", data)
            ids.update(re.findall(r"\b\d{7}\b", text))
            comparison_rows.append({"pair": [target, ch], "path": rel, "rawSha256": sha(data),
                                    "title": re.search(r"^title: (.+)$", text, re.M).group(1)})
    write(PACKET / "comparison-bindings.json", comparison_rows)
    receipts, selected = {}, {}
    for source, (filename, compressed, decompressed, tag) in INPUTS.items():
        path = ROOT / "control" / "inputs" / filename
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(65536), b""):
                guard.check()
                digest.update(chunk)
        assert digest.hexdigest() == compressed
        nodes, hashes, memberships = {}, {}, {}
        queries = {}
        if source == "jmdict":
            queries = {f"exact-spelling:{x}": [] for x in sorted(EXACT)}
            queries.update({f"exact-reading:{x}": [] for x in sorted(READINGS)})
            queries.update({f"entry-id-cited-by-actual-comparison:{x}": [] for x in sorted(ids)})
        else:
            queries = {f"literal:{x}": [] for x in sorted(EXACT) if len(x) == 1}
        with gzip.open(path, "rb") as stream:
            reader = HashReader(stream, guard)
            context = ET.iterparse(reader, events=("start", "end"))
            _, root = next(context)
            for event, node in context:
                if event != "end" or node.tag != tag:
                    continue
                if source == "jmdict":
                    key = node.findtext("ent_seq")
                    kebs = {n.text for n in node.findall("k_ele/keb")}
                    rebs = {n.text for n in node.findall("r_ele/reb")}
                    predicates = [f"exact-spelling:{x}" for x in sorted(EXACT & kebs)]
                    predicates += [f"exact-reading:{x}" for x in sorted(READINGS & rebs)]
                    if key in ids:
                        predicates.append(f"entry-id-cited-by-actual-comparison:{key}")
                else:
                    key = node.findtext("literal")
                    predicates = [f"literal:{key}"] if f"literal:{key}" in queries else []
                if predicates:
                    nodes[key] = copy.deepcopy(node)
                    hashes[key] = sha(canonical(node).encode())
                    memberships[key] = predicates
                    for predicate in predicates:
                        queries[predicate].append(key)
                node.clear()
                root.clear()
        assert reader.digest.hexdigest() == decompressed
        xml = ET.Element("JMdict" if source == "jmdict" else "kanjidic2")
        xml.extend(nodes.values())
        ET.indent(xml, space="  ")
        raw = ET.tostring(xml, encoding="utf-8", xml_declaration=True) + b"\n"
        actual = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
        assert actual == hashes
        name = f"{source}-complete-records.xml"
        write(PACKET / name, raw)
        write(PACKET / f"{source}-query-membership.json", {"queries": queries, "recordPredicates": memberships,
                                                         "zeroMatches": [q for q, values in queries.items() if not values]})
        receipts[source] = {
            "input": {"path": str(path), "compressedSha256": compressed, "decompressedSha256": decompressed},
            "output": {"path": name, "sha256": sha(raw), "bytes": len(raw), "canonicalRecordHashes": hashes},
            "predicate": "Union of all exact spellings, exact readings and explicit entry IDs cited by the 28 actual comparison cards; no substring, priority, age, frequency, language or sense filter." if source == "jmdict" else "Complete records for the exact literal queries.",
            "completeCanonicalEquality": True, "transformation": "Complete parsed/reserialized XML records, not raw source slices.",
            "selectionCounts": {"records": len(nodes), "queries": len(queries), "zeroMatchQueries": sum(not v for v in queries.values())},
        }
        selected[source] = nodes
    write(PACKET / "complete-source-receipt.json", {"parent": PARENT, "sources": receipts,
                                                   "producerSha256": sha(Path(__file__).read_bytes())})
    readback = []
    for target, comparisons in PAIRS.items():
        for ch in comparisons:
            kd = selected["kanjidic2"][ch]
            readback.append(f"\n===== {target}/{ch}: COMPLETE KANJIDIC2 =====\n" + ET.tostring(kd, encoding="unicode"))
    for eid, node in selected["jmdict"].items():
        readback.append(f"\n===== COMPLETE JMdict {eid} =====\n" + ET.tostring(node, encoding="unicode"))
    write(HERE / "complete-source-readback.txt", "\n".join(readback).encode())
    print(json.dumps({"completeSources": receipts, "next": "Fetch finite monolingual comparisons separately."}, ensure_ascii=False))
finally:
    write(HERE / "source-memory-001.json", guard.finish())
