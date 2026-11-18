import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from r131_common import *

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

ADDITIONS = {"霜": list("氷凍酒涼久害枯殺卒"), "衛": list("援循番士軍送抵")}

# Each tuple independently addresses the two actual displayed-answer directions.
DECISIONS = [
    ("R1", "霜", "氷", [1488840, 1488850, 1488880, 1583430, 1593100], ["05:17-18"],
     "Ice is a defensible substance description for deposited frost crystals and refrigerator fine ice; this is a direct supplied definition, not an unrestricted hypernym policy.",
     "Frost is not a replacement for every ice mass, hailstone or shaved ice; the overlapping fine-ice region nevertheless warrants a direct guard.",
     "Required direct guard; no assertion that every form of ice is frost."),
    ("R2", "霜", "凍", [1446180, 1446210, 1446230, 1557170, 1593100], ["05:17-18"],
     "The freeze/frozen label reaches the frozen deposit explicitly defined for frost, including refrigerator frost.",
     "Frost does not translate every freezing event, chilled body or congealing material. The specific frozen-deposit overlap is enough for a precaution in either option direction.",
     "Required direct guard, not frost-heave/permafrost English extrapolation or a universal freezing synonym."),
    ("R3", "衛", "援", [1176650, 1176660, 1179840, 1229070, 1310100, 1380460, 1588790], ["01:12,39-40"],
     "Aid/assistance can describe the directly protective saving/helping region of guarding; KANJIDIC2 援 explicitly includes save. The complete 援 article independently retains rescue/protection.",
     "Guard/defense is defensible for protective rescue or covering from attack, not for general financial assistance, cheering or merely drawing something toward oneself.",
     "Required qualified direct guard. Complete 援護 family retains its 援護-only help restriction and its separate unrestricted protection sense; no third-card transitivity."),
    ("R4", "衛", "循", [1341340], ["01:13,43"],
     "Cycle is defensible for the unrestricted going-around branch 周りをまわる/取り巻く, reinforced by the historical メグル lookup; it is not restricted to satellites orbiting a centre.",
     "Guard/defense is not a definition of following a sequence. Going around can reach 衛's circling branch, while ordinary sequential following need not guard anything.",
     "Required direct precaution for partial circling overlap, not a generic follow/defend equation."),
    ("Q1", "霜", "酒", [1329010, 1329040, 1464670, 2862891, 2862909, 2862910], ["06:27-33"],
     "Alcohol/sake is a direct answer for the independently listed bare 霜しも jargon sense 酒類一切, not an inference from white appearance or a compound.",
     "Frost is not an ordinary definition of 酒. The broad alcoholic-drink sense overlaps the explicitly attested jargon denotation in the opposite direction.",
     "Qualified precaution for a compilation of Meiji-and-later jargon; not proof of ordinary modern 霜 usage. No additional reading/practice key."),
    ("Q2", "霜", "冴", [1297040, 1297050, 1877830, 1911790, 2576510, 2679180], ["05:14,47"],
     "Clear; sharp-minded is not a defensible answer for frost deposits, white hair, elapsed years, powdered preparation, loss or the white/cold/sharp/severe comparisons. Sharpness of an edge/severity is not mental alertness or clarity; the shared English stem does not establish that sense.",
     "Frost (the noun taught here: deposited ice) is not a definition of clearness, skill, wakefulness, appearance or the older becoming-frigid sense. Even 冴's complete KANJIDIC2 こおる/ひえる inventory describes freezing/cold, not that deposited substance. Weather capable of producing frost is not the noun frost.",
     "Bounded non-collision for these actual displayed labels and complete opened senses only. Positive old-fashioned frigid/intensely-cold sense in 1297050, rare 冴寒, KD cold/freezing keys and Spanish freezing gloss remain; no assertion that the two characters never share cold-related contexts."),
    ("Q3", "霜", "涼", [1554370, 1554380, 1585180, 2105640, 2729660], ["05:14,47"],
     "Cool can be a defensible broad label for the explicitly listed cold-things comparison, although pleasant refreshing coolness is narrower than severe cold.",
     "Frost is not an ordinary gloss of cooling oneself, clear eyes, composure or refreshing air. This direct precaution protects the broad cool/cold label region rather than erasing those distinctions.",
     "Qualified precaution, not an inference through 冷/寒 or an assertion that every cool breeze is frost."),
    ("Q4", "霜", "久", [1227340, 1227370, 1576520, 1577900], ["05:13,29,46"],
     "A long time can describe the attested elapsed-years としつき/年月/歴年 branch; the duration is positive source evidence, not merely an old-looking frosty object.",
     "Frost does not define every long interval, old story or eternity. The direct safeguard covers broad elapsed-time answers without turning all durations into weather.",
     "Qualified precaution; not transitive through 年/歴 and not a claim that every elapsed year is necessarily a long time."),
    ("Q5", "霜", "害", [1204330, 1484350, 1541140, 1611870], ["05:43,48"],
     "Harm/damage can be a broad answer for the independently listed loss/perishing branch, but the exact historical reach of うしなう is not settled by the primary weather noun.",
     "Frost does not ordinarily define injury, damage or evil influence. The source-positive destructive/loss region gets a precaution, not a new assertion that 霜害 allocates all harm to bare 霜.",
     "Qualified lexical-allocation precaution, not frost-causes-damage reasoning or an inference through 損."),
    ("Q6", "霜", "枯", [1267210, 1267220, 1267250], ["05:43,48"],
     "Wither can be a defensible special case of the positive perishing branch when plants perish; the exact scope remains qualified.",
     "Frost is not the ordinary definition of withering, personality maturation or seasoning lumber. KD 枯 die and complete 枯れる die are retained, so the death/perishing region is protected directly.",
     "Qualified precaution from independent perishing/death evidence, not an allocation from the compound 霜枯れ or from a third-card 死 guard."),
    ("Q7", "霜", "殺", [1299030], ["05:43,48"],
     "Kill is not automatically equivalent to intransitive perish. The positive うしなう/loss branch and historical destructive explanation leave the breadth toward destructive kill uncertain, so a direct safeguard is preferable to asserting a clean non-collision.",
     "Frost is not the ordinary definition of murder, suppressing a voice, spoiling talent/flavour, baseball putting-out or pawning. All complete 殺す secondary senses remain; none proves that every such action belongs to bare 霜.",
     "Qualified precaution, not a taught general kill sense. Image gaps in the historical quotation remain; no invented glyph reading, frost-kills-plants causal proof, or 討/死 transitivity."),
    ("Q8", "霜", "卒", [1332760, 1405880, 1405890, 1405940, 1581360, 1589600, 1952760, 2259940], ["05:48"],
     "Finish can be a loose answer for a life's ending in the positive perishing branch; graduation is not a frost sense.",
     "Frost does not ordinarily mean graduating, completing a task, a soldier or formal death. The actual retained 卒する formal death and 卒る ending families support a qualified life-ending precaution.",
     "Qualified precaution; preserves search-only 卒える and rare 卒る distinctions, not unrestricted ordinary spellings or a transitive 衛/卒/亡 chain."),
    ("Q9", "衛", "番", [1165970, 1449220, 1482290, 2022640, 2199920], ["01:12,40"],
     "Turn in a series is not a primary defense definition, but a guard's turn on watch can be described that way; protect rather than assume the short title exhausts 番.",
     "Guard is an explicit ordinary sense of bare 番 in complete 2022640, alongside watch/lookout; thus 衛's displayed label is directly defensible. The pair/joint and numbering senses remain separate.",
     "Qualified direct precaution; stronger independent bare-word evidence than 当番 alone, no watch-guard transitivity."),
    ("Q10", "衛", "士", [1314780, 1512850, 1583680, 1714320, 2815550], ["01:12,40"],
     "Warrior can describe the military guard-person region, though neither every guard nor every professional is a warrior.",
     "Guard/defense can be defensible for the military-retainer role in the historical 士/侍 warrior family; not for every licensed professional or respected man.",
     "Qualified role-overlap precaution based on the directly attested guard-person/military branch, not transfer through 兵 or 卒."),
    ("Q11", "衛", "軍", [1247660, 1248080, 1248710, 1587140], ["01:40"],
     "Troops can be a defensible broad description of the collective military guarding region in 守るもの、宿衛、軍衛. This does not allocate every compound sense to 衛.",
     "Guard/defense is defensible for troops acting as a protective military guard, not every army, war/battle, team or military authority. Bare 軍 and its unmarked いくさ war sense remain in full.",
     "Qualified collective-role precaution rather than proof that bare 衛 universally means army; compound allocation remains limited, with no 兵/卒 chain."),
    ("Q12", "衛", "送", [1271510, 1402730, 2825310], ["01:12,39"],
     "Escort can describe guarding someone while accompanying them. Complete 護衛/衛護 corroborate that use but are not the sole basis for assigning unrestricted escort to bare 衛.",
     "Guard is defensible for a protective escort, but not every ordinary 送る taking-home, mail dispatch, funeral, passing time or okurigana action includes protection.",
     "Qualified protective-function precaution grounded in guarding; bare-constituent allocation is not asserted from compounds alone. 贈る gift remains separate."),
    ("Q13", "衛", "抵", [1414580, 1436260, 1436280, 1436290], ["01:39"],
     "Resist can be defensible for warding off an attack under the explicit ふせぐ branch, not a meaning inferred through 防.",
     "Guard/defense can describe protective resistance, not every collision, contact, reluctance, electrical resistance, mortgage or approximate amount.",
     "Qualified direct precaution for warding-off/opposition, not a claim that every resistance is defensive."),
]

guard = start_guard()
try:
    receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf8"))
    jm = {n.findtext("ent_seq"): n for n in ET.parse(PACKET / "jmdict-families.xml").getroot()}
    rows = []
    for key, target, comp, ids, refs, forward, reverse, limit in DECISIONS:
        assert all(str(i) in jm for i in ids), (key, ids)
        target_fm, _ = n1lib.parse(normalized(REPO / "kanji" / (target + ".md")))
        comp_fm, _ = n1lib.parse(normalized(PACKET / "comparison-cards" / (comp + ".md")))
        rows.append({
            "id": key, "pair": [target, comp],
            "displayedLabels": [target_fm["title"], comp_fm["title"]],
            "decision": "bounded-non-collision" if key == "Q2" else "qualified-direct-precaution",
            "directExclusionOnNewEndpoint": key != "Q2", "openQuizHold": False,
            "comparisonLabelOnTarget": forward, "targetLabelOnComparison": reverse,
            "sources": {"completeComparisonCard": f"comparison-cards/{comp}.md",
                        "comparisonCardSha256": sha((PACKET / "comparison-cards" / (comp + ".md")).read_bytes()),
                        "completeKanjidicRecords": [target, comp], "completeJmdictEntryIds": ids,
                        "canonicalFamilyHashes": {str(i): sha(ET.canonicalize(ET.tostring(jm[str(i)], encoding="unicode"), strip_text=True).encode()) for i in ids},
                        "frozenExtractLines": refs,
                        "bindings": ["source-receipt.json", "external-source-bindings.json"]},
            "qualificationAndResidualLimits": limit})
    assert [r["id"] for r in rows[4:]] == [f"Q{i}" for i in range(1, 14)]
    assert {tuple(r["pair"]) for r in rows if r["directExclusionOnNewEndpoint"]} == {
        (ch, c) for ch, additions in ADDITIONS.items() for c in additions}
    write(PACKET / "pair-dispositions-001.json", {
        "parent": PARENT, "publishedBase": BASE, "rows": rows,
        "sourceReceiptSha256": sha((PACKET / "source-receipt.json").read_bytes()),
        "supersession": "Addendum only for these 17 pairs. Original source/scans/decisions remain immutable historical evidence; all other finite dispositions stay bounded and unchanged.",
        "criterion": "Both actual displayed-label directions assessed using complete opened comparison articles, complete relevant families and positive secondary/historical sources. Direct declarations work symmetrically and are never transitive.",
        "status": "Author dispositions awaiting two independent original-family confirmations; no publication acceptance.",
        "limits": "Precautions are not proven universal synonymy. Q2 is bounded to opened senses, not a whole-index absence claim. Historical, rare, supplemental, native-word, name, register and allocation limits are retained."})
    write(PACKET / "authored-source-analysis-001.json", {
        "sourceFamilyReadback": {"completeJmdictFamilies": 78, "completeKanjidicRecords": 19,
                                "comparisonCards": 17, "localFullReadbackChunks": 8},
        "sourceDiscrepancies": [
            "霜's pinned KD has ソウ/しも, while supplemental ショウ/ほろぶ/うしなう remain qualified; no metadata change.",
            "冴 cold/freezing keys and old-fashioned intense cold remain positive, notwithstanding its current clear/sharp-minded displayed title.",
            "卒える is search-only; 卒る is rare; character source 卒わる differs from the complete JM family spellings.",
            "衛 source-specific circling and historical forms do not disappear behind the 衛星 example or KD empty kun list.",
            "Weblio's bare 霜 alcohol entry is a historical-jargon compilation, not ordinary modern weather usage.",
            "Whole-word 護衛/衛護 and 軍衛 examples are not independently sufficient to allocate every full-family sense to one bare constituent.",
            "Historical image-only glyph gaps remain; no invented completion or generalized etymology."],
        "unchangedReadingScope": "Original full ordered metadata, selected practice and all explicitly supplied supplemental/name keys unchanged. Reuse original 874-family union by exact bindings. New 78-family extraction is for the finite semantic comparisons, not new practice.",
        "sourceAbsences": "Exact spelling zero matches in receipt are retained as query outcomes, not proofs of lexical absence or clean quiz distinctions.",
        "copyrightScope": "Only attributed short phrases and original analysis from external character sources. Full response/extract bytes remain local, hash-bound.",
        "unaffected": "羊, four support wrappers, all strokes/fonts, ordinary membership and prior evidence unchanged. No new article or device work."})
    print(json.dumps({"pairs": len(rows), "addedGuards": sum(map(len, ADDITIONS.values())),
                      "boundedNonCollisions": ["Q2"], "openAuthorHolds": []}))
finally:
    write(HERE / "decisions-memory-001.json", guard.finish())
