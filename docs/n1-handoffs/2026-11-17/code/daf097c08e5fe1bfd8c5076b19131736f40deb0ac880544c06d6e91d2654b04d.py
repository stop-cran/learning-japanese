import importlib.util
import json
import re
import unicodedata
from pathlib import Path

from fontTools.ttLib import TTFont
from common_134 import BASE, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write

MEMBERSHIP = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\n1-published-membership-e17cb97c.json")


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert git("remote", "get-url", "origin").decode().strip() == "https://github.com/stop-cran/learning-japanese.git"
        assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
        membership = json.loads(MEMBERSHIP.read_bytes())
        assert membership["head"] == BASE and membership["counts"]["frozenPendingMembersPresent"] == 271
        assert membership["counts"]["undelivered"] == 957
        assert "紫" not in {r["kanji"] for r in membership["present"]}
        write(PACKET / "published-membership-binding.json", {
            "path": str(MEMBERSHIP), "sha256": sha(MEMBERSHIP.read_bytes()), "base": BASE,
            "counts": membership["counts"], "selectedMissing": ["紫"]})
        source = HERE / "source-002"
        for path in sorted(source.rglob("*")):
            if path.is_file():
                write(PACKET / path.relative_to(source), path.read_bytes())
        for path in sorted((HERE / "supplement-001").rglob("*")):
            if path.is_file():
                write(PACKET / "supplement" / path.relative_to(HERE / "supplement-001"), path.read_bytes())
        for name in ("common_134.py", "sources_134.py", "verify_sources_134.py", "sources_134_final.py",
                     "verify_sources_134_final.py", "inspect_comparisons_134.py", "supplement_134.py",
                     "generate_stroke_134.py", "make_pairs_134.py", "prepare_134.py",
                     "bounded_launch_134.py", "check_reading_134.py", "run_134_gates.py", "preserve_134.py"):
            write(PACKET / "producers" / name, (HERE / name).read_bytes())
        pairs = json.loads((HERE / "analysis-001" / "pair-dispositions.json").read_bytes())
        write(PACKET / "pair-dispositions.json", pairs)
        row = json.loads((source / "source-rows.json").read_bytes())[0]
        assert row["sourceRow"] == 831 and row["statusAtFreeze"] == "pending"
        spec = importlib.util.spec_from_file_location("converter_b134", REPO / "tools" / "generate_strokes.py")
        converter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(converter)
        converter_hash = sha((REPO / "tools" / "generate_strokes.py").read_bytes())
        assert converter_hash == "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
        svg = (source / "kanjivg" / "07d2b.svg").read_bytes()
        stroke = converter.convert("紫", svg.decode())
        assert stroke["strokeCount"] == row["metadata"]["strokes"]
        expected = (json.dumps(stroke, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
        assert (REPO / "strokes" / "紫.json").read_bytes() == expected
        receipt = json.loads((HERE / "stroke-001.json").read_bytes())
        assert receipt["strokeSha256"] == sha(expected) and receipt["svgSha256"] == sha(svg)
        comparisons = {p["pair"][1] for p in pairs["members"][0]["pairs"]}
        text = normalized(REPO / "kanji" / "紫.md") + normalized(REPO / "words" / "紫.md")
        glyphs = "".join(sorted(set(re.findall(r"[\u3400-\u9fff]", text)) | comparisons | set("紫茈此糸止比")))
        fonts = []
        for path in sorted((ROOT / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
            with TTFont(path) as font:
                cmap = font.getBestCmap()
                fonts.append({"filename": path.name, "sha256": sha(path.read_bytes()),
                              "coverage": {f"U+{ord(ch):04X}": ord(ch) in cmap for ch in glyphs}})
        assert len(fonts) == 3 and all(f["coverage"]["U+7D2B"] for f in fonts)
        write(PACKET / "stroke-font-evidence.json", {
            "members": [receipt], "converterSha256": converter_hash, "kanjivgRevision": converter.KANJIVG_REVISION,
            "fonts": fonts, "codePoints": [{"character": c, "codePoint": f"U+{ord(c):04X}",
                                              "unicodeName": unicodedata.name(c)} for c in glyphs],
            "scope": "Han in final target/support articles, finite comparison cards' identities, and named radical/component/variant codepoints.",
            "limits": "Bounded actual bundled font cmaps only; not rendered/visual/native/device/fallback acceptance."})
        write(PACKET / "selection.json", {
            "batch": 134, "base": BASE, "members": ["紫"], "sourceRows": [831], "supports": [["紫", "紫"]],
            "publishedDelivered": 271, "undelivered": 957, "localDrafts": 1,
            "deliveryNotIncremented": True, "proseException": None,
            "split": "One member because its full native secondary-sense, source discrepancy and comparison packet requires an independently reviewable bounded source packet; no fixed batch-size quota.",
            "notSelected": {
                "伯": "row 33 deferred; 伯母さん does not establish ハク.",
                "憶": "row 395 deferred.", "撲": "row 461 deferred; 相撲 does not establish ボク.",
                "皇": "B131 unresolved native/prefix/secondary senses remain separate.",
                "桜": "B131 native secondary senses remain separate.",
                "詩": "Separate source packet; not authorized by survey ranking alone.",
                "嵐": "Separate source packet; not authorized by survey ranking alone.",
                "矢": "Separate source packet; not authorized by survey ranking alone."}})
        write(PACKET / "authored-source-analysis.json", {
            "base": BASE,
            "members": {"紫": {
                "practice": {"on": [], "kun": ["むらさき"]}, "support": "紫 at N2",
                "readingDisposition": "Full ordered シ/むらさき metadata; linked むらさき practice only. 紫外線 supports compound シ recognition; ゆかり and さい are KANJIDIC2 nanori, historical ツツム remains uncertain. 紫陽花 あじさい is whole-word jukujikun, not an independent 紫 reading. All five keys deliberately tested in bounded host model.",
                "positiveSecondary": "JMdict 1311640 color, purple gromwell and soy sauce; complete native source adds colored paper or cloth, sardine, woman, 検校 and specific Edo, Murasaki Shikibu and The Tale of Genji abbreviations. The literary ゆかり relationship is a contextual association, not unconditional lexical synonymy.",
                "restrictions": "Complete family 1311640 marks gromwell usually kana; 茈 is a search-only form. Full sense and spelling/read restrictions remain in the retained complete records. Compounds such as 紫陽花 are not reallocated as bare-character readings.",
                "variants": "Complete exact 茈, 紫, 此, 糸, 止 and 比 KANJIDIC2 records retained; contains:茈 returns one complete family.",
                "discrepancies": "KANJIDIC2 and pinned KanjiVG specify 12 strokes, whereas 字通 capture labels 紫 11; do not reconcile by changing source metadata or geometry.",
                "comparison": "50 expanded baseline scan hits and three curated distinct distractors, evaluated in both directions. Direct exclusions are symmetric and non-transitive; broad precautions are not universal synonyms."}},
            "externalCaptures": "Reused B132 survey captures with exact raw/text hashes; full captures stay local.",
            "limits": "Author assessment only, finite scan, not independent review or publication acceptance."})
        snippets = {
            "kotobank": ["紫色。また、その色の紙や布。", "常用漢字 11画",
                         "2. 美しく神聖なものに用いる。", "〔名義抄〕紫　ムラサキ・ツツム",
                         "」から ) 江戸をいう。", "「源氏物語」をいう。"],
            "weblio": [],
        }
        excerpts = []
        for item in json.loads((source / "external-capture-bindings.json").read_bytes())["captures"]:
            raw = Path(item["localRawCapture"])
            text = raw.with_suffix(".txt").read_text(encoding="utf-8")
            assert sha(raw.read_bytes()) == item["rawSha256"] and sha(raw.with_suffix(".txt").read_bytes()) == item["textSha256"]
            quoted = []
            for snippet in snippets[item["provider"]]:
                assert snippet in text, snippet
                offset = text.index(snippet)
                quoted.append({"text": snippet, "line": text[:offset].count("\n") + 1})
            excerpts.append({"character": "紫", "provider": item["provider"], "url": item["finalUrl"],
                             "textSha256": item["textSha256"], "excerpts": quoted})
        write(PACKET / "bounded-excerpts.json", {
            "attribution": "Kotobank: Shogakukan Digital Daijisen/日本国語大辞典 and Heibonsha 字通; Weblio: attributed constituent dictionaries.",
            "captures": excerpts, "limits": "Short attributable quotations only. Full captures local; empty excerpts do not mean a page was absent."})
        history = {}
        for directory in ("source-001", "source-002", "supplement-001", "analysis-001"):
            for path in sorted((HERE / directory).rglob("*")):
                if path.is_file():
                    history[str(path.relative_to(HERE)).replace("\\", "/")] = sha(path.read_bytes())
        for name in ("reading-preflight-001.log", "stroke-001.json", "supplement-attempt-001.stdout",
                     "supplement-attempt-001.stderr", "pairs-attempt-001.stdout", "pairs-attempt-001.stderr"):
            path = HERE / name
            history[name] = sha(path.read_bytes())
        write(PACKET / "local-history-bindings.json", {"directory": str(HERE), "files": history,
              "limits": "Earlier attempts and reused full captures remain local and unaltered; coordinator review directory not touched."})
        print(json.dumps({"pairs": len(pairs["members"][0]["pairs"]),
                          "fontMisses": {f["filename"]: [k for k, v in f["coverage"].items() if not v] for f in fonts}},
                         ensure_ascii=False))
    finally:
        write(HERE / "preparation-memory-001.json", guard.finish())


if __name__ == "__main__":
    main()
