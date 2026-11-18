import copy
import json
import re
from pathlib import Path

from common_134 import HERE, INPUTS, REPO, canonical, git, normalized, records, sha, start_guard, write, xml_output

CANDIDATE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
OUT = HERE / "reconciliation-sources-001"
CHARS = "絹衣服書誌紀詞層列段階冠根殿隻紅紺青町薬典料糸維綿妻花油被系濃薄稲久館包"
EXTRA = {"紫", "紫衣", "紫闥", "紫宸殿", "紫禁", "紫紺", "青紫", "紅紫",
         "赤紫", "紫根", "検校", "江戸", "源氏物語", "紫式部", "紅絹", "絹布",
         "布帛", "紫草", "醤油", "鰯"}
READINGS = {"きぬ", "ふみ", "もみ", "め", "わた", "せき"}


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == CANDIDATE
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        chars = sorted(set(CHARS))
        exact = set(chars) | EXTRA
        cards = {}
        for ch in chars:
            raw = git("show", f"{CANDIDATE}:kanji/{ch}.md")
            text = raw.replace(b"\r\n", b"\n").decode("utf-8")
            assert (REPO / "kanji" / (ch + ".md")).read_bytes() == raw
            linked = sorted(set(re.findall(r"\]\(\.\./words/([^/)]+)\.md\)", text)))
            exact.update(linked)
            cards[ch] = {"title": re.search(r"^title: (.+)$", text, re.M).group(1),
                         "sha256": sha(raw), "linkedWords": linked,
                         "existingExclusions": re.search(r"^quiz_exclusions: (.+)$", text, re.M).group(1)
                         if re.search(r"^quiz_exclusions: (.+)$", text, re.M) else None}
            write(OUT / "comparison-cards" / (ch + ".md"), raw)
        counts = {f"exact-spelling:{s}": 0 for s in sorted(exact)}
        counts.update({f"exact-reading:{r}": 0 for r in sorted(READINGS)})
        selected, membership = [], {}
        for n in records("jmdict", guard):
            spellings = {x.text for x in n.findall("k_ele/keb")}
            readings = {x.text for x in n.findall("r_ele/reb")}
            predicates = [f"exact-spelling:{s}" for s in sorted(spellings & exact)]
            predicates += [f"exact-reading:{r}" for r in sorted(readings & READINGS)]
            if predicates:
                selected.append(copy.deepcopy(n))
                membership[n.findtext("ent_seq")] = predicates
                for p in predicates:
                    counts[p] += 1
        kd = {}
        for n in records("kanjidic2", guard):
            ch = n.findtext("literal")
            if ch in chars or ch == "紫":
                assert ch not in kd
                kd[ch] = copy.deepcopy(n)
        assert set(kd) == set(chars) | {"紫"}
        write(OUT / "comparison-index.json", cards)
        write(OUT / "query-membership.json", membership)
        outputs = {
            "jmdict-complete-families.xml": xml_output(OUT / "jmdict-complete-families.xml", "JMdict", selected),
            "kanjidic2-complete-characters.xml": xml_output(OUT / "kanjidic2-complete-characters.xml", "kanjidic2", [kd[c] for c in sorted(kd)]),
        }
        old = json.loads((REPO / "docs" / "n1-sources" / "batch-134" / "source-receipt.json").read_bytes())
        equality = {}
        for name, old_info in old["outputs"].items():
            new_name = "jmdict-complete-families.xml" if name.startswith("jmdict") else "kanjidic2-complete-characters.xml"
            for key, digest in old_info["canonicalRecordHashes"].items():
                if key in outputs[new_name]["canonicalRecordHashes"]:
                    assert outputs[new_name]["canonicalRecordHashes"][key] == digest, key
                    equality[key] = digest
        write(OUT / "receipt.json", {
            "candidate": CANDIDATE, "inputs": INPUTS, "exactSpellings": sorted(exact),
            "exactReadings": sorted(READINGS), "comparisonCharacters": chars,
            "predicate": "Union of complete families with any exact spelling equal to a comparison character, its linked word, or explicitly listed target/source-driven spelling, OR exact reading among the six kana forms. No priority, usage, sense, register, spelling restriction or age filter.",
            "countsIncludingZero": counts, "membershipSha256": sha((OUT / "query-membership.json").read_bytes()),
            "comparisonIndexSha256": sha((OUT / "comparison-index.json").read_bytes()), "outputs": outputs,
            "originalPacketCanonicalEquality": equality,
            "transformation": "Complete parsed/reserialized records, not raw source slices; all original record fields retained.",
            "attribution": "JMdict/KANJIDIC2: copyright James William Breen and EDRDG, CC BY-SA 4.0.",
            "producerSha256": sha(Path(__file__).read_bytes())})
        print(json.dumps({"characters": len(kd), "families": len(selected), "zeroQueries": [k for k, v in counts.items() if not v], "equality": len(equality)}, ensure_ascii=False))
    finally:
        write(OUT / "memory.json", guard.finish())


if __name__ == "__main__":
    main()
