import hashlib
import importlib.util
import json
import re
import unicodedata
from pathlib import Path

from fontTools.ttLib import TTFont
from common_132 import BASE, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write

SOURCE = HERE / "source-003"
CH = "墓"
PAIRS = {
    "暮": ("curated", "Dusk, season-end, livelihood, living and sinking into despair do not denote a grave or tomb; a grave likewise is not the time of dusk or a livelihood. Death associations do not equate these displayed labels."),
    "募": ("curated", "Recruitment, solicitation and increasing intensity do not denote a grave or tomb, and a grave is neither recruitment nor solicitation. Similar modern shapes and shared ボ do not establish synonymy."),
    "川": ("curated", "A river or stream is not a grave or tomb; a grave is not a river. Proximity of burial sites to water is an association, not lexical identity."),
    "埋": ("guard", "Burying or covering is an action, whereas a grave is a place or structure; burial overlap warrants a conservative direct precaution without equating every act of filling or burying with a tomb."),
    "石": ("guard", "日本国語大辞典 includes grave markers and gravestones in はか; a gravestone is a stone, but not every stone, jewel, game piece or calculus is a grave. This is a conservative direct broad-label precaution."),
    "相": ("distinct", "KANJIDIC2's inter- means mutual or between, not the English verb inter meaning bury. Aspect, phase, minister, nature and alternating do not mean a grave; a grave does not mean mutual or aspect."),
}


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        scan = json.loads((SOURCE / "scans" / (CH + ".json")).read_bytes())
        assert set(scan["matches"]) <= PAIRS.keys()
        source_files = [
            "source-rows.json", "source-receipt.json", "query-membership.json", "reading-keys.json",
            "independent-source-verification.json", "jmdict-complete-families.xml",
            "kanjidic2-targets.xml", "kanjidic2-comparisons.xml", "external-capture-bindings.json",
            "supplemental-query-membership.json", "supplemental-source-receipt.json", "supplemental-verification.json",
            "jmdict-supplemental-families.xml", "kanjivg/05893.svg", "scans/墓.json", "baseline-words/墓.md",
        ]
        source_files += [f"comparison-cards/{c}.md" for c in sorted(PAIRS)]
        for name in source_files:
            write(PACKET / name, (SOURCE / name).read_bytes())
        producers = ["common_132.py", "survey_132.py", "sources_132.py", "sources_132_visual.py",
                     "verify_sources_132.py", "verify_sources_132_visual.py", "supplement_132.py", "verify_supplement_132.py",
                     "prepare_132.py"]
        for name in producers:
            write(PACKET / "producers" / name, (HERE / name).read_bytes())
        for name in ("memory.json", "verification-memory.json", "supplement-memory.json", "supplement-verification-memory.json"):
            write(PACKET / "author-evidence" / name, (SOURCE / name).read_bytes())
        row = json.loads((SOURCE / "source-rows.json").read_bytes())[0]
        svg = (SOURCE / "kanjivg" / "05893.svg").read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(svg)).encode() + b"\0" + svg).hexdigest()
        assert blob == row["kanjivgInventory"]["sha"]
        converter_path = REPO / "tools" / "generate_strokes.py"
        assert sha(converter_path.read_bytes()) == "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
        spec = importlib.util.spec_from_file_location("converter_b132", converter_path)
        converter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(converter)
        strokes = converter.convert(CH, svg.decode("utf-8"))
        assert strokes["strokeCount"] == row["metadata"]["strokes"] == 13
        stroke_raw = (json.dumps(strokes, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
        write(REPO / "strokes" / (CH + ".json"), stroke_raw)
        text = normalized(REPO / "kanji" / (CH + ".md")) + normalized(REPO / "words" / (CH + ".md"))
        glyphs = "".join(sorted(set(re.findall(r"[\u3400-\u9fff]", text)) | set(PAIRS) | set("墓莫土")))
        fonts = []
        for path in sorted((ROOT / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
            guard.check()
            with TTFont(path) as font:
                cmap = font.getBestCmap()
                fonts.append({"filename": path.name, "sha256": sha(path.read_bytes()),
                              "coverage": {f"U+{ord(ch):04X}": ord(ch) in cmap for ch in glyphs}})
        assert len(fonts) == 3
        font_record = {
            "members": [{"kanji": CH, "strokeCount": 13, "strokeSha256": sha(stroke_raw), "svgSha256": sha(svg), "kanjivgBlob": blob}],
            "converterSha256": sha(converter_path.read_bytes()), "kanjivgRevision": converter.KANJIVG_REVISION,
            "fonts": fonts, "codePoints": [{"character": c, "codePoint": f"U+{ord(c):04X}", "unicodeName": unicodedata.name(c)} for c in glyphs],
            "scope": "Han in final target card and support article plus finite comparisons and named modern components/radical, actual bundled font cmaps only.",
            "limits": "Cmap membership is not visual, native/device, or rendered fallback acceptance.",
            "producerSha256": sha(Path(__file__).read_bytes())}
        write(PACKET / "stroke-font-evidence.json", font_record)
        pairs = []
        for other, (decision, reason) in PAIRS.items():
            path = SOURCE / "comparison-cards" / (other + ".md")
            raw = path.read_bytes()
            assert raw == git("show", f"{BASE}:kanji/{other}.md")
            title = re.search(r"^title: (.+)$", raw.replace(b"\r\n", b"\n").decode(), re.M).group(1)
            pairs.append({"pair": [CH, other], "comparisonTitle": title, "decision": decision,
                          "comparisonLabelOnTarget": f"Considered {title!r} against 墓's complete qualified sense range. {reason}",
                          "targetLabelOnComparison": f"Considered 'grave; tomb' against {other}'s full actual card and sourced range. {reason}",
                          "baselineCardSha256": sha(raw), "scanMatch": other in scan["matches"],
                          "readbackSha256": sha((SOURCE / "comparison-readback" / (other + ".json")).read_bytes())})
        write(PACKET / "pair-dispositions.json", {
            "base": BASE, "members": [{"kanji": CH, "targetTitle": "grave; tomb", "scanRows": len(scan["rows"]), "pairs": pairs}],
            "rule": "Direct symmetric pairs only; no transitive closure. Precautions protect against unresolved broad labels, not universal synonymy.",
            "readCoverage": "All six actual comparison cards, complete KANJIDIC2 records, exact-spelling JMdict families, and supplemental actual-comparison vocabulary families inspected. Full target-containing 53 complete families and actual support article inspected.",
            "limits": "Finite scan and comparison scope, not exhaustive synonym discovery or independent linguistic review.",
            "producerSha256": sha(Path(__file__).read_bytes())})
        write(PACKET / "selection.json", {
            "batch": 132, "base": BASE, "members": [CH], "sourceRows": [197], "supports": [[CH, CH]],
            "deliveredAtBase": 267, "undeliveredAtBase": 961, "deliveryNotIncremented": True,
            "reason": "Split after the two-member source packet required 34 actual comparisons and approximately 500 KB of complete readbacks before supplemental queries; this one-member packet enables bounded independent review.",
            "notSelected": {"嵐": "Deferred: positive mountain mist, violent weather, figurative disturbance and supplemental/name readings need their full 28-match comparison review.",
                            "琴": "Deferred: positive 字通 Chu-language mound sense overlaps 墓; not assumed distinct.",
                            "紫": "Deferred: multiple native secondary senses and stroke-count discrepancy require separate adjudication.",
                            "詩": "Deferred: aesthetic and supplemental character senses require separate adjudication.",
                            "鉛": "Deferred: counterfeit-money and cosmetic senses require separate adjudication.",
                            "矢": "Deferred: positive wedge, oath, arranging and excrement senses, plus stale support sentence, require separate adjudication.",
                            "滝": "Deferred: rapids, water abbreviation and supplemental wet/moisten readings require separate adjudication."},
            "previousDeferrals": {"皇": "Separate native/prefix and secondary-sense packet.", "桜": "Separate native and secondary-sense packet.", "伯": "row 33; 伯母さん does not establish ハク.", "憶": "row 395; unresolved remember/think evidence.", "撲": "row 461; 相撲 does not establish ボク."},
            "proseException": None})
        write(PACKET / "authored-source-analysis.json", {
            "base": BASE, "kanji": CH, "support": "墓", "sourceRow": 197,
            "metadata": {"on": ["ボ"], "kun": ["はか"], "radical": "土", "radicalNumber": 32, "strokes": 13},
            "practice": {"on": [], "kun": ["はか"]},
            "readingDisposition": "JMdict 1514840 supplies the linked はか; 1504630 ふんぼ supplies recognition for ボ, not a linked practice slot. Weblio/Wiktionary adds モ; 字通 adds おくつき and records old dictionary ツカ・ムハフ・ハカ・クサ. All explicit positive forms are supplied to the bounded host check, without asserting they are ordinary modern readings.",
            "positiveSecondary": "日本国語大辞典 standalone はか includes grave markers and gravestones, while ぼ includes a narrower imperial-family burial place. 字通 adds grave precincts. No generalized burial method is imposed.",
            "restrictions": "浅墓 is marked rare ateji in complete JMdict family 1609030. Its shallow/thoughtless senses belong to the whole word, not automatically to 墓.",
            "sourceDiscrepancy": "字通 shows historical glyphs as missing images in extracted text; their forms are not reconstructed or used as a claim about etymology.",
            "semanticDisposition": "Six finite bidirectional comparisons, including qualified direct 埋 and 石 precautions. 暮's living/dusk and 募's gathering/stronger senses remain distinct despite visual overlap.",
            "externalCapture": "Complete raw captures remain local and are bound by external-capture-bindings.json; no full third-party webpage is committed.",
            "limits": "No independent review, arbitrary-pool, native/device, rendered fallback, whole-set or publication acceptance."})
        history = {}
        for name in ("survey-001/membership.json", "survey-001/dictionary-receipt.json", "survey-001/verification-001.json",
                     "survey-001/external-bindings.json", "source-001/source-receipt.json", "source-002/source-receipt.json"):
            path = HERE / name
            history[name] = sha(path.read_bytes())
        write(PACKET / "local-history-bindings.json", {
            "directory": str(HERE), "files": history,
            "limits": "survey-001 ran two git probes using subprocess.run(timeout=10), not the prescribed <=0.1s child-wait loop; no guard breach was observed. Later source packets use the bounded child-wait helper. Historical outputs and original source-001 producer preserved; complete external captures remain local."})
        print(json.dumps({"stroke": sha(stroke_raw), "comparisons": len(pairs),
                          "missingFonts": {f["filename"]: [k for k, v in f["coverage"].items() if not v] for f in fonts}}, ensure_ascii=False))
    finally:
        write(HERE / "preparation-memory-001.json", guard.finish())


if __name__ == "__main__":
    main()
