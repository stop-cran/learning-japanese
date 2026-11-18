import json
import re
import sys
from pathlib import Path
from b130_common import BASE, CHARS, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

REASONS = {c: {} for c in CHARS}


def group(ch, others, decision, reason):
    for other in others:
        assert other not in REASONS[ch], (ch, other)
        REASONS[ch][other] = (decision, reason)


group("塀", "囲境界辺畔関包括障標", "guard",
      "Full enclosure/fence, boundary/edge, barrier, enclosing or cordoning-off ranges intersect the broad boundary-wall label. Direct precaution; an enclosure action, field ridge, checkpoint, sign and physical fence are not universally interchangeable.")
group("塀", "働凪匁笹込", "distinct",
      "The 国字 scan is a classification hit, not a meaning of wall. Work, calm, a weight unit, bamboo and crowding do not name a boundary structure, even including the complete secondary ranges.")
group("拍", "打当撃批触接抵摩擦", "guard",
      "Striking/contact and the positive うつ・たたく inventory make the broad contact labels unresolved; 摩/擦 additionally protect the unresolved historical ナヅ/ニシル allocation. Not all collision, resistance, criticism or rubbing is clapping.")
group("拍", "律調整楽曲音刻時", "guard",
      "Complete character/word records retain rhythm, metre, musical time, music or sound beyond the first displayed label. 拍 is a musical timing unit, not an arbitrary time duration or every tune.")
group("拍", "木板盤析", "guard",
      "字通 positively names wooden clappers. Complete 木 families and the 柝 family including search-only 析 preserve clapper nouns; board/plate labels get a conservative instrument precaution. Neither clappers nor their material are universally a beat.")
group("拍", "動印標点書著送伝寄輸入注結括投払給作造備設演耕訪伺参", "guard",
      "Complete JMdict 1408810 retains moving/impressing, marking/writing, transmitting, inserting/injecting, binding, throwing, paying, making/preparing, performing/tilling and visiting. 拍つ is flagged rarely-used; the unallocated multi-spelling family does NOT establish every sense for every spelling. These are conservative direct broad-label precautions, not modern bare-character teaching claims.")
group("拍", "励勧賛騒", "guard",
      "字通's はやし/はやしたてる supplies positive cheering/encouragement and noisy acclamation; protect broad encouraging/praising/noise labels without equating every recommendation or uproar with clapping.")
group("拍", "久元先再分初宙度悠昔暮期歴秒際", "distinct",
      "Long/former/previous/repeated/initial time, parts, remoteness, occurrence counts, periods, seconds and occasions are not the musical beat or mora. 拍子's moment/chance is a whole-word sense, not proof that 拍 alone denotes every occasion or duration.")
group("拍", "乗亭商局川材梓樹版町画移補越", "distinct",
      "Boarding, a venue, trading, a bureau, river, material/timber/tree, printing block, town block, picture/brushstroke, shifting, supplementing and exceeding are distinct. Material, location, written stroke and possible object relations do not transfer the clapper, beating or rhythm senses.")
group("拍", "努勉勇", "distinct",
      "Exertion, diligence and courage are not clapping or musical time. The complete encourage sense of 勉 is retained; an effect/purpose of cheering does not make the displayed effort/bravery labels names for 拍.")
group("拍", "召", "distinct",
      "Honorific summoning/eating/putting-on and related 召 senses are not sending a message, the specified pilgrimage visit, clapping or a beat.")
group("拍", "丸使", "distinct",
      "Roundness/pellets/counters and using/employing/messengers are not a clap or musical unit. Round shape is not time; generic doing in the unallocated native family does not make every use of a tool a 拍 sense.")
group("拍", "徹喫星的跡草識贈捨償収営賞碁符", "distinct",
      "Complete positive secondary senses remain visible, but neither displayed-label direction is established: figurative strike-home is not physical clapping; receiving a blow is not giving a clap; celestial point/target/trace/grass/knowledge are not generic marking/writing; gift/discard/recompense/collect/business/prize are not the specified native-family actions. Go and tokens are objects of play or signs, not the action or timing unit itself. No transitive extension of a guard.")
group("耗", "減損失費消使喫害痛割破殺亡弱縮古傾負暮", "guard",
      "Depletion/loss/expenditure/use, damage or wearing-out ranges are positive. 古's actual card illustrates 使い古す; 傾 retains wane; 暮 retains spending time. Broad harm, breaking, perishing and contraction labels are precautions, not an equation of all pain or killing with ordinary resource use.")
group("耗", "悪凶貧薄細荒暗濃乱騒", "guard",
      "字通 positively supplies bad/poor/barren/thin/dark/disordered ranges. Protect broad badness, thinness, darkness and commotion labels while preserving each comparison's other senses. Dark colour is not universally darkness or depletion.")
group("耗", "動変嫌憎空別離帰戻返復転代換化移改倒断", "guard",
      "Historical ツイユ・ヤブル・ヘナル・カヘル・ニクム・ムナシ and the positive みだれる inventory leave collapse/break/separation/return/change/hate/empty labels unresolved. Guards are conservative pending historical allocation, not claims that every modern spelling or physical movement is an ordinary 耗 sense.")
group("耗", "報告届伝", "guard",
      "Verified 漢字ペディア 耗 gives たより・知らせ and 音耗. News/report and broad informing/notifying/conveying choices receive direct precautions; this is not universal equivalence between a message noun and every act of telling.")
group("耗", "冒毒障折討不厄短曲草紺凹析投", "distinct",
      "Braving/poisoning/obstructing/folding/attacking, negation, calamity, shortness, bending/music, grass, navy, concavity, analysis and throwing are not established by either displayed-label direction. Harm is not every cause of harm; dark is not specifically navy; empty is not specifically a concave shape; separation is not analysis. Complete secondary positives are retained, not inherited transitively.")
group("耗", "召子字枚注涙着著被貯魔", "distinct",
      "Summoning/eating/putting-on, zodiac Rat, letter-as-character, sheet counters, pouring, tears, donning/arriving, writing, covering, saving and demon senses do not denote depletion through use. 耗子 is a whole rat word; キヌ is an unresolved historical string, not evidence that depletion means donning clothes. Wearing clothes and wearing-out are different English senses.")
group("耗", "便書信知識触", "distinct",
      "Complete letter/news/proclamation/information secondary senses remain positive and inspected. But the current convenience/write/trust/know/awareness/touch labels do not name depletion, and 耗's news noun does not mean convenience, writing, reliance, knowledge or touching. Homophonous たより news and reliance families must not be collapsed. A common secondary topic alone does not compel a guard.")
group("耗", "否", "distinct",
      "Denial/not/no is not bad condition, depletion or news. Negative evaluation does not turn every negative predicate into a 耗 sense.")
for ch in "塀拍":
    group(ch, "古右石", "curated",
          "Old (including antique and wearing-out uses), right (including direction and prioritising), and stone (including flint, game pieces, calculus and counters) do not name a fence or clapping/musical timing. Properties, material and objects of play are not identity.")
group("耗", "右石未", "curated",
      "Right/prioritising, stone/game-piece/calculus/counters and not-yet plus Sheep-branch/time/direction/month do not denote depletion, news, damage or the qualified historical actions. These choices do not rely only on different titles.")
group("耗", "毛耕", "rejected",
      "Not curated: 毛 shares モウ; 耕 shares コウ with the complete metadata. Shape relation and the 耒 radical do not make them safe reading distractors. Hair/tilling are not depletion or news.")
REASONS["拍"]["石"] = ("distinct", REASONS["拍"]["石"][1])
REASONS["拍"]["川"] = ("curated", "River/stream, including the actual whole card and full exact-family range, is not clapping, a musical beat or a mora. Flowing waves having rhythm is a property/event association, not lexical identity. Starter membership fills the third curated slot without the original 百/ヒャク fallback.")
for other in "石未":
    REASONS["耗"][other] = ("distinct", REASONS["耗"][other][1])
for other in "川本":
    REASONS["耗"][other] = ("curated", "River/stream and book/script/origin/base/main/true/real/present plus counters do not mean depletion, news, damage or the qualified historical actions. A written source need not be news, and flowing water need not be loss. Full actual cards and complete families were inspected; Starter membership closes fallback slots.")

guard = start_guard()
try:
    members = []
    for ch in CHARS:
        fm, _ = n1lib.parse(normalized(REPO / "kanji" / (ch + ".md")))
        scanpath = PACKET / "scans-002" / (ch + ".json")
        scan = json.loads(scanpath.read_text(encoding="utf8"))
        required = set(scan["matches"]) | set(fm["distractors"]) | set(fm["quiz_exclusions"])
        assert required <= REASONS[ch].keys(), (ch, sorted(required - REASONS[ch].keys()))
        assert set(fm["quiz_exclusions"]) == {k for k, (d, _) in REASONS[ch].items() if d == "guard"}
        assert set(fm["distractors"]) == {k for k, (d, _) in REASONS[ch].items() if d == "curated"}
        pairs = []
        for other, (decision, reason) in REASONS[ch].items():
            path = PACKET / "comparison-cards" / (other + ".md")
            raw = path.read_bytes()
            assert raw == git("show", f"{BASE}:kanji/{other}.md")
            ofm, _ = n1lib.parse(raw.replace(b"\r\n", b"\n").decode())
            pairs.append({"pair": [ch, other], "comparisonTitle": ofm["title"], "decision": decision,
                          "comparisonLabelOnTarget": f"Considered actual {ofm['title']!r} against the full qualified {ch} range. {reason}",
                          "targetLabelOnComparison": f"Considered actual {fm['title']!r} against the complete {other} range; no universal equivalence is asserted. {reason}",
                          "baselineCardSha256": sha(raw), "scanMatch": other in scan["matches"]})
        members.append({"kanji": ch, "targetTitle": fm["title"], "scanRows": len(scan["rows"]),
                        "scanFile": f"scans-002/{ch}.json", "scanSha256": sha(scanpath.read_bytes()), "pairs": pairs})
    for a, b in [("塀", "拍"), ("塀", "耗"), ("拍", "耗")]:
        members.append({"newMemberPair": [a, b], "decision": "distinct",
                        "bothDirections": "Boundary wall/fence, clapping/musical timing/mora and depletion/wearing-out/news are distinct. Historical damage is not a wall; paying a deposit in the unallocated 拍つ family does not itself mean wearing out. A physical boundary, the action of striking it and its eventual wear are object/event relations, not interchangeable lexical identities."})
    write(PACKET / "pair-dispositions-002.json", {
        "base": BASE, "members": members,
        "rule": "Actual scan hits plus curated, excluded and rejected candidates; both displayed-label directions considered with complete secondary evidence. Exclusions use direct OR symmetry, never transitive closure. Precautions protect unresolved labels, not universal synonymy.",
        "readCoverage": "All 189 comparison Meaning/Notes projections, complete exact-family sense projections and complete KANJIDIC2 English/on/kun inventories read. Curated cards and supports read in full. Projections are not whole-card or raw-XML read claims; complete records and actual comparison copies remain authoritative.",
        "producerSha256": sha(Path(__file__).read_bytes())})
    captures = []
    for name in ("external-capture-bindings.json", "supplemental-external-bindings.json"):
        captures.append({"file": name, "sha256": sha((PACKET / name).read_bytes()),
                         "receipt": json.loads((PACKET / name).read_text(encoding="utf8"))})
    write(PACKET / "authored-source-analysis-002.json", {
        "completeFamilies": 519, "completeCharacterRecords": 192, "actualComparisonCopies": 189,
        "bindingFiles": captures,
        "excerpts": [
            {"character": "塀", "source": "Kotobank / 字通", "quote": "[字訓] かき", "qualification": "Supplemental form; not inserted into empty frozen kun list. Kokuji vs phonosemantic historical accounts remain discrepant."},
            {"character": "拍", "source": "Kotobank / 字通", "quote": "うつ・たたく・はやし", "qualification": "Positive character glosses; keep historical オフス・ヒムササラ・ナヅ・ニシル qualified. Mora is not necessarily syllable."},
            {"character": "耗", "source": "漢字ペディア https://www.kanjipedia.jp/kanji/0006729100", "quote": "②たより。知らせ。「音耗」", "qualification": "Verified actual page and body; positive news/information despite absent 音耗/耗る in pinned JMdict."},
            {"character": "耗", "source": "Kotobank / 字通", "quote": "[字音] コウ(カウ)・ボウ(バウ)・モウ", "qualification": "ボウ is supplemental and discrepant; preserve ordered モウ・コウ frozen metadata. Full local capture retains historical strings and missing-image limitations."}
        ],
        "supportAudit": [
            {"character": "塀", "word": "塀", "entry": "1506870", "practice": "ヘイ", "levelPreserved": 3},
            {"character": "拍", "word": "拍手", "entry": "1474820", "practice": "ハク", "levelPreserved": 3},
            {"character": "耗", "word": "消耗", "entry": "1580310", "practice": "モウ", "levelPreserved": 2}
        ],
        "sourceQualifications": [
            "All retained XML is complete parsed/reserialized records, not raw byte slices. Original compressed/decompressed hashes and mixed selection predicates are in receipts and final-query-membership.json, including absent queries.",
            "519-family union and 192 character records independently checked against full decompression. Positive search-only, rare spelling, no-kanji forms, restrictions and secondary senses are retained.",
            "JMdict 1408810 does not allocate every 打つ-family sense to every spelling. 拍手 かしわで and instrument readings are whole words, not freely distributable character readings.",
            "塀の中 prison, 拍子 chance and 心神耗弱 legal capacity are whole-term senses; 耗子 does not make 耗 a generic rat or zodiac branch.",
            "Initial web-search prose contained unreliable navigation URLs. Only followed identity/body-checked page 0006729100 supports the Kanjipedia claim.",
            "Supplement attempt001 failed because parsed spans split へる・たより. Original bytes, failed producer/log and memory receipt preserved. Attempt002 checks concatenated text without changing source.",
            "Missing image glyphs are unresolved. Invented modern-shape mnemonics are explicitly non-etymological.",
            "Full copyrighted external HTML/text remains local; only bindings, short attributable excerpts and authored analysis committed.",
            "All three bundled font cmaps lack 尸 U+5C38, 并 U+5E76, 扌 U+624C and 耒 U+8012. Target glyphs are present. No rendered fallback or visual/native/device acceptance claimed."
        ],
        "licenses": "JMdict/KANJIDIC2: EDRDG CC BY-SA 4.0 attribution in source receipts; KanjiVG CC BY-SA 3.0, pinned SVGs and converter bound in stroke-font-evidence.json.",
        "limits": "Finite author evidence only; not independent linguistic review, publication, arbitrary/custom/multiple-borrow pools, Kotlin/native/device, visual fallback or whole-task acceptance."})
    print(json.dumps({"pairRows": sum(len(m.get("pairs", [])) for m in members)}, ensure_ascii=False))
finally:
    write(HERE / "editorial-memory-003.json", guard.finish())
