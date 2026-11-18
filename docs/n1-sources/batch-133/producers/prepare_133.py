import hashlib
import importlib.util
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from fontTools.ttLib import TTFont
from common_133 import BASE, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write

CHARS = "琴鉛滝"
SUPPORTS = {"琴": "琴", "鉛": "鉛筆", "滝": "滝"}
CURATED = {"琴": "古右川", "鉛": "古右川", "滝": "古右寺"}
GUARDS = {"琴": "器械墓丘曲楽整調", "鉛": "両厚末札粉素財貨重量金鈍顔銀", "滝": "川急水河注流湿落降雨音響騒鳴"}
REASONS = {
    "琴": {
        "亭": "A pavilion, restaurant or music-hall building is not the instrument played there; a zither is not a building.",
        "器": "Broad device/instrument labels include a musical instrument. Conservative direct broad-label precaution, not every vessel or ability being a zither.",
        "墓": "字通 positively gives the Chu-language 冢/塚 sense. A tomb label is unsafe despite the modern musical focus; not claimed ordinary modern Japanese equivalence.",
        "官": "Organ in the complete character meanings is anatomical/official, not the English musical organ in 風琴; government and officials are not zithers.",
        "張": "Tension, stretching, a counter for stringed instruments and a constellation are not the counted instrument itself.",
        "拍": "A beat, mora, clap or strike is not a zither; an instrument can produce beats without naming the unit or act.",
        "整": "Full source meanings include tune/tone/music key. Direct precaution for unresolved musical labels, not every adjustment or ordering being an instrument.",
        "曲": "Music/melody/composition labels warrant a qualified precaution; a musical piece is not universally identical to the instrument.",
        "械": "Complete character meanings include instrument; precaution for that broad label, not every shackle or machine being a zither.",
        "楽": "Music labels warrant a qualified direct precaution; music, comfort and pleasure are not universally interchangeable with a koto.",
        "管": "管's instrument sense is specifically wind instrument. Bare 琴's sourced string-instrument range is different; compound 風琴=organ is not proof bare 琴=every wind instrument.",
        "調": "Tuning, musical key/mode/rhythm labels warrant a qualified direct precaution; investigating and tax-in-kind do not all mean a zither.",
        "丘": "The source-positive burial-mound sense merits a conservative mound/hill precaution. Complete 丘 family 2251090 explicitly has mound; not every hill is a tomb.",
    },
    "鉛": {
        "両": "Full family includes currency and weight units. Qualified precaution for source-positive counterfeit-money/heaviness labels, not all ryō being counterfeit.",
        "似": "Resembling/imitating is not the noun counterfeit money. Resemblance alone does not establish a shared material or monetary meaning.",
        "冒": "Face/brave/risk are actions, not face powder; assume a surname and chemical harm do not make the subject the metal.",
        "厚": "Complete character meanings include heavy. Conservative unresolved heavy-label precaution, not all thick/kind things being lead.",
        "向": "Facing/toward and a facing direction are not cosmetic powder, money or metal.",
        "対": "Facing/opposition/pairing is not the substance applied to a face, counterfeit money or metal.",
        "帰": "The English verbal 'lead to' is not the metal lead; return, homecoming and results are distinct.",
        "息": "Breath, son and interest on money are not counterfeit money or lead; monetary association is not identity.",
        "悪": "False/bad/evil describes evaluation, not specifically counterfeit money; no automatic equivalence between a false thing and every money/material noun.",
        "押": "Push/press/seal/subdue is not the metal or cosmetic; physical pressure from a heavy object is only association.",
        "末": "Complete family 1525260 includes powder as a suffix. Direct powder-label precaution despite displayed end/tip.",
        "札": "Full banknote/money sense motivates conservative counterfeit-money protection; not all notes or labels are counterfeit.",
        "率": "Lead as a guiding verb is an English homograph, not Pb; rate/proportion/frankness do not name lead.",
        "督": "Supervision/command/lead as a verb is not the metal or powder; no material sense established.",
        "粉": "Complete powder sense overlaps character-source face powder. Not every flour, dust or heroin sense is lead.",
        "素": "Actual card includes chemical element/material; conservative broad element-label protection, not every principle, nature or plain thing being Pb.",
        "財": "Money/property/wealth labels receive a conservative counterfeit-money precaution; not every possession is fake money.",
        "貨": "Currency/money labels receive a direct precaution; treasure and every traded good are not thereby counterfeit.",
        "連": "Lead/take along are guiding/accompanying, not metal lead; stanza, tribe, party, title and counters add no monetary/material identity.",
        "重": "Heavy/slow/serious range intersects standalone なまり's heavy/dull comparison. Direct precaution, not every layer or seriousness being lead.",
        "量": "Weight/weigh/quantity labels receive conservative unresolved heaviness protection; not every volume or generosity being lead.",
        "金": "Full native families give metal and money, beyond KD's gold. Direct protection for elemental lead and counterfeit-money senses, not universal synonymy.",
        "鈍": "Dull/sluggish/slow directly intersects the positive native-word heavy/dull range; not every blunt blade being Pb.",
        "面": "Face, surface, mask, aspect and page do not independently name cosmetics in the complete captured families; distinguish 顔's actual makeup sense.",
        "顔": "Complete native family 1217730 sense 7 gives makeup/cosmetics. Powder overlap is lexical evidence, not merely application to a body part.",
        "化": "Transformation, enchantment and -ization do not denote the cosmetic material; 化粧's compound meaning cannot simply be assigned to bare 化.",
        "銀": "1595090 includes money and silver coin. Direct conservative counterfeit-money precaution; silver Ag and lead Pb remain different elements.",
        "白": "White, innocence, blank, game pieces, food and spoken lines do not independently mean face powder; white color alone is not the powder noun.",
        "筆": "Brush/pen/writing is not the metal. Whole 鉛筆 means pencil, not bare 鉛=every writing implement; 鉛槧's literature sense stays compound-wide.",
        "炭": "Charcoal, coal and charred remains differ from Pb and from graphite in 黒鉛; shared carbon association does not equate materials.",
    },
    "滝": {
        "倒": "Topple/collapse/reverse is not flowing waterfall/rapids; falling over is different from the water feature and sourced wet/rain-sound senses.",
        "凌": "Keep rain out/endure/surpass is not rain sound or a watercourse; relation to rain does not equate meanings.",
        "岩": "Rock/cliff is the landform beside or under water, not the waterfall or rapids itself.",
        "川": "Rapids are a river/current feature. Direct broad river-label precaution, not every stream being a waterfall.",
        "急": "Complete 急 family includes rapid and steep; precaution for unresolved rapid-label overlap, not every urgency or emergency being a waterfall.",
        "水": "Water/current and the source-positive 滝水 abbreviation warrant a direct water-label precaution; not every water or Wednesday sense being 滝.",
        "河": "Rapids/river range warrants a direct broad-label precaution; mahjong discards are separate.",
        "泉": "A spring/source or fountain is not a waterfall/rapid solely because it contains water; no source makes the origins identical.",
        "注": "Pouring/flowing water labels warrant a qualified precaution; annotation or explanatory notes do not mean waterfall.",
        "流": "Current/flow/stream overlaps rapids. Direct precaution, not every style, school, exile or flag counter being a waterfall.",
        "湯": "Hot water, bath, molten iron and soup do not require a waterfall. No source establishes bare 滝=hot water.",
        "湿": "Moisture/wet range intersects 字通's soaking/moistening. Direct precaution, not every humidity or scabies sense being a waterfall.",
        "滴": "A drop, drip or drop counter is a small quantity/action, not a waterfall/rapids or rain sound; physical droplets alone are association.",
        "粒": "Grain/bead/drop or a small-object counter is not the whole flowing feature or supplemental moistening sense.",
        "落": "Fall/drop labels receive a conservative direct precaution; not every omission, defeat or decline is a waterfall.",
        "降": "Descend/fall labels receive a conservative direct precaution; surrender is not a waterfall.",
        "険": "Steepness/precipitous terrain is a possible setting, not the water feature or soaking/rain-sound sense.",
        "雨": "字通 positively records rain sound. Conservative broad rain-label protection, not every shower being a waterfall.",
        "音": "The positive character-source rain-sound sense warrants sound/noise protection, including 音's complete native families; not all sounds are 滝.",
        "響": "Complete family 1602130 explicitly includes distinctive rain sound. Direct precaution, not universal equivalence with every echo/emotion.",
        "騒": "Noise/turbulence labels receive a conservative sound-range precaution; not all unrest, Chinese verse or disturbances are 滝.",
        "鳴": "Sound/ring/cry range receives a conservative source-sound precaution; not all animal calls or mahjong calls are waterfalls.",
    },
}


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert git("remote", "get-url", "origin").decode().strip() == "https://github.com/stop-cran/learning-japanese.git"
        assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
        membership_path = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\n1-published-membership-6858fcfb.json")
        membership = json.loads(membership_path.read_bytes())
        assert membership["head"] == BASE and membership["counts"]["frozenPendingMembersPresent"] == 268
        assert all(c not in {r["kanji"] for r in membership["present"]} for c in CHARS)
        write(PACKET / "published-membership-binding.json", {
            "path": str(membership_path), "sha256": sha(membership_path.read_bytes()), "base": BASE,
            "counts": membership["counts"], "selectedMissing": list(CHARS)})
        source = HERE / "source-002"
        for path in sorted(source.rglob("*")):
            if path.is_file():
                write(PACKET / path.relative_to(source), path.read_bytes())
        for path in sorted((HERE / "additional-001").rglob("*")):
            if path.is_file() and path.name != "readback.txt":
                write(PACKET / "additional" / path.relative_to(HERE / "additional-001"), path.read_bytes())
        for name in ("common_133.py", "survey_133.py", "sources_133.py", "sources_133_final.py",
                     "verify_sources_133.py", "verify_sources_133_final.py", "supplement_133.py",
                     "additional_133.py", "readback_133.py", "compact_readback_133.py", "prepare_133.py"):
            write(PACKET / "producers" / name, (HERE / name).read_bytes())
        spec = importlib.util.spec_from_file_location("converter_b133", REPO / "tools" / "generate_strokes.py")
        converter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(converter)
        assert sha((REPO / "tools" / "generate_strokes.py").read_bytes()) == "6993834d66221d23399547e5a17771d2d638dc68b2d08d47e9875ddc2c932081"
        rows = json.loads((PACKET / "source-rows.json").read_bytes())
        stroke_members = []
        pair_members = []
        for row in rows:
            ch = row["kanji"]
            svg = (source / "kanjivg" / f"{ord(ch):05x}.svg").read_bytes()
            blob = hashlib.sha1(b"blob " + str(len(svg)).encode() + b"\0" + svg).hexdigest()
            assert blob == row["kanjivgInventory"]["sha"]
            strokes = converter.convert(ch, svg.decode())
            assert strokes["strokeCount"] == row["metadata"]["strokes"]
            raw = (json.dumps(strokes, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
            write(REPO / "strokes" / f"{ch}.json", raw)
            stroke_members.append({"kanji": ch, "strokeCount": strokes["strokeCount"], "strokeSha256": sha(raw), "svgSha256": sha(svg), "kanjivgBlob": blob})
            scan = json.loads((source / "scans" / f"{ch}.json").read_bytes())
            assert len(scan["rows"]) == 1258 and set(scan["matches"]) <= REASONS[ch].keys()
            reasons = dict(REASONS[ch])
            for other in CURATED[ch]:
                reasons[other] = {
                    "古": "Old/ancient/secondhand describes age or used goods, not this target's full material/instrument/water/supplemental sense range. An old instance is only an association.",
                    "右": "Direction, above-mentioned, right-wing, superiority and right-hand senses do not denote the target's full qualified sense range; spatial placement is not lexical identity.",
                    "川": "River/stream differs from the instrument or the metal, powder, counterfeit-money and heaviness senses. Physical proximity to a river does not equate them.",
                    "寺": "A Buddhist temple/religious building or temple counter is not waterfall/rapids, rain sound or soaking; a waterfall in temple grounds is only association.",
                }[other]
            pairs = []
            title = re.search(r"^title: (.+)$", normalized(REPO / "kanji" / f"{ch}.md"), re.M).group(1)
            for other, reason in reasons.items():
                path = source / "comparison-cards" / f"{other}.md"
                if not path.exists():
                    path = HERE / "additional-001" / "comparison-cards" / f"{other}.md"
                baseline_raw = git("show", f"{BASE}:kanji/{other}.md")
                assert path.read_bytes() == baseline_raw
                comparison_title = re.search(r"^title: (.+)$", baseline_raw.replace(b"\r\n", b"\n").decode(), re.M).group(1)
                pairs.append({
                    "pair": [ch, other], "comparisonTitle": comparison_title,
                    "decision": "curated" if other in CURATED[ch] else "guard" if other in GUARDS[ch] else "distinct",
                    "comparisonLabelOnTarget": f"Considered displayed {comparison_title!r} against {ch}'s complete qualified range. {reason}",
                    "targetLabelOnComparison": f"Considered displayed {title!r} against {other}'s actual card, full character meanings and complete applicable word senses. {reason}",
                    "baselineCardSha256": sha(baseline_raw), "scanMatch": other in scan["matches"],
                    "additionalSourceDrivenComparison": other not in scan["matches"] and other not in CURATED[ch]})
            pair_members.append({"kanji": ch, "targetTitle": title, "scanRows": len(scan["rows"]), "pairs": pairs})
        new_pairs = [
            {"pair": ["琴", "鉛"], "decision": "distinct", "bothDirections": "Instrument/burial mound is neither metal, face powder, counterfeit money nor heavy/dull quality. Musical instruments made from metal do not establish synonymy."},
            {"pair": ["琴", "滝"], "decision": "distinct", "bothDirections": "Instrument/burial mound is not waterfall/rapids/soaking/rain sound. 水琴窟 is a whole compound; sound made by both is association, not bare 琴=rain sound."},
            {"pair": ["鉛", "滝"], "decision": "distinct", "bothDirections": "Metal/powder/counterfeit money/heavy-dull range is not waterfall/rapids/soaking/rain sound; material in water does not establish identity."},
        ]
        write(PACKET / "pair-dispositions.json", {
            "base": BASE, "members": pair_members, "newMemberPairs": new_pairs,
            "rule": "Direct symmetric pairs only, no transitive closure. Precautions protect unresolved broad labels, not universal synonymy.",
            "coverage": "Actual complete cards, full English character meanings and all captured applicable word-family senses read; 491-family original union plus separately verified source-driven additions. Scan has every baseline card, not first-label-only matching.",
            "limits": "Finite manually expanded scan and source-driven comparison set; not exhaustive synonym discovery or independent review."})
        text = "".join(normalized(REPO / "kanji" / f"{c}.md") + normalized(REPO / "words" / f"{SUPPORTS[c]}.md") for c in CHARS)
        comparisons = set().union(*(set(REASONS[c]) | set(CURATED[c]) for c in CHARS))
        glyphs = "".join(sorted(set(re.findall(r"[\u3400-\u9fff]", text)) | comparisons | set("玉王今金八口水氵竜龍珡琹鈆瀧")))
        fonts = []
        for path in sorted((ROOT / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
            with TTFont(path) as font:
                cmap = font.getBestCmap()
                fonts.append({"filename": path.name, "sha256": sha(path.read_bytes()),
                              "coverage": {f"U+{ord(ch):04X}": ord(ch) in cmap for ch in glyphs}})
        assert len(fonts) == 3
        write(PACKET / "stroke-font-evidence.json", {
            "members": stroke_members, "converterSha256": sha((REPO / "tools" / "generate_strokes.py").read_bytes()),
            "kanjivgRevision": converter.KANJIVG_REVISION, "fonts": fonts,
            "codePoints": [{"character": c, "codePoint": f"U+{ord(c):04X}", "unicodeName": unicodedata.name(c)} for c in glyphs],
            "scope": "Han in final target/support articles plus finite comparisons and named radical/component/variant codepoints.",
            "limits": "Actual bounded bundled font cmap membership only; not rendered/visual/native/device/fallback acceptance."})
        write(PACKET / "selection.json", {
            "batch": 133, "base": BASE, "members": list(CHARS), "sourceRows": [707, 1120, 643],
            "supports": [[c, SUPPORTS[c]] for c in CHARS], "publishedDelivered": 268, "undelivered": 960,
            "localDrafts": 3, "deliveryNotIncremented": True, "proseException": None,
            "split": "Original five-member 琴紫詩鉛滝 packet: 1097 families/146 comparisons. Final three-member main packet: 487 families/62 comparisons; supplemental 17 families gives canonical-equality checked union 491, plus six source-driven comparison cards and their full families.",
            "notSelected": {"嵐": "Separate mountain-mist/weather/disturbance and reading packet.", "紫": "Separate native secondary-sense and stroke discrepancy packet.", "詩": "Separate aesthetic/supplemental character-sense packet.", "矢": "Separate wedge/oath/arrange/excrement and stale prose packet.", "皇": "B131 unresolved native/prefix/secondary senses remain separate.", "桜": "B131 native secondary senses remain separate.", "伯": "row33 deferred; 伯母さん does not establish ハク.", "憶": "row395 deferred.", "撲": "row461 deferred; 相撲 does not establish ボク."}})
        analysis = {
            "琴": {
                "practice": {"on": [], "kun": ["こと"]}, "support": "琴 at N2",
                "readingDisposition": "Full ordered キン/ゴン/こと metadata; standalone きん 2229960 and わごん 2204940 are recognition, only linked こと practice. そう is restricted to 箏/筝 in 1241450. External old ゴム/キム/ことのを/きのこと over-tested, not ordinary modern assertions.",
                "positiveSecondary": "Full monolingual native こと includes older broader string-instrument use. 字通 explicitly records Chu-language 冢/塚; conservatively guard 墓 and 丘 without claiming ordinary modern synonymy. 琴瑟 happy marriage, 琴線 heartstrings and compound instrument/animal/constellation names stay whole-word allocations.",
                "variants": "Complete KD 珡 and 琹 retained; complete JMdict variant-containing queries both zero."},
            "鉛": {
                "practice": {"on": ["エン"], "kun": []}, "support": "鉛筆 at N5",
                "readingDisposition": "Complete エン/なまり retained; linked えんぴつ supports エン, not independent ピツ. Native なまり and old くろなまり recognition only.",
                "positiveSecondary": "Native なまり: metal, heavy/dull comparison and counterfeit money. Character source: face powder and lead-like compound substances graphite/zinc/bismuth. 顔 1217730 sense7 makeup, 金 full native metal/money, 銀 full native money, 末 suffix powder all retained despite narrower displayed titles. Broad precautions do not claim every coin/element/weight is lead.",
                "restrictions": "2180400 cosmetic lead carbonate vs 2180410 lead writing powder retain separate complete families. 鉛筆 graphite core is not Pb; 鉛槧 writing literature remains compound-wide.",
                "variants": "Complete KD 鈆 retained; complete variant-containing JMdict query zero."},
            "滝": {
                "practice": {"on": [], "kun": ["たき"]}, "support": "滝 at N2",
                "readingDisposition": "Full ordered ロウ/ソウ/たき metadata. Source-only リョウ/サウ/はやせ/ひたす/うるおす, name/outside-standard らき, older たるみ and uncertain voiced たぎ explicitly over-tested. Not discarded on standard-list grounds, not all independent ordinary readings.",
                "positiveSecondary": "Native たき: waterfall, rapids, 滝水 abbreviation. Character source: rain sound, rapids, soak/moisten. Complete 1415520 has archaic flag on rapids and old-form spelling 瀧. Profit sense in 潤す does not automatically transfer to bare 滝; preserve allocation uncertainty. 白滝 noodle sense is compound-wide.",
                "variants": "瀧 complete KD:19 strokes, 龍 shape, not modern 13-stroke 滝/竜 geometry. Complete 瀧-containing query returns one family."},
        }
        write(PACKET / "authored-source-analysis.json", {
            "base": BASE, "members": analysis, "externalCaptures": "Reused B132 survey captures, exact raw/text hashes verified; not new B133 fetches. Full pages stay local.",
            "discrepancies": "Historical glyph images are absent from extracted pages; not reconstructed. Non-etymological shape mnemonics avoid asserting disputed historical analyses. Different dictionary scopes/readings are preserved, not silently harmonized.",
            "limits": "Author source adjudication only; no reviewer launched, no native/device/visual/whole-set/publication acceptance."})
        snippets = {
            ("琴", "kotobank"): ["2. 楚の語で、冢（塚）をいう。", "〔和名抄〕琴　古度乃乎（ことのを）〔名義抄〕琴　コト・キノコト"],
            ("琴", "weblio"): ["ゴム", "キム"],
            ("鉛", "kotobank"): ["(にせがね)", "奈万利（くろなまり）"],
            ("鉛", "weblio"): [],
            ("滝", "kotobank"): ["ロウ・リョウ・ソウ（サウ）", "はやせ・たき・ひたす", "3. ひたす、うるおす。"],
            ("滝", "weblio"): ["らき"],
        }
        excerpts = []
        for item in json.loads((source / "external-capture-bindings.json").read_bytes())["captures"]:
            text = Path(item["localRawCapture"]).with_suffix(".txt").read_text(encoding="utf-8")
            quoted = []
            for snippet in snippets[(item["character"], item["provider"])]:
                assert snippet in text
                offset = text.index(snippet)
                quoted.append({"text": snippet, "line": text[:offset].count("\n") + 1})
            excerpts.append({"character": item["character"], "provider": item["provider"], "url": item["finalUrl"],
                             "textSha256": item["textSha256"], "excerpts": quoted})
        write(PACKET / "bounded-excerpts.json", {
            "attribution": "Kotobank: Shogakukan Digital Daijisen/日本国語大辞典 and Heibonsha 字通; Weblio: attributed constituent character dictionaries/Wiktionary sections.",
            "captures": excerpts, "limits": "Short attributable quotations only. Full pages are local, bound separately. Empty excerpts do not mean the page was absent."})
        history = {}
        for directory in ("survey-001", "source-001", "source-002", "additional-001", "readback-001", "readback-002"):
            for p in sorted((HERE / directory).rglob("*")):
                if p.is_file():
                    history[str(p.relative_to(HERE)).replace("\\", "/")] = sha(p.read_bytes())
        write(PACKET / "local-history-bindings.json", {"directory": str(HERE), "files": history,
              "limits": "Historical broader selection and all original evidence preserved. Complete external pages live at the exact reused-capture paths; review directory untouched."})
        print(json.dumps({"pairs": sum(len(m["pairs"]) for m in pair_members), "newPairs": len(new_pairs),
                          "comparisons": len(comparisons), "missingFonts": {f["filename"]: [k for k, v in f["coverage"].items() if not v] for f in fonts}}, ensure_ascii=False))
    finally:
        write(HERE / "preparation-memory-001.json", guard.finish())


if __name__ == "__main__":
    main()
