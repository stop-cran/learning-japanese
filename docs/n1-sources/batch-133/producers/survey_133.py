import copy
import json
import re
from common_133 import BASE, HERE, REPO, ROOT, git, normalized, records, sha, start_guard, write, xml_output

CHARS = "嵐琴紫詩鉛矢滝"
OUT = HERE / "survey-001"


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        index_raw = git("show", f"{BASE}:docs/n1-sources/source-index.json")
        index = {r["kanji"]: r for r in json.loads(index_raw)}
        manifest_raw = git("show", f"{BASE}:manifest.json")
        manifest = json.loads(manifest_raw)
        supports = {c: [] for c in CHARS}
        for path in sorted((REPO / "words").glob("*.md")):
            text = normalized(path)
            match = re.search(r"^kanji: \[([^\]]*)\]$", text, re.M)
            if match:
                for c in CHARS:
                    if c in [p.strip() for p in match.group(1).split(",")]:
                        supports[c].append(path.stem)
        for c in CHARS:
            assert index[c]["statusAtFreeze"] == "pending" and index[c]["article"] not in manifest["files"]
            for w in supports[c]:
                write(OUT / "baseline-words" / (w + ".md"), git("show", f"{BASE}:words/{w}.md"))
        write(OUT / "membership.json", {"base": BASE, "sourceIndexSha256": sha(index_raw), "manifestSha256": sha(manifest_raw),
                                       "rows": [index[c] for c in CHARS], "supports": supports})
        kd = [copy.deepcopy(n) for n in records("kanjidic2", guard) if n.findtext("literal") in CHARS]
        families = []
        for n in records("jmdict", guard):
            if any(c in s.text for s in n.findall("k_ele/keb") for c in CHARS):
                families.append(copy.deepcopy(n))
        outputs = {
            "kanjidic2-targets.xml": xml_output(OUT / "kanjidic2-targets.xml", "kanjidic2", kd),
            "jmdict-target-families.xml": xml_output(OUT / "jmdict-target-families.xml", "JMdict", families),
        }
        write(OUT / "dictionary-receipt.json", {"base": BASE, "outputs": outputs,
              "predicate": "Union of complete families with any spelling containing 嵐琴紫詩鉛矢滝; complete target character records. No priority or sense filter. Parsed/reserialized XML, not raw slices."})
        captures = json.loads((ROOT / "scratch-132" / "survey-001" / "external-bindings.json").read_bytes())
        captures["captures"] = [c for c in captures["captures"] if c["character"] in CHARS]
        assert len(captures["captures"]) == 2 * len(CHARS)
        for item in captures["captures"]:
            assert "error" not in item
            raw = __import__("pathlib").Path(item["localRawCapture"])
            assert sha(raw.read_bytes()) == item["rawSha256"]
            assert sha(raw.with_suffix(".txt").read_bytes()) == item["textSha256"]
        write(OUT / "reused-capture-bindings.json", captures)
        print(json.dumps({"supports": supports, "families": len(families), "rows": [(c, index[c]["sourceRow"], index[c]["metadata"]) for c in CHARS]}, ensure_ascii=False))
    finally:
        write(OUT / "memory.json", guard.finish())


if __name__ == "__main__":
    main()
