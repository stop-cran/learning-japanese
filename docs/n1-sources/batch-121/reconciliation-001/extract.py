import gzip
import hashlib
import json
import os
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(r"C:\Users\stop-\n1-kanji-workspace")
repo = root / "b121-worktree"
here = root / "scratch-121" / "reconciliation-001"
base = "b5302617bf4c7232bab5bcd1e76b8ae6b938bc3a"
assert os.environ["N1_REPO"] == str(repo)
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo).decode().strip() == base
sources = {
    "jmdict": (root / "control" / "inputs" / "n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d"),
    "kanjidic2": (root / "control" / "inputs" / "n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed"),
}
for path, expected in sources.values():
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != expected:
        raise ValueError(f"source hash mismatch: {path}")

chars = set("徳厚礼愛助援幸豊品訓授者偉性能格財師与給贈受拝儀資金宝優功富享人教待復徹徒律循")
queries = set("""
徳 道徳 徳行 徳利 得 得る 徳用 得用
厚 厚い 厚意 礼 礼儀 お礼 御礼 愛 愛する 愛情 愛徳
助ける 助かる 援助 応援 幸 幸せ 幸福 豊か 豊富
品 品性 品格 訓 訓える 教え 教える 授ける 授かる 者 人格
偉い 偉大 性 性質 性格 能 能力 才能 財 財産
師 教師 与える 給う 給 贈る 受ける 享受 拝む 儀 儀式 礼儀
資 資本 資金 金 お金 宝 宝物 宝石
優しい 優れる 功 功績 功徳 富 富む 享 人
待つ 復 復する 回復 復習 徹 徹する 徹底 徹夜 徒 徒歩 生徒
律 法律 循 循環
""".split())
out = {}
for name, tag, needles in (("jmdict", "entry", queries), ("kanjidic2", "character", chars)):
    doc = ET.Element("JMdict" if name == "jmdict" else "kanjidic2")
    with gzip.open(sources[name][0], "rb") as stream:
        parser = ET.iterparse(stream, events=("start", "end"))
        _, docroot = next(parser)
        for event, node in parser:
            if event != "end" or node.tag != tag:
                continue
            keys = {x.text for x in node.findall("k_ele/keb")} if name == "jmdict" else {node.findtext("literal")}
            if keys & needles:
                doc.append(node)
            else:
                node.clear()
            docroot.clear()
    ET.indent(doc, space="  ")
    raw = ET.tostring(doc, encoding="utf-8", xml_declaration=True) + b"\n"
    target = here / f"{name}-records.xml"
    with target.open("xb") as stream:
        stream.write(raw)
    found = [x.findtext("ent_seq") if name == "jmdict" else x.findtext("literal") for x in doc]
    if name == "kanjidic2" and set(found) != chars:
        raise ValueError(f"missing records: {chars-set(found)}")
    out[name] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "entries": found}

snapshots = here / "comparison-cards"
snapshots.mkdir(exist_ok=False)
for char in sorted(chars - {"徳"}):
    raw = subprocess.check_output(["git", "show", f"{base}:kanji/{char}.md"], cwd=repo)
    with (snapshots / f"{char}.md").open("xb") as stream:
        stream.write(raw)
absence = {}
for char in "善恵仁":
    result = subprocess.run(["git", "cat-file", "-e", f"{base}:kanji/{char}.md"], cwd=repo, capture_output=True)
    absence[char] = result.returncode != 0
assert all(absence.values())
print(json.dumps({"base": base, "inputSha256": {k: v[1] for k, v in sources.items()},
                  "queries": sorted(queries), "characters": sorted(chars), "result": out,
                  "absentCards": absence, "comparisonCount": len(chars)-1,
                  "limits": "Complete matching parsed entries reserialized, not original compressed byte slices."},
                 ensure_ascii=False, indent=2))
