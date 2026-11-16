import json
from pathlib import Path
from b131_common import HERE, PACKET, REPO, sha, start_guard, write
from candidate_b131 import BASE

ANALYSIS = {
    "衛": {
        "sourceRow": 977, "supports": ["自衛", "衛星"], "practice": {"on": ["エイ"], "kun": []},
        "completeMetadataReadings": {"on": ["エイ", "エ"], "kun": []},
        "readingDispositions": {
            "エイ": "Existing 自衛 1317400 and 衛星 1174760 support practice; full natural/artificial satellite senses retained.",
            "エ": "近衛 1630300 このえ and archaic 衛護 2825310 えご retain positive evidence; not additional linked practice.",
            "supplemental": "Daijisen まもる/まもり; Jitsu's historical マホリ/マモリ/メグル/マモル/カクム/モル/メグラス and body かこむ. Weblio/Wiktionary い/まもる/もり. Historic ヱイ/ヱ are historical spellings, not omitted modern metadata readings.",
            "nameUse": "Daijisen ひろ/もり/よし; Weblio/JMnedict surname section うえい/えい/まもり/まもる. Model also reports KD nanori もり/い/まもる. Name evidence is positive but not permission to read every ordinary word that way; 兵衛 endings and 衛士 are whole-word allocations."
        },
        "semanticDisposition": "Protection/guarding/guard-person and circling/surrounding retained. Direct precaution groups in pair table include protection/watch-over, guard/soldier and enclosure/circuit/revolving. Broader aid, generic military objects, state/territory and boundary/material associations are not inherited transitively.",
        "positiveSecondary": "The ancient named state and Jitsu 衛服 territorial category are preserved and distinguished from a generic modern country/province label. Hygiene and civil-engineering toilet sense in 衛生 are complete-compound senses, not a bare health gloss.",
        "sourceDiscrepancies": [
            "Daijisen/MyPedia call 康叔 武王's brother; Nikkoku/Nipponica call him 周公's brother. No resolution or founder-genealogy teaching claimed.",
            "Daijisen/Nikkoku/other encyclopedia sections give destruction in 209 BCE; Nipponica argues 221 BCE and calls the former record a compilation misallocation. No specific date taught.",
            "Jitsu historical glyph images are absent from extracted text. No missing glyph reconstructed or etymology asserted."
        ],
        "boundedQuote": {"provider": "Digital Daijisen via Kotobank", "text": "周りをまわる。取り巻く。"}
    },
    "羊": {
        "sourceRow": 870, "supports": ["羊毛"], "practice": {"on": ["ヨウ"], "kun": []},
        "completeMetadataReadings": {"on": ["ヨウ"], "kun": ["ひつじ"]},
        "readingDispositions": {
            "ヨウ": "Existing 羊毛 1546530 ようもう supports practice.",
            "ひつじ": "Standalone 羊 1546490 positively supports recognition; no existing bare 羊 word article, so no linked practice slot. JMdict ヒツジ re_nokanji retained.",
            "supplemental": "Weblio/Wiktionary ジョウ/ショウ explicitly tested. KD nanori よ is also reported/tested by the actual model, not assigned as ordinary vocabulary.",
            "wholeWords": "山羊/野羊 1303200 やぎ and 羊歯/歯朶 1594360 しだ are special whole-word spellings. 公羊伝/春秋公羊伝 are named works, not general bare reading rules."
        },
        "positiveSecondary": [
            "Nikkoku native ひつじ: paper, paper products, banknotes, hairdresser/hairdressing shop through かみ wordplay; obsolete Noh-play title. Weblio criminal/slang explicitly includes head hair.",
            "Jitsu: standing for 祥, good/auspicious/auspicious-sign uses; 相羊 wandering is a qualified complete expression."
        ],
        "semanticDisposition": "Direct paper/currency/hair/tuft and auspicious/good broad-label precautions retained, including 未's actual Sheep-zodiac identity despite its not-yet title. Other calendar animals, generic signs, ballot material, drama/performance and wandering-related verbs remain independently distinguished. Hairdresser is not silently discarded; paper products do not transfer every object made from paper.",
        "readingFailureAndResolution": "Original 古/右/石 had only two Starter choices; actual model disclosed ジョウ and ショウ padded hits despite exit zero. Replaced 石 with independently sourced Starter 川 on all three cards and made wrapper assert zero production/padded hits. Original output/producers preserved.",
        "boundedQuote": {"provider": "Jitsu via Kotobank", "text": "（祥）の字に用いることが多いが、省文にすぎない。"}
    },
    "霜": {
        "sourceRow": 1174, "supports": ["霜"], "practice": {"on": [], "kun": ["しも"]},
        "completeMetadataReadings": {"on": ["ソウ"], "kun": ["しも"]},
        "readingDispositions": {
            "しも": "Existing 霜 word article and complete family 1402930 support native practice; poetic white/grey-hair sense retained.",
            "ソウ": "霜害 1402950 そうがい and 星霜 1376420 せいそう support recognition, not additional linked practice. Obsolete 星霜 せいぞう retained with restrictions.",
            "supplemental": "Weblio/Wiktionary ショウ; Jitsu ほろぶ/うしなう explicitly over-tested as qualified positive character glosses, not ordinary weather-noun pronunciations.",
            "compoundRestrictions": "じも rendaku does not replace metadata しも. 秋霜 1734140 harshness/white-hair/sharp-sword senses restricted しゅうそう, native あきしも distinct. Complete 霜降り senses and 霜露 transience are not unrestricted bare-character glosses."
        },
        "positiveSecondary": [
            "Daijisen: surface/refrigerator frost, poetic grey/white hair; character years/time and white/cold/severe things.",
            "Nikkoku standalone: years/time, charred powdered medicinal material. Jitsu: frost/forming frost, years, white/sharp/intense/severe, perishing/loss.",
            "Nikkoku historical/poetic 霜ふる/霜おく coexist with ordinary 霜がおりる; the existing support's modern collocation is preserved, not generalized into universal invalidity."
        ],
        "semanticDisposition": "Direct guards for white/hair/cold, sharp/severe, years/time, powder/medicine and loss/perishing; individual property/object, consequence/action and complete-compound distinctions retained for every scan row. No transitive extension to all bitter/harmful/difficult/cold/black things or every sword.",
        "boundedQuote": {"provider": "Jitsu via Kotobank", "text": "ほろぶ、うしなう。"}
    }
}

guard = start_guard()
try:
    audit = json.loads((PACKET / "final-source-audit-002.json").read_text(encoding="utf8"))
    for ch, row in ANALYSIS.items():
        source_text = (HERE / "external-003" / (ch + "-kotobank.txt")).read_text(encoding="utf8")
        assert "".join(row["boundedQuote"]["text"].split()) in "".join(source_text.split())
    write(PACKET / "authored-source-analysis.json", {
        "base": BASE, "originalSourceBase": "6da1184b82b60553f9b65c57f53289c779f96f7c",
        "members": ANALYSIS, "completeJmdictFamilies": audit["completeJmdictUnion"],
        "completeKanjidicRecords": audit["completeKanjidicRecordsRechecked"],
        "comparisonCopies": 179, "baselineRowsPerMember": 1254, "finitePairRows": 195, "withinBatchPairs": 3,
        "activePairTable": "pair-dispositions-002.json", "activeSourceAudit": "final-source-audit-002.json",
        "activeFontEvidence": "stroke-font-evidence-002.json",
        "fullInputAndOutputBindings": "source-receipt.json, supplemental-source-receipt.json, manual-source-receipt.json and final-source-audit-002.json; initial/supplemental/final per-entry query membership retains mixed predicates.",
        "readCoverage": "All target-containing complete families, full actual supports, all 178 comparison Meaning/Notes/KD-English/complete-exact-family projections and complete manual 川 card/records inspected. Complete machine canonical equality is distinct from manual linguistic reading.",
        "selectionLimit": "皇/桜 split to separate future packets; 伯/憶/撲 remain unresolved. Three local drafts do not advance published 264/1228 or reduce 964 remaining.",
        "resourceAndModelLimit": "Pinned >2GiB admission/<1GiB abort guard; 0.25s sampling, own-child <=0.1s waits and <=10s cleanup stages. Bounded host N1/All/Starter + one target checks only, no arbitrary/multi-borrow/native/device/rendered-font/whole-set/publication claim.",
        "fontWarnings": "All three actual cmaps lack 亍 U+4E8D, 凜 U+51DC, 彳 U+5F73, 衞 U+885E and 韋 U+97CB in the finite taught/comparison scope. Fallback/rendering unverified.",
        "rawExternalEvidence": "Complete six selected raw captures and extracted text remain local with exact bindings; bounded short excerpts and authored analysis only committed. Image omissions and positive secondary branches preserved.",
        "producerSha256": sha(Path(__file__).read_bytes())})
    print(json.dumps({"members": list(ANALYSIS), "sourceAuditSha256": sha((PACKET / "final-source-audit-002.json").read_bytes())}))
finally:
    write(HERE / "source-analysis-memory-001.json", guard.finish())
